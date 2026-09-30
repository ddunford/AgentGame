---
name: asset-breakdown
description: Turn a decomposed phase plus its spec and design docs into the phase's asset bill-of-materials — every asset it needs, by class, each classified HAVE / ACQUIRE / GENERATE, with a concrete Fab search list ready for fab-acquire.
fires-when: After a phase is decomposed (plan-milestone / bootstrap-from-spec) and before any asset is acquired or built. The upstream asset-requirements step: it produces the bill-of-materials that fab-acquire and ingest-asset then work through.
---

# asset-breakdown

**Owner: `tech-artist`.** `art-director` is consulted on the creative-quality and style-fit of every art asset — the breakdown names *what* is needed; the look-bible (`docs/design/art/look-bible.md`) decides whether a candidate is *ours*. Pipeline position: **decompose → asset-breakdown → `fab-acquire` → `ingest-asset` → build.** The downstream half already exists — `fab-acquire` gets a known free asset in, `ingest-asset` measures/curates/collision/budgets it, and `Tools/required-content.json` declares what is already in use. This is the missing upstream step that says, from the plan, *what to get in the first place*.

Doctrine this enforces: **spec-first** (2) — the asset list is drawn from the committed spec and phase plan, never invented at build time; **complete or descope** (6) — nothing the phase builds is missing from the list, and a gap is surfaced, never silently faked. The buy→generate→compose order (free listings first) is the studio asset rule (`ROSTER.md` / project AGENTS.md).

## Procedure

Given a milestone/phase (`plan/<milestone>.md`), `SPEC.md`, and the relevant design docs (`docs/design/` — look-bible, `world/neon-hub.md`, `design/experience.md`, city-design, etc.):

1. **Enumerate every asset the phase needs, by class.** Walk the phase's tasks *and* the design docs behind them, and list each required asset concretely — not "some props", but the actual thing the build task consumes. Cover every class:
   - **Static meshes** — architecture, props, clutter, kit pieces.
   - **Skeletal meshes / characters** — player pawn, NPCs, crowd agents.
   - **Animations** — locomotion sets, gestures/emotes, montages, additives (name the skeleton they must target).
   - **Audio** — ambient bed, diegetic point sources, interactive one-shots, music.
   - **Materials / textures** — master materials, instances, decals, tiling/trim sheets.
   - **VFX / Niagara** — ability cues, ambient life, transitions.
   - **UI / UMG** — widgets, icons, fonts.
   - **Anything else** — decals, fonts, HDRI/sky, PCG source assets.
2. **Classify each asset — HAVE / ACQUIRE / GENERATE.**
   - **HAVE** — already in `Content/ElseCity/` or a declared vendor pack; check `Tools/required-content.json` before claiming it. Cite the path or pack.
   - **ACQUIRE** — get it from Fab / Megascans / MetaHuman, **free listings first** (buy→generate→compose order).
   - **GENERATE** — author it, or Meshy/ElevenLabs-class generation (audio via `sound-designer`, characters via `character-artist`).
   Classification is honest, not aspirational — "we probably have something close" is HAVE only if you can name the asset.
3. **For each ACQUIRE, emit a concrete Fab search list** ready to hand to `fab-acquire`: the search term(s) plus the acceptance criteria that `ingest-asset` will enforce — budget class (polycount), PBR maps present, correct scale/pivot/forward, **standard project skeleton** for characters/animations, and **licence = free**. A search line with no acceptance criteria is not done.
4. **Emit the breakdown as a committed artifact.** Write it to `docs/design/asset-breakdown-<phase>.md` (alongside the phase's other design docs; if the phase keeps its docs under `plan/`, co-locate there instead — one convention per project, stated in the file header). This is the phase's bill-of-materials: `fab-acquire` and `ingest-asset` work through the ACQUIRE rows, the build tasks consume the results, and each landed ACQUIRE updates `Tools/required-content.json` (the declare step is `ingest-asset`'s — this skill points at it, it does not do it).
5. **Hand off.** Each ACQUIRE row → `fab-acquire` (search + add) → `ingest-asset` (measure/curate/collision/budget/provenance/declare). Each GENERATE row → its authoring owner. HAVE rows are ready to place. Re-check have-vs-need whenever the phase re-scopes at a gate.

## Quality bar

- **Complete** — nothing the phase builds is unlisted. If a build task will need an asset, it is in the breakdown.
- **Actionable** — every ACQUIRE carries a real search term *and* acceptance criteria, not "find something suitable".
- **Honest classification** — HAVE means named-and-verified; ACQUIRE respects free-first; GENERATE names the authoring owner. No aspirational HAVEs.

## Common failure modes

- **The invisible asset** — a build task blocks mid-phase because an asset nobody listed turns out to be needed. That is a breakdown that wasn't complete.
- **"We'll find something"** — an ACQUIRE with no search term. It defers the real work to the moment it's most expensive.
- **Paid when free exists** — skipping the free-listings-first order and acquiring a paid asset.
- **Compatibility ignored** — an animation on the wrong skeleton, a mesh at the wrong scale, a mesh over its budget class. The acceptance criteria exist to catch this before `ingest-asset` does.
- **Stale have-vs-need** — classifying against a `required-content.json` that drifted, or not re-checking after the phase re-scopes. Re-check at every gate.
