---
name: native-iteration
description: Iterate Unreal C++ safely — Live Coding for in-session trials, and the persistent rebuild cycle (save all, quit the editor through its own command, build with the editor closed, relaunch, reconnect, prove the live binary matches source) for anything that must survive a restart. "Compiled" is never "live".
fires-when: Whenever native source changes must be tested in a running editor or persisted, and after any editor restart before trusting a trial. Skip for content-, data- or shader-only changes that need no C++ build.
---

# native-iteration

**Owner: the one agent that owns the live editor this round** (usually the producer/root or `build-engineer`); the code author is often a different agent. Live-editor ownership and the never-kill rule live in `guides/tooling-ue.md`; engine facts about Live Coding and reinstancing belong in `guides/unreal-engine.md` with source citations (`verify-engine-claim`). The project adapter names its own build, quit, save and probe scripts; this skill is the pattern they implement.

Doctrine this enforces: **verify claims against source** (10) — a live binary is proven, not assumed; **tool success is not proof** (`lessons.md`) — "build succeeded" says the compiler ran, not that the editor runs the new code.

## Who may do what
- **Code authors and workers edit source only.** They never close the editor and never build. Their report lists the changed files with hashes under "native changes pending rebuild", and the check to run afterwards.
- **One build owner** runs the persistent cycle, and only when all hold: no worker owns or depends on the editor (a worker launched from inside the editor dies with it), PIE is stopped, everything is saved, and the editor will close through its own quit command. Otherwise the owner runs it.

## Live Coding — in-session only
- Live Coding patches the running process; the module binary on disk is unchanged, so **a restart silently drops every patch**. A fix tested under Live Coding and never rebuilt reverts at the next launch, and every later trial runs old code.
- Recent engine versions may reinstance some reflected changes in session too `[verify — per engine version]`; nothing persists either way. New classes, structs, reflected properties and functions need the persistent cycle before they can be relied on.
- Prefer the synchronous compile command so the result can be read; read success or failure from the log, never from the call returning.
- Patch only from a locally built baseline. Never copy binaries built by another host or packaging run into the project.
- Scripting wrappers can go stale after a reflected change; call through reflection, or restart.
- Keep a **build marker**: a revision constant the code exposes at runtime, bumped with every native change, so a probe can tell old code from new.

## Persistent rebuild cycle
1. **No other editor owner.** Confirm workers that drive or were launched from the editor have exited.
2. **PIE stopped**, no transient trial values applied.
3. **Save all and confirm clean.** A save script that logs the dirty list; anything still dirty stops the cycle.
4. **Exactly one editor process, its PID captured.** A second editor or a server process sharing the image name aborts the cycle — never kill by image name.
5. **Clear the previous build result** so a stale success cannot be read as this build.
6. **Start the build watcher outside the editor** (a background shell task, never a child of editor scripting): it waits for that PID to exit, refuses if any editor remains, builds the editor target with the editor closed, writes a result file and log, then relaunches the project.
7. **Quit the editor through its own quit command.** Never kill it.
8. **Wait for the watcher's completion**, without a polling loop. Read the result code and the build line from the log. A watcher that relaunches after a failed build leaves the editor on the old binary — fix source and repeat; never accept an in-editor "rebuild modules" prompt as the build route.
9. **Wait for the map to load** (the log's map-load and map-check lines), then **reconnect** the control session (clear any cached session id). The console may not accept input for some seconds after load; resend and confirm the command actually ran.
10. **Prove the live binary matches source.** The build-marker probe reads the new revision (stale = the build did not load). Then read back one value only the new code produces — a new property, a new default, a parameter only the new code writes — and check the saved level does not keep an old value as an override of a changed default.
11. Only then run the change's tests and trials.

## Crashes
Copy (never move) the crash folder and logs to a recovery location before relaunching, and check for hardware errors before blaming the build (`guides/tooling-ue.md`). Record the time, last command and log tail. A cause is a hypothesis until a repro or a source read proves it.

## Evidence required
The save-all line, the PID used, the build result and build log line, the map-load lines, the probe result, the marker readback, test results, and anything not verified.

## Block these
- Trusting a Live Coding fix after a restart without the probe.
- Killing the editor, or building as a child of the editor.
- Calling a change "live" because it compiled.
