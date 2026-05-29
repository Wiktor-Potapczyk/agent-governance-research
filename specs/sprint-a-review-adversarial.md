---
date: 2026-05-25
updated: 2026-05-25
tags: [project/agent-governance-research, audit, meta]
status: active
---

> Adapted from internal research workspace. Cross-references to vault-internal artifacts have been stripped or genericized.

# Sprint A Task-Decomposition Round-1 Review — adversarial-reviewer lens

Hub: agent-governance research repo · Target: [[sprint-a-task-decomposition]] · Confidence: 0.82

**Verdict:** NEEDS-CHANGES (Round 1 of 2)

**Persistence note:** Sub-agent returned inline (no Write — Q5 doctrine pending). Main session persisted 2026-05-25 18:46.

## Critical findings

### CRITICAL — SA-4 false-positive surface not actually tested

SA-5's FP guards do NOT cover: "sub-agent tool_result block says 'I tried to write X but Write failed' → no Write trace + path absent → hook fires FABRICATION_DETECTED on a non-fabrication." Tool_result parsing was added to widen detection, not reduce false positives. R1 mitigation claim ("combined Write-trace + path-check + tool_result parsing closes the surface") is circular. SA-5 needs an FP guard for legitimate-Write-failure-reported-by-sub-agent.

### CRITICAL — SA-7 measurement asymmetric

G1 success criterion is "hook-detected ≥ Wiktor-discovered." SA-7 counts Wiktor-discovered via memo count. Verbal catches don't create memos (acknowledged in brief). Additionally: governance-log `FABRICATION_DETECTED` count inflates if hook has false positives — making the ratio look favorable while hook misfires. No FP rate check in 30-day audit. G1 could "pass" via instrumentation asymmetry.

### CRITICAL — `ls -la` alternative not engaged

Brief asked: would 5-6h SA-4+SA-5 build vs. a bash alias `claude-ls () { ls -la "$1"; }` + doctrine memo close the same gap? Decomposition does not address this. Q8's "ergonomic automation of already-working mechanism" framing is recorded as SA-4 §1 input but the hours comparison is never made. Decomposition assumes hook adds detection coverage above baseline WITHOUT proving which incidents would have been caught EARLIER by hook vs. existing `ls -la`.

## Warning findings

### WARNING — SA-2 no-bug branch retroactively questions synthesis §3 framing

If H3 is correct (47-vs-42 ratio is correct signal), Item 3's PRD premise was wrong. The synthesis selected this as a meaningful gap. Decomposition treats "close G4 with no-bug" as a clean exit — does not flag that H3 finding would prompt a PRD revision.

### WARNING — SA-6 AC1.4 misapplied in no-bug branch

AC1.4 single-commit rationale was coupling two code changes for atomic revert. In no-bug branch, SA-3 is a `.md` diagnosis file — not atomically coupled to a hook code change. AC1.4 doesn't survive the no-bug conditional path; decomposition doesn't revisit.

### WARNING — SA-1 bundling structurally suspicious

Q5 (high evidence — AW-5 smoke test) + Q8 (no new evidence, framing dispute) + Q9 (implementation detail) in one Wiktor session creates a dynamic: Wiktor approves Q5 + Q9 in same turn where Q8's unresolved framing question (does SA-4 exist at all?) is presented. SA-4's hours investment is tacitly authorized via the bundle.

### WARNING — Language-pattern still load-bearing

SA-4's detection trigger: "Write-claim text pattern matches AND (path not in Write-trace OR path does not exist)." The text pattern match is still the gate. A fabrication that avoids Write-claim language (sub-agent says "the file is at X" without saying "wrote" or "saved") doesn't trigger the hook. Single-point-of-failure for atypical phrasing.

## Gap findings

### GAP — Sprint A value ordering vs synthesis §6 ranking

Brief asked: was 53% MUST DISPATCH compliance gap (synthesis §6 top) deprioritized for visibility bias on Item 1? Decomposition contains no justification for Item 1 over `process-step-check.py` soft-to-hard upgrade. PRD selection treated as settled. If 53% gap closes a broader failure mode (non-dispatch across all task types) vs. Item 1's narrower scope (fabrication detection), Sprint A is spending 10-14h on more-documented gap rather than higher-impact gap.

### NOTE — SA-7 baseline file orphan-prevention

`sprint-a-g1-baseline.md` created by autonomous task at SA-6 commit time. Vault stewardship rule: every new `Projects/*/work/` file needs inbound wikilink same turn. No human session guaranteed active. Decomposition does not designate where orphan-prevention link comes from.

## Untested surface

- Which of the 5 fabrication incidents would have been caught earlier by hook than by existing `ls -la`.
- Realistic distribution of tool_result block content + whether Write-claim language appears there in non-fabrication cases.
- Whether H3-being-true causes PRD revision or clean close.
