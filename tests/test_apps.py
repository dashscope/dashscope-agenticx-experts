# -*- coding: utf-8 -*-
"""App Catalog schema checks using the installed AgenticX Runtime."""
from pathlib import Path

from dashscope_agenticx.apps.manifest import load_app_manifest
from dashscope_agenticx.apps.store import runtime_compatible


ROOT = Path(__file__).resolve().parents[1]
APP_NAMES = {"basic-chat", "dashscope-sdk-expert", "bailian-expert"}


def test_catalog_apps_are_installable():
    root = ROOT / "apps"
    assert APP_NAMES <= {path.name for path in root.iterdir() if path.is_dir()}
    for name in APP_NAMES:
        bundle = root / name
        manifest = load_app_manifest(bundle)
        assert manifest is not None
        assert runtime_compatible(manifest)
        assert (bundle / manifest.profile).is_dir()
        assert (bundle / manifest.eval_path).is_file()
        assert (bundle / manifest.acceptance_path).is_file()


def test_source_trees_have_no_legacy_profiles():
    source_roots = [ROOT / "apps" / name for name in APP_NAMES]

    for source in source_roots:
        assert not any(source.rglob(".agenticcli"))
        assert not any(source.rglob(".acli"))


def test_catalog_has_no_top_level_examples():
    assert not (ROOT / "basic-chat").exists()
    assert not (ROOT / "dashscope-sdk-expert").exists()


def test_expert_profiles_are_self_contained():
    for name in ("basic-chat", "dashscope-sdk-expert"):
        profile = ROOT / "apps" / name / ".agenticx"
        assert (profile / "config.toml").is_file()
        assert (profile / "custom-extensions.toml").is_file()
        assert (profile / "hooks.toml").is_file()
        assert list((profile / "skills").glob("*.md"))

    skills = ROOT / "apps" / "dashscope-sdk-expert" / ".agenticx" / "skills"
    assert {
        "text-generation.md",
        "multimodal.md",
        "speech.md",
        "retrieval.md",
        "diagnose.md",
    } <= {path.name for path in skills.glob("*.md")}


def test_apps_require_stable_runtime():
    for name in APP_NAMES:
        manifest = load_app_manifest(ROOT / "apps" / name)
        assert manifest is not None
        assert manifest.version == "1.0.0"
        assert manifest.runtime_requires == ">=1.0.0,<2"
