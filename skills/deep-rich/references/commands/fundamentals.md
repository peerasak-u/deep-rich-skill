# fundamentals

Fundamental data per symbol.

```bash
python3 scripts/dr.py fundamentals <SYM>
python3 scripts/dr.py thai-561 <SYM> --url
python3 scripts/dr.py thai-561 <SYM> /path/to/report.pdf
```

**US:** SEC EDGAR + Yahoo — price, 52W, XBRL revenue/income/assets/liabilities/equity, recent filings.

**Thai:** Yahoo `.BK` + SEC 56-1. P/E, P/BV, ESG → `dr fundamentals-detail <SYM>`.

Sources + cache → [DATA-SOURCES](../DATA-SOURCES.md).