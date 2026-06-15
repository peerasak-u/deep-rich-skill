# summary

Portfolio as JSON for agents/scripts.

```bash
python3 scripts/dr.py summary
```

Keys: `total_thb`, `total_usd`, `usd_thb_rate`, `emergency_floor_thb`, `deployable_cash_thb`, `classes{value_thb,pct,target_pct,drift}`, `holdings[]{symbol,class,quantity,price,value_thb,cost_basis}`, `calculated_at`.

Live prices during run. Holdings sorted by value desc.