# performance

Show portfolio performance comparing cost basis to current value.

## Usage

```bash
python3 scripts/dr.py performance
```

## Output

Shows per-holding and per-class:
- Cost basis (ทุน) in THB
- Current value in THB
- Gain/Loss in THB and percentage

```
================================================================================
  📈 Performance by Holding
================================================================================

  US Market
  Symbol            Qty     Cost (THB)    Value (THB)      Gain/Loss        %
  ---------- ---------- -------------- -------------- -------------- --------
  NVDA            17.96  ฿      33,284 ฿     120,509 🟢 ฿     +87,225  +262.1%
  GOOGL            9.01  ฿      38,381 ฿     108,659 🟢 ฿     +70,278  +183.1%
  ...

================================================================================
  📊 Portfolio Total
================================================================================
  Total Cost:    ฿     1,540,585
  Total Value:   ฿     1,793,447
  Gain/Loss:     🟢 ฿    +252,862  (+16.4%)
================================================================================
```

## Notes

- Cost basis comes from `portfolio.json`
- Crypto (BTC/ETH) shows ❓ N/A if cost basis is missing
- Cash always shows 0% gain (cost = value)
