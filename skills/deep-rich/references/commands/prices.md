# prices

Fetch and cache live prices for all asset classes.

## Usage

```bash
python3 scripts/dr.py prices
```

## Output

```
📡 Fetching prices...
   USD/THB: 32.72
   BTC: $62,400
   ETH: $1,631
   Updated: 2026-06-07T17:36:12
```

## Data Sources

| Asset | Source | Endpoint |
|-------|--------|----------|
| BTC, ETH | CoinGecko | `api.coingecko.com/api/v3/simple/price` |
| USD/THB | Open Exchange Rates | `open.er-api.com/v6/latest/USD` |
| US Stocks | Yahoo Finance | `query2.finance.yahoo.com/v8/finance/chart` |
| Thai Stocks | Yahoo Finance | Same, with `.BK` suffix |

## Cache

Prices are stored in `price_cache` table in SQLite.

## Notes

- Run this before `portfolio` to get latest prices
- Thai stock prices use Yahoo Finance `.BK` suffix (e.g., `KBANK.BK`)
- No API keys required for any source
