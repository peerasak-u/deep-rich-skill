#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""
Deep Rich Signals — context-aware suggestions for portfolio actions.

Reads the portfolio manager app's `.deep-rich/` JSON files and calls the app's
`dr.py` calculation path. This script belongs to the skill repo; private data
stays in the portfolio manager repo resolved by --home or DEEP_RICH_HOME.

Usage:
    uv run skills/deep-rich/scripts/signals.py --home /path/to/deep-rich
    uv run skills/deep-rich/scripts/signals.py --json
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

from _common import resolve_deep_rich_home

EMERGENCY_FLOOR_THB = 300_000
STALE_HOURS = 24
DRIFT_WARNING = 5.0
DRIFT_CRITICAL = 15.0


def load_json(path: Path) -> dict:
    with path.open() as f:
        return json.load(f)


def import_calculate_portfolio(home: Path):
    scripts_dir = str(home / "scripts")
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    from dr import calculate_portfolio  # type: ignore

    return calculate_portfolio


def check_price_staleness(home: Path) -> dict:
    """Check if prices are older than STALE_HOURS."""
    prices_path = home / ".deep-rich" / "prices.json"
    if not prices_path.exists():
        return {"status": "no_prices", "message": "Prices file not found. Run `python3 scripts/dr.py prices`."}

    prices_data = load_json(prices_path)
    updated_at = prices_data.get("updated_at", "")

    if not updated_at:
        return {"status": "no_timestamp", "message": "No timestamp in prices.json. Run `python3 scripts/dr.py prices`."}

    try:
        updated = datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
        if updated.tzinfo is None:
            updated = updated.replace(tzinfo=UTC)
    except Exception:
        return {"status": "parse_error", "message": "Cannot parse timestamp. Run `python3 scripts/dr.py prices`."}

    cutoff = datetime.now(UTC) - timedelta(hours=STALE_HOURS)
    age_hours = (datetime.now(UTC) - updated).total_seconds() / 3600

    if updated < cutoff:
        return {
            "status": "stale",
            "message": f"Prices are {age_hours:.0f}h old (>{STALE_HOURS}h). Run `python3 scripts/dr.py prices`.",
            "updated_at": updated_at,
            "age_hours": round(age_hours, 1),
        }

    return {
        "status": "ok",
        "message": f"All prices are fresh ({age_hours:.0f}h old).",
        "updated_at": updated_at,
        "age_hours": round(age_hours, 1),
    }


def check_drift(home: Path) -> list[dict]:
    """Check asset class drift from the app's canonical calculation path."""
    calculate_portfolio = import_calculate_portfolio(home)
    data = calculate_portfolio()
    alerts = []

    for name, info in data["classes"].items():
        if name in ("Cash", "Gold"):
            continue

        abs_drift = abs(info["drift"])
        if abs_drift >= DRIFT_CRITICAL:
            severity = "critical"
        elif abs_drift >= DRIFT_WARNING:
            severity = "warning"
        else:
            continue

        alerts.append(
            {
                "asset_class": name,
                "current_pct": info["pct"],
                "target_pct": info["target_pct"],
                "drift": info["drift"],
                "severity": severity,
                "message": f"{name}: {info['pct']:.1f}% vs {info['target_pct']:.1f}% target (drift {info['drift']:+.1f}%)",
            }
        )

    return sorted(alerts, key=lambda x: abs(x["drift"]), reverse=True)


def check_emergency_floor(home: Path) -> dict | None:
    """Check if cash is above emergency floor."""
    portfolio_path = home / ".deep-rich" / "portfolio.json"
    if not portfolio_path.exists():
        return None

    calculate_portfolio = import_calculate_portfolio(home)
    data = calculate_portfolio()
    cash_value = data["classes"].get("Cash", {}).get("value_thb", 0)
    floor = data.get("emergency_floor_thb", EMERGENCY_FLOOR_THB)

    if cash_value < floor:
        return {
            "status": "critical",
            "message": f"Cash (฿{cash_value:,.0f}) is BELOW emergency floor (฿{floor:,.0f}). Do not deploy.",
            "cash": cash_value,
            "floor": floor,
        }
    if cash_value < floor * 1.2:
        return {
            "status": "warning",
            "message": f"Cash (฿{cash_value:,.0f}) is near emergency floor (฿{floor:,.0f}). Deploy cautiously.",
            "cash": cash_value,
            "floor": floor,
        }

    return {
        "status": "ok",
        "message": f"Cash (฿{cash_value:,.0f}) is well above emergency floor (฿{floor:,.0f}).",
        "cash": cash_value,
        "floor": floor,
    }


def suggest_actions(signals: dict) -> list[dict]:
    """Generate recommended actions from signals."""
    actions = []

    if signals["prices"]["status"] in ("stale", "no_prices", "no_timestamp", "parse_error"):
        actions.append(
            {
                "priority": "high",
                "action": "python3 scripts/dr.py prices",
                "reason": "Prices need refreshing before any portfolio analysis",
            }
        )

    critical_drift = [d for d in signals["drift"] if d["severity"] == "critical"]
    warning_drift = [d for d in signals["drift"] if d["severity"] == "warning"]

    if critical_drift:
        actions.append(
            {
                "priority": "high",
                "action": "python3 scripts/dr.py deployment",
                "reason": f"Critical drift in {', '.join(d['asset_class'] for d in critical_drift)}. Check deployment plan.",
            }
        )

    if warning_drift:
        actions.append(
            {
                "priority": "medium",
                "action": "python3 scripts/dr.py deployment",
                "reason": f"Drift warning in {', '.join(d['asset_class'] for d in warning_drift)}.",
            }
        )

    floor = signals["emergency_floor"]
    if floor and floor["status"] == "critical":
        actions.append(
            {
                "priority": "critical",
                "action": "Review cash position",
                "reason": floor["message"],
            }
        )

    if not actions:
        actions.append(
            {
                "priority": "low",
                "action": "python3 scripts/dr.py health watchlist",
                "reason": "Portfolio looks healthy. Run health scan to check individual holdings.",
            }
        )

    return actions


def build_signals(home: Path) -> dict:
    signals = {
        "prices": check_price_staleness(home),
        "drift": check_drift(home),
        "emergency_floor": check_emergency_floor(home),
    }
    signals["actions"] = suggest_actions(signals)
    return signals


def print_human(signals: dict) -> None:
    print("=" * 60)
    print("  📡 Deep Rich Signals")
    print("=" * 60)

    prices = signals["prices"]
    icon = {"ok": "✅", "stale": "⚠️", "no_prices": "❌", "no_timestamp": "❌", "parse_error": "❌"}.get(
        prices["status"], "❓"
    )
    print(f"\n  {icon} Prices: {prices['message']}")

    emergency_floor = signals["emergency_floor"]
    if emergency_floor:
        icon = {"ok": "✅", "warning": "⚠️", "critical": "🚨"}.get(emergency_floor["status"], "❓")
        print(f"  {icon} Cash: {emergency_floor['message']}")

    if signals["drift"]:
        print("\n  📊 Drift Alerts:")
        for drift in signals["drift"]:
            icon = "🔴" if drift["severity"] == "critical" else "🟡"
            print(f"    {icon} {drift['message']}")
    else:
        print("\n  📊 Drift: No significant drift detected")

    print("\n  🎯 Recommended Actions:")
    for action in signals["actions"]:
        icon = {"critical": "🚨", "high": "🔴", "medium": "🟡", "low": "🟢"}.get(action["priority"], "⚪")
        print(f"    {icon} {action['action']}")
        print(f"       {action['reason']}")
    print()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--home", help="Explicit Deep Rich app root")
    parser.add_argument("--json", action="store_true", help="Print machine-readable output")
    args = parser.parse_args()

    try:
        home = resolve_deep_rich_home(args.home)
        signals = build_signals(home)
    except Exception as exc:
        if args.json:
            print(json.dumps({"ok": False, "error": str(exc)}, indent=2))
        else:
            print(f"Deep Rich signals failed: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps({"ok": True, "deep_rich_home": str(home), "signals": signals}, indent=2))
    else:
        print_human(signals)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
