#!/usr/bin/env python3
"""Validate the portable component manifest without requiring Figma access."""

from __future__ import annotations

import json
import sys
from pathlib import Path


REQUIRED_COMPONENT_KEYS = {
    "drawerHeader",
    "closeIcon",
    "tag",
    "select",
    "tableShell",
    "headerCell",
    "row",
    "contentCell",
    "text",
    "pagination",
}


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parents[1] / "references" / "portable-component-manifest.json"
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FAIL: cannot read manifest: {exc}")
        return 1

    errors: list[str] = []
    if manifest.get("mode") != "PORTABLE_KIT":
        errors.append("mode must be PORTABLE_KIT")
    components = manifest.get("components")
    if not isinstance(components, dict):
        errors.append("components must be an object")
        components = {}
    missing = REQUIRED_COMPONENT_KEYS - components.keys()
    if missing:
        errors.append(f"missing component keys: {', '.join(sorted(missing))}")
    names = []
    for key, item in components.items():
        if not isinstance(item, dict) or not item.get("name"):
            errors.append(f"{key} must contain a non-empty name")
        else:
            names.append(item["name"])
        if isinstance(item, dict) and item.get("required") is not True:
            errors.append(f"{key}.required must be true")
    if len(names) != len(set(names)):
        errors.append("component names must be unique")
    styles = manifest.get("textStyles")
    if not isinstance(styles, list) or not styles:
        errors.append("textStyles must be a non-empty list")
    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"PASS: {path} ({len(components)} components, {len(styles)} text styles)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
