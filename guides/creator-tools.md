# Guide — In-game creator tooling (player-facing UGC) method

> Read before designing any part of the player's world-building editor. The core idea: **this is the pitch — "every door leads somewhere else" means players build the somewhere-elses, so the creator tool is not a feature, it is the product.** It succeeds only when an ordinary player can build something they're proud of within minutes, everything they build is **data, not code**, every primitive is **whitelisted and budget-capped**, and nothing a creator makes can harm another player. It is done only when it is learnable, expressive within safe bounds, performant at scale, and its abuse surface is understood and handed to trust & safety.

## What this role owns, and the critical distinction
This role owns the **player-facing** creation experience: the in-game world-building editor, the palette of what players can place and do, the creation UX, the data model UGC compiles to, and the safety envelope around it. It is **distinct from `tools-programmer`**, which owns the *agent's / developer's* editor tooling (approved automation and editor integrations). One builds tools for the team; this builds tools for the player. They share nothing but the word "tools."

It defers:
- **The economy and progression** built *on* creation (what creating earns, how it's monetized, power-gating) — `game-designer` (`guides/game-design.md`). This role owns *what can be built*; game design owns *what building is worth*.
- **The on-screen UI of the editor** — layout, hierarchy, gamepad support, readability — is co-owned with `ui-ux-designer` (`guides/ui-ux.md`). This role owns the *creation model and affordances*; UI owns *how they're presented and operated*.
- **The authoritative networking and persistence** of placed content — `network-engineer` (`guides/networking.md`). Placement is a client-reachable, server-authoritative action.
- **Moderation and trust & safety** of what's created — a separate discipline this role *hands the abuse surface to*, not one it owns (see below).

## The two failures this prevents
1. **UGC as code — the security catastrophe.** Letting players ship *behaviour* (scripts, arbitrary logic, uncapped anything) into a shared, all-ages, persistent world. That is a remote-code-execution and abuse surface of the worst kind. The rule is absolute and settled: **UGC is data, not code. Whitelisted, budget-capped primitives. No user scripting at launch.** A creator assembles from a safe palette; they never author logic that runs on anyone else's machine or the server. Everything the tool exposes is a *parameter on a known-safe primitive*, validated server-side.
2. **A creator tool only a developer could love.** A powerful editor so complex, so unguided, or so unforgiving that an ordinary player bounces off it — so the "everyone creates" pitch is true only for the few. If the median player can't make something they like quickly, the product's core promise fails regardless of how deep the tool is. Accessible-first, depth-behind-it.

## "Data not code" does not mean safe
A critical, non-obvious truth carried from the project doctrine: **"data, not code" removes the code-execution surface, not the abuse surface.** Malicious *geometry and data* are a real attack vector even with zero scripting:
- **Malicious geometry** — shapes built to grief: performance bombs (millions of primitives, degenerate meshes), collision traps (invisible walls, inescapable boxes around a spawn), sightline blockers, or geometry arranged to render offensive imagery.
- **Malicious arrangement** — safe primitives composed into hateful symbols, slurs spelled in blocks, harassing scenes — no single primitive is unsafe, the *composition* is.
- **Resource abuse** — content authored to blow memory, streaming, or bandwidth budgets and degrade the space for everyone in it.
Every one of these is possible with pure data and a whitelisted palette. **Budget caps and validation are the primary defence; moderation is the backstop.** This is why the abuse surface is handed to trust & safety as a first-class concern, not treated as solved by "it's only data."

## PRINCIPLES
- **The creator tool is the product.** Design it with the seriousness of the core loop, because it *is* the core loop. Every decision is measured against "does this help an ordinary player build a somewhere-else they're proud of."
- **Data, not code — no exceptions at launch.** The player composes from a **whitelisted palette of primitives**, each with **bounded, validated parameters**. No user scripting, no arbitrary logic, no behaviour that executes on another machine. Every creation serializes to *data* the engine interprets, never *code* the engine runs. Any future scripting is a post-launch, sandboxed, owner-reserved decision — not a launch capability.
- **Budget-capped, always.** Every primitive, every zone, every creator has hard **budgets** (primitive count, triangle/memory/draw-call ceilings, collision-body limits, texture/material limits) enforced server-side at author time — not discovered when the space chugs. Budgets live in **data tables, not code** (mirrors the fairness rule, `guides/game-design.md`), so they're tunable without a build. Over-budget content is *refused at authoring*, with a clear reason to the creator.
- **Whitelist, never blacklist.** The palette is an *allow*-list of known-safe primitives and parameters; anything not explicitly allowed is forbidden. A blacklist ("everything except…") always leaks. New primitives are *added* to the whitelist deliberately, each vetted for its abuse potential before it ships.
- **Server-authoritative and validated at the boundary.** Placement, edit, and publish are client-reachable actions → every one is server-authoritative and validated, each check naming the exploit it prevents (doctrine 11, `guides/networking.md`, → `security-reviewer`). Never trust the client's claim about what it placed, where, at what cost, or that it was within budget. The client is a convenience; the server is the truth.
- **Accessible-first, depth-behind-it.** The first five minutes must produce something the median player likes; mastery is optional depth layered on top, never a prerequisite. Progressive disclosure, sensible defaults, forgiving edits (undo, non-destructive), immediate feedback (`guides/ui-ux.md`).
- **Abuse is a design input, not an afterthought.** For every capability, ask *how is this griefed, and can a player harm another with it* before it ships — and hand the answer to trust & safety. Budget caps, validation, and moderation hooks are designed *in*, the same way security is (doctrine 11).
- **Safe by default, per district.** Creation happens in spaces behind doors (their own maps/instances, `guides/networking.md`); the safety register of a space governs what creation and content is permitted there. All-ages spaces carry stricter content bounds; mature content sits behind age-gating. Creation never lets content escape its space's safety contract.
- **Prove it in a spike.** The creator tool is a P1 spike (below); its data model, palette, and safety envelope are proven in isolation and reviewed before the main build depends on them — because that data model constrains backend, moderation, and the economy downstream (doctrine 3).

---

## The data model — what UGC compiles to
The single most consequential artifact this role produces, because everything downstream (persistence, replication, moderation, economy) is shaped by it:
- **A serializable description of a creation as data** — a list of whitelisted primitive instances, each with validated transform and bounded parameters, plus space-level metadata (budgets consumed, safety register, ownership). No embedded logic, no references to arbitrary assets, no code.
- **Versioned and migratable** — the format will evolve; design it so existing creations survive a format change (mirrors the backend save-format concern, `guides/production-pipeline.md §3.5`). Coordinate the schema with backend/online-services early — a late change forces a data migration of everyone's creations.
- **Bounded references only** — a creation references whitelisted assets by safe ID, never a path or a blob a client supplies; the server resolves and validates every reference.
- **Cheap to validate** — the format is structured so the server can cheaply confirm budget compliance and whitelist compliance on publish, without executing anything.

## The palette — whitelisted, budget-capped primitives
- **A curated set of building blocks** — geometry primitives, pre-approved props (from `Content/ElseCity`, ingested per `guides/environment-art.md` / tech-art), materials/colours from a safe range, placeable interactive elements (doors, lights, spawn points) with fixed, safe behaviour.
- **Each primitive carries its own budget cost and abuse vetting.** A primitive is added to the whitelist only after: its cost is known (counts against creator/zone budgets), its parameters are bounded (no "scale to infinity", no degenerate values), and its griefing potential is assessed. New primitives are a deliberate, reviewed addition — never an open door.
- **Interactive primitives have fixed, safe behaviour** — a "door" does the one safe thing a door does; the creator parameterises it (where it leads, within allowed destinations), they do not script it. This is how expressiveness is delivered *without* code.

## The creation UX — learnable, expressive, forgiving
Co-owned with `ui-ux-designer`:
- **Minutes to a first result** — a guided first creation, strong defaults, a small starting palette that grows as the player learns. Onboarding is part of the tool, not separate from it.
- **Non-destructive and forgiving** — undo/redo, move-don't-commit, no way to irrecoverably ruin a creation. Fear of mistakes kills creativity.
- **Immediate, honest feedback** — the creator sees cost against budget live (so a budget refusal is never a surprise), sees what's placed clearly, and gets a clear reason when an action is refused (over budget, not whitelisted, not permitted here).
- **Gamepad and accessibility from the start** — the editor is operable without a mouse-and-keyboard assumption (`guides/ui-ux.md`); a creation tool that excludes controller players excludes most of the audience.

## The abuse surface — handed to trust & safety
This role *identifies and bounds* the abuse surface; **trust & safety (a separate discipline, activating P1 policy · P2 tooling per `guides/production-pipeline.md §3.5`) owns moderating it.** The handoff is explicit:
- **Enumerate the abuse vectors** for every capability (performance bombs, collision traps, offensive geometry/arrangement, resource abuse, harassment via placed content) and document them as a living record for trust & safety.
- **Design moderation hooks in** — the data model and the systems must support reporting, review, takedown, rollback, and creator sanction *from the start*; retrofitting moderation onto content already shipped is far costlier (the doctrine's long-lead warning). A creation must be inspectable and removable by moderators.
- **Budget caps and validation as first-line defence; moderation as backstop.** The technical envelope stops most abuse cheaply; moderation handles what composition-of-safe-parts enables. Both are required — neither alone suffices.
- **Age/safety register enforcement** — creation respects the space's safety contract; all-ages bounds are stricter; mature content is gated. This role builds the enforcement; trust & safety sets the policy.

## Engine & pipeline facts live elsewhere
Anything about *how* UE serializes, streams, or replicates player-built content — the persistence format on disk, replication of placed actors under Iris, streaming zones behind doors as their own instances, runtime mesh/geometry generation, asset reference resolution — belongs in `guides/unreal-engine.md` (engine mechanics, verified via `engine-verifier`) or `guides/networking.md` (authority/replication/persistence). Do not duplicate them here. Asset ingest and budget classes for palette content are `tech-artist` / `guides/environment-art.md`. `[verify — web pass: UE 5.x runtime-safe geometry/primitive systems suitable for player building — Geometry Script, runtime mesh, modular primitive placement — and their server-authoritative viability]`

## Phase activation
Per `guides/production-pipeline.md §3.5`, in-game UGC / creator tooling **activates P1 (spike) · P2 (build)** and is flagged critical: *"It **is** the pitch. Its data model constrains backend, moderation, and the economy — a late spike risks building systems it can't plug into."* The P1 spike must prove the data model, the palette-and-budget concept, and the safety envelope in isolation, reviewed and backported to the vault, *before* backend/moderation/economy build on it. It heads a dependency chain into moderation (`UGC creates the moderation surface`, §3.3) — so trust & safety's policy work runs alongside from P1.

## QUALITY BAR
Creator-tool work is ready to recommend when all of these hold — judged fresh (`security-reviewer` for the abuse boundary, `qa-network` for authority, `creative-review` for on-pitch, playtesting for learnability), never self-signed:
- **An ordinary player builds something they like in minutes** — the pitch's promise verified with real (non-developer) players, not asserted.
- **Data, not code — provably.** No user scripting, no arbitrary logic, no client-supplied behaviour executes anywhere; every creation is validated data against a whitelist.
- **Whitelisted and budget-capped.** Palette is an allow-list; every primitive/zone/creator has enforced budgets (count, tris, memory, draw calls, collision) in data tables; over-budget content refused at authoring with a clear reason.
- **Server-authoritative and validated.** Every placement/edit/publish is server-validated; each check names the exploit; the client is never trusted for cost, position, whitelist, or budget compliance (`security-reviewer` clean).
- **Abuse surface understood and handed off.** Vectors (performance bombs, collision traps, offensive geometry/arrangement, resource abuse, harassment) enumerated; moderation hooks (report/review/takedown/rollback/sanction) designed in; documented for trust & safety.
- **Safety-register-correct.** Creation respects each space's safety contract; all-ages bounds stricter; mature content gated; no content escapes its space.
- **Data model stable and coordinated.** Serializable, versioned, migratable; schema agreed with backend/online-services; downstream (moderation, economy) can plug in.
- **Accessible.** Learnable with progressive disclosure, forgiving (undo/non-destructive), immediate cost feedback, gamepad + accessibility support.

## COMMON FAILURE MODES
- **UGC as code.** Any path to user scripting or arbitrary behaviour in a shared all-ages world — the RCE/abuse catastrophe. → data not code, whitelisted primitives, no scripting at launch, no exceptions.
- **"It's only data, so it's safe."** Treating budget/moderation as unnecessary because there's no code. → data-not-code removes code-exec, not abuse; budget caps + validation + moderation all required.
- **Blacklist thinking.** "Allow everything except…" — always leaks. → whitelist; anything not explicitly allowed is forbidden; new primitives vetted before adding.
- **No budget enforcement.** Uncapped placement discovered when a zone chugs or blows memory/bandwidth. → hard budgets in data tables, enforced server-side at authoring, refused over-budget.
- **Client trusted.** Server accepts the client's claim of what/where/cost. → server-authoritative validation of every author action; `security-reviewer`.
- **Developer-only tool.** Powerful but unlearnable; the "everyone creates" pitch true only for the few. → accessible-first, minutes to a first result, playtested with real players.
- **Moderation retrofitted.** Report/takedown/rollback bolted on after content ships. → moderation hooks designed into the data model and systems from P1; handed to trust & safety.
- **Late/unstable data model.** Schema changed after backend/economy built on it, forcing a migration of everyone's creations. → prove and stabilise the model in the P1 spike; coordinate with backend early; version and migrate.

## CHECKLIST
**Before building (P1 spike):**
- [ ] The data-model schema drafted (serializable, versioned, whitelisted references, no logic) and reviewed with backend/online-services.
- [ ] The initial palette defined as a whitelist, each primitive with its budget cost and bounded parameters.
- [ ] Budget model defined (per primitive / zone / creator) and located in data tables, not code.
- [ ] The abuse-vector enumeration drafted and shared with trust & safety; moderation-hook requirements identified.
- [ ] Onboarding / first-five-minutes flow designed with `ui-ux-designer`.
- [ ] Spiked in isolation; data model + palette + safety envelope proven and backported to the vault before the main build depends on them (doctrine 3).

**During building:**
- [ ] No path to user scripting or client-supplied behaviour anywhere; every creation is validated data.
- [ ] Palette is an allow-list; each primitive vetted for abuse before it's added; interactive primitives have fixed safe behaviour, parameterised not scripted.
- [ ] Every placement/edit/publish server-authoritative and validated; each check names the exploit (`security-reviewer`, `network-engineer`).
- [ ] Budgets enforced at authoring; over-budget refused with a clear reason; live cost-vs-budget feedback in the UX.
- [ ] Moderation hooks (inspect/report/takedown/rollback/sanction) present in the data model and systems.
- [ ] Safety register enforced per space; all-ages bounds stricter; mature content gated.
- [ ] Non-destructive editing (undo/redo), forgiving, gamepad + accessibility support (`ui-ux-designer`).

**Before recommending done:**
- [ ] Quality bar met.
- [ ] Abuse surface documented and formally handed to trust & safety; data model confirmed stable with backend.
- [ ] Any engine-behaviour claim (runtime geometry, serialization, replication) verified via `engine-verifier`.
- [ ] Authority verified by `qa-network`; abuse boundary audited by `security-reviewer` (each check names its exploit).
- [ ] Learnability verified by playtesting with real (non-developer) players — the pitch's promise, not asserted.
- [ ] Judged fresh by `creative-review` (on-pitch — is this the "every door leads somewhere else" promise) — never self-run.
- [ ] One-line done recommendation to the Producer — never a self-sign-off.

## Sources
Craft grounded in UGC-platform and creation-tool practice — pin exact references in the web pass:
- **UGC platform design & safety** — the Roblox / Fortnite Creative / Dreams / LittleBigPlanet body of practice on player creation, whitelisted palettes, and moderating user content at scale. `[verify — web pass: pin canonical talks/postmortems — Roblox creation & moderation, Media Molecule Dreams tooling, Fortnite Creative/UEFN safety model]`
- **"Data not code" / capability-sandboxing** — the security principle behind refusing user scripting; the abuse-surface analysis of pure-data UGC. `[verify — web pass]`
- **Creation-tool UX** — accessibility, progressive disclosure, and forgiving editing in player-facing editors. `[verify — web pass]`
- The economy/progression built on creation lives in `guides/game-design.md`; the editor UI in `guides/ui-ux.md`; authority/persistence/replication in `guides/networking.md`; asset ingest & budget classes in `guides/environment-art.md`; engine mechanics in `guides/unreal-engine.md`. Moderation of created content is a separate discipline (trust & safety) this role hands the abuse surface to.
