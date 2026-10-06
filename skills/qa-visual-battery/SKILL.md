---
name: qa-visual-battery
description: Run the fixed multi-view battery on a level — ortho plan + straight-on elevations + eye-level gravity-walk + silhouette, re-shot identically each pass — and report defects against the spec.
fires-when: After ANY change to geometry, materials, lighting, or placement, and always before calling level work done. Runs as a fresh pass, never the builder.
---

# qa-visual-battery

**Owner: `qa-visual`** (Verify & Judge). The battery definition lives in `guides/level-design.md`; the saved-lighting and structural-vs-visual split in `guides/workflow.md`; where this sits in the milestone loop in `guides/production-pipeline.md`. Capture via `CaptureTools` (`guides/tooling-ue.md`). Run cold — never the agent that built the level; a pass with zero findings is a suspicious result.

Doctrine this enforces: **multi-view or it isn't verified** (4), **build ≠ verify** (1), **the owner's eyes outrank the tool** (9).

## Procedure

1. **Check the level is viewable before visual QA.** Visual QA requires a **saved lighting rig in the level**. If the level is unlit, the verdict is "not ready for visual QA — needs a saved lighting register", not a pass and not a fail. A verdict never rests on transient/injected capture lighting — that renders black in a real viewport and nobody else can reproduce it.
2. **Structural checks are an earlier, separate gate** — footprints, seating, collision, walkability on the *unlit* level via geometry-truth tools (`GeometryAuditTools`) and a full-gravity walk. Don't fold them into the visual pass, and don't wait for lighting to run them.
3. **Shoot the fixed battery, re-shot identically each pass** so changes are comparable:
   - **Top-down plan** — orthographic.
   - **Straight-on elevation, one per face** — orthographic (a perspective camera makes foreshortening read as false tilt/rotation).
   - **Eye-level walk** — the human view, at metric eye height.
   - **Silhouette** — reads massing and shape.
   Set **manual exposure + fill** first, or base/corner seating is unverifiable. Record the resolved camera poses so the next pass re-shoots identically.
4. **Fly EVERY position.** Two flattering hero angles standing in for the battery is the exact failure this exists to prevent.
5. **Sweep for floating / interpenetrating geometry** with the geometry tools — do not trust `placed=N` or `get_actor_bounds` on packed/instanced actors; check true base *and* the human elevation view.
6. **Placement audit — the hard rule the AABB sweep alone does NOT satisfy.** An interpenetration sweep that returns pairs and then reasons them away as "intended slop" is the exact failure that shipped a market of stalls overlapping at wonky angles past a green check. So:
   - **Never interpret-away an overlap pair.** Every pair the sweep reports is a defect to *look at*, not dismiss — the burden is to prove it's clean by eye, not to explain it away by category. "Festoon over cart = vertical slop" is only acceptable after a capture confirms it reads clean.
   - **Capture at ALL angles, and judge every prop RELATIVE to the buildings and to each other** — not just the fixed night-hero poses (night + building occlusion *hide* placement mess; that is how this defect passed). Shoot a **high-exposure top-down over the building footprints** + **oblique 3/4 views from N/E/S/W** + an **iso** — a placement layer reads against the building masses this way. ⚠️ **Tool caveat:** `capture_view` renders through the level's committed (night) exposure and can't be fully flattened — a night-rig top-down leaves unlit zones dark, so **lean on the steep obliques + both-direction eye-level where props sit in lit zones**, and cross-check the dark top-down regions there. A true unlit/base-colour flat top-down is a known toolkit gap (`tools-programmer`); until it lands, the obliques are the primary instrument, not the top-down alone.
   - **Check ROTATION, not just position.** Every prop's yaw must be *intentional* — squared to its aisle/wall, or deliberately angled with reason. Arbitrary/random yaw (a stall skewed 20° for no reason, a cart cross-wise in the lane) is a defect. Bunching on one side, props clipping each other, and overhead strings (festoons/wires) strung at chaotic diagonals instead of coherent runs are all placement defects the top-down + obliques expose.
   - This audit is mandatory after ANY set-dress/placement change, and its output is prop-level: name the actor, the defect (overlap / bad-yaw / bunched / clips-building), and the angle it's seen from.
7. **Evaluate against the committed spec + the block checklist.** A defect is "doesn't match the spec," not an opinion. If the capture set can't answer an acceptance criterion, the verdict is "re-shoot", not a guess.
   - **For a set-dress / art pass, placement-clean is NOT a pass.** Hero props sitting on flat untextured ground with no ground grime/wear decals, no signage, no filler clutter, and countable tiling is a *blockout with props*, not a dressed space — fail it as "detail tier missing" (the `compose → layer → detail` bar; `environment-art.md`). The detail layer is a required deliverable, not polish.
   - **The honest whole-scene read — the top-line verdict, and the one that stops "done" theatre.** Before any per-view PASS, state plainly **what the scene actually IS** at true committed exposure, judged as a player sees it, not on a curve: *blockout · dressed-blockout · art-complete*. **Name the dominant surfaces** — the buildings/walls, the ground, the sky/backdrop — because they fill most of every frame and decide the read. **If a dominant surface is graybox/untextured/flat (e.g. blank building masses), the scene READS AS A BLOCKOUT — say so as the headline, even when that work is a known-deferred task.** "Deferred" is a valid *reason*, never an *exemption*: the verdict is "reads as blockout because the buildings are undesigned," not "PASS (buildings out of scope)." A pass that green-lights a scene whose dominant visual is blank is the exact failure this gate exists to prevent. Never grade a hero space "on-pitch / ready" while it reads as boxes; the owner's eye (doctrine 9) will call it, and the producer must LOOK at the actual multi-angle capture before relaying any "done."
8. **Report a defect list** — each with the viewpoint it was seen from and a severity. Rendering-only: this proves it *renders* right, not that a player can *walk* it (that's `qa-network`/PIE).
9. **The owner's eyes outrank the query.** If the owner sees a defect a check missed, the check is wrong — audit what it measures; never re-assert the green.

## Capture contract — any before/after or A/B capture

Every comparison capture (visual QA, `realism-judge`, `perf-gate` cost runs, a look trial) obeys this, whatever tool shoots it:

1. **Fix the comparison before the run** — the same framing (camera pose, field of view, viewport size), the same seed and sim time, the same exposure (manual/fixed), the same light. A pair that differs in any of these compares the setup, not the change.
2. **One variable per run.** A run that changes two things answers neither.
3. **Measure the noise floor in the same session** — capture the baseline, then repeat it unchanged; the baseline-vs-repeat difference is the floor a candidate must beat. Never compare against a number or frame from another session, and re-measure the floor after any restart or crash.
4. **Read back every override and restore it.** Record the baseline of anything global the run changes (console variables, show flags, project settings), read back each applied value into the run's record, restore after, and read the restore back. Global overrides outlive the play session.
5. **Validity readbacks make a run invalid, not a result.** The run records proof it measured what it meant to — the live build matches source, the intended settings are in effect, the real render size, that the subject actually drew, no debug mode left on. A run failing any of them is discarded and re-run, never scored.
6. **One log line per finished run** (name, the variable, key metrics, note), appended as it goes (`team-execute` step 3).
7. **Check derived review images.** A zoomed crop must really be zoomed (output size = input region × scale), and paired images share height and exposure handling; a broken crop tool silently makes the judge grade the full frame.

Metrics from a capture flag defects; they never pass a look — the fresh judges do.
