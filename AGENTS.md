# AGENTS.md

Instructions for AI coding agents working in this repository.

## Purpose

`deep-rich-skill` is the Pi skill package for the Deep Rich portfolio manager. This repo contains the **agent workflow layer only**: skill instructions, workflow references, lightweight helpers, and tests. The actual portfolio manager app and private `.deep-rich/` data live outside this repo, usually in `../deep-rich`.

## Project Map

```text
deep-rich-skill/
├── AGENTS.md                         # Agent instructions and working agreement
├── README.md                         # Installation, runtime contract, privacy rules
├── pyproject.toml                    # Python/uv/pytest/ruff configuration
├── uv.lock                           # uv lockfile
├── skills/
│   └── deep-rich/
│       ├── SKILL.md                  # Main Pi skill: routing, guardrails, workflows
│       ├── agents/
│       │   └── stock-research.toml   # Specialized stock research subagent
│       ├── references/
│       │   ├── DATA-SOURCES.md       # External data-source details
│       │   └── commands/             # Workflow docs for dr.py commands
│       └── scripts/
│           ├── _common.py            # Resolve the Deep Rich app root
│           ├── probe.py              # Check app-root discovery
│           └── signals.py            # Build portfolio action signals
└── tests/
    └── test_skill_package.py         # Metadata, links, privacy, routing, helpers
```

## Build, Test, and Lint

Use `uv` for all Python workflows.

```bash
uv sync
uv run pytest
uv run ruff check .
```

Do not introduce `pip`, `poetry`, `npm`, or other package-management conventions unless the project explicitly changes direction.

## Code Style

- Python target: `>=3.12`.
- Ruff line length: `120`.
- Ruff lint rules: `E`, `F`, `I`, `UP`, `B`; `E501` is ignored.
- Keep helpers small and dependency-free unless there is a concrete need.
- Prefer clear workflow documentation over clever code.
- Markdown links under `skills/deep-rich/` must point to real files or directories.

## Deep Rich Runtime Contract

The seam between this skill package and the portfolio manager app is the app CLI:

```bash
python3 scripts/dr.py doctor
python3 scripts/dr.py prices
python3 scripts/dr.py portfolio
python3 scripts/dr.py performance
python3 scripts/dr.py deployment
python3 scripts/dr.py summary
```

Before any serious portfolio advice workflow:

1. Resolve the app root via explicit `--home`, `DEEP_RICH_HOME`, current directory ancestors, or sibling `../deep-rich`.
2. Verify the app root contains both `scripts/dr.py` and `.deep-rich/`.
3. Run `python3 scripts/dr.py doctor`.
4. If doctor says advice is blocked, stop and fix/onboard data before recommending actions.

## Portfolio Advice Guardrails

- Suggest, do not pressure. The user decides.
- Show the numbers behind recommendations.
- Warn on stale prices older than 24 hours; refresh prices before interpretation when possible.
- Show aggregate portfolio values in THB.
- For US/crypto positions, include both native currency and THB when relevant.
- Emergency floor: never recommend deploying cash below ฿300,000 THB.
- Gold is passive: do not recommend buying or selling gold for rebalancing.
- Cash is the deployment source, not a rebalancing target.
- Flag concentration risk; do not force sells.
- Missing thesis is acceptable. Mark it unknown and research before buy/sell pressure.

## Privacy and Safety Boundaries

Never commit or create private portfolio artifacts in this repo:

- `.deep-rich/portfolio.json`
- `.deep-rich/prices.json`
- `.deep-rich/reviews/`
- API keys, account identifiers, broker data, or credentials
- Hardcoded local absolute paths such as `/Users/...`

If private data is needed, read it only from the resolved Deep Rich app root and keep generated artifacts there unless the user explicitly asks otherwise.

## Testing Expectations

- Run `uv run pytest` after changing Python helpers, skill routing, command references, or Markdown links.
- Run `uv run ruff check .` after changing Python code.
- For docs-only changes outside tested link paths, tests are optional but still preferred before committing.
- If a test fails, inspect the failure and fix the underlying issue; do not weaken privacy/link/routing tests without a clear reason.

## Git and Commit Conventions

- Use Conventional Commits: `<type>(<scope>): <summary>`.
- Include a useful commit body for non-trivial changes.
- Commit only when Peerasak asks.
- Do not push unless explicitly asked.
- If files are ambiguous, ask before staging.

## Working Agreement with Peerasak

- Be concise, direct, and practical.
- State assumptions when they matter.
- Ask when the request is ambiguous or could touch private data.
- Prefer the smallest change that solves the problem.
- Do not silently refactor unrelated code.
- Challenge plans when they conflict with the project model or guardrails.
- Surface risks plainly; no false confidence.
- Keep a clear project map in your head: this repo teaches agents how to operate Deep Rich, but the real app and private data live next door.

## Karpathy-Style Agent Behavior

- Think before coding: name uncertainty instead of guessing.
- Simplicity first: no speculative abstractions or extra features.
- Surgical changes: every changed line should trace back to the request.
- Goal-driven execution: define how the change will be verified, then verify it.
