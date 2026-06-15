# briefing

Event-driven quick check — what happened to YOUR portfolio since last check.

## When to use

- After market events (earnings, WWDC, Fed meeting, geopolitical news)
- When user asks "what happened" / "any news" / "how's my portfolio doing"
- When user mentions a specific event that might affect holdings

**Not** for weekly reviews — use `review` for that.

## Workflow

### Step 1: Get current holdings

```bash
cd "$DEEP_RICH_HOME"
python3 scripts/dr.py portfolio
```

Extract the list of symbols you own.

### Step 2: Check recent price moves

```bash
python3 scripts/dr.py prices
python3 scripts/dr.py performance
```

Note any big moves (>5% in a day or since last check).

### Step 3: Search news for YOUR holdings

For each holding with significant news:

```
web_search: "[SYM] stock news this week"
web_search: "[SYM] earnings report"
```

For the specific event the user mentioned:

```
web_search: "[event] impact on stocks"
web_search: "[event] announcements"
```

Filter: only news that affects YOUR holdings. Don't report on stocks you don't own.

### Step 4: Synthesize

Present in this order:

```
══════════════════════════════════════════════════════════════════════
  📰 Briefing — [Event/Date]
══════════════════════════════════════════════════════════════════════

  Since your last check ([X] days ago):
  Portfolio: ฿+/-X (+/-Y%)

  ── Big Moves ─────────────────────────────────────────────────────
  [List holdings with >5% moves]

  ── News That Matters ─────────────────────────────────────────────
  [Only news affecting YOUR holdings]

  ── Action Needed? ────────────────────────────────────────────────
  [If any news requires action: buy, sell, or hold]
```

## Example: Post-WWDC briefing

```
══════════════════════════════════════════════════════════════════════
  📰 Briefing — Post-WWDC 2026
══════════════════════════════════════════════════════════════════════

  Since your last check (3 days ago):
  Portfolio: ฿+45,230 (+2.5%)

  ── Big Moves ─────────────────────────────────────────────────────
  NVDA: +8.2% ($209 → $226) — earnings beat expectations
  GOOGL: +3.1% — Gemini 2.0 launched, competing with OpenAI
  MSFT: +1.2% — Azure AI partnerships announced

  ── News That Matters ─────────────────────────────────────────────
  NVDA: Data center demand exceeding expectations. Your +262% gain
        continues. Consider profit-taking (see review).
  GOOGL: Gemini 2.0 launch could accelerate cloud revenue.
         Your +183% gain. Watch for Q2 earnings.
  MSFT: Azure AI partnerships with OpenAI expanding.
         Your +10% gain. Thesis intact.

  ── Action Needed? ────────────────────────────────────────────────
  No immediate action. Your US tech holdings benefited from AI
  momentum. Next review: check if profit-taking thresholds hit.

  Note: KBANK not affected by WWDC. Thai market separate story.
```

## Example: Market crash briefing

```
══════════════════════════════════════════════════════════════════════
  📰 Briefing — Market Selloff
══════════════════════════════════════════════════════════════════════

  Since yesterday:
  Portfolio: ฿-89,000 (-5.0%)

  ── Big Moves ─────────────────────────────────────────────────────
  NVDA: -12% — profit-taking after earnings
  GOOGL: -8% — sector rotation out of tech
  MSFT: -6% — broad market selloff
  KBANK: -3% — regional bank concerns

  ── News That Matters ─────────────────────────────────────────────
  Market: Fed signals higher-for-longer rates. Tech selling off.
  NVDA: No company-specific news. Sector-wide rotation.
  KBANK: Bank of Thailand holds rates. Neutral for banks.

  ── Action Needed? ────────────────────────────────────────────────
  No panic selling. This is sector rotation, not fundamental damage.

  Your health grades: NVDA (A), GOOGL (A), MSFT (B). All healthy.

  Opportunity? If you have cash, this could be a buying opportunity.
  Your Cash: ฿991k (55% of portfolio). Deploy some?
```

## Guards

- **Don't alarm**: A 3% drop isn't a crisis. Context matters.
- **Filter noise**: Not every news item matters. Only report what affects YOUR holdings.
- **No action without reason**: If no action is needed, say so clearly.
- **Respect the user's time**: Briefing should be quick — 30 seconds to read.

## Tools used

- `dr.py portfolio` — current holdings
- `dr.py prices` — latest prices
- `dr.py performance` — gains/losses
- `dr.py news <SYM>` — news for specific holdings
- `web_search` — news search for events
- `agent_browser` — if user wants to check specific pages (earnings call, event page)
