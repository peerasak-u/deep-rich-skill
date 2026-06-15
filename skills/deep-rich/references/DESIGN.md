# Report Design

HTML reports: dashboard, company profile, review, decision brief. One product feel — calm private-banking dashboard, not trading terminal.

Artifacts in app root — not skill repo. Paths: [APP-LAYOUT](APP-LAYOUT.md).

## Theme

Light default (match `dashboard/index.html`). Copy `:root` tokens from app dashboard or use:

`--ink`, `--surface`, `--line`, `--coral`, `--mint`, `--cyan`, `--warning`, `--danger`, `--success`, `--radius: 14px`, `--font-ui`, `--font-mono`

Dark only for explicit off-dashboard presentations.

## Required components

1. Top bar — product, artifact type, update time, source
2. Pill nav — section anchors
3. Hero decision card — one-sentence conclusion
4. Fact strip — 3–5 metrics with dates/currencies
5. Two-column layout — narrative + numeric support
6. Tables — comparable data
7. Callout — guardrail/caveat
8. Data-quality boundary — facts vs calculated vs estimates vs unknowns
9. Logos — local `.deep-rich/company-assets/logos/` only; !hotlink providers

## Logo

Path: `.deep-rich/company-assets/logos/<sym-lower>.<ext>`

Fallback: `companies/<SYM>.json.logo.path` → standard extensions → ticker tile. Missing logo !block report — note in data quality.

From `company/<sym>.html` → `../.deep-rich/company-assets/logos/…` or embed small PNG/SVG as data URI.

Metadata in profile JSON: `path`, `source`, `source_url`, `fetched_at`, `license_note`, `confidence`. Source priority → [DATA-SOURCES](DATA-SOURCES.md#company-logos).

## Company profile

Generate from [templates/company-profile.html](templates/company-profile.html) via exporter — agent fills JSON, script renders.

Section order: header → position (if held) → overview → logo → evidence map (readable bars; !radar label overlap; !SWS branding) → valuation guardrail (multiples only) → future growth (estimates) → past performance → financial health → thesis → risks → mgmt/ownership → data status.

## Charts

CDN OK for viz only — never upload private data. Embed data locally. Chart.js default: `https://cdn.jsdelivr.net/npm/chart.js`. Mermaid for flows only. HTML fallback on decision-critical charts.

## Visual rules

Cards/tables over paragraphs. Green=strength, yellow=caution, red/coral=risk, cyan=info. Chip rows: `align-items: flex-start`; short chips `white-space: nowrap`. !imply false precision. !copy SWS UI/scoring.

## Copy labels

| Label | Meaning |
|-------|---------|
| Fact | Sourced + dated |
| Calculated | Derived from visible inputs/scripts |
| Estimate | Analyst/guidance/TAM/forecast |
| Interpretation | Agent synthesis |
| Unknown | Missing/stale/unresearched |

Forecasts, fair value, analyst targets, TAM, future margins = estimates unless transparent model shown.