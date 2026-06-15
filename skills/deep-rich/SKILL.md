---
name: deep-rich
description: Portfolio manager for Thai SET, US stocks, Crypto, Gold, and Cash. Use when asking about portfolio status, allocation drift, stock fundamentals, deployment plans, investment decisions, rebalancing, or performance tracking.
---

# Deep Rich

Weekly portfolio review + decision support. Thai SET, US, Crypto, Gold, Cash.

## Glossary

| shorthand | meaning |
|-----------|---------|
| `dr` | `python3 scripts/dr.py` @ resolved app root |
| `home` | portfolio app root (`DEEP_RICH_HOME`, cwd ancestors, or `../deep-rich`) |
| `gate` | resolve home → verify `scripts/dr.py` + `.deep-rich/` → `dr doctor` |
| `blocked` | doctor `advice_mode=blocked` → fix data before portfolio actions |
| `floor` | ฿300k emergency deploy minimum |
| `deployable` | cash − floor |
| `stale` | prices `updated_at` >24h → warn; interpret → `dr prices` first |
| `agg` | portfolio totals/drift/deployment in THB |
| `conc` | flag holding >5% port or >15% class; never force sell |
| `labels` | Fact \| Calculated \| Estimate \| Interpretation \| Unknown |

## Contract

Skill = workflow layer only. App + private data live outside this repo.

**Interface:** human → agent. Never tell user to run `dr.py` as primary UI. Infer intent, run scripts internally, explain in human terms.

HTML artifacts → [DESIGN](references/DESIGN.md). Label facts/calculations/estimates/interpretations/unknowns.

## Gate (before advice)

1. Resolve `home`
2. Verify `scripts/dr.py` + `.deep-rich/`
3. `dr doctor` — `blocked` → stop; help fix/onboard
4. Stale/missing prices → `dr prices` before interpreting
5. Optional: `skills/deep-rich/scripts/signals.py`

## Guards

Enforce [GUARDS](references/GUARDS.md). Mnemonic: trust-onboard, floor, stale, THB-agg, conc, gold-passive, cash-source, suggest-not-pressure.

Load workflow-specific guards from active command ref when present.

## Routing

Infer workflow from natural language. Load ref on demand — don't preload all docs.

**Disambiguation:** weekly ritual / "what should I do" → `review`. Event pulse ("after WWDC", "any news today") → `briefing`.

| User says | Workflow | Reference |
|-----------|----------|-----------|
| "setup my portfolio" / "start Deep Rich" / "onboard me" | `onboard` | [onboard](references/commands/onboard.md) |
| "is my data okay" / "health check" / "doctor" | `doctor` | [doctor](references/commands/doctor.md) |
| "how's my portfolio" / "what should I do" / "review" | `review` | [review](references/commands/review.md) |
| "what happened" / "any news" / "how's my portfolio after [event]" | `briefing` | [briefing](references/commands/briefing.md) |
| "should I buy X" / "is X worth buying" / "research EGCO" | `research <SYM>` | [research](references/commands/research.md) |
| "I have cash, where should I put it" / "deployment" | `deploy` | [deploy](references/commands/deploy.md) |
| "should I rebalance" / "how do I fix my allocation" | `rebalance mechanical` | [rebalance](references/commands/rebalance.md) |
| "I want to rotate [losers] to [opportunity]" | `rebalance rotate` | [rebalance](references/commands/rebalance.md) |
| "why did I buy X" / "what was my thesis" / "log this decision" | `journal` | [journal](references/commands/journal.md) |
| "what's my risk" / "what could hurt me" | `risk` | [risk](references/commands/risk.md) |
| "am I on track" / "when will I hit X" / "set a goal" | `goals` | [goals](references/commands/goals.md) |
| "update skills" / "sync skills" / "refresh deep-rich" | `update` | [update](references/commands/update.md) |
| "I onboarded holdings / finish setup" | `onboard` → `doctor` → `research <SYM>` backfill | [onboard](references/commands/onboard.md), [research](references/commands/research.md) |

### Chains

| Intent | Chain |
|--------|-------|
| "should I buy more MSFT" | `research MSFT` → allocation check → `deploy` → reason |
| "portfolio review + what to buy" | `review` → `deploy` → synthesize |
| "cut my losers and buy data center" | `rebalance rotate` → `research EGCO` → synthesize |

## Scripts (internal — not user UI)

| Command | Purpose |
|---------|---------|
| `dr.py onboard` / `setup` | Fresh or existing portfolio capture |
| `dr.py doctor` | Data health + readiness gate |
| `dr.py portfolio` | State + drift |
| `dr.py performance` | Gains/losses by holding |
| `dr.py health <SYM>` / `watchlist` | Health grades |
| `dr.py fundamentals <SYM>` | Valuation, financials |
| `dr.py deployment` | Cash allocation plan |
| `dr.py prices` | Fresh prices |
| `dr.py thai-561 <SYM>` | Thai SEC 56-1 |
| `signals.py` | Context-aware alerts |
| `export_dashboard.py` | HTML dashboard |
| `export_company_profile.py` | Company profile HTML |

## References (load on demand)

| Topic | Reference |
|-------|-----------|
| Hard rules | [GUARDS](references/GUARDS.md) |
| Profit/loss, allocation, drift | [RULES](references/RULES.md) |
| News + conviction | [AGENTIC-NEWS](references/AGENTIC-NEWS.md) |
| App paths + artifacts | [APP-LAYOUT](references/APP-LAYOUT.md) |
| HTML styling | [DESIGN](references/DESIGN.md) |
| API feeds | [DATA-SOURCES](references/DATA-SOURCES.md) |
| Workflows | [commands/](references/commands/) |