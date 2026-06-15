# review

Weekly portfolio review — the private banking ritual. Your one-command portfolio health check with specific actions.

## When to use

- Every week (check last review date in `.deep-rich/reviews/`)
- When user asks "how's my portfolio" / "what should I do" / "review my portfolio"
- When user hasn't reviewed in >7 days (remind them)

## Workflow

### Step 1: Gather data

```bash
cd "$DEEP_RICH_HOME"

# Portfolio overview + drift
python3 scripts/dr.py portfolio

# Health grades for all holdings
python3 scripts/dr.py health watchlist

# Performance (gains/losses by holding)
python3 scripts/dr.py performance

# Deployment plan (where cash should go)
python3 scripts/dr.py deployment
```

### Step 2: Apply profit-taking rules

For each holding, calculate gain from cost basis. Flag:

| Gain | Action | Rule |
|------|--------|------|
| > +100% | **Strongly consider selling 50%** | Take initial investment off the table |
| > +50% | **Consider trimming 25-50%** | Lock in gains, let rest ride |
| > +30% | **Watch closely** | Set mental trailing stop |

When suggesting profit-taking, always show:
- Current gain (% and ฿)
- What selling 25%/50% would look like
- Where the money could go (deployment plan)
- **Macro context**: industry trends, tariff impacts, sector headwinds/tailwinds
- **Research highlights + warnings** from health analysis
- **Original thesis** and whether it's still valid
- **Conviction checklist**: pass/fail items (thesis valid? margins healthy? catalyst ahead? valuation reasonable?)

### Step 3: Apply loss-cutting rules

For each holding, check health grade and loss:

| Health | Loss | Action |
|--------|------|--------|
| F | Any | **Cut losses** — sell within 1 month |
| D | > -20% | **Seriously consider cutting** — thesis likely broken |
| D | < -20% | **Watch closely** — set alert |
| C | > -30% | **Review thesis** — is the story still valid? |

When suggesting cuts, always show:
- Current loss (% and ฿)
- What cutting would recover
- **Macro context**: industry trends, tariff impacts, macro headwinds that affect the thesis
- **Research highlights + warnings** from health analysis
- **Original thesis** and why it's broken
- **Conviction checklist**: pass/fail items showing exactly what failed
- What the health grade signals mean

### Step 4: Check drift

| Drift | Action |
|-------|--------|
| > 15% (🔴) | **Rebalancing needed** — calculate specific amounts |
| 5-15% (🟡) | **Monitor** — mention but don't force action |
| < 5% (🟢) | **On track** — no action needed |

If Cash > 20% above target, calculate deployable amount (above emergency floor).

### Step 5: Synthesize

Present in this order:

```
══════════════════════════════════════════════════════════════════════
  📋 Weekly Review — [Date]
══════════════════════════════════════════════════════════════════════

  Portfolio: ฿X (+Y% all-time)
  vs Last Week: ฿+/-X (+/-Y%)
  vs Benchmark: [if available]

  ── 🎯 Profit-Taking Candidates ─────────────────────────────────
  [List stocks up >50% with suggested trim amounts]

  ── 🚨 Loss-Cutting Candidates ──────────────────────────────────
  [List F/D grade stocks with losses]

  ── 📊 Drift Status ──────────────────────────────────────────────
  [Show drift with deployment suggestions]

  ── 💡 Suggested Actions ─────────────────────────────────────────
  [Numbered list of specific actions with amounts]
```

### Step 6: Generate HTML review

After synthesizing the review, generate an interactive HTML page:

```bash
# Pipe review data as JSON to export_review.py
cd "$DEEP_RICH_HOME"
python3 scripts/dr.py export-review < /tmp/review-data.json --open
```

The HTML review provides:
- Visual stat cards (portfolio value, deployable cash, health distribution)
- Side-by-side profit-taking vs loss-cutting action cards
- Holdings table with health grade badges and gain/loss coloring
- Allocation drift bars with current vs target
- Print-friendly layout

Save the review data as JSON with this structure. Each stock memo includes research, thesis, and conviction checklist:

```json
{{
  "date": "YYYY-MM-DD",
  "portfolio": {{ "total_thb": N, "total_usd": N, "all_time_return": N, "fx_rate": N }},
  "profit_take": [
    {{
      "symbol": "NVDA",
      "gain_pct": 268.3,
      "position_label": "฿123k · cost ฿33k",
      "action": "Sell 50%",
      "proceeds": 61000,
      "reason": "Detailed reasoning for the action...",
      "macro_context": [
        {{"claim": "AI capex cycle: hyperscalers increasing AI spend", "source": "MSFT/GOOGL Q1 2026 earnings calls"}},
        {{"claim": "US-China tensions: export restrictions", "source": "US Commerce Dept, Oct 2024 rules"}}
      ],
      "research": {{
        "grade": "A",
        "highlights": [
          {{"claim": "Revenue +61% YoY", "source": "SEC 10-Q, Q1 2026"}}
        ],
        "warnings": [
          {{"claim": "P/E elevated", "source": "Yahoo Finance, forward P/E"}}
        ]
      }},
      "conviction": {{
        "thesis": "Original investment thesis...",
        "level": "high|medium|low|broken",
        "original_date": "2024-08"
      }},
      "checklist": [
        {{ "label": "Thesis still valid?", "pass": true }},
        {{ "label": "Position too large?", "pass": false }}
      ]
    }}
  ],
  "loss_cut": [/* same structure as profit_take */],
  "holdings_action": [/* holds with conviction checks */],
  "drift": [{{ "class": "X", "current_pct": N, "target_pct": N }}],
  "deployment": {{ "deployable": N }},
  "actions": ["action 1", "action 2"],
  "notes": ["note 1", "note 2"]
}}
```

The HTML output is a blog-style investment memo:
- Each stock gets its own card with thesis, research, and conviction checklist
- Checklist items show pass/fail with visual indicators
- Conviction levels (high/medium/low/broken) are color-coded
- Drift bars show current vs target allocation
- Print-friendly for paper reviews

### Step 7: Log review (markdown backup)

Also save review summary to `.deep-rich/reviews/YYYY-MM-DD.md`:

```markdown
# Review — YYYY-MM-DD

## Portfolio Summary
- Total: ฿X
- Change since last review: +/-฿X

## Actions Taken
- [List any actions user agreed to]

## Actions Pending
- [List suggested actions]

## Notes
- [Any observations]
```

### Step 8: Log decisions to journal

If the user agrees to any buy/sell actions during the review, log each one to `.deep-rich/journal.md`:

```markdown
## YYYY-MM-DD — BUY/SELL <SYM>

**Price:** $X
**Amount:** ฿X (N shares)
**Thesis:** [Why — from the review]
**Risk:** [What could go wrong]
**Health grade:** [A/B/C/D/F]
```

Don't skip this. Every decision needs a record. The NSL lesson happened because there was no journal.

## Guards

- **Emergency floor**: Never suggest deploying below ฿300k
- **Gold is passive**: Never suggest rebalancing gold
- **Don't force actions**: Suggest, don't pressure. It's their money.
- **Show your work**: Always show the numbers behind each suggestion
- **No selling pressure**: If a stock is up 60% and they want to hold, respect it. Mention the option, don't push.

## Reference data

The review uses these internal commands:
- `portfolio` — current state, drift
- `health watchlist` — all health grades
- `performance` — gains/losses by holding
- `deployment` — where cash should go
- `signals.py` — context-aware alerts

## Example output

```
══════════════════════════════════════════════════════════════════════
  📋 Weekly Review — June 8, 2026
══════════════════════════════════════════════════════════════════════

  Portfolio: ฿1,793,324 (+16.4% all-time)
  vs Last Week: ฿+12,340 (+0.7%)

  ── 🎯 Profit-Taking Candidates ─────────────────────────────────
  NVDA: +262% ($56 → $209) — ฿120,509 position
    💡 Sell 50% (฿60k) → take initial investment off table
    💡 Let remaining ฿60k ride as "house money"

  GOOGL: +183% ($130 → $363) — ฿108,659 position
    💡 Sell 25% (฿27k) → lock in gains

  KBANK: +61% (฿125 → ฿201) — ฿40,200 position
    💡 Hold — Thai SET is underweight, keep for allocation

  ── 🚨 Loss-Cutting Candidates ──────────────────────────────────
  SISB: -43%, Health: F
    💡 Cut losses — sell ฿10,890, recover capital
    💡 Use proceeds to deploy to Thai SET (still underweight)

  AAI: -37%, Health: F
    💡 Cut losses — sell ฿7,080

  AMPH: -61%, Health: D
    💡 Seriously consider cutting — ฿25,422 at risk
    💡 Revenue declining -36.9%, thesis likely broken

  ── 📊 Drift Status ──────────────────────────────────────────────
  🔴 Cash: 55.3% (target 20%) — ฿691k deployable
  🔴 Thai SET: 6.0% (target 25%) — need ฿340k more
  🟡 US Market: 24.9% (target 35%) — need ฿178k more
  🟢 Crypto: 6.1% (target 10%) — need ฿70k more
  🟢 Gold: 7.8% (target 10%) — passive, no action

  ── 💡 Suggested Actions ─────────────────────────────────────────
  1. Trim NVDA: sell ฿60k (take profit, +262%)
  2. Cut SISB + AAI: recover ฿18k (stop losses, F-grade)
  3. Deploy ฿200k to Thai SET (KBANK or new opportunity)
  4. Deploy ฿100k to US Market (MSFT or GOOGL)
  5. Research: data center trend — EGCO, GPSC, BGRIM?

  📁 Review saved to .deep-rich/reviews/2026-06-08.md
```
