# Agent-agnostic workflow review

Reviewed 2026-09-30 against the working branch `agent-agnostic-workflows`.

## Scope

Portable process entrypoint, role metadata, host adapters and control-independent
execution. Preserve the existing framework name, licence and Claude compatibility.
No host hooks, MCP server or toolkit were installed or executed for this change.

## Checks run

- `scripts/validate_framework.py`:41 role names/descriptions,25 skill metadata
  entries, roster coverage and15 local Markdown links passed. Standard library
  only; this is not a complete YAML-schema or external-URL validation.
- Git whitespace/diff check passed after formatting corrections.
- Independent reviewer `workflow_pilot` inspected active execution paths. It
  found mandatory ingest/geometry tools, automatic tool-building, concurrency
  wording, fresh-subagent-only review and inactive-hook claims. Those findings
  were corrected and re-reviewed; no actionable adoption blockers remained in
  the reviewed paths.
- Document scenario: computer-control-only host, Beads queue, no subagents.
  Outcome: authorized builder can work with available controls; no required MCP
  installation or duplicate queue; independent sign-off remains pending until a
  different agent/context or person reviews the saved result.

## Limits and follow-through

This is a documentation/contract review, not a native integration certification
for every agent host. No live editor, game traversal or packaged build was tested
by this change. Run a bounded game POC through the actual builder-to-reviewer
handoff and capture process failures before treating runtime adoption as proven.
Historical engine/tool observations and game examples still require local scope
and version checks; they are not new tests of the consuming project.
