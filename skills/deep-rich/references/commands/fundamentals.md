# fundamentals

Get fundamental data for a stock.

## Usage

```bash
python3 scripts/dr.py fundamentals <SYMBOL>
```

## Examples

```bash
# US stock (SEC EDGAR + Yahoo Finance)
python3 scripts/dr.py fundamentals MSFT
python3 scripts/dr.py fundamentals NVDA

# Thai stock (Yahoo Finance .BK + SEC 56-1)
python3 scripts/dr.py fundamentals KBANK
python3 scripts/dr.py fundamentals NSL

# Get Thai SEC 56-1 download URL
python3 scripts/dr.py thai-561 KBANK --url

# Extract from downloaded PDF
python3 scripts/dr.py thai-561 KBANK /path/to/report.pdf
```

## Output (US Stock)

```
============================================================
  📊 MSFT — Fundamentals
  Asset Class: US Market
============================================================

  Price:          416.67
  Day Change:     🔴 -51.01 (-10.9%)
  52W Range:      356.28 - 555.45
  52W Position:   30.3% (Mid-range)

  ────────────────────────────────────────
  SEC EDGAR Financials (USD):
  ────────────────────────────────────────
  revenue                   $        82.9B
  net_income                $        31.8B
  total_assets              $       694.2B
  total_liabilities         $       279.9B
  stockholders_equity       $       414.4B

  ────────────────────────────────────────
  Recent SEC Filings:
  ────────────────────────────────────────
    10-Q     2026-04-29
    10-Q     2026-01-28

  ────────────────────────────────────────
  Data Sources:
    ✅ yahoo
    ✅ sec_edgar
    ✅ sec_xbrl
```

## Output (Thai Stock)

```
============================================================
  📊 KBANK — Fundamentals
  Asset Class: Thai SET
============================================================

  Price:          201.00
  Day Change:     🟢 +44.50 (+28.4%)
  52W Range:      147.00 - 208.00
  52W Position:   88.5% (Near 52W High 📈)

  💡 For P/E, P/BV, ESG: use 'python3 scripts/dr.py fundamentals-detail KBANK'
```

## Data Sources

| Market | Source | Data |
|--------|--------|------|
| US | Yahoo Finance | Price, 52W range, volume |
| US | SEC EDGAR | 10-K/10-Q filings |
| US | SEC XBRL | Revenue, net income, assets, equity |
| Thai | Yahoo Finance (.BK) | Price, 52W range, volume |

## 52W Position Indicator

| Range | Label |
|-------|-------|
| < 25% | Near 52W Low 📉 |
| 25-75% | Mid-range |
| > 75% | Near 52W High 📈 |

## Notes

- SEC EDGAR data requires User-Agent header (automatically set)
- XBRL financials are from most recent 10-K or 10-Q
- For Thai SEC 56-1 data, use `thai_fundamentals.py` (PDF extraction)
- For SET Factsheet (P/E, P/BV), use `set_scraper.py` (browser-based)
