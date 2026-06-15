# update

Sync skills from [deep-rich-skill](https://github.com/peerasak-u/deep-rich-skill) → `./.agents/skills/`.

## When

"update skills" / "sync skills" / "refresh deep-rich" / after pulling skill repo changes

## Command

```bash
python3 skills/deep-rich/scripts/update_skills.py
python3 skills/deep-rich/scripts/update_skills.py --skills deep-rich
python3 skills/deep-rich/scripts/update_skills.py --dry-run
```

## Flow

1. Ask: all or specific skills
2. Run script
3. Show `git status`

Rules: project scope only (`./.agents/skills/`); source = repo `skills/`; use `--dry-run` to preview.