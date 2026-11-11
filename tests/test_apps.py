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


def test_expert_profiles_pass_download_safety_validation():
    from dashscope_agenticx.cli.experts import (
        _expert_files,
        _validate_expert_profile,
    )

    for name in APP_NAMES:
        bundle = ROOT / "apps" / name
        _validate_expert_profile(bundle, _expert_files(bundle))


def test_source_trees_have_no_legacy_profiles():
    source_roots = [ROOT / "apps" / name for name in APP_NAMES]

    for source in source_roots:
        assert not any(source.rglob(".agenticcli"))
        assert not any(source.rglob(".acli"))


def test_catalog_has_no_top_level_experts():
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


def test_expert_profiles_record_their_identity():
    from dashscope_agenticx.utils.toml import load_toml

    for name in APP_NAMES:
        marker = ROOT / "apps" / name / ".agenticx" / "expert.toml"
        assert load_toml(marker) == {"name": name}


def test_apps_require_stable_runtime():
    for name in APP_NAMES:
        manifest = load_app_manifest(ROOT / "apps" / name)
        assert manifest is not None
        expected_version = (
            "1.0.1" if name == "dashscope-sdk-expert" else "1.0.0"
        )
        assert manifest.version == expected_version
        assert manifest.runtime_requires == ">=1.0.0,<2"


def test_expert_profiles_use_flash_default_and_lowercase_models():
    from dashscope_agenticx.utils.toml import load_toml

    for name in ("basic-chat", "dashscope-sdk-expert"):
        profile = ROOT / "apps" / name / ".agenticx"
        config = load_toml(profile / "config.toml")
        assert config["model"] == "qwen3.8-flash"
        for provider in load_toml(profile / "custom-extensions.toml")[
            "providers"
        ]:
            assert provider["default_model"] == "qwen3.8-flash"
            models = provider["models"]
            assert models[0] == "qwen3.8-flash"
            assert len(models) == len(set(models))
            assert all(model == model.strip().lower() for model in models)
