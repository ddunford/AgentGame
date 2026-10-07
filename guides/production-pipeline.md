# Guide — The studio SOP (running a milestone end to end)

> **The operating procedure for the whole studio: given a milestone or spec, exactly how it is run to done** — decompose → phases → tasks → per-task test-plan → build → testing → quality gate → review → close — with the owning agent and the method named at every step. `AGENTS.md` states the doctrine and the phase gates; `guides/workflow.md` is the per-*task* choreography; **this is the milestone-level SOP that sits above both** and the phase×discipline reference the whole studio is measured against. It links the craft guides rather than restating them (one fact, one home).

**How to read this doc.** Part 1 is the headline — the repeatable loop for running any milestone. Part 2 is the inventory of what the studio has to run it with. Part 3 is the reference layer the SOP points into: the discipline map, the per-phase deliverables, the handoff graph, and the activation schedule.

---

# Part 1 — The SOP: running a milestone to done

Everything below is driven by the **`producer`**, who owns *when and in what order*, dispatches each step to its owner, and keeps the single "you are here" line true. The producer runs the whole loop via **`team-execute`** (the autopilot the constitution names). The one law the loop exists to enforce: **whoever builds a thing never signs it off** (doctrine 1). Every arrow from build to verify crosses to a *different* agent.

## The loop

```
  MILESTONE / SPEC
        │
  1 FRAME ........... producer + Directors ....... is this the right thing, and what is "done"?
        │
  2 DECOMPOSE ....... producer ................... phases → tasks, each with owner + acceptance + test-plan
        │  (spec-first: level/game-design spec · engineering-heavy → tech-design TDD
        │   · spike unknowns in isolation — via `spike` — before this closes)
        │
  2a ASSET-BREAKDOWN  tech-artist (art-director) . phase bill-of-materials: every asset, HAVE/ACQUIRE/GENERATE
        │  (feeds fab-acquire → ingest-asset → build)
        ▼
  ┌── per task ─────────────────────────────────────────────────────────┐
  │ 3 TEST-PLAN ..... the verifying QA agent ..... declared BEFORE build  │
  │      └ engineering-heavy? tech-design TDD committed + fresh-reviewed   │
  │ 4 BUILD ......... the discipline agent ....... serial on the editor   │
  │      └ instrument as you build (analytics-engineer) if it has a signal │
  │ 5 TEST .......... fresh QA / verify agents ... is it broken/correct?  │
  │ 6 QUALITY GATE .. verify agents .............. pass/fail vs test-plan  │
  │ 7 REVIEW ........ fresh senior eyes ........... is it good / is it sound?
  │      └ art → creative-review · code → code-review (fresh, never author) │
  └──────────────────────────────────────────────────────────────────────┘
        │  (loop per task; file-only steps parallel, all live-editor steps serial)
        ▼
  8 CLOSE ........... producer .................. drain · retro · risk-walk · vault · gate · lessons
        │
     PHASE GATE (Director / owner) → next phase
```

## Step by step — owner and method for each

| # | Step | Owner (agent) | Method / skill | Produces |
|---|---|---|---|---|
| 1 | **Frame** | `producer` + relevant Director | `plan-milestone` | Milestone restated against `roadmap.md`'s definition of done; owner-reserved calls flagged |
| 2 | **Decompose** | `producer` | `plan-milestone` | `plan/<milestone>.md` — phases and tasks, each with **owner + acceptance criteria + verification link** (doctrine 8) |
| 2a | **Asset breakdown** | `tech-artist` (`art-director` consulted) | `asset-breakdown` | The phase's asset bill-of-materials — every asset by class, each **HAVE / ACQUIRE / GENERATE**, each ACQUIRE with a Fab search line; feeds `fab-acquire` → `ingest-asset` → build |
| — | *Spec-first gate (spatial / systems)* | `level-designer` / `game-designer`; Director approves | `guides/level-design.md`, `guides/game-design.md` | Committed spec (plan/metrics/canonical views) *before* any build (doctrine 2) |
| — | *Tech-design gate (engineering-heavy)* | `technical-director` (+ `backend-engineer` / `network-engineer` on their systems); fresh reviewer approves | `tech-design` | Committed TDD (problem/approach/data model/interfaces/failure modes) *before* build — the engineering equivalent of the spec-first gate (doctrine 2) |
| — | *Spike unknowns* | the discipline agent, reviewed by `creative-director`; `engine-verifier` for engine claims | `spike` (isolated throwaway map, doctrine 3); `verify-engine-claim` for engine behaviour | Proven approach, backported to the vault, before the main build is touched |
| 3 | **Test-plan** | the verifying agent (`qa-visual` / `qa-network` / `qa-functional` / `security-reviewer`) | its own battery, declared up front | Each task's test named *before* build, or `[no-test: <reason>]` — no third option (doctrine 8) |
| 4 | **Build** | the discipline agent (see Part 3.1) | the craft guide + `guides/workflow.md`; tools per `guides/tooling-ue.md` | The work, saved; **serial on the editor** — one owner for all live-editor operations |
| 4a | **Instrument** *(if it has a behavioural signal)* | `analytics-engineer` | instrument-as-you-build, not a retrofit | The events/metrics the feature's signal needs, wired in the same pass as the build — never bolted on after |
| 5 | **Test** | `qa-visual`, `qa-network`, `qa-functional`, `security-reviewer`, `engine-verifier` — **fresh, never the builder** | multi-view battery · server+2-clients+negative test · spec-match functional battery · exploit enumeration · source check | Defects against the spec, or a clean pass |
| 6 | **Quality gate** | the verify agents | pass/fail against the committed test-plan | *Is it broken / correct / secure?* — a defect is "doesn't match the spec," not an opinion |
| 7 | **Review** | `art-director` / `creative-review` (art, on-pitch) · `code-review` (engineering soundness) — **always an independent reviewer (different agent/context or person), never the author** | senior craft/creative judgement (`creative-review`); engineering is-it-sound judgement (`code-review`) | *Is it good / is it ours / is it sound?* — standing to say off-pitch, stop |
| 8 | **Close** | `producer` | drain rule (doctrine 6); `process-retro`; `plan/risk-register.md` walk; `knowledge-keeper` for the vault; doctrine 13 for lessons | Every task done/moved/dropped-with-reason · process retro run (`plan/<phase>-retro.md`) · risk register walked row-by-row · vault describes **what was built** · phase file signed off · lessons written into the owning guide · remaining phases re-scoped |

## The inner loop is the whole game

Steps 3–7 repeat **per task** and are the repeatable unit anyone can follow:

1. **The test is declared before the build** (step 3), so "done" is defined before work starts and can't be moved to fit the result.
2. **The builder hands off; it never verifies its own work** (steps 4→5). This is doctrine 1, and it is violated by convenience.
3. **Two different questions, two different gates:** the quality gate (step 6) asks *is it broken/correct*; the review (step 7) asks *is it good*. Both are fresh eyes; neither is the builder. For level work these split further — structural verification (footprints, seating, collision, a full-gravity walk on an unlit level) runs before visual QA (which needs the level lit); see `guides/workflow.md`.
4. **Craft goes through the senior eye before the owner — always.** The owner is never the first competent reviewer of authored look or feel (`guides/workflow.md`).

## Cross-cutting acceptance criteria — design-in now, don't retrofit

Some concerns are **cheap to design in during the current phase and ruinously expensive to bolt on later** — so they are enforced as **per-task acceptance criteria**, not deferred to their full P3 pass. The producer adds the applicable line to a task's acceptance in `plan-milestone`; the verifying agent checks it like any other criterion:

- **Externalize strings** — on *any* task with player-facing text (UI, signage, prompts). No hard-coded display strings; text goes through the localization path from day one (owner `localization`; full pipeline is P3, but the discipline starts at P1).
- **Accessibility basics** — on *any* player-facing surface (a screen, a control scheme, a feedback channel). Remappable input, legible contrast, no colour-only signalling, subtitle-ready (owner `accessibility` for depth; the basics live with `ui-ux-designer` in-screen; full pass is P3).
- **Compliance framing flagged** — on *anything* touching minors, personal data, payments, or the public surface. The task carries a compliance-framing flag so `compliance-advisor` frames the risk *before* it is built, not after (owner-reserved; needs qualified counsel — R7/R8 in `plan/risk-register.md`).

These fire in whatever phase the task lands in. The **full** localization pipeline, accessibility pass, and compliance implementation are scheduled disciplines (§3.5) — these criteria are the cheap-window enforcement that keeps those later passes from becoming retrofits.

## Serial vs parallel

One owner operates the live editor, including captures, PIE and state-dependent queries. File-only research/review may run in parallel. Transfer editor ownership explicitly; see `guides/tooling-ue.md`. This is a workflow coordination rule, not a universal engine deadlock claim.

## Decision rights inside the loop

- **Agent-decidable** (reversible + plan-aligned + no spend + no public surface): `technical-director` decides via the `decide` method and logs it to the decisions log.
- **Owner-reserved** (money, public-facing surface, the vision, irreversible): framed by the Director, **decided by the owner**. The loop stops and waits.

## What tracks what — the trackers, no overlap

Outstanding work and truth are tracked in distinct places, each owning one scope; if they overlap they drift, so one fact has one home:

| Tracker | Owns | Lifecycle |
|---|---|---|
| **the declared project queue** (repo root) | **The live driver** — the flat, ordered, always-current queue of the active phase's work: what's next / in-progress / blocked / done, plus the single "you are here" line. `team-execute` picks the next open item and keeps it current as it works. | Live; drained at phase close |
| **`plan/<phase>.md`** | **Task detail** — each queue item's owner, acceptance criteria, test-plan, and verify/judge owners. The queue links to it; it does not restate the queue's status. | Signed off at close, kept as history. Committed |
| **`plan/game-roadmap.md`** | Milestone/phase status and definitions of done | Durable |
| **`plan/risk-register.md`** | Risks — owner, mitigation, review-gate | Durable; walked every close |
| **`SPEC.md` + `docs/design/`** | The spec — what the game is and the per-phase DoD | Durable |

the declared project queue is the *queue + status*; the phase file is the *detail*. `team-execute` keeps the two in sync — each queue item references its phase-file task, and detail is never copied down into the queue. Small debts with no phase task also live in the declared project queue (its "no other home" section), and survive there across a gate until they land somewhere.

## Close — the drain rule (doctrine 6)

A phase file is signed off **only when every open item in the declared project queue has a new home**: done · moved to `game-roadmap.md` · consciously dropped *with a reason* (a debt with no phase attachment survives in the the declared project queue "no other home" section). Then: confirm the vault describes what was **built**, not what was planned; update `game-roadmap.md`; capture every lesson into its owning guide **in the same session** (doctrine 13). "We'll remember" is not one of the options.

**Then two required close sub-steps run before sign-off:**
- **Process retro** (`process-retro`, owner `producer`) — interrogate how the studio *worked* this phase: what in the SOP, a skill, or an agent's method failed, was missing, or slowed the phase down, and feed the fix back into the process the same session. Produces a committed `plan/<phase>-retro.md`. This is distinct from doctrine-13 craft-lesson capture (which fixes the *content* of a craft/engine lesson into its guide); the retro fixes the *process*.
- **Risk register walk** (`plan/risk-register.md`, owner `producer`) — walk **every row** as part of the re-scope: is it retired (mitigated/accepted/gone — say why and close it), still open (carry forward, re-score against what the phase taught), or newly surfaced (add it with an owner, mitigation, and review-gate)? The three 🔴 long-lead rows (R1/R2/R3) are checked first. Never delete a row silently.

**Then, before the next phase opens: the re-scope review.** Every phase-close triggers a mandatory review of all remaining phases in the roadmap (`plan/game-roadmap.md`) — for each, decide **carry forward / rescope / drop**, and rewrite it as current (doctrine 12). A closing phase almost always reshapes a downstream assumption; a downstream forecast is never treated as locked truth, so it is re-scoped against what this phase actually taught *before* any of it is built. This is the discipline that makes decomposing the whole arc up front a living forecast rather than a waterfall (`skills/bootstrap-from-spec`). Only after the drain, the retro, and the risk walk is the phase file marked complete.

## Skills this SOP references

The callable procedures in `<studio-root>/skills/` that this SOP dispatches to, grouped by where they sit in the loop:

- **Orient & plan:** `resume-work` (cold-session pickup) · `bootstrap-from-spec` (standup → phase roadmap) · `plan-milestone` (frame + decompose) · `asset-breakdown` (phase bill-of-materials) · `team-execute` (the producer autopilot).
- **Establish truth before building:** `verify-engine-claim` (`engine-verifier`) · `vault-doc-update` (`knowledge-keeper`) · `tech-design` (engineering-heavy TDD, pre-build) · `spike` (prove an unknown in isolation, backport or discard).
- **Build & acquire:** `fab-acquire` → `ingest-asset` (assets in) · `harden-endpoint` (`security-reviewer`, client-reachable surface) · `native-iteration` (Live Coding vs persistent rebuild; live binary proven against source; headless automation tests) · `unreal-repo-setup` (`build-engineer`, what Git/LFS carries, safe pushes) · `codex-cli-worker` (a second, non-editor worker pool) · `activate-discipline` (bring a dormant discipline online at its phase, §3.5).
- **Verify & judge:** `qa-visual` battery · `video-capture` (real video of anything that moves, for judges and the owner) · `qa-network` harness · `qa-functional` (spec-match correctness) · `perf-gate` (perf budget, per-task check + P3–P4 hard gate) · `build-validate` (cooked build boots) · `security-reviewer` · `creative-review` (is-it-good, art) · `realism-judge` (blind photo-realism gate for realism-targeted looks) · `code-review` (is-it-sound, engineering) · `playtest` (`user-researcher`, "found the fun" signal) · `decide` (`technical-director`, agent-decidable forks).
- **Close & freeze:** `process-retro` (phase process retro → `plan/<phase>-retro.md`) · `content-lock` (Phase-3 content-complete freeze).

Each skill owns its own *how*; this SOP names *when and in what order* it runs. Where a skill is not yet authored (the deferred cross-cutting passes in §3.5), run the method from the owning agent's definition until it is.

---

# Part 2 — What the studio has to work with

The SOP points at real resources. Here is the inventory.

## Agents — the roster (`ROSTER.md`)

**41 agents authored** — the full leadership spine, the build departments (design, including narrative and creator tooling; art, including character art, animation, concept, VFX and cinematics; engineering, including backend, performance, build/CI and crowd/NPC AI; audio), the builder-independent Verify & Judge layer, Knowledge, and the operate-at-scale disciplines a persistent social world needs (moderation/trust & safety, live-ops, monetization, analytics, localization, accessibility, compliance). Every discipline in the map is staffed. A role activates — goes on the critical path — at the phase the activation schedule (3.5) sets, not the moment it is authored; a role scheduled for a later phase is staffed now and dormant until then. `ROSTER.md` names the roster; Part 3.1 maps each discipline to its phase and status.

## Skills — the callable procedures (`<studio-root>/skills/`)

**Authored procedures, loaded through the chosen host.** The SOP dispatches to them at the steps and gates named in Part 1; the full inventory grouped by loop stage is in "Skills this SOP references" above. Each skill owns its *how*; the SOP owns *when and in what order*. The only unwritten ones are the deferred cross-cutting passes scheduled in §3.5 (authored at their activation phase); until then their method lives in the owning agent's definition.

## Modules — reusable system contracts (`<studio-root>/modules/`)

**Not yet scaffolded.** Referenced by the constitution; authored when a system is stable enough to have a fixed "same config in, same result out" contract.

## Controls and optional integrations

Use available supported controls per `guides/tooling-ue.md`. Computer control is a first-class route. MCP, Remote Control and toolkit details are optional integrations, not studio prerequisites. Tool inventory and measured capabilities belong to the consuming environment, not this generic phase map.

---

# Part 3 — Conditional discipline catalogue

This catalogue includes online-world examples. Apply each deliverable only when its feature/target is in the consuming game’s scope: backend, dedicated servers, replication, UGC, economy, payments and live operations are not requirements for a single-player POC. Record applicable gates in the project plan rather than copying the whole catalogue. Examples of project stages, trademarks or deployment stacks are not current facts about the consuming game.

The SOP above dispatches to disciplines; this is the map of them — who they are, what each phase needs from them, who feeds whom, and when each activates.

## 3.1 The discipline map

All disciplines a game of this ambition needs, grouped by where they sit in the studio. Every row is **HAVE** — an agent plus its guide/method exists. Role briefs exist; live workers and expertise are not implied. what varies between disciplines is *when* each activates, which is where the activation schedule (3.5) — the phase each role goes on the critical path — takes over. Craft depth lives in the linked guide; this table does not restate it.

### Leadership spine — owner-reserved authority
| Discipline | Owner | Status | Method / guide |
|---|---|---|---|
| Creative direction | `creative-director` | HAVE | vision · pillars · anti-goals |
| Technical direction | `technical-director` | HAVE | the `decide` method |
| Production | `producer` | HAVE | `guides/workflow.md`, this guide |
| Fused Director call | `director` | HAVE | owner-reserved gate |

### Build — Design
| Discipline | Owner | Status | Guide |
|---|---|---|---|
| Game / systems design | `game-designer` | HAVE | `guides/game-design.md`, `guides/game-feel.md` |
| Level design | `level-designer` | HAVE | `guides/level-design.md` |
| Narrative & worldbuilding | `narrative-designer` | HAVE | `guides/narrative.md` (story-in-play and worldbuilding; onboarding-as-UI stays `ui-ux-designer`'s) |
| UI / UX | `ui-ux-designer` | HAVE | `guides/ui-ux.md` (single owner — logic + visuals; the old split is resolved) |
| In-game UGC / creator tooling | `creator-tools-designer` | HAVE | `guides/creator-tools.md` (**the pitch itself** — the tooling/systems behind the door; the creator-tool *UI* stays `ui-ux-designer`'s) |

### Build — Art
| Discipline | Owner | Status | Guide |
|---|---|---|---|
| Art direction | `art-director` | HAVE | `guides/art-direction.md` |
| Environment art | `environment-artist` | HAVE | `guides/environment-art.md` |
| Lighting | `lighting-artist` | HAVE | `guides/lighting.md` |
| Tech art (ingest/collision/budgets/PCG/materials) | `tech-artist` | HAVE | `guides/tooling-ue.md`, `guides/environment-art.md` |
| Concept art / previz | `concept-artist` | HAVE | `guides/concept-art.md` |
| VFX / Niagara | `vfx-artist` | HAVE | `guides/vfx.md` |
| Character design & character art (MetaHuman/Fab) | `character-artist` | HAVE | `guides/character-art.md` |
| Animation (rig/retarget/Control Rig/IK/state machines) | `animator` | HAVE | `guides/animation.md` |
| Cinematics / Sequencer | `cinematics` | HAVE | `guides/cinematics.md` (owns Sequencer/cameras/cutscenes; `animator` owns montages/emotes) |

### Build — Engineering
| Discipline | Owner | Status | Guide |
|---|---|---|---|
| Gameplay engineering | `gameplay-engineer` | HAVE | `guides/game-feel.md`; GAS facts in `guides/unreal-engine.md §3` (a GAS-implementation guide is **to author**) |
| Networking | `network-engineer` | HAVE | `guides/networking.md` |
| Editor-tools programming | `tools-programmer` | HAVE | `guides/tooling-ue.md` |
| Performance / optimization | `performance-engineer` | HAVE | `guides/performance.md` (sets budgets P1, perf gate P3–P4 · 3.5) |
| Build-release / DevOps / cook / packaging / CI | `build-engineer` | HAVE | `guides/build-release.md` (needs a source-built engine · 3.5) |
| Backend / online services (accounts, DB, transactions, matchmaking, save-infra, EOS, server-fleet) | `backend-engineer` | HAVE | `guides/backend-services.md` (**long-lead — architect P1 · 3.5**) |
| Crowd / NPC AI | `ai-engineer` | HAVE | `guides/npc-ai.md` (perceived density: real players first, ambient crowd fills the gaps) |

### Build — Audio
| Discipline | Owner | Status | Guide |
|---|---|---|---|
| Audio (SFX, ambience, music, client-side wiring) | `sound-designer` | HAVE | `guides/audio.md` |

### Verify & Judge — builder-independent
| Discipline | Owner | Status |
|---|---|---|
| Visual QA | `qa-visual` | HAVE |
| Network QA | `qa-network` | HAVE |
| Creative review ("is it good") | `creative-review` | HAVE |
| Security review (client-endpoint) | `security-reviewer` | HAVE (client-endpoint only) |
| Engine verification | `engine-verifier` | HAVE |
| Functional / gameplay QA | `qa-functional` | HAVE (spec-match correctness — the gap visual/network QA don't cover) |
| Playtesting / user research | `user-researcher` | HAVE (moderated playtests, synthesised into findings) |

### Knowledge & Ops
| Discipline | Owner | Status | Guide |
|---|---|---|---|
| Knowledge / design docs | `knowledge-keeper` | HAVE | `guides/design-docs.md` |

### Operate — the live game
| Discipline | Owner | Status |
|---|---|---|
| Community / moderation / trust & safety | `trust-safety` | HAVE (**long-lead — policy P1, tooling P2 — 3.5**) |
| Monetization / storefront / payments | `monetization-designer` | HAVE |
| Live-ops | `live-ops` | HAVE |
| Analytics / telemetry | `analytics-engineer` | HAVE |
| Localization | `localization` | HAVE |
| Accessibility | `accessibility` | HAVE (dedicated full-pass owner; `ui-ux-designer` still owns the basics in-screen) |
| Legal / IP / compliance / age-verification / privacy | `compliance-advisor` | HAVE (advisory — frames risk; owner-reserved and needs a qualified human lawyer) |

**Tally:** **41 HAVE** across all 41 discipline rows — every discipline is staffed with an agent and its guide. The open question for any role is never *whether* it is staffed but *when it activates* and goes on the critical path — 3.5.

## 3.2 Per-phase deliverable checklists

Each phase passes its gate only when its deliverables **exist and are committed** (doctrine 2). A gate failure is therefore "deliverable X is missing," not an opinion. Each deliverable names the discipline that produces it; a not-yet-active discipline whose deliverable a phase needs is a blocking dependency the activation schedule (3.5) must have already scheduled.

### Phase 0 — Ideation → gate: **greenlight (owner)**
- `vision.md`: pitch, pillars, anti-goals, audience — `creative-director`.
- Ranked emotional beats / core-loop hypothesis — `game-designer` + `creative-director`.
- Top technical risks & rough feasibility read — `technical-director`.
- `roadmap.md` with each phase's definition of done, and the design vault scaffolded — `producer` + `knowledge-keeper`.
- **The activation schedule (3.5) reviewed and its early-activation calls confirmed by the owner.**
- *Gate:* the owner greenlights the pitch.

### Phase 1 — Preproduction → gate: **vertical slice approved ("found the fun, and it's feasible")**
- Committed spec (plan / metrics / canonical views) for the slice — `level-designer` + `game-designer`.
- A **playable** slice of the core loop in the main build, walked with full gravity (doctrine 5).
- Art-direction bible & look target — `art-director`; both lighting registers — `lighting-artist`; audio bed proven — `sound-designer`.
- Every core unknown spiked in isolation, reviewed, **and backported to the vault** — all builders + `engine-verifier` (doctrine 3, 10).
- One door / zone transition, server-authoritative and hardened — `network-engineer` + `security-reviewer`; proven server + 2 clients — `qa-network`.
- GAS kit skeleton — `gameplay-engineer`; a proven Fab→ingest→place asset pipeline — `tech-artist`.
- Slice passes the multi-view battery (`qa-visual`) and `creative-review`.
- **The "found the fun" signal comes from a moderated `playtest` with real target-audience players** (`user-researcher`) — the qualitative verdict the gate needs; expert review alone is not it.
- **Long-lead groundwork now active (even if not built): backend/online-services architecture decided; moderation/trust&safety policy sketched; UGC creator-tooling concept spiked; string externalization & accessibility principles adopted.**
- *Gate:* Director + owner — the fun is found (via `playtest`) and it is feasible.

### Phase 2 — Production → gate: **alpha (feature-complete)**
- Every core system implemented (not polished); one path playable end-to-end.
- **Backend/online services live** (accounts, save-infra, matchmaking) — *requires the backend discipline active by now.*
- UGC creator tooling functional; economy & progression tuned — `game-designer`.
- Districts blocked out and art-passed; character + animation pipeline delivering; crowd/NPC AI populating the city.
- Analytics/telemetry instrumented; functional/gameplay QA on every feature (`qa-functional`); performance budgets enforced (`perf-gate`, per-task check on hot-path work).
- **From P2 onward, a cooked build must boot** — `build-validate` (`build-engineer`) cooks, packages, and smoke-launches the artifact, and confirms the dedicated server boots and a client connects. A green editor session proves none of this.
- *Gate:* feature-complete — and the milestone build passes `build-validate`.

### Phase 3 — Content-lock → gate: **beta (content-complete)**
- All content in and locked (`content-lock`, owner `producer` with the discipline leads) — the freeze applies to authored content, not the player-UGC stream; after it, only fixes enter the build.
- Full art/lighting/audio pass on every space; cinematics in.
- **Performance within budget on target — the P3–P4 hard `perf-gate`** (`performance-engineer`), measured on a representative source-built target, not a PIE number; build/release pipeline producing cooked, packaged builds on CI, each passing `build-validate`.
- Age-verification & compliance implemented; moderation tooling live; localization underway; accessibility pass.
- Playtesting/user-research feeding back (`playtest`); full client-surface security review.
- *Gate:* content-complete (`content-lock`) — no new authored content after.

### Phase 4 — Ship → gate: **gold (owner)**
- Cook/package/ship pipeline validated (`build-validate`); perf certified on target hardware — the final P3–P4 hard `perf-gate` (`performance-engineer`); server fleet provisioned.
- Store presence & monetization live; legal/IP/privacy sign-off; localization & accessibility complete.
- Live-ops runbooks; day-one moderation staffed; final security + network QA.
- *Gate:* gold — owner.

### Phase 5 — Live → gate: **per live change**
- Live-ops cadence; analytics dashboards watched; ongoing community/moderation; economy monitoring; incident response.
- Every content update runs the **same gated pipeline** (Part 1) — build ≠ verify does not lapse post-launch.
- *Gate:* per change; owner-reserved for anything public-facing, money, or irreversible.

## 3.3 Dependency & handoff graph

Who feeds whom. An arrow means the downstream discipline cannot finish until the upstream one hands off. Long-lead chains are marked ⏳.

```
vision ─► game-design ─► level-design ─► environment-art ─► lighting ─► set-dress ─► qa-visual ─► creative-review
                │
                ├─► ⏳ backend/online-services ─► economy tuning ─► monetization
                │
                └─► ⏳ UGC creator-tooling ─► ⏳ moderation / trust & safety
                                              (UGC creates the moderation surface)

⏳ character-design ─► ⏳ animation (rig/retarget/Control Rig) ─► gameplay-engineering (state machines, IK, feel)
                                                                        └─► cinematics / Sequencer

concept-art ─► art-direction ─► (environment-art · character-art · VFX)

tech-art (asset pipeline) ─► ALL art build          networking ─► security-review ─► qa-network
build-release / CI ─► packaged builds ─► ship        analytics ─► live-ops ─► community
```

**Reading it:** the art chain (design → layout → dress → light → judge) is the well-worn path the studio already runs. The three ⏳ chains — backend, UGC→moderation, and character→animation→gameplay — are where late activation bites, because each has multiple links and a long lead time.

## 3.4 Load across the phases

Where each discipline switches on and how hard it works across the phases. `on` = ramp-up / groundwork, `PEAK` = heaviest load, `·` = maintenance, blank = not yet active. The point of the table is that a long-lead discipline must be *active before* its PEAK column, not spun up at it.

| Discipline | P0 | P1 | P2 | P3 | P4 | P5 |
|---|---|---|---|---|---|---|
| Creative / technical direction, production | PEAK | PEAK | · | · | · | · |
| Game & level design | on | PEAK | PEAK | · | | · |
| Art direction / environment / lighting / tech-art | | on | PEAK | PEAK | · | · |
| Gameplay engineering | | on | PEAK | · | · | · |
| Networking | | on | PEAK | · | · | · |
| Audio | | on | on | PEAK | · | · |
| ⏳ Backend / online services | | **on (architect)** | PEAK | · | PEAK | · |
| ⏳ UGC creator tooling | | **on (spike)** | PEAK | · | | · |
| ⏳ Character / animation / cinematics | | on | PEAK | PEAK | · | · |
| ⏳ Crowd / NPC AI | | | PEAK | · | · | · |
| Performance / optimization | | on (budgets) | on | PEAK | PEAK | · |
| Build-release / CI / cook | | on | on | PEAK | PEAK | · |
| Analytics / telemetry | | | on | PEAK | · | PEAK |
| ⏳ Moderation / trust & safety | | **on (policy)** | on (tooling) | PEAK | PEAK | PEAK |
| Monetization / storefront | | | | on | PEAK | PEAK |
| Localization | | on (externalize) | on | PEAK | · | · |
| Accessibility | | on (principles) | on | PEAK | · | · |
| Legal / IP / compliance / age-verify | | on (framing) | on | on | PEAK | · |
| Live-ops / community | | | | on | on | PEAK |

The **bold** cells are the trap: backend, UGC, and moderation each need real work in P1–P2 — before their PEAK — or the PEAK arrives with nothing to build on.

## 3.5 The activation schedule

Every discipline is staffed; each is switched on — put on the critical path — at the phase below. This table sequences every discipline: the phase each role **activates**, and the risk if it activates late. A role scheduled for a later phase is staffed now and dormant until its window. It is a **living decision record** (doctrine 12): the "activates" calls are the recommended defaults and the owner adjusts them — but a role never drops off the schedule silently; it moves only when the owner rewrites its window.

**Every activation runs through the `activate-discipline` on-ramp.** The **Activates** column names *when* a role comes online; `activate-discipline` (triggered by the `producer` on schedule, run by the activating discipline) is *how* — the procedure that brings a dormant discipline into a phases-deep build oriented against the current vault, not re-deriving settled facts cold. It ends with the discipline's first artifact and a registration with the producer.

**Three foundations cannot be spun up at their peak** and are flagged 🔴 long-lead — their heavy build lands later, but their design/architecture must be active in Phase 1:
- **Backend / online-services** — its persistence/account schema shapes the save format and every server-authoritative system.
- **Moderation / trust & safety** — the moderation surface exists the instant UGC ships.
- **Character → animation → gameplay pipeline** — a multi-link chain whose late start cascades into feel-tuning and cinematics. `character-artist`, `animator`, and `cinematics` are staffed; the chain's risk is sequencing (the identity call is upstream of rig, which is upstream of gameplay feel), not staffing.

| Discipline | Snapshot | Activates | Risk if it activates late |
|---|---|---|---|
| 🔴 Backend / online services | HAVE | **P1 architect · P2 build** | Save format, economy, and every server-authoritative system are shaped by the persistence/account schema. Retrofitting forces a data migration and re-architecture of systems built on wrong assumptions. *(`plan/risk-register.md` R1)* |
| 🔴 Community / moderation / trust & safety | HAVE | **P1 policy · P2 tooling** | UGC + all-ages + mixed-social creates the moderation surface the instant UGC ships. No tooling = no safe launch; policy retrofitted after content is in is far costlier. *(`plan/risk-register.md` R2)* |
| 🔴 Character / animation / cinematics | HAVE | **P1 spike · P2 build** (cinematics P3) | Heads the rig→anim→gameplay chain; a late start cascades into feel-tuning and blocks cinematics. MetaHuman/Fab shortens lead time but the identity call is upstream. *(`plan/risk-register.md` R3)* |
| In-game UGC / creator tooling | HAVE | **P1 spike · P2 build** | It *is* the pitch ("every door leads somewhere else"). Its data model constrains backend, moderation, and the economy — a late spike risks building systems it can't plug into. |
| Crowd / NPC AI | HAVE | P2 | City density is a pillar; activate past P2 and the city reads empty at alpha. A core-production system, not polish. |
| Performance / optimization | HAVE | P1 budgets · P2 ongoing · P3–P4 hard gate | Perf debt compounds; a late pass on a locked build forces content cuts. |
| Build-release / DevOps / cook / CI | HAVE | P2 | Gates packaged-build validation and the source-built dedicated server (a Launcher build can't link the server target today — on the critical path to real at-scale multiplayer testing). |
| Analytics / telemetry | HAVE | P2 | Instrument before you need the data; retrofitting events post-launch means launch itself is unmeasured. |
| Monetization / storefront / payments | HAVE | P3 build · P4 live | Public-facing + money = owner-reserved; needs legal. Follows content, but store & payment compliance carry their own lead time before gold. |
| Localization | HAVE | P1 externalize · P3 translate | Cheap to design in (externalize strings day one), expensive to retrofit. Infra decision is P1; translation is P3. |
| Accessibility | HAVE | P1 principles · P3 full pass | Design-in, not bolt-on. Retrofitting remapping, subtitles, colourblind-safe palettes after art-lock is costly and partial. |
| Legal / IP / compliance / age-verification / privacy | HAVE | P1 framing · P4 sign-off | Trademark clearance on `else.city` is already outstanding; all-ages + mature-zone gating + UGC + payments each carry compliance load. Late legal review can block ship. |
| Narrative & worldbuilding | HAVE | P1–P2 | Worldbuilding underpins district identity; can run light through Stage 0 but must be active as districts take shape. |
| UI / UX | HAVE (`ui-ux-designer`, single owner) | **P1** | Owned end-to-end as one discipline — logic and visuals together. Splitting UI logic from UI visuals produces incoherent screens (a screen owned by two roles is owned by neither), which is why this stays one owner. |
| Concept art / previz | HAVE | P1 | Feeds art direction & environment art; the look can run on reference boards short-term. |
| VFX / Niagara | HAVE | P2 | Polish-adjacent; the door-transition VFX is the first real need. |
| Functional / gameplay QA | HAVE | P2 | `qa-visual`/`qa-network` don't cover functional gameplay correctness; needed once mechanics multiply. |
| Playtesting / user research | HAVE | P1 | "Found the fun" is a playtest verdict — the slice gate needs real player signal, not only internal review. |

> **One discipline, one owner — never a persona carrying disciplines that fight for its attention.** The art/design specialists are each their own role: `concept-artist`, `vfx-artist`, `character-artist`, `animator`, and `ui-ux-designer` (which owns UI logic *and* visuals as one — see its row). The engineering/ops disciplines — `performance-engineer`, `ai-engineer` (crowd/NPC AI), `build-engineer`, `backend-engineer` — are each a discrete owner, not bundled into one overloaded role. Narrative/worldbuilding is likewise its own owner, `narrative-designer` (its onboarding-as-UI half stays `ui-ux-designer`'s).

### Deferred cross-cutting skills — authored at activation

Four cross-cutting *skills* are scheduled but **deliberately not yet authored** — writing them before their discipline goes on the critical path is premature (the shape of the work is not yet known). Each is authored **at its activation phase**, by its owning discipline, when the phase makes the need concrete. Until then, the cheap-window design-in is enforced by the per-task cross-cutting acceptance criteria (Part 1), and the method lives in the owning agent's definition.

| Deferred skill | Owner | Authored at | Covers |
|---|---|---|---|
| `loc-pipeline` | `localization` | **P3** | Extract → translate → reimport → build; text-fit and pseudo-localization; culturalization review. (P1–P2 externalize-strings acceptance criterion feeds it.) |
| `a11y-pass` | `accessibility` | **P3** | The dedicated accessibility full pass against recognised game-accessibility standards. (P1–P2 accessibility-basics acceptance criterion feeds it.) |
| `asset-optimize` | `performance-engineer` / `tech-artist` | **P2/P3** | LODs, texture/mesh budgets, draw-call and memory reduction on placed content — the optimization pass `perf-gate` measures against. |
| `load-soak` | `performance-engineer` + `backend-engineer` | **P2–P3** | Sustained-load / soak testing of the persistent world at the CCU target on a representative source-built server (R6/R9 in `plan/risk-register.md`). |

---

## Keeping this SOP honest

This is the `knowledge-keeper`'s standing artifact. When the owner changes an "activates" window, edit the row. When a new discipline need surfaces, add it to the schedule with an owner, an activation phase, and a risk — never left as a silent gap. The status column stays true to the roster: a role is HAVE when its agent and guide exist, and `ROSTER.md` is the source of truth for the roster itself (doctrine 12 — the doc reads as current; git history is the audit trail).
