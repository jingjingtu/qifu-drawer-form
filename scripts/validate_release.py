#!/usr/bin/env python3
"""Validate the generated qifu-drawer-form release repository."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
PACKAGES = ("qifu-drawer-form", "qifu-shared")
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
FRONTMATTER_NAME = re.compile(r"^name:\s*([^\n]+)$", re.MULTILINE)
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
SKIP_PARTS = {".git", "__pycache__", ".pytest_cache"}
SECRET_PATTERNS = {
    "GitHub token": re.compile(r"(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})"),
    "Figma token": re.compile(r"figd_[A-Za-z0-9_-]{20,}"),
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
}


def release_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and path.name != "RELEASE_MANIFEST.json"
        and not SKIP_PARTS.intersection(path.parts)
    )


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_packages(errors: list[str]) -> dict[str, str]:
    versions: dict[str, str] = {}
    for package in PACKAGES:
        package_dir = SKILLS / package
        skill_file = package_dir / "SKILL.md"
        version_file = package_dir / "VERSION"
        agent_file = package_dir / "agents" / "openai.yaml"
        for required in (skill_file, version_file, agent_file):
            if not required.is_file():
                errors.append(f"missing required file: {required.relative_to(ROOT)}")
        if not skill_file.is_file() or not version_file.is_file():
            continue
        text = skill_file.read_text(encoding="utf-8")
        match = FRONTMATTER_NAME.search(text)
        if not match or match.group(1).strip(" '\"") != package:
            errors.append(f"{skill_file.relative_to(ROOT)}: frontmatter name must be {package}")
        version = version_file.read_text(encoding="utf-8").strip()
        if not SEMVER.fullmatch(version):
            errors.append(f"{version_file.relative_to(ROOT)}: expected SemVer")
        versions[package] = version
    return versions


def validate_links(errors: list[str]) -> None:
    for markdown in release_files():
        if markdown.suffix.lower() != ".md":
            continue
        text = markdown.read_text(encoding="utf-8")
        for raw_target in MARKDOWN_LINK.findall(text):
            target = raw_target.strip()
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            path_text = unquote(target.split("#", 1)[0])
            if path_text and not (markdown.parent / path_text).resolve().exists():
                errors.append(
                    f"{markdown.relative_to(ROOT)}: broken local link: {raw_target}"
                )


def validate_content(errors: list[str]) -> None:
    for path in release_files():
        if path.suffix.lower() == ".json":
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                errors.append(f"{path.relative_to(ROOT)}: invalid JSON: {exc}")
        if path.suffix.lower() in {".md", ".json", ".yaml", ".yml", ".py", ".less"}:
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for label, pattern in SECRET_PATTERNS.items():
                if pattern.search(text):
                    errors.append(f"{path.relative_to(ROOT)}: possible {label}")

    component_maps = list(SKILLS.rglob("component-map.md"))
    platform_yushu = list(SKILLS.rglob("platform-yushu.md"))
    expected_component_map = SKILLS / "qifu-shared" / "references" / "component-map.md"
    expected_platform_yushu = SKILLS / "qifu-shared" / "references" / "platform-yushu.md"
    if component_maps != [expected_component_map]:
        errors.append("component-map.md must exist only in qifu-shared")
    if platform_yushu != [expected_platform_yushu]:
        errors.append("platform-yushu.md must exist only in qifu-shared")


def validate_manifest(versions: dict[str, str], errors: list[str]) -> None:
    manifest_path = ROOT / "RELEASE_MANIFEST.json"
    if not manifest_path.is_file():
        errors.append("missing RELEASE_MANIFEST.json")
        return
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid RELEASE_MANIFEST.json: {exc}")
        return
    if manifest.get("schemaVersion") != 1:
        errors.append("RELEASE_MANIFEST.json: schemaVersion must be 1")
    if manifest.get("sourceRepository") != "jingjingtu/qifu-skills":
        errors.append("RELEASE_MANIFEST.json: unexpected sourceRepository")
    if not re.fullmatch(r"[0-9a-f]{40}", str(manifest.get("sourceCommit", ""))):
        errors.append("RELEASE_MANIFEST.json: sourceCommit must be a full Git SHA")
    if manifest.get("packages") != versions:
        errors.append("RELEASE_MANIFEST.json: package versions do not match VERSION files")
    actual_files = {
        path.relative_to(ROOT).as_posix(): sha256(path) for path in release_files()
    }
    if manifest.get("files") != actual_files:
        errors.append("RELEASE_MANIFEST.json: file hashes do not match release contents")


def main() -> int:
    errors: list[str] = []
    versions = validate_packages(errors)
    validate_links(errors)
    validate_content(errors)
    validate_manifest(versions, errors)

    package_validators = (
        (
            SKILLS / "qifu-drawer-form" / "scripts" / "validate_portable_manifest.py",
            "portable component manifest validation failed",
        ),
        (
            SKILLS / "qifu-drawer-form" / "scripts" / "validate_multi_platform_contract.py",
            "multi-platform contract validation failed",
        ),
    )
    for validator, failure_message in package_validators:
        if not validator.is_file():
            errors.append(f"missing package validator: {validator.relative_to(ROOT)}")
            continue
        result = subprocess.run([sys.executable, str(validator)], cwd=ROOT, check=False)
        if result.returncode:
            errors.append(failure_message)

    if errors:
        print("FAIL: drawer release validation")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        "PASS: drawer release validated "
        f"(drawer {versions['qifu-drawer-form']}, shared {versions['qifu-shared']})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
