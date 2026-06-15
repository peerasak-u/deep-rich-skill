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
- **Allocation chart:** Doughnut chart of asset classes, preferably with Chart.js CDN or equivalent readable SVG
- **Drift visualization:** Color-coded bars vs target
- **Deployment plan:** Recommended cash allocation
- **Holdings table:** Per-stock performance with gain/loss and local cached company logos
- **Class summary:** Per-class allocation and drift

## Logo Handling

The dashboard exporter must use downloaded local logos from `.deep-rich`; it must not hotlink third-party logo provider URLs.

For each stock holding:

1. Prefer `.deep-rich/companies/<SYM>.json.logo.path` if present and the file exists.
2. Otherwise check `.deep-rich/company-assets/logos/<symbol-lower>.png`, `.webp`, `.jpg`, `.svg`.
3. If no logo exists, render a generated ticker/initials tile.
4. Include the resolved `logo_path` or fallback status in `dashboard/data.json` so the HTML renderer is deterministic.

Recommended data shape for each holding:

```json
{
  "symbol": "NET",
  "name": "Cloudflare, Inc.",
  "logo_path": ".deep-rich/company-assets/logos/net.png",
  "logo_source": "official_website",
  "logo_available": true
}
```

When embedding data inline into `dashboard.html`, keep paths relative to `dashboard/dashboard.html`. From the dashboard folder, `.deep-rich/company-assets/logos/net.png` is typically referenced as `../.deep-rich/company-assets/logos/net.png`. If the dashboard must be fully standalone, embed cached local logos as small data URIs.

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
