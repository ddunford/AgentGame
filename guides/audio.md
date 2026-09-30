# Guide — Audio craft

> Read before authoring or revising any space's sound. The core idea: **a soundscape is composed, not summed — every sound is given a place in level, in the frequency spectrum, and in physical space, so that at any instant the player hears a legible mix that leads the ear, and it is judged by ear by a fresh reviewer, never declared done because the files played.**
>
> This guide owns the **craft** — the artistic and mix principles, engine-agnostic. The **client-side wiring rule** (audio never replicates; per-client actors and data layers; the door's street-hum → garden-stillness contrast) is the `sound-designer` agent's law and lives in the vault `zones.md`; it is folded in here as principle, never re-specified. Engine mechanics (MetaSounds, Sound Attenuation assets, Submixes, Concurrency, occlusion traces, the PLA-drops-audio rule) will be captured in `guides/unreal-engine.md` as we hit each one — the PLA-drops-audio rule is there now (§5) — and cross-referenced from here, never duplicated.

## The failure this exists to prevent

A pass generates a good ambient bed, a good rain loop, a good crowd murmur, three good one-shots — every asset clean on its own — plays them all at once at full level, and the result is **mush**. Nothing is heard because everything is heard. There is no headroom for a footstep to register, dialogue is buried under crowd, the rain and the bed fight for the same frequencies and turn to grey noise, and a sound with no attenuation plays at full volume whether the player is next to its source or across the district. Every asset passed on its own. The **mix** was never designed — and the mix *is* the design. That is the wall of sound, and it is the #1 failure: **a sound with nowhere to sit is noise.**

---

## PRINCIPLES

### 1. Layer the soundscape — bed, point sources, one-shots, music (the foundation)
A space's sound is built from distinct layers, each with a different job — this is the `sound-designer`'s working model and everything below is how you make the layers coexist:

- **Ambient bed** — the continuous 2D-ish tone of the place (room tone, city hum, wind, distant traffic). Non-positional or very wide; it establishes *where you are* and must never dominate.
- **Diegetic point sources** — positioned emitters the player can walk toward and away from (a fountain, a neon sign's buzz, a vent, a busker, a doorway spilling music). These carry realism and space; they live or die by attenuation (Principle 6).
- **Interactive one-shots** — event-driven: footsteps, UI, impacts, ability activations, door open/close. They must *cut through* the bed at the instant they fire (Principles 3–4).
- **Music** — where a moment calls for it, adaptive not looped-forever (Principle 9).

The layers are not a stack of equal voices — they are a **hierarchy**. The bed is a floor; point sources sit on it; one-shots and dialogue punch above it. Design the hierarchy first, then mix to protect it.

### 2. Mix for loudness and headroom — leave room for the moment
A mix with everything near maximum has nowhere to go — the important sound cannot get louder than the unimportant one, and transients clip. Design to a loudness target with headroom.

- **Measure loudness in LUFS, not peak.** LUFS (Loudness Units referenced to Full Scale, K-weighted) is the perceptual loudness unit standardised in **ITU-R BS.1770** and **EBU R128**; broadcast targets **-23 LUFS integrated (±0.5 LU)**, streaming platforms sit louder (Spotify/YouTube/Tidal ≈ **-14 LUFS**, Apple Music ≈ **-16 LUFS**). `[web]` [EBU R 128](https://en.wikipedia.org/wiki/EBU_R_128) Games commonly reference the same **ITU-R BS.1770** measurement and target the overall mix around the broadcast **-23 LUFS** neighbourhood (louder for mobile/handheld); the exact number matters less than *anchoring the whole mix to one reference element* — usually dialogue — and mixing everything else relative to it.
- **Keep true-peak headroom.** Cap true peak at **-1 dBTP** so inter-sample peaks and downstream processing never clip. `[web]` [EBU R 128](https://en.wikipedia.org/wiki/EBU_R_128) A one-shot must have room to land *above* the bed without hitting 0 dBFS — that room is headroom, and a bed mixed too hot steals it.
- **Loudness Range (LRA) is a feature, not a bug.** Dynamic range — the gap between the quiet bed and the loud peak — is what makes a soundscape breathe. A brick-walled, everything-loud mix is fatiguing and unreadable. Preserve contrast: a *quiet* space is a design tool (the garden behind the door), not an empty one.

### 3. Carve the spectrum — give every layer its own frequency space
Two sounds occupying the same frequency band at similar level **mask** each other: "the perception of one sound is affected by the presence of another," and within one critical band a louder tone renders a quieter one inaudible. `[web]` [Auditory masking](https://en.wikipedia.org/wiki/Auditory_masking) Low-frequency maskers smear across a *wider* range than high ones (upward spread of masking), so uncontrolled low-end is the usual culprit behind a muddy mix. `[web]` [Auditory masking](https://en.wikipedia.org/wiki/Auditory_masking)

- **Assign each layer a home band.** Bed owns the low-mid body and air; point sources sit where their real source sits; dialogue owns roughly **1–4 kHz** (intelligibility); one-shots get presence around **2–6 kHz** to click through. When two elements want the same band, decide which one wins there and **EQ-carve the other out of it** (complementary / reciprocal EQ). `[web]` [Auditory masking](https://en.wikipedia.org/wiki/Auditory_masking)
- **High-pass everything that isn't bass.** Rumble and sub energy pile up under the mix and mask everything above. Roll off the low end of every layer that has no business down there — the bed keeps its floor, the rest clears out of it.
- **EQ discipline is subtraction first.** Carve to make room, don't boost to compete — boosting to win a band just raises the masking floor and drives the wall of sound.

### 4. Prioritise by ducking — the important sound wins in real time
When a high-priority sound fires (dialogue, a critical cue, a threat), the mix must *make room for it* automatically rather than hope it is loud enough. **Ducking** is side-chain compression: the level of one signal is reduced by the presence of another — the classic case is music/ambience dipping under speech, with the speech routed to the compressor's side-chain input. `[web]` [Dynamic range compression](https://en.wikipedia.org/wiki/Dynamic_range_compression)

- **Duck the bed and music under dialogue and key one-shots**, not the reverse. Tune attack fast enough that the important sound is never clipped at its onset and release slow enough that the bed doesn't pump back up between words.
- **Ducking is a routing problem** — it only works if the thing being ducked and the trigger are on separate buses (Principle 5). You cannot duck ambience under dialogue if they share a submix.
- **Loudness-driven ducking (HDR-style) scales this.** Rather than hand-wiring every pair, a loudness-window system lets the loudest active sound automatically push quieter ones down, so a nearby explosion momentarily makes distant footsteps inaudible — realistic and self-balancing. Reserve it for dense combat spaces (the unsafe districts), not the calm ones.

### 5. Route through submixes/buses — the architecture mixing depends on
You cannot mix, duck, or master what you cannot address as a group. **Bus routing** sends many sources to one destination for shared processing and level control — the same reason a console feeds sixteen channels to one reverb, or groups them to a submaster. `[web]` [Aux-send](https://en.wikipedia.org/wiki/Aux-send)

- **Establish the standard bus tree:** `Ambience`, `SFX`, `Music`, `Voice`, each feeding a `Master`. This is the minimum structure that lets you (a) balance whole categories with one fader, (b) duck one category under another (Principle 4), and (c) put a master limiter on the final bus to guarantee the true-peak ceiling (Principle 2).
- **Sends vs. routing.** A sound's *primary* route sets which category bus it belongs to; a **send** taps a copy to a shared effect (reverb, Principle 7) without moving it off its bus — post-fader, so the effect follows the source's level. `[web]` [Aux-send](https://en.wikipedia.org/wiki/Aux-send)
- **Effect chains live on buses, not on every sound.** One compressor on `Voice`, one reverb the whole space sends to, one limiter on `Master` — process the group, not each emitter. Cheaper and consistent.

### 6. Place every sound in space — attenuation is how a point source becomes real
A diegetic emitter that plays at the same volume everywhere is the audio floating-light: it has a position the ear cannot believe. Give every point source an **attenuation** setup. `[web]` [UE Sound Attenuation](https://dev.epicgames.com/documentation/en-us/unreal-engine/sound-attenuation-in-unreal-engine)

- **Inner radius + falloff distance.** The inner area plays at full volume; volume falls from the edge of that inner area to silence at the falloff distance. Set the inner radius to the physical size of the source and the falloff to how far it could plausibly carry. `[web]` [UE Sound Attenuation](https://dev.epicgames.com/documentation/en-us/unreal-engine/sound-attenuation-in-unreal-engine)
- **Choose the falloff curve deliberately** — Linear, Logarithmic, Inverse, Log Reverse, Natural Sound, or Custom. Real sound obeys the **inverse-square law** (double the distance, quarter the intensity), so *Natural Sound* / *Inverse* read more believably than *Linear* for most spot sounds; a hard Linear cutoff reads as fake. `[web]` [UE Sound Attenuation](https://dev.epicgames.com/documentation/en-us/unreal-engine/sound-attenuation-in-unreal-engine)
- **Match the attenuation shape to the source** — Sphere for most spot sounds, Box for room tone/ambience sized to the room, Capsule for linear sources (a pipe, a rail), Cone for directional throw (a speaker, a PA). `[web]` [UE Sound Attenuation](https://dev.epicgames.com/documentation/en-us/unreal-engine/sound-attenuation-in-unreal-engine)
- **Spatialize point sources; keep the bed wide.** Enable spatialization for 3D positioning (binaural for headphones, panning for speakers); use the non-spatialized radius so a source collapses gracefully to 2D as the player stands on top of it. The bed itself is usually non-spatialized or very wide by design. `[web]` [UE Sound Attenuation](https://dev.epicgames.com/documentation/en-us/unreal-engine/sound-attenuation-in-unreal-engine)
- **Air absorption sells distance.** A distant source loses high frequencies; enable the distance-based low-pass so far sounds go dull and near sounds stay bright. `[web]` [UE Sound Attenuation](https://dev.epicgames.com/documentation/en-us/unreal-engine/sound-attenuation-in-unreal-engine)

### 7. Occlude, obstruct, and reverberate — sound respects geometry
A sound that passes through a wall unchanged breaks the space as badly as light leaking through it.

- **Occlusion.** A trace from source to listener, when blocked, applies a low-pass filter and a volume attenuation with an interpolation time so the transition is smooth, not a click. Muffle a source behind a wall; open it up as the player rounds the corner. `[web]` [UE Sound Attenuation](https://dev.epicgames.com/documentation/en-us/unreal-engine/sound-attenuation-in-unreal-engine) Tune interpolation so it glides — an instant filter snap reads as a bug.
- **Reverb communicates the room.** Reverberation is the persistence of sound after the source stops — **early reflections** first, then a decaying **late tail**; the decay time (**RT60/T60**, the time to fall 60 dB) tells the ear the room's size and material, and it is frequency-dependent. `[web]` [Reverberation](https://en.wikipedia.org/wiki/Reverberation) A big stone hall has a long tail; a small carpeted room barely any.
- **Reverb is a shared send, not a per-sound effect.** Route many sources to one reverb submix per acoustic zone (the console aux-send model, Principle 5) — consistent, cheap, and it means *changing the room changes every sound in it at once*. `[web]` [Aux-send](https://en.wikipedia.org/wiki/Aux-send)
- **Contrast across a threshold is the payoff.** The door beat — loud, wet, wide street hum on one side; quiet, dry, close garden stillness on the other — is authored as a change in *bed level, reverb send, and occlusion* across the boundary. The attenuation and reverb discipline of this section is what makes that moment land (and it is wired client-side, Principle 11).

### 8. Score adaptively — music that responds without fatigue
Looping one track forever is the fastest route to fatigue. Adaptive music changes in response to real-time events. `[web]` [Adaptive music](https://en.wikipedia.org/wiki/Adaptive_music)

- **Vertical layering (vertical remixing)** — stems that fade in and out over a constant base to raise or lower intensity without interrupting the flow; best for *gradual* change (rising tension as enemies close, as in *Dead Space 2*'s fear-level layers). `[web]` [Adaptive music](https://en.wikipedia.org/wiki/Adaptive_music)
- **Horizontal re-sequencing** — distinct pieces that transition into each other for *significant* events (entering a district, a fight starting), via crossfade, phrase-branching (wait for the current bar/phrase to end), or a composed bridge segment. Transition **on a musical boundary**, never mid-bar, or the cut is jarring. `[web]` [Adaptive music](https://en.wikipedia.org/wiki/Adaptive_music)
- **Stingers** — short musical punctuations laid over the current music for a discrete event (a discovery, a death), timed to the beat.
- **State-driven mixing** — game state (safe/unsafe district, combat/explore) drives which layers and buses are up. In ElseCity, Neon Hub is a low-intensity social register; the unsafe districts carry the peaks — music state should follow that, and duck under dialogue like everything else (Principle 4).

### 9. Fight repetition and voice-clutter — variation and limiting
Two failures at the ends of the same axis: too *few* distinct sounds (fatiguing repetition) and too *many* at once (clutter and cost).

- **Vary the repeated.** A footstep or impact that plays the identical file every time reads as mechanical. Rotate a small pool of variations and randomise pitch/volume within a tight range so no two firings are identical. Loops must be seamless *and* long or evolving enough that the loop point isn't a metronome.
- **Limit simultaneous voices (concurrency).** Cap how many instances of a sound (or a category) play at once, with a rule for what happens on overflow — stop the oldest, stop the quietest, or refuse the new one. This protects both the **mix** (ten overlapping footsteps become noise; two read clearly) and **performance** (voices are not free). Prioritise: dialogue and key cues should never be stolen by ambient clutter.

### 10. Wire it client-side — audio is per-player, and never replicates
This is the agent's standing rule, folded in as craft: **audio is a client-only presentation layer.** It is generated by no server, replicated to no one, and driven by non-replicating actors and client-only data layers. Two players in the same spot may hear different mixes (their own footsteps loud, distance-attenuated from each other) — that is correct. The full rule, and the non-replicating actor / client-data-layer mechanism, is the `sound-designer` agent's law and the vault `zones.md`; do not re-derive or duplicate it here. The consequence for the craft: **the mix is authored for one listener at a time**, so spatialization, occlusion, and reverb are all computed relative to *this* client's listener — which is exactly why they work.

---

## QUALITY BAR

A soundscape is at bar when:
- **The mix has a clear hierarchy** — bed sits under, point sources sit in space, one-shots and dialogue punch through; at no instant does the important sound lose to the unimportant one.
- **Loudness and headroom are controlled** — the overall mix sits at a deliberate LUFS target anchored to a reference element, true peak stays under **-1 dBTP**, and there is dynamic range left for a peak to land.
- **The spectrum is carved** — each layer owns its band, non-bass elements are high-passed, and no two elements turn to mud fighting the same frequencies.
- **Priority is enforced by ducking** — dialogue and key cues automatically make room in the mix; the bed and music dip and recover cleanly, not audibly pumping.
- **Every point source is attenuated and placed** — believable falloff curve and radius matched to the source, spatialized, air-absorbed with distance; nothing plays omnipresent that shouldn't.
- **Geometry is respected** — occluded sources are muffled and re-open smoothly; each acoustic zone has a reverb whose decay reads its size and material.
- **A bus/submix tree exists** — Ambience / SFX / Music / Voice → Master, with effects on buses and a limiter on Master.
- **Music is adaptive and non-fatiguing** — layered or re-sequenced to state, transitioning on musical boundaries, not one loop forever.
- **Repetition is broken and voices are limited** — varied one-shots, seamless loops, concurrency caps that protect the mix and the frame.
- **Judged by ear, in place, by a fresh reviewer** — `creative-review` (fresh) first, then an owner listen in-session; never self-approved, never handed to the owner first.

---

## COMMON FAILURE MODES

- **Wall of sound / no priority (the #1 failure).** Every layer at full level, no ducking, no hierarchy — the player hears mush and no single sound registers. → design the hierarchy; duck low-priority under high (P1, P4); leave headroom (P2).
- **Frequency masking / muddy mix.** Layers fighting the same band, uncontrolled low-end smearing everything above. → carve the spectrum, high-pass non-bass, subtract before you boost (P3).
- **Clipping / no headroom.** Mix mastered so hot a one-shot has nowhere to land; transients hit 0 dBFS and distort. → LUFS target with true-peak ceiling at -1 dBTP; master limiter on the Master bus (P2, P5).
- **No attenuation discipline → too loud / omnipresent.** A point source at the same volume everywhere, or a hard Linear cutoff — a position the ear can't believe. → inner radius + falloff matched to the source, inverse-square-like curve, spatialize, air-absorb (P6).
- **No occlusion → sound through walls.** A source heard full and bright from behind solid geometry. → occlusion trace with low-pass + volume attenuation and smooth interpolation (P7).
- **No reverb / wrong room.** Dry sound in a stone hall, or one global reverb for every space. → per-zone reverb send whose decay matches the room (P7).
- **Repetitive / fatiguing loops.** The identical footstep/impact every time; a short bed loop that ticks like a metronome; one music track forever. → varied pools, randomised pitch/level, seamless/evolving loops, adaptive music (P8, P9).
- **No submix structure.** Every sound routed flat to the master, so nothing can be balanced, ducked, or mastered as a group. → the Ambience/SFX/Music/Voice → Master tree, effects on buses (P5).
- **Replicated or server-loaded audio.** Audio treated as shared world state instead of a per-client presentation layer. → client-side wiring, non-replicating actors (P10; the agent's hard block).
- **Declared done without a listen.** "The files play" is not "it sounds good." → by-ear judgement by a fresh `creative-review`, then owner, always.

---

## CHECKLIST (before handing to `creative-review`)

- [ ] **Layer hierarchy designed** — bed / point sources / one-shots / music, with the bed as floor and dialogue/key cues on top. *(the headline gate)*
- [ ] **Loudness target set** and the mix anchored to a reference element; **true peak ≤ -1 dBTP**; audible dynamic range preserved.
- [ ] **Spectrum carved** — each layer has a home band; non-bass high-passed; no muddy clashes.
- [ ] **Ducking wired** — low-priority buses dip under dialogue / key cues, attack/release tuned; no pumping.
- [ ] **Bus tree in place** — Ambience / SFX / Music / Voice → Master; effects on buses; limiter on Master.
- [ ] **Every point source attenuated** — falloff curve + radius matched to source, spatialized, air absorption on distance; nothing omnipresent.
- [ ] **Occlusion on sources that sit behind geometry**, with smooth interpolation.
- [ ] **Per-zone reverb send** whose decay reads the room; threshold contrast (e.g. street → interior) authored in bed level + reverb + occlusion.
- [ ] **Music is adaptive** — layered or re-sequenced to game state, transitioning on musical boundaries; stingers on the beat.
- [ ] **Repetition broken** (varied pools, randomised pitch/level, seamless loops) and **concurrency capped** so voices can't clutter.
- [ ] **Wired client-side** — non-replicating, per-listener; nothing routed through the server (per the agent's law + `zones.md`).
- [ ] **Provenance recorded** — generation prompts and licence terms captured.
- [ ] Handed to `creative-review` (fresh, judged **by ear**) → then an owner listen in-session — **never self-approved, never straight to the owner**.

---

## Acquiring or generating audio

Use project-approved licensed recordings, packs or generation services through available supported tools. No provider, browser transport or credential-relay service is required. Follow host authentication rules; never copy secrets into logs or workflow documents.

Inspect the actual downloaded format and rights, convert through approved tools to an engine-supported format when necessary, and verify the saved import. Choose duration/loop treatment for the intended ambience and audition seams in the game. Provider defaults and output formats can change; verify them instead of inheriting a historical setting.

---

## Engine cross-reference

The **how** in this engine will be captured in `guides/unreal-engine.md` as we hit each mechanic (the PLA-drops-audio rule is there now, §5); until then the UE Audio docs are the reference for the mechanics behind the craft above:
- **Sound Attenuation assets** — shapes, falloff functions, spatialization method, air absorption, occlusion trace channel + low-pass + interpolation, reverb/submix sends, and the focus system. `[web]` [UE Sound Attenuation](https://dev.epicgames.com/documentation/en-us/unreal-engine/sound-attenuation-in-unreal-engine)
- **Sound Submixes** — the bus tree, submix effect chains (EQ/dynamics/reverb), and submix sends that make Principles 4–5 and 7 achievable in-engine.
- **Sound Concurrency** — the voice-limiting/culling rules behind Principle 9 (max count + resolution: stop oldest / stop quietest / prevent new).
- **MetaSounds** — procedural source generation for variation and randomisation (Principle 9) and interactive one-shots.
- **A Packed Level Actor DROPS interior point audio (`AmbientSound`/`UAudioComponent`) at pack time, exactly as it drops lights** — the ISM builder clusters only `UStaticMeshComponent`s, so audio takes the "Component was not packed" warning path. So an interior point source must be authored as a **separate external World-Partition actor** (the same treatment door light-spill / neon gets), never inside the PLA. Mechanism + citations: `guides/unreal-engine.md §5`.
- **The client-side rule (Principle 10) is engine-enforced by `replicates=false` on the audio actor AND a `ClientOnly` runtime Data Layer whose instance is present in the map** — together they keep audio off the wire *and* off the dedicated server (zero server memory, physics, replication). Mechanism + the load-filter-needs-an-instance gotcha: `guides/unreal-engine.md §5` (and §2 for the Data Layer load filter).

The rule: **this guide tells you what a good soundscape *is*; the engine reference tells you what UE will and won't *let you do* to build it.** On any conflict of engine fact, the source-cited engine guide wins — raise a `[verify]` via `engine-verifier`.

---

## Sources
- **Loudness / mix metering:** [EBU R 128](https://en.wikipedia.org/wiki/EBU_R_128) (LUFS/LKFS, -23 LUFS integrated, -1 dBTP true peak, LRA, momentary/short-term/integrated, ITU-R BS.1770 basis, streaming targets).
- **Frequency separation / masking:** [Auditory masking](https://en.wikipedia.org/wiki/Auditory_masking) (simultaneous masking, critical bands, upward spread of masking).
- **Ducking / side-chain:** [Dynamic range compression](https://en.wikipedia.org/wiki/Dynamic_range_compression) (ducking definition, side-chain input, de-essing).
- **Bus / submix routing:** [Aux-send](https://en.wikipedia.org/wiki/Aux-send) (aux sends, pre/post-fader, grouping to a bus for shared processing).
- **Spatialization / attenuation / occlusion / reverb sends:** [Sound Attenuation in Unreal Engine](https://dev.epicgames.com/documentation/en-us/unreal-engine/sound-attenuation-in-unreal-engine) (shapes, falloff functions, spatialization, air absorption, occlusion, focus).
- **Reverb:** [Reverberation](https://en.wikipedia.org/wiki/Reverberation) (early reflections vs late tail, RT60/T60, send architecture).
- **Adaptive / interactive music:** [Adaptive music](https://en.wikipedia.org/wiki/Adaptive_music) (vertical layering, horizontal re-sequencing, crossfade/branch/bridge transitions, Dead Space 2, iMUSE).
