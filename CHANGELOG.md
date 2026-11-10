# Changelog

## [1.0.0] - 2026-11-10

### Added

- Versioned App Bundles for `basic-chat`, `dashscope-sdk-expert`, and
  `bailian-expert`, each with a self-contained profile, manifest, evaluation
  metadata, and acceptance configuration.
- Complete teaching and DashScope domain Skills within their corresponding
  bundles, without dependencies on sibling Expert directories.
- Seven offline catalog unit tests covering manifest compatibility, profile
  identity, stable Runtime requirements, and default model configuration.
- Main-branch push and pull-request checks for catalog unit tests on Python
  3.10 and 3.13, plus repository-wide pre-commit checks.

### Changed

- All Apps require AgenticX Runtime `>=1.0.0,<2`; CI installs the Runtime
  distribution from PyPI, not the Runtime's Git main branch.
- Workspace profile downloads use the canonical `/expert` and
  `agenticx expert` commands. Profiles record their Expert identity for the
  Runtime welcome panel.
- Default text models use `qwen3.8-flash`; model identifiers are lowercase.

### Removed

- Legacy top-level example directories and old `.agenticcli` / `.acli`
  profile layouts. Installable bundles live only under `apps/<name>/`.
