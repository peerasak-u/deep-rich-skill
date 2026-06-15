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


def _fmt_large(value: float, currency: str = "USD") -> str:
    """Format large amounts with B/M suffix."""
    symbol = {"USD": "$", "THB": "฿", "EUR": "€", "GBP": "£"}.get(currency, currency + " ")
    if abs(value) >= 1_000_000_000:
        return f"{symbol}{value / 1_000_000_000:.2f}B"
    if abs(value) >= 1_000_000:
        return f"{symbol}{value / 1_000_000:.1f}M"
    return f"{symbol}{value:,.0f}"


def _profile_currency(fin: dict) -> str:
    return fin.get("currency", "USD")


def _growth_read(pct: float) -> str:
    if pct > 15:
        return "Strong growth"
    if pct > 0:
        return "Moderate growth"
    if pct > -10:
        return "Slight decline"
    return "Material decline"


def _normalize_list_items(items: list) -> list[str]:
    """Accept plain strings or dict rows from heterogeneous company JSON."""
    out: list[str] = []
    for item in items:
        if isinstance(item, str):
            out.append(item)
        elif isinstance(item, dict):
            out.append(
                item.get("risk")
                or item.get("catalyst")
                or item.get("text")
                or item.get("description")
                or item.get("summary")
                or ""
            )
    return [x for x in out if x]


def _revenue_growth_yoy(fin: dict) -> float | None:
    for key in ("fy2025_revenue_growth_yoy", "revenue_growth_yoy", "revenue_growth_yoy_2025"):
        if key in fin:
            return fin[key]
    return None


def _fmt_revenue(fin: dict) -> str | None:
    currency = _profile_currency(fin)
    if fin.get("fy2025_revenue"):
        return _fmt_large(fin["fy2025_revenue"], currency)
    if fin.get("revenue_fy2025_m_thb"):
        return f"฿{fin['revenue_fy2025_m_thb']:,.0f}M"
    if fin.get("revenue_2025"):
        return f"฿{fin['revenue_2025']:,.0f}M"
    return None


def _cost_per_share(pos: dict, fin: dict, qty: float) -> tuple[float, str]:
    currency = _profile_currency(fin)
    if currency == "THB":
        cost = pos.get("cost_per_share") or pos.get("cost_basis_thb", 0)
        if qty and cost > 1000:
            cost = pos.get("cost_per_share") or (pos.get("cost_basis_thb", 0) / qty)
        return cost, "THB"
    cost = pos.get("cost_basis_usd") or pos.get("cost_per_share", 0)
    return cost, "USD"


def _position_gain_pct(pos: dict) -> float:
    return pos.get("unrealized_gain_pct", pos.get("gain_loss_pct", 0)) or 0


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


def _competitors_table(competitors: list[dict], ticker: str) -> str:
    """Render competitors table HTML."""
    rows = []
    for c in competitors:
        name = _escape(c.get("name", ""))
        comp_ticker = _escape(c.get("ticker", ""))
        adv = _escape(c.get("advantage", ""))
        dis = _escape(c.get("disadvantage", ""))
        rows.append(
            f"<tr><td><strong>{name}</strong><br><small>{comp_ticker}</small></td>"
            f"<td>{adv}</td><td>{dis}</td></tr>"
        )
    return (
        f"<table><thead><tr><th>Competitor</th><th>Advantage vs {ticker}</th>"
        f"<th>Disadvantage vs {ticker}</th></tr></thead><tbody>{''.join(rows)}</tbody></table>"
    )


def _risks_catalysts(profile: dict) -> str:
    """Render risks + catalysts side-by-side."""
    return (
        '<div class="grid two">'
        f"<div><h3>Risks</h3>{_li(_normalize_list_items(profile.get('risks', [])))}</div>"
        f"<div><h3>Catalysts</h3>{_li(_normalize_list_items(profile.get('catalysts', [])))}</div>"
        "</div>"
    )


def _data_quality(profile: dict) -> str:
    """Render data quality boundary section."""
    dq = profile.get("data_quality", {})
    missing = dq.get("missing_or_to_verify") or dq.get("unknowns", [])
    return (
        '<div class="grid three">'
        f"<div><h3>Facts</h3>{_li(dq.get('facts', []))}</div>"
        f"<div><h3>Estimates</h3>{_li(dq.get('estimates', []))}</div>"
        f"<div><h3>Missing / verify</h3>{_li(missing)}</div>"
        "</div>"
    )


def _business_flow(profile: dict) -> str:
    """Render the three-node business flow from profile fields."""
    business = profile.get("business", {})
    segments = business.get("revenue_segments", [])
    products = business.get("products", [])
    pipeline = profile.get("pipeline", [])

    steps: list[tuple[str, str]] = []
    if segments:
        detail = segments[1] if len(segments) > 1 else (products[0] if products else "")
        steps.append((segments[0], detail))
    if pipeline:
        item = pipeline[0]
        steps.append((item.get("name", "Pipeline"), item.get("target_market", item.get("notes", ""))))
    elif len(products) >= 2:
        steps.append((products[0], products[1]))
    if business.get("moat"):
        steps.append(("Competitive position", business["moat"][:120]))
    elif len(segments) > 1:
        steps.append(("Revenue mix", segments[-1]))

    if len(steps) < 2:
        desc = business.get("description", "See profile")
        steps = [
            ("Core business", desc[:100]),
            (
                "Products / services",
                ", ".join(products[:2]) if products else (segments[0] if segments else "See IR"),
            ),
            ("Market", profile.get("market", {}).get("tam", "See thesis")[:100]),
        ]

    parts = []
    for idx, (label, detail) in enumerate(steps[:3]):
        parts.append(f'<div class="node"><strong>{_escape(label)}</strong><span>{_escape(detail)}</span></div>')
        if idx < min(len(steps), 3) - 1:
            parts.append('<div class="arrow">→</div>')
    return "".join(parts)


def _health_score(fin: dict) -> int:
    health = fin.get("health_grade", "C")
    health_score_map = {"A": 80, "B": 65, "C": 48, "D": 30, "F": 15}
    return health_score_map.get(health, 48)


def _dividend_score(profile: dict) -> int:
    fin = profile.get("financials", {})
    val = profile.get("valuation", {})
    div_yield = val.get("dividend_yield_pct") or fin.get("dividend_yield_2025") or 0
    return min(90, int(div_yield * 10)) if div_yield else 8


def _past_score(fin: dict) -> int:
    growth = _revenue_growth_yoy(fin)
    if growth is None:
        return 48
    if growth > 15:
        return 76
    if growth > 0:
        return 55
    if growth > -10:
        return 40
    return 25


def _evidence_chart(profile: dict) -> dict:
    """Build the Chart.js radar data from profile."""
    fin = profile.get("financials", {})
    return {
        "labels": ["Value", "Future", "Past", "Health", "Dividend"],
        "values": [42, 82, _past_score(fin), _health_score(fin), _dividend_score(profile)],
    }


def _evidence_fallback(profile: dict) -> str:
    """Build fallback text for the radar chart."""
    chart = _evidence_chart(profile)
    vals = chart["values"]
    return f"Value {vals[0]}, Future {vals[1]}, Past {vals[2]}, Health {vals[3]}, Dividend {vals[4]}."


def _evidence_summary(profile: dict) -> str:
    fin = profile.get("financials", {})
    val = profile.get("valuation", {})
    health = fin.get("health_grade", "C")
    div_yield = val.get("dividend_yield_pct") or fin.get("dividend_yield_2025")
    if div_yield and div_yield >= 3:
        div_clause = f"meaningful dividend angle (~{div_yield:.1f}% yield),"
    else:
        div_clause = "limited dividend profile,"
    return (
        "The visual summarizes our current evidence: "
        f"{div_clause} health grade {health}, "
        "and valuation treated as a guardrail rather than a fair-value claim."
    )


def _market_cap_label(profile: dict) -> str:
    """Build a market cap label string."""
    fin = profile.get("financials", {})
    currency = _profile_currency(fin)
    if fin.get("market_cap"):
        unit = fin.get("market_cap_unit", "M THB")
        if "THB" in unit:
            return f"Market Cap ฿{fin['market_cap']:,.0f}M"
        return f"Market Cap {_fmt_large(fin['market_cap'] * 1_000_000, currency)}"
    rev = fin.get("fy2025_revenue", 0)
    if rev:
        approx = rev * 40
        if approx >= 1e9:
            return f"Est. Market Cap ~{_fmt_large(approx, currency)}"
    return "Market Cap N/A"


def _past_performance_rows(fin: dict) -> list[tuple[str, str, str]]:
    currency = _profile_currency(fin)
    rows: list[tuple[str, str, str]] = []
    growth = _revenue_growth_yoy(fin)
    revenue_fmt = _fmt_revenue(fin)
    if revenue_fmt:
        rows.append(("FY2025 revenue", revenue_fmt, _growth_read(growth or 0)))
    if growth is not None:
        rows.append(("Revenue growth YoY", _fmt_pct(growth), _growth_read(growth)))

    if fin.get("free_cash_flow_q1_2026") is not None:
        fcf = fin["free_cash_flow_q1_2026"]
        rows.append(
            (
                "Q1 2026 free cash flow",
                _fmt_large(fcf, currency),
                "Cash generation improving" if fcf > 0 else "Cash burn",
            )
        )
        if fin.get("free_cash_flow_margin_q1_2026") is not None:
            margin = fin["free_cash_flow_margin_q1_2026"]
            rows.append(
                (
                    "FCF margin",
                    _fmt_pct(margin),
                    "Positive but still maturing" if margin > 0 else "Negative",
                )
            )
    elif fin.get("net_profit_fy2025_m_thb") is not None:
        np_growth = fin.get("net_profit_growth_yoy")
        rows.append(
            (
                "FY2025 net profit",
                f"฿{fin['net_profit_fy2025_m_thb']:,.0f}M",
                _growth_read(np_growth or 0) if np_growth is not None else "Reported net profit",
            )
        )
        if np_growth is not None:
            rows.append(("Net profit growth YoY", _fmt_pct(np_growth), _growth_read(np_growth)))
        elif fin.get("ebitda_margin_fy2025_pct") is not None:
            rows.append(
                (
                    "EBITDA margin FY2025",
                    _fmt_pct(fin["ebitda_margin_fy2025_pct"], sign=False),
                    "Margin context for cyclical earnings",
                )
            )
    elif fin.get("net_income_2025") is not None:
        rows.append(("FY2025 net income", f"฿{fin['net_income_2025']:,.0f}M", "Reported net income"))

    return rows[:4]


def _past_performance_html(fin: dict) -> str:
    rows = _past_performance_rows(fin)
    body = "".join(f"<tr><td>{label}</td><td>{value}</td><td>{read}</td></tr>" for label, value, read in rows)
    return (
        "<table><thead><tr><th>Metric</th><th>Value</th><th>Read</th></tr></thead><tbody>"
        f"{body}</tbody></table>"
    )


def _health_metrics(fin: dict) -> list[tuple[str, str, str | None]]:
    currency = _profile_currency(fin)
    metrics: list[tuple[str, str, str | None]] = []
    de_metric: tuple[str, str, str | None] | None = None

    if fin.get("latest_assets") is not None:
        metrics.append(("Assets", _fmt_large(fin["latest_assets"], currency), None))
    if fin.get("latest_liabilities") is not None:
        metrics.append(("Liabilities", _fmt_large(fin["latest_liabilities"], currency), None))
    if fin.get("latest_equity") is not None:
        metrics.append(("Equity", _fmt_large(fin["latest_equity"], currency), None))

    if not metrics:
        for label, key in (
            ("ROE FY2025", "roe_fy2025_pct"),
            ("ROE FY2025", "roe_2025"),
            ("EBITDA margin", "ebitda_margin_fy2025_pct"),
            ("Gross margin FY2025", "gross_margin_fy2025_pct"),
            ("Net margin FY2025", "net_margin_fy2025_pct"),
        ):
            if fin.get(key) is not None and not any(m[0] == label for m in metrics):
                metrics.append((label, _fmt_pct(fin[key], sign=False), None))

    if fin.get("debt_equity") is not None:
        de = fin["debt_equity"]
        css = "loss" if de > 1.5 else None
        de_metric = ("Debt / Equity", f"{de:.2f}x", css)

    if de_metric:
        metrics = (metrics[:3] + [de_metric]) if len(metrics) >= 3 else metrics + [de_metric]

    return metrics[:4]


def _health_html(fin: dict) -> str:
    metrics = _health_metrics(fin)
    parts = []
    for label, value, css in metrics:
        cls = f' class="{css}"' if css else ""
        parts.append(f'<dl class="metric"><dt>{label}</dt><dd{cls}>{value}</dd></dl>')
    return f'<div class="grid four">{"".join(parts)}</div>'


def _future_growth_html(profile: dict) -> str:
    market = profile.get("market", {})
    drivers = market.get("growth_drivers", [])
    tam = _escape(market.get("tam", "N/A"))
    tam_src = _escape(market.get("tam_source", ""))
    key_engine = _escape(drivers[0] if drivers else "See company IR")
    key_detail = _escape(", ".join(drivers[1:3]) if len(drivers) > 1 else (market.get("trends", [""])[0]))
    return (
        '<div class="grid two">'
        f'<div class="metric"><dt>TAM cited by company</dt><dd>{tam}</dd><small>{tam_src}</small></div>'
        f'<div class="metric"><dt>Key growth engine</dt><dd>{key_engine}</dd><small>{key_detail}</small></div>'
        "</div>"
    )


def _build_vars(profile: dict, app_root: Path) -> dict:
    """Build all template variable substitutions from profile JSON."""
    fin = profile.get("financials", {})
    pos = profile.get("position", {})
    thesis = profile.get("thesis", {})

    ticker = profile.get("ticker", "")
    currency = _profile_currency(fin)
    price = fin.get("price", 0)
    gain_pct = _position_gain_pct(pos)
    range_low = fin.get("52w_low", 0)
    range_high = fin.get("52w_high", 0)
    range_pos = fin.get("52w_position", 0)
    health = fin.get("health_grade", "C")
    health_summary = fin.get("health_summary") or fin.get("health_note") or "Deep Rich health script flags this holding."
    verdict = thesis.get("verdict", "HOLD")
    verdict_reason = thesis.get("verdict_reason", "")
    suggested_action = thesis.get("suggested_action", "")
    bull = thesis.get("bull_case", [])
    bear = thesis.get("bear_case", [])

    qty = pos.get("quantity", 0)
    position_badge = "Held position" if qty > 0 else "No position"

    evidence = _evidence_chart(profile)
    cost, cost_currency = _cost_per_share(pos, fin, qty)
    gain_class = "gain" if gain_pct >= 0 else "loss"

    pos_value_thb = _fmt_currency(pos.get("market_value_thb", 0), "THB")
    pos_value_usd = pos.get("market_value_usd", 0)
    fx_rate = pos.get("fx_usd_thb") or pos.get("fx_rate", 0)
    if pos_value_usd and fx_rate:
        fx_line = f"{_fmt_currency(pos_value_usd)} at USD/THB {fx_rate:.2f}"
    else:
        fx_line = "THB position — no USD conversion in profile"

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
        "{{current_price}}": _fmt_currency(price, currency),
        "{{gain_pct}}": _fmt_pct(gain_pct),
        "{{quantity}}": f"{qty:.4f}",
        "{{range_low}}": _fmt_currency(range_low, currency),
        "{{range_high}}": _fmt_currency(range_high, currency),
        "{{range_position_pct}}": str(range_pos),
        "{{suggested_action}}": _escape(suggested_action),
        # Profile section
        "{{market_cap_label}}": _market_cap_label(profile),
        "{{evidence_summary}}": _escape(_evidence_summary(profile)),
        "{{business_flow_html}}": _business_flow(profile),
        "{{evidence_chart_json}}": json.dumps(evidence),
        "{{evidence_fallback}}": _evidence_fallback(profile),
        # Valuation
        "{{valuation_html}}": (
            '<div class="grid three">'
            f"<dl class=\"metric\"><dt>Position value</dt><dd>{pos_value_thb}</dd>"
            f"<small>{fx_line}</small></dl>"
            f"<dl class=\"metric\"><dt>Cost basis</dt><dd>{_fmt_currency(cost, cost_currency)}</dd>"
            "<small>Per share</small></dl>"
            f"<dl class=\"metric\"><dt>Unrealized gain</dt><dd class=\"{gain_class}\">{_fmt_pct(gain_pct)}</dd>"
            "<small>Not a sell signal by itself</small></dl>"
            "</div>"
            "<div class=\"callout warning\">Missing before strong add decision: current market cap "
            "verification, P/S or EV/Sales, peer valuation table, and explicit valuation threshold.</div>"
        ),
        # Future growth
        "{{future_growth_html}}": _future_growth_html(profile),
        # Past performance
        "{{past_performance_html}}": _past_performance_html(fin),
        # Financial health
        "{{health_summary}}": _escape(health_summary),
        "{{health_grade}}": health,
        "{{health_html}}": _health_html(fin),
        # Thesis
        "{{verdict_reason}}": _escape(verdict_reason),
        "{{bull_case_html}}": _li(bull),
        "{{bear_case_html}}": _li(bear),
        # Risks + competitors
        "{{risks_catalysts_html}}": _risks_catalysts(profile),
        "{{competitors_table_html}}": _competitors_table(profile.get("competitors", []), ticker),
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
