---
name: ingest-asset
description: Verify acquired or generated asset scale, dependencies, collision, budgets and provenance before use in the consuming game.
fires-when: Before placing or referencing a newly acquired or generated asset.
---

# Ingest an asset

Owner: tech-artist. Read the game’s asset policy and guides/tooling-ue.md. Use supported computer control or available suitable APIs; no named audit toolkit is required. Hand placement to an independent reviewer.

1. Measure relevant mesh/component/instance geometry, pivot, scale and orientation using editor views, measured dimensions or a verified tool. For skeletal assets check the declared project skeleton. Do not infer rendered geometry solely from aggregate actor bounds; if reliable measurement is unavailable, keep that criterion pending.
2. Check project budgets, PBR maps, texture formats/sizes, LOD/Nanite requirements and collision where relevant. Record observed values and failures.
3. Follow the game’s declared content-root and dependency policy. Use supported reference-aware editor operations. Moving/duplicating can preserve unintended vendor references; inspect transitive dependencies and fix them deliberately. Preserve approved originals and user assets; do not automatically delete packs or redirectors.
4. Set collision for intended gameplay. Validate on the saved asset and actual player interaction, not just a successful import.
5. Record source, licence, permitted use and provenance. Keep generation prompts/settings where applicable. A published technique may be reimplemented; other people's files (engine sample content, demo assets, share-alike or research data) are test references only — never shipped, never a runtime dependency — and are recorded as such. Commit versus external-content declaration follows licence, size and project policy; no universal vendor-folder or asset-commit rule is imposed.
6. Verify saved files, loaded references and a fresh/reproducible checkout or supported dependency audit. Refresh stale registry data when using APIs. A copied asset that still relies on an undeclared local pack is not portable.
7. Update the project’s content manifest if it uses one; do not invent a validator that is not installed. Report missing evidence and hand the result to QA before calling it ready.
