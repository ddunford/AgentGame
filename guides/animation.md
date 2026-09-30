# Guide — Animation method

> Read before rigging, retargeting, or wiring any character motion. The core idea: **animation is where a character becomes alive or reads as a broken puppet, and the difference is almost entirely in the transitions — the blends, the plants, the retarget fidelity — not the individual poses.** A clip that looks right played alone can slide, pop, and snap the instant it's blended into a state machine under real input. Motion is proven by being *watched in motion under gravity and input*, never asserted from a thumbnail or a single-node preview — the same trap the emote pack hit (`Content/ElseCity/Animations/Emotes/EMOTE_PROVENANCE.md`: static pose capture could not even identify which clip was which).

The `animator` agent carries the short rules; this is the depth behind them. Animation is the **middle of the character chain** — it takes a rig-ready mesh and makes it move, then hands the driving logic to gameplay. It pairs tightly with `guides/game-feel.md` (which owns *responsiveness and juice* — animation serves feel, it does not define the latency budget) and defers every engine fact to `guides/unreal-engine.md` (skeleton, Anim Blueprint threading, Iris, root-motion-over-network) rather than restating them.

## The pipeline this sits in

```
character design → model → rig → animation → gameplay
                          │        │            │
              (guides/character-art.md)  (this guide)   (gameplay-engineer)
```

- **rig ← model:** the rig is only as good as the deformation topology it drives (`guides/character-art.md` §2). A mesh with loops at every joint rigs and skins cleanly; one without cannot be rescued in the rig.
- **animation → gameplay:** this guide delivers the motion set (locomotion, jumps, emotes, montages) and the Anim Blueprint that blends it; `gameplay-engineer` drives it with input, state, and the ability system, and owns the *feel-tuning* of the numbers (`guides/game-feel.md`). The handoff is a clean state machine with named entry conditions, not a pile of loose clips.

**The skeleton is the contract.** Everything here is built on the **project skeleton** `/Game/Characters/Mannequins/Meshes/SK_Mannequin` (UE5 Manny). The emote channel is already retargeted onto it; every new clip either authors onto it directly or retargets onto it. A clip on any other skeleton cannot be used until retargeted — this is the single most common way motion work is wasted.

## The failures this prevents

1. **Foot sliding.** Feet that drift across the floor instead of planting — the loudest "this is fake" tell in all of character animation. Caused by a locomotion speed that doesn't match the clip's stride, a missing distance-matching or foot-lock pass, or root motion fighting the movement component.
2. **Popping / blend-snapping.** A visible jump between states or poses — an instant snap where a blend should be, a re-pose on loop, a hitch when a montage ends. The character reads as a puppet whose strings jerked.
3. **Bad retarget.** Motion moved onto the wrong or a mismatched skeleton — limbs stretched, feet through the floor, hips at the wrong height, fingers frozen or exploded. Looks like the clip is broken; the clip is fine, the retarget is wrong.
4. **Missing root motion (or root motion where it shouldn't be).** A clip that should drive world movement from the animation (a mantle, a dodge, a cinematic step) left in-place so the character moonwalks; or an in-place locomotion clip carrying stray root motion so it drifts. Getting the root-motion-vs-in-place decision wrong breaks either movement or authority.
5. **T-pose / ref-pose leaks.** The character flashing to its bind pose (T- or A-pose) or the animation ref pose — a state with no valid pose, a failed asset load, an additive applied to the wrong base, or a state machine with an unreachable/empty state. The single most jarring visible defect there is.

---

## PRINCIPLES

### 1. Rigging — the deformation the rest rides on
- **Skeleton first, always the project Manny.** Rig to `/Game/Characters/Mannequins/Meshes/SK_Mannequin` so the character shares the motion stock. A bespoke skeleton is a decision that isolates the character from every existing clip and must be justified, not defaulted into.
- **Skin weights are the deformation.** Smooth weights across every joint, no stray influences, no more than the platform's max influences per vertex `[verify — web pass]`. The clean edge loops `character-art.md` delivered are what make good weights *possible*; bad topology cannot be weighted well.
- **Bind pose matches the skeleton's.** Match Manny's bind pose (A/T as it ships) or every retarget onto it fights a pose offset.
- **Rig for the animator, not just the deformation.** Where the project uses **Control Rig** (below), the rig exposes controls that map to how a human poses a figure — IK/FK limbs, a spine that arcs, foot and hand controls — not raw bone rotations.

### 2. Retargeting — moving motion between skeletons
Retargeting is how the project reuses motion (Fab packs, Mixamo, MetaHuman, mocap) without re-authoring it, and it is a first-class, routine operation here — the emote channel proves the path end to end.

- **The IK Retargeter is the tool.** Source skeleton + mesh, target skeleton + mesh, a chain map pairing the source's limb chains to the target's, then bake. Where the hierarchies are identical (e.g. UE5 Manny → project Manny) the chain map is identity and the bake is **lossless** — exactly how the emotes were done (`EMOTE_PROVENANCE.md`: `IKRetargetBatchOperation`, identity chain map, frame counts preserved, retargeted assets reference *only* the project skeleton).
- **Retargeted assets must be self-contained.** After retarget, the clip references the **project** skeleton and carries **no dependency on the vendor pack** — verify this, because a lingering vendor dependency means the clip breaks on a fresh clone and drags a gitignored pack into the manifest. The vendor pack stays gitignored and re-downloadable; only the curated retargeted clips are kept (`AGENTS.md` §Assets).
- **Different proportions need a real chain map and a check.** When source and target proportions differ (Mixamo, MetaHuman, a taller mocap actor), identity mapping is not enough — feet plant at the wrong height, hips float, the pose offsets. Author the chain map, set the retarget root and pelvis correctly, and **verify by playback**, not by a static pose.
- **Verify retargets in motion, animated.** Static editor pose capture is unreliable for single-node anim in this project's SceneCapture path (`EMOTE_PROVENANCE.md`) — a retarget is confirmed by *watching it play* on the target mesh, checking feet, hips, hands, and fingers, in PIE or a playback pass.

### 3. Control Rig — authoring and procedural pose
- **Control Rig for authored motion and runtime procedural adjustment.** It drives a rig from high-level controls both at author time (posing, keying) and at runtime (procedural foot placement, look-at, physics-driven secondary motion) inside the Anim Blueprint.
- **Backwards solve / bake between Control Rig and sequences.** Author or adjust on the control rig, bake to an AnimSequence for runtime where a baked clip is cheaper; use runtime Control Rig only where the procedural adjustment must respond to the world (terrain, aim, contact). Name the cost — runtime Control Rig is not free. `[verify — web pass]` for the project's runtime Control Rig budget.

### 4. IK — foot placement, hands, aim
- **Foot IK plants feet on terrain and stairs** so they don't float above or sink through uneven ground — the counterpart to fixing foot *sliding* (below). Drive it from ground traces feeding the leg IK, blended out when the foot is in flight.
- **Hand IK for contact** — hands on ladders, weapons, held props, wall contacts — so the hand meets the surface regardless of the base clip.
- **Aim / look-at** offsets orient the head/spine/weapon toward a target as an additive or procedural layer over the base locomotion.
- **Full-Body IK / two-bone IK** are the tools; the engine specifics and the current recommended node live in `guides/unreal-engine.md` `[verify — web pass]`. Author IK as a layer *over* good base motion, never as a substitute for it.

### 5. Anim Blueprints & state machines — the blend logic
The Anim Blueprint is where clips become continuous, input-driven motion; it is the deliverable that hands off to gameplay.

- **State machines model the character's motion states** — idle, locomotion, jump (start/loop/land), crouch, emote, montage-driven actions — with **transitions that blend, never snap**. Every transition has a named condition and a blend duration; an instant transition is a pop unless it's deliberate.
- **Blend times are feel.** Transition and blend durations are tuned by watching, and the numbers live in data where they can be iterated without a recompile — the same data-driven discipline `game-feel.md` demands of every feel number. Too short pops; too long feels mushy and unresponsive.
- **Event-driven, and cheap per frame.** The Anim Blueprint updates every frame on every visible character; keep the graph lean, prefer state/notify events over polling, and respect the frame budget (`game-feel.md` §per-frame budget). The engine facts about Anim Blueprint threading (the fast-path / multithreaded update, what may run off the game thread) live in `guides/unreal-engine.md` `[verify — web pass]` — do not restate them here; obey them.
- **Layered blend per bone** lets an upper-body action (aim, carry, wave) play over a lower-body locomotion without a second full clip — the standard way to multiply a motion set without multiplying clips.

### 6. Blend spaces — continuous motion from a few clips
- **Blend spaces interpolate a small set of clips across a continuous input** — a 1D speed axis (idle→walk→jog→run) or a 2D speed/direction (strafing locomotion) — so movement is smooth across the whole speed range from a handful of samples.
- **Sample at the speeds the movement component actually produces**, and match the clip's authored stride speed to the locomotion speed at that sample, or the feet slide (see §7). The blend space and the `CharacterMovementComponent` numbers (`game-feel.md`) are tuned *together*, not in isolation.

### 7. Root motion vs in-place — the decision that breaks movement or authority
This is the highest-consequence choice in the guide; getting it wrong causes both foot-sliding and networking bugs.

- **In-place + capsule-driven for looping locomotion.** Walk/run loops play in place; the `CharacterMovementComponent` moves the capsule; the animation is matched to that speed (via the blend space and, ideally, distance matching / foot-locking) so the feet appear to plant. This is the default for networked locomotion because the *movement* is authoritative capsule motion, not animation.
- **Root motion for discrete, motion-defining actions** — mantles, dodges, attacks with committed displacement, cinematic steps — where the *animation* must drive the exact world displacement. The clip carries root motion; the movement component consumes it.
- **Root motion over the network is a networking concern, not just an animation one.** Server authority over position must hold; root-motion montages that displace the character are replicated through the movement/montage system and pair with `network-engineer` and `guides/unreal-engine.md` `[verify — web pass]`. Never let a client's root-motion animation become the unchecked source of truth for position (`AGENTS.md`: never trust the client).
- **Foot sliding is a symptom of this decision plus stride mismatch.** Fix it at the source: match locomotion speed to authored stride, add distance matching / foot-locking, and confirm root-motion-vs-in-place is right for the clip — not by hiding it under motion blur.

### 8. Montages & additives — one-shot actions and layered nuance
- **Montages play one-shot actions** (emotes, attacks, interactions, mantles) over or instead of the base state, with **notifies** firing gameplay/audio/VFX events on exact frames and **blend-in/blend-out** curves that must be authored so the action enters and exits without a pop. A montage that snaps back to locomotion on its last frame is a blend-out defect.
- **Additive animations layer nuance** — breathing, lean, recoil, fatigue, aim sway — on top of a base pose without replacing it. Additives are **authored against, and applied over, the correct base pose**; an additive built on one base and applied to another distorts the character (a ref-pose leak's cousin). This is the discipline that prevents the T-pose/ref-pose additive bug.
- **Slots route montages into the Anim Blueprint** so a montage plays through a defined slot (full body, upper body) and blends with the state machine rather than fighting it.

### 9. Locomotion & the emote pipeline — the concrete deliverables
- **Locomotion set:** idle, walk, jog/run, start/stop, turn-in-place, jump (start/apex/loop/land), crouch variants as the design needs — assembled into a blend-space-driven state machine matched to the movement component's speeds, feet planted, transitions blended. This is the walkable-slice avatar's core and the first thing gameplay drives.
- **The emote pipeline is proven and is the template for reused motion.** Free Fab pack → 12 mocap emotes on UE5 Manny → IK-retarget (identity chain map) onto the project skeleton → self-contained curated clips (`AS_Emote_101…112`) → gitignore the vendor pack (`EMOTE_PROVENANCE.md`). Emotes are wired as montages through an emote slot; the crowd/presence channel plays them. **Open item carried from that work:** the clips are named opaquely and must be identified by an *animated* playback pass and renamed to gestures (`AS_Emote_Point`, `AS_Emote_Beckon`, …) — a live reminder that motion is identified in motion, not from a static pose.
- **Emotes are cosmetic and client-side where they carry no authoritative state** — route their feedback like any cue (`game-feel.md` §GAS cues); anything that *does* affect gameplay state goes through the authoritative path and to `security-reviewer`.

---

## QUALITY BAR
A motion set is ready to recommend when all of these hold — watched *in motion under input and gravity*, judged by a fresh pass (`qa-visual` for broken, `creative-review` for on-pitch), never self-signed:
- **Feet plant.** No sliding at any locomotion speed; foot IK holds on terrain and stairs; stride matches speed across the blend space.
- **No pops.** Every state transition and montage blend-in/out is smooth; no snap, no loop re-pose, no hitch when a montage ends.
- **Retargets are clean and self-contained.** Every reused clip is on the project skeleton, references no vendor pack, and plays correctly (feet, hips, hands, fingers) verified by *playback*.
- **Root motion is where it belongs.** Looping locomotion is in-place + capsule-driven; discrete displacing actions use root motion; server authority over position holds (paired with `network-engineer`).
- **No T-pose / ref-pose leaks.** Every state has a valid pose; every additive is applied over its correct base; no unreachable/empty state, no bind-pose flash on load or transition.
- **Within the frame budget.** The Anim Blueprint graph is lean, event-driven, obeys the threading rules in `guides/unreal-engine.md`, and introduces no hitch (`game-feel.md`).
- **Blends and timings are data-driven.** Transition/blend durations live in data and were tuned by watching, not hardcoded guesses.
- **Serves the feel.** Motion supports the responsiveness `game-feel.md` owns — animation reacts on the input frame (or the character predicts locally); a committed action reads as committed. Feel is judged felt, by someone who didn't build it.
- **Judged fresh.** `qa-visual` (in motion, multi-view) + `creative-review`; never straight to the owner.

---

## COMMON FAILURE MODES
- **Foot sliding.** Feet drift instead of planting. → Match authored stride to locomotion speed across the blend space; add distance matching / foot-locking and foot IK; confirm the root-motion-vs-in-place choice.
- **Popping / blend-snapping.** Visible snap between states or on a montage's end; loop re-pose. → Every transition gets a named condition *and* a tuned blend duration; author montage blend-in/out curves; sync loop points.
- **Bad retarget.** Stretched limbs, feet through floor, floating hips, frozen/exploded fingers on a reused clip. → Author a real chain map for differing proportions (not identity); set retarget root/pelvis; **verify by animated playback**, never a static pose; confirm the asset is self-contained on the project skeleton.
- **Missing / misplaced root motion.** Moonwalking on a clip that should drive movement; drift on an in-place clip carrying stray root motion. → Make the root-motion-vs-in-place decision per clip; in-place + capsule for locomotion, root motion for discrete displacement; keep the server authoritative over position.
- **T-pose / ref-pose leaks.** Bind-pose or ref-pose flash. → Every state has a valid pose; additives applied over their correct base; no empty/unreachable states; guard against failed async loads.
- **Retarget dependency on the vendor pack.** A "done" clip that breaks on a fresh clone. → Verify the retargeted asset references only the project skeleton and drags in no gitignored pack (the emote-pack lesson).
- **Motion identified from a static pose.** Guessing a clip's content from a thumbnail (the emote naming open-item). → Identify and verify all motion by *playback*; the SceneCapture static path is unreliable for single-node anim here.
- **Anim Blueprint tick-storm.** A heavy per-frame graph on every visible character hitching the frame. → Lean graph, event/notify-driven, obey the threading rules; measure with `stat` (`game-feel.md`).
- **Animation asserted, not watched.** "It looks right" from one preview. → Watched in motion, under input and gravity, multi-view, by a fresh reviewer.

---

## CHECKLIST
**Rig & retarget:**
- [ ] Rigged to the project Manny skeleton (bespoke skeleton justified, not defaulted); bind pose matches.
- [ ] Skin weights smooth at every joint, no stray influences, within max-influences limit.
- [ ] Every reused clip retargeted onto the project skeleton via IK Retargeter; chain map is identity only where hierarchies match, authored where proportions differ.
- [ ] Retargeted assets self-contained — reference the project skeleton only, no vendor-pack dependency; vendor pack left gitignored.
- [ ] Every retarget verified by **animated playback** (feet, hips, hands, fingers), never a static pose.

**Blend logic:**
- [ ] State machine covers the needed states; every transition has a named condition and a tuned blend duration (no unintended snaps).
- [ ] Blend spaces sampled at the speeds the movement component produces; stride matched to speed.
- [ ] Layered/per-bone blends and slots route upper-body and montage actions cleanly.
- [ ] Blend/transition timings live in data, tuned by watching.
- [ ] Anim Blueprint lean, event-driven, obeys `guides/unreal-engine.md` threading rules; `stat` clean, no hitch.

**Motion content:**
- [ ] Root-motion-vs-in-place decided per clip; locomotion in-place + capsule; discrete displacement via root motion; position stays server-authoritative (paired with `network-engineer`).
- [ ] Foot IK plants on terrain/stairs; hand IK/aim layered over good base motion, not substituting for it.
- [ ] Montage blend-in/out authored; notifies on correct frames; additives applied over their correct base pose.
- [ ] Locomotion set assembled and matched to feel; emotes wired as montages through the emote slot; emote clips identified by playback and renamed to gestures.
- [ ] No T-pose / ref-pose leak on any state, transition, or load.

**Before recommending:**
- [ ] Quality bar met — watched in motion, under input and gravity, multi-view.
- [ ] Compiled/loaded clean; new reflected types got a full build + restart (`game-feel.md`).
- [ ] Judged by a fresh reviewer (`qa-visual` broken / `creative-review` on-pitch; `qa-network` if root motion or emote state replicates); never self-approved, never straight to the owner.
- [ ] Handed to `gameplay-engineer` as a clean state machine with named entry conditions — not loose clips.

---

## Sources
Craft grounded in standard animation and UE practice; specific engine numbers and the current recommended nodes/settings are marked `[verify — web pass]` above and resolved in the researched pass.
- **UE IK Retargeter / `IKRetargetBatchOperation`** — the proven retarget path, evidenced in-project by `Content/ElseCity/Animations/Emotes/EMOTE_PROVENANCE.md` (identity chain map, lossless bake, self-contained assets).
- **UE Control Rig, Foot IK / Full-Body IK, Anim Blueprint state machines, blend spaces, montages, additives, root motion** — Epic documentation, to be cited in the web pass. `[verify — web pass]`
- **Root motion over the network** — Epic replication/movement docs. `[verify — web pass]`
- Cross-references (not duplicated here): `guides/game-feel.md` (responsiveness, latency budget, the feel a motion serves; GAS cues), `guides/character-art.md` (the rig-ready mesh and skeleton contract upstream), `guides/unreal-engine.md` (skeleton, Anim Blueprint threading, Iris, root-motion-over-network engine facts), `guides/networking.md` (remote-proxy interpolation of other players' motion), `AGENTS.md` §Assets (retarget curation, gitignore, never-trust-the-client).
