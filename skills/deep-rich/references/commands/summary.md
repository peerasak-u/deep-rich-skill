# summary

Output portfolio data as JSON for programmatic use or AI integration.

## Usage

```bash
python3 scripts/dr.py summary
```

## Output

JSON object with:

```json
{
  "total_thb": 1793447.23,
  "total_usd": 54814.52,
  "usd_thb_rate": 32.72,
  "emergency_floor_thb": 300000,
  "deployable_cash_thb": 691789.13,
  "classes": {
    "Cash": {
      "value_thb": 989947.13,
      "pct": 55.2,
      "target_pct": 20.0,
      "drift": 35.2
    },
    ...
  },
  "holdings": [
    {
      "symbol": "KBANK",
      "class": "Thai SET",
      "quantity": 200,
      "price": 201.0,
      "price_source": "live",
      "value_thb": 40200,
      "cost_basis": 124.51,
      "cost_currency": "THB"
    },
    ...
  ],
  "calculated_at": "2026-06-07T17:36:12"
}
```

## Use Cases

- AI agent integration (pipe to other tools)
- Custom reporting scripts
- Data analysis in Python/R
- Export to spreadsheets

## Notes

- Prices are fetched live during execution
- All values in THB (converted using USD/THB rate)
- `holdings` array is sorted by value (descending)
