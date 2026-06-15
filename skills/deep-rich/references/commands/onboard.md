# onboard / setup

Trust-first bootstrap. Before advice when portfolio, allocation, or thesis missing.

## When

- "setup my portfolio" / "start Deep Rich" / "onboard me" / existing portfolio
- No invest idea yet; holdings without thesis; doctor reports missing data/thesis

## Command

```bash
cd "$DEEP_RICH_HOME"
python3 scripts/dr.py onboard
python3 scripts/dr.py onboard --fresh
python3 scripts/dr.py onboard --existing
python3 scripts/dr.py setup
```

## Rules

!force invest. User unsure → discover assets/risks/thesis. Cash while learning = valid.

**Fresh:** ask floor THB, target allocation?, investable now?, monthly deploy?, markets, themes, exclusions, risk style, goal? → draft: empty portfolio, config, research queue, discovery notes, no buys.

**Existing:** 1 asset at a time — symbol, class, qty, cost basis, thesis (blank=unknown), conviction, sell trigger, add another?

- Blank thesis OK → `unknown`, `needs_research: true`
- Cash: no thesis needed

## Safety

Draft first: `.deep-rich/onboarding/draft-YYYYMMDD-HHMMSS-{fresh|existing}.json`

Apply only after confirm. Overwrite → backup `.deep-rich/onboarding/backup-YYYYMMDD-HHMMSS/`

## After

```bash
python3 scripts/dr.py doctor
```

`limited`/`blocked` → fix data or research thesis before review/deploy/rebalance.

### Profile backfill

After confirm + doctor reads live portfolio → build `.deep-rich/companies/<SYM>.json` for held stocks:

`onboard → confirm → doctor → research <SYM> backfill → review/deploy/rebalance`

Per non-cash holding: check `companies/<SYM>.json`; if missing/stale → `research <SYM>`. Priority: unknown thesis → largest weight → losers → stale fundamentals.

!block onboarding on full research.