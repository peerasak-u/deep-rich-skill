# prices

Fetch + cache live prices all classes.

```bash
python3 scripts/dr.py prices
```

Updates USD/THB, BTC, ETH, US, Thai (`.BK`). Stored in SQLite `price_cache`. No API keys.

Run before `portfolio` when stale (>24h). Sources → [DATA-SOURCES](../DATA-SOURCES.md#prices).