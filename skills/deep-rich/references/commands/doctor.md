# doctor

Read-only data health + advice readiness gate.

## When

- Before serious advice, deploy, rebalance
- After onboarding or portfolio edits
- Stale prices/thesis/allocation
- "is my data okay" / "health check" / "doctor"

## Command

```bash
cd "$DEEP_RICH_HOME"
python3 scripts/dr.py doctor
python3 scripts/dr.py doctor --json
```

## Behavior

Read-only. No network. No price refresh. No mutation. Warnings downgrade advice mode — missing thesis = research first, not buy/sell now.

## Checks

| Area | Validates |
|------|-----------|
| Workspace | `.deep-rich/` exists; `config.json` valid; floor numeric ≥0; allocation sums 100% |
| Portfolio | `portfolio.json` valid; classes Thai SET/US/Crypto/Gold/Cash; holdings shape; qty ≥0; currencies THB/USD; dup symbols flagged |
| Prices | `prices.json` valid; `updated_at` <24h; USD/THB rate; every holding priced |
| Thesis | `data/thesis.json` valid; Thai/US/Crypto thesis coverage; unknown = warning |
| History | snapshot in `snapshots/`; portfolio calc OK; conc >5% port or >15% class flagged |

## Advice modes

| Mode | Meaning |
|------|---------|
| `ready` | Normal workflows OK |
| `limited` | Usable with caveats — explain gaps |
| `blocked` | Fix data first — no portfolio action advice |

## JSON (`--json`)

Keys: `generated_at`, `score`, `advice_mode`, `advice_label`, `checks[]`, `warnings[]`, `errors[]`, `next_actions[]`