# analyze

8-area company analysis.

```bash
python3 scripts/dr.py analyze <SYM>
python3 scripts/analyze.py <SYM> [--json]
```

| # | Section | US | Thai |
|---|---------|----|------|
| 1 | Overview | SEC + Yahoo | Yahoo |
| 2 | Valuation | cap, 52W | 52W |
| 3 | Future growth | analyst API needed | N/A |
| 4 | Past performance | revenue, margin, returns | price returns |
| 5 | Financial health | assets, D/E, FCF | limited |
| 6 | Dividend | DPS, yield | N/A |
| 7 | Management | SEC filings | limited |
| 8 | Ownership | 13F needed | N/A |

Sources: SEC EDGAR, Yahoo (`.BK` Thai). For deep research use [research](research.md).