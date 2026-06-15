# deployment

Show cash deployment plan — how to allocate excess cash to underweight asset classes.

## Usage

```bash
python3 scripts/dr.py deployment
```

## Output

```
============================================================
  🚀 Deployment Plan
============================================================
  Available:      ฿     691,789
  Emergency floor: ฿     300,000
  Current cash:   ฿     989,947
============================================================

  Class         Current   Target    Drift     Allocate
  ------------ -------- -------- -------- ------------
  Thai SET         6.0%    25.0%   -19.0% ฿   396,409
  US Market       24.9%    35.0%   -10.1% ฿   211,638
  Crypto           6.1%    10.0%    -3.9% ฿    81,900

  💡 Deploy gradually over 3-6 months via dollar-cost averaging
```

## How It Works

1. Calculates excess cash: `current_cash - emergency_floor`
2. Identifies underweight classes (drift < 0)
3. Allocates proportionally to drift magnitude
4. Excludes Cash and Gold (passive)

## Key Rules

- **Emergency floor:** ฿300,000 (configurable in `config.json`)
- **Gold is excluded** — passive, no rebalancing
- **Cash is excluded** — it's the source, not a target

## Notes

- Allocation is proportional to drift (more underweight = more allocation)
- Recommendation: deploy gradually, not all at once
- Consider market conditions before deploying
