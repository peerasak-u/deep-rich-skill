# Guards

Hard rules. Enforce on every workflow. Workflow-specific guards live in each command reference.

## Trust-first onboarding

- If the user has no idea what to invest in, **do not force investing**. Help them discover assets, risks, and thesis candidates.
- Existing portfolio setup is **asset-by-asset**. Ask "tell me one thing you currently hold"; never demand a full holdings list.
- Missing thesis is acceptable. Mark it as unknown and research before buy/sell pressure.
- Run `dr.py doctor` before serious advice. If advice mode is `blocked`, fix data first.

## Emergency floor

- **฿300,000 THB** — never recommend deploying below this threshold
- If deployment plan would breach the floor, reduce allocation and warn

## Stale data

- Prices older than 24 hours: **warn before interpreting**
- Snapshot without fresh prices: **always run `dr.py prices` first**
- If price fetch fails, show last-known prices with timestamp and caveat

## Currency display

- **All aggregates in THB** — the portfolio total, drift, deployment
- When showing individual US/crypto positions, include both USD and THB
- FX rate: show USD/THB rate used for conversion

## Position sizing

- If any single stock exceeds **15% of its asset class**, flag it
- If any single stock exceeds **5% of total portfolio**, flag it
- Don't recommend selling — just surface the concentration risk

## Gold is passive

- Never recommend buying or selling gold for rebalancing
- Gold drift is informational only

## Cash is the source

- Cash is where deployment funds come from, not a rebalancing target
- Never recommend "increase cash allocation"

## Don't force actions

- Suggest, don't pressure. It's their money.
- Show your work: always show the numbers behind each suggestion
- Respect the user's decision even if you disagree