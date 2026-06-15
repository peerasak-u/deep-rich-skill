---
name: deep-rich
description: Portfolio manager for Thai SET, US stocks, Crypto, Gold, and Cash. Use when asking about portfolio status, allocation drift, stock fundamentals, deployment plans, investment decisions, rebalancing, or performance tracking.
---

# Deep Rich Portfolio Manager

Private banking for normal people. A weekly portfolio review ritual with decision support, profit-taking signals, and opportunistic rebalancing.

## Agent Contract

This skill is the agent workflow layer. The portfolio manager app and private data live outside this skill repo.

The user-facing contact point is always **human → agent**. Do not tell users to run `dr.py` commands as the primary interface. Infer their intent from natural language, run the required scripts underneath the workflow, then explain results and next choices in human terms.

For generated HTML artifacts, follow the shared report design system in [DESIGN](references/DESIGN.md). Keep visual reports consistent with the Deep Rich dashboard theme and label facts, calculations, estimates, interpretations, and unknowns clearly.

Before any advice workflow:

1. Resolve the portfolio app root (`DEEP_RICH_HOME`, current app directory, or sibling `../deep-rich`).
2. Verify it contains both `scripts/dr.py` and `.deep-rich/`.
3. Run `python3 scripts/dr.py doctor` as an internal readiness gate.
4. If doctor reports `blocked`, stop and help fix/onboard data before recommending portfolio actions.
5. If prices are stale or missing, run `python3 scripts/dr.py prices` internally before interpreting the portfolio.
6. Optionally run `skills/deep-rich/scripts/signals.py` for context-aware alerts when available.

## Routing

Map the user's intent to the right workflow. Don't ask which command and don't expose scripts as the UX — infer from what they said.

| User says | Workflow | Reference |
|-----------|----------|-----------|
| "setup my portfolio" / "start Deep Rich" / "onboard me" | `onboard` | [onboard](references/commands/onboard.md) |
| "is my data okay" / "health check" / "doctor" | `doctor` | [doctor](references/commands/doctor.md) |
| "how's my portfolio" / "what should I do" / "review" | `review` | [review](references/commands/review.md) |
| "what happened" / "any news" / "how's my portfolio after [event]" | `briefing` | [briefing](references/commands/briefing.md) |
| "update skills" / "sync skills" / "refresh deep-rich" | `update` | [update](references/commands/update.md) |
| "I onboarded holdings / finish setup" | `onboard` → `doctor` → profile backfill via `research <SYM>` for held stocks | [onboard](references/commands/onboard.md), [research](references/commands/research.md) |
| "I have cash, where should I put it" / "deployment" | `deploy` | [deploy](references/commands/deploy.md) |
| "should I rebalance" / "how do I fix my allocation" | `rebalance mechanical` | [rebalance](references/commands/rebalance.md) |
| "I want to rotate [losers] to [opportunity]" | `rebalance rotate` | [rebalance](references/commands/rebalance.md) |
| "why did I buy X" / "what was my thesis" / "log this decision" | `journal` | [journal](references/commands/journal.md) |
| "what's my risk" / "what could hurt me" | `risk` | [risk](references/commands/risk.md) |
| "am I on track" / "when will I hit X" / "set a goal" | `goals` | [goals](references/commands/goals.md) |

### Multi-workflow patterns

Some requests need chaining. Load multiple references:

| Intent | Chain |
|--------|-------|
| "should I buy more MSFT" | `research MSFT` → check allocation → `deploy` → reason |
| "portfolio review + what to buy" | `review` → `deploy` → synthesize |
| "cut my losers and buy data center" | `rebalance rotate` → `research EGCO` → synthesize |

## Internal Workflow Commands

These names are for agents reading this skill, tests, and workflow documentation. They are not the user's interface; the user's interface is a conversation with the agent.

| Command | Category | Description | Reference |
|---------|----------|-------------|-----------|
| `onboard` / `setup` | Bootstrap | Trust-first setup, fresh discovery, or existing asset-by-asset capture | [onboard](references/commands/onboard.md) |
| `doctor` | Bootstrap | Read-only data health + advice readiness check | [doctor](references/commands/doctor.md) |
| `review` | Weekly | Portfolio health + profit-taking + loss-cutting + actions | [review](references/commands/review.md) |
| `briefing` | Event | Quick "what happened to my money" after events | [briefing](references/commands/briefing.md) |
| `update` | Maintenance | Sync skills from deep-rich-skill repo | [update](references/commands/update.md) |
| `research <SYM>` | Decision / Data prep | Stock analysis with bull/bear/verdict; creates reusable `.deep-rich/companies/<SYM>.json` and visual `company/<symbol>.html` profiles after onboarding | [research](references/commands/research.md) |
| `deploy` | Decision | Cash deployment to underweight classes | [deploy](references/commands/deploy.md) |
| `rebalance` | Decision | Mechanical or rotate rebalancing | [rebalance](references/commands/rebalance.md) |
| `journal` | Reflection | Decision tracking + pattern recognition | [journal](references/commands/journal.md) |
| `risk` | Review | Concentration, quality, market risk assessment | [risk](references/commands/risk.md) |
| `goals` | Planning | Goal tracking + trajectory analysis | [goals](references/commands/goals.md) |

### Script tools

These CLI commands are implementation details used by workflows — not directly by users:

| Command | Used by | Purpose |
|---------|---------|---------|
| `dr.py onboard` | setup | Guided fresh discovery or existing portfolio capture |
| `dr.py setup` | setup | Alias for `onboard` |
| `dr.py doctor` | all | Read-only data health + readiness gate |
| `dr.py portfolio` | review, briefing, deploy | Current state + drift |
| `dr.py performance` | review, journal | Gains/losses by holding |
| `dr.py health <SYM>` | research, rebalance | Health grade |
| `dr.py health watchlist` | review, rebalance | All health grades |
| `dr.py fundamentals <SYM>` | research | Valuation, financials |
| `dr.py deployment` | review, deploy | Cash allocation plan |
| `dr.py prices` | all | Fresh price data |
| `dr.py thai-561 <SYM>` | fundamentals | Thai SEC 56-1 data + download URL |
| `signals.py` | review | Context-aware alerts |
| `export_dashboard.py` | — | HTML dashboard |
| `export_company_profile.py` | research | Company profile HTML from JSON + template |

### Quick Examples

```bash
# Bootstrap / trust checks
"setup my portfolio"           → runs onboard workflow
"I already have some holdings" → runs onboard --existing flow
"is my data okay?"             → runs doctor workflow

# Weekly ritual
"review my portfolio"          → runs review workflow
"what should I do this week?"  → runs review workflow

# After events
"any news after WWDC?"         → runs briefing workflow
"how's my portfolio doing?"    → runs briefing workflow

# Decision support
"should I buy EGCO?"           → runs research workflow
"I have ฿200k to invest"       → runs deploy workflow

# Rebalancing
"rebalance my portfolio"       → runs rebalance mechanical
"rotate my losers to data center" → runs rebalance rotate

# Reflection
"why did I buy NSL?"           → runs journal workflow
"what's my biggest risk?"      → runs risk workflow
"am I on track for ฿3M?"       → runs goals workflow
```

## Profit-Taking Rules

The NSL lesson: +60% → +0.2% without taking profit. These rules prevent that:

| Gain | Action | Rule |
|------|--------|------|
| > +100% | **Strongly consider selling 50%** | Take initial investment off the table |
| > +50% | **Consider trimming 25-50%** | Lock in gains, let rest ride |
| > +30% | **Watch closely** | Set mental trailing stop |

These are suggestions, not mandates. The user decides.

## Loss-Cutting Rules

| Health | Loss | Action |
|--------|------|--------|
| F | Any | **Cut losses** — sell within 1 month |
| D | > -20% | **Seriously consider cutting** — thesis likely broken |
| D | < -20% | **Watch closely** — set alert |
| C | > -30% | **Review thesis** — is the story still valid? |

## Asset Classes

| Class | Target | Currency | Behavior |
|-------|--------|----------|----------|
| Thai SET | 25% | THB | Active — grow toward target |
| US Market | 35% | USD | Active — growth engine |
| Crypto | 10% | USD | Active — BTC+ETH bucket |
| Gold | 10% | THB | Passive — hold steady |
| Cash | 20% | THB+USD | Active — deploy source |

## Drift Indicators

| Icon | Range | Meaning |
|------|-------|---------|
| 🟢 | < 5% | On track |
| 🟡 | 5-15% | Needs attention |
| 🔴 | > 15% | Significant rebalancing |

## Guards

Hard rules. Enforce these on every workflow.

### Trust-first onboarding
- If the user has no idea what to invest in, **do not force investing**. Help them discover assets, risks, and thesis candidates.
- Existing portfolio setup is **asset-by-asset**. Ask "tell me one thing you currently hold"; never demand a full holdings list.
- Missing thesis is acceptable. Mark it as unknown and research before buy/sell pressure.
- Run `dr.py doctor` before serious advice. If advice mode is `blocked`, fix data first.

### Emergency floor
- **฿300,000 THB** — never recommend deploying below this threshold
- If deployment plan would breach the floor, reduce allocation and warn

### Stale data
- Prices older than 24 hours: **warn before interpreting**
- Snapshot without fresh prices: **always run `dr.py prices` first**
- If price fetch fails, show last-known prices with timestamp and caveat

### Currency display
- **All aggregates in THB** — the portfolio total, drift, deployment
- When showing individual US/crypto positions, include both USD and THB
- FX rate: show USD/THB rate used for conversion

### Position sizing
- If any single stock exceeds **15% of its asset class**, flag it
- If any single stock exceeds **5% of total portfolio**, flag it
- Don't recommend selling — just surface the concentration risk

### Gold is passive
- Never recommend buying or selling gold for rebalancing
- Gold drift is informational only

### Cash is the source
- Cash is where deployment funds come from, not a rebalancing target
- Never recommend "increase cash allocation"

### Don't force actions
- Suggest, don't pressure. It's their money.
- Show your work: always show the numbers behind each suggestion
- Respect the user's decision even if you disagree

## News Discovery (Agentic)

**Use the agent's native tools for news — not `dr.py news`.** Modern models can:
- Search multiple sources simultaneously
- Understand context, sarcasm, nuance
- Read full articles, not just titles
- Adapt to what's relevant for the situation

### Default: `web_search`

```
web_search: "[COMPANY] stock news today"
web_search: "[COMPANY] earnings [QUARTER]"
web_search: "[COMPANY] [EVENT] impact"
```

For Thai stocks:
```
web_search: "[THAI COMPANY] ข่าวหุ้น ล่าสุด"
```

### Deep Dive: `agent_browser`

Open specific pages for detailed research:
- Investor relations / earnings press releases
- SEC filings (10-K, 10-Q)
- SET or SEC Thailand filings
- Reddit, Twitter/X for retail sentiment

### When to use each

| Need | Tool |
|------|------|
| Quick pulse check | `web_search` x2-3 |
| Event impact (earnings, WWDC) | `web_search` + synthesis |
| Deep research before buy/sell | `agent_browser` open links |
| Thai stock with limited English | `web_search` + Thai terms |
| Sentiment from discussions | `web_search` for Reddit/Twitter |

### Conviction Test (Agentic)

The `conviction_test.py` script tests whether your investment thesis is still valid.

**The good parts** (keep as script):
- Price performance checks (1Y return)
- P&L calculation from buy price
- Verdict algorithm (INTACT/DAMAGED/BROKEN/UNCERTAIN)

**Improved** (agentic news):
- News sentiment now uses `web_search` instead of keyword matching
- Use `test_conviction_with_sentiment()` with agentic results

**Agent workflow for conviction test:**
```
1. web_search: "[SYM] stock news this week"
2. Analyze sentiment natively (context, nuance, risks)
3. Call conviction test with results:
   agentic_sentiment = {
       "overall": "positive",  # positive/negative/neutral/mixed
       "positive_count": 5,
       "negative_count": 1,
       "key_findings": ["AI growth", "earnings beat"],
       "risks_mentioned": ["competition"]
   }
   test_conviction_with_sentiment(SYM, thesis, holding, agentic_sentiment)
```

### Old `news.py` (Deprecated)

The `scripts/news.py` script used Google News RSS + keyword matching.
**It's deprecated.** Use agentic tools instead for better context understanding.

| Market | Source | Data |
|--------|--------|------|
| Thai SET | Yahoo Finance (.BK) | Price, 52W range |
| Thai SET | SET Factsheet | P/E, P/BV, Market Cap, ESG |
| Thai SET | Thai SEC 56-1 | Financial statements, ratios, dividends |
| Thai SET | Thai SEC (via browser) | Download PDF from market.sec.or.th |
| US Market | Yahoo Finance | Price, 52W range |
| US Market | SEC EDGAR | 10-K/10-Q, XBRL financials |
| Crypto | CoinGecko | BTC, ETH prices |
| FX | Open Exchange Rates | USD/THB |

## Files

All portfolio artifacts live in the portfolio manager app's `.deep-rich/` directory:

| File | Purpose |
|------|--------|
| `.deep-rich/portfolio.json` | Edit to add/modify holdings |
| `.deep-rich/config.json` | Settings (emergency floor) |
| `.deep-rich/prices.json` | Cached prices (auto-updated) |
| `.deep-rich/snapshots/` | Portfolio snapshots (on `--snapshot`) |
| `.deep-rich/journal.md` | Decision journal |
| `.deep-rich/goals.json` | Financial goals |
| `.deep-rich/data/thesis.json` | Captured asset thesis + conviction |
| `.deep-rich/onboarding/` | Onboarding drafts + backups |
| `.deep-rich/reviews/` | Saved portfolio reviews |
| `.deep-rich/companies/` | Company research profiles (JSON) |
| `CONTEXT.md` | Domain glossary |
| `scripts/dr.py` | Main CLI in the portfolio manager app |
| `scripts/fundamentals.py` | SEC EDGAR + Yahoo in the portfolio manager app |
| `scripts/export_dashboard.py` | Dashboard export in the portfolio manager app |
| `scripts/export_company_profile.py` | Company profile HTML export in the portfolio manager app |
| `dashboard/dashboard.html` | Self-contained dashboard in the portfolio manager app |
| `company/<sym>.html` | Visual company profile generated from JSON + template |
| `skills/deep-rich/` | This skill package; keep agent workflow docs and helpers here |

## References

- [Onboard](references/commands/onboard.md) — Trust-first setup and discovery
- [Doctor](references/commands/doctor.md) — Data health + advice readiness
- [Command docs](references/commands/) — Workflow-specific command documentation
- [Data Sources](references/DATA-SOURCES.md) — API details and setup
