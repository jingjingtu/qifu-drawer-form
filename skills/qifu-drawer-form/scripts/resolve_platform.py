#!/usr/bin/env python3
"""Resolve a Qifu platform from deterministic registry signals."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


DRAWER = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = DRAWER.parent / "qifu-shared" / "references" / "platform-registry.json"


def normalized(value: str) -> str:
    return value.strip().casefold()


def load_platforms(path: Path) -> dict[str, dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    platforms = data.get("platforms")
    if not isinstance(platforms, dict):
        raise ValueError("registry platforms must be an object")
    return platforms


def resolve(platforms: dict[str, dict], args: argparse.Namespace) -> tuple[dict, int]:
    evidence: dict[str, list[str]] = {}

    def record(platform_key: str, signal: str) -> None:
        evidence.setdefault(platform_key, []).append(signal)

    if args.platform_key:
        if args.platform_key not in platforms:
            return {
                "status": "UNRESOLVED",
                "reason": "UNKNOWN_PLATFORM_KEY",
                "input": args.platform_key,
            }, 2
        record(args.platform_key, f"platformKey:{args.platform_key}")

    if args.name:
        name = normalized(args.name)
        for key, platform in platforms.items():
            aliases = {normalized(str(alias)) for alias in platform.get("aliases", [])}
            if name in aliases or name == normalized(str(platform.get("displayName", ""))):
                record(key, f"name:{args.name}")

    signal_inputs = {
        "figmaNodeNames": args.figma_node_name,
        "figmaVariableModes": args.figma_variable_mode,
        "templateNodeIds": args.template_node_id,
    }
    for signal_type, values in signal_inputs.items():
        for value in values:
            needle = normalized(value)
            for key, platform in platforms.items():
                registered = {
                    normalized(str(item))
                    for item in platform.get("detectionSignals", {}).get(signal_type, [])
                }
                if needle in registered:
                    record(key, f"{signal_type}:{value}")

    explicit = args.platform_key
    if explicit:
        conflicts = sorted(key for key in evidence if key != explicit)
        if conflicts:
            return {
                "status": "CONFLICT",
                "platformKey": explicit,
                "evidence": evidence,
                "conflicts": conflicts,
            }, 3
        candidates = [explicit]
    else:
        candidates = sorted(evidence)

    if not candidates:
        return {
            "status": "UNRESOLVED",
            "reason": "NO_DETERMINISTIC_SIGNAL",
            "evidence": evidence,
        }, 2
    if len(candidates) > 1:
        return {
            "status": "AMBIGUOUS",
            "candidates": candidates,
            "evidence": evidence,
        }, 3

    key = candidates[0]
    platform = platforms[key]
    return {
        "status": "RESOLVED",
        "platformKey": key,
        "platformName": platform.get("displayName"),
        "detectedBy": evidence[key],
        "adapter": platform.get("adapter"),
        "defaultTheme": platform.get("defaultTheme"),
        "generationStrategy": platform.get("generationStrategy"),
        "shellReadiness": platform.get("shellReadiness"),
        "backgroundPriority": platform.get("backgroundPriority"),
    }, 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--platform-key")
    parser.add_argument("--name")
    parser.add_argument("--figma-node-name", action="append", default=[])
    parser.add_argument("--figma-variable-mode", action="append", default=[])
    parser.add_argument("--template-node-id", action="append", default=[])
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        platforms = load_platforms(args.registry)
        result, code = resolve(platforms, args)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(json.dumps({"status": "ERROR", "reason": str(exc)}, ensure_ascii=False))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
