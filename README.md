# Deep Rich Skill

Portfolio management workflow for AI coding agents. Decision support, profit-taking signals, rebalancing, and weekly review rituals for Thai SET, US stocks, Crypto, Gold, and Cash.

> **Quick start:** Set `DEEP_RICH_HOME` to your portfolio manager app root, then run `python3 scripts/dr.py doctor` before any advice workflow. See [SKILL.md](skills/deep-rich/SKILL.md) for the full routing table.

## Why Deep Rich?

Most portfolio tools show you numbers. Deep Rich helps you think — and act. It wraps a portfolio manager app with structured advice workflows, guardrails, and a profit-taking signal engine so agents can give useful guidance without pressure or speculation.

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

### Helper Scripts

```bash
# Probe the portfolio manager app root
uv run skills/deep-rich/scripts/probe.py --json

# Build context-aware portfolio signals
uv run skills/deep-rich/scripts/signals.py --home /path/to/deep-rich --json
```

### Workflow References

Detailed command docs live in `skills/deep-rich/references/commands/`:
`analyze`, `briefing`, `dashboard`, `deploy`, `deployment`, `doctor`, `fundamentals`, `goals`, `health`, `journal`, `news`, `onboard`, `performance`, `portfolio`, `prices`, `rebalance`, `research`, `review`, `risk`, `summary`.

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

## Usage

Once installed, the skill activates when your request matches a routing pattern. Example sessions:

```
"review my portfolio"          → runs review workflow
"should I buy EGCO?"          → runs research workflow
"I have ฿200k to invest"       → runs deploy workflow
"rebalance my portfolio"        → runs rebalance workflow
"what's my biggest risk?"     → runs risk workflow
```

Before any advice workflow, the skill runs `dr.py doctor` to check data health. If the check is blocked, it stops and asks you to fix the data first.

## Guardrails

- **Suggest, don't pressure.** The user decides.
- **Emergency floor:** never recommend deploying below ฿300,000 THB.
- **Gold is passive:** do not recommend buying or selling gold for rebalancing.
- **Cash is the source:** do not recommend increasing cash allocation.
- **Stale prices:** warn when prices are older than 24 hours.
- **Missing thesis:** mark it unknown and research before buy/sell pressure.

## Development

```bash
uv sync
uv run pytest
uv run ruff check .
```

## Privacy

This repo is the agent workflow layer only. Private portfolio data (`.deep-rich/portfolio.json`, prices, journal, reviews) stays in the portfolio manager app directory. Never commit private artifacts here.
