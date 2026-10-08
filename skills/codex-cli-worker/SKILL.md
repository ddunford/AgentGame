---
name: codex-cli-worker
description: Run the Codex CLI as a second, non-editor worker pool — `codex exec` in a workspace-write sandbox with a role brief and a one-file write scope — for design notes, code reading, offline analysis and reviews of frozen files, then verify its scope with git status and relay its result. Never for editor-driving work.
fires-when: The producer has independent non-editor work (a design or research note, a code read, an offline analysis, a review of frozen files) and wants it off the main agent's usage or run in parallel. Skip for anything that drives the editor, needs the task tracker CLI, needs executables outside the workspace, or must be judged by a specific fresh reviewer role the host's own agents provide.
---

# codex-cli-worker

**Owner: the producer (root).** It writes the brief, launches the worker, checks the scope afterwards and posts the result to the task tracker. The worker is a contributor like any other subagent: the single-editor-writer rule, one writer per file per round, and "workers report, the producer decides" all apply (`guides/workflow.md`, `guides/tooling-ue.md`).

Doctrine this enforces: **build and verify are different owners**; **tool success is not proof** — a worker's "done" is checked against `git status` and the file it was allowed to write.

## Suitable work
Design and research notes, code reading and structural checks, offline analysis scripts, and reviews of files frozen and hashed for the round. Not suitable: editor or MCP/Remote Control work, live trials, anything needing the tracker CLI, GPU or image tooling outside the workspace.

## Run
```
codex exec -s workspace-write -C <repo> -o <scratch>/<task>.last.md - < <scratch>/<task>.brief.md > <scratch>/<task>.log 2>&1
```
- Run it in the background and wait for completion; do not poll it in a loop.
- `-o` writes the worker's last message (its report); the log holds the full transcript.
- The binary may not be on `PATH` in agent shells; launch using the **full path to codex.exe** and record the path and version in the project adapter. Check the first log line: redirected "command not found" can exit 127 silently into the log (verified 2026-10-08).
- Briefs, logs and last-message files go in the project's git-ignored scratch folder.

## Brief rules
- **Role:** name the studio role file in `agents/` the worker loads, and the task id.
- **Write scope:** the exact file (or few files) it may create or edit. Everything else is read-only.
- **Forbidden:** the editor (MCP and Remote Control), plugin or engine source unless assigned, large data and output directories (simulation output, evidence, captures) — name them. Recursive searches over data directories are forbidden too.
- **Inputs by path and section,** not pasted history; state live facts with their readback paths and the ruled-out options so it does not re-propose them.
- **Unreal C++ it cannot compile:** state that Unreal unity builds merge several `.cpp` files into one translation unit, so file-local helpers (anonymous namespace or `static`) must carry a name unique across the module (prefix with the file's subject, e.g. `TornadoSmooth`), and ask the worker to grep the module for each new free-function name before using it. A generic `Smooth`/`Clamp01`/`Lerp` helper collided with another file's and failed the build (verified 2026-10-08). Unreal also compiles with warnings as errors: no local variable may shadow an outer one (C4456/C4457/C4458 fail the build), so the brief asks for fresh names in nested scopes.
- **Report:** what it did, files written with hashes, what it did not do or could not verify, inferred vs verified claims marked. Ask for a "not done" list; workers drop trailing items silently when they hit limits.

## Sandbox limits (workspace-write)
- **Executables outside the workspace are blocked** ("Access is denied"), e.g. a system-installed ffmpeg. The engine's bundled Python runs but lacks numpy, Pillow and OpenCV. For image, video or numeric analysis the worker writes the script and the producer runs it, or the job goes to a host subagent instead.
- **The task tracker CLI is not reachable** inside the sandbox. The producer posts the tracker comment from the worker's last message.
- Network and credential use follow the sandbox; never hand it secrets in the brief.
- **Some workspace folders are read-only to it**, e.g. a hidden agent-skills folder such as `.agents/`, while a submodule or `docs/` stays writable. For files there, the brief asks for complete replacement files in a staging folder. The producer checks the diff is what was asked (`git diff --no-index --numstat`), then copies them into place.

## After the run
1. Check the process exit and the last-message file exist and are non-empty.
2. `git status --short` (and the scratch folder listing): only the assigned files changed. Anything else is reverted and reported.
3. Read the written file before relaying it; claims it marks "verified" need a citation the producer can check. A worker's root cause is a hypothesis.
4. Post the tracker comment, and record the brief, log and result paths.

## Evidence required
The brief path, the command line, exit status, the last-message path, the `git status` scope check, and the tracker comment.

## Block these
- A Codex worker touching the editor, or running while another worker owns a file it writes.
- A brief without an explicit write scope.
- Relaying a worker's result without the scope check.
