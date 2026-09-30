---
name: build-validate
description: Package the project’s declared target, launch the artifact and smoke-test its critical path with saved evidence; add server/client checks only for a server target.
fires-when: Validating a milestone build or release candidate, or adding build verification to CI.
---

# Validate a build

Owner: build-engineer. Read AGENTS.md, project target/build instructions and guides/tooling-ue.md. Verify installed engine/toolchain support for that target; do not infer a source-engine requirement for all packaging or assume a particular project server target.

1. Record target, platform, engine/version, build configuration and reproducible inputs. Use the supported project build route with saved source/assets; coordinate any required editor closure and preserve work.
2. Cook/package, inspect diagnostics and required-content/dependency integrity. A zero exit status is necessary evidence but not proof the artifact runs.
3. Launch the packaged artifact itself. Test the declared critical path and check missing content, startup errors and version identity. Editor PIE is not a packaged pass.
4. For a project that actually ships a server target, verify that target’s engine requirements, boot the server and connect a client. For a single-player target this step is not applicable, not a missing multiplayer feature.
5. Return evidence and limitations to independent QA/review. Keep unavailable target tests pending; do not silently substitute another build. Publication remains governed by project/user authorization.
