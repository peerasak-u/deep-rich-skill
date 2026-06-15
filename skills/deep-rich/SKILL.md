---
name: deep-rich
description: Portfolio manager for Thai SET, US stocks, Crypto, Gold, and Cash. Use when asking about portfolio status, allocation drift, stock fundamentals, deployment plans, investment decisions, rebalancing, or performance tracking.
---

# Deep Rich Portfolio Manager

Private banking for normal people. A weekly portfolio review ritual with decision support, profit-taking signals, and opportunistic rebalancing.

## Agent Contract

This skill is the agent workflow layer. The portfolio manager app and private data live outside this skill repo.

The user-facing contact point is always **human → agent**. Do not tell users to run `dr.py` commands as the primary interface. Infer their intent from natural language, run the required scripts underneath the workflow, then explain results and next choices in human terms.

For generated HTML artifacts, follow [DESIGN](references/DESIGN.md). Label facts, calculations, estimates, interpretations, and unknowns clearly.

Before any advice workflow:

1. Resolve the portfolio app root (`DEEP_RICH_HOME`, current app directory, or sibling `../deep-rich`).
2. Verify it contains both `scripts/dr.py` and `.deep-rich/`.
3. Run `python3 scripts/dr.py doctor` as an internal readiness gate.
4. If doctor reports `blocked`, stop and help fix/onboard data before recommending portfolio actions.
5. If prices are stale or missing, run `python3 scripts/dr.py prices` internally before interpreting the portfolio.
6. Optionally run `skills/deep-rich/scripts/signals.py` for context-aware alerts when available.

## Guards

Enforce [GUARDS](references/GUARDS.md) on every workflow. Summary:

- Trust-first onboarding — no forced investing; asset-by-asset capture; doctor gate before advice
- **฿300,000 THB** emergency floor — never deploy below
- Stale prices (>24h) — warn and refresh when possible
- Aggregates in THB; US/crypto positions show native currency too
- Flag concentration (>15% of class, >5% of portfolio) — don't force sells
- Gold is passive; cash is deployment source, not a rebalancing target
- Suggest, don't pressure — show the numbers

Load workflow-specific guards from the active command reference when they add local rules.

## Routing

Map intent to workflow. Don't ask which command — infer from what they said, load the reference, execute.

**Disambiguation:** weekly ritual or "what should I do" → `review`. Event-driven pulse ("after WWDC", "any news today") → `briefing`.

| User says | Workflow | Category | Reference |
|-----------|----------|----------|-----------|
| "setup my portfolio" / "start Deep Rich" / "onboard me" | `onboard` | Bootstrap | [onboard](references/commands/onboard.md) |
| "is my data okay" / "health check" / "doctor" | `doctor` | Bootstrap | [doctor](references/commands/doctor.md) |
| "how's my portfolio" / "what should I do" / "review" | `review` | Weekly | [review](references/commands/review.md) |
| "what happened" / "any news" / "how's my portfolio after [event]" | `briefing` | Event | [briefing](references/commands/briefing.md) |
| "should I buy X" / "is X worth buying" / "research EGCO" | `research <SYM>` | Decision | [research](references/commands/research.md) |
| "I have cash, where should I put it" / "deployment" | `deploy` | Decision | [deploy](references/commands/deploy.md) |
| "should I rebalance" / "how do I fix my allocation" | `rebalance mechanical` | Decision | [rebalance](references/commands/rebalance.md) |
| "I want to rotate [losers] to [opportunity]" | `rebalance rotate` | Decision | [rebalance](references/commands/rebalance.md) |
| "why did I buy X" / "what was my thesis" / "log this decision" | `journal` | Reflection | [journal](references/commands/journal.md) |
| "what's my risk" / "what could hurt me" | `risk` | Review | [risk](references/commands/risk.md) |
| "am I on track" / "when will I hit X" / "set a goal" | `goals` | Planning | [goals](references/commands/goals.md) |
| "update skills" / "sync skills" / "refresh deep-rich" | `update` | Maintenance | [update](references/commands/update.md) |
| "I onboarded holdings / finish setup" | `onboard` → `doctor` → `research <SYM>` backfill | Bootstrap | [onboard](references/commands/onboard.md), [research](references/commands/research.md) |

### Multi-workflow patterns

| Intent | Chain |
|--------|-------|
| "should I buy more MSFT" | `research MSFT` → check allocation → `deploy` → reason |
| "portfolio review + what to buy" | `review` → `deploy` → synthesize |
| "cut my losers and buy data center" | `rebalance rotate` → `research EGCO` → synthesize |

## Script tools

CLI implementation details — not the user interface:

| Command | Used by | Purpose |
|---------|---------|---------|
| `dr.py onboard` / `setup` | onboard | Fresh discovery or existing portfolio capture |
| `dr.py doctor` | all | Data health + readiness gate |
| `dr.py portfolio` | review, briefing, deploy | Current state + drift |
| `dr.py performance` | review, journal | Gains/losses by holding |
| `dr.py health <SYM>` / `watchlist` | research, review, rebalance | Health grades |
| `dr.py fundamentals <SYM>` | research | Valuation, financials |
| `dr.py deployment` | review, deploy | Cash allocation plan |
| `dr.py prices` | all | Fresh price data |
| `dr.py thai-561 <SYM>` | fundamentals | Thai SEC 56-1 data |
| `signals.py` | review | Context-aware alerts |
| `export_dashboard.py` | dashboard | HTML dashboard |
| `export_company_profile.py` | research | Company profile HTML |

## References

Load on demand — do not preload every workflow doc.

| Topic | Reference |
|-------|-----------|
| Hard rules | [GUARDS](references/GUARDS.md) |
| Profit/loss, allocation, drift | [RULES](references/RULES.md) |
| News and conviction tests | [AGENTIC-NEWS](references/AGENTIC-NEWS.md) |
| App paths and artifacts | [APP-LAYOUT](references/APP-LAYOUT.md) |
| HTML report styling | [DESIGN](references/DESIGN.md) |
| API feeds | [DATA-SOURCES](references/DATA-SOURCES.md) |
| Workflows | [commands/](references/commands/) |