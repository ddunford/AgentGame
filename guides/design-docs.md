# Guide — Design docs (the vault)

> Read before creating, structuring, or arguing about where a design fact lives. The core idea: **the design lives as a set of small, cross-linked, always-current docs with one home per fact and a map that finds them — not a monolithic GDD, and not an append-only history.** `agents/knowledge-keeper` owns keeping it honest; this guide defines the shape it keeps.

## Why not one big document

The monolithic Game Design Document is obsolete. Modern practice — and especially small, fast teams — keeps **modular, cross-linked, living documentation**, organised as a wiki/vault with an index that navigates it. The reasons are practical, not stylistic:

- **A monolith rots.** One giant file is never current: nobody re-reads 80 pages to check one number, so the number drifts. Game Developer: *"the days of any monolithic GDD… are long gone"* in favour of *"a living wiki style document… organized with a directory."* Wikipedia calls the GDD a *"living document."*
- **Change is local when structure is local.** Organise by system/subsystem and *"if you change the jump you only update that section"* (Strudo). A lean, sectioned reference (Wayline, Codecks) keeps edits surgical — which is exactly what doctrine 12 and the `knowledge-keeper` require.
- **Navigation beats hierarchy.** A tiny team finds docs by a **map-of-content index**, not by remembering a deep folder tree.

The taxonomy real teams converge on: a **one-page vision/pitch**, a central design reference (not a monolith), **discipline docs** (technical/TDD, art bible, world/level, systems/economy, narrative), and a **decision log**. The scaffold below is that taxonomy.

## The scaffold

```
<vault>/
  index.md          front-door / map-of-content — links into every folder
  vision.md         pitch · pillars · anti-goals · audience  (the one-pager)
  roadmap.md        phase/stage status · gate definitions of done
  decisions-log.md  current-state decision table (see "Why not an ADR log", below)
  memory-map.md     maps each fact → its owning doc, by path

  design/           how the game plays (living reference): core loop, experience, systems, economy
  art/              art bible / style guide, audio direction
  world/            places — one doc per district / area / level
  tech/             architecture / TDD, networking, persistence
  stages/<stage>/   stage-scoped process artifacts (spike findings, playtest & gate reports)
```

The four root files plus the four discipline folders are the durable spine; `stages/` is the disposable process layer. The medium is free — an Obsidian vault, a wiki, or a plain folder of Markdown in the repo — as long as it supports cross-links and one file per topic.

**Root files** are the always-loaded, always-current top layer:
- `index.md` — the map-of-content. Every doc is reachable from here. This is how a cold session or the owner navigates; it is *not* itself a home for facts, only links.
- `vision.md` — the one-pager: pitch, pillars, anti-goals, audience. If it needs a scroll, it is doing too much.
- `roadmap.md` — phase/stage status and each gate's definition of done. The durable answer to "what are we building toward and how do we know we got there."
- `decisions-log.md` — the current-state table of settled decisions (below).
- `memory-map.md` — the fact→doc index the `knowledge-keeper` maintains: for any fact, which doc owns it. This is what makes one-fact-one-home enforceable instead of aspirational.

**Discipline folders** hold the durable, evolving design, split by who owns it: `design/` (systems, loops, economy), `art/` (look and audio bibles), `world/` (one doc per place), `tech/` (architecture, networking, persistence). They map onto the studio's departments, so each has a clear owning agent.

**`stages/`** holds process output scoped to one phase — spike findings, playtest notes, gate reports. This is disposable by design: it records *how a phase went*, not *what the game is*. A finding that outlives its stage is promoted into a discipline doc; it does not live in `stages/` forever.

## The principles

- **One fact, one home.** Every fact lives in exactly one doc; every other reference links to it. Two homes means two truths, and one goes stale. `memory-map.md` records the home; `index.md` links to it.
- **Shallow, not deep.** Prefer more small docs at a flat level over nested folder trees. A tiny team navigates by the index and by links, not by drilling. If a folder needs sub-folders to stay legible, first ask whether the index would do the job instead.
- **Folders give one home; links do the cross-referencing.** Folders are the *storage* decision — one home per doc, by discipline. Links (and the index) are the *navigation* decision — anything relates to anything. Do not try to make the folder tree express relationships; that is what links are for. This is why the structure stays shallow: the folders only need to answer "who owns this," and links carry the rest.
- **Durable docs by discipline; process output by stage.** If a doc describes *what the game is*, it goes in a discipline folder and evolves forever. If it describes *how a phase went*, it goes in `stages/` and is disposable. Keeping these apart is what stops the durable design from silting up with dated process notes.
- **One doc per place.** `world/` gets a doc per district/area/level, not one "world" file. A place changes independently of its neighbours; separate docs keep those edits surgical.
- **Attachments go up as raw files, with a size check.** Upload images full-size as raw files (an upload link and a raw HTTP PUT, or the host's file upload), never as inline base64 text, which long payloads corrupt in transit; confirm the stored size equals the local size. Improve an image by overwriting it at the same path so every embed keeps working.
- **Write as current (doctrine 12).** Every doc reads as if written fresh today. Delete the wrong thing; state the right thing as fact. No changelogs, no "v2", no dated edit notes inside a doc. Keep a *reason* only where it stops a mistake recurring.
- **The scaffold is a starting point, not law.** There is no industry-standard structure. These folder names are a sane default; rename, merge, or split them to fit the game (a narrative-heavy game earns a `narrative/` folder; a game with no economy drops it). What is *not* optional is the shape: a one-page vision, discipline docs not a monolith, a decisions log, an index that maps facts to homes, and write-as-current throughout.

## Why not an ADR log — the deliberate divergence

The standard architecture-decision-record convention (MADR, Microsoft Well-Architected) is **append-only**: you never edit a decision; you write a new record that *supersedes* the old one, and keep the superseded chain as an audit trail. GameClaude **deliberately rejects that** for the design vault.

`decisions-log.md` is a **current-state table**: the row says what is true *now*, with the date it was settled and the rationale. When a decision changes, you **edit the row** — you do not append a superseding record and keep the corpse. A superseded decision is kept only in the one case where its history stops a live mistake recurring ("we tried X; it failed because Y; do not propose X again"), and then it is stated as present-tense guidance, not as an archived record.

This is a conscious trade-off, and the reason is team size. An append-only ADR trail serves a large org that needs to *audit who decided what and when* across teams and years. A tiny studio does not have that problem — it has the opposite one: **an append-only log becomes archaeology nobody reads, and the reader has to reconstruct the current state from a stack of superseded records.** Doctrine 12 optimises for the reader who needs to know *what is true today*, fast, with zero reconstruction. The git history is the audit trail if anyone ever needs one; the doc is for the present.

## Setting up the vault (once per project, at Stage 0)

This is a one-time scaffold, not a recurring process — hence a guide checklist, not a skill. `agents/knowledge-keeper` seeds it:

1. Create the five root files (`index.md`, `vision.md`, `roadmap.md`, `decisions-log.md`, `memory-map.md`) and the discipline folders the game actually needs.
2. `vision.md` first — the one-pager. Everything else hangs off the pillars and anti-goals.
3. `index.md` links to every file created; `memory-map.md` records which doc owns which class of fact.
4. From here on it is maintenance, and maintenance is the `knowledge-keeper`'s standing job: surgical edits, one-fact-one-home, decisions logged, the map kept true. There is no separate "audit the vault" ceremony — the doctrine-12 discipline is continuous.
