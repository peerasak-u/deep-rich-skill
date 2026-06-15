# goals

Goal tracking — are you on track for your financial targets?

## When to use

- Monthly (regular goal check)
- When user asks "am I on track" / "when will I hit X"
- When user sets a new financial goal
- When reviewing portfolio performance

## Goals file

Location: `.deep-rich/goals.json`

Format:

```json
{
  "goals": [
    {
      "id": "portfolio-3m",
      "name": "Portfolio reaches ฿3M",
      "target_amount": 3000000,
      "currency": "THB",
      "target_date": "2028-12-31",
      "created": "2026-06-09",
      "notes": "Based on current growth rate + monthly contributions"
    },
    {
      "id": "passive-income",
      "name": "Passive income ฿10k/month",
      "target_amount": 10000,
      "currency": "THB",
      "type": "monthly_income",
      "target_date": "2027-12-31",
      "created": "2026-06-09"
    }
  ]
}
```

---

## Setting goals workflow

When user says "I want to reach X by Y":

### Step 1: Understand the goal

Ask:
- Target amount?
- Target date?
- Any constraints (risk tolerance, liquidity needs)?

### Step 2: Assess feasibility

```bash
cd "$DEEP_RICH_HOME"
python3 scripts/dr.py portfolio
python3 scripts/dr.py performance
```

Calculate:
- Current portfolio value
- Historical growth rate
- Required growth rate to hit target
- Monthly contribution needed (if any)

### Step 3: Save goal

Write to `.deep-rich/goals.json`

### Step 4: Synthesize

```
══════════════════════════════════════════════════════════════════════
  🎯 Goal: Portfolio reaches ฿3M by 2028
══════════════════════════════════════════════════════════════════════

  Current: ฿1,793,324
  Target: ฿3,000,000
  Gap: ฿1,206,676

  ── Feasibility ───────────────────────────────────────────────────
  Time: 2.5 years (30 months)
  Required growth: +67% total, +21% annualized
  Your historical: +16.4% (since inception)

  ── Paths to Goal ─────────────────────────────────────────────────
  Option A: Growth only
    Need +21% annualized (vs your +16.4%)
    Gap: need 4.6% more annualized return
    Risk: aggressive, requires strong stock picking

  Option B: Growth + contributions
    Assume +16% annualized growth
    Need ฿25,000/month contribution
    Total: ฿750k contributions + ฿456k growth

  Option C: Extend timeline
    At +16% annualized, hit ฿3M in 3.2 years (mid-2029)
    More realistic, less stress

  ── Recommendation ────────────────────────────────────────────────
  Option B or C. Don't chase higher returns to hit the date.
  Consistent contributions + reasonable growth beats aggressive bets.
```

---

## Tracking workflow

When user asks "am I on track":

### Step 1: Read goals

Read `.deep-rich/goals.json`

### Step 2: Check current progress

```bash
python3 scripts/dr.py portfolio
```

### Step 3: Calculate trajectory

For each goal:
- Current value vs target
- Time remaining
- Required monthly growth
- On track? (based on historical growth rate)

### Step 4: Synthesize

```
══════════════════════════════════════════════════════════════════════
  🎯 Goal Progress
══════════════════════════════════════════════════════════════════════

  ── Portfolio ฿3M by 2028 ────────────────────────────────────────
  Current: ฿1,793,324 (59.8% of target)
  Time left: 2.5 years
  Required: +21% annualized
  Your pace: +16.4% annualized

  Status: 🟡 Behind pace
  Gap: need ฿25k/month contributions or higher returns

  ── Passive Income ฿10k/month by 2027 ────────────────────────────
  Current dividend yield: ~0.5% (฿9k/year, ฿750/month)
  Target: ฿10k/month (฿120k/year)
  Required yield: 6.7%

  Status: 🔴 Far behind
  Gap: need to shift to high-dividend stocks or increase portfolio
  Note: Your growth stocks (NVDA, GOOGL) don't pay dividends

  ── Suggested Adjustments ─────────────────────────────────────────
  1. Add ฿25k/month contributions to stay on track
  2. Consider dividend stocks for income goal (KBANK pays 3-4%)
  3. Don't chase returns — consistent beats aggressive
```

---

## Guards

- **Be realistic**: Don't promise returns you can't deliver
- **Show multiple paths**: Growth-only, contributions, extended timeline
- **Don't pressure**: Goals are guides, not deadlines
- **Adjust when needed**: Life changes, goals can change too
- **Celebrate progress**: 60% of the way is still progress

## Tools used

- `dr.py portfolio` — current value
- `dr.py performance` — historical returns
- File read/write — `.deep-rich/goals.json`
