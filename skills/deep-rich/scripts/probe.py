#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Locate the Deep Rich portfolio manager app for skill workflows."""

from __future__ import annotations

import argparse
import json
import sys

from _common import resolve_deep_rich_home


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--home", help="Explicit Deep Rich app root")
    parser.add_argument("--json", action="store_true", help="Print machine-readable output")
    args = parser.parse_args()

    try:
        home = resolve_deep_rich_home(args.home)
    except FileNotFoundError as exc:
        if args.json:
            print(json.dumps({"ok": False, "error": str(exc)}, indent=2))
        else:
            print(str(exc), file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps({"ok": True, "deep_rich_home": str(home)}, indent=2))
    else:
        print(home)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
