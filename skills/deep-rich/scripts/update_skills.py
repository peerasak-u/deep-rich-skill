"""Update agent skills from the deep-rich-skill repo."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_URL = "https://github.com/peerasak-u/deep-rich-skill"
SKILLS_SOURCE = "skills"
INSTALL_TARGET = Path("./.agents/skills")


def run(cmd: list[str], **kwargs) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=True, capture_output=True, text=True, **kwargs)


def list_local_skills() -> list[str]:
    """List skills already installed in the project."""
    if not INSTALL_TARGET.is_dir():
        return []
    return sorted(d.name for d in INSTALL_TARGET.iterdir() if d.is_dir())


def list_available_skills(clone_dir: Path) -> list[str]:
    """List skills in the cloned repo."""
    source = clone_dir / SKILLS_SOURCE
    if not source.is_dir():
        return []
    return sorted(d.name for d in source.iterdir() if d.is_dir())


def update_skill(skill: str, source_dir: Path) -> bool:
    """Copy a single skill into the install target. Returns True if updated."""
    target = INSTALL_TARGET / skill
    src = source_dir / skill
    if not src.is_dir():
        print(f"⚠️  Not found in repo: {skill}")
        return False

    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(src, target)
    print(f"✅ Updated: {skill}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Update skills from deep-rich-skill repo.")
    parser.add_argument(
        "--skills",
        nargs="+",
        default=["all"],
        help="Skill names to update. Omit or use 'all' to update everything.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes.",
    )
    args = parser.parse_args()

    # Clone to temp dir
    with tempfile.TemporaryDirectory(prefix="deep-rich-skill-") as tmp:
        tmp_path = Path(tmp)
        print(f"Cloning {REPO_URL} ...")
        try:
            run(["git", "clone", "--quiet", REPO_URL, str(tmp_path / "repo")])
        except subprocess.CalledProcessError as e:
            print(f"❌ Git clone failed:\n{e.stderr}")
            return 1

        repo_dir = tmp_path / "repo"
        available = list_available_skills(repo_dir)

        if not available:
            print("❌ No skills found in repo.")
            return 1

        print(f"\nAvailable skills in repo: {', '.join(available)}")

        if args.skills == ["all"]:
            selected = available
        else:
            selected = [s for s in args.skills if s in available]
            missing = [s for s in args.skills if s not in available]
            for m in missing:
                print(f"⚠️  Unknown skill: {m}")

        if not selected:
            print("❌ Nothing to update.")
            return 1

        print(f"\nUpdating: {', '.join(selected)}")

        if args.dry_run:
            for skill in selected:
                print(f"  [dry-run] Would update: {skill}")
            return 0

        INSTALL_TARGET.mkdir(parents=True, exist_ok=True)
        for skill in selected:
            update_skill(skill, repo_dir / SKILLS_SOURCE)

        # Cleanup
        shutil.rmtree(repo_dir)

    # Show result
    print(f"\nInstalled skills ({INSTALL_TARGET}):")
    for d in sorted(INSTALL_TARGET.iterdir()):
        if d.is_dir():
            print(f"  {d.name}/")

    # Show git diff
    result = subprocess.run(
        ["git", "status", "--short", str(INSTALL_TARGET)],
        capture_output=True,
        text=True,
    )
    if result.stdout.strip():
        print(f"\nChanges:\n{result.stdout}")

    return 0


if __name__ == "__main__":
    sys.exit(main())