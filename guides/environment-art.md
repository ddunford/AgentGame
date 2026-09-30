# Guide — Environment Art method

> Read before dressing any space. The core idea: **a frozen, walked, approved blockout is a shape; dressing is what turns the shape into a place someone lives or works in.** Dressing is present-or-absent to a checklist and alive-or-dead to a human — and the difference is *intent*. Every prop, decal, texture break and patch of wear answers a question about *who* was here and *what they do*. Evenly-spaced clutter, visible tiling and grid-obvious modularity are the tells that no one is home.

The `environment-artist` agent carries the short rules; this is the depth behind them. It sits alongside `level-design.md` (which owns the massing you dress) and hands off to `light-scene`/`lighting-artist` — composition and light are authored together, not in series.

## The failures this prevents
1. **The asset-flip.** Content that ticks the "props present" box while reading as a warehouse dump — evenly spaced, unmotivated, no story. A checklist says done; a human says dead.
2. **The seams show.** Visible texture tiling, grid-obvious modular repetition, mismatched scale — the eye stops believing the world the instant it sees the construction kit.
3. **Noise or void.** Detail with no hierarchy reads as chaos and kills readability; too little reads as an unfinished grey-box with textures on it. Both fail the same way: the player can't parse the space.

---

## PRINCIPLES

### 1. Compose — silhouette first, then layer, then detail
Placement is composition, not distribution. The compositional *theory* — focal points, leading lines, foreground/mid/background depth, negative space — is owned by `guides/art-direction.md` (Composition & visual hierarchy); this section is its **application to dressing**. Work the reads in this order, because a later one can't fix an earlier one:

- **Silhouette first.** Before any texture or small prop, the massing and large props must read as distinct shapes against the sky/backdrop. Clean silhouette precedes material complexity — model and place readable forms before surface detail ([RMCAD playbook][rmcad]). This is the same silhouette gate `qa-visual` shoots.
- **Depth in every framed view.** Something close, something at conversational distance, something far to anchor the horizon — a flat single-plane read is the amateur tell.
- **Big / medium / small mass rhythm.** Vary object size deliberately — bigger elements catch the eye first, so scale the things you *want* seen up and the filler down ([Game Developer][gamedev-comp]). Uniform-sized props read as inventory, not environment.
- **Dress toward the focal point.** On a walked route the door/hero frontage is the focal point; frame it with surrounding dressing — a doorway, an arch, a window, or a change in colour/value/texture ([MAGES][mages]) — and steer the eye toward it ([StudioBinder][focal]).
- **Negative space.** Rest areas make the dense areas read; wall-to-wall clutter flattens everything to one busy plane — emptiness is a tool, not a gap to fill.
- **Hero / mid / filler hierarchy.** Plan the prop list in three tiers — **hero** props that ground an important place, **mid** props that furnish, **filler** (foliage, small clutter) that softens edges ([RMCAD][rmcad], [Level Design Book][ldb]). Spend fidelity on heroes; filler earns its place only by supporting them.

### 2. Human traces — environmental storytelling with intent
Every believable space answers *who is here and what do they do*. Dressing is the answer, made physical.

- **Placed with purpose, never as decoration.** Set dressing reflects events and occupancy — an overturned chair, worn books, a faded sign, tools mid-task ([gamedesignskills][gds]). Ask of each object: *why is this here, who put it here?* If there's no answer, it's noise.
- **Wear tells the story of use.** Wear patterns are spatial and narrative information. Naughty Dog used ivy coverage on *The Last of Us Part II* to mark neglected/closed buildings and *cleared* ivy to signal buildings the player should enter — the wear both dresses and guides ([gamedesignskills][gds]). Traffic paths wear the floor; hands wear door edges and handrails; weather wears the tops and windward faces. Wear where use is, clean where it isn't.
- **Cluster into stories, not scatter.** Compose set dressing in **clusters of related detail** — proximity, similarity and implied connection let the eye read a group as one idea ([Level Design Book][ldb]). A toolbench: tools + offcuts + a stool + a mug, together. Scattered single props read as random; a cluster reads as an event.
- **Believable, not literal chaos.** Debris that sells a story but blocks movement is solved by baking clutter into static meshes with smooth collision proxies — "the illusion of mess with the feel of grace" ([gamedesignskills][gds]). Never let a story-prop break the walk.

### 3. Break the texture — kill visible tiling
A tiling texture that visibly repeats destroys the read faster than any missing prop. Break it at both frequencies:

- **Macro / micro variation.** Layer the same tileable texture two or three times at *different tiling scales* and blend them, so a large low-frequency variation rides over the small high-frequency detail — the repeat stops reading as a repeat ([World of Level Design][wold], [80.lv][80lv-tiling]). Pair with **distance-based tiling** so the scale adjusts with camera distance.
- **Macro/micro detail overlays.** Combine base PBR maps with a low-frequency detail texture on base-colour and roughness; add high-spec accents around the areas you want grouped and seen ([80.lv][80lv-tiling]).
- **Vertex / colour-paint blending.** Blend two materials across a surface with a vertex-painted or noise mask so edges (a dry wall meeting a damp base, clean meeting grimy) transition organically rather than at a UV seam ([Beyond Extent][be]).
- **Dirt and wear masks.** World-space detail textures and curvature/AO-driven masks add dirt, edge-wear and aging that ignore the tiling grid entirely ([Beyond Extent][be]). Grime pools where water sits and hands don't reach.

### 4. Modular kits, trim sheets, decals — reuse without the grid showing
Reuse is how the world gets built at scale; the craft is making reuse *invisible*.

- **Kit on the grid, dress off it.** Main modular pieces snap to the grid; the *dressing* does not. "It looks always more interesting to break things up on a smaller level" — rotate, scale and off-grid the small components; add freely-placed extensions (ledges, panels, awnings) on top of the big pieces to break the grid locally ([Beyond Extent][be]).
- **Trim sheets** carry shared edge/panel/pipe detail across many meshes from one texture — layer a second UV set with baked normal/AO over the trim UVs for perceived detail at texture-budget cost ([Beyond Extent][be], [80.lv][sanxia]).
- **Decals are the primary grid-breaker.** Projected or atlas decals break repetition without new geometry ([Beyond Extent][be]). Three storytelling roles ([80.lv][sanxia]):
  - **Environmental** — cracks, stains, scuffs, patches; break the tiling and add age.
  - **Text** — signage, notices, carvings; communicate place, language and purpose.
  - **Narrative** — a specific mark of a specific person or event.
- **Silhouette breakers.** Where a modular run repeats a shape, a unique hero piece or a silhouette-breaking prop (a lean-to, a broken section, an overgrowth) stops the eye counting the modules.

### 5. Compose for a *walked* space
The blockout was validated on foot; the dressing is too. Nothing here is judged from a fly-cam.

- **Something at eye level on every walked route.** Eye height is ~152 cm (`level-design.md`). The reads that sell the place — handles, notices, wear, small clutter, a framed focal prop — must land in the eye-level band along the path, not only on rooftops or floors a walker never studies.
- **Terminate sightlines.** Where the path gives a long view, put something worth looking at at the end of it — a focal prop or framed door. A sightline that ends on blank wall is a wasted composition.
- **Frame the views the player actually gets.** Dress for the *walked* framings (which `qa-visual`'s eye-level pass captures), not for a hero screenshot angle. If a framing only works from a spot the player can't stand, it doesn't work.
- **Readability over richness.** As detail goes in, the space risks becoming "illegible and difficult to read" ([Level Design Book][ldb]). Keep navigable-vs-blocked legible; reserve loud colour/value for gameplay meaning; keep materials reading as their substance from distance. Clutter control is a storytelling *and* navigation tool ([RMCAD][rmcad]).

### 6. Asset hygiene at the art level
- **Scale consistency.** One human reference across the whole space; a prop that violates the established scale (door, step and player metrics live in `guides/level-design.md`) breaks belief instantly. Enforce texel density with a reference grid so surfaces share detail density ([RMCAD][rmcad]).
- **Kitbash discipline.** Kitbash toward a clean silhouette and a coherent story, not toward "more stuff." Every kitbashed piece still answers *why is this here*.
- **Seat everything.** Confirm true bases with `GeometryAuditTools` (`measure_true_base`, `sweep_interpenetration`), not lying actor bounds — a top-down capture catches edge-clumping and floaters the eye-level view hides. Props floating, clipped, or driven into tree trunks are the classic seat failures.
- **Place only from the project content root.** Everything is placed from `Content/ElseCity` after `tech-artist`/`ingest-asset` has ingested it — never from a gitignored vendor path (works on this machine, nowhere else). See `AGENTS.md` §Assets.
- **Iterate in stages, in context.** Reach ~50% across many elements and judge them *together* before finishing any one — "don't try to make the 100% final version of every asset" first ([Level Design Book][ldb]). Composition is judged as a whole; a perfect prop in a broken group is still broken.

---

## QUALITY BAR
- Silhouette reads as distinct, hierarchical shapes before any detail is added.
- Every framed view along the walk has foreground / mid / background depth and a clear focal point.
- No visible texture repetition on any surface the player passes close to.
- No grid-obvious modular repeat that the eye can count.
- Every prop cluster answers *who is here and what do they do*; wear is where use is.
- Something worth reading sits at eye level on every walked route; sightlines terminate on something meaningful.
- Everything seated (geometry-truth verified), scaled consistently, placed from the content root.
- Dense areas and rest areas both present — neither noise nor void.
- Handed to `qa-visual` (multi-view) → `art-director` → `creative-review` (fresh). Never self-approved, never straight to the owner — "crude" excuses low fidelity, never unmotivated dressing (`guides/workflow.md`).

---

## COMMON FAILURE MODES
- **Evenly-spaced asset-flip.** Props on a regular pitch, uniform size, no story. The single loudest tell that no one lives here. Cluster with intent; vary size; motivate every placement.
- **Visible tiling.** A texture whose repeat the eye can count. Break it with macro/micro variation, blend masks, decals and dirt.
- **Grid-obvious modularity.** The same module read back to back. Break the grid with off-grid dressing, unique hero pieces, decals and silhouette breakers.
- **Clutter-as-noise.** So much unclustered detail the player can't read the space or the path. Cluster, establish hierarchy, protect negative space and navigability.
- **Scale inconsistency.** A prop that fights the established human scale — breaks belief instantly. Hold one reference throughout; enforce texel density.
- **Dressing with no story.** Props that decorate but don't answer *who/what*. Every object earns its place by implying occupancy.
- **Dead / empty OR over-stuffed.** A grey-box with textures (nothing at eye level, no human trace) or a hoarder's room (no negative space, no hierarchy). Both are unreadable; aim for composed density with rest.
- **Floating / clipped / trunk-buried props.** Seat failures the eye-level view hides. Verify true bases top-down with `GeometryAuditTools`. ⚠️ **`measure_true_base` is BLIND to rotation** — it computes the base from the mesh's *local* bounds transformed by scale and world-Z only, so a prop tipped on its side still reports `true_base = 0` and passes the floating check. A clean seating audit therefore does **not** prove props are upright — a tilted prop is a *rotation* defect the seating tool cannot see, and it only shows in a capture. Always eyeball orientation, never trust the seating audit alone for tilt.
- **Wonky rotation — the placement tell that reads as broken.** A prop's **yaw is never arbitrary**: square it to its aisle/wall/building, or angle it deliberately with a reason (a cart pulled askew to imply use). A stall skewed 20° for nothing, a food cart cross-wise blocking its own lane, a shelf off-parallel to the wall behind it — each reads instantly as "an object dropped by a machine," the loudest not-a-place tell after the asset-flip. Set an intentional rotation on **every** actor; never leave the placement default or a random spin. ⚠️ **When placing via Python, construct rotations with keyword args — `unreal.Rotator(pitch=..., yaw=..., roll=...)`.** The positional constructor order is `(roll, pitch, yaw)`, so `Rotator(0, yaw, 0)` silently sets *pitch*, tipping every prop and decal onto its face while the seating audit still reads clean (see above). This trap is what turned a whole dressing pass of intended yaws into a field of pitched-over props.
- **Props on top of each other / one-sided bunching.** `sweep_interpenetration` returning "0 intended" is NOT proof — an AABB category can hide real clipping. Prove it clean by eye on a **bright top-down + N/E/S/W obliques judged relative to the buildings** (the `qa-visual` placement audit). Distribute with intent across *both* sides of a street; do not pile the whole prop set against one wall and leave the other bare.
- **Overhead strings at chaotic diagonals.** Festoons / wires / bunting run **coherent lines** — along the street, or squared across it bay-to-bay — never a tangle of random diagonal spans. A criss-cross of angled strings reads as broken, not festive.
- **Fly-cam composition.** Dressed for an angle the player never stands at. Compose and judge the walked framings.

---

## CHECKLIST (before handing to `qa-visual`)
- [ ] Layout is **frozen, walked, approved** (refuse to dress otherwise).
- [ ] Silhouette reads first — distinct, hierarchical, against the backdrop.
- [ ] Every walked framing has fg/mg/bg depth and a focal point; focal points are framed and sightlines terminate meaningfully.
- [ ] Hero / mid / filler hierarchy in place; big/medium/small rhythm, not uniform.
- [ ] No visible tiling on any close surface (macro/micro + masks + decals applied).
- [ ] No countable modular repeat (grid broken with off-grid dressing / unique pieces / decals).
- [ ] Every prop cluster answers *who is here, what do they do*; wear matches use; decals carry environmental / text / narrative roles.
- [ ] Something at eye level on **every** walked route.
- [ ] Negative space preserved; navigability and readability intact.
- [ ] Scale consistent to one human reference; texel density enforced.
- [ ] Everything seated — `measure_true_base` + `sweep_interpenetration`, top-down checked; nothing floating / clipped / in trunks.
- [ ] **Every prop's rotation is intentional** — squared to aisle/wall/building or deliberately angled with a reason; no arbitrary/default yaw; nothing cross-wise blocking its own lane.
- [ ] **Placement proven clean on a bright top-down + N/E/S/W obliques judged relative to the buildings** — no props on top of each other, no one-sided bunching, overhead strings run coherent lines not random diagonals. (An AABB "0 intended" is not proof.)
- [ ] Placed only from `Content/ElseCity` (ingested), never a vendor path.
- [ ] Iterated with `lighting-artist` — composition and light authored together.
- [ ] Handed to `qa-visual` → `art-director` → `creative-review`. Not self-approved, not straight to owner.

---

## Sources
- [Environment Art — The Level Design Book][ldb] — readability, clustering, hero/mid/filler, iteration in context.
- [Balancing modularity and uniqueness — Beyond Extent][be] — breaking the grid, trim sheets, decals, shader/vertex variation, dirt masks.
- [Fix landscape tiling: macro/micro variation — World of Level Design][wold] — the multi-scale blend technique.
- [Tiling textures in game environments — 80.lv][80lv-tiling] — macro/micro detail, spec accents, master-material breakup.
- [SanXia Street: modular approach, trim sheets, decals — 80.lv][sanxia] — decal storytelling categories (environmental / text / narrative).
- [Environmental storytelling in video games — gamedesignskills][gds] — set dressing with purpose, wear patterns as guidance, clustering, believable clutter.
- [Composition in level design — Game Developer][gamedev-comp] — mass hierarchy, size and attention.
- [Effective composition in concept art environments — MAGES][mages] — framing, focal points, positive/negative space.
- [What is a focal point — StudioBinder][focal] — focal points and leading the eye.
- [Environment Artist Playbook: Blockout to Final Pass — RMCAD][rmcad] — six-stage workflow, silhouette-first, texel density, clutter control.

[ldb]: https://book.leveldesignbook.com/process/env-art
[be]: https://www.beyondextent.com/articles/balancing-modularity-and-uniqueness-in-environment-art
[wold]: https://www.worldofleveldesign.com/categories/ue4/landscape-macro-tiling-variation.php
[80lv-tiling]: https://80.lv/articles/tiling-textures-in-game-environments
[sanxia]: https://80.lv/articles/005cg-001agt-sanxia-street-1940-modular-approach-trim-sheets-decals
[gds]: https://gamedesignskills.com/game-design/environmental-storytelling/
[gamedev-comp]: https://www.gamedeveloper.com/design/composition-in-level-design
[mages]: https://mages.edu.sg/blog/effective-composition-in-concept-art-environments/
[focal]: https://www.studiobinder.com/blog/what-is-a-focal-point-definition/
[rmcad]: https://www.rmcad.edu/blog/environment-artist-playbook-from-blockout-to-final-pass/
