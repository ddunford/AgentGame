# Onboarding

1. Read [AGENTS.md](AGENTS.md) and [ROSTER.md](ROSTER.md). Preserve the game’s current scope and phase; adopting a workflow is not restarting it.
2. Pin this framework at a reviewed revision. Add the game-local bridge described in [adapters](adapters/README.md), merging with existing instructions.
3. Declare the game’s task tracker, knowledge/evidence paths, available controls, independent review mechanism and spend/publication policy.
4. Choose a bounded real feature or defect. Assign a builder, independent verifier and relevant creative reviewer; write acceptance before changes.
5. Run build → verify → judge. One operator owns the live editor. Use the requested supported control method; no toolkit installation is required by the process.
6. Record passed, failed and untested criteria. Keep game facts in the game repo and reusable process improvements here. A document rehearsal is not a gameplay test.

Roles run through the host’s supported delegation mechanism or an independent human reviewer. If independent review cannot run, keep the gate pending. No background service or hook becomes active by copying these files. [Claude compatibility](adapters/claude/README.md) is optional.
