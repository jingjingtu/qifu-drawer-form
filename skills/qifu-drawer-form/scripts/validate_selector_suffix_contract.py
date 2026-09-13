#!/usr/bin/env python3
"""Validate the shared Select/Cascader suffix token and documentation contract."""

from __future__ import annotations

import json
from pathlib import Path


DRAWER = Path(__file__).resolve().parents[1]
SHARED = DRAWER.parent / "qifu-shared"
BASIC_SOURCE = SHARED / "theme" / "source" / "basic.json"
TOKENS = SHARED / "theme" / "tokens.json"
LESS = SHARED / "theme" / "_light.less"
COMPONENT_MAP = SHARED / "references" / "component-map.md"
FIELD_MAP = DRAWER / "references" / "field-control-map.md"
VALIDATION = DRAWER / "references" / "figma-execution-validation.md"

TOKEN_PATH = "图标颜色/--qifu-icon-color-tertiary"
EXPECTED_ALIASES = {
    "毓数/Light": "mode/green/--qifu-icon-color-1",
    "智能运营/Light": "mode/blue/--qifu-icon-color-1",
}


def main() -> int:
    errors: list[str] = []
    try:
        basic = json.loads(BASIC_SOURCE.read_text(encoding="utf-8"))
        tokens = json.loads(TOKENS.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FAIL: cannot read selector suffix token data: {exc}")
        return 1

    matches = [
        item
        for item in basic.get("variables", [])
        if isinstance(item, dict) and item.get("figmaPath") == TOKEN_PATH
    ]
    if len(matches) != 1:
        errors.append(f"{TOKEN_PATH} must occur exactly once in basic.json")
    elif matches[0].get("values") != EXPECTED_ALIASES:
        errors.append(f"{TOKEN_PATH} must alias the registered green/blue icon-color-1 primitives")

    collections = {
        item.get("key"): item
        for item in tokens.get("collections", [])
        if isinstance(item, dict)
    }
    if collections.get("basic", {}).get("variableCount") != len(basic.get("variables", [])):
        errors.append("tokens.json basic.variableCount must match source/basic.json")
    expected_total = sum(
        item.get("variableCount", 0)
        for item in tokens.get("collections", [])
        if isinstance(item, dict)
    )
    if tokens.get("totalVariableCount") != expected_total:
        errors.append("tokens.json totalVariableCount must equal collection totals")

    required_text = {
        LESS: "@qifu-icon-color-tertiary: #BABAC2;",
        COMPONENT_MAP: "Select / Cascader 后缀一致性",
        FIELD_MAP: "COMPONENT_SOURCE_GAP: selector suffix contract",
        VALIDATION: "图标颜色/--qifu-icon-color-tertiary",
    }
    for path, needle in required_text.items():
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            errors.append(f"cannot read {path}: {exc}")
            continue
        if needle not in text:
            errors.append(f"{path.relative_to(DRAWER.parent)}: missing {needle}")

    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS: Select/Cascader suffix token and validation contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
