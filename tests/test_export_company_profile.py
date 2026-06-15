from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "deep-rich" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from export_company_profile import (  # noqa: E402
    _build_vars,
    _business_flow,
    _competitors_table,
    _data_quality,
    _past_performance_html,
    _sub_all,
)

TEMPLATE = "<price>{{current_price}}</price><past>{{past_performance_html}}</past>"


THB_PROFILE = {
    "ticker": "TASCO",
    "name": "Tipco Asphalt Public Company Limited",
    "exchange": "SET",
    "sector": "Materials",
    "industry": "Asphalt",
    "country": "Thailand",
    "business": {
        "description": "Thai asphalt manufacturer.",
        "revenue_segments": ["Asphalt sales and service", "Construction business"],
        "products": ["Asphalt cement", "Road paving materials"],
        "moat": "Regional distribution network.",
    },
    "market": {
        "tam": "Thailand road construction demand",
        "tam_source": "Company IR",
        "growth_drivers": [
            "Thai government infrastructure budgets",
            "Export recovery if oversupply eases",
        ],
        "trends": ["Margin compression in 4Q25"],
    },
    "pipeline": [
        {
            "name": "Construction backlog",
            "target_market": "Thailand road construction",
            "notes": "THB 6.6B backlog",
        }
    ],
    "competitors": [
        {
            "name": "IRPC",
            "ticker": "IRPC",
            "advantage": "Integrated refinery scale",
            "disadvantage": "Less asphalt focus",
        }
    ],
    "financials": {
        "price": 14.0,
        "currency": "THB",
        "52w_low": 12.4,
        "52w_high": 15.7,
        "revenue_fy2025_m_thb": 26962,
        "revenue_growth_yoy": -3.6,
        "net_profit_fy2025_m_thb": 1137,
        "net_profit_growth_yoy": -19.8,
        "roe_fy2025_pct": 7.4,
        "ebitda_margin_fy2025_pct": 7.6,
        "debt_equity": 0.3,
        "health_grade": "D",
    },
    "valuation": {"dividend_yield_pct": 7.25},
    "position": {
        "quantity": 1000,
        "cost_basis_thb": 16.13,
        "market_value_thb": 14000,
        "unrealized_gain_pct": -13.2,
    },
    "thesis": {"verdict": "HOLD/WATCH", "bull_case": [], "bear_case": []},
    "risks": ["Cyclical margins"],
    "catalysts": ["Road spending"],
    "data_quality": {
        "facts": ["Price THB 14.00"],
        "estimates": ["2026 recovery"],
        "unknowns": ["Full 56-1 history"],
    },
    "meta": {"updated_at": "2026-06-15"},
}


USD_PROFILE = {
    "ticker": "NET",
    "name": "Cloudflare, Inc.",
    "business": {
        "description": "Connectivity cloud.",
        "revenue_segments": ["Cloud services"],
        "products": ["CDN", "Zero Trust"],
    },
    "market": {
        "tam": "$196B opportunity",
        "growth_drivers": ["Zero Trust adoption", "Edge compute"],
    },
    "competitors": [],
    "financials": {
        "price": 228.48,
        "currency": "USD",
        "52w_low": 158.83,
        "52w_high": 276.81,
        "fy2025_revenue": 2_167_900_000,
        "fy2025_revenue_growth_yoy": 29.8,
        "free_cash_flow_q1_2026": 84_100_000,
        "free_cash_flow_margin_q1_2026": 13.0,
        "latest_assets": 6_200_000_000,
        "latest_liabilities": 4_600_000_000,
        "latest_equity": 1_500_000_000,
        "debt_equity": 3.04,
        "health_grade": "C",
    },
    "position": {
        "quantity": 3.87,
        "cost_basis_usd": 192.10,
        "market_value_thb": 28902.58,
        "market_value_usd": 884.95,
        "fx_usd_thb": 32.66,
        "unrealized_gain_pct": 18.9,
    },
    "thesis": {"verdict": "HOLD", "bull_case": [], "bear_case": []},
    "risks": [],
    "catalysts": [],
    "data_quality": {"facts": [], "estimates": [], "missing_or_to_verify": ["P/S"]},
    "meta": {"updated_at": "2026-06-15"},
}


@pytest.fixture
def app_root(tmp_path: Path) -> Path:
    home = tmp_path / "deep-rich"
    (home / "scripts").mkdir(parents=True)
    (home / ".deep-rich").mkdir()
    (home / "scripts" / "dr.py").write_text("# stub")
    return home


def test_thb_profile_maps_revenue_and_price(app_root: Path):
    vars_map = _build_vars(THB_PROFILE, app_root)

    assert vars_map["{{current_price}}"] == "฿14.00"
    assert "฿26,962M" in vars_map["{{past_performance_html}}"]
    assert "$0" not in vars_map["{{past_performance_html}}"]
    assert "฿16.13" in vars_map["{{valuation_html}}"]
    assert "Cloudflare" not in vars_map["{{future_growth_html}}"]
    assert "Thai government infrastructure budgets" in vars_map["{{future_growth_html}}"]


def test_usd_profile_still_maps_net_schema(app_root: Path):
    vars_map = _build_vars(USD_PROFILE, app_root)

    assert vars_map["{{current_price}}"] == "$228.48"
    assert "$2.17B" in vars_map["{{past_performance_html}}"]
    assert "+29.8%" in vars_map["{{past_performance_html}}"]
    assert "$84.1M" in vars_map["{{past_performance_html}}"]
    assert "$6.20B" in vars_map["{{health_html}}"]
    assert "$192.10" in vars_map["{{valuation_html}}"]


def test_business_flow_comes_from_profile_not_hardcoded_template():
    flow = _business_flow(THB_PROFILE)

    assert "Asphalt sales and service" in flow
    assert "Construction backlog" in flow
    assert "Cloudflare edge" not in flow


def test_competitors_table_uses_profile_ticker():
    table = _competitors_table(THB_PROFILE["competitors"], "TASCO")

    assert "Advantage vs TASCO" in table
    assert "Advantage vs NET" not in table


def test_data_quality_accepts_unknowns_alias():
    html = _data_quality(THB_PROFILE)

    assert "Full 56-1 history" in html


def test_export_substitutes_template_vars(app_root: Path):
    vars_map = _build_vars(THB_PROFILE, app_root)
    html = _sub_all(TEMPLATE, vars_map)

    assert "<price>฿14.00</price>" in html
    assert "฿26,962M" in html


def test_past_performance_read_reflects_decline():
    html = _past_performance_html(THB_PROFILE["financials"])

    assert "Material decline" in html
    assert "฿1,137M" in html