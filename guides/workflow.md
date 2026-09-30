# Guide — How the studio works (the choreography)

> The concrete task-flow. `AGENTS.md` states the doctrine and the phase gates; this spells out *exactly* how a piece of work moves through the team, so a cold session (or the owner) can see the machine turn. For the level above this — the milestone-execution SOP, the phase×discipline deliverable map, and the discipline activation schedule — see `guides/production-pipeline.md`; this guide is its per-task detail.

## The one-line shape
**Owner intent → Producer plans → the right agent builds → a *fresh* agent verifies → a *fresh* agent judges → the gate → the owner.** Build and verify are never the same agent (doctrine 1).

## The flow, step by step

1. **Owner states intent.** "Build the hub street", "add the door mechanic". Not a spec yet — a want.

2. **Producer decomposes it** into `plan/<milestone>.md`. Every task gets, without exception:
   - an **owner** (an agent from `ROSTER.md`),
   - **acceptance criteria** (what "done" means, concretely),
   - a **verification link** — which independent reviewer checks it, or `[no-test: <reason>]` (doctrine 8).
   - the applicable **cross-cutting design-in criteria** — externalize-strings on any player-facing text, accessibility-basics on any player-facing surface, and a compliance-framing flag on anything touching minors/data/payments/the public surface. These are cheap to design in now and ruinous to retrofit, so they ride on the task's acceptance in whatever phase it lands, ahead of their full P3 passes (`guides/production-pipeline.md` Part 1, "Cross-cutting acceptance criteria").
   The phase file is the task **detail**; the live **queue** those tasks are worked from is the declared project queue (repo root) — the flat, ordered, always-current checklist `team-execute` reads and keeps updated, carrying the single "you are here" line the Producer keeps true at all times (`guides/production-pipeline.md`, "What tracks what").

3. **Design before build (Directors gate).** For anything spatial, `level-designer` writes the committed spec (plan / metrics / elevations / hero views) *before* a primitive is placed. For a system, `game-designer` writes the spec. The relevant Director approves the spec. **No spec, no build** (doctrine 2).

4. **Spike the unknowns first.** If an approach is a guess, build it in an **isolated throwaway map**, get `creative-director` review, then integrate into the main build — or discard (doctrine 3). The main map is never touched by unproven work.

5. **Build — serial on the editor.** The owning build agent (`level-designer`, `gameplay-engineer`, `environment-artist`, `lighting-artist`, `sound-designer`, `network-engineer`, `tech-artist`) does the work, driving the editor per `guides/tooling-ue.md`. **Only one owner interacts with the live editor at a time** — the editor is single-threaded. Save, then work from the saved state.

6. **Verify — fresh, and parallel for file-only work.** The builder hands off; it does **not** sign its own work:
   - `qa-visual` — the multi-view battery (top-down / elevation / eye-level / silhouette) for anything rendered.
   - `qa-network` — server + 2 clients + the negative test for anything networked.
   - `qa-functional` — the spec-match correctness battery (happy path + edges/boundaries/invalid input/state transitions/system interactions) for any mechanic, system, economy rule, or save/load whose correctness isn't a rendered frame or a replicated value.
   - `security-reviewer` — every client-reachable endpoint; names the exploit each check prevents.
   - `perf-gate` — for hot-path or perf-sensitive work, `stat unit` before/after against the committed budget (the P3–P4 hard gate is the milestone-level version, `guides/production-pipeline.md`).
   - `engine-verifier` — any engine-behaviour claim the work rests on.
   These are independent reviewers. File-only passes can run in parallel; live-editor captures, queries and PIE require sole ownership. If independent review cannot run, record the gate pending.

7. **Judge — is it good / is it sound?** Two fresh-eyes judges, by surface:
   - `creative-review` (always an independent reviewer (different agent/context or person)) — for authored look/feel: spec-matches, then scores the ranked beats. Standing to say *off-pitch, stop*.
   - `code-review` — for any non-trivial C++/systems change, **before merge**: architecture, maintainability, convention, and the doctrine rules. The engineering equivalent of the creative senior eye — a fresh reviewer, **never the author** (doctrine 1). `qa-functional`/`qa-network`/`security-reviewer` ask *does it work / is it authoritative / can it be exploited*; `code-review` asks *is it sound*.

8. **The gate.** The Producer assembles the verified + judged result. A phase gate (greenlight / slice / alpha / beta / gold) is crossed by the **Director/owner**, never on the builder's say-so. Owner-reserved calls (money, public surface, vision, irreversible) stop and wait for the owner.

9. **Drain at close.** No open the declared project queue item is left homeless: done / moved to `game-roadmap.md` / consciously dropped-with-reason (a debt with no phase attachment survives in the the declared project queue "no other home" section). Then the phase file is signed off, its record kept as history.

## Level work — structural verification and visual QA are different gates
Two different questions, run as two gates in this order:

- **Structural verification** asks *is it built right* — footprints, seating, collision, walkability. It needs geometry-truth metrics and a full-gravity walk, **not** rendering, so it runs **early, on an unlit level**. This is where floating / colliding / mislaid geometry is caught.
- **Visual QA** (`qa-visual`) asks *does it read right* — massing-in-context, silhouette, the look. It needs the level to be **viewable**, so it runs **only once the level is lit**.

Never fold the two into one gate. Structural defects are caught without a single light; visual judgment waits for light.

### Viewable before visual QA
A level enters visual QA only when it is in a **self-contained, viewable state — it has a saved baseline lighting rig in the level**. A saved baseline lit state is part of "blockout done / ready for QA", not a later polish-only gate. No visual QA on an unlit level.

A visual verdict never rests on lighting that isn't saved in the level. An optional capture tool may inject a transient sun/fill/skylight rig to make an unlit level legible enough to shoot (`guides/tooling-ue.md`) — that crutch produces an *image*, not a QA-of-record: the same level renders black in a real viewport, so the owner cannot reproduce what the tool "passed", and green checks diverge from what the owner sees. If a level needs a rig to be seen, the rig belongs in the saved level.

### Match process weight to the stakes — mechanical QA only
Two different reviews run on built work, and only **one** of them scales to the stakes. Do not conflate them.

- **Mechanical / technical QA** — the structural checks and the `qa-visual` multi-view battery. Asks *is it built right*: is it lit, does it match the spec metrics, no fall-through, no floating/colliding geometry. This one **scales to stakes** — a crude spike or whitebox gets a light structural check, not the full repeated battery. Over-ceremony on throwaway work is itself a process defect: slow and low-value. It does **not** judge craft quality and will never catch "the lighting is unmotivated / makes no sense".
- **Senior craft / creative review** — `art-director` on the look, `creative-review` on-pitch. Asks *is it good*: is it motivated, does it make sense, is it ours. This is **not ceremony and does not scale away** — see the next section.

Weight-to-stakes governs the mechanical QA. It never removes the senior craft eye.

### Craft goes through the senior eye before the owner — always
Any authored *look or feel* — lighting, set-dress, art, audio, any craft/creative deliverable — is reviewed by its **senior domain authority** (`art-director` for the look, `creative-review` for on-pitch) **before it reaches the owner.** The owner is never the first competent reviewer of craft work: **build → senior craft review → owner.** This review can be fast, but it always happens.

This holds for crude and throwaway-ish work too. "Crude" excuses **low fidelity** — a rough shape, a placeholder texture, one register instead of two. It never excuses **unmotivated or nonsensical craft** — e.g. bare point lights floating in the middle of a street with no physical source — and it never excuses skipping the senior eye. Routing raw first-draft craft straight to the owner, in the name of speed or matching ceremony to stakes, is exactly the gate failure the gated studio exists to prevent (doctrine 1): the owner becomes the first competent set of eyes on unfinished work.

### Owner-in-the-loop, fast
Prefer getting a **viewable artifact in front of the owner to walk** over long async QA cycles the owner can't see. Use the requested supported control method efficiently, preserving observable and reproducible results. Scripting is optional, not a prerequisite.

But *fast* still means **through the senior craft eye first** (above): the artifact the owner walks has already passed `art-director` / `creative-review`. Speed comes from cheap iteration, never from making the owner the first reviewer.

## Who decides what
- **Agent-decidable** (reversible + plan-aligned + no spend + no public surface): `technical-director` decides via the `decide` method and logs it.
- **Owner-reserved** (money, public-facing, the vision, irreversible): framed by the Director, **decided by the owner**. Agents recommend; they never self-approve these.

## A worked example — "add a door that teleports the player"
1. Owner: "a door you walk through to somewhere else."
2. Producer: tasks → [design the mechanic · spike it · build it · harden it · verify it · judge it], each with owner + acceptance + verifier.
3. `game-designer` specs it; `technical-director` confirms the approach is sound (routes the "does Iris separate the two spaces?" claim to `engine-verifier` first).
4. `gameplay-engineer` spikes it in an isolated map → `creative-director` reviews the feel → integrate.
5. `gameplay-engineer` + `network-engineer` build it server-authoritative.
6. `security-reviewer` audits the overlap (what can a hostile client send?); `qa-network` runs server + 2 clients + the negative test; `qa-visual` checks it reads.
7. `creative-review` judges whether the *moment* lands.
8. Producer reports; owner gates.

Every arrow that crosses from "build" to "verify" crosses to a **different agent**. That is the whole game.
