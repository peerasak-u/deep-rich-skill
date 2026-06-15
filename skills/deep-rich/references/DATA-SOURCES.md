# Data Sources

## Prices

| Asset | Source | Notes |
|-------|--------|-------|
| BTC, ETH | CoinGecko `api.coingecko.com/api/v3/simple/price` | Real-time, no key |
| US + Thai | Yahoo `query2.finance.yahoo.com/v8/finance/chart/{sym}` | Thai: `.BK` suffix; ~15m delay |
| USD/THB | Open Exchange Rates `open.er-api.com/v6/latest/USD` | Daily, no key |

## Fundamentals

| Market | Source | Data | Method |
|--------|--------|------|--------|
| US | SEC EDGAR `data.sec.gov` | 10-K/10-Q, XBRL financials | User-Agent required; 10 req/s |
| US price | Yahoo | Price, 52W, volume | — |
| Thai | SET factsheet `set.or.th/.../factsheet` | P/E, P/BV, cap, ESG | agent-browser scrape |
| Thai | SEC Thailand `market.sec.or.th/.../FinancialReport` | Statements, ratios | agent-browser |
| Thai 56-1 | `dr thai-561 <SYM>` | SEC filings | — |
| SETSMART API | — | EOD, ratios | Not implemented; key required |

### US ticker → CIK

No hardcoded CIK list. App resolves any US ticker dynamically:

| Step | What |
|------|------|
| Master list | SEC `company_tickers.json` — `https://www.sec.gov/files/company_tickers.json` |
| Resolver | `scripts/sec_lookup.py` → `get_cik(ticker)`, `get_company_name(ticker)` |
| Cache | `.deep-rich/data/sec_tickers.json` (fetched once, reused) |
| Consumers | `fundamentals.py`, `health.py`, `analyze.py` |

Requires User-Agent header on SEC requests. If lookup fails: ticker may be non-US, delisted, or typo — try Yahoo fundamentals or manual CIK from [SEC EDGAR](https://www.sec.gov/edgar/searchedgar/companysearch).

## Company logos

Cache locally — visual aid not financial data. Path + JSON metadata → [DESIGN](DESIGN.md#logo).

| Priority | Source | Use |
|---:|---|---|
| 1 | Official website / IR | Best accuracy |
| 2 | Logo.dev | Ticker API, token |
| 3 | Benzinga | CIK/ISIN match |
| 4 | CompanyLogo.xyz | Normalized PNG |
| 5 | LogoKit | Ticker fallback |
| 6 | Domain logo endpoints | Last resort |

**US match keys:** ticker+exchange → CIK → ISIN/CUSIP/FIGI → domain from SEC.

**Thai match keys:** SET symbol → `SYM.BK` → domain from factsheet/filings → ISIN.

Flow: official domain logo → vendor APIs → generated monogram tile. !hotlink in reports. Missing logo !block workflow.

## Cache (SQLite `fundamentals_cache`)

| Source | TTL |
|--------|-----|
| Yahoo | 4h |
| SEC EDGAR | 24h |
| CoinGecko | none |
| SET Factsheet | 4h |

Clear: `DELETE FROM fundamentals_cache;`

Add source: fetch fn in `fundamentals.py` → `cache_fundamentals()` → `get_fundamentals()` → update this doc.