---
name: activate-discipline
description: Mid-project onboarding for a dormant discipline coming online — the on-ramp a role runs when it goes on the critical path, so it joins a running build oriented, not cold. Ends with its first artifact and a registration with the producer.
fires-when: A staffed-but-dormant discipline reaches its activation phase (guides/production-pipeline.md §3.5) and goes on the critical path — the long-lead activations especially (backend P1, trust-safety P1, character→animation P1, crowd/NPC AI P2, analytics P2, build-engineer P2, monetization P3, and the rest).
---

# activate-discipline

**Owner: `producer`** (who triggers the activation on schedule and confirms it landed) **+ the activating discipline** (who runs the on-ramp). Role briefs are available, but only disciplines selected by the game plan become active (`guides/production-pipeline.md` §3.5); this is the procedure that brings one online without it joining a running build cold and re-deriving what the studio already settled.

It exists because a role that activates into a phases-deep build with no on-ramp either stalls while it reconstructs context or, worse, builds on assumptions the vault already closed. The on-ramp makes the first thing a newly-active discipline does *orient*, not *guess*.

Doctrine this enforces: **spec-first** (2) — a discipline produces its first artifact against the committed spec, not an opinion; **traceability** (8) — its first artifact declares its verification; **docs written as current** (12) — it reads the world as it is now, not the edit history that got there.

## When it fires

The producer activates an applicable discipline when the consuming game plan requires it; §3.5 is a conditional catalogue, not a universal staffing mandate. For in-scope disciplines, activation follows the selected phase — not the moment its agent was authored. The **🔴 long-lead** activations are the ones this on-ramp matters most for, because they land in a build that is already moving and feed chains that cannot be spun up at their peak:
- **P1:** `backend-engineer` (architect the schema), `trust-safety` (policy), `character-artist`→`animator` (identity + rig spike), `creator-tools-designer` (UGC spike), `localization` (externalize), `accessibility` (principles), `compliance-advisor` (framing), `performance-engineer` (budgets), `user-researcher`, `ui-ux-designer`, `concept-artist`, `narrative-designer`.
- **P2:** `ai-engineer`, `build-engineer`, `analytics-engineer`, `vfx-artist`, `qa-functional`.
- **P3–P4:** `monetization-designer`, `cinematics`, `live-ops`.

## Procedure — the on-ramp a role runs when it comes online

1. **Read the spec.** the game’s declared specification (for example `SPEC.md` at the game root) — what the game is and the per-phase definition-of-done — then the design detail under `docs/design/` for the area you own. Never build on the vault's edit history; read it as current (doctrine 12).
2. **Read your own guide.** Your craft depth lives in your `guides/` reference (mapped in `guides/production-pipeline.md` §3.1). It is your standing method; do not re-invent it.
3. **Read the current plan and where the build actually is.** The open `plan/<phase>.md` and its "you are here" line, `plan/game-roadmap.md` for the arc, and `plan/risk-register.md` for any risk you now own or feed. You are joining mid-motion — know what has already shipped and what is in flight before you touch anything.
4. **Read your handoff-graph row.** `guides/production-pipeline.md` §3.3 — who feeds *you* (you cannot finish before those upstream hand off) and whom *you* feed (they are waiting on you). This is the single most important orientation step for a long-lead role: it tells you why you activated now and what your late start would cascade into.
5. **Confirm your activation is real, not premature.** Check §3.5 says this is your phase and your upstream inputs (step 4) exist. If they don't, you activated too early — surface it to the producer rather than building on absent inputs.
6. **Produce your first artifact.** The deliverable your phase's checklist (`guides/production-pipeline.md` §3.2) names for your discipline — the backend schema decision, the trust-&-safety policy sketch, the perf budgets, the character identity call. Spec-first (doctrine 2): committed, and against the spec. Route it through the normal gates — a fresh verify/judge owner, never self-signed (doctrine 1).
7. **Register with the producer.** Report that you are live: what you now own, your first artifact and where it landed, what you are blocked on (and on whom, per step 4), and any risk-register row you now hold. The producer folds you into the plan's task flow and updates the "you are here" line. You are not "active" until this registration closes the loop.

## Block these

- Building before orienting — a first commit before steps 1–4 is a role guessing at settled facts.
- Activating on assumptions whose upstream inputs don't exist yet (step 5) — that is the late-start cascade the schedule exists to prevent, run in reverse.
- A first artifact self-signed by the discipline that produced it (doctrine 1).
- Going live silently — without the step-7 registration the producer's "you are here" is already stale.
