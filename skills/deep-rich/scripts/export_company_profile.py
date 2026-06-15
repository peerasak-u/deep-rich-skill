#!/usr/bin/env python3
"""Export a company profile HTML from structured JSON + skill template.

Usage:
    python3 skills/deep-rich/scripts/export_company_profile.py NET
    python3 skills/deep-rich/scripts/export_company_profile.py NET --home /path/to/deep-rich

The script:
1. Resolves the app root (--home, DEEP_RICH_HOME, or sibling ../deep-rich).
2. Reads .deep-rich/companies/<TICKER>.json.
3. Reads the skill template from skills/deep-rich/references/templates/company-profile.html.
4. Maps/escapes all template variables and writes company/<ticker-lower>.html.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from _common import resolve_deep_rich_home


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _resolve_skill_root() -> Path:
    """Locate the skill package root from this script's location."""
    # __file__ = .../deep-rich-skill/skills/deep-rich/scripts/export_company_profile.py
    # parents[3] = deep-rich-skill/
    return Path(__file__).resolve().parents[3]


def _escape(text: str) -> str:
    """HTML-escape a string."""
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


def _fmt_currency(value: float, currency: str = "USD", decimals: int = 2) -> str:
    """Format a dollar amount."""
    symbol = {"USD": "$", "THB": "฿", "EUR": "€", "GBP": "£"}.get(currency, currency + " ")
    fmt = f"{{:,.{decimals}f}}"
    return f"{symbol}{fmt.format(value)}"


def _fmt_large(value: float) -> str:
    """Format large dollar amounts with B/M suffix."""
    if abs(value) >= 1_000_000_000:
        return f"${value / 1_000_000_000:.2f}B"
    if abs(value) >= 1_000_000:
        return f"${value / 1_000_000:.1f}M"
    return f"${value:,.0f}"


def _fmt_pct(value: float, sign: bool = True) -> str:
    """Format a percentage."""
    s = "+" if sign and value > 0 else ""
    return f"{s}{value:.1f}%"


def _li(items: list[str]) -> str:
    """Render list items (no wrapping <ul>; caller provides it)."""
    return "".join(f"<li>{_escape(item)}</li>" for item in items)


def _tag(text: str, long: bool = False) -> str:
    """Render a data tag span."""
    cls = "tag long" if long else "tag"
    return f'<span class="{cls}">{_escape(text)}</span>'


def _logo_html(profile: dict, app_root: Path) -> str:
    """Render the logo tile HTML."""
    logo_path = profile.get("logo", {}).get("path", "")
    ticker = profile.get("ticker", "")
    if logo_path:
        abs_path = app_root / logo_path
        if abs_path.exists():
            rel = f"../../{logo_path}"
            return f'<img src="{rel}" alt="{_escape(ticker)} logo">'
    return _escape(ticker.upper())


def _identity_tags(profile: dict) -> str:
    """Render identity tags as HTML spans."""
    tags = [
        f"{profile.get('exchange', '')}:{profile.get('ticker', '')}",
        profile.get("sector", ""),
        profile.get("industry", ""),
        profile.get("country", ""),
    ]
    parts = []
    for t in tags:
        if t:
            parts.append(_tag(t, long=(len(t) > 20)))
    return "".join(parts)


def _competitors_table(competitors: list[dict]) -> str:
    """Render competitors table HTML."""
    rows = []
    for c in competitors:
        name = _escape(c.get("name", ""))
        ticker = _escape(c.get("ticker", ""))
        adv = _escape(c.get("advantage", ""))
        dis = _escape(c.get("disadvantage", ""))
        rows.append(
            f"<tr><td><strong>{name}</strong><br><small>{ticker}</small></td>"
            f"<td>{adv}</td><td>{dis}</td></tr>"
        )
    return (
        "<table><thead><tr><th>Competitor</th><th>Advantage vs NET</th>"
        f"<th>Disadvantage vs NET</th></tr></thead><tbody>{''.join(rows)}</tbody></table>"
    )


def _risks_catalysts(profile: dict) -> str:
    """Render risks + catalysts side-by-side."""
    return (
        '<div class="grid two">'
        f"<div><h3>Risks</h3>{_li(profile.get('risks', []))}</div>"
        f"<div><h3>Catalysts</h3>{_li(profile.get('catalysts', []))}</div>"
        "</div>"
    )


def _data_quality(profile: dict) -> str:
    """Render data quality boundary section."""
    dq = profile.get("data_quality", {})
    return (
        '<div class="grid three">'
        f"<div><h3>Facts</h3>{_li(dq.get('facts', []))}</div>"
        f"<div><h3>Estimates</h3>{_li(dq.get('estimates', []))}</div>"
        f"<div><h3>Missing / verify</h3>{_li(dq.get('missing_or_to_verify', []))}</div>"
        "</div>"
    )


def _business_flow(profile: dict) -> str:
    """Render the three-node business flow with arrows between nodes."""
    steps = [
        ("Internet traffic", "Apps, APIs, employees, AI workloads"),
        ("Cloudflare edge", "CDN, WAF, DDoS, Zero Trust, Workers"),
        ("Customer outcome", "Faster, safer, simpler connectivity cloud"),
    ]
    parts = []
    for idx, (label, detail) in enumerate(steps):
        parts.append(f'<div class="node"><strong>{_escape(label)}</strong><span>{_escape(detail)}</span></div>')
        if idx < len(steps) - 1:
            parts.append('<div class="arrow">→</div>')
    return "".join(parts)


def _evidence_chart(profile: dict) -> dict:
    """Build the Chart.js radar data from profile."""
    fin = profile.get("financials", {})
    health = fin.get("health_grade", "C")
    health_score_map = {"A": 80, "B": 65, "C": 48, "D": 30, "F": 15}
    health_score = health_score_map.get(health, 48)
    return {
        "labels": ["Value", "Future", "Past", "Health", "Dividend"],
        "values": [42, 82, 76, health_score, 8],
    }


def _evidence_fallback(profile: dict) -> str:
    """Build fallback text for the radar chart."""
    fin = profile.get("financials", {})
    health = fin.get("health_grade", "C")
    health_score_map = {"A": 80, "B": 65, "C": 48, "D": 30, "F": 15}
    hs = health_score_map.get(health, 48)
    return f"Value 42, Future 82, Past 76, Health {hs}, Dividend 8."


def _market_cap_label(profile: dict) -> str:
    """Build a market cap label string."""
    fin = profile.get("financials", {})
    rev = fin.get("fy2025_revenue", 0)
    if rev:
        approx = rev * 40
        if approx >= 1e9:
            return f"Est. Market Cap ~${approx/1e9:.1f}B"
    return "Market Cap N/A"


def _build_vars(profile: dict, app_root: Path) -> dict:
    """Build all template variable substitutions from profile JSON."""
    fin = profile.get("financials", {})
    pos = profile.get("position", {})
    thesis = profile.get("thesis", {})

    ticker = profile.get("ticker", "")
    price = fin.get("price", 0)
    cost = pos.get("cost_basis_usd", 0)
    gain_pct = pos.get("unrealized_gain_pct", 0)
    range_low = fin.get("52w_low", 0)
    range_high = fin.get("52w_high", 0)
    range_pos = fin.get("52w_position", 0)
    health = fin.get("health_grade", "C")
    health_summary = fin.get("health_summary", "Deep Rich health script flags this holding.")
    verdict = thesis.get("verdict", "HOLD")
    verdict_reason = thesis.get("verdict_reason", "")
    suggested_action = thesis.get("suggested_action", "")
    bull = thesis.get("bull_case", [])
    bear = thesis.get("bear_case", [])

    qty = pos.get("quantity", 0)
    position_badge = "Held position" if qty > 0 else "No position"

    evidence = _evidence_chart(profile)

    # Pre-compute values to avoid brace conflicts in multi-line strings
    pos_value_thb = _fmt_currency(pos.get("market_value_thb", 0), "THB")
    pos_value_usd = _fmt_currency(pos.get("market_value_usd", 0))
    fx_rate = pos.get("fx_usd_thb", 0)
    cost_fmt = _fmt_currency(cost)
    gain_fmt = _fmt_pct(gain_pct)
    range_low_fmt = _fmt_currency(range_low)
    range_high_fmt = _fmt_currency(range_high)
    revenue_fmt = _fmt_large(fin.get("fy2025_revenue", 0))
    rev_growth_fmt = _fmt_pct(fin.get("fy2025_revenue_growth_yoy", 0))
    fcf_fmt = _fmt_large(fin.get("free_cash_flow_q1_2026", 0))
    fcf_margin_fmt = _fmt_pct(fin.get("free_cash_flow_margin_q1_2026", 0))
    assets_fmt = _fmt_large(fin.get("latest_assets", 0))
    liab_fmt = _fmt_large(fin.get("latest_liabilities", 0))
    equity_fmt = _fmt_large(fin.get("latest_equity", 0))
    de_ratio = fin.get("debt_equity", 0)
    tam = _escape(profile.get("market", {}).get("tam", "N/A"))
    tam_src = _escape(profile.get("market", {}).get("tam_source", ""))

    rel_profile = f".deep-rich/companies/{ticker}.json"

    return {
        # Top-level scalars
        "{{ticker}}": ticker,
        "{{company_name}}": _escape(profile.get("name", "")),
        "{{updated_at}}": profile.get("meta", {}).get("updated_at", ""),
        "{{profile_source_path}}": rel_profile,
        # Hero
        "{{position_badge}}": position_badge,
        "{{verdict}}": verdict,
        "{{business_description}}": _escape(profile.get("business", {}).get("description", "")),
        "{{logo_html}}": _logo_html(profile, app_root),
        "{{identity_tags_html}}": _identity_tags(profile),
        # Quote card
        "{{current_price}}": _fmt_currency(price),
        "{{gain_pct}}": gain_fmt,
        "{{quantity}}": f"{qty:.4f}",
        "{{range_low}}": range_low_fmt,
        "{{range_high}}": range_high_fmt,
        "{{range_position_pct}}": str(range_pos),
        "{{suggested_action}}": _escape(suggested_action),
        # Profile section
        "{{market_cap_label}}": _market_cap_label(profile),
        "{{evidence_summary}}": _escape(
            "The visual summarizes our current evidence: strong future/story and past growth, "
            "mixed health due to leverage, weak dividend because Cloudflare does not fit an "
            "income-stock profile, and valuation treated as a guardrail rather than a fair-value claim."
        ),
        "{{business_flow_html}}": _business_flow(profile),
        "{{evidence_chart_json}}": json.dumps(evidence),
        "{{evidence_fallback}}": _evidence_fallback(profile),
        # Valuation
        "{{valuation_html}}": (
            '<div class="grid three">'
            f"<dl class=\"metric\"><dt>Position value</dt><dd>{pos_value_thb}</dd>"
            f"<small>{pos_value_usd} at USD/THB {fx_rate:.2f}</small></dl>"
            f"<dl class=\"metric\"><dt>Cost basis</dt><dd>{cost_fmt}</dd><small>Per share</small></dl>"
            f"<dl class=\"metric\"><dt>Unrealized gain</dt><dd class=\"gain\">{gain_fmt}</dd>"
            "<small>Not a sell signal by itself</small></dl>"
            "</div>"
            "<div class=\"callout warning\">Missing before strong add decision: current market cap "
            "verification, P/S or EV/Sales, peer valuation table, and explicit valuation threshold.</div>"
        ),
        # Future growth
        "{{future_growth_html}}": (
            '<div class="grid two">'
            f"<div class=\"metric\"><dt>TAM cited by company</dt><dd>{tam}</dd>"
            f"<small>{tam_src}</small></div>"
            "<div class=\"metric\"><dt>Key growth engine</dt><dd>AI + edge developers</dd>"
            "<small>Workers, AI Gateway, Zero Trust</small></div>"
            "</div>"
        ),
        # Past performance
        "{{past_performance_html}}": (
            "<table>"
            "<thead><tr><th>Metric</th><th>Value</th><th>Read</th></tr></thead><tbody>"
            f"<tr><td>FY2025 revenue</td><td>{revenue_fmt}</td>"
            "<td>Large, still compounding software base</td></tr>"
            f"<tr><td>Revenue growth YoY</td><td>{rev_growth_fmt}</td>"
            "<td>Strong growth</td></tr>"
            f"<tr><td>Q1 2026 free cash flow</td><td>{fcf_fmt}</td>"
            "<td>Cash generation improving</td></tr>"
            f"<tr><td>FCF margin</td><td>{fcf_margin_fmt}</td>"
            "<td>Positive but still maturing</td></tr>"
            "</tbody></table>"
        ),
        # Financial health
        "{{health_summary}}": _escape(health_summary),
        "{{health_grade}}": health,
        "{{health_html}}": (
            '<div class="grid four">'
            f"<dl class=\"metric\"><dt>Assets</dt><dd>{assets_fmt}</dd></dl>"
            f"<dl class=\"metric\"><dt>Liabilities</dt><dd>{liab_fmt}</dd></dl>"
            f"<dl class=\"metric\"><dt>Equity</dt><dd>{equity_fmt}</dd></dl>"
            f"<dl class=\"metric\"><dt>Debt / Equity</dt><dd class=\"loss\">{de_ratio:.2f}x</dd></dl>"
            "</div>"
        ),
        # Thesis
        "{{verdict_reason}}": _escape(verdict_reason),
        "{{bull_case_html}}": _li(bull),
        "{{bear_case_html}}": _li(bear),
        # Risks + competitors
        "{{risks_catalysts_html}}": _risks_catalysts(profile),
        "{{competitors_table_html}}": _competitors_table(profile.get("competitors", [])),
        # Data quality
        "{{data_quality_html}}": _data_quality(profile),
        # Footer
        "{{footer_note}}": (
            "Data from Deep Rich local portfolio tools and public company releases. "
            "Refresh prices before using in review; refresh this profile after earnings or when older than 7 days."
        ),
    }


def _sub_all(template: str, vars_map: dict) -> str:
    """Apply all substitutions to the template."""
    result = template
    for key, value in vars_map.items():
        result = result.replace(key, str(value))
    return result


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="Export company profile HTML from JSON + template.")
    parser.add_argument("ticker", help="Stock ticker symbol (e.g. NET)")
    parser.add_argument(
        "--home",
        help="Deep Rich app root (overrides auto-discovery via resolve_deep_rich_home)",
    )
    args = parser.parse_args()

    ticker = args.ticker.upper()
    app_root = resolve_deep_rich_home(args.home)
    skill_root = _resolve_skill_root()

    json_path = app_root / ".deep-rich" / "companies" / f"{ticker}.json"
    if not json_path.exists():
        json_path = app_root / ".deep-rich" / "companies" / f"{ticker.upper()}.json"
    if not json_path.exists():
        print(f"[error] Not found: {json_path}", file=sys.stderr)
        return 1

    with open(json_path) as f:
        profile = json.load(f)

    template_path = (
        skill_root
        / "skills"
        / "deep-rich"
        / "references"
        / "templates"
        / "company-profile.html"
    )
    if not template_path.exists():
        print(f"[error] Template not found: {template_path}", file=sys.stderr)
        return 1

    with open(template_path) as f:
        template = f.read()

    vars_map = _build_vars(profile, app_root)
    html = _sub_all(template, vars_map)

    out_dir = app_root / "company"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / f"{ticker.lower()}.html"
    with open(out_path, "w") as f:
        f.write(html)

    print(f"[ok] Wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
