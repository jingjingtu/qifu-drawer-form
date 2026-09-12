from __future__ import annotations

import argparse
import importlib.util
import unittest
from pathlib import Path


DRAWER = Path(__file__).resolve().parents[1]
SCRIPT = DRAWER / "scripts" / "resolve_platform.py"
SPEC = importlib.util.spec_from_file_location("resolve_platform", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("unable to load resolve_platform.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
PLATFORMS = MODULE.load_platforms(MODULE.DEFAULT_REGISTRY)


def args(**overrides: object) -> argparse.Namespace:
    values = {
        "platform_key": None,
        "name": None,
        "figma_node_name": [],
        "figma_variable_mode": [],
        "template_node_id": [],
    }
    values.update(overrides)
    return argparse.Namespace(**values)


class PlatformResolutionTest(unittest.TestCase):
    def test_resolves_registered_chinese_name(self) -> None:
        result, code = MODULE.resolve(PLATFORMS, args(name="智能运营平台"))
        self.assertEqual(code, 0)
        self.assertEqual(result["platformKey"], "zhineng-yunying")
        self.assertEqual(result["defaultTheme"], "smartops-blue")

    def test_resolves_exact_template_node(self) -> None:
        result, code = MODULE.resolve(
            PLATFORMS, args(template_node_id=["4892:34812"])
        )
        self.assertEqual(code, 0)
        self.assertEqual(result["platformKey"], "zhikexing")

    def test_resolves_exact_variable_mode(self) -> None:
        result, code = MODULE.resolve(
            PLATFORMS, args(figma_variable_mode=["毓数/Light"])
        )
        self.assertEqual(code, 0)
        self.assertEqual(result["platformKey"], "yushu")

    def test_rejects_visual_guess_without_registered_signal(self) -> None:
        result, code = MODULE.resolve(PLATFORMS, args(name="绿色后台"))
        self.assertEqual(code, 2)
        self.assertEqual(result["reason"], "NO_DETERMINISTIC_SIGNAL")

    def test_reports_conflicting_explicit_platform_and_template(self) -> None:
        result, code = MODULE.resolve(
            PLATFORMS,
            args(platform_key="yushu", template_node_id=["4892:34812"]),
        )
        self.assertEqual(code, 3)
        self.assertEqual(result["status"], "CONFLICT")
        self.assertEqual(result["conflicts"], ["zhikexing"])


if __name__ == "__main__":
    unittest.main()
