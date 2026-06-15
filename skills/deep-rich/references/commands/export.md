# export

Company profile HTML from `.deep-rich/companies/<TICKER>.json`.

```bash
python3 skills/deep-rich/scripts/export_company_profile.py <TICKER> [--home PATH]
```

Reads JSON + [templates/company-profile.html](../templates/company-profile.html) → writes `company/<ticker-lower>.html`. Exit 0=OK, 1=missing JSON/template.

Agent fills JSON; script handles `{{var}}` substitution, escaping, logos, Chart.js data. !hand-edit output HTML — fix template/exporter.

Key vars: `ticker`, `company_name`, `updated_at`, `verdict`, `business_description`, `logo_html`, `current_price`, `gain_pct`, `evidence_chart_json`, `valuation_html`, `bull_case_html`, `bear_case_html`, `competitors_table_html`, `data_quality_html`. Full list in exporter source.

Logo: `logo.path` in JSON → verify file → relative img from `company/`; else ticker tile. Missing logo !block generation.

After JSON update → re-run exporter. Design → [DESIGN](../DESIGN.md).