---
name: build-spec
description: Establish the repo-canonical game spec — a single SPEC.md at the repo root that owns the top-level definition of what the game is and the definition-of-done, links the detailed design docs in-repo, and makes a clone self-contained (no external vault dependency).
fires-when: Before the plan is stood up, whenever "what the game is + when it's done" is not yet a self-contained, repo-canonical artifact — the design lives only in an external vault, or nowhere yet, or SPEC.md exists and needs checking for completeness. Sits UPSTREAM of bootstrap-from-spec (define the game → forecast the phases → run). Not for editing a settled spec's content (that is a normal vault/doc edit) and not for planning (plan-milestone / bootstrap-from-spec).
---

# build-spec

**Owner: `knowledge-keeper`** (framing the definition-of-done with the relevant Director; greenfield interview with the owner). The level *above* `bootstrap-from-spec`: that skill turns a committed spec into a phase roadmap and decomposes it; this one **produces the committed spec it reads**, as a self-contained, repo-canonical artifact. It is the first link in the standup chain — **build-spec → bootstrap-from-spec → team-execute** (define the game → forecast the phases → run).

Doctrine this enforces: **spec-first** (2) — the plan is drawn from a committed spec, never invented, so `SPEC.md` must exist and be canonical *before* `bootstrap-from-spec` runs; **one fact, one home** — `SPEC.md` owns the top-level definition and the definition-of-done outright and **links** the detail rather than restating it; **written as current** (12) — the spec reads as if written fresh today, no changelog; **guides/docs are living** (13) — the repo is the one home, so the spec cannot depend on an external system a clone can't read.

## The one discipline that makes the spec load-bearing

`SPEC.md` at the repo root is the **repo-canonical single source of truth** for *what the game is* and *when it's done*. That means two boundaries, held exactly:

- **`SPEC.md` owns** the top-level definition (pitch, the core reframe, pillars, anti-goals, audience, the core loop, the settled decisions in summary) **and the definition-of-done in full** (the game's per-phase gates). It is the entry point a cold reader opens first.
- **The detailed design docs own the detail** — the loop elaborated, the feature-level acceptance, the spatial metrics, the look bible, the technical architecture. They live **in the repo** (`docs/design/`), and `SPEC.md` **links** them; it never restates their content. A summary spine plus a link is not duplication; a second copy of the detail is.
- **`<studio-root>/` owns studio process and engine/tooling knowledge — never game design.** The per-phase *deliverable checklist* (`guides/production-pipeline.md §3.2`) is process and stays there; `SPEC.md`'s definition-of-done is the *game-specific* gate for each phase and **links** §3.2 for the generic deliverables that operationalize it.

The point is self-containment: a fresh clone must answer "what is this game, and when is it done?" from the repo alone, with no external vault, wiki, or MCP server in the loop. Where a design vault exists elsewhere, it becomes the owner's **optional read-only mirror** — never a second source of truth. One home, in the repo.

## Procedure

1. **Frame the source and pick the mode.** Establish where the design currently lives and choose the branch:
   - **synthesize** — design docs already exist (an external vault, a folder of docs, a wiki). Consolidate them into a canonical repo `SPEC.md` and bring the detail into the repo.
   - **greenfield** — no design docs exist. Interview the owner, then build `SPEC.md` from the answers.
   - **coverage-check** — a `SPEC.md` already exists. Verify it plus the in-repo detail docs capture everything the source design holds, and report gaps. A completeness gate, run before `bootstrap-from-spec` trusts the spec.

   ---

   ### Mode A — synthesize (existing design → canonical repo spec)

2A. **Read the source design in full.** Every design doc, wherever it lives — pitch/vision, the loop, the decisions log, the discipline docs (design, art, world, tech), and the stage/process artifacts. Read the studio's per-phase gate reference (`guides/production-pipeline.md §3.2`) and the roadmap so the definition-of-done can be stated per phase. Do not invent design the source does not support — where the source is silent on something `SPEC.md` needs (a downstream DoD, an unsettled call), that is a gap to surface, not to fill.
3A. **Bring the detail docs into the repo.** Mirror the source's design-doc tree into `docs/design/`, preserving its structure (the root spine — vision, roadmap, decisions-log, index, memory-map — plus the discipline folders design/ art/ world/ tech/ and the stage folders). These become the in-repo canonical detail docs `SPEC.md` links to. The mirror is faithful; content is written-as-current already, so copy, don't rewrite.
4A. **Write `SPEC.md` at the repo root** as the canonical top-level definition, drawn from the source and stating each thing once:
   - **Pitch · the core reframe · pillars · anti-goals · audience** — the crisp canonical statement of each; link the detail doc for depth.
   - **The core loop** — the game's central loop, named and stated as the flywheel/verb spine; link the detail.
   - **Settled decisions** — the concept calls, the durable platform decisions, and any engineering ADRs, one line each; the **authoritative table with rationale stays in the decisions log** (link it), so `SPEC.md` carries the summary spine only.
   - **Definition-of-done, per phase** — the game's own gate for each phase (the current milestone's stated verbatim), linking `guides/production-pipeline.md §3.2` for the generic deliverable checklist that operationalizes each gate. This section `SPEC.md` **owns outright**.
   - **A map** at the top: what `SPEC.md` owns, what `docs/design/` owns, what `<studio-root>/` owns — so the boundaries are legible to the next reader.
5A. **State the one-source discipline** in `SPEC.md` and in a `docs/design/` README/index: the repo is now canonical; design edits happen here; any external vault is the owner's optional **read-only mirror**, not a second source of truth. Then run the coverage-check (step 2C) as a self-check before handing off.

   ---

   ### Mode B — greenfield (no docs → interview → spec)

2B. **Interview the owner** to establish the definition. Ask, in order, and stop at anything owner-reserved rather than guessing:
   - **What is the game?** — the one-paragraph pitch, and the single core reframe/hook if there is one.
   - **Who is it for?** — primary/secondary/tertiary audience, and the age target (it drives compliance downstream).
   - **What is the core loop?** — what the player does moment to moment, and why it retains.
   - **What are the pillars?** — the few load-bearing values every feature must serve.
   - **What are the anti-goals?** — what the game is explicitly NOT, especially the one guarded hardest.
   - **What is "done"?** — the definition-of-done for the first provable milestone (the vertical-slice test), stated verbatim in the owner's words, and a rough read on what later phases must prove.
3B. **Scaffold the in-repo design docs** the answers justify — at minimum the root spine (`docs/design/` index, vision, roadmap, decisions-log, memory-map) and the discipline folders the game actually needs (see `guides/design-docs.md` for the shape). Seed each with what the interview settled, written as current. `SPEC.md` links these; they hold the detail as it grows.
4B. **Write `SPEC.md` at the repo root** from the interview answers, same structure and same ownership boundaries as Mode A step 4A — pitch, reframe, pillars, anti-goals, audience, core loop, settled decisions (summary → decisions log), the per-phase definition-of-done (owned outright), and the ownership map at the top.
5B. **State the one-source discipline** (Mode A step 5A) and **flag every unresolved owner-reserved gap** the interview left open, so `bootstrap-from-spec` stops at it rather than planning past it. Then run the coverage-check as a self-check.

   ---

   ### Mode C — coverage-check (verify the spec is complete and self-contained)

2C. **Check `SPEC.md` against the source design and against its own contract.** Confirm, and report any gap by name:
   - **Definition present** — pitch, reframe, pillars, anti-goals, audience, core loop, settled decisions summary are all in `SPEC.md`, each stated once and linking its detail doc.
   - **Definition-of-done present** — a per-phase gate for every phase, the current milestone's stated verbatim, linking §3.2. This is the section most often left thin.
   - **Detail is in-repo** — every design doc the source holds has a home under `docs/design/`; nothing `SPEC.md` links resolves only to an external vault/MCP/wiki. A clone can answer "what is the game + when is it done" from the repo alone.
   - **No duplication** — `SPEC.md` summarizes and links; it does not restate the detail docs, and it does not restate `<studio-root>/` process content. The decisions log, not `SPEC.md`, holds the authoritative rationale.
   - **One-source rule stated** — the repo-canonical / external-mirror-read-only discipline is written into `SPEC.md` and the `docs/design/` index.
3C. **Report the coverage verdict** — complete, or a named list of what is missing or duplicated. If gaps exist, resolve them via Mode A (missing detail/synthesis) or surface them to the owner (missing owner-reserved answers); coverage-check finds gaps, it does not invent the content to fill owner-reserved ones.

   ---

6. **Hand off to `bootstrap-from-spec`.** With `SPEC.md` committed and coverage clean, the spec is the committed artifact the standup reads. `build-spec` does not itself decompose or plan — it establishes the spec, then stops.

## What it produces

- `SPEC.md` at the repo root — the repo-canonical single source of truth: the top-level definition + the per-phase definition-of-done, linking the detail docs and `guides/production-pipeline.md §3.2`, with the ownership map at the top and the one-source rule stated.
- `docs/design/` — the in-repo canonical detail docs `SPEC.md` links (the design-doc tree, mirrored or scaffolded), with an index/README stating the one-source discipline.
- A coverage verdict — complete, or a named gap list.
