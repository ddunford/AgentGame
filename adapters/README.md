# Host integration contract

The portable core is AGENTS.md plus role/skill/guide Markdown. An adapter maps
that process onto a host; it does not add capabilities or authority. Model names,
agent-launch APIs, native skill registration and memory settings belong in local
host configuration, not generic role frontmatter.

## Game-local bridge

Merge a section like this into the game's existing instructions:

```markdown
## Studio workflow
Read .studio/GameClaude/AGENTS.md for reusable process.
Game instructions and user choices govern scope and tools.
Framework root/revision: [reviewed path and pin].
Project knowledge and evidence: [game-local paths].
Authoritative task queue: [existing tracker; do not duplicate].
Editor control: [available/preferred method; verify at runtime].
Independent review: [supported agent or human mechanism].
Spend/publication: [existing project policy].
Load only relevant roles, skills and guides from the framework root.
```

Replace the bracketed values. Resolve framework paths from `<studio-root>` and
game paths from the game repository. TODO.md/plan files in procedures are default
examples: map them to the declared queue and linked task detail, including Beads
when selected. Do not create a shadow queue or rewrite established game history.

## Capability mapping

| Capability | Host mapping | If unavailable |
|---|---|---|
| Read instructions | Supported instruction entrypoint or explicit file read | Include relevant Markdown in task context |
| Run a role | Native subagent with role, inputs, acceptance and editor ownership | Builder can continue; arrange independent review separately |
| Independent review | Different agent/context or qualified human | Mark pending; self-review is not independent |
| Tasks/messages | Host-supported delegation and project queue | Saved handoff; never invent a named API |
| Editor operation | Computer control or supported suitable engine tools | Prepare work and report the specific untested runtime check |
| Model/memory | User/host configuration | Inherit defaults; no model-family requirement |
| Hooks | Optional audited host integration | Workflow remains usable; no automatic-enforcement claim |

Hosts recognizing AGENTS.md may load it directly or through the game's bridge.
Other hosts can explicitly read it. This is a portable manual contract, not a
claim of tested auto-discovery/native registration on every product/version.
[Claude compatibility](claude/README.md) remains optional.

## Validate adoption

Run a bounded POC: check instruction loading, single queue, scoped assignments,
one live-editor owner, saved evidence and independent review. Include a
computer-control-only scenario without assuming MCP. Record document checks
separately from live editor/playtest results. Installing the framework does not
prove its workflow passes these checks.
