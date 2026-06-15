# analyze

Comprehensive company analysis covering 8 key areas.

## Usage

```bash
python3 scripts/dr.py analyze <SYMBOL>
python3 scripts/analyze.py <SYMBOL> [--json]
```

## Examples

```bash
# US stock with full SEC data
python3 scripts/dr.py analyze MSFT
python3 scripts/dr.py analyze NVDA

# Thai stock (limited to Yahoo Finance data)
python3 scripts/dr.py analyze KBANK

# JSON output for programmatic use
python3 scripts/analyze.py MSFT --json
```

## Analysis Sections

| # | Section | US Stocks | Thai Stocks |
|---|---------|-----------|-------------|
| 1 | Company Overview | ✅ SEC name + Yahoo | ✅ Yahoo only |
| 2 | Valuation | ✅ Market cap, 52W range | ✅ 52W range |
| 3 | Future Growth | ⚠️ Requires analyst API | ⚠️ Not available |
| 4 | Past Performance | ✅ Revenue, net income, margins, returns | ✅ Price returns |
| 5 | Financial Health | ✅ Assets, liabilities, D/E, FCF | ⚠️ SEC only |
| 6 | Dividend | ✅ DPS, yield | ⚠️ Not available |
| 7 | Management | ✅ Recent SEC filings | ⚠️ SEC only |
| 8 | Ownership | ⚠️ Requires 13F data | ⚠️ Not available |

## Output Example (MSFT)

```
══════════════════════════════════════════════════════════════════════
  📊 MSFT — Comprehensive Analysis
  Asset Class: US Market
══════════════════════════════════════════════════════════════════════

  ┌─ 1. Company Overview ─────────────────────────────────────┐
  │  Name:      MICROSOFT CORP
  │  Exchange:  NasdaqGS
  │  Price:     416.67 🟢 +165.88
  └──────────────────────────────────────────────────────────┘

  ┌─ 2. Valuation ───────────────────────────────────────────┐
  │  52W Range:         356.28 - 555.45
  │  52W Position:      30% 📊 Mid-range
  └──────────────────────────────────────────────────────────┘

  ┌─ 4. Past Performance ────────────────────────────────────┐
  │  1Y Return:         🔴 -17.8%
  │  3Y Return (ann.):  🟢 +8.3%
  │  Revenue:           $+281.7B
  │  Net Income:        $+101.8B
  │  Net Margin:        36.1%
  └──────────────────────────────────────────────────────────┘

  ┌─ 5. Financial Health ────────────────────────────────────┐
  │  Total Assets:      $+694.2B
  │  Total Liabilities: $+279.9B
  │  Stockholders Eq:   $+414.4B
  │  Debt/Equity:       0.68x 🟢 Conservative
  │  Free Cash Flow:    $+71.6B
  └──────────────────────────────────────────────────────────┘
```

## Data Sources

| Section | Source | Coverage |
|---------|--------|----------|
| Company name | SEC EDGAR submissions | US only |
| Price, 52W range | Yahoo Finance | US + Thai (.BK) |
| Historical returns | Yahoo Finance (5Y chart) | US + Thai (.BK) |
| Revenue, net income | SEC XBRL (10-K annual) | US only |
| Balance sheet | SEC XBRL (latest filing) | US only |
| Dividends | SEC XBRL | US only |
| Recent filings | SEC EDGAR submissions | US only |

## Debt/Equity Rating

| D/E Ratio | Label |
|-----------|-------|
| < 1.0 | 🟢 Conservative |
| 1.0 - 2.0 | 🟡 Moderate |
| > 2.0 | 🔴 High leverage |

## 52W Position Rating

| Position | Label |
|----------|-------|
| < 25% | 📉 Near 52W Low |
| 25-75% | 📊 Mid-range |
| > 75% | 📈 Near 52W High |

## Notes

- Annual revenue/net income preferred over quarterly
- Uses `RevenueFromContractWithCustomerExcludingAssessedTax` (ASC 606) when available
- Thai stocks have limited data (no SEC EDGAR)
- Future growth requires analyst estimates API (not yet implemented)
- Ownership requires 13F filings API (not yet implemented)
