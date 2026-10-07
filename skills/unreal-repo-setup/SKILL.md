---
name: unreal-repo-setup
description: Put an Unreal project under Git + LFS correctly — what to commit and what never to, vendor packs declared-not-committed with a required-content manifest, a reference scan before excluding any folder, a nested plugin repo as a submodule, LFS patterns that catch upper-case extensions, a fresh public history via an orphan branch, and a safe push routine (outgoing LFS list checked; never a dry-run as an auth test; never force-push main).
fires-when: Creating or re-shaping a project repository, publishing a project's history somewhere new, adding a plugin repo inside the project, excluding a content folder, or before any push that may carry LFS content. Skip for routine commits inside an already-correct repo, except the push checks.
---

# unreal-repo-setup

**Owner: `build-engineer`** (the producer/root when no build engineer is active). The rules of what a reproducible build must declare live in `guides/build-release.md`; vendor-pack policy in `agents/build-engineer.md` and `agents/tech-artist.md`. This skill is the procedure. Pushing and publishing follow the project's own authority rules: an agent pushes only where the owner has granted it, and a first public push is owner-reserved.

Doctrine this enforces: **reproducible from a clean checkout, or it is not a build** (`guides/build-release.md`); **tool success is not proof** — a push that "succeeded" may have uploaded content that must never leave the machine.

## Commit
- `<Project>.uproject`, `Config/`, `Source/`.
- `Content/` minus vendor packs and spike/test content; World Partition `__ExternalActors__/` and `__ExternalObjects__/` (they are `.uasset` files, so LFS).
- Plugin source, shaders, content, `Resources/` generators and descriptors (`.uplugin`, `Config/FilterPlugin.ini`).
- Source art you author and cannot regenerate; small reports or manifests that describe generated art.
- The task tracker's text export if the project keeps one in Git (never its live database).

## Never commit
- `Binaries/`, `Intermediate/`, `Saved/`, `DerivedDataCache/` — at the root **and in every plugin** (the patterns without a leading slash cover both), IDE files (`.vs/`, `*.sln`, `*.VC.db`, `*.suo`), `__pycache__/`.
- Vendor packs (Fab, Marketplace, engine template content): their licences allow use in the game, not redistribution in a repository. Declared, not committed (below).
- Spike, test and developer content (`Content/Developers/`, `Content/Collections/`, spike folders) not referenced by the game.
- Agent work products: scratch scripts, evidence and captures, research notes, transcripts, tool session files, `.env` files and secrets.
- Personal or machine-local settings (`.claude/settings.local.json`, local backups, `*.blend1`).
- The live task database, its credentials and activity logs.
- Reference photos used only for judging, and generated source art that a committed generator reproduces byte-identically (keep its hash in a provenance file).

## Vendor packs: declared, not committed
- A **required-content manifest** (Markdown table or JSON) lists each pack: folder, source, how to add it, what uses it, and a sentinel asset. Optionally a startup validator fails loudly with the missing list, so a fresh clone never opens an empty level silently.
- **Before excluding any folder, scan kept content for references into it.** Package files carry their imports as plain strings, so a byte search of every kept `.uasset`/`.umap` for the excluded mount path (`/Game/<Folder>/`) finds every dependent. A kept asset that references an excluded folder is either a declared dependency (add it to the manifest) or the folder is not excludable. Re-run the scan after each placement pass; the manifest drifts otherwise.
- Licence records live where the project keeps licences; the manifest does not grant one.

## LFS patterns (`.gitattributes`)
- Route `*.uasset`, `*.umap`, source art (`*.blend`, `*.fbx`, `*.obj`, `*.psd`), images (`*.png`, `*.jpg`, `*.jpeg`, `*.tga`, `*.exr`, `*.hdr`, `*.dds`), volumes (`*.vdb`), audio and video through LFS.
- **Patterns are case-sensitive.** Add the upper-case variants your content actually uses (`*.FBX`, `*.PNG`); a missed variant goes into Git as a normal blob and stays in history.
- Check: `git lfs status` shows each staged binary as LFS before the commit; after it, `git lfs ls-files` lists every binary and `git ls-files` filtered for binary extensions shows nothing outside that list.

## Nested plugin repository: a submodule
A plugin that is also its own product gets its own repository and is added as a submodule (`git submodule add <url> Plugins/<Plugin>`). Push order is fixed: **commit and push the plugin first, then commit the bumped pointer in the game and push the game.** A game commit whose submodule pointer is not on the plugin remote is a broken clone.

## Fresh public history (orphan branch)
When the existing history holds content that must not be published (vendor packs, secrets, evidence), publish a new history rather than rewriting the old one:
1. `git checkout --orphan <new-branch>`
2. `git rm -r --cached -f .` — **`-f` is required.** Without it, files staged differently from `HEAD` make it abort, and it leaves the **old index in place**: the next commit then silently carries the old tree.
3. Fix `.gitignore` and `.gitattributes` first, then `git add -A`, and inspect `git status` and `git lfs status` against the never-commit list.
4. Commit, then rename the branch and push it as the new remote's default branch.

## Push routine (every push)
1. **List the outgoing LFS files** before pushing: `git lfs push --dry-run <remote> <branch>` lists the objects that would upload; read it against the never-commit list. Anything vendor, evidence or secret stops the push.
2. **Never use `git push --dry-run` as an auth or connectivity test.** It still runs the LFS pre-push hook, which **uploads every LFS object** of the pushed ref; only the ref update is skipped. Uploaded LFS objects stay on the host even when no branch points at them (observed 2026-10-06: an "auth check" dry-run uploaded several hundred objects, vendor content among them, that were never meant to leave the machine). Test access with `git ls-remote` (read), or a push of a throwaway commit with no LFS content, or with the hook disabled (`GIT_LFS_SKIP_PUSH=1`).
3. **Never force-push or rewrite `main`.** A fresh history goes to a new remote or a new branch, never over the published one.
4. Push the plugin submodule before the game when its pointer moved.

## Evidence required
`git status --short` before the commit, the staged/outgoing LFS file list, the reference-scan result for any excluded folder, the manifest diff, and the push output (ref and LFS object count).

## Block these
- Committing a vendor pack, evidence, secrets or a live task database.
- Excluding a folder without the reference scan.
- An LFS pattern set that misses an upper-case extension in use.
- `git rm -r --cached .` without `-f` when building a fresh history.
- A dry-run push as an auth test; a push without reading the outgoing LFS list; a force-push to `main`.
