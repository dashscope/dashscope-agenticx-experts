# DashScope AgenticX Experts

Versioned domain experts and App Bundles for **DashScope AgenticX 1.0**.
This repository contains application profiles and Skills, not a copy of the
AgenticX Runtime.

## Catalog

All bundles live under `apps/<name>/`. There are no legacy top-level Expert
directories or legacy profile layouts.

| App | Purpose |
|---|---|
| `basic-chat` | Minimal conversation profile and reusable teaching Skills |
| `dashscope-sdk-expert` | DashScope SDK usage, diagnosis, and API migration |
| `bailian-expert` | Bailian application design, configuration, and diagnosis |

Each bundle contains `app.toml`, a self-contained `.agenticx/` profile,
evaluation metadata, and acceptance configuration. The SDK Expert includes
its complete domain Skills; it does not depend on a sibling Expert directory.

Each profile includes `.agenticx/expert.toml` with its Expert name. AgenticX
uses this record to display the selected Expert in its welcome panel. The
canonical role-template commands are `/expert` and `agenticx expert`.

## Install an App

Requires Python 3.10+ and AgenticX Runtime 1.0.0.

```bash
python -m pip install "dashscope-agenticx>=1.0.0,<2"
git clone https://github.com/dashscope/dashscope-agenticx-experts.git
cd dashscope-agenticx-experts
agenticx app install ./apps/dashscope-sdk-expert
agenticx app info dashscope-sdk-expert
agenticx app verify dashscope-sdk-expert
```

Inspect the App's manifest and requested permissions before installation.
A checksum verifies content identity, not publisher authenticity. An App's
publisher field alone does not confer official trust.

## Scaffold a Workspace

For a teaching workspace, the Runtime can download a profile from `apps/`
into the current workspace's `.agenticx/` directory:

```bash
export DASHSCOPE_API_KEY="<your-api-key>"
agenticx expert download basic-chat
agenticx
```

Workspace scaffolding is not a substitute for versioned App installation or
permission review. Keep credentials in environment variables or the OS
keyring; never put real secrets in committed profiles.

## Validate the Catalog

With AgenticX Runtime 1.0.0 installed:

```bash
python -m pip install pytest
python -m pytest -q tests/test_apps.py
```

The catalog tests check manifests, runtime requirements, evaluation and
acceptance files, self-contained profiles, and the absence of legacy
top-level Expert directories. They do not call model APIs.
