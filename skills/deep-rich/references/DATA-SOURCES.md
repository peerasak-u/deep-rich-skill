# Data Sources

## Price Feeds

### CoinGecko (Crypto)
- **URL:** `https://api.coingecko.com/api/v3/simple/price`
- **Data:** BTC, ETH prices in USD
- **Rate limit:** Free tier, no key required
- **Update frequency:** Real-time

### Yahoo Finance (US + Thai)
- **URL:** `https://query2.finance.yahoo.com/v8/finance/chart/{symbol}`
- **Data:** Price, 52W high/low, volume, prev close
- **Thai stocks:** Use `.BK` suffix (e.g., `KBANK.BK`)
- **Rate limit:** No key required, reasonable use
- **Update frequency:** 15-min delay

### Open Exchange Rates (FX)
- **URL:** `https://open.er-api.com/v6/latest/USD`
- **Data:** USD/THB rate
- **Rate limit:** Free, no key
- **Update frequency:** Daily

## Fundamental Data

### SEC EDGAR (US Stocks)
- **URL:** `https://data.sec.gov/`
- **Data:**
  - Company submissions (10-K, 10-Q filings)
  - XBRL financials (revenue, net income, EPS, assets, liabilities, equity)
- **Auth:** No key, but requires User-Agent header
- **Rate limit:** 10 requests/second
- **Coverage:** All US public companies

**Known CIKs (hardcoded):**
| Ticker | CIK |
|--------|-----|
| MSFT | 0000789019 |
| AAPL | 0000320193 |
| GOOGL | 0001652044 |
| AMZN | 0001018724 |
| NVDA | 0001045810 |
| META | 0001326801 |
| TSLA | 0001318605 |
| NET | 0001477333 |
| ARM | 0001973239 |
| AMPH | 0000867665 |

To add more: edit `scripts/fundamentals.py` → `cik_map` dict.

### SET Factsheet (Thai Stocks)
- **URL:** `https://www.set.or.th/th/market/product/stock/quote/{symbol}/factsheet`
- **Data:** P/E, P/BV, Market Cap, ESG rating, Paid-up capital
- **Method:** Browser scraping (agent-browser)
- **Limitation:** Requires browser automation

### Thai SEC (Thai Stocks)
- **URL:** `https://market.sec.or.th/public/idisc/th/FinancialReport/`
- **Data:** Financial statements, MD&A, financial ratios
- **Method:** Browser scraping
- **Coverage:** All SET/mai listed companies

### SETSMART API (Thai Stocks)
- **URL:** `https://www.setsmart.com/api/listed-company-api/`
- **Data:** EOD prices, financial ratios, financial statements
- **Auth:** API key required (register at SETSMART)
- **Status:** Not implemented (future enhancement)

## Caching

All data is cached in SQLite (`fundamentals_cache` table):

| Source | Cache Duration |
|--------|----------------|
| Yahoo Finance | 4 hours |
| SEC EDGAR | 24 hours |
| CoinGecko | Real-time (no cache) |
| SET Factsheet | 4 hours |

To clear cache:
```sql
DELETE FROM fundamentals_cache;
```

## Adding New Sources

1. Add fetch function in `scripts/fundamentals.py`
2. Use `cache_fundamentals()` for caching
3. Integrate into `get_fundamentals()` based on asset class
4. Update this documentation
