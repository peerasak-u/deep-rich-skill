# health

Quantitative health score — revenue, earnings, margins, FCF, debt.

```bash
python3 scripts/dr.py health <SYM>
python3 scripts/dr.py health watchlist
python3 scripts/health.py <SYM> [--json]
```

## Grades

| Grade | Score | Meaning |
|-------|-------|---------|
| 🟢 A | 80%+ | Excellent |
| 🔵 B | 65–79% | Good |
| 🟡 C | 50–64% | Monitor |
| 🟠 D | 35–49% | Warning |
| 🔴 F | <35% | Critical |

## Scoring weights

Revenue growth 25% | Earnings growth 25% | Margin trend 20% | FCF 15% | D/E 15%

## Signals

**Warnings:** revenue declining; growth decelerating; earnings −>10%; revenue↑ earnings↓; earnings↑ FCF↓; margin compression >3%; D/E >2.0

**Highlights:** revenue >10%; earnings > revenue growth; margin expanding; D/E <0.5

## Sources

US: SEC XBRL + Yahoo (price, 1Y/3Y). Thai: Yahoo price only (limited health data).