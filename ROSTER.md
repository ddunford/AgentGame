# The Studio Roster

The team, as agents. Three leadership **spines** meet in one **Director** (owner-reserved); departments hang off them; **Verify & Judge** gates work out, independent of who built it; **Operate** runs the live game at scale. Solo, these are hats — but the hats never merge build with verify.

**Departments:** `DIR` Direction · `DSN` Design · `ART` Art · `ENG` Engineering · `AUD` Audio · `V&J` Verify & Judge · `OPS` Operate · `PROD` Production & Knowledge.

Every role links its craft depth to a `guides/` guide and runs its process through a `skills/` procedure. Late-activating disciplines note the phase they switch on (schedule: `guides/production-pipeline.md §3.5`); the rest are active from day one.

## Leadership — the three spines (DIR · PROD)
| Agent | Spine | Owns |
|---|---|---|
| `director` | all three (fused) | Final "good / sound / ship" — **owner-reserved** |
| `creative-director` | creative | Vision, pillars, on-pitch veto, spike review |
| `technical-director` | technical | Architecture, UE5 calls, the `decide` call |
| `producer` | production | Plan, sequence, gates, "you are here", resume |

## Design (DSN)
| Agent | Owns |
|---|---|
| `game-designer` | Mechanics, systems, economy, tuning data |
| `level-designer` | Plan · metrics · blockout, from canonical views |
| `ui-ux-designer` | The whole UI/UX surface — UMG logic and visuals, HUD, menus, flows, input, accessibility basics |
| `narrative-designer` | Story, worldbuilding, lore, in-world text, environmental narrative, tone |
| `creator-tools-designer` | The player-facing world-building editor — palette, data-not-code model, abuse boundary |

## Art (ART)
| Agent | Owns |
|---|---|
| `art-director` | Style bible, palette, silhouette, lighting registers, visual consistency |
| `tech-artist` | Ingest, collision, budgets, materials, PCG, asset pipeline |
| `environment-artist` | Set-dressing, clutter, decals, wear, vegetation — the human traces |
| `lighting-artist` | Day/night registers, exposure, contact shadows |
| `character-artist` | Character design/modelling, topology, texturing, rig-ready mesh |
| `animator` | Rigging, retargeting, Control Rig, Anim BPs, locomotion, emotes |
| `concept-artist` | Concept & previz — exploration before commitment, feeding the look-bible |
| `vfx-artist` | Real-time Niagara VFX, FX materials, per-effect budgets, readability |
| `cinematics` | Sequencer, cameras, cutscenes, in-engine authored beats |

## Engineering (ENG)
| Agent | Owns |
|---|---|
| `network-engineer` | Replication, authority, relevancy, persistence |
| `gameplay-engineer` | Abilities, movement, feel (GAS, BP↔C++) |
| `tools-programmer` | Approved development tools and reliable editor access |
| `backend-engineer` | Accounts, save schema, atomic transactions, matchmaking, server fleet · *long-lead, P1* |
| `performance-engineer` | Frame / memory / bandwidth budgets — sets P1, gates P3–P4 |
| `build-engineer` | CI, cook, packaging, dedicated-server build, release/versioning · *P2* |
| `ai-engineer` | Crowd/traffic AI and NPC behaviour — perceived density, not a simulated city |

## Audio (AUD)
| Agent | Owns |
|---|---|
| `sound-designer` | SFX, ambience, music, client-side wiring |

## Verify & Judge (V&J) — builder-independent
| Agent | Owns |
|---|---|
| `qa-visual` | Multi-view level QA battery |
| `qa-network` | Server + 2 clients, negative tests |
| `qa-functional` | Feature-correctness against spec — edges, boundaries, regression · *P2* |
| `creative-review` | "Is it good?" — fresh judge, never the builder |
| `security-reviewer` | Name the exploit each check prevents |
| `engine-verifier` | Claims vs engine source |
| `user-researcher` | Moderated playtests — the qualitative "found the fun" signal · *P1* |

## Operate (OPS) — the live game at scale
| Agent | Owns |
|---|---|
| `trust-safety` | Player safety and moderation — UGC harm surface, reporting, age-gating · *long-lead: policy P1, tooling P2* |
| `live-ops` | Release cadence, live events, hotfix/rollback, incident response · *P5, runbooks P3–P4* |
| `analytics-engineer` | Telemetry, metric definitions, dashboards — the data-informed signal · *P2* |
| `monetization-designer` | Storefront, payments, premium currency, creator payouts · *P3–P4* |
| `localization` | String externalization, loc pipeline, culturalization · *externalize P1, translate P3* |
| `accessibility` | Input/visual/audio/cognitive accessibility to recognised standards · *principles P1, pass P3* |
| `compliance-advisor` | IP/age/privacy/payment risk — advisory, owner-and-counsel reserved · *framing P1, sign-off P4* |

## Knowledge (PROD)
| Agent | Owns |
|---|---|
| `knowledge-keeper` | Design docs / source of truth, written-as-current |

---
**41 agents authored** — the full studio. The core-loop disciplines are active from day one; the operate-at-scale and late-production roles switch on at the phase the activation schedule sets (`guides/production-pipeline.md §3.5`), authored when their stage arrives.

**Method depth** lives in `guides/` (the per-discipline craft references) and process runs through `skills/` (the callable procedures — `plan-milestone`, `team-execute`, `resume-work`, the QA batteries, `harden-endpoint`, `ingest-asset`, `fab-acquire`, `verify-engine-claim`, `vault-doc-update`, `decide`). Reusable system contracts belong in `modules/` as they are written; `hooks/` enforces guards, injects context, and surfaces progress.
