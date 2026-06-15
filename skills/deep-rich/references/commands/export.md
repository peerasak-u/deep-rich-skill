# export

Generate a visual company profile HTML from a structured JSON company profile.

## Command

```bash
python3 skills/deep-rich/scripts/export_company_profile.py <TICKER> [--home /path/to/deep-rich]
```

## What it does

1. **Resolves the app root** via `--home`, `DEEP_RICH_HOME`, or sibling `../deep-rich` discovery.
2. **Reads** `.deep-rich/companies/<TICKER>.json`.
3. **Reads** the skill template at `skills/deep-rich/references/templates/company-profile.html`.
4. **Builds** all `{{var}}` substitutions from the JSON (prices, position, financials, thesis, risks, competitors, data quality, etc.).
5. **Substitutes** and **writes** `company/<ticker-lower>.html`.

## Arguments

| Argument | Required | Description |
|---|---|---|
| `TICKER` | ✅ | Stock ticker symbol, e.g. `NET`. Case-insensitive; normalized to uppercase internally. |
| `--home PATH` | No | Override the app root discovery. Use when running from outside the workspace. |

## Exit codes

| Code | Meaning |
|---|---|
| 0 | HTML written successfully. |
| 1 | JSON or template not found. |

## Template variables

The exporter maps these `{{var}}` placeholders in `company-profile.html`. Agents do not need to produce these directly; they come from the JSON.

| Variable | Source in JSON |
|---|---|
| `{{ticker}}` | `ticker` |
| `{{company_name}}` | `name` |
| `{{updated_at}}` | `meta.updated_at` |
| `{{profile_source_path}}` | Computed relative path to JSON |
| `{{position_badge}}` | `"Held position"` if `position.quantity > 0`, else `"No position"` |
| `{{verdict}}` | `thesis.verdict` |
| `{{business_description}}` | `business.description` |
| `{{logo_html}}` | Resolved from `logo.path` against app root; fallback to ticker tile |
| `{{identity_tags_html}}` | Exchange:ticker, sector, industry, country tags |
| `{{current_price}}` | `financials.price` |
| `{{gain_pct}}` | `position.unrealized_gain_pct` |
| `{{quantity}}` | `position.quantity` |
| `{{range_low}}`, `{{range_high}}` | `financials.52w_low`, `financials.52w_high` |
| `{{range_position_pct}}` | `financials.52w_position` |
| `{{suggested_action}}` | `thesis.suggested_action` |
| `{{market_cap_label}}` | Estimated from `financials.fy2025_revenue * 40`; verify before use |
| `{{evidence_summary}}` | Static Deep Rich framing text |
| `{{business_flow_html}}` | Three-node CDN→edge→outcome flow |
| `{{evidence_chart_json}}` | Chart.js radar data from health grade |
| `{{evidence_fallback}}` | Text fallback for radar chart |
| `{{valuation_html}}` | Position value (THB/USD), cost basis, gain/loss |
| `{{future_growth_html}}` | TAM and key growth engine |
| `{{past_performance_html}}` | Revenue, growth, FCF table |
| `{{health_summary}}` | `financials.health_summary` |
| `{{health_grade}}` | `financials.health_grade` |
| `{{health_html}}` | Assets, liabilities, equity, D/E ratio |
| `{{verdict_reason}}` | `thesis.verdict_reason` |
| `{{bull_case_html}}` | `thesis.bull_case` list items |
| `{{bear_case_html}}` | `thesis.bear_case` list items |
| `{{risks_catalysts_html}}` | Risks and catalysts side-by-side |
| `{{competitors_table_html}}` | Competitors table with advantages/disadvantages |
| `{{data_quality_html}}` | Facts / estimates / missing boundary |
| `{{footer_note}}` | Static Deep Rich data policy note |

## Logo resolution

1. Check `logo.path` in JSON (e.g. `.deep-rich/company-assets/logos/net.png`).
2. Resolve against the app root — verify the file actually exists.
3. If found, embed as `<img src="../../{logo.path}" alt="...">` (relative from `company/<sym>.html`).
4. If not found, render a ticker tile with the ticker symbol.

Missing logos do **not** block generation.

## Example

```bash
# From the skill package directory
cd ~/Workspace/indie/deep-rich-skill
PYTHONPATH=skills/deep-rich/scripts \
  python3 skills/deep-rich/scripts/export_company_profile.py NET

# From anywhere with explicit home
python3 skills/deep-rich/scripts/export_company_profile.py NET \
  --home ~/Workspace/indie/deep-rich
```

Output:

```
[ok] Wrote ~/Workspace/indie/deep-rich/company/net.html
```

## For agents

After updating `.deep-rich/companies/<SYM>.json` (e.g. after refreshing prices or refreshing the thesis), re-run the exporter to regenerate the HTML:

```bash
python3 skills/deep-rich/scripts/export_company_profile.py <SYM>
```

Do not hand-edit `company/<symbol>.html`. All visual consistency lives in the template; all data lives in the JSON. If something looks wrong, fix the exporter script or the template, not the output HTML.
