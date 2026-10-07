---
name: video-capture
description: Record what moves in an Unreal editor or PIE session as real video — MediaIO (UFileMediaOutput + CaptureActiveSceneViewport) for the game viewport, one MediaIO frame per step for stepped or seek-driven sequences, an ffmpeg desktop-duplication screen recorder for anything the editor UI must show — then inspect it with ffmpeg and label it honestly. Never a HighResShot sequence.
fires-when: Any claim about motion (drift, growth, boil, flicker, popping, a moving sun, rain fall, a lifecycle), any time-lapse or stepped playback of authored or simulated data, and any clip handed to a judge or shown to the owner. Skip for a single scene-state still, which a still capture covers.
---

# video-capture

**Owner: the one agent that owns the live editor this round.** Recording attaches to a running editor or PIE session, so it obeys the single-writer rule in `guides/tooling-ue.md`; reviewers judge the clip afterwards, fresh. Engine facts behind each route are cited per engine version (`verify-engine-claim`); the project adapter names its own capture and recorder scripts and evidence paths. This skill is the pattern they implement.

Doctrine this enforces: **evidence, not assertion** — a pair of stills never proves motion; **tool success is not proof** (`lessons.md`) — a capture that "started" has proven nothing until its frames are on disk and show the game view.

## Choose the route
| Need | Route |
|---|---|
| Real-time clip of the game view in PIE | MediaIO capture of the active scene viewport (below). Preferred. |
| Stepped or seek-driven sequence (one frame per keyframe, per reimport, per seek) | The same MediaIO capture running for the session; keep one frame per step after it settles. |
| Anything the editor UI, a UMG HUD or a non-PIE editor viewport must show | Screen recorder (ffmpeg `ddagrab`). |
| Deterministic fixed-timestep render of a sequence | Engine offline routes (below), in their own PIE. |
| A single still for look metrics | A still capture; not this skill. |

**Never a HighResShot sequence.** It is slow (tens of seconds a frame), floods the editor with screenshot notifications, and renders a fresh view through a different path from the one the player sees, so a sequence of them is neither real time nor what the player gets. Briefs must not offer it for sequences.

## MediaIO capture of the running PIE viewport
- **Plugin:** MediaIOFramework is off by default; enable it in the `.uproject` and restart once (`native-iteration`).
- **Objects:** a transient `UFileMediaOutput` (`file_path`, `base_file_name`, `write_options` with format JPG/PNG/EXR, async writes, `override_desired_size` + `desired_size`), `create_media_capture()`, then `capture_active_scene_viewport(MediaCaptureOptions)`. The viewport lookup prefers the PIE viewport and falls back to the active level-editor viewport, so refuse to start when PIE is not running unless the editor viewport is what you want. Nothing is saved; transient objects are collected.
- **Drive it from game-thread Python** with a Slate post-tick callback: start, count engine ticks, stop after N real seconds (`stop_capture`), wait about 1.5 s for the async write queue to drain, then count files and write a summary JSON (frames written, capture fps, wall and game ms per frame, engine fps and p95 during the capture, frames per engine tick). Results return only through log lines and that JSON.
- **Width must be a multiple of 64.** The file capture rejects padded readback rows (GPU row pitch aligns to 256 bytes) and drops to state ERROR on the first frame. Round the width down and resize in the render pass (`RESIZE_IN_RENDER_PASS`); check the capture state each tick and stop on ERROR.
- **Overrun** (measured 2026-10-06, UE 5.8, 10 s same-session A/B): `SKIP` (default) writes about 0.8 frames per engine frame with no measurable frame-time cost — use it for review clips. `FLUSH` writes every engine frame but stalls on readback (p95 frame time roughly tripled in measurement) — use it only when every frame matters. Set `skip_frame_when_running_expensive_tasks = False`.
- **JPG frames** (quality ~90) are about 100 KB at ~1200x900, a few MB/s at 40 fps; PNG or EXR only when the metric needs it.
- **Measure the cost** with a same-session `measure` run (frame timing with no capture) against the capture run; baselines drift tens of percent between runs, so never compare against another session.
- **Encode:** `ffmpeg -framerate <capture_fps> -i <dir>/frame_%05d.jpg -c:v libx264 -pix_fmt yuv420p -crf 20 clip.mp4`.
- **What it includes:** the final tonemapped scene viewport (post-process, volumetrics); no editor UI and no UMG HUD. Colour matched a screen recording of the same viewport within 1/255 in measurement. Whether it works with the editor window hidden or minimised is unproven.
- **Warm-up PIE after any material recompile.** The first PIE after a live material recompile is not ready and the capture records the editor viewport instead of the game view. Start and stop one PIE first, then capture; discard any frame that shows the editor view.

### Stepped and seek-driven sequences
Run one MediaIO capture for the whole session into a raw folder. Per step: apply the step (seek, reimport the texture for that keyframe, set the state), let it settle a fixed number of ticks, then keep the Nth frame that lands after the settle (copy it to `frames/f_<i>.jpg`) and delete the other raw frames as they arrive. The same pruning gives a uniform real-time lapse (keep one frame per interval, optionally every frame of a short opening excerpt) without filling the disk. Record each kept frame's step id and arrival time in the summary.

## Screen recorder fallback (ffmpeg desktop duplication)
- `ffmpeg -f lavfi -i "ddagrab=output_idx=<n>:framerate=30:draw_mouse=0:offset_x=<x>:offset_y=<y>:video_size=<w>x<h>" -t <s> -vf "hwdownload,format=bgra,format=yuv420p" -c:v libx264 -preset veryfast -crf 18 out.mp4`, with the rectangle taken from the editor window (`GetWindowRect`, process DPI-aware) clipped to its monitor and made even. Write a JSON beside the clip: rectangle, monitor, fps, start time (UTC).
- **Read-only:** it never sends input or changes focus; the window must be visible and not minimised. Never use OS input injection to bring it forward.
- **Monitor index:** `ddagrab` numbers outputs in DXGI order, which is not the .NET `Screen.AllScreens` order. Map by display number (`\\.\DISPLAY1`, `DISPLAY3`, ...) and allow an explicit output-index override; check the first frame of every new setup shows the right screen.
- `gdigrab` drops frames and runs below real time; do not use it. `ddagrab` held a steady 30 fps in measurement.
- From a POSIX shell on Windows, call PowerShell recorders with `-NoProfile -ExecutionPolicy Bypass -File`; a restrictive policy otherwise refuses the script and nothing is recorded.

## Engine offline routes (verified in source, own PIE)
- `r.DumpingMovie N`: dumps the post-processed game viewport each frame, but its synchronous readback drops the frame rate, so frames are irregular real-time samples. A fallback when MediaIO is unavailable.
- `ULevelCapture` via `SequencerTools.RenderMovie` (deprecated but compiled): launches its own PIE and runs a fixed timestep (1/FrameRate a frame), so motion steps are deterministic; refuses while PIE is running.
- Movie Render Queue (PIE executor): deterministic custom timestep, native MP4 and image sequences; needs the plugin enabled and a restart, and a Level Sequence. A smoke test rendered without volumetric clouds; the cause is unverified, so prove the subject renders before relying on it.
- Fixed-timestep routes force the game clock: any game time-compression must still advance from world delta time to be valid.

## Inspect with ffmpeg
- One frame: `ffmpeg -ss <t> -i clip.mp4 -frames:v 1 f.jpg`.
- Contact sheet: `-vf "fps=2,scale=480:-2,tile=6x4"`.
- Change and brightness over time: `-vf "crop=...,signalstats" -f null -` per crop, or frame differences; a pop is a step well above the median frame change.
- Judges get the clip plus a sheet, never a single still.

## Label every clip honestly
State the clock (real-time screen or viewport capture, seek- or step-driven sequence, or offline fixed-timestep render), the speed-up and how it was produced (game compression, step interval, encode framerate), the view (player or study), the seed and the camera. A simulation time-lapse is not real-time gameplay. A paused comparison is labelled paused.

## Evidence required
The capture summary JSON (frames written, capture fps, overrun mode, size, engine fps and p95), the first frame checked for game view vs editor view, the encode command, the clip and sheet paths, the label, and what was not verified.

## Block these
- A HighResShot sequence, or a pair of stills offered as motion evidence.
- A capture accepted from "started" without frames on disk and a first-frame check.
- A capture right after a material recompile without a warm-up PIE.
- A clip with no clock, speed-up or view label.
