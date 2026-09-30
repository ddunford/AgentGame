# Driving Unreal with available controls

The studio requires evidence, not a particular transport. Read the host’s actual control skill/tool contract and game instructions first. Do not assume computer access, MCP, Remote Control, scripting or a companion plugin is installed.

## Choose a method by capability

| Method | Use when | Evidence |
|---|---|---|
| Computer control | Supported visible editor/browser work, especially when requested | Fresh UI state, correct target window, saved result and actual player-view checks |
| Supported engine tools/API | Structured operations are available and suitable | Discovered schema, checked result and saved-state/runtime verification |
| CLI/build tools | Project-supported source/build/package/log work | Diagnostics and actual build/run outcome |
| Optional MCP/toolkit | Already available and useful, or installation specifically authorized | Live capability check; no historical inventory assumption |
| Human operation | Required action unavailable to the agent | Concrete prepared work and identified pending check |

Computer control can work without MCP; an available API can still help. Honour the user's selected method. Do not silently install or expose services to satisfy a role brief. Build new tooling only when its value justifies the work after considering existing controls.

## Shared operational rules

- One owner uses the live editor, including PIE, capture, camera and state-dependent queries. Transfer ownership explicitly. File-only research can run in parallel. This coordination rule does not assert that every simultaneous engine request deadlocks.
- Identify the project/map, editor or PIE world and window. Refresh stale UI references; follow the host’s computer-control constraints.
- Save a baseline and the result. Verify persistence, especially external actor packages and imports. A successful response is not proof of the intended saved change.
- Wait for compilation/preparation before judging blank views.
- Verify gameplay in the actual possessed player view with intended movement/input. Editor cameras, temporary capture lighting and teleported pawns do not prove the player experience.
- Record relevant versions, map/seed, settings, timing and evidence. Old surveys do not prove new-session access.
- Avoid routine app closure. Save and explain necessary restarts; never kill every process sharing an editor image name to stop one test.
- Tool success means the operation returned, not that the acceptance criteria passed. Use an independent reviewer.

## Optional integration reference

[Unreal MCP reference](integrations/unreal-mcp-reference.md) preserves a prior environment’s tool inventory and lessons for projects using that stack. It is not required setup. Revalidate versions, schemas and behaviour locally; host restrictions and these ownership rules take precedence. A missing capability remains untested, not silently replaced by weaker evidence.
