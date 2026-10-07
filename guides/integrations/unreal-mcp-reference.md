# Optional Unreal MCP integration reference

This preserves a prior environment-specific tool survey. It is not a required studio dependency, a current capability promise or an installation instruction. Dated MEASURED labels belong to that surveyed environment only; validate versions, schemas and behaviour locally. The portable routing and ownership rules in ../tooling-ue.md take precedence. In particular, do not assume all concurrency deadlocks, that Launcher builds cannot package, or that a position setter proves real movement input. Host computer-control restrictions and user choices take precedence over any historical workaround below.

# Guide — Driving Unreal Engine

> Read this before any editor work. It defines **which tool surface to use for which job**, the **full-editor-access capability map**, and the **gaps we are closing**. Specific engine-behaviour claims here are marked `[verify]` — confirm against engine source (`agents/engine-verifier`) before relying on them; this framework starts from a clean slate and inherits no unverified "facts".

## The three surfaces — and the one rule

We drive the editor through three surfaces. Naming is deliberate; use the right name so it is always clear what is being called.

| Surface | What it is | Call it | Best for |
|---|---|---|---|
| **Unreal's MCP** | Epic's in-engine `ModelContextProtocol` server + `AllToolsets` (SceneTools, ObjectTools, EditorAppToolset, DataTableTools, Blueprint tools, …) | the MCP client tools (`list_toolsets` / `describe_toolset` / `call_tool`) | Standard editor operations Epic already covers well — placing/querying actors, properties, assets, Blueprints, config. |
| **Remote Control** | Epic's `RemoteControl` plugin, HTTP on `localhost:30010` — runs **arbitrary game-thread Python** and **console commands** | `curl` → `KismetSystemLibrary.ExecuteConsoleCommand` → `py "<script>"` | The long tail: anything no toolset exposes, batch scripts, console commands. The full editor Python API on the game thread. |
| **Our toolkit** (`ue-mcp-toolkit`) | *Our* plugin, registering custom toolsets into Unreal's MCP server. Six toolsets, all verified callable and returning structured JSON `[MEASURED: 2026-07-21]`: `GeometryAuditTools`, `ContentAuditTools`, `CaptureTools`, `NetworkHarnessTools`, `BlockoutTools` (Python, hot-registered) + `BrowserToolset` (C++). | same MCP client tools | The **gaps** and the **reliable, structured, high-level** operations we own. |

**THE ROUTING RULE:**
> **Unreal's MCP for what it does well · Remote Control for the long tail · our toolkit for the gaps and anything we need reliable and structured.**

And the ambition: **we strive for full, first-class editor access.** When a job recurs and the raw route is fiddly or fragile, that is the signal — the **Tools Programmer** (`agents/tools-programmer`) builds a first-class toolkit tool for it, with a structured return, and this guide's capability map gains a row. Leave no rock unturned; close every gap we hit.

> ⚠️ **We ride Epic's MCP server; we do not fork or replace it.** Epic's plugin ships in-engine (experimental, NoRedist). We *extend* it by registering toolsets via the public `ToolsetRegistry`, and we *configure* it (`.ini`). A standalone server would just re-implement transport Epic gives us free.

---

## The capability map — full editor access, by job

What we can do, which surface does it, and where the gap is. This is the **target state**; rows marked ⧗ are toolkit work not yet built.

| Job | Surface / how | Status |
|---|---|---|
| **Place / move / duplicate / query actors** | Unreal MCP — `SceneTools`, `ObjectTools` | ✅ |
| **Read/write actor & asset properties** | Unreal MCP — `ObjectTools` (public props); Remote Control `py` (anything editable) | ✅ |
| **Read *reflection-flag-gated* `UPROPERTY`s** (WP grid, engine internals) | our toolkit — C++ tool (`FindFProperty` + `ContainerPtrToValuePtr` ignores the `CPF_Edit \| CPF_BlueprintVisible` flag gate every Python route enforces — see `guides/unreal-engine.md` §10; it is NOT the C++ `protected`/`private` keyword) | ⧗ build |
| **Author Blueprints / Materials / DataTables / Niagara / Sequencer** | Unreal MCP — the respective toolsets | ✅ |
| **Arbitrary editor Python (game thread)** | Remote Control → `py "<path>"`; log results, read via logs | ✅ |
| **Console commands / cvars** | Remote Control → `ExecuteConsoleCommand` | ✅ |
| **Geometry truth** — true rendered base, seating, interpenetration. `measure_true_base` measures a PLA/ISM from instance transforms (its `get_actor_bounds` *lies*) and a plain StaticMeshComponent from the component's world-space bounds; an actor with neither is reported in `skipped`, never silently seated | our toolkit — `GeometryAuditTools.measure_true_base` / `sweep_interpenetration` | ✅ |
| **Content / asset audit** — mesh-path provenance, dependency closure, dangling refs | our toolkit — `ContentAuditTools` | ✅ |
| **Per-LOD tri/vert counts, LOD count, Nanite state, LOD thresholds, mesh bounds** | Unreal MCP — `StaticMeshTools` (`get_triangle_count`/`get_vertex_count` per `lod_index`, `get_lod_count`, `is_nanite_enabled`, `get_lod_thresholds`, `get_bounds`) | ✅ (Epic-covered — **not** a toolkit gap; only UV-channel count + per-LOD resource-memory bytes remain unreflected) |
| **Screenshots / views** (top-down, elevation, eye-level, silhouette) | our toolkit — `CaptureTools.capture_view` (single view) / `capture_battery` (canonical set in one call). Wraps a transient `ASceneCapture2D` → render target → PNG, on the game thread. **True orthographic** projection for plan/elevation; auto-frames a `target_filter` (or the whole level); manual exposure; cold-start priming; temporary legibility lighting on unlit levels — legibility only, **not** a QA-of-record basis: a visual verdict rests on lighting *saved* in the level (`guides/workflow.md`), because this transient rig makes an unlit level shootable while it still renders black in a real viewport. Returns the PNG path + the fully-resolved camera pose so a later pass re-shoots identically. All the requirements below are baked in and `[MEASURED: 2026-07-21]`: cold-start prime (first render is black — `prime_frames` capture passes); sun+key/fill+skylight added if the level has none (empty levels render black; a single sun crushes the camera-facing faces of an elevation to black); **orthographic for plan & elevation** (perspective foreshortening reads as false tilt/rotation to a reviewer — proven: an ortho image is pixel-identical across camera distances, diff 0.0, perspective is not); **manual exposure**; canonical battery (`top`+4 elevations ortho + `iso` perspective) in one call | ✅ |
| **Design & build levels** | plan/metrics/elevation spec (`agents/level-designer`) → build via Unreal MCP + Remote Control, seated by geometry-truth tools | ✅ (method) |
| **Build a whitebox blockout FAST** — author massing as data, build/rebuild in one pass | our toolkit — `BlockoutTools.build_blockout` reads a JSON massing definition (`Tools/blockout/*.blockout.json`) and spawns every solid mass in one batched game-thread call. Idempotent (tag `blockout:<id>`, clear-and-rebuild → no duplicates), metric→cm, exact seating by construction, per-mass outliner folder/collision/tag. A layout change is "edit the data, re-run". `[MEASURED: 2026-07-21 — 33-mass Neon Hub massing built in ~0.25 s; edit-and-rebuild clears 33 / spawns 33, no dupes]` | ✅ |
| **Play & test — PIE / dedicated server + clients** | our toolkit — `NetworkHarnessTools`: `begin_session` (records+sets the net-mode CDO, starts PIE server+N clients in one process) → `get_session_state` (per-world server/client + pawns) → `drive_pawn` / `assert_pawn_at` / `assert_pawns_consistent` → `end_session` (restores CDO). Stateful multi-call: PIE ticks *between* calls, so one blocking call can't drive it. Structured JSON pass/fail from all parties | ✅ (verified 2026-07-21 — server + 2 clients, replication asserted from all three, negative test discriminates, Iris confirmed on the net driver) |
| **Automated playtest input** — walk a route, trigger a door | our toolkit — `NetworkHarnessTools.drive_pawn` (server-authoritative `set_actor_location` on the chosen pawn; replicates to all clients within a few ticks). Enough to position bodies and prove door/zone transitions; true simulated *input* (analog movement/keys) is still fiddly and unbuilt | ✅ (positioning) · ⧗ (input sim) |
| **Human playtest — out-of-process `-server` + clients** (T-HOST) | our toolkit — `Tools/host/run_server.ps1` / `run_client.ps1` / `stop_server.ps1`. `UnrealEditor.exe -server` is a genuine out-of-process dedicated server on a Launcher build (no server target needed); teardown by captured PID, **never** `taskkill /IM`. For the V5 moderated feel-proof, not automated assertions | ✅ (server boot verified 2026-07-21 — dedicated world, Iris, listening on port; client-connect documented, first real use is qa-network/V5) |
| **Perf capture** — frame/CPU/GPU times | Remote Control `stat` cvars off a PIE/`-server` run → parse | ⧗ tool |
| **Acquire assets — Fab (free)** | our toolkit — `BrowserToolset` drives the Fab panel's embedded browser (`ExecuteJavascript`). Research exact listings first via Playwright MCP | ✅ |
| **Generate assets** — props (Meshy-class), and **sound effects & music** | driven through authenticated web tools via **Playwright MCP** + `.env.services` creds (never printed). Sound/music: ElevenLabs. Ingest → `Content/<Project>/`, wire client-side | ✅ (method) |
| **Ingest assets** — measure, collision, budget class, provenance, curate into the project content root | `agents/tech-artist` (`ingest-asset` method) + `ContentAuditTools` | ✅ |
| **Compile C++** | `LiveCodingToolset.CompileLiveCoding` (function bodies); full `Build.bat` + editor restart for new `UFUNCTION`/`UPROPERTY`/classes | ✅ |
| **Config / project settings** | Unreal MCP `ConfigSettingsToolset`; some pages are `.ini`-only (edit + restart) `[verify]` | ✅ |
| **Cook / package / build lighting / build HLOD** | limited on a Launcher build; needs a source-built engine | ⛔ gap (engine) |

**When you request rather than build:** if an asset (mesh, sound, music) is needed and not acquirable free/automatically, or a capability needs the source-built engine, **surface the request to the owner** — never silently work around it or fake it (doctrine 6).

---

## The surveyed surface — every registered toolset `[MEASURED: 2026-07-21]`

Not "treat missing as unknown" any more — this is the full `list_toolsets` enumeration, surveyed live. **59 toolsets register:** 53 from Epic's `AllToolsets`, plus our 6. Call each by its **fully-qualified** registered name (the prefix shown), never the short form.

**Epic — authoring:** `editor_toolset.*` — `SceneTools`, `ActorTools`, `ObjectTools`, `PrimitiveTools`, `AssetTools`, `BlueprintTools`, `StaticMeshTools`, `SkeletalMeshTools`, `MaterialTools`, `MaterialInstanceTools`, `TextureTools`, `DataTableTools`, `CurveTableTools`, `DataAssetTools`, `StringTableTools`, `ProgrammaticToolset` · `UMGToolSet` · `PCGToolset.{PCGToolset,PCGSpatialToolset}` · `PhysicsToolsets.PhysicsAssetToolset` · `NiagaraToolsets.{_Info,_Component,_Blueprint,_System,_Assets}` (5).

**Epic — animation/cinematics:** `animation_toolset.*` — `ControlRigTools`, `SequencerTools`, `SequencerKeyframingTools`, `SequencerControlRigTools`, `SequencerOutlinerTools`, `SequencerConditionTools`, `SequencerCustomBindingTools`, `SequencerImportExportTools` (8).

**Epic — gameplay/AI/systems:** `GASToolsets.{GameplayCueToolset,AttributeSetToolset,AbilitySystemInspectorToolset}` (3) · `GameplayTagsToolset` · `aimodule_toolset.toolsets.behavior_tree.BehaviorTreeTools` · `state_tree_toolset.toolsets.state_tree.StateTreeTools` · `WorldConditionsToolset.WorldConditionTools` · `conversation_toolset.toolsets.conversation.ConversationTools` · `DataRegistryToolset.DataRegistryTools`.

**Epic — editor/infra:** `EditorToolset.{EditorAppToolset,LogsToolset}` · `ConfigSettingsToolset` · `LiveCodingToolset` · `PluginToolset` · `GameFeaturesToolset` · `AutomationTestToolset` · `SlateInspectorToolset` · `SemanticSearchToolset` · `ToolsetRegistry.AgentSkillToolset` · `DataflowAgent.DataflowAgentToolset`.

**Ours (`ue-mcp-toolkit`) — all verified callable this survey:** `ue_mcp_toolkit.toolsets.{geometry.GeometryAuditTools, content.ContentAuditTools, capture.CaptureTools, network_harness.NetworkHarnessTools, blockout.BlockoutTools}` (Python) · `UeMcpToolkitEditor.BrowserToolset` (C++). Read-only smoke calls all returned structured JSON (GeometryAudit `measure_true_base`, ContentAudit `audit_mesh_paths`, Capture `capture_view` iso PNG, NetworkHarness `get_session_state` = no-session, Blockout `clear_blockout` = 0 cleared, Browser `ListBrowsers` = `[]`). The Remote Control long-tail route (`:30010` → `py` → `unreal.log` → `LogsToolset.GetLogEntries`) round-trips on the game thread `[MEASURED: 2026-07-21]`.

### Every discipline knows what it drives

| Discipline | Primary toolsets |
|---|---|
| **animator** | `ControlRigTools` · `SequencerControlRigTools` · `SequencerImportExportTools` (FBX/AnimSequence in-out) · `SkeletalMeshTools` (bones/sockets) · Anim BP graphs via `BlueprintTools` |
| **vfx-artist** | the 5 `NiagaraToolsets` (`_System` is primary; `_Assets` to discover modules, `_Component` for runtime overrides, `_Blueprint` to wrap as actors) · `MaterialTools` (FX materials) |
| **cinematics** | the 8 `animation_toolset` Sequencer toolsets (`SequencerTools` core → keyframing/controlrig/outliner/conditions/custom_bindings/import_export) · `EditorAppToolset` (viewport camera) · `CaptureTools` (stills) |
| **ui-ux-designer** | `UMGToolSet` **with the mandatory `ObjectTools.list_properties`→`get`→`set` workflow** (guessed property names fail silently) · `StringTableTools` · `DataTableTools` |
| **gameplay-engineer** | `BlueprintTools` · GAS ×3 (`GameplayCueToolset`/`AttributeSetToolset`/`AbilitySystemInspectorToolset`) · `GameplayTagsToolset` · `WorldConditionTools` · `LiveCodingToolset` (function-body recompile) · `ObjectTools` |
| **network-engineer** | our `NetworkHarnessTools` (PIE server+clients, replication assert) · `LiveCodingToolset` · `ObjectTools`/`BlueprintTools` · RC console for `net.Iris.*` cvars. Static replication-coverage audit is roadmap **R2** (gap) |
| **level-designer** | `SceneTools` · `ActorTools` · `PrimitiveTools` · `ObjectTools` · our `BlockoutTools` (data-driven whitebox) · our `GeometryAuditTools` (seating truth) · our `CaptureTools` (plan/elevation battery). WP grid knobs are roadmap **A2** (gap) |
| **environment-artist** | `SceneTools` · `StaticMeshTools` · `MaterialInstanceTools` · `PCGToolset`/`PCGSpatialToolset` · `TextureTools` · our `GeometryAuditTools` + `ContentAuditTools` · Fab via our `BrowserToolset` |
| **lighting-artist** | `SceneTools` (place lights) · `ObjectTools` (light/post-process/exposure props) · `EditorAppToolset` (lighting cvars) · `ConfigSettingsToolset` · our `CaptureTools` (manual-exposure capture; luminance analysis is roadmap **R1**) |
| **character-artist** | `SkeletalMeshTools` · `StaticMeshTools` · `MaterialInstanceTools` · `TextureTools` · `PhysicsAssetToolset` · `AssetTools`/`StaticMeshTools.import_file` |
| **ai-engineer** | `BehaviorTreeTools` · `StateTreeTools` · `WorldConditionTools` · `SceneTools` (nav volumes). Navmesh **build** is roadmap **A5** (gap — no build toolset registers) |
| **tech-artist** | `StaticMeshTools` (LOD/collision/Nanite + per-LOD `get_triangle_count`/`get_vertex_count`) · `MaterialTools`/`MaterialInstanceTools` · `PCGToolset` ×2 · `TextureTools` · `PhysicsAssetToolset` · `AssetTools` · our `GeometryAuditTools` + `ContentAuditTools` |
| **qa-visual** | our `CaptureTools` (battery) + `GeometryAuditTools` (floating/interpenetration) · `EditorAppToolset`/`SceneTools` (camera) |
| **qa-network** | our `NetworkHarnessTools` (all parties) · `EditorAppToolset` (PIE control) |
| **qa-functional** | `AutomationTestToolset` (`DiscoverTests`→`RunTestsByFilter`→`GetTestResults`, structured pass/fail) · `BlueprintTools` · `ObjectTools` |
| **performance-engineer** | `StaticMeshTools` counts · our `ContentAuditTools` (closure size) · RC `stat` cvars. Structured frame-timing capture is roadmap **A3** (gap — no perf toolset registers) |
| **build-engineer** | `LiveCodingToolset` · `PluginToolset` · `GameFeaturesToolset` · `ConfigSettingsToolset` · `AutomationTestToolset` (validation) |
| **game-designer / economy** | `DataTableTools` · `CurveTableTools` · `DataAssetTools` · `DataRegistryTools` |
| **narrative-designer** | `conversation_toolset` `ConversationTools` (dialogue graphs) · `StringTableTools` |
| **tools-programmer** (us) | `AgentSkillToolset` · `PluginToolset` · `LiveCodingToolset` · `ProgrammaticToolset` · `SlateInspectorToolset` · all of ours |

---

## Hard rules for the editor (operational — `[verify]` the engine specifics)

- **Work on a branch.** Never commit editor-automation output to the game's main branch; never push/merge unless asked.
- **MCP calls run on the game thread — serial, never parallel.** Concurrent calls deadlock. One at a time. Parallelise only *read-only* agents (reviews, audits, research); serialise every editor mutation.
- **Save, then verify the SAVED state.** MCP edits are often not undoable across compilation. A capture or check must read the committed+saved level, not an in-memory hope.
- **To save level edits, use `AssetTools.save_assets([])` (empty list = all dirty packages), NOT `SceneTools.save_actor`** `[MEASURED: 2026-07-22]`. On a World-Partition / OFPA level, `save_actor` fails on an existing external actor with a spurious `Asset does not exist: /Game/__ExternalActors__/...` — it validates the external-actor package path in a way that rejects the very actor it is asked to save. `save_assets([])` correctly writes the level and every dirty external actor (verified on disk: the edited actor's `__ExternalActors__` `.uasset` showed Modified and a newly-spawned actor's package appeared). Then confirm the SAVED state by `load_level` (reload from disk) and re-measuring.
- **⚠️ A package is only written if it is DIRTY — and a Python `set_actor_location`/`set_actor_rotation` does NOT dirty an OFPA actor's external package** `[MEASURED: 2026-07-22]`. Moving/rotating an existing external actor via `EditorActorSubsystem` changes it in memory (captures show the new pose) but leaves its `__ExternalActors__/.../*.uasset` **clean**, so `save_assets([])` / `save_current_level` return `true` and silently write only the `.umap` — the moved actor's real transform is never persisted. This is the save-saga trap: a `true` return plus a freshly-touched `.umap` is NOT proof the actor moved on disk. **Fix:** call `actor.modify(True)` immediately before (and after) the transform edit to dirty the external package; then `save_current_level()` flushes the level + its dirty external actors. **Verify on disk with `git status` showing the `__ExternalActors__/.../*.uasset` files Modified (not just the `.umap`), or reload the map and re-measure** — the umap alone changing means the props are unsaved.
- **A tool returning success proves the tool ran, not that the work is right.** Always verify the result; for anything visual, verify with the multi-view battery and a *fresh* reviewer (doctrine 1, 4).
- **Confirm which editor you're driving** if behaviour contradicts a change you just made — one MCP server per port; a stale editor keeps answering.
- **A new *Python* toolset hot-registers — no editor restart.** Add the class to `ue_mcp_toolkit/toolsets/__init__.py`, then from Remote Control `reload` the package and call `_registration.register()`; the MCP server enumerates it live (verified 2026-07-21 — `CaptureTools` appeared in `list_toolsets` mid-session). This is the opposite of a **C++** toolset, which enumerates once at startup and needs a full restart. So: build/iterate toolkit tools in Python where possible; reserve C++ for what only C++ can reach (e.g. protected-property reads). While iterating a Python tool's logic mid-session, drive its module-level functions directly via Remote Control `py` — same code, no re-register churn.
- **`unreal.Rotator` positional order is `(roll, pitch, yaw)`, NOT `(pitch, yaw, roll)`.** `Rotator(-90,0,0)` sets *roll* and leaves a "top-down" camera staring at the horizon. Always construct by keyword (`unreal.Rotator(pitch=-90, yaw=0, roll=0)`) or aim with `unreal.MathLibrary.make_rot_from_x(direction)`.
- **`CaptureViewport` / `HighResShot` target the editor viewport, not the live-PIE floating window** `[MEASURED: 2026-07-21]` — so they cannot frame an arbitrary pose inside a running PIE session. **Controllable, arbitrary-pose crowd/scene capture is therefore done in the editor world via `CaptureTools`** (the transient `ASceneCapture2D` route above), which poses freely; the **`NetworkHarnessTools` PIE rig owns the *replication truth*** (structured JSON pass/fail from all parties), **not** the visual. Keep the two jobs on their own tools — capture is visual + editor-world, the harness is structured + PIE.
- **🚨 Never `taskkill //IM UnrealEditor.exe`** — the `-server` process and the owner's editor share one image name; kill one captured PID, never a name. Shut a `-server` run down from inside (`quit` in its exec list).
- **Remote Control returns nothing useful — `ExecuteConsoleCommand` is void, so a successful call is `{}`.** An empty `{}` is **not** proof of success, and a Python traceback appears only in the log. Have the `py` script `unreal.log(...)` its results and read them back with `LogsToolset.GetLogEntries`. Two gates must be open for the `py` route (Project ▸ Plugins ▸ Remote Control): `bAllowConsoleCommandRemoteExecution` **and** an allowlist entry for `KismetSystemLibrary::ExecuteConsoleCommand`; leave `bAllowAnyRemoteFunctionCall` **off**. ⚠️ Anything that can reach `localhost:30010` can then run arbitrary editor Python.
- **Call a toolset by its fully-qualified registered name** exactly as `list_toolsets` reports it (`EditorToolset.EditorAppToolset`, not `EditorAppToolset`) — the short form returns `Toolset 'X' not found`, which reads like the toolset is missing rather than misnamed. **`call_tool` splits that name across two params: `toolset_name` = the fully-qualified toolset id (`ue_mcp_toolkit.toolsets.capture.CaptureTools`) and `tool_name` = the bare method (`capture_view`), plus `arguments`.** Passing the whole dotted path in `tool_name` returns `Tool '...' not found` — which reads like the tool is missing rather than mis-split `[MEASURED: 2026-07-22]`.
- **A `false` / failed return means "you called it wrong" at least as often as "the engine forbids it."** Run `describe_toolset` and read the parameter schema before concluding anything is impossible.
- **A C++ toolset must register from `UEditorSubsystem::Initialize`, never `StartupModule`** — the MCP server builds its tool list once, so module startup is too early (the toolset compiles, links, loads cleanly, and is never enumerated) and runtime registration is too late. `SlateInspectorToolset` is the only engine C++ toolset that registers, and it uses a subsystem. (Contrast the Python hot-register above.)
- **`PluginToolset.SetPluginEnabled` only takes effect after an editor restart, and can no-op silently** — check the `.uproject` after the call (procedure: `skills/native-iteration`, "Plugins the change needs"), restart, then `StartServer` in the new editor's console to reconnect the session.
- **PCG `GetNodeDataView` / `ExecuteGraphInstance` share state per graph asset** — concurrent calls on actors sharing one graph **freeze the editor**. A second concurrency hazard beyond the game-thread-serial rule.
- **Toolset plugins are `NoRedist`** — editor-time only, never shipped.

---

## Schema traps that fail silently
The main hazard on this surface is a call that returns `false` or no-ops with no error on the wire:
- **Several params take a JSON *string*, not an object** — `ObjectTools.set_properties.values`, `ConfigSettingsToolset.SetSectionProperties.propertiesJson`, `DataTableTools.set_rows.values`, PCG/Dataflow `jsonParams`. Passing an object returns `false` and no-ops.
- **Some `comment` params default to leaked C++ doc-comments** (GameplayTags, GameplayCue, PCG, Dataflow) — pass them explicitly or you write Doxygen into the project as data.
- **`LogsToolset` defaults `category` to `"LogsToolset"`** — always pass the real category or you filter to an empty set.
- **Many optional-feeling params are actually required** — pass an empty string / array.
- **`UMGToolSet` silently sets the *wrong* property** unless you `ObjectTools.list_properties` first.
- **`GameplayTagsToolset.RenameTag` / `RemoveTag` return nothing** — verify with `ListTags`.

## UI automation (SlateInspector) — the walkable-window rule
The Slate inspector is the fallback when no toolset reaches a thing, but it has two traps that read exactly like "the widget isn't there":
- **`Snapshot` / `WaitFor` read an observer cache, not the live widget tree.** With no deep observer they return empty / `false` — a false negative. Call `Observe("", 30)` first and confirm `ListObservers` shows a non-zero `cachedSnapshotSize` before trusting any negative result. Refs go stale when a menu re-renders or a window reopens — re-snapshot, don't reuse.
- **Floating windows walk; docked content does not.** Menus, submenus, dropdowns and floating panels snapshot down to their buttons and text. Anything docked in the main window — viewport, Outliner, Details, Content Drawer — reports its container as childless even at depth-30, so it cannot be clicked/dragged and drag-and-drop between a docked browser and a panel is not achievable. **Trick:** open a panel from `Window ▸ …` when it is *not* already in the layout — it opens floating, and floating is walkable.
- **`EditorAppToolset.CaptureEditorImage` shows the editor as the user sees it**, but its base64 exceeds the tool limit — decode the saved tool-result file to PNG and `Read` that. `SlateInspectorToolset.Screenshot` returns empty.

---

## Setup the toolkit expects (documented dependency)

The game project must have, in `Plugins/`, the **`ue-mcp-toolkit`** plugin, and in the engine/project, Epic's **`ModelContextProtocol`**, **`AllToolsets`**, and **`RemoteControl`** enabled and configured (auto-start server; RC console-command allowlist). The toolkit repo's own README owns the install steps; this guide owns *how to drive it*.

*One home per fact: engine-behaviour truths live in the specific `guides/` topic or the toolkit's docs, verified — not duplicated here.*
