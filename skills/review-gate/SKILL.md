---
name: review-gate
description: Classify a change, register its mandatory independent reviews, and block task or phase closure until evidence-backed verdicts pass or the owner explicitly overrides them. Use when planning review coverage and at quality, review, and phase-close gates.
---

# Review gate

Owner: producer; technical-director resolves technical classification questions. This is the routing and closure contract for the [production pipeline](../../guides/production-pipeline.md), not a replacement for its review procedures.

## Register before building

1. State the task's one question, acceptance and rejection criteria. For uncertain approaches use [spike](../spike/SKILL.md). Record the target stage, platform, build configuration, representative scenario, budgets, seeds, references and evidence required before trials start.
2. Classify **all** affected surfaces using the matrix. Take the union of mandatory reviews; an optional entry never cancels a mandatory entry in another row. Add project-specific gates. Reclassify when scope changes; never weaken criteria after seeing results without a recorded owner decision.
3. Put the verdict table on the task before build, naming each independent reviewer. Optional reviews are selected by risk with a reason; unselected ones are recorded as N/A with that reason. Unavailable reviewers or tools leave required rows PENDING, not N/A.
4. The builder supplies a reproducible evidence packet: frozen revision/file hashes, build identity, settings, test commands and logs, baseline/candidate captures and known limitations. The reviewer checks its validity, reproduces the relevant checks and judges; the builder's success report is not a verdict.
5. Reviewers are fresh people or agent contexts, **never the builder**. Look judges receive neutral, shuffled captures and matched references without the change narrative or hoped-for result; the producer retains the blind key. QA and creative judgement remain separate roles. For code and designs, optionally request a second independent reviewer using a different model or tool; record both findings and resolve disagreements against evidence, not majority vote. A second tool run by the builder does not provide independence.

## Review matrix

Every row also inherits the universal requirements below. M = mandatory; O = optional unless another row or trigger makes it mandatory. Reviews not listed in a row are optional, subject to those triggers.

| Change type | M: mandatory reviews | O: useful additional reviews |
|---|---|---|
| Code/system, including scripts and shaders | code-review; qa-functional; stage-scaled security | second code/design reviewer; perf-gate; playtest |
| Gameplay feel | qa-functional; creative-review; playtest; accessibility | qa-visual; realism/art; perf-gate |
| Visual look | qa-visual; creative-review; realism/art; perf-gate; accessibility basics | playtest; qa-functional |
| Motion/animation | qa-visual in motion; qa-functional transitions; creative-review; realism/art in motion; perf-gate; accessibility | playtest |
| Lighting/exposure | qa-visual; qa-functional across lighting transitions; creative-review; realism/art; perf-gate; accessibility basics | playtest |
| Performance-sensitive: render, tick, memory | perf-gate; qa-functional regression | code-review if no code changed; qa-visual; playtest |
| Networking/authority | code-review; qa-functional; qa-network; security-reviewer + harden-endpoint; perf-gate; build-validate with packaged network smoke | playtest; second code/design reviewer |
| UGC/player-facing input | qa-functional including malformed input; stage-scaled security; accessibility; compliance framing | playtest; localization if no text changed |
| Plugin/package/release | build-validate + packaged smoke; stage-scaled security; compliance/licence; qa-functional on the delivered artifact | second code/design reviewer; playtest |
| Content/assets (licence) | compliance/licence and provenance; qa-visual for visible assets | creative-review; realism/art; perf-gate; playtest |
| UI/text | qa-functional; qa-visual; creative-review; accessibility; localization | playtest; perf-gate; realism/art |

Universal requirements:

- Every implementation change gets a lightweight security exposure check using the current stage below; unchanged surfaces may cite still-valid evidence. Documentation-only edits need a fresh accuracy/link/scope review, not an invented runtime test.
- Every implementation phase close and release runs build-validate / packaged smoke and representative performance checks on the final candidate. Between closes, code changes build their affected targets; dependency, module, cook or packaging changes trigger packaged validation immediately.
- Every phase closes with process-retro. A spike's narrow question limits its claims, not its required reviews; integrating it requires the affected production gates.
- Player-facing controls, cues, motion and readability require accessibility basics. Player-facing strings require localization review (externalization and fit now; supported-language checks at release). New dependencies/imports require licence and provenance checks even when introduced through code. Personal data, payments, minors or public distribution trigger compliance framing and the relevant owner decision.
- UGC/live surfaces add trust-safety review; ordinary local input does not activate an online service programme. No matrix row authorizes new features, publishing, purchases or remote access.

## Route to existing procedures

- Engineering and correctness: [code-review](../code-review/SKILL.md), [qa-functional](../qa-functional/SKILL.md), [qa-network](../../agents/qa-network.md).
- Look: [qa-visual / qa-visual-battery](../qa-visual-battery/SKILL.md), [creative-review](../creative-review/SKILL.md), and [realism-judge](../realism-judge/SKILL.md) for photographic targets. For stylised targets, an independent [art-director](../../agents/art-director.md) checks the approved style bible instead; record the chosen realism/art route before build and keep its verdict separate from creative-review. Motion requires video, stated timing/compression and temporal inspection; stills cannot pass motion.
- Cost and delivery: [perf-gate](../perf-gate/SKILL.md), [build-validate](../build-validate/SKILL.md). Follow the capture contract in qa-visual-battery for comparisons.
- Risk and inclusion: [security-reviewer](../../agents/security-reviewer.md), [harden-endpoint](../harden-endpoint/SKILL.md), [compliance-advisor](../../agents/compliance-advisor.md), [accessibility](../../agents/accessibility.md), [localization](../../agents/localization.md), [trust-safety](../../agents/trust-safety.md). Compliance findings are advisory; a completed briefing is not legal clearance.
- Experience and closure: [playtest](../playtest/SKILL.md), [process-retro](../process-retro/SKILL.md).

## Security scaled by stage

**Prototype / single-player:** record changed attack surfaces and check that editor remote-execution services are disabled in cooked/shipped builds; secrets are absent from repository changes and delivered artifacts; editor-only and debug execution code is excluded from runtime; data/preset parsing rejects malformed, oversized or out-of-range input and unsafe paths without executing it. Check dependency provenance, licences, pinned versions and relevant supply-chain changes. Agent jobs use scoped file/network/tool permissions and treat imported content as data; a review never grants permission bypass. Validate exclusions on the packaged artifact, not just from configuration intent.

**Networked:** retain the baseline and add security-reviewer plus harden-endpoint for every client-reachable authority surface; pair findings with qa-network negative tests. Review identity, server-derived decisions, replay/order and rate/resource limits.

**UGC / live:** retain applicable earlier checks and add trust-safety for ingestion, harmful content, reporting/moderation, abuse response and rollout/rollback. Add compliance framing for the actual audience/data surface. Scale to the product's real exposure; single-player is not a reason to omit the baseline.

## Performance and packaged cadence

Measure the representative workload on target-class hardware with fixed resolution, scalability, seed, route and duration. Record CPU/game/render/GPU frame times, hitches and peak memory as applicable against preregistered budgets. A PIE number is labelled **proxy**; it cannot certify shipping performance.

Default cadence: package, launch, smoke-test the critical path and measure performance at **each implementation phase close**, and for every release candidate. Register any tighter cadence (for example every five implementation commits) on the phase task with its next due revision. Run earlier after module, dependency or cook changes. A passing package from an earlier revision does not pass a changed closing candidate. Missing hardware or a failed cook leaves the gate pending/failed until resolved or explicitly overridden.

## Verdict and close

Record each required review separately on the task; attach detailed reports by link. PASS means its preregistered criteria were met on the named candidate. FAIL, PENDING and INVALID evidence all block closure. Fixes invalidate affected verdicts and require fresh re-review; retain unaffected verdicts only with a recorded reason and unchanged evidence inputs.

| Review | Required by / M or O | Independent reviewer | Candidate/build + evidence link | Criterion and observed result | Verdict | Finding owner / next action |
|---|---|---|---|---|---|---|
| <review> | <type/trigger; M> | <person/context> | <revision/hash, build, report> | <threshold; measurement> | PENDING | <owner; test/fix> |

Task header: classifications; stage; criteria/spec link; baseline and candidate identity; packaged cadence/next due check. Verdicts: PASS / FAIL / PENDING / INVALID / N/A (optional or genuinely untriggered only) / OWNER OVERRIDE.

Close only when **every mandatory row passes**, or the project owner explicitly overrides each remaining row. An override records owner identity, date, exact decision reference, waived criterion, failed or missing evidence, residual risk, scope/expiry and a follow-up owner/task. Preserve the underlying failure; never relabel it PASS. Producer/technical-director convenience is not owner authorization. Record the overall outcome as PASS or CLOSED WITH OWNER OVERRIDE, and retain any separate owner phase go/no-go required by the project. This is a producer-enforced checklist, not a claim that automated enforcement is installed.
