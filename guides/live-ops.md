# Guide — Live-ops (running the live game)

> Read before shipping anything to a live build, running a live event, or responding to an incident. The core idea: **once players are in the world, every change runs the same gated pipeline the game shipped through — build ≠ verify does not lapse at launch — and every live change is measured against the blast radius of getting it wrong on a persistent, populated world.** This is the constitution's Phase 5.

## The two failures this prevents
1. **The post-launch shortcut.** "It's just a hotfix" — pushing a change to live without the gated pipeline (`guides/production-pipeline.md`) because the game already shipped. A live persistent world is the *highest*-stakes place to skip verify, not the lowest: the defect ships to everyone at once, on top of state that cannot be rolled back like a build can.
2. **No way back.** Shipping a live change with no rollback path and no measured baseline, so when it goes wrong there is neither a signal that it went wrong (that is `guides/analytics.md`'s job) nor a lever to undo it. Every live change is planned backwards from "how do we revert this."

## The Phase 5 gate — per live change
Phase 5's gate is **per change**, and it is owner-reserved for anything public-facing, involving money, or irreversible (`<studio-root>/AGENTS.md`, `guides/production-pipeline.md §3.2`). Live-ops owns *running* that gate:
- **Every content update runs the full gated loop** — build by the discipline owner, verified fresh by `qa-*` / `creative-review`, perf-gated (`guides/performance.md`), security-reviewed if it touches a client endpoint (`security-reviewer`). Live is not an exemption from the loop; it is the loop with real players downstream.
- **Classify every change by blast radius and reversibility.** Cosmetic + reversible + no economy/public/money surface → agent-decidable, log it. Anything touching the economy, the public surface, real money, or player-persistent state → **owner-reserved**, framed with a recommendation and a rollback plan. The `decide` classification (`technical-director`) applies unchanged.
- **A live change is not done when it deploys** — it is done when the post-deploy signal (`guides/analytics.md`) confirms it did what it intended and broke nothing, within the watch window.

## Release cadence, live events, and the persistent-world constraints
- **Cadence is a rhythm the players feel** — regular, predictable content and event beats sustain a live world; erratic drops read as a dying game. Size each release to what the gated pipeline can verify, not to a marketing date.
- **Live events** are authored, verified, and scheduled content — they run through the same gate. A time-boxed event has a *start and an end that must both be tested*, and a fallback if it misbehaves live.
- **The persistent, zone-sharded world shapes every operation** — this is where the engine facts bite (link, do not restate):
  - **Server memory residency grows monotonically and only a restart resets it** (`guides/unreal-engine.md §2`). So a maintenance/restart cadence is a live-ops operational lever, not just a deploy mechanism — plan restarts, and drain players gracefully.
  - **128 connections is a hard per-instance cap on this engine** (`guides/unreal-engine.md §3`) — capacity planning and instance/shard counts are sized against it, not guessed.
  - **Cross-district travel is a disconnect-reconnect + full map load** (`guides/unreal-engine.md §9`) — a deploy that changes a destination map is a change players hit at a door, mid-experience; sequence it so nobody is mid-travel into a version that no longer exists.

## Hotfix, rollback, and incident response
- **Rollback is designed before deploy, not improvised during an incident.** Know, for every change: how to revert the binary, how to revert or migrate any data/schema change (a data migration is *not* trivially reversible — treat it as owner-reserved and irreversible-leaning), and how to disable a feature behind a flag without a full redeploy.
- **Feature flags / server-config toggles are the first-line live lever** — turning a misbehaving feature off should not require a build. Prefer a toggle to a hotfix where the failure is contained.
- **Incident response is a rehearsed runbook, not a scramble.** Detect (from `guides/analytics.md` signal + crash reports keyed to the build version, `guides/build-release.md`) → assess blast radius → mitigate (flag off / rollback / restart) → communicate → post-mortem into the owning guide (doctrine 13). Severity sets the speed: a live economy exploit or a data-loss bug is stop-the-line; a cosmetic glitch is next-cadence.
- **Never trust the client, still and especially live** — a live exploit is a live economy/security incident (`security-reviewer`, doctrine 11). The moderation/trust-&-safety surface (a separate long-lead discipline) is a live-ops partner, not this role's remit.

## PRINCIPLES
- **The gated pipeline does not lapse at launch.** Every live change is built by one owner and verified by another. Build ≠ verify, on live, most of all.
- **Plan the rollback before the rollout.** No change ships without a known way back and a measured baseline to detect it went wrong.
- **Classify by blast radius.** Reversible + cosmetic + no money/public/persistent-state surface is agent-decidable; everything else is owner-reserved with a recommendation.
- **Cadence is a promise.** Predictable beats sustain the world; size releases to what can be verified, not to a date.
- **A deploy is not done until the signal confirms it.** Watch the post-deploy window (`guides/analytics.md`) before calling a change good.
- **Toggles before hotfixes; hotfixes before firefights.** Contain failure with a flag; escalate to redeploy only when you must.
- **Restarts are an operational lever.** Persistent-world server residency and capacity are managed, planned, and drained — not left to chance (`guides/unreal-engine.md §2–3`).

## QUALITY BAR
A live change is ready to ship when all hold:
- **Ran the full gated pipeline** — built, verified fresh, perf-gated, security-reviewed if client-reachable.
- **Rollback path known and tested** — binary revert, data revert/migration plan, and/or a feature flag to disable without redeploy.
- **Baseline + watch metric defined** (`guides/analytics.md`) so "it worked / it broke" is measurable within the watch window.
- **Blast radius classified**; owner-reserved calls (money / public / persistent-state / irreversible) escalated with a recommendation, not self-decided.
- **Version-stamped and traceable** to the commit and to crash/analytics data (`guides/build-release.md`).
- **Capacity + restart plan** accounts for the 128-connection cap and monotonic server residency.
- **Players not stranded** — no deploy leaves someone mid-travel or mid-transaction against a version that no longer exists.

## COMMON FAILURE MODES
- **"Just a hotfix."** Skipping the gate because the game already shipped. → the gate is per-change and hardest-stakes on live.
- **No rollback.** Shipping with no way back; discovering the need mid-incident. → design the revert first.
- **Deploy-and-forget.** No post-deploy watch, so a regression rides for hours before anyone notices. → defined baseline + watch window.
- **Silent economy/exploit damage.** A live change opens a dupe/exploit; the client was trusted. → security-review client-reachable changes; treat economy incidents as stop-the-line.
- **Erratic cadence.** Feast-or-famine drops; the world reads as abandoned. → a predictable rhythm sized to verify capacity.
- **Capacity guessed.** Instance/shard counts not sized against the 128-cap and residency growth. → plan capacity and restarts against the engine facts.
- **Improvised incident response.** No runbook, no severity ladder, no post-mortem. → rehearsed detect→assess→mitigate→communicate→learn; capture the lesson (doctrine 13).
- **Irreversible data change treated as reversible.** A schema/data migration shipped as if it could be rolled back like a binary. → data migrations are owner-reserved and irreversible-leaning.

## CHECKLIST
**Per live change (before deploy):**
- [ ] Ran the full gated pipeline (build by one owner, verified by another; perf + security as applicable).
- [ ] Rollback path known and tested (binary / data / feature flag).
- [ ] Baseline + watch metric defined with `guides/analytics.md`.
- [ ] Blast radius classified; owner-reserved calls escalated with a recommendation + rollback plan.
- [ ] Version-stamped and traceable (`guides/build-release.md`).
- [ ] Capacity/restart impact checked against the 128-cap and residency growth (`guides/unreal-engine.md §2–3`).
- [ ] No player stranded mid-travel/transaction by the deploy (`guides/unreal-engine.md §9`).

**Live event:**
- [ ] Start *and* end both tested; fallback if it misbehaves.
- [ ] Scheduled with a defined watch window.

**Incident:**
- [ ] Severity classified; stop-the-line for economy/data-loss/security.
- [ ] Detect → assess → mitigate (flag/rollback/restart) → communicate → post-mortem.
- [ ] Lesson written into the owning guide the same session (doctrine 13).

## Sources
- Live-service operations practice — release cadence, feature-flagging, incident-response runbooks, blameless post-mortems (SRE literature). `[verify — web pass]`
- Persistent-world / MMO live-ops patterns — graceful restarts, capacity planning, event scheduling. `[verify — web pass]`
- Engine facts (server residency, 128-connection cap, cross-district travel) live in `guides/unreal-engine.md §2, §3, §9`. Signal + dashboards: `guides/analytics.md`. Build traceability: `guides/build-release.md`.
