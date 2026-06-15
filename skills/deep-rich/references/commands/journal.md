# journal

Decision tracking — log why you bought/sold, review past decisions, find patterns.

## When to use

- After any buy/sell decision (log the reasoning)
- When user asks "why did I buy X" / "what was my thesis"
- Monthly review (check outcomes vs thesis)
- When user wants to learn from mistakes

## Journal file

Location: `.deep-rich/journal.md`

Format:

```markdown
# Decision Journal

## YYYY-MM-DD — BUY/SELL/HOLD <SYM>

**Price:** $X
**Amount:** ฿X (N shares)
**Thesis:** [Why you bought/sold]
**Risk:** [What could go wrong]
**Target:** [Price target or condition to sell]

### Outcome (updated later)
**Current price:** $X
**Gain/Loss:** +/-X%
**Thesis valid?** [Yes/No/Partially]
**Lesson:** [What you learned]
```

---

## Logging workflow

When user makes a buy/sell decision:

### Step 1: Gather context

```bash
cd "$DEEP_RICH_HOME"
python3 scripts/dr.py fundamentals <SYM>
python3 scripts/dr.py health <SYM>
```

### Step 2: Ask for thesis

Ask the user:
- Why are you buying/selling?
- What's your price target?
- What would make you sell?
- What's the risk?

### Step 3: Write journal entry

Append to `.deep-rich/journal.md`:

```markdown
## YYYY-MM-DD — BUY <SYM>

**Price:** $X
**Amount:** ฿X (N shares)
**Thesis:** [User's reasoning]
**Risk:** [What could go wrong]
**Target:** [When to take profit or cut loss]
**Health grade:** [A/B/C/D/F]
**Allocation:** [Current % of class]
```

---

## Review workflow

When user asks to review past decisions:

### Step 1: Read journal

Read `.deep-rich/journal.md`

### Step 2: Check outcomes

For each decision:
```bash
python3 scripts/dr.py performance
```

Calculate:
- Gain/loss since decision
- Whether thesis is still valid
- Whether risk materialized

### Step 3: Identify patterns

Analyze:
- **Win rate**: % of profitable decisions
- **Average winner**: avg gain on winners
- **Average loser**: avg loss on losers
- **Biggest mistake**: worst decision and why
- **What works**: patterns in winning decisions
- **What doesn't**: patterns in losing decisions

### Step 4: Synthesize

```
══════════════════════════════════════════════════════════════════════
  📝 Decision Journal Review
══════════════════════════════════════════════════════════════════════

  ── Recent Decisions ──────────────────────────────────────────────

  May 15, 2026 — BUY MSFT @ $380
  Thesis: "AI infrastructure play, Azure growing 30%+"
  Since then: -4% ($380 → $365)
  Status: Thesis still valid ✅

  Mar 20, 2026 — BUY NVDA @ $56 (split-adj)
  Thesis: "Data center GPU demand, AI training"
  Since then: +262% ($56 → $209)
  Status: ⚠️ Consider taking profit

  Jan 10, 2026 — HOLD NSL (didn't sell at +60%)
  Reason: "Letting winners run"
  Since then: +0.2% (peak was +60%)
  Lesson: ⚠️ Should have trimmed at +50%

  ── Patterns ──────────────────────────────────────────────────────
  📊 Win rate: 67% (8/12 trades profitable)
  📊 Avg winner: +45%
  📊 Avg loser: -28%
  📊 Biggest mistake: Not taking profit on NSL

  ── What You Do Well ─────────────────────────────────────────────
  ✅ Good at finding quality (NVDA, GOOGL, MSFT)
  ✅ Good at holding through volatility

  ── What to Work On ──────────────────────────────────────────────
  ⚠️ Take profit when up >50%
  ⚠️ Cut losers faster (don't hold F-grade stocks)
```

---

## Example: Logging a buy decision

User: "I'm buying EGCO because data center trend"

```
══════════════════════════════════════════════════════════════════════
  📝 Log Decision: BUY EGCO
══════════════════════════════════════════════════════════════════════

  Current price: ฿185
  Your order: ฿50,000 (270 shares)
  Health grade: B
  Thai SET allocation: 6.0% → 8.5%

  ── Your Thesis ───────────────────────────────────────────────────
  "Data center trend in Thailand needs power. EGCO is Thailand's
  largest private power producer. Renewable + traditional = stable."

  ── Risk ──────────────────────────────────────────────────────────
  "Regulated industry, government policy could change."

  ── Target ────────────────────────────────────────────────────────
  "Hold for 2-3 years. Sell if health drops to D or thesis breaks."

  ── Saved ─────────────────────────────────────────────────────────
  ✅ Logged to .deep-rich/journal.md
  📅 Review in 3 months (September 2026)
```

---

## Guards

- **Always log**: Every buy/sell should have a journal entry
- **Be honest**: Log the real reasoning, not post-hoc rationalization
- **Review regularly**: Check outcomes monthly
- **Learn from mistakes**: Don't repeat the same errors
- **No judgment**: The journal is for learning, not self-criticism

## Tools used

- `dr.py fundamentals <SYM>` — context for decision
- `dr.py health <SYM>` — quality check
- `dr.py performance` — check outcomes
- File read/write — `.deep-rich/journal.md`
- `web_search` — news discovery for conviction tests
- `test_conviction_with_sentiment()` — conviction test with agentic sentiment
