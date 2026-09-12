#!/usr/bin/env python3
"""Validate the platform/theme registries used by drawer batch generation."""

from __future__ import annotations

import json
import sys
from pathlib import Path


DRAWER = Path(__file__).resolve().parents[1]
SKILLS = DRAWER.parent
SHARED = SKILLS / "qifu-shared"
PLATFORM_REGISTRY = SHARED / "references" / "platform-registry.json"
THEME_REGISTRY = SHARED / "theme" / "theme-registry.json"
TOKENS = SHARED / "theme" / "tokens.json"
COLOR_SOURCE = SHARED / "theme" / "source" / "color.json"


def load_json(path: Path, errors: list[str]) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{path}: cannot read JSON: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{path}: root must be an object")
        return {}
    return value


def main() -> int:
    errors: list[str] = []
    platform_data = load_json(PLATFORM_REGISTRY, errors)
    theme_data = load_json(THEME_REGISTRY, errors)
    token_data = load_json(TOKENS, errors)
    color_data = load_json(COLOR_SOURCE, errors)

    platforms = platform_data.get("platforms")
    themes = theme_data.get("themes")
    if not isinstance(platforms, dict) or not platforms:
        errors.append("platform-registry.json: platforms must be a non-empty object")
        platforms = {}
    if not isinstance(themes, dict) or not themes:
        errors.append("theme-registry.json: themes must be a non-empty object")
        themes = {}

    fallback = platform_data.get("fallbackPlatform")
    if fallback != "qifu-generic" or fallback not in platforms:
        errors.append("platform registry must use registered qifu-generic as fallback")

    seen_aliases: dict[str, str] = {}
    required_platform_fields = {
        "displayName",
        "aliases",
        "adapter",
        "defaultTheme",
        "generationStrategy",
        "shellReadiness",
        "detectionSignals",
        "backgroundPriority",
    }
    for key, platform in platforms.items():
        if not isinstance(platform, dict):
            errors.append(f"platform {key}: definition must be an object")
            continue
        missing = required_platform_fields - platform.keys()
        if missing:
            errors.append(f"platform {key}: missing {', '.join(sorted(missing))}")
        aliases = platform.get("aliases")
        if not isinstance(aliases, list) or not aliases:
            errors.append(f"platform {key}: aliases must be non-empty")
            aliases = []
        for alias in aliases:
            normalized = str(alias).strip().casefold()
            if not normalized:
                errors.append(f"platform {key}: aliases cannot contain empty values")
            elif normalized in seen_aliases and seen_aliases[normalized] != key:
                errors.append(
                    f"platform alias {alias!r} is shared by {seen_aliases[normalized]} and {key}"
                )
            else:
                seen_aliases[normalized] = key
        adapter = SHARED / str(platform.get("adapter", ""))
        if not adapter.is_file():
            errors.append(f"platform {key}: missing adapter {adapter}")
        if platform.get("defaultTheme") not in themes:
            errors.append(f"platform {key}: unknown default theme")
        signals = platform.get("detectionSignals")
        if not isinstance(signals, dict):
            errors.append(f"platform {key}: detectionSignals must be an object")
            signals = {}
        for signal_key in ("figmaNodeNames", "figmaVariableModes", "templateNodeIds"):
            if not isinstance(signals.get(signal_key), list):
                errors.append(f"platform {key}: {signal_key} must be a list")
        if platform.get("generationStrategy") == "copyTemplate":
            if not signals.get("figmaNodeNames") or not signals.get("templateNodeIds"):
                errors.append(f"platform {key}: copyTemplate requires exact template signals")

    collection_modes = {
        collection.get("name"): set(collection.get("modes", []))
        for collection in token_data.get("collections", [])
        if isinstance(collection, dict)
    }
    color_groups = {
        variable.get("group")
        for variable in color_data.get("variables", [])
        if isinstance(variable, dict)
    }
    required_theme_fields = {
        "primary",
        "bindingStrategy",
        "figmaCollection",
        "figmaMode",
        "colorVariableGroup",
        "supportedAppearance",
    }
    for key, theme in themes.items():
        if not isinstance(theme, dict):
            errors.append(f"theme {key}: definition must be an object")
            continue
        missing = required_theme_fields - theme.keys()
        if missing:
            errors.append(f"theme {key}: missing {', '.join(sorted(missing))}")
        collection = theme.get("figmaCollection")
        mode = theme.get("figmaMode")
        if collection is not None and collection not in collection_modes:
            errors.append(f"theme {key}: unknown Figma collection {collection}")
        if mode is not None and mode not in collection_modes.get(collection, set()):
            errors.append(f"theme {key}: unknown Figma mode {mode}")
        color_group = theme.get("colorVariableGroup")
        if color_group is not None and color_group not in color_groups:
            errors.append(f"theme {key}: unknown color variable group {color_group}")
        if key == "custom" and theme.get("requiresThemePrimary") is not True:
            errors.append("custom theme must require themePrimary")

    required_files = (
        DRAWER / "references" / "multi-platform-batch.md",
        SHARED / "references" / "platform-zhineng-yunying.md",
    )
    for path in required_files:
        if not path.is_file():
            errors.append(f"missing multi-platform contract: {path}")

    if errors:
        print("FAIL: multi-platform drawer contract")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        "PASS: multi-platform drawer contract "
        f"({len(platforms)} platforms, {len(themes)} themes, {len(seen_aliases)} aliases)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
