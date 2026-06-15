"""Shared helpers for Deep Rich skill scripts."""

from __future__ import annotations

import os
from collections.abc import Iterable
from pathlib import Path


def is_deep_rich_home(path: Path) -> bool:
    """Return True when path looks like the Deep Rich portfolio manager app."""
    return (path / "scripts" / "dr.py").is_file() and (path / ".deep-rich").exists()


def _ancestors(start: Path) -> Iterable[Path]:
    current = start.resolve()
    if current.is_file():
        current = current.parent
    yield current
    yield from current.parents


def candidate_homes(explicit: str | None = None, start: Path | None = None) -> list[Path]:
    """Return ordered Deep Rich home candidates without checking validity."""
    candidates: list[Path] = []

    def add(value: str | Path | None) -> None:
        if not value:
            return
        path = Path(value).expanduser()
        if path not in candidates:
            candidates.append(path)

    add(explicit)
    add(os.environ.get("DEEP_RICH_HOME"))

    for ancestor in _ancestors(start or Path.cwd()):
        add(ancestor)

    # Local development layout:
    #   <workspace>/deep-rich
    #   <workspace>/deep-rich-skill/skills/deep-rich/scripts/_common.py
    skill_repo = Path(__file__).resolve().parents[3]
    add(skill_repo.parent / "deep-rich")

    return candidates


def resolve_deep_rich_home(explicit: str | None = None, start: Path | None = None) -> Path:
    """Resolve the portfolio manager app root.

    Search order:
    1. explicit --home value
    2. DEEP_RICH_HOME
    3. current working directory and ancestors
    4. sibling ../deep-rich when developing this skill from deep-rich-skill
    """
    checked = []
    for candidate in candidate_homes(explicit=explicit, start=start):
        path = candidate.resolve()
        checked.append(str(path))
        if is_deep_rich_home(path):
            return path

    raise FileNotFoundError(
        "Could not find Deep Rich portfolio manager app root. "
        "Set DEEP_RICH_HOME to a directory containing scripts/dr.py and .deep-rich/. "
        f"Checked: {', '.join(checked)}"
    )
