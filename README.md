# Deep Rich Skill

Portfolio management workflow for AI coding agents. Decision support, profit-taking signals, rebalancing, and weekly review rituals for Thai SET, US stocks, Crypto, Gold, and Cash.

> **Quick start:** Install the skill, then talk to the agent: "review my portfolio", "is my data okay?", or "should I buy EGCO?". The underlying scripts are internal workflow tools; users should not need to know or run them directly.

## Why Deep Rich?

Most portfolio tools show you numbers. Deep Rich helps you think — and act. It gives agents structured advice workflows, guardrails, and a profit-taking signal engine so the first contact point is human → agent, not human → script.

## What's Included

### The Skill: deep-rich

Pi skill that routes natural language to the right portfolio workflow:

| User says | Workflow |
|-----------|----------|
| "setup my portfolio" | `onboard` |
| "is my data okay" | `doctor` |
| "how's my portfolio" | `review` |
| "what happened" | `briefing` |
| "should I buy X" | `research <SYM>` |
| "I have cash, where to put it" | `deploy` |
| "should I rebalance" | `rebalance` |
| "why did I buy X" | `journal` |
| "what's my risk" | `risk` |
| "am I on track" | `goals` |

See [SKILL.md](skills/deep-rich/SKILL.md) for the full routing table, guardrails, and workflow details.

### Internal Helpers

The skill includes lightweight helper scripts for agents and developers. They are implementation details used underneath the natural-language workflows, not user-facing commands.

```bash
# Agent/dev diagnostic: probe the portfolio manager app root
uv run skills/deep-rich/scripts/probe.py --json

# Agent/dev diagnostic: build context-aware portfolio signals
uv run skills/deep-rich/scripts/signals.py --home /path/to/deep-rich --json
```

### Workflow References

Detailed command docs live in `skills/deep-rich/references/commands/`:
`analyze`, `briefing`, `dashboard`, `deploy`, `deployment`, `doctor`, `fundamentals`, `goals`, `health`, `journal`, `news`, `onboard`, `performance`, `portfolio`, `prices`, `rebalance`, `research`, `review`, `risk`, `summary`.

## Usage

Once installed, start with normal language. The agent infers the workflow, resolves the app root, runs readiness checks, calls the required internal scripts, and explains the result in human terms.

Example sessions:

```
"review my portfolio"          → runs review workflow
"should I buy EGCO?"          → runs research workflow
"I have ฿200k to invest"       → runs deploy workflow
"rebalance my portfolio"        → runs rebalance workflow
"what's my biggest risk?"     → runs risk workflow
```

Behind the scenes, the agent runs a data-health check before any serious advice workflow. If advice is blocked, it stops and helps you fix or onboard the missing data before recommending actions.

## Anti-Patterns

The skill includes explicit guidance on what to avoid:

- **Don't pressure decisions.** Suggest, don't push. The user decides.
- **Don't deploy below ฿300,000 THB.** Emergency floor is non-negotiable.
- **Don't touch gold.** Gold is passive — never recommend buying or selling gold for rebalancing.
- **Don't increase cash.** Cash is the deployment source, not a rebalancing target.
- **Don't ignore stale prices.** Warn when prices are older than 24 hours.
- **Don't force a thesis.** Mark it unknown and research before buy/sell pressure.
- **Don't expose scripts to users.** The contact point is human → agent, not human → script.

## Installation

### Option 1: Pi packages (Recommended for Pi users)

Add to your Pi settings file (`~/.pi/settings.json` or `.pi/settings.json`):

```json
{
  "packages": ["/path/to/deep-rich-skill"]
}
```

Pi discovers `skills/deep-rich/SKILL.md` by convention.

### Option 2: Clone into `.pi/skills`

```bash
git clone https://github.com/peerasak-u/deep-rich-skill ~/.pi/skills/deep-rich-skill
```

### Option 3: Copy skill folder

```bash
# Project-specific
cp -r skills/deep-rich /path/to/your-project/.pi/skills/

# Or global
cp -r skills/deep-rich ~/.pi/skills/
```

### Option 4: Reference from another project

If your portfolio manager app lives at `../deep-rich`, add this repo as a package in `../deep-rich/.pi/settings.json`:

```json
{
  "packages": ["../deep-rich-skill"]
}
```

## Supported Tools

- [Pi](https://pi.dev/)
- [Claude Code](https://claude.ai/code)
- [Codex CLI](https://github.com/openai/codex)

## Development

```bash
uv sync
uv run pytest
uv run ruff check .
```

## Privacy

This repo is the agent workflow layer only. Private portfolio data (`.deep-rich/portfolio.json`, prices, journal, reviews) stays in the portfolio manager app directory. Never commit private artifacts here.

---

Created by [Peerasak U](https://github.com/peerasak-u)
