# update

Sync agent skills from the [deep-rich-skill](https://github.com/peerasak-u/deep-rich-skill) repo into the project.

## When to Use

- User says "update skills", "sync skills", "refresh deep-rich", or "update deep-rich agent skills"
- After pulling new changes to this repo that include skill updates

## How It Works

1. Clones the repo to a temp directory.
2. Lists available skills from `skills/` in the repo.
3. Copies selected skills to `./.agents/skills/` (project scope only).
4. Cleans up the temp clone.
5. Shows `git status` of what changed.

## Source & Target

| | Path |
|---|---|
| **Repo** | `https://github.com/peerasak-u/deep-rich-skill` |
| **Source** | `skills/` in repo root |
| **Install** | `./.agents/skills/` (project scope only) |

## Run the Script

```bash
# Update all skills
python3 skills/deep-rich/scripts/update_skills.py

# Update specific skills only
python3 skills/deep-rich/scripts/update_skills.py --skills deep-rich

# Dry run — show what would be updated
python3 skills/deep-rich/scripts/update_skills.py --dry-run
```

## Agent Flow

1. Ask user which skills to update (`all` or specific names).
2. Run the update script with selected skills.
3. Show `git status` to confirm changes.

## Rules

- **Project scope only** — always installs to `./.agents/skills/`, never global.
- **Source is fixed** — always the `skills/` directory in the deep-rich-skill repo.
- **Show diff** — after updating, `git status` shows what changed.
- **Use `--dry-run` to preview** — safe to run before committing.