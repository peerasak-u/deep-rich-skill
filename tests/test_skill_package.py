from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "deep-rich"
SKILL_MD = SKILL / "SKILL.md"


def iter_repo_files():
    ignored_parts = {".git", ".venv", "__pycache__", ".pytest_cache", ".ruff_cache"}
    for path in ROOT.rglob("*"):
        if path.is_file() and not ignored_parts.intersection(path.parts):
            yield path


def parse_frontmatter(text: str) -> dict[str, str]:
    assert text.startswith("---\n"), "SKILL.md must start with YAML frontmatter"
    _, raw, _body = text.split("---", 2)
    data: dict[str, str] = {}
    for line in raw.strip().splitlines():
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()
    return data


def test_skill_frontmatter_is_valid():
    data = parse_frontmatter(SKILL_MD.read_text())

    assert data["name"] == "deep-rich"
    assert re.fullmatch(r"[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?", data["name"])
    assert "description" in data
    assert len(data["description"]) <= 1024
    assert "<" not in data["description"] and ">" not in data["description"]


def test_markdown_links_point_to_existing_files_or_directories():
    link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    missing = []

    for path in SKILL.rglob("*.md"):
        text = path.read_text()
        for match in link_pattern.finditer(text):
            target = match.group(1).strip()
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = target.split("#", 1)[0]
            if not target:
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                missing.append(f"{path.relative_to(ROOT)} -> {target}")

    assert missing == []


def test_private_portfolio_data_is_not_present():
    assert not (ROOT / ".deep-rich").exists()

    private_names = {"portfolio.json", "prices.json", "goals.json", "fundamentals_cache.db"}
    leaked = [str(path.relative_to(ROOT)) for path in iter_repo_files() if path.name in private_names]
    assert leaked == []


def test_no_hardcoded_local_absolute_paths():
    offenders = []
    local_path = re.compile("/" + "Users" + r"/[^\s`'\"]+")
    for path in iter_repo_files():
        if path.suffix not in {".md", ".py", ".toml", ".json", ".txt"}:
            continue
        for line_no, line in enumerate(path.read_text(errors="ignore").splitlines(), 1):
            if local_path.search(line):
                offenders.append(f"{path.relative_to(ROOT)}:{line_no}: {line.strip()}")
    assert offenders == []


@pytest.mark.parametrize(
    ("phrase", "workflow_doc"),
    [
        ("setup my portfolio", "onboard.md"),
        ("is my data okay", "doctor.md"),
        ("review", "review.md"),
        ("any news", "briefing.md"),
        ("should I buy X", "research.md"),
        ("where should I put it", "deploy.md"),
        ("should I rebalance", "rebalance.md"),
        ("why did I buy X", "journal.md"),
        ("what's my risk", "risk.md"),
        ("am I on track", "goals.md"),
    ],
)
def test_routing_table_has_expected_workflows(phrase: str, workflow_doc: str):
    text = SKILL_MD.read_text()
    assert phrase in text
    assert (SKILL / "references" / "commands" / workflow_doc).exists()


def make_fake_app(tmp_path: Path) -> Path:
    home = tmp_path / "deep-rich"
    (home / "scripts").mkdir(parents=True)
    (home / ".deep-rich").mkdir()
    (home / "scripts" / "dr.py").write_text(
        "def calculate_portfolio():\n"
        "    return {\n"
        "        'classes': {\n"
        "            'Thai SET': {'pct': 10.0, 'target_pct': 25.0, 'drift': -15.0},\n"
        "            'US Market': {'pct': 35.0, 'target_pct': 35.0, 'drift': 0.0},\n"
        "            'Gold': {'pct': 10.0, 'target_pct': 10.0, 'drift': 0.0},\n"
        "            'Cash': {'pct': 45.0, 'target_pct': 20.0, 'drift': 25.0, 'value_thb': 500000},\n"
        "        },\n"
        "        'emergency_floor_thb': 300000,\n"
        "    }\n"
    )
    (home / ".deep-rich" / "portfolio.json").write_text(json.dumps({"asset_classes": {}}))
    (home / ".deep-rich" / "prices.json").write_text(
        json.dumps({"updated_at": "2999-01-01T00:00:00Z", "prices": {}})
    )
    return home


def test_probe_resolves_explicit_deep_rich_home(tmp_path: Path):
    from _common import resolve_deep_rich_home

    home = make_fake_app(tmp_path)
    assert resolve_deep_rich_home(str(home)) == home


def test_signals_use_explicit_home(tmp_path: Path):
    import signals

    home = make_fake_app(tmp_path)
    result = signals.build_signals(home)

    assert result["prices"]["status"] == "ok"
    assert result["emergency_floor"]["status"] == "ok"
    assert result["drift"][0]["asset_class"] == "Thai SET"
    assert result["actions"][0]["action"] == "python3 scripts/dr.py deployment"
