---
name: realistic-weather-rendering
description: Diagnose UE5 cloud and tornado realism by separating shape, sampling, lighting and compositing; design seeded weather against real-weather cues.
fires-when: Procedural clouds look spherical or flat, tornadoes look solid, or a weather generator needs renderer-versus-shape bounds and a photographic judging rubric.
---

# Realistic weather rendering

**Owner: `tech-artist`; reviewers: `lighting-artist`, `realism-judge`, `performance-engineer`.**
Generate varied weather from options, seed and simulation time. Expose tunable ranges and units; preserve
deterministic seeking. Do not substitute a fixed scene for a weather system. Use
[ue-sky-atmosphere-colour](../ue-sky-atmosphere-colour/SKILL.md) for atmosphere and exposure diagnosis.

Evidence labels matter: **Verified** below means UE 5.8 source or cited research checked on 2026-10-08/11,
not a live visual or cost pass. **Inferred** means a working interpretation. **Untested** means a proposed
experiment. Recheck engine paths on other versions. Keep project captures, hashes, runtime readbacks and
research records in the project's companion skill; this generic method carries no project assets.

## Verified: stock cloud rendering constraints

Paths below are relative to `Engine/`. Shader paths begin `Shaders/Private/`; renderer paths begin
`Source/Runtime/Renderer/Private/`.

- Cloud view steps are uniform: approximately `step = max(L,D)/Nmax`, with the minimum-count clamp for very
  short rays. `L` is the in-layer traced path, `D=r.VolumetricCloud.DistanceToSampleMaxCount` defaults to 15 km,
  and `Nmax=clamp(96*ViewSampleCountScale,2,768)` at default caps. Opaque depth and tracing distance limit L;
  distance from the camera alone does not determine the step. There is no refine-on-hit or SDF adaptivity.
  Zero-conservative-density skipping only enlarges empty steps. Sources: `VolumetricCloud.usf:709-718,797-866`;
  `VolumetricCloudRendering.cpp:52-80,1773-1776`.
- Thus minimum step is 19.5 m at N768, or 65 m for a 50 km traced path. **Inferred band-limit rule:** require
  several steps across a visible feature (roughly 4-8 for billow structure); fewer than two samples flicker
  under jitter. Do not add sub-step tufts and expect detail. Use meshes or independently sampled volumes for
  thin funnels/near detail, or demonstrate a viable shorter path/higher sample budget. A cloud cannot draw
  below its layer. Lowering the layer to ground adds ground-pixel marches and changes altitude-based lighting.
- Mode 0 traces quarter resolution and reconstructs at half resolution over time
  (`VolumetricRenderTarget.cpp:33-34`). Assess motion and ghosting, not just paused silhouettes.
- Multiple scattering uses up to two extra Wrenninge-style octaves: scattering scales by Contribution^i,
  shadow optical depth by Occlusion^i, and phase approaches isotropic via Eccentricity^i
  (`VolumetricCloud.usf:341-428,1076`). One extra octave is Epic's game recommendation.
  **Inferred:** Contribution 1 / Occlusion 0.08 / Eccentricity 0.2 can fill creases with nearly unshadowed,
  isotropic energy; flat lighting is a hypothesis until the T1 bound, not proof of a bad integrator.
- Sky ambient uses the atmosphere's distant-sky LUT when SkyAtmosphere exists, not SkyLight intensity.
  Material AO scales sky ambient only, not sunlight octaves or ground bounce
  (`VolumetricCloud.usf:722-739,943-954`). Keep these lighting families separate.
- The stock cloud integrator has Beer attenuation, dual-lobe HG and MS octaves, but no powder/dark-edge term
  (`VolumetricCloud*.usf`, `ParticipatingMediaCommon.ush`). Material extinction/albedo shaping is an
  **untested approximation**, not an engine powder switch. Shadow rays also have a finite budget: base 10
  samples times ShadowViewSampleCountScale, cap 80, quadratically distributed along ShadowTracingDistance
  (`VolumetricCloudRendering.cpp:1774-1775`; `VolumetricCloud.usf:1094-1099`).

Reference: [Epic Volumetric Cloud](https://dev.epicgames.com/documentation/en-us/unreal-engine/volumetric-cloud-component-in-unreal-engine).

## Verified: choose compositing deliberately

- Ordinary translucent meshes draw after cloud compositing. Sort priority orders translucent primitives,
  not cloud depth. Apply Cloud Fogging requires Apply Fogging and overlays the cloud column when the mesh
  is beyond the cloud's transmittance-weighted mean depth, with a default 0.5 km blending ramp. It cannot
  represent a mesh partly inside the volume. Source: `BasePassPixelShader.usf:1594-1604`,
  `VolumetricCloudCommon.ush:91-112`, `TranslucentRendering.cpp:1238-1270`.
- HeterogeneousVolume (HV) composites `HVRadiance + SceneColor*HVTransmittance` after the cloud, without
  cloud depth. **It always draws over the cloud**, including a funnel geometrically behind its base.
  Cloud and HV have no mutual shadowing on this path. Do not generalise this to every separate rain mesh;
  test its translucency ordering. Source: `DeferredShadingRenderer.cpp:3666-3958,4181-4184`;
  `HeterogeneousVolumes/HeterogeneousVolumesComposite.usf:213`.
- `r.HeterogeneousVolumes.MaxTraceDistance` defaults to 30000 cm (**300 m**); raise and read it back for
  kilometre-range tests. HV sampling uses its own voxel scale times StepFactor, independent of the cloud march.
  `r.HeterogeneousVolumes.Preshading` defaults to 0; the live pipeline calls `CalcPixelMaterialInputs` per sample,
  so procedural material evaluation is supported. **Inferred:** analytic density driven by explicit simulation
  time can be seek-exact; verify this live. Source: `HeterogeneousVolumes/HeterogeneousVolumes.cpp:172-190`;
  `HeterogeneousVolumesLiveShadingPipeline.usf:281-283,673-675`.
- HV is a runtime feature, subject to SM5/deferred/scalability gates. UE 5.8 settings label it Beta, while
  [Epic's documentation](https://dev.epicgames.com/documentation/en-us/unreal-engine/heterogeneous-volumes-in-unreal-engine)
  calls it Experimental. Its dense lighting cache and voxel/step budgets require measurement, not assumed savings.

## Verified references; inferred generator method

[Nubis 2015](https://www.advances.realtimerendering.com/s2015/The%20Real-time%20Volumetric%20Cloudscapes%20of%20Horizon%20-%20Zero%20Dawn%20-%20ARTR.pdf)
uses a Perlin-Worley base, Worley erosion, curl distortion, cloud-type height profiles, weather-map coverage,
wind advection and view-dependent powder lighting. [Nubis cubed](https://www.guerrilla-games.com/read/nubis-cubed)
describes fluid-modelled voxel shapes, compressed-SDF acceleration, noise up-resolution, accelerated light sampling,
dark edges and inner glow. These capabilities are not all present in stock UE clouds.

**Inferred method:** carve a low-frequency envelope with curl-distorted Worley detail at fixed world scale.
Subtract/remap detail near the boundary instead of multiplying uniform noise through a union of growing spheres.
Advect detail with rising flow, overturning and shear; avoid radius inflation as the growth animation. Use
phase-blended flow coordinates to limit stretching, and band-limit detail to the actual march. Distinguish
young liquid edges from aged fibrous ice. Validate this interpretation at equal measured cost before adoption.

## Real-weather rubric: inferred checks, not universal meteorological laws

Match weather type, lifecycle, viewing direction and exposure to references. Mark inapplicable cues N/A; fair-weather
cumulus does not require a near-black base, and non-supercell funnels do not require a wall cloud.

1. A coherent condensation base is flat and comparatively hard; local lowering/scud has an identifiable cause.
2. A thick cumulonimbus base contrasts strongly with sunlit tops and the bright horizon slot.
3. Young liquid turrets have crisp cauliflower creases; old turrets/anvils become fibrous.
4. Lobes have a scale hierarchy: roughly 1-3 km turrets, 100-300 m sub-lobes, 10-50 m tufts where resolvable.
5. Shaded faces trend blue-grey, sunlit faces warm-white; backlighting darkens the body and brightens rims.
6. Haze affects distant low bases more than high tops; avoid equal fog at all heights.
7. Anvils streak along upper winds and transmit light at thin edges.
8. Apparent scale agrees with distance, storm dimensions and funnel width; preserve horizon/curvature cues.
9. Scud rises into inflow, bands converge, shelf undersides boil, and turrets rise and fray over minutes.
10. Funnels show path-length opacity, ragged rims, a translucent sheath and a potentially wider debris skirt.
11. Funnel colour follows light; debris follows soil; the base join does not have an arbitrary colour seam.
12. Supercell funnels join a lowering with coherent wall-cloud/clear-slot anatomy; do not apply this to landspouts.
13. Shape fits environment and stage: contorted rope-out, broad low-contrast wedges, laminar landspouts.
14. Rotation differs across core, sheath and debris; brief subvortices orbit rather than rigidly scrolling together.
15. Use a consistent measured exposure, plausible highlight clipping and distant softness; grain is a camera cue,
    not a substitute for shape. Stills cannot pass motion.

Primary reference anchors: [WMO cumulus](https://cloudatlas.wmo.int/en/cumulus-cu.html),
[cumulonimbus](https://cloudatlas.wmo.int/en/cumulonimbus-cb.html),
[arcus](https://cloudatlas.wmo.int/en/clouds-supplementary-features-arcus.html),
[NWS supercell anatomy](https://www.weather.gov/spotterguide/supercell2),
[tornado lifecycle](https://www.weather.gov/spotterguide/tor_life),
[SPC tornado FAQ](https://www.spc.noaa.gov/faq/tornado/),
[Dodge City funnel/debris observations](https://par.nsf.gov/servlets/purl/10384234).
Visible condensation is not the whole vortex; opacity/shape is not a reliable intensity rating.

## Untested: layered soft-shell tornado bound

Film uses separate funnel, sheath, debris and parent-cloud layers
([Twisters production](https://blog.siggraph.org/2024/12/the-special-and-visual-effects-behind-twisters.html/)).
The following shell counts and costs are proposals, not a demonstrated photorealistic recipe:

- Try four condensation shells at profile radii x0.5/0.7/0.85/1.0 and one or two dust shells x1.15-1.4,
  restricted to the lower 30-50% when ground contact exists.
- Start per-shell alpha at 0.2-0.35; put seeded streak/noise variation throughout opacity, not only colour or
  silhouette. Stacked alpha `1-(1-a)^k` creates central density without a uniform opaque fill.
- Offset noise per shell, stretch it vertically and shear angle with height. Increase noise scale outward.
  Use constant angular velocity within a modified-Rankine core and roughly r^-1.6 outside; outer shells billow.
  Rope uses 1-2 layers; wedge favours the sheath; multiple vortices use small tubes within a broad sheath.
- Compare transient shells at 0.3, 2, 10 and 25 km. Reject visible concentric contours, sort popping in rotation,
  implausible haze contrast or no blind-review improvement. Record video and cost before adding complexity.
- If shells fail, bound a 16-32-step raymarch in a translucent proxy with opaque-depth clipping; test full-screen
  overdraw near the camera. Bound HV separately with range raised and an explicit behind-cloud occlusion test.
  Reserve analytic seeded particles for secondary dust/debris until the core representation passes.

## Untested: renderer-versus-shape decision sequence

Verify live hashes, material pins, cvars and camera state first. Hold seed, time, sun and exposure; keep a repeat
baseline and restore readback. Use one bounded hypothesis at a time, same-session player captures plus labelled
study views, independent review and GPU measurements. Stop after repeated failed bounds and investigate structure.

- **T0, learn from a reference volume, offline:** measure a credible reference density (e.g. the
  [WDAS cloud data](https://disneyanimation.com/resources/clouds/), CC BY-SA 3.0) for the qualities that make a cloud
  fluffy: edge density falloff, detail layered across scales, internal structure. Compare those numbers with the
  generator's output. Never copy a reference's outline or shape into the scene or the generator, and never ship
  reference data; shape is irrelevant because real clouds keep changing. Record licence and provenance.
- **Sampling isolation:** render the generator's own density in a HeterogeneousVolume (MaxTraceDistance raised,
  overlapping clouds hidden). Better detail implicates the cloud step; lighting/compositing differences remain a
  confound to control.
- **T1, MS family bound:** keep density fixed; compare a high-Contribution/low-Occlusion setup with
  Contribution 0.5 / Occlusion 0.5. This paired family bound tests excess fill, not either pin individually.
  Improved crease/core contrast supports the MS hypothesis; it does not independently pass realism.
- **T2, shape method:** compare envelope-minus-curl-distorted-Worley erosion with the current form at equal cost,
  fixed world detail scale and matched lighting. Improvement supports adopting erosion before a new renderer.

If all routes fail, the integrator is a hypothesis, not a proven ceiling: check import, scale, lighting parity and
reference suitability before bounding a material dark-edge term or custom march. Record remaining failures,
motion evidence and packaged performance separately. Research and compilation never constitute visual acceptance.
