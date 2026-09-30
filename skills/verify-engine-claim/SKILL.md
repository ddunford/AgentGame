---
name: verify-engine-claim
description: Verify a claim about Unreal Engine behaviour against engine source, with a file:line citation, before it is asserted or built on; resolve every [verify] tag.
fires-when: Before stating how UE works — a cvar's effect, an ini section, whether an API is supported, a config default, what a tool can or can't do — or before acting on anyone else's UE assertion, including this framework's own notes. Skip only for a claim already carrying a verified file:line citation.
---

# verify-engine-claim

**Owner: `engine-verifier`.** Nothing about how the engine behaves is trusted until it has been seen in the source (doctrine 10). This is the gate every `[verify]` tag resolves through.

## Procedure

1. **State the claim precisely.** Reduce it to one testable assertion — "cvar X in ini section Y does Z", "API A is supported on this build", "toolset T can do U". A vague claim can't be verified.
2. **Treat the source as a claim, not proof.** A doc, forum post, marketplace listing, this framework's own guides, or another agent's assertion is a *claim*. Only engine source settles it.
3. **Locate the engine source.** Find the owning file in the engine tree (path in `guides/tooling-ue.md` / project AGENTS.md). Read the actual definition — the cvar registration, the ini-read, the API signature, the default in the header.
4. **Confirm runtime behaviour where it matters.** If the claim is about runtime effect, back the source read with a minimal live check (using available supported controls per `guides/tooling-ue.md`) — but the citation, not the check, is the record.
5. **Don't conclude "impossible" from a `false`/empty return.** That usually means "called it wrong", not "the engine forbids it" — read the parameter schema / `describe_toolset` / source before concluding a capability is absent.
6. **Record the finding as present-tense fact + `file:line` citation.** Either the verified claim or a correction of the asserted one, written-as-current (doctrine 12) — ready to write into the owning guide.
7. **Backport immediately (doctrine 13).** An engine-behaviour fact goes into `guides/unreal-engine.md` with its citation; replace the `[verify]` tag in place with the cited fact or correction. A lesson that lives only in the session is lost.

## Output

A verified claim with `file:line`, or a correction of the asserted claim — cited, present-tense, backported to the owning guide.

## Block these
- Asserting engine behaviour from memory, docs, or a marketplace page.
- Concluding "impossible" without reading the source/schema.
- Leaving a load-bearing `[verify]` tag unresolved.
