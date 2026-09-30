---
name: creative-review
description: Judge whether a craft/creative deliverable is on-pitch — spec-match element-by-element first, then score the ranked emotional beats in priority order — with standing to say off-pitch, stop. Always a fresh reviewer, never the builder.
fires-when: Before committing to a design direction, at milestone close, when the owner says something feels wrong, when two disciplines disagree about "good", and before any craft/creative work reaches the owner. Skip for work with no creative surface.
---

# creative-review

**Owner: `creative-review`** (Verify & Judge — judges, does not build). What "ours" means — the pitch, pillars, anti-goals, and the ranked emotional beats — lives in the game's vision/pitch doc and each space's own spec; the senior-eye-before-owner rule in `guides/workflow.md`; where this gate sits in the loop in `guides/production-pipeline.md`. This is the **"is it good, and is it ours"** call that no other discipline owns — every discipline can pass while the result is dead. **Always run as an independent reviewer (different agent/context or person):** the agent that built a thing is the worst judge of it.

Doctrine this enforces: **build ≠ verify** (1) — the on-pitch judge is never the builder; **spec first** (2) — a defect is "doesn't match the spec," not an opinion.

## Procedure

1. **Run fresh, never the builder.** If you built it, you cannot review it — hand it to a cold pass. This is the keystone of doctrine 1 and it does not scale away for speed.
2. **Spec-match FIRST, before any feel judgement.** Check the build element-by-element against the space's own spec — layout / ground / key assets / lighting register / named beats — and mark each **MATCH / PARTIAL / MISS**, citing the spec line. The register/crux miss is the highest-leverage one; a beautiful thing that misses the spec still fails.
3. **Judge from a real look** — the multi-view shots (top-down + eye-level walk included), never a single flattering hero angle. If the capture set can't answer whether an element matches, the verdict is "re-shoot", not a guess.
4. **Then score the ranked emotional beats, in priority order, stopping at the first failure.** A lower beat cannot redeem a failed higher one — say where it breaks and stop.
5. **Exercise standing to stop.** If it's off the pitch, say so plainly — *off pitch, stop*. On-pitch is a gate work crosses out, not a courtesy. "Crude" excuses low fidelity, never unmotivated or nonsensical craft.
6. **Render the verdict: ON PITCH / ON PITCH WITH CHANGES / OFF PITCH**, backed by the spec-match table and the beat scores with reasons. This is the mandatory on-pitch gate **before the owner** — the owner is never the first competent reviewer of craft work (`guides/workflow.md`, senior-eye rule). Run fast, but always run.
7. **Stay in lane vs the other judges.** You are the *expert* on-pitch call; `user-researcher`/`playtest` brings many real players' lived experience; QA asks *is it broken*. When the owner's eyes see a defect a check missed, the check is wrong (doctrine 9) — don't re-assert a green.
