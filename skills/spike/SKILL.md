---
name: spike
description: Prove an unknown — a mechanic, an area, or an engine assumption — in an isolated throwaway map, get it reviewed, then backport the finding or discard it, before any of it touches the main build.
fires-when: Preproduction and any time an approach is a guess — "does this feel right", "does this area read", "will UE behave this way", a mechanic or space not yet proven feasible or fun. The main build is never touched by unproven work.
---

# spike

**Owner: the relevant discipline agent** (whoever will build the real thing — `gameplay-engineer`, `level-designer`, `network-engineer`…), **reviewed by `creative-director`** for a mechanic or area (`creative-review` when the built prototype needs the fresh is-it-good pass). The spike lane runs alongside every phase; where it sits in the pipeline is in `guides/production-pipeline.md`, and the isolate-then-integrate rule is `guides/workflow.md`. Link, never restate.

Doctrine this enforces: **spike before you integrate** (3) — prove it in an *isolated* throwaway map, get it reviewed, then pull it in or discard it; **build ≠ verify** (1) — the builder never self-approves the spike; **capture the lesson immediately** (13) — a finding that stays in disposable scratch is lost the moment that directory is cleared.

## Procedure

1. **Frame the one unknown.** State the single question the spike answers — *does this mechanic feel right*, *does this area read as a place*, *does UE behave the way we assumed*. A spike with two questions is two spikes. If the question is "how does the engine behave", the record is a source citation, so pair this with `verify-engine-claim` — a spike proves *feel and feasibility*; only source settles *behaviour*.
2. **Isolate in a throwaway map.** A dedicated sandbox / `.research` map, never the main build — doctrine 3 is absolute: the main map is never touched by unproven work, not even temporarily.
3. **Build the crudest prototype that answers the question.** Solid enough to judge, no polish — complete-or-descope (doctrine 6) does not bind a spike, because a spike is *declared throwaway*, not a deliverable. What must be real is the *answer*: a fly-cam impression is not a walked, gravity-on verdict (doctrine 5). Drive the editor per `guides/tooling-ue.md` — the supported control methods and evidence requirements — and obey its serial/save-verify/never-taskkill rules even for throwaway work.
4. **Review by the right authority, fresh (doctrine 1).** A mechanic or area goes to `creative-director` for a **pull-in / change / discard** call before it can be integrated; a built prototype that needs the is-it-good judgement gets a fresh `creative-review`. The agent that built the spike is the worst judge of it.
5. **Backport the finding or discard it (doctrine 13) — this is the point of the spike.** A kept finding is written as present-tense fact into the owning guide / design doc (an engine fact into `guides/unreal-engine.md` with its citation) *before* anyone builds on it. A rejected approach is discarded — and, where its history stops the mistake recurring, the *reason* is kept as present-tense guidance ("we tried X; it failed because Y").
6. **Integrate the finding, never the prototype.** Only a reviewed, backported finding enters the main build — rebuilt to spec by the discipline. The throwaway map and its crude assets are discarded either way; nothing from the sandbox is promoted wholesale.

## Block these
- Spiking in, or promoting a prototype into, the main build.
- Judging a fly-cam impression instead of a gravity-on walk.
- The builder self-approving the spike.
- Clearing the scratch map before the finding is backported — the knowledge is then gone.
