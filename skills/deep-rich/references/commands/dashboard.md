# dashboard

Export portfolio data and generate a self-contained HTML dashboard.

## Usage

```bash
python3 scripts/export_dashboard.py
open dashboard/dashboard.html
```

## Output Files

| File | Purpose |
|------|---------|
| `dashboard/data.json` | Raw JSON data |
| `dashboard/dashboard.html` | Self-contained HTML (open this) |

## Dashboard Features

- **Summary cards:** Total value, gain/loss, deployable cash
- **Allocation chart:** Doughnut chart of asset classes
- **Drift visualization:** Color-coded bars vs target
- **Deployment plan:** Recommended cash allocation
- **Holdings table:** Per-stock performance with gain/loss
- **Class summary:** Per-class allocation and drift

## Drift Color Coding

| Color | Range | Meaning |
|-------|-------|---------|
| Green | < 5% | On track |
| Yellow | 5-15% | Needs attention |
| Red | > 15% | Significant rebalancing |

## Notes

- `dashboard.html` is self-contained — works offline, shareable
- Data is embedded inline (no CORS issues with file://)
- Re-run `export_dashboard.py` to refresh data
- No server required — just open the HTML file
