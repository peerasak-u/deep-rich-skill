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

## Company Logos

Company logos are visual aids, not financial data. Cache them locally and record the source so generated company profiles are stable offline and do not hotlink untrusted assets.

### Recommended source priority

| Priority | Source | Coverage | Trust / licensing notes | Use |
|---:|---|---|---|---|
| 1 | Official company website / investor relations site | US + Thai | Best brand accuracy; check site terms before redistribution | Download logo or favicon when company website is known from filings/factsheet |
| 2 | Logo.dev Stock Ticker Logo API | Global tickers, 60+ exchanges | Commercial API; token required; purpose-built for ticker logos | Good default vendor if we add a logo API key |
| 3 | Benzinga Logos API | Companies, funds, crypto; symbol, CIK, ISIN, CUSIP, FIGI lookup | Commercial API; authenticated; returns light/dark logos and metadata | Strong US-source fallback because CIK/ISIN matching reduces ambiguity |
| 4 | CompanyLogo.xyz | Global exchanges, standardized 200x200 PNG | Commercial API; exchange + ticker endpoint | Good normalized image fallback |
| 5 | LogoKit Stock Logo API | Global stock/fund logos | Commercial API; ticker/domain logo URLs and fallback behavior | Useful fallback if coverage is better for a symbol |
| 6 | Clearbit-style domain logo endpoints | Domain-based only | Convenient but not exchange/security aware; verify terms/current availability | Last resort for company website logos |

### US stocks

Best matching keys:

1. `ticker` + exchange (NYSE/Nasdaq)
2. SEC `CIK`
3. `ISIN` / `CUSIP` / `FIGI` when available
4. company website domain from SEC submissions

Preferred approach:

```text
SEC/company website domain → official logo/favicon
if missing → Benzinga by CIK or symbol
if missing → Logo.dev / CompanyLogo.xyz / LogoKit by ticker
if missing → generated monogram tile
```

### Thai stocks

Trusted Thai market data sources such as SET/SETSMART and Thai SEC are strong for company identity, factsheets, filings, and financials, but a public official logo API was not identified. Treat logos separately from Thai financial data.

Best matching keys:

1. SET symbol, e.g. `KBANK`, `PTT`, `NSL`
2. Yahoo-style symbol with suffix, e.g. `KBANK.BK`
3. company website domain from SET factsheet, annual report, or Thai SEC filings
4. ISIN if available from a licensed source

Preferred approach:

```text
SET factsheet / Thai SEC / annual report → company website domain → official logo/favicon
if missing → Logo.dev / CompanyLogo.xyz / LogoKit using SET symbol or .BK ticker if supported
if missing → generated monogram tile
```

### Local cache contract

When implemented, store downloaded logos under the Deep Rich app root, not this skill repo:

```text
.deep-rich/company-assets/logos/<symbol-lower>.<ext>
```

Add logo metadata to `.deep-rich/companies/<SYM>.json`:

```json
{
  "logo": {
    "path": ".deep-rich/company-assets/logos/net.png",
    "source": "official_website | benzinga | logo_dev | companylogo_xyz | logokit | generated",
    "source_url": "https://...",
    "fetched_at": "YYYY-MM-DD",
    "license_note": "internal report use; verify before redistribution",
    "confidence": "high | medium | low"
  }
}
```

Rules:

- Prefer local cached files in generated HTML: `../.deep-rich/company-assets/logos/net.png` from `company/net.html` if browser path allows it.
- If local file access is awkward, embed as a data URI only for small PNG/SVG assets.
- Do not hotlink third-party logo URLs in private reports unless explicitly acceptable by that provider's terms.
- If no trusted logo is available, use a consistent generated tile with the ticker initials.
- Never let missing logos block research or advice workflows.

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
