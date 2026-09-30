# Guide — Level Design method

> Read before defining or building any level or area. The core idea: **the level is built to match the spec, not the spec reverse-engineered from the level — and it is done only when it reads correctly from plan, elevation, AND eye-level, judged by a fresh reviewer.**

## The two failures this prevents
1. **The flat-card / single-angle trap.** A level that photographs well from one eye-level hero angle and falls apart from every other. Trial-1 built thin facade cards on misaligned masses and self-approved from one street shot; top-down and angled showed a colliding mess.
2. **No authority.** Building with no committed spec, so "wrong" is an opinion and there's nothing to hold the build to.

## PRINCIPLES
The craft rules that hold across every level and area. The stages tell you *when*; these tell you *what good looks like*.
- **Metrics first, always.** Geometry is built to the locked metrics sheet — never the sheet reverse-engineered from geometry. Scale is the one thing that breaks everything downstream and cannot be art-passed away.
- **The whole area before any part.** Block the entire space holistically before detailing a corner. A pretty corner on an unproven layout is wasted work — the layout is what you are testing.
- **Solid massing, never flat cards.** Volumetric primitives at metric scale. A facade is not a building; a walked space is not a photograph.
- **Walk it, don't fly it.** Every judgement about a space is made from the player's eye height, under gravity and collision. The fly-cam lies about scale, enclosure, and what the player can actually see.
- **Compose every sightline; never leave the eye unguided.** A player looks where the space tells them to. Decide what terminates each sightline and what draws the eye onward — or the player gets lost and the space reads as noise.
- **Pace the route, don't just lay out the rooms.** A level is experienced in time, as a sequence of tension and release — not surveyed as a plan. Rhythm is designed, not emergent.
- **Readable before beautiful.** The player must understand the space — where they are, where they can go, where the goal is — before art makes it gorgeous. Confusion is a layout defect, not a lighting one.
- **The spec is the authority.** Committed before the build, so a defect is "doesn't match the plan," not an opinion.

## Stages — gate to gate
0. **Intent & metrics.** Know what the player *does* here. Lock the **metrics sheet** (below). Optionally a throwaway metric-playground to walk-test scale first.
1. **Paper layout (2D, no engine).** Thumbnails → bubble diagram → top-down plan. Decide the street/space network here, not in 3D.
2. **Blockout (solid massing).** Build the plan as **solid volumetric geometry** at metric scale on a gridded ground — the *whole* area before detailing any part. Walk it with **full gravity + collision**, never fly-cam.
3. **Iterate to a layout freeze.** Expect to delete and rebuild — cheap now, expensive later. Freeze only when it reads and plays. After freeze, changing massing is expensive; art starts only here.
4. **Handoff.** The frozen blockout + the spec artifacts are the authority the art pass (`tech-artist`, `environment-artist`, `lighting-artist`) and QA are held to.

## The committed spec artifacts (this role's outputs)
Committed to the game repo's `plan/` alongside the phase file — so QA and `creative-review` check the build against them:
- **Metrics sheet** — the locked numbers (one page).
- **Top-down plan** — block/space footprints, path widths, node/landmark/door positions on a metric grid.
- **Straight-on elevations** — per key street/space face: heights, roofline rhythm, which frontage is the door/hero.
- **Hero views** — the 2–3 eye-level shots that define the target feel.

## Metrics sheet (UE = centimetres) — starting numbers, tune per game `[verify feel by walking]`
- **Grid:** blockout on a **100 uu (1 m)** grid; kits at 100 uu multiples; snap on.
- **Player:** capsule ~**60 × 176 cm**, **eye height ~152 cm** — build to eye height.
- **Wall** ≥ 20 cm thick, interior ≥ **300 cm** floor-to-ceiling. **Door** 110 × 220 cm. **Passage** ≥ **150 cm** (≥ 2× player width). **Stairs** 15 cm rise / 25 cm run.
- **Camera height + FOV locked early** — they set perceived scale for the whole world.

## Composition & wayfinding — reading the space, and guiding the eye
The player builds a mental map and navigates by what they can see. Two jobs: make the space **legible** (Lynch) and make the route **guided** (composition + wayfinding). Both are layout decisions, provable in the blockout, long before art.

**Legibility — Kevin Lynch's five elements, checked per view:**
Paths · Edges · Districts · Nodes · Landmarks. Each is checked in the view that reveals it: paths in plan + eye-level; **edges** (e.g. a safe→unsafe boundary) in plan + elevation, "visually unmistakable"; districts in plan + silhouette; nodes at eye-level ("does the player see a choice here?"); landmarks in silhouette + from every hero point ("we orient by them, we don't enter them").

**Guidance — composing the sightline.** A **sightline** is a line of open space that offers a view of somewhere else; the player uses it to decide where to go. The general composition theory these draw on — leading lines, framing, focal points, negative space — is owned by `guides/art-direction.md` (Composition & visual hierarchy); here it is applied to navigation. Author them deliberately:
- **Landmarks are beacons** (Disney's "wienies") — a tall, distinct, contrasting feature at the end of a sightline is an invitation to move toward it. In ElseCity the district landmarks double as the orientation system; place them so at least one is visible from every node.
- **Leading lines** — geometry that points: a colonnade, a rail, a kerb line, a run of lights, a change in floor material. They funnel the eye (and the feet) toward the goal without a marker.
- **Framing** — arches, gaps, windows and overhangs that bracket a view concentrate attention on what is inside the frame. A framed landmark reads as "go here".
- **Contrast draws the eye** — the player looks toward difference in colour, shape, light, and *movement*, and rarely looks up unless something pulls them. Blockout cannot light, but it *can* place the aperture, the height break, and the gap that a later light or motion will exploit — leave the composition ready for it.

**Signposting & affordance — telling the player what they can do.** A space must advertise its own navigability: a passage wide enough to read as "you can go through", a ledge that says "you can cross", a door that reads as a door. Match the **certainty** of the cue to how badly the player must not miss it — a subtle floor-material change is a hint (~20%); a framed, lit landmark is a strong pull (~60%); a funnelled chokepoint is near-compulsion (~90%); a wall is a hard no (~98%). Over-signposting a minor branch is as much a defect as under-signposting the critical path.

## Pacing & intensity — the rhythm of a walked route
A level is experienced *in time*. Lay out the rooms and you have a floor plan; sequence the tension and release and you have an *experience*. Pace it explicitly, on paper, before the blockout — the massing then serves the rhythm.

**Plot the intensity curve.** Time (minutes along the route) on X, intensity on Y (0–10). "Intensity" is the player's *stake / suspense / engagement*, not just difficulty. Rank the key beats and space them so the curve **rises overall, with alternating peaks and troughs** — never a flat line and never a permanent climb. Sustained high intensity past ~10 minutes exhausts; sustained low bores. Classic structure ends on *falling* action — the final beat is inevitable, not maximum-intensity.

**Design in beats.** A beat is a self-contained chunk of activity. Categorise them so the mix is deliberate:
- **Explore / rest** — low-intensity traversal, breathing room, orientation. Usually opens and closes a level.
- **Encounter** — the intensity peaks (combat in unsafe districts, a hazard, a time pressure).
- **Choreo / set-piece** — scripted or authored moments; a reveal, a vista, a transition.
- **Puzzle / choice** — spaces a decision out from the peaks.

Arrange them with **teach → test → twist** (introduce, confirm, complicate), and use **rest beats for contrast** — a sparse space makes the next dense one feel intense. **Negative space is a tool, not a gap to fill**: the lull before a reveal is what makes the reveal land.

**Pace the space, not just the events.** Enclosure is a pacing instrument: a tight corridor tightens, an opening-out releases. A **compression-then-release** (narrow passage → wide vista on a framed landmark) is the single most reliable pacing move in the blockout, and it is a *massing* decision you own. Alternate enclosure along the route to match the intensity curve.

**In ElseCity specifically:** Neon Hub is a rest/social register — low intensity, high legibility, safe. The unsafe districts carry the encounter peaks. The **door transition** (street hum → garden stillness) is a pacing beat in its own right — a hard release — and the compression/release of the threshold sells it.

## Encounter, cover & flow — where the space carries a challenge
Applies to any space built for confrontation or hazard — the unsafe districts, not Neon Hub. Skip for purely social/traversal space, but the *flow and readability* half applies everywhere.

**The encounter space (arena) reads on entry.** The player should grasp the scope and their options as they arrive — often via an **elevated entry vantage** that lays out the navigable space and the cover before they commit. A space whose shape cannot be read on entry produces flailing, not tactics. Obscuring *some* of it is fine; hiding *all* of it is a defect.

**Cover, to metric.** Standardise it so the player reads protection at a glance:
- **Full/tall cover ≥ ~175 cm** (blocks sight and line of fire), **low cover ~100–125 cm** (shoot-over), **under ~50 cm is not cover** — build cover to these bands so it reads unambiguously.
- Primary aspects: **height, width, solidity** (hard blocks sight/fire; soft only conceals), **facing** (directional cover creates flanks; freestanding exposes 360°). Sharp 90° corners protect; broken/cracked edges read as unclear and frustrate.
- **Less cover, placed well, beats more cover scattered.** Excess cover kills sightlines and wayfinding. Low cover generally out-performs tall — it preserves the read across the space.
- **Space cover to form a route.** Gaps wide enough to move and re-cover (≥ ~2 player-widths), positioned so there is a legible path *through* the encounter — for the player and for AI approach. Randomly scattered cover has no flow.

**Flow, chokepoints & flanking.** A **chokepoint** concentrates movement — powerful for pacing and tension, punishing if it is the *only* route (a dead-end funnel frustrates). Give an encounter space **more than one line** through it; a roughly circular arena offers options while keeping the player wary of flanks. Per the world rules, a **server/zone boundary goes at a chokepoint (metro, lift, tunnel, door), never mid-street** — so design chokepoints as deliberate transitions, not accidental pinch points.

**Readable navigation is universal.** Even with no combat, the player must always be able to answer "where can I go, and where is the goal?" from where they stand. Dead-ends that look like paths, branches that hide the critical route, and geometry too broken to read as walkable are flow defects wherever they appear.

## The multi-view verification battery (the "done" gate — run by `qa-visual`, a fresh pass)
Re-shot **identically** every pass so changes are comparable, not cherry-picked:
1. **Top-down (plan)** — matches the approved plan; footprints, widths, no unintended dead-ends; nothing overlapping/colliding.
2. **Straight-on elevation** (per face) — real depth and varied massing (not a flat wall of same-height boxes); everything **seated** (verify with reliable geometry measurements, backed by the human eye).
3. **Eye-level walk** — walked with gravity/collision; player fits doors/passages; sightlines terminate on something meaningful; ground-floor has eye-height detail; enclosure varies.
4. **Silhouette** — landmarks read as distinct black shapes against sky; hierarchy holds.

A single flattering angle is not QA. The builder never runs their own gate.

**Capture discipline (or the battery lies) — `[MEASURED: 2026-07-21]`, smoke test:**
- **Plan and elevation MUST be orthographic captures**, not a perspective camera pointed down/sideways. A perspective camera foreshortens, and foreshortening reads as *tilt and rotation that isn't there* — a fresh reviewer will (correctly, given the image) report walls "leaning" and a plinth "rotated" when the geometry is dead-on axis-aligned. False defects waste a verify cycle. Use an orthographic projection for views 1 & 2.
- **Set manual exposure + a fill/skylight before capturing.** Blown-white or crushed-black frames make base/corner **seating unverifiable** — the reviewer cannot confirm "nothing floating, no base gaps", which is half the point of the battery. Underexposed silhouettes and bloomed overviews both fail this.
- Corollary: pair the *human* elevation read with a *reliable geometry measurement* (editor dimensions/component measurements or a verified optional audit tool) — the measurement establishes seating beyond visual impression, the eye gives the composition the measurement cannot. Neither alone is the gate.
- **`CaptureTools.exposure_bias` is inverted — MORE NEGATIVE is BRIGHTER `[MEASURED: 2026-07-21]`.** This is the **capture tool's** convention and is the *opposite sign* of the register's post-process `ExposureCompensation` (positive = brighter, `guides/unreal-engine.md §5`) — don't conflate the two params. For this project's blockout, eye-level/hero perspective reads well at ≈ **-6.5**; orthographic elevations and the overhead plan need to go *further* negative (≈ **-8**) or they crush to near-black and seating is unverifiable. Sweep the bias per view rather than trusting one value across the battery.
- **The overhead top-down ortho is the weakest footprint check on a flat-roofed blockout `[MEASURED: 2026-07-21]`.** Looking straight down at equal-height flat roofs under a temp rig gives almost no edge contrast, so footprints and gaps barely read at any exposure. Read footprints/widths from the **iso** view + the **geometry-truth dump** (authoritative XY bounds), and use the top-down only as a coarse cross-check. A tight, target-framed top-down of a single sub-area (e.g. one courtyard) reads far better than the whole-level plan.

## QUALITY BAR
A blockout is ready to recommend for freeze when all of these hold — verified by a fresh pass (`qa-visual`), never self-signed:
- **Matches the committed spec** — footprints, widths, heights, and landmark/door positions match plan and elevations within grid tolerance.
- **Scale is right, walked.** Player fits every door and passage; ceilings, streets and vistas feel their intended size at eye height under gravity — not judged from the fly-cam.
- **Solid and seated.** Volumetric massing, nothing floating, no base gaps — confirmed by the reliable geometry measurement *and* the human eye, not by bounds.
- **Varied massing.** Real depth and height variation; not a flat wall of same-height boxes.
- **Legible.** The player can place themselves and read where to go from any node; landmarks visible where orientation is needed; edges unmistakable.
- **Composed.** Every major sightline terminates on something intended; the critical path is guided; branches signposted at the right certainty, neither over nor under.
- **Paced.** The route has a designed intensity rhythm — rest and peak, compression and release — not a flat line or a monotone corridor.
- **Flows.** No accidental dead-ends; encounter spaces read on entry and offer more than one line; chokepoints are deliberate.
- **Reads from every canonical view** — top-down, elevation, eye-level walk, and silhouette, re-shot identically.

## COMMON FAILURE MODES
The two structural failures the whole method exists to prevent (above), plus the craft failures a fresh review catches:
- **Flat-card / single-angle.** A space that photographs from one hero angle and collapses from every other. → solid massing; run the full multi-view battery.
- **No authority.** Building with no committed spec, so "wrong" is opinion. → spec committed before build.
- **Flat pacing / all-intensity-no-rest.** A monotone route — every space the same enclosure and stake, or wall-to-wall peaks with no breathing room. Exhausting or dull; either way unmemorable. → plot the intensity curve; design rest beats and compression/release.
- **No sightline composition / nothing to navigate by.** Sightlines terminate on nothing; no landmarks; the eye is never guided. The player wanders and the space reads as noise. → compose sightlines; place beacons; leave the frame ready for light.
- **Confusing flow.** The critical path is not signposted, or branches out-shout it; the player cannot tell where to go. → match cue certainty to importance; guide the critical path, subordinate the rest.
- **Dead-end frustration.** Paths that look navigable and are not; single-route funnels with no alternative; encounter spaces with one line through. → readable affordance; more than one line through anything tense.
- **Unreadable space.** Geometry too broken or too uniform to parse — cover you cannot read, arenas you cannot grasp on entry, walkable surfaces that do not look walkable. → readable primitives; grasp-on-entry; cover to metric bands.
- **Detailing before freeze.** Art-passing an unproven layout — the expensive way to learn the massing was wrong. → whole area, proven and frozen, *then* art.

## CHECKLIST
**Before building (spec):**
- [ ] Metrics sheet locked and committed.
- [ ] Top-down plan: path network, footprints, node/landmark/door positions on the metric grid.
- [ ] Straight-on elevations per key face: heights, roofline rhythm, hero/door frontage.
- [ ] Hero views defining target feel.
- [ ] Intensity curve plotted: beats ranked and spaced; rest and peak identified.
- [ ] Sightlines and landmark/beacon positions marked on the plan; critical path and its signposting decided.
- [ ] Plan approved by the Directors *before* any geometry.

**During the blockout:**
- [ ] Whole area blocked solid at metric scale on the grid, before any detailing.
- [ ] Walked at eye height under gravity + collision — fit, scale, enclosure.
- [ ] Enclosure alternates to match the intensity curve; at least one compression→release onto a framed landmark.
- [ ] Every major sightline terminates on something intended.
- [ ] Encounter spaces (where relevant) read on entry; cover to metric bands; ≥ one line through; chokepoints deliberate.
- [ ] Everything seated — reliable geometry measurement + eye.

**Before recommending freeze:**
- [ ] Quality bar met.
- [ ] Handed to `qa-visual` (multi-view battery) and `creative-review` (fresh review) — not self-run.
- [ ] Layout fixes applied and re-verified on the *saved* state.
- [ ] One-line freeze recommendation to Producer + Directors — never a self-freeze.

## Sources
Craft grounded in the standard level-design literature:
- **The Level Design Book** — *Pacing*, *Wayfinding*, *Composition*, *Cover*, *Encounter*, *Map balance* (`book.leveldesignbook.com`).
- **Pete Ellis**, *Single Player Level Design Pacing and Gameplay Beats* (World of Level Design).
- **Valve** beat categories — Explore / Combat / Choreo / Puzzle.
- **Fullbright**, *Basics of effective FPS encounter design* (F.E.A.R.).
- **Disney Imagineering** — the "wienie" (landmark-as-beacon).
