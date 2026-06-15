# doctor

Read-only health check for Deep Rich data quality and advice readiness.

## When to use

- Before serious portfolio advice, deploy, or rebalance decisions
- After onboarding or editing `.deep-rich/portfolio.json`
- When prices, thesis, allocation, or snapshots may be stale/missing
- User says "is my data okay", "health check", "doctor", or "can I trust the tool?"

## Command

```bash
cd "$DEEP_RICH_HOME"
python3 scripts/dr.py doctor
python3 scripts/dr.py doctor --json
```

## Philosophy

Bad data creates bad advice. Doctor should be supportive and clear:

- read-only by default
- no network calls
- no automatic price refresh
- no portfolio mutation
- warnings downgrade advice mode instead of shaming the user
- missing thesis means "research first", not "sell/buy now"

## Checks

### Workspace/config

- `.deep-rich/` exists
- `.deep-rich/config.json` is valid JSON
- emergency floor is numeric and non-negative
- target allocation sums to 100%

### Portfolio data

- `.deep-rich/portfolio.json` exists and is valid JSON
- required asset classes exist: Thai SET, US Market, Crypto, Gold, Cash
- holdings list shape is valid
- quantities are numeric and non-negative
- cost basis is numeric when present
- currencies are valid (`THB`, `USD`)
- duplicate symbols are flagged

### Prices

- `.deep-rich/prices.json` exists and is valid JSON
- `updated_at` is present and less than 24h old
- USD/THB rate exists
- every holding has a cached price

### Thesis/readiness

- `.deep-rich/data/thesis.json` exists and is valid JSON
- Thai SET / US Market / Crypto holdings have thesis coverage
- `unknown`, blank, or missing thesis is a warning, not a fatal error

### History/risk

- snapshot exists in `.deep-rich/snapshots/`
- portfolio calculation succeeds
- concentration risk is flagged:
  - holding >5% of total portfolio
  - holding >15% of its asset class

## Advice modes

| Mode | Meaning |
|------|---------|
| `ready` | Data looks usable for normal review/research/deploy workflows |
| `limited` | Usable with caveats; explain missing data before advice |
| `blocked` | Fix data first; do not provide portfolio action advice |

## Example output

```text
🩺 Deep Rich Doctor
✅ portfolio.json valid
⚠️ Prices are 31h old (> 24h)
⚠️ Thesis missing/unknown for 4/12 holdings: BTC, ETH, ARM, AAI

Readiness: 78%
Advice mode: limited — usable with caveats

Next actions
1. Run `python3 scripts/dr.py prices` before interpreting valuation or drift.
2. Use `python3 scripts/dr.py onboard --existing` or research each asset before forcing buy/sell decisions.
```

## JSON output

`doctor --json` returns:

```json
{
  "generated_at": "2026-06-11T00:00:00+00:00",
  "score": 78,
  "advice_mode": "limited",
  "advice_label": "limited — usable with caveats",
  "checks": [],
  "warnings": [],
  "errors": [],
  "next_actions": []
}
```

Use JSON mode when an agent needs to gate workflows automatically.
