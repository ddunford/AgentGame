---
name: ue-sky-atmosphere-colour
description: Diagnose UE 5.8 sky and twilight colour against real photo ranges, separating camera processing, ozone absorption, atmosphere scattering and ground illumination.
fires-when: A SkyAtmosphere twilight is mauve, the sunset glow is missing, or ground readability and sky brightness disagree. Use before atmosphere or exposure tuning; not as a cloud-shape workflow.
---

# UE sky-atmosphere colour

**Owner: `lighting-artist`.** Use `verify-engine-claim` for engine assertions and a fresh visual reviewer for
acceptance. This procedure records source and measured findings verified 2026-10-08; numeric trial outcomes are
diagnostics from one scene, not universal settings or a visual pass. Keep project evidence paths in the project's
own skill, linked to this method.

## Measure before choosing a lever

1. Match real photographs by sun elevation, solar/antisolar direction, cloud cover and camera framing. Preserve
   provenance, licences, white-balance limits and excluded processed images. Infer sun elevation from time/location
   only when reliable; label the inference. Build ranges per band, not one twilight-wide target. Upper sky in a
   photograph is not necessarily zenith. A criterion preserving a known-wrong magenta baseline must be replaced by
   photo ranges, with the earlier rejection retained rather than retroactively passed.
2. Read the live atmosphere, fog, sun, sky light and merged camera/volume post-process settings. Separate component
   defaults from the settings actually rendered. Hold seed, sun, camera and exposure fixed. Repeat a baseline in
   the same session; count effects only beyond three times repeat noise and the preregistered gap threshold.
3. Use per-shot MediaIO capture, ON and clouds-hidden OFF. Stop capture after each shot so PNG writes do not queue
   throughout a long run. Keep a settled frame; validate the manifest and restore state. Use the actual player view,
   sun azimuth +/-35 deg at the same pitch, and a clearly labelled +60 deg study view for zenith measurements.
   At least two fixed seeds guard against one favourable weather state. Stills do not prove motion.
4. Linearise sRGB before ratios. Record shadow `R/B - G/B` (lavender index), horizon/sky10 luma, upper-sky D65 Lab
   hue/chroma, ground/upper-sky log2 ratio, lit p99 and clipped-pixel fraction. One verified mask uses max-channel
   ON/OFF difference >=8/255 above 0.2 deg; darkest 30% for shadow and brightest quarter for lit colour. Clip means
   any encoded channel >=250. Match angular regions: horizon 0.5-2 deg, sky10 9-11, upper 24-30, zenith 75-88,
   ground -6..-1. Do not mix linearised display ratios with scene-referred exposure brackets.

Before long capture runs, check **free commit**, not just physical RAM, and per-process private bytes, including
`SteelSeriesCaptureSvc` when installed. A verified 2026-10-08 editor OOM coincided with a capture-service leak of
over 100 GB. Per-shot capture does not fix a leaking external service. Do not start the batch with exhausted or
rapidly falling commit headroom; resolve the process owner first and repeat the baseline after any restart.

## Bound the camera pipeline

Use one transient family bound: `ShowFlag.LocalExposure 0`, post-process `ExpandGamut=0` and `BlueCorrection=0`.
Keep exposure unchanged and read back the effective volume. Restore the show flag to 2 and the original property
values. Reject this family as the shared colour explanation if hue/chroma/lavender barely approach photo ranges;
still record highlight changes separately. In the verified case, colour gaps closed <30% while lit p99 rose
10-14%: camera processing affected highlights but did not explain mauve twilight. This is not proof that every
camera setting is irrelevant in every scene.

## Ozone colour, not just amount

UE defaults to ozone extinction `(0.000650,0.001881,0.000085)/km`, equivalent to single wavelength samples
680/550/440 nm of Bruneton's cross-section. The Chappuis peak lies inside the sRGB red response; these samples
under-absorb red, leaving red and blue while removing green. Source: `Engine/Source/Runtime/Engine/Private/Components/
SkyAtmosphereComponent.cpp:121-126`; coefficient product/clamp in
`Engine/Source/Runtime/Engine/Public/Rendering/SkyAtmosphereCommonData.cpp:135`; absorption in
`Engine/Shaders/Private/SkyAtmosphereCommon.ush:329-348`.

A zero-ozone bound can remove mauve but leave grey/cream; tripling the default amount can saturate violet instead
of making blue. A verified sRGB-integrated 300 DU candidate is `OtherAbsorption=(1.0,0.72,0.0)` and
`OtherAbsorptionScale=0.00249` per km, effective `(0.00249,0.00179,0)/km`. Set it transiently through the component
setters, preserving the original values for restoration. It gives blue twilight in the tested scene; it is not an
automatically adopted production preset. Check noon colour, solar glow, chroma and ground/sky on both seeds before
adoption. A hue fix alone does not pass twilight realism.

The integration uses Bruneton solar irradiance and ozone cross-sections, CIE 1931 colour matching, XYZ-to-linear-sRGB
and effective `k=-ln(rgb_transmitted/rgb_incident)/(15 km * slant_columns)`. Blue's slightly negative fitted
coefficient clamps to zero. It is an RGB approximation, not a spectral atmosphere renderer. Sources:
[Bruneton implementation](https://github.com/ebruneton/precomputed_atmospheric_scattering),
[Lange et al., ozone and sky blue](https://acp.copernicus.org/articles/23/14829/2023/),
[Spitschan et al., outdoor illumination](https://pmc.ncbi.nlm.nih.gov/articles/PMC4895134/).

## Separate sky decay from ground illumination

Bracket exposure at fixed solar elevations. For each region find bias b* that reaches the same encoded luma;
relative scene log2 luminance is -b*, cancelling the tonemapper at that target. Exclude clipped-cache warning frames
and mark extrapolated points. In the verified setup, bias >15 was excluded; targets 30 and 60 kept the -6 deg
measurements in range. Re-derive this boundary for the actual cache pre-exposure and camera setup.

If ground is too dark relative to the sky, exposure alone raises both. Bound sky-light intensity independently,
then express a successful gain as a clamped curve against geometric sun elevation with monotone interpolation.
Use a Movable or Stationary sky light with real-time capture so captured lighting follows the sky. Its intensity
scales lit surfaces and reflections without brightening the visible sky. `SetIntensity` does not recapture;
registered Static lights reject it (`Engine/Source/Runtime/Engine/Private/Components/SkyLightComponent.cpp:971-980,
486-505`). A clock owning intensity must restore the pre-drive value on Off, disable, rebind and EndPlay, and skip
Static lights. Verify selection, monotonicity, clamps, readback and release with automation and live checks.

At late civil twilight, matching photographic darkness can make the road unreadable. Test local headlights while
holding sky/storm exposure fixed; do not assume their presence proves driving readability or acceptable GPU cost.
Keep both player navigation and storm visibility in the acceptance criteria.

## Multiple scattering, cloud ambient and fog

- The atmosphere MS LUT defaults to two rays (up/down); `r.SkyAtmosphere.MultiScatteringLUT.HighQuality 1` uses
  64 sphere directions (`Engine/Shaders/Private/SkyAtmosphere.usf:1253-1281`). The default is 0
  (`Engine/Source/Runtime/Renderer/Private/SkyAtmosphereRendering.cpp:242-244`). `MultiScatteringFactor` scales the
  LUT (`SkyAtmosphere.usf:1334-1336`). These are separate from a cloud material's multiple-scattering octaves.
- Bound HQ and MSF separately, measuring ground, zenith and solar horizon. The verified HQ case gives -8.78/-8.68
  stops of sky decay over sun 0..-6 deg, near the cited ~8.5, but washes the sunset glow. Ground gains 1.43 stops
  while horizon gains 2.71: this rejects the LUT as the tested dark-ground-ratio cause. An attractive source
  hypothesis cannot override that live result. No measured LUT cost increase in one PIE A/B/A is not a shipping
  performance pass.
- `r.EyeAdaptation.CachedLightingPreExposure` changes storage range, not brightness. The -3 -> -6 control changes
  measured regions by 0.00 stop at sun -6 in the verified setup. Source:
  `Engine/Source/Runtime/Renderer/Private/PostProcess/PostProcessEyeAdaptation.cpp:235-253` and
  `Engine/Source/Runtime/Renderer/Private/SceneRendering.cpp:2076,2091-2101`. Deeper twilight still needs a range check.
- Distant sky-light LUT gives one mean-sky sample at default 6 km, used for cloud ambient and non-directional fog
  in-scatter (`SkyAtmosphereRendering.cpp:264-265`; `SkyAtmosphere.usf:1424-1466`; `VolumetricCloud.usf:726-732`;
  `HeightFogCommon.ush:190`). It is distinct from a real-time captured sky-light cubemap.
- Fog directional in-scatter follows an existing sun and its atmospheric transmittance, gated by start distance
  (`FogRendering.cpp:438,179`; `HeightFogCommon.ush:334-339,363-368`). A below-horizon fog discontinuity still needs
  its own readback and bound; do not attribute it from the ozone or ground tests alone.

### Cloud direct light, ambient and veil bounds

Verified in UE 5.8 on 2026-10-08; shader paths are under `Engine/Shaders/Private/`.
With SkyAtmosphere present, cloud ambient uses its distant sky-light LUT, not SkyLight intensity
(`VolumetricCloud.usf:723-738`). Sun illuminance scales the LUT (`SkyAtmosphere.usf:1458-1466`);
a sun-intensity gain therefore does not prove direct sunlight. More SkyLight plus darker exposure
can lift surfaces while blackening clouds and inverting ground/sky: the tested twilight family lost
12/12 blind comparisons (baseline scores 1.5, candidate 1.0). Bound this separation before tuning.

`bUsePerSampleAtmosphericLightTransmittance` selects outer-space illuminance times sample-position
transmittance (`VolumetricCloud.usf:645-650,923-930`). Flag-off uses the CPU 500 m ground path
(`Engine/Source/Runtime/Engine/Public/Rendering/SkyAtmosphereCommonData.cpp:231-269`).
Planet occlusion returns zero (`SkyAtmosphereCommon.ush:254-257`). Overhead shadow heights are
about 1 km at -1 and 8.7 km at -3; actual cloud height and local geometry matter. The tested
low clouds showed no flag effect below the horizon; shadowed clouds receive distant sky ambient.
Do not generalise this to high towers.

At +1 the flag gave golden tops (+0.74 stop, R/B 0.97 -> 1.41), but exposed a clouds-on field veil
(+144 luma). Bound one switch at a time: cloud `GroundAlbedo=(0,0,0)` removed 98%,
`r.VolumetricCloud.EnableAerialPerspectiveSampling 0` removed 99% but lost distant-cloud fade,
and `r.VolumetricRenderTarget 0` removed only 77%. Black cloud ground albedo retained fade and was
selected for that scene; it also removes cloud-base ground bounce, to revisit when cloud structure
changes. Ground bounce approximates ground transmittance with sample sun transmittance
(`VolumetricCloud.usf:1025-1034`); AP is coverage/mean-depth weighted (`:1492-1541`), and samples
outside the shell are skipped (`:892-898`). These bounds do not prove low cloud density or a
specific reconstruction fault.

The combined flag/black-albedo case won 10/11 non-tied blind pairs and cost +0.11 ms cloud pass
in PIE, but retained sun-facing top clipping (up to 7.9%), seed-dependent warm ground tint and
failed absolute realism. Record the tradeoffs; this is a diagnostic route, not a universal preset.

## Evidence and acceptance

Retain per-shot state, seed, geometric sun elevation, camera, exposure, ON/OFF frames, baseline repeat noise,
photo provenance/ranges, metric tables and restore readbacks in the project's evidence location. Label player versus
study views and scene versus display measurements. Keep each original trial verdict and name remaining failures.
Run a fresh blind photo comparison and the project's visual/performance gates before adopting the combined look.
Night lighting, other atmospheres, headlight readability and packaged cost remain unproven by these findings.
