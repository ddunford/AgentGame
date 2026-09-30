# Guide — Character Art method

> Read before designing, modelling, or ingesting any character. The core idea: **a character is not a prop with a face — it is a shape that must read at a glance, deform without breaking, and rig onto a skeleton the animation and gameplay chain already expects.** Appeal is authored, deformation is engineered, and the skeleton is a contract. A mesh that looks right in a T-pose and folds into spaghetti at the elbow has failed; so has a beautiful one that lands on the wrong skeleton and cannot be animated.

The `character-artist` agent carries the short rules; this is the depth behind them. It is the **head of the character chain** — its output is the thing everything downstream deforms, rigs, animates, and drives. It sits under `guides/art-direction.md` (which owns the world's shape language, palette, and the on-style rubric this must satisfy) and hands off to `guides/animation.md`. It does **not** re-own asset ingest, collision, or budget *enforcement* — those live with `tech-artist` / the ingest flow (`AGENTS.md` §Assets); this guide owns the character-specific craft that must be right *before* ingest can pass.

## The pipeline this heads

```
character design → model → rig → animation → gameplay
   (this guide)  (this guide)  │      │           │
                               └ guides/animation.md ┘   (rig + anim)
                                                     └ gameplay-engineer (state machines, IK, feel)
```

- **character design → model:** the design (silhouette, shape language, proportion, palette) is locked and reviewed *before* a single vert is pushed — the model is built to the design, never the design reverse-engineered from a model. Same rule as `level-design.md`'s metrics-first.
- **model → rig:** this guide delivers a mesh that is **rig-ready** — clean deformation topology, sensible edge loops at every joint, a pose that matches the target skeleton, and correct real-world scale. The rig (`guides/animation.md`) is only as good as the loops it deforms.
- **rig → animation → gameplay:** downstream owners. This guide's job is to hand them something that will not fight them.

**The skeleton is the contract that binds the whole chain.** ElseCity's animation stock — the crowd/emote channel — is retargeted onto the **project skeleton** `/Game/Characters/Mannequins/Meshes/SK_Mannequin` (the UE5 Manny hierarchy; see `Content/ElseCity/Animations/Emotes/EMOTE_PROVENANCE.md`). A character that does not skin to that skeleton (or a rig that retargets cleanly onto it) cannot use any of that motion. Choosing or building a character therefore starts from the skeleton, not the look.

## The failures this prevents

1. **Off-model.** The character drifts from its locked design — proportion, silhouette, shape language, or palette no longer matches the callout sheet or the world's on-style rubric (`guides/art-direction.md`). A face that is "close" is off-model; players read character silhouettes more sharply than any prop.
2. **Topology that deforms badly.** Geometry that looks fine static and collapses, pinches, or candy-wraps when posed — too few loops at a joint, edge flow that fights the bend, triangles in a deforming area. This is invisible in the modelling viewport and glaring the instant the rig moves it, which is why it is caught here, not in animation.
3. **Over-budget.** Polycount, material/draw-call count, texture resolution, or bone count past the character's budget class — a hero-density mesh used as a crowd extra tanks a scene of them. Budget *enforcement* is `tech-artist`'s gate; hitting the budget is authored here.
4. **Wrong / incompatible skeleton.** A mesh skinned to a bespoke or vendor skeleton that the project's animation stock cannot retarget onto — it looks done and can never move.
5. **Scale drift.** A character authored at the wrong real-world size. Everything downstream — capsule, eye height, camera, IK, prop attachment, the whole `level-design.md` metrics sheet — is calibrated to a ~176 cm figure; a character built at the wrong scale breaks all of it and cannot be art-passed back.

---

## PRINCIPLES

### 1. Appeal, silhouette, shape language — design before model
Character *design* is the load-bearing pass; modelling executes it. The compositional theory — shape language, silhouette reading, palette ratio — is owned by `guides/art-direction.md`; this is its **application to a figure**.

- **Silhouette first, read at a glance.** The character must be recognisable as a flat black shape before any surface detail — the same flat-black test `art-direction.md` applies to a frame. If two characters share a silhouette, one of them is not designed yet. Distinct silhouette carries identity at distance, in a crowd, and in gameplay reads.
- **Shape language communicates.** Round/soft reads friendly and safe; sharp/angular reads unstable or threatening ([RocketBrush character-style guide][rb]). Every character's dominant shapes must say what the design intends and stay inside the world's vocabulary — a character whose shapes contradict its role is off-style however well made.
- **Proportion is a locked decision, not a slider.** Head-count height, limb ratios, hands and feet sizing — decided at design, held through the model. Proportion drift is the most common off-model failure and the hardest to see from inside the work.
- **Palette holds the bible's ratio.** Skin, hair, clothing and accent colours sit inside the look-bible's swatches and the 60/30/10 discipline (`art-direction.md` §Color); chroma is reserved for the focal read (face, a signature accent), not sprayed across every panel.
- **Design as a committed artifact.** A front/side/back orthographic + a callout sheet annotating *why* each form is what it is (proportion, material, shape intent) exists and is reviewed before the model — doctrine 2, the same design packet `art-direction.md` requires.

### 2. Topology & edge flow — model for deformation
The model exists to be deformed. Every topology choice is judged by how it bends, not how it looks at rest.

- **Edge loops follow the forms that move.** Concentric loops around every deforming joint — elbow, knee, shoulder, hip, wrist, the mouth and eyes — so the surface has the geometry to bend without pinching. A joint with too few loops candy-wraps; the loops are what let the skin rotate. `[verify — web pass]` for a per-joint loop-count starting table.
- **Edge flow follows anatomy and muscle direction.** Flow that follows the underlying forms deforms naturally; flow that cuts across them creates shading and pinching artefacts under motion. Faces especially: loops around the eyes and mouth (the two spheres and the sphincter) are non-negotiable for expression.
- **Quads in deforming areas; triangles only where nothing bends.** Deforming surfaces stay quad-dominant so subdivision and skinning behave predictably; triangles and n-gons are tolerable only in rigid, hidden, or non-deforming regions.
- **Even, purposeful density where it bends; economy where it doesn't.** Spend polys on the faces, hands, and joints that carry the read and the deformation; strip them from flat, rigid, or unseen areas. Density is a deformation and budget decision at once.
- **Symmetry until it shouldn't be.** Model symmetric, break symmetry only for deliberate design or asymmetric detail — and know that a symmetric mesh often shares one UV half, which is a texture-budget win.

### 3. UVs & texel density
- **Lay out for the read and the budget.** Maximise used UV space, minimise seams, and hide the seams you must have where they won't be seen (inside limbs, under hair, behind straps). The face gets the most texel space because it carries identity and takes the closest camera.
- **Consistent texel density.** One density target across the character (raised on the face) so no region reads softer or sharper than its neighbours — enforce against a reference grid, the same discipline `environment-art.md` applies to surfaces. `[verify — web pass]` for the project's texels-per-cm target by budget class.
- **Overlap and mirror to save budget** where symmetric, but keep unique space for anything that must differ left/right (a logo, a wound, asymmetric wear).
- **UDIMs / multiple sets only when the budget class justifies it** — a hero head may warrant its own set; a crowd extra shares one.

### 4. PBR texturing
- **Author to the metallic/roughness PBR standard** the project uses, with the full map set the material expects (base colour, normal, roughness, metallic/specular, AO; plus masks for skin, hair, cloth as needed). Skin wants subsurface treatment; do not paint lighting into base colour.
- **Materials as instances off a shared master.** A character master material with per-instance parameters (tint, wear, roughness scale) so variants are data, not new materials — the same instance discipline `tech-artist` owns for the pipeline, and it keeps draw calls in budget.
- **Detail where the camera goes.** Micro-normal and pore/fabric detail on the face and hero surfaces; broad treatment on filler. Match `environment-art.md`'s macro/micro logic so a character doesn't read at a different fidelity than its world.

### 5. LODs
- **Every character ships a LOD chain sized to how it's seen.** A hero seen close needs more LODs and a higher LOD0; a crowd extra can start lower and drop fast. Reduction preserves silhouette and the deforming loops longest — never decimate away the loops a distant-but-still-animating mesh still needs.
- **Bone LODs too.** Distant characters can drop fingers and minor bones from the skinning; this is a real cost saving on a crowded scene and is set per-LOD. `[verify — web pass]` for the project's LOD screen-size and reduction-percentage starting values.
- **Budget class decides the whole chain.** Hero / NPC / crowd-extra are different budget classes with different poly, texture, material, and bone ceilings — `tech-artist` owns the numbers and the enforcement gate; this guide authors to them.

### 6. Skeleton & rig-readiness — the contract
- **Target the project skeleton from the start.** The character is built, proportioned, and posed to skin onto `/Game/Characters/Mannequins/Meshes/SK_Mannequin` (UE5 Manny), or onto a rig that retargets cleanly onto it — because that is what the animation stock (`guides/animation.md`, the emote channel) is built on. Skeleton choice is the *first* decision, not a late one.
- **Bind pose matches the target.** Model in the pose the target skeleton expects (A-pose vs T-pose — match Manny). A mismatched bind pose is a retarget headache the rigger inherits.
- **Clean skin weights are a handoff deliverable, not the rigger's problem to discover.** Where this guide's owner also does the initial skin, weights are smooth across every joint with no stray influences; where the rig is downstream, the topology is delivered *ready* to weight.
- **Real-world scale, locked.** ~176 cm reference figure (`level-design.md` metrics), correct up-axis and forward, pivot at the feet. Scale is verified with geometry-truth tools at ingest — async/imported meshes report fake bounds (`tech-artist`), so scale is *measured*, never trusted from the import dialog.

### 7. MetaHuman & the acquisition route — buy before you build
- **Buy → generate → author, same as every asset.** The fastest route to a rig-ready, LOD'd, skeleton-compatible human is usually **MetaHuman** or a **Fab/Megascans** character, not a from-scratch sculpt. MetaHuman ships appeal, topology, UVs, LODs, and a standard skeleton already solved — the design work becomes *selection and customisation* against the look-bible, not raw modelling. `[verify — web pass]` for MetaHuman's current skeleton compatibility with the project Manny retarget path and its LOD/bone-count profile.
- **Acquisition is the ingest flow's job, not this guide's.** Fab/Megascans/MetaHuman acquisition, curation into `Content/ElseCity`, collision, budget class, and provenance are owned by `tech-artist` / `ingest-asset` (`AGENTS.md` §Assets) — do not duplicate that mechanism here. This guide decides *what character* and *whether it's on-model and rig-ready*; the ingest flow makes it run and pipeline cleanly.
- **A bought character still faces the on-style rubric.** MetaHuman-default or a Fab human is a starting point, not a pass — it goes to `art-director` / `creative-review` against the world's shape language and palette like anything else.

### 8. Hair & cloth (basic)
- **Groom or cards to the budget class.** Strand-based groom for hero, hair cards for the rest; either way it reads as the world's stylisation level, not a fidelity outlier. `[verify — web pass]` for the project's hero-vs-crowd hair approach and cost.
- **Cloth is skinned first, simulated only where it earns it.** Most garments are skinned to the skeleton and deform with it; runtime cloth sim is reserved for a hero silhouette element where the movement is worth the cost, and its cost is named. A cloth sim that self-intersects or jitters is a defect, not polish.
- **Everything downstream still has to move it.** Hair and cloth that read fine static but pop, clip, or lag under the locomotion set are `guides/animation.md`'s problem to catch — author them so they don't create it.

---

## QUALITY BAR
A character is ready to recommend when all of these hold — judged by a fresh pass (`art-director` on the look, `creative-review` for on-pitch), never self-signed:
- **On-model.** Silhouette, proportion, shape language, and palette match the locked design and the world's on-style rubric; recognisable as a flat black shape.
- **Deforms cleanly.** Edge loops at every joint; quad-dominant deforming surfaces; face loops around eyes and mouth; no pinching, candy-wrapping, or shading artefacts when posed.
- **On budget.** Poly, texture, material/draw-call, and bone counts inside the character's budget class; a LOD chain sized to how it's seen, preserving silhouette and deforming loops longest.
- **UVs sound.** Efficient layout, hidden seams, consistent texel density (raised on the face), symmetric overlap where it saves budget without breaking unique detail.
- **Textured to standard.** Full PBR map set to the project standard; material as an instance off the shared master; no lighting baked into base colour.
- **Rig-ready on the right skeleton.** Skins onto (or retargets cleanly onto) the project Manny skeleton; bind pose matches; scale locked to the ~176 cm reference, pivot at feet, verified with geometry-truth tools.
- **Ingested cleanly.** Curated into `Content/ElseCity` with collision, budget class, and provenance via the ingest flow — never referenced from a vendor path.
- **Judged fresh.** `art-director` (look) + `creative-review` (on-pitch); never straight to the owner — "crude" excuses low fidelity, never off-model or bad-deforming topology.

---

## COMMON FAILURE MODES
- **Off-model.** Proportion/silhouette/shape/palette drift from the locked design. → Design as a committed orthographic + callout sheet first; review against it and the on-style rubric before modelling proceeds.
- **Topology that deforms badly.** Too few loops at a joint, edge flow across the bend, tris/n-gons in a deforming area — invisible static, glaring in motion. → Loops around every joint; quad-dominant deforming surfaces; flow follows anatomy; verify by *posing*, not by looking at the rest mesh.
- **Over-budget.** Hero density on a crowd extra; too many materials/draw calls; texture too large; too many bones. → Author to the budget class; LOD chain and bone LODs sized to how it's seen; `tech-artist` enforces the ceiling.
- **Wrong / incompatible skeleton.** Skinned to a bespoke or vendor skeleton the animation stock can't retarget onto — looks done, cannot move. → Target the project Manny skeleton from the first decision; match its bind pose.
- **Scale drift.** Built at the wrong real-world size; breaks capsule, camera, IK, prop attachment, the whole metrics sheet. → ~176 cm reference, correct axes, pivot at feet, *measured* at ingest with geometry-truth tools (import bounds lie).
- **Seams / texel inconsistency.** Visible UV seams in view; one region softer/sharper than its neighbours. → Hide seams where unseen; hold one texel-density target (raised on the face) against a reference grid.
- **Built-from-scratch when a bought base would do.** Weeks sculpting what MetaHuman/Fab ships rig-ready and LOD'd. → Buy → generate → author; reserve from-scratch for what the catalogue can't give.
- **Cloth/hair that breaks in motion.** Reads fine static, clips/pops/lags under locomotion. → Skin first, sim only where it earns it and name the cost; hand off knowing `animation.md` will catch what moves wrong.

---

## CHECKLIST
**Design (before modelling):**
- [ ] Front/side/back orthographic + callout sheet exists, annotating proportion / material / shape intent (doctrine 2).
- [ ] Silhouette reads as a distinct flat-black shape; shape language matches the world's vocabulary and the character's role.
- [ ] Palette sits inside the look-bible swatches and the 60/30/10 ratio; chroma reserved for the focal read.
- [ ] **Target skeleton chosen** (project Manny, or a clean-retarget rig) — the first decision, not the last.
- [ ] Buy/generate/author decision made — is MetaHuman/Fab the base, or is scratch justified?
- [ ] Reviewed against the design and on-style rubric (`art-director`) before a vert is pushed.

**Model & texture:**
- [ ] Edge loops around every deforming joint; face loops around eyes and mouth; quad-dominant deforming surfaces; tris only where nothing bends.
- [ ] Edge flow follows anatomy; density on faces/hands/joints, economy on rigid/unseen areas.
- [ ] UVs efficient, seams hidden, texel density consistent (raised on the face), symmetric overlap where it saves budget.
- [ ] Full PBR map set to project standard; material is an instance off the shared master; no baked lighting in base colour.
- [ ] LOD chain sized to budget class; silhouette and deforming loops preserved longest; bone LODs set.
- [ ] Hair/cloth to budget class (groom/cards; skin-first, sim only where earned and costed).

**Rig-readiness & ingest:**
- [ ] Skins onto / retargets cleanly onto the project Manny skeleton; bind pose matches.
- [ ] Skin weights smooth at every joint, no stray influences (where skinned here).
- [ ] Real-world scale ~176 cm, correct up/forward axes, pivot at feet — **measured** with geometry-truth tools, not trusted from import.
- [ ] Ingested into `Content/ElseCity` with collision, budget class, provenance via `tech-artist` / `ingest-asset`; no vendor-path references.

**Before recommending:**
- [ ] Quality bar met; posed-and-checked, not rest-mesh-checked.
- [ ] Handed to `art-director` (look) + `creative-review` (on-pitch), fresh, never self-approved, never straight to the owner.
- [ ] Handed to the rig/animation chain (`guides/animation.md`) with the skeleton and scale confirmed.

---

## Sources
Craft grounded in the standard character-art references; specific numeric targets (loop counts per joint, texel density, LOD screen-sizes/reductions, MetaHuman skeleton/bone profiles, hair approach) are marked `[verify — web pass]` above and resolved in the researched pass.
- [The Ultimate Character Art Style Guide — RocketBrush][rb] — shape language and appeal, character stylisation. `[verify — web pass]`
- Standard deformation-topology practice (edge loops at joints, quad-dominant deforming surfaces, face loops around eyes/mouth) — to be cited in the web pass. `[verify — web pass]`
- Epic **MetaHuman** documentation — skeleton compatibility, LOD/bone profile, customisation route. `[verify — web pass]`
- Cross-references (not duplicated here): `guides/art-direction.md` (shape language, palette, silhouette, on-style rubric), `guides/animation.md` (rig/retarget/deform-in-motion), `guides/level-design.md` (the ~176 cm metrics), `AGENTS.md` §Assets + `tech-artist` (acquisition, collision, budget enforcement, provenance), `guides/unreal-engine.md` (engine facts).

[rb]: https://rocketbrush.com/blog/the-ultimate-character-art-style-guide-for-artists-and-developers
