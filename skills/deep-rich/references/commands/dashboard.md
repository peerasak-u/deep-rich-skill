# dashboard

Self-contained HTML portfolio dashboard.

```bash
python3 scripts/export_dashboard.py
open dashboard/dashboard.html
```

Outputs: `dashboard/data.json`, `dashboard/dashboard.html` (open this).

Features: summary cards, allocation chart (Chart.js), drift bars, deployment plan, holdings table with local logos, class summary.

Logos: `companies/<SYM>.json.logo.path` → `company-assets/logos/<sym>.{png,webp,jpg,svg}` → ticker tile. !hotlink. Include `logo_path`, `logo_source`, `logo_available` in `data.json`.

Drift colors: green <5%, yellow 5–15%, red >15%. Self-contained/offline — re-run to refresh.