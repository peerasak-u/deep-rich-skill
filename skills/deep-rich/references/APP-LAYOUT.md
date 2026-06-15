# App Layout

All portfolio artifacts live in the portfolio manager app root, not this skill repo.

## `.deep-rich/` data

| File | Purpose |
|------|---------|
| `.deep-rich/portfolio.json` | Holdings |
| `.deep-rich/config.json` | Settings (emergency floor) |
| `.deep-rich/prices.json` | Cached prices (auto-updated) |
| `.deep-rich/snapshots/` | Portfolio snapshots (on `--snapshot`) |
| `.deep-rich/journal.md` | Decision journal |
| `.deep-rich/goals.json` | Financial goals |
| `.deep-rich/data/thesis.json` | Asset thesis + conviction |
| `.deep-rich/onboarding/` | Onboarding drafts + backups |
| `.deep-rich/reviews/` | Saved portfolio reviews |
| `.deep-rich/companies/` | Company research profiles (JSON) |
| `.deep-rich/company-assets/logos/` | Cached company logos |

## App scripts and outputs

| Path | Purpose |
|------|---------|
| `CONTEXT.md` | Domain glossary |
| `scripts/dr.py` | Main CLI |
| `scripts/fundamentals.py` | SEC EDGAR + Yahoo |
| `scripts/export_dashboard.py` | Dashboard export |
| `scripts/export_company_profile.py` | Company profile HTML export |
| `dashboard/dashboard.html` | Self-contained dashboard |
| `company/<sym>.html` | Visual company profile from JSON + template |
| `skills/deep-rich/` | This skill package |