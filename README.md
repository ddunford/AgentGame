# GameClaude

An **AI-agent-agnostic game studio workflow**: roles, skills, craft guides and independent review. The name is retained for continuity; Claude, MCP, hooks and a companion toolkit are not requirements.

Start with [AGENTS.md](AGENTS.md), [ROSTER.md](ROSTER.md) and [ONBOARDING.md](ONBOARDING.md).

- agents/: 41 portable role briefs defining responsibilities and outputs.
- skills/: workflow procedures from planning/spikes to QA and retrospectives.
- guides/: production and craft references, loaded as needed.
- adapters/: host integration contracts, separate from process.
- hooks/: optional legacy Claude examples, inactive unless deliberately configured.

Reusable system contracts may be added under modules/ when authored; no such runtime dependency is required. These documents do not launch workers, guarantee expertise or grant permissions.

## Use in a game

Keep a reviewed pinned checkout/snapshot, for example at .studio/GameClaude/. Link its AGENTS.md from the game’s root instructions. Record project paths, task tracker, available controls and constraints in a game-local adapter; see [adapter guidance](adapters/README.md). Existing Claude .claude/ installations can retain that layout and compatibility entrypoint.

The studio owns reusable process. The game owns domain research, vision, settings, assets, licences, tasks and evidence. Do not duplicate its task queue.

Computer control, engine APIs, CLI and MCP are possible control methods. Discover actual capabilities and honour user preferences. [Tool routing](guides/tooling-ue.md) specifies observable outcomes; old MCP details remain an optional reference. Documentation checks do not prove live gameplay or native integration on every host.

## Licence

Copyright ©2026 Munero Limited. [LICENSE](LICENSE) remains all rights reserved, licence TBD/internal studio framework. This change does not relicense the repository or call it open source.
