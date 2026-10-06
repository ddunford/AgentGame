---
name: realism-judge
description: Judge whether renders could pass for real photographs — a blind comparison against a reference-photo set matched to each capture's framing, with named give-aways scored 0–3 and a ranked list of what betrays the render. The photographic-realism gate for any look that targets reality. Always a fresh reviewer, never the builder.
fires-when: At the end of any look phase on a realism-targeted surface (sky, weather, terrain, materials, lighting), before anyone tells the owner a look is "more real" or "better", and whenever a worker or judge claims a visual pass. Skip for stylised targets — `creative-review` judges those against the look-bible.
---

# realism-judge

**Owner: `creative-review`** (Verify & Judge — judges, does not build), run alongside the other gates, never instead of them: `qa-visual-battery` asks *is it broken from every view*, `creative-review` asks *is it on pitch*, this asks *could it pass for a photograph taken from the same spot*. Captures come from the capture contract in `qa-visual-battery`; cost claims go through `perf-gate`, engine assumptions through `verify-engine-claim`. The reference set's sourcing and licence follow `ingest-asset` (references are judging material only, never shipped).

Doctrine this enforces: **build ≠ verify** (1) — the judge never built the change and is not told what changed; **the owner's eyes outrank the tool** (9) — when the owner says it looks fake, it is fake, and the job is to find out why from the references.

**The bar is photographic.** "Looks nice", "better than before" and "reads as the right kind of thing" are not passes. A pass means the judge cannot reliably tell the render from the matched photos, or every gap is named and ranked.

## Inputs
- **Captures** from the capture contract (`qa-visual-battery`): the player view at fixed exposure, fixed framing and seed. Study views and paused stills are labelled as such.
- **A reference-photo set** with an index (subject, light direction/elevation, distance, camera height, source, licence). Art and concept images are targets, not truth; where they disagree with photographs on physics, the photographs win. A missing reference type is a recorded gap — acquire it with the owner's approval rather than judging without it.

## Procedure

1. **Judge like with like — match before comparing.** For each capture, choose 2–3 references with the same subject, viewing distance, angle, camera height, light direction and the same way the subject shades the scene. A mismatched framing can fail every candidate whatever its quality. If nothing matches, say so and re-shoot or source references — never score a mismatch.
2. **Check the inputs are what they claim** — the capture contract's crop check (`qa-visual-battery`), images at the same height, and no names or captions that reveal which is which.
3. **Build a shuffled blind set.** Mix the candidate render(s) with the matched photos **and** the controls — the current baseline render and, where useful, a known-bad render — under neutral names, with the key kept by the producer, not the judge. Controls show whether the judge can tell renders apart at all and whether the candidate moved.
4. **Measure what can be measured, on render and references alike** — e.g. lit-face vs adjacent-background luminance ratio, shadow vs lit ratio, darkest region vs background, horizon vs higher-sky brightness, white balance of lit and shaded faces, edge width at matched angular size, saturation, coverage. Report the render against the reference **range** (min–max over the matched photos); a value outside the range is a named gap.
4b. **Judge motion with a time-lapse whenever the subject evolves or moves** (weather, water, fire, foliage, crowds,
   growth). Stills never prove motion. Render the candidate's whole life from a fixed tripod view, at a stated time
   compression, with lighting that changes as it really would over that span (no staged light), and encode it as a
   video plus a 6–12 frame contact sheet. Then:
   - **Measure before looking.** Set the pop threshold first (e.g. no single-frame change in the subject region larger
     than 3× the median frame-to-frame change); report every frame that exceeds it, and any flicker from sampling noise
     or exposure pumping.
   - **Compare against real time-lapse or footage** matched in subject, distance and time compression. Where speeds can
     be measured (growth, rise, spread, drift), check them against real measured ranges, not against how it feels.
   - **Ask the judge** whether the motion reads as real at this compression, and to name motion give-aways (rubric:
     *Motion*).
   - A video labelled for the public states that it is an engine time-lapse and its compression; it is not presented as
     real-time gameplay.
5. **Run the fresh judge.** A new agent/context or person that did not build the change, given only the blind set, the matched-reference rationale and this rubric. Ask:
   - "Which of these are photographs and which are renders, and why?"
   - "Could this pass for a photo taken from the same spot?"
   - "List every cue that gives a render away", then score each give-away **0–3** (0 = obviously CG, 3 = indistinguishable) and **rank** the images from most to least photographic.
6. **Render the verdict.** **PASS** only if the judge cannot reliably pick the candidate out of the photos and every measured value sits in the reference range. Otherwise **FAIL** with the ranked give-away list — that list is the next iteration's input. A candidate ranked below its own baseline is a regression whatever its other merits.

## Give-away rubric (the project fills in its subject's specifics)
- **Shape:** uniform sizes, repeated or symmetric forms, missing multi-scale detail, wrong silhouette for the subject.
- **Edges:** fur, grain, aliasing, over-soft or over-hard rims compared with the matched photos.
- **Light:** flat shading, missing lit/shaded contrast, missing back-light effects, wrong colour of lit or shadowed faces, missing bounce from surroundings.
- **Atmosphere:** no aerial perspective with distance, no haze gradient, wrong horizon brightness for the light.
- **Scale:** no distance cues, wrong proportions between parts, the subject not dwarfing what it should.
- **Camera:** an exposure no real camera would pick, no highlight roll-off, bloom/flare the photos lack, a "CG-clean" surface.
- **Motion** (when judged in motion): speeds outside real time-lapse or footage; popping or sudden jumps between
  frames; texture swimming or sliding over a form instead of the form itself changing; everything moving at one
  uniform rate; the whole subject changing at once instead of parts evolving in their own time; no internal churn
  where the real thing boils or rolls; flicker from sampling noise or exposure.

## Report
Per judged set: the sheet path, the matched references and why each matches, the blind key (revealed after judging), the measured table (render vs reference range), the judge's give-away list with 0–3 scores and ranking, the verdict, and what was not judged. Record a FAIL as a FAIL in the task tracker and any progress diary. Never state or imply realism to the owner without a sheet and a fresh verdict behind it.

## Block these
- Comparing a near render with a distant photo, or a front-lit render with a back-lit photo.
- A judge who built the change, or who was told what changed or what is hoped.
- A pass declared from metrics alone — metrics flag gaps, they never pass a look.
- Shipping or depending on a reference photo.
