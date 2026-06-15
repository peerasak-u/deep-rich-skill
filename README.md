# Deep Rich Skill

Pi skill package for the [Deep Rich](../deep-rich) portfolio manager.

This repository contains the **agent workflow layer** only. The portfolio manager app, dashboard, CLI, and private `.deep-rich/` data stay in `../deep-rich`.

## Structure

```text
deep-rich-skill/
├── pyproject.toml
├── skills/
│   └── deep-rich/
│       ├── SKILL.md
│       ├── agents/
│       ├── references/
│       └── scripts/
│           ├── _common.py
│           ├── probe.py
│           └── signals.py
└── tests/
```

## Local install from the portfolio manager repo

Create or update `../deep-rich/.pi/settings.json`:

```json
{
  "packages": ["../deep-rich-skill"]
}
```

Pi discovers `skills/deep-rich/SKILL.md` by convention.

## Runtime contract

The seam between this skill and the app is the Deep Rich CLI:

```bash
python3 scripts/dr.py doctor
python3 scripts/dr.py prices
python3 scripts/dr.py portfolio
python3 scripts/dr.py performance
python3 scripts/dr.py deployment
python3 scripts/dr.py summary
```

Resolve the app root with either:

```bash
export DEEP_RICH_HOME=/path/to/deep-rich
```

or run Pi from inside the `deep-rich` app repository.

Optional skill helpers:

```bash
uv run skills/deep-rich/scripts/probe.py --json
uv run skills/deep-rich/scripts/signals.py --home ../deep-rich --json
```

## Development

```bash
uv sync
uv run pytest
uv run ruff check .
```

## Privacy rule

Do not commit private portfolio artifacts here. This repo should never contain:

- `.deep-rich/portfolio.json`
- `.deep-rich/prices.json`
- `.deep-rich/reviews/`
- API keys or account identifiers
- hardcoded local absolute paths
