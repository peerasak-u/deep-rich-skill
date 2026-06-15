# goals

Track financial targets — on track?

## When

- Monthly; "am I on track" / "when will I hit X" / new goal

## File

`.deep-rich/goals.json` — `goals[]` with `id`, `name`, `target_amount`, `currency`, `target_date`, `created`, optional `type`/`notes`

## Set goal

1. Ask: target amount, date, constraints
2. `dr portfolio` + `dr performance` — current value, historical growth, required rate, monthly contribution needed
3. Write `goals.json`
4. Synth: current vs target → feasibility → paths (growth-only | growth+contributions | extend timeline) → recommendation

## Track

1. Read `goals.json`
2. `dr portfolio`
3. Per goal: progress %, time left, required pace vs historical, on-track status
4. Synth: per-goal status + adjustments

## Guards

Realistic returns; multiple paths; goals = guides not deadlines; celebrate progress.