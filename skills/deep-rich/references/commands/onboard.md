# onboard / setup

Trust-first bootstrap for Deep Rich. Use this before advice when portfolio data, target allocation, or thesis coverage is missing.

## When to use

- User says "setup my portfolio", "start Deep Rich", "onboard me", or "I have an existing portfolio"
- User is new and has no idea what to invest in
- User has holdings but no written thesis for why they hold them
- Doctor reports missing portfolio, missing thesis, or low advice readiness

## Command

```bash
cd "$DEEP_RICH_HOME"
python3 scripts/dr.py onboard

# optional direct modes
python3 scripts/dr.py onboard --fresh
python3 scripts/dr.py onboard --existing
python3 scripts/dr.py setup
```

## Core principle

Do **not** force investing. If the user has no idea what to buy, help them discover assets, risks, and thesis candidates. Staying in cash while learning is valid.

## Mode A: Fresh / no portfolio yet

The command asks gentle discovery questions:

- emergency floor in THB
- whether the user already knows target allocation
- money truly investable now, optional
- monthly contribution/deployment amount, optional
- markets the user understands or wants to learn
- assets/themes they are curious about
- assets they absolutely do not want
- risk style: conservative / balanced / aggressive / unsure
- optional financial goal

Output is a draft with:

- empty portfolio template
- config with emergency floor and target allocation
- research queue
- discovery notes
- no buy recommendations

## Mode B: Existing portfolio

Ask **one asset at a time**. Do not ask for a full list.

Prompt shape:

```text
Tell me one thing you currently hold (symbol/name): MSFT
Asset class: US Market
Quantity: 10
Cost basis per unit: 378
Why do you hold MSFT? (blank = unknown): AI platform + cloud compounding
Conviction: high/medium/low/unsure
What would make you sell/reduce it?: thesis broken or valuation absurd
Add another holding? [y/N]
```

Rules:

- Blank thesis is okay; mark it `unknown` and `needs_research: true`
- Cash does not need an investment thesis
- Gold/stock/crypto thesis can be captured if the user knows it
- If the user is unsure, capture the holding and let doctor downgrade advice mode

## Safety behavior

Onboarding always saves a draft first:

```text
.deep-rich/onboarding/draft-YYYYMMDD-HHMMSS-fresh.json
.deep-rich/onboarding/draft-YYYYMMDD-HHMMSS-existing.json
```

It only writes live files after explicit confirmation:

```text
Apply this draft to live `.deep-rich` files now? [y/N]
```

If applying would overwrite files, previous files are backed up under:

```text
.deep-rich/onboarding/backup-YYYYMMDD-HHMMSS/
```

## After onboarding

Run:

```bash
python3 scripts/dr.py doctor
```

If doctor says data is limited or blocked, fix data or research thesis before review/deploy/rebalance advice.
