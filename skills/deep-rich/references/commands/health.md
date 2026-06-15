# health

Quantitative health score for a company — grades business quality on revenue growth, earnings, margins, FCF, and debt.

## Usage

```bash
python3 scripts/dr.py health <SYMBOL>
python3 scripts/dr.py health watchlist
python3 scripts/health.py <SYMBOL> [--json]
```

## Examples

```bash
# Single stock health check
python3 scripts/dr.py health MSFT
python3 scripts/dr.py health NVDA

# Portfolio-wide health scan
python3 scripts/dr.py health watchlist

# JSON output
python3 scripts/health.py MSFT --json
```

## Health Grades

| Grade | Score | Meaning |
|-------|-------|---------|
| 🟢 A | 80%+ | Excellent — strong growth, healthy margins, low debt |
| 🔵 B | 65-79% | Good — solid fundamentals with minor concerns |
| 🟡 C | 50-64% | Concerning — mixed signals, needs monitoring |
| 🟠 D | 35-49% | Warning — significant issues detected |
| 🔴 F | <35% | Critical — major problems, review immediately |

## Scoring Components

| Component | Weight | What It Measures |
|-----------|--------|------------------|
| Revenue Growth | 25% | YoY growth rate and CAGR |
| Earnings Growth | 25% | Net income growth vs revenue growth |
| Margin Trend | 20% | Net margin expanding or compressing |
| FCF Growth | 15% | Free cash flow trajectory |
| Debt/Equity | 15% | Balance sheet leverage |

## Output Example (US Stock)

```
══════════════════════════════════════════════════════════════════════
  🏥 MSFT — Health Score: 🔵 B
  Asset Class: US Market
══════════════════════════════════════════════════════════════════════

  Price:          416.67
  1Y Return:      🔴 -17.8%
  3Y Return:      🟢 +8.3% (annualized)

  ── Revenue Growth ───────────────────────────────────────────────
  YoY:            🟢 +14.9%
  CAGR (6yr):     +14.5%
  Trend:          ➡️ Stable

  ── Earnings Growth ──────────────────────────────────────────────
  YoY:            🟢 +15.5%
  CAGR (6yr):     +18.1%
  Trend:          📉 Decelerating

  ── Net Margin Trend ─────────────────────────────────────────────
  2022:     36.7%  ██████████████████
  2023:     34.1%  █████████████████
  2024:     36.0%  ██████████████████
  2025:     36.1%  ██████████████████

  ── Free Cash Flow ───────────────────────────────────────────────
  YoY:            🔴 -3.3%
  CAGR (6yr):     +9.6%

  ── Financial Health ──────────────────────────────────────────────
  Debt/Equity:    0.68x 🟢 Conservative

  ── Signals ──────────────────────────────────────────────────────
  ✅ Strong revenue growth (+14.9%)

══════════════════════════════════════════════════════════════════════
```

## Watchlist Mode

```bash
python3 scripts/dr.py health watchlist
```

Runs health check on all portfolio holdings and shows summary table:

```
══════════════════════════════════════════════════════════════════════
  📋 Portfolio Health Watchlist
══════════════════════════════════════════════════════════════════════

  Symbol   Class        Grade    1Y Ret   Rev Growth Warnings
  ──────── ──────────── ────── ──────── ──────────── ──────────────────────────────
  AAI      Thai SET     🔴 F      -26.9%            — Weak 1Y price return (-26.9%)
  KBANK    Thai SET     🟡 C      +19.3%            — —
  MSFT     US Market    🔵 B      -17.8%       +14.9% —
  NVDA     US Market    🟢 A      +17.8%       +61.4% —

  🚨 Needs Attention:
     AAI: Weak 1Y price return (-26.9%)

  💪 Strong Performers:
     NVDA: Strong revenue growth (+61.4%)
     NVDA: Margin expanding: 26.0% → 36.2%

══════════════════════════════════════════════════════════════════════
```

## Warning Signals

| Signal | Meaning |
|--------|---------|
| Revenue declining | Top line shrinking YoY |
| Revenue growth decelerating | Growth rate slowing |
| Earnings declining sharply | Net income dropping >10% |
| 🚩 Revenue growing but earnings declining | Margin pressure — costs rising faster |
| 🚩 Earnings up but FCF down | Check earnings quality |
| Margin compression | Net margin falling >3% |
| High leverage | D/E > 2.0x |

## Highlight Signals

| Signal | Meaning |
|--------|---------|
| Strong revenue growth | >10% YoY growth |
| Earnings growing faster than revenue | Improving efficiency |
| Margin expanding | Net margin increasing |
| Conservative debt | D/E < 0.5x |

## Data Sources

| Market | Source | Coverage |
|--------|--------|----------|
| US | SEC XBRL companyfacts | Revenue, earnings, FCF, balance sheet |
| US | Yahoo Finance | Price, 1Y/3Y returns |
| Thai | Yahoo Finance | Price, 1Y/3Y returns only |

## Notes

- Thai stocks have limited health data (price-based only)
- SEC XBRL data uses 10-K annual filings for revenue/earnings
- CAGR calculated over available positive years (up to 6)
- Grade is relative — a "B" in a healthy market may be different in a downturn
