# App Layout

Artifacts in portfolio app root — not this skill repo.

## `.deep-rich/`

| File | Purpose |
|------|---------|
| `portfolio.json` | Holdings |
| `config.json` | Settings (emergency floor) |
| `prices.json` | Cached prices |
| `snapshots/` | Portfolio snapshots (`--snapshot`) |
| `journal.md` | Decision journal |
| `goals.json` | Financial goals |
| `data/thesis.json` | Asset thesis + conviction |
| `data/sec_tickers.json` | Cached SEC ticker→CIK map |
| `onboarding/` | Onboarding drafts + backups |
| `reviews/` | Saved reviews |
| `companies/` | Company profiles (JSON) |
| `company-assets/logos/` | Cached logos |

## App scripts

| Path | Purpose |
|------|---------|
| `CONTEXT.md` | Domain glossary |
| `scripts/dr.py` | Main CLI |
| `scripts/sec_lookup.py` | SEC ticker→CIK resolver |
| `scripts/fundamentals.py` | SEC EDGAR + Yahoo |
| `scripts/export_dashboard.py` | Dashboard export |
| `scripts/export_company_profile.py` | Company profile HTML |
| `dashboard/dashboard.html` | Self-contained dashboard |
| `company/<sym>.html` | Company profile |
| `skills/deep-rich/` | This skill package |