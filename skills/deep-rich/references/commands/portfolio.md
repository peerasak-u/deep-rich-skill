# portfolio

Show portfolio overview with allocation drift analysis.

## Usage

```bash
python3 scripts/dr.py portfolio [OPTIONS]
```

## Options

| Option | Description |
|--------|-------------|
| `--snapshot` | Save current state to database |
| `--history` | Show past snapshots (last 10) |

## Examples

```bash
# Basic portfolio view
python3 scripts/dr.py portfolio

# Save snapshot
python3 scripts/dr.py portfolio --snapshot

# View history
python3 scripts/dr.py portfolio --history
```

## Output

```
============================================================
  📊 Deep Rich Portfolio
============================================================
  Total:     ฿     1,793,447  ($    54,814)
  Rate:      USD/THB = 32.72
  Floor:     ฿       300,000  (emergency)
  Deploy:    ฿       691,789  (available)
============================================================

  Class           Value (THB)       %   Target    Drift
  ------------ -------------- ------- -------- --------
  Cash         ฿     989,947   55.2%    20.0%  🔴+35.2%
  US Market    ฿     445,724   24.9%    35.0%  🟡-10.1%
  Gold         ฿     140,000    7.8%    10.0%   🟢-2.2%
  Crypto       ฿     108,791    6.1%    10.0%   🟢-3.9%
  Thai SET     ฿     107,020    6.0%    25.0%  🟡-19.0%
```

## Drift Indicators

| Icon | Range | Meaning |
|------|-------|---------|
| 🟢 | < 5% | On track |
| 🟡 | 5-15% | Needs attention |
| 🔴 | > 15% | Significant rebalancing needed |

## Notes

- Prices are fetched live (crypto, USD/THB, US stocks, Thai stocks)
- Thai stocks use Yahoo Finance with `.BK` suffix
- Snapshot saves to `snapshots` table in SQLite
