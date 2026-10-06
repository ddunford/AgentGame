---
name: team-execute
description: Run an approved milestone through bounded role assignments, independent verification and creative review while keeping the project task queue current.
fires-when: Executing multi-role planned work; use a lighter direct workflow for a simple one-owner task.
---

# Execute studio work

Owner: producer. Read AGENTS.md, the game-local adapter, selected task tracker and guides/production-pipeline.md. This procedure uses host-supported delegation; it does not assume a named agent API, model or automated background service.

1. Read the next ready task from the game's authoritative queue. Load its linked specification and acceptance; do not create a second TODO queue.
2. Name the builder, independent verifier and relevant creative/engineering reviewer. Record preconditions, measurable outcomes and evidence before implementation. Acceptance and rejection criteria are fixed before a run and never changed after it, neither loosened nor tightened; a worker may not add its own criteria, and an extra attempt is allowed only for a specific, sourced cause logged before that run. A different label in the builder's context is not independence; if independent review is unavailable, mark that gate pending.
3. Assign bounded work with game constraints, relevant roles/guides, input paths, output/evidence locations and explicit editor ownership. A worker running a series appends one report line per finished run as it goes, so a crash never loses the findings; after a crash the evidence already on disk stays valid, but the noise floor is re-measured in the new session before any new comparison. Do not send an upstream role without the game adapter.
4. Build and save. Only one owner may operate/query the live editor, including PIE and capture. File-only research/review can overlap. Transfer editor ownership before runtime verification.
5. Verify saved results against acceptance using supported controls. Report pass, fail or not tested, with repro/evidence. Run networking/security/server-build checks only for actual project surfaces and targets; a single-player POC does not acquire multiplayer scope from the roster.
6. Have a fresh reviewer judge authored look/feel or non-trivial engineering. Correct defects and rerun affected checks. Tool success, a green compile or a hero image alone cannot satisfy gameplay acceptance.
7. Update the existing queue after meaningful changes. Done requires the declared verification/review; unresolved work gets a tracked home. Surface user-reserved decisions with concrete prepared work, preserving existing authorization for ordinary reversible choices.
8. At a milestone boundary, run process-retro and applicable risk/gate reviews. Save learned game facts in the game repo and reusable process improvements in the framework. Commits/publication follow project policy; no automatic push.

Report the phase/task, builder/verifier identities, actual evidence, pending criteria and next action. The producer must inspect relevant visual evidence before presenting a deliverable as visually ready. This workflow does not restart settled phases or install tools/hooks.
