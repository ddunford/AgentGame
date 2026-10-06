---
name: perf-gate
description: Profile a scene or change against a committed budget (stat unit → Insights), name the bound, check the worst frame under load, and gate work out on perf — a lightweight per-task check for hot-path work and the P3–P4 hard gate. Measure on a representative build; a PIE number is not a shipping number.
fires-when: Setting or enforcing a frame/memory/bandwidth budget, profiling a hot-path change, diagnosing a hitch or a memory/bandwidth blowout, or gating a build on perf (P3–P4). Runs fresh, never the builder.
---

# perf-gate

**Owner: `performance-engineer`** (Verify & Judge for perf — sets the budget, then gates against it). Craft depth — the budget discipline, the profiling method, ElseCity's compounding pressure (streaming × density × UGC) — lives in `guides/performance.md`; the per-frame budget in `guides/game-feel.md`, bandwidth in `guides/networking.md §4`, engine perf facts (the `WITH_EDITOR` caveat, monotonic server residency, ISM server-collision cost, Nanite reduces per-draw not draw calls) in `guides/unreal-engine.md`. Profiling via `stat`/Unreal Insights (`guides/tooling-ue.md`). Run fresh — the builder never signs off their own perf.

Doctrine this enforces: **build ≠ verify** (1) — a fresh perf pass against the committed budget; **spec first** (2) — budgets committed in P1, the pass measures against them, no budget = no gate; **verify claims against source** (10) — route any engine-behaviour claim to `engine-verifier`.

## Procedure

1. **Confirm a committed budget exists.** Frame (split by thread + draw calls), memory (client pools + server-at-full-map), bandwidth (per-connection cap × 128), per target platform. No budget means no gate — set and commit it (P1) before enforcing. A defect is "misses the 16.6 ms game-thread budget at density," not an opinion.
2. **`stat unit` first — find the bound before optimizing.** It names the thread you're bound on (game / render / GPU / draw). Optimizing the wrong bound (a GPU win on a game-thread-bound frame) buys nothing. Add `stat game`, `stat scenerendering`, `stat rhi`, `Stat Net` as the readout narrows it.
3. **Trace the worst frame with Unreal Insights**, not the live average — a timeline capture across a session catches the GC spike, the tick storm, the streaming hitch a `stat` readout averages away. Design against the worst frame, never the mean.
4. **Profile the interaction, at load.** Target player density × UGC present × streaming active, together — never an empty hub. Their product is where the frame, server memory, and bandwidth all blow at once. Budget server residency against the **full map** — server streaming's loaded set is monotonic; a restart is the only reset.
5. **Lightweight per-task check for hot-path work** (P2 onward): for a change on a hot path, `stat unit` before and after on a representative scene under the capture contract (`qa-visual-battery`: same framing, same-session baseline and repeat, overrides read back and restored; single GPU profile dumps are noisy, so compare medians), confirm no new hitch and no regression against the budget. Watch for avoidable ticks — event-driven where an event would do; the server pays for no cosmetic-only work.
6. **The P3–P4 hard gate: representative build or the number is a lie.** PIE and `-server` run `WITH_EDITOR=1` — valid for *correctness* (finding a tick storm, a relevancy mistake), invalid for a *shipping* frame/bandwidth number. The hard gate waits for the cooked build on the source-built engine, on target hardware.
7. **Render a fresh pass/fail against the committed budget** — every budget met at the worst frame under load, server tick holds (a server hitch reads as lag on every client), bandwidth within the per-connection cap. Never self-signed.
8. **Decision rights.** Budget values within the plan and optimization approach are agent-decidable — decide and log. Content/scope cuts to hit a budget are owner-reserved — escalate with a recommendation.
