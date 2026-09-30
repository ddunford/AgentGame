---
name: plan-milestone
description: Decompose a milestone or spec into phases and tasks, each with an owner, acceptance criteria, and a named test-plan, committed before any build.
fires-when: Starting or closing a milestone; before building anything whose approach is a guess. Skip for work under a day, or work the vault already specifies.
---

# plan-milestone

**Owner: `producer`** (framing with the relevant Director). Covers steps 1–2 of the SOP loop in `guides/production-pipeline.md` Part 1. The output is the committed `plan/<milestone>.md`.

Doctrine this enforces: **spec-first** (2), **traceability** (8), **spike-before-integrate** (3). Every task carries an owner + acceptance + a verification link, or it is not a task.

## Procedure

1. **Frame the milestone.** Restate it against its definition of done in `roadmap.md`. Name what "done" means concretely. If the milestone has no DoD row, that is the first gap — surface it.
2. **Classify the owner-reserved calls up front.** Anything touching money, the public surface, the creative vision, or the irreversible is owner-reserved — flag it now so the plan stops at it rather than guessing past it. Reversible/plan-aligned/no-spend/no-public forks route to the `decide` method.
3. **Decompose into phases, then tasks.** Break the milestone into the ordered pieces of work. Keep each task small enough that one owner can build it in one pass; too big → split or ask (doctrine 6).
4. **Assign an owner to every task.** Map each to an agent in `ROSTER.md` and the discipline map (`guides/production-pipeline.md` §3.1). A task with a visual *and* networked surface has multiple owners (build + each verifier).
5. **Write acceptance criteria for every task.** What "done" means, concretely and testably — the yardstick a fresh reviewer measures against, not an opinion.
6. **Name the test-plan for every task, before build.** The verifying agent (`qa-visual` / `qa-network` / `qa-functional` / `security-reviewer` / `engine-verifier`) and its check, declared now — or `[no-test: <reason>]`. No third option (doctrine 8).
7. **Order by dependency.** Sequence tasks so no task starts before its inputs exist (`guides/production-pipeline.md` §3.3). Mark editor-mutating tasks — they serialize; read-only tasks can run in parallel.
8. **Route the spec-first work.** Anything spatial gets a committed spec from `level-designer` before build; a system gets one from `game-designer`; the Director approves. An **engineering-heavy system** (persistence/save schema, netcode design, GAS architecture, a transaction model, a service API) additionally names a committed, fresh-reviewed **`tech-design`** TDD as a pre-build deliverable — the engineering equivalent of the spec-first gate. No spec/TDD, no build.
9. **List the unknowns as a spike lane.** Every guess-based approach gets an isolated-throwaway-map **`spike`** task (doctrine 3) with a reviewer, and every engine-behaviour assumption gets a `verify-engine-claim` task. Findings backport to the vault **before** the main build — the backport is a task, not an afterthought.
10. **Commit `plan/<milestone>.md`.** Include a **Current state** ("you are here") line at the top and the task list with status markers: `[ ]` not started · `[~]` in progress · `[!]` blocked · `[x]` done-and-verified.
11. **Stop for the review.** The plan is reviewed before time is spent on spikes. Once decomposed, `asset-breakdown` (owner `tech-artist`) turns the phase into its asset bill-of-materials — every asset, classified HAVE / ACQUIRE / GENERATE — which feeds `fab-acquire` → `ingest-asset` → build. Then hand to `team-execute` to run it.

## Task shape (every row)

`[ ] <task>` — **owner:** `<agent>` · **tool/skill:** `<skill + the specific tool/route the owner drives>` · **acceptance:** `<concrete done>` · **verify:** `<agent + check>` or `[no-test: <reason>]`

The **tool/skill** field names the owning procedure and an available supported control method. See `guides/tooling-ue.md`: computer control, engine APIs and optional adapters can all serve the task. No prescribed MCP/toolkit is required. Describe the required outcome and verification; discover actual capabilities rather than infer them from a role.
