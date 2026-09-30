---
name: process-retro
description: The phase-close PROCESS retrospective — interrogate how the studio WORKED this phase, find what in the SOP or a skill failed or was missing, and feed the fix back into the process. Produces plan/<phase>-retro.md.
fires-when: At every phase close, as part of the drain-and-close (guides/production-pipeline.md Part 1 close), before the phase file is signed off and the gate is handed to the Director/owner.
---

# process-retro

**Owner: `producer`.** The studio's feedback organ for its own way of working. It runs at every phase close, after the drain rule and before sign-off, and asks one question the rest of the pipeline never asks: **how did we *work* this phase — what in the SOP or a skill failed, was missing, or slowed us down, and what do we change so the next phase runs better?** The output is a committed `plan/<phase>-retro.md`.

This is the organ whose **absence let process gaps surface reactively** — a missing skill or an unwired SOP step was only ever discovered when a phase tripped over it, never caught by a standing review. `process-retro` makes that review standing.

It is distinct from two things it is easy to confuse with:
- **Doctrine 13 craft-lesson-capture** fixes the *content* of a craft/engine lesson into its owning guide (an engine quirk → `guides/unreal-engine.md`, a lighting gotcha → `guides/lighting.md`). `process-retro` fixes the *process* — the SOP, a skill's checklist, an agent's method, the activation schedule, the handoff graph.
- **Live-ops incident post-mortems** (`guides/live-ops.md`) dissect a *production incident* on a live build. `process-retro` dissects a *phase of development*, whether or not anything broke in production.

Doctrine this enforces: **guides are living — capture the lesson immediately** (13), applied to process; **docs written as current** (12) when a fix is written into a skill or guide.

## Procedure

1. **Open the retro at close, not after.** It runs *inside* the phase-close (`guides/production-pipeline.md` Part 1 close), after the drain rule has given every task a home and before the phase file is signed off. A retro deferred to "later" is a retro that never happens.
2. **Interrogate how the work flowed, task by task.** Walk the phase's task history and ask of each rough patch: was this a *content* miss (→ doctrine 13, into the owning guide) or a *process* miss? Only process misses belong here. Prompts: Where did a task stall waiting on an owner, a gate, or an input the plan didn't sequence? Where did the verify→judge chain get short-circuited or skipped? Where did serial/parallel get called wrong and deadlock or waste the editor? Where did the "you are here" line go stale? Where did a task have no clear owner — the signal a discipline or skill is missing (`guides/production-pipeline.md` §3.1)?
3. **Name the root process cause, not the symptom.** "T4 slipped" is a symptom; "the plan sequenced T4 before its backend input existed, because the handoff graph row was wrong" is a cause. Trace each to the SOP step, skill, agent method, or schedule row that should have prevented it.
4. **Classify each finding by where the fix lands.** SOP step (`guides/production-pipeline.md`) · a skill's checklist (`<studio-root>/skills/<name>/SKILL.md`) · an agent's method (`<studio-root>/agents/`) · the activation schedule (§3.5) · the handoff graph (§3.3) · the risk register (`plan/risk-register.md`). A recurring ownerless task shape is a missing-skill finding — note it; on its third recurrence, the fix is to write the skill.
5. **Apply the fixes this session (doctrine 13 for process).** Rewrite the owning skill/guide/agent *in place*, as present-tense fact — no "v2", no changelog, no dated note (doctrine 12). A process lesson that lives only in the retro file is lost the same way a craft lesson left in a commit message is lost. If a fix is owner-reserved or too large to apply now, log it as a task with an owner rather than leaving it as prose.
6. **Feed the risk register.** Any process weakness the phase exposed that could bite a later phase becomes a row (or updates one) in `plan/risk-register.md`.
7. **Write `plan/<phase>-retro.md` and commit it.** Structure: what worked (keep doing it — validated process, not only failures) · what failed or was missing (with root cause) · fixes applied this session (with the file each landed in) · fixes deferred (as owned tasks) · risk-register changes. Kept as history alongside the phase file; never a source of truth over the SOP it feeds.
8. **Confirm before sign-off.** The producer does not mark the phase file complete or hand the gate up until this retro exists, its same-session fixes are applied, and its deferred fixes are owned. "We'll remember the process problem" is not one of the options.

## What worked belongs here too

Capture the process the phase *validated*, not only what it broke (the same reason feedback is saved from success as well as correction). A sequencing that ran clean, a gate that caught a real defect, a parallelization that saved a day — naming it stops the next phase drifting away from a way of working that already proved itself.
