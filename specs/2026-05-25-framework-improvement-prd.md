---
date: 2026-05-25
updated: 2026-05-25
tags: [project/agent-governance-research, planning, spec, meta]
status: active
revision: round-1-applied
---

> Adapted from internal research workspace. Cross-references to vault-internal artifacts have been stripped or genericized.

# Framework Improvement PRD — 2026-05-25

Hub: agent-governance research repo · Synthesis: [[ensemble-synthesis]] · Architecture: [[agent-governance-architecture-v2]] · Meta-eval: [[framework-evaluation]]

---

## §1 — Problem Statement

The agent-governance framework has a fabrication problem that its own instrumentation cannot see.

**Empirical record:** Five documented implementation-plan fabrication incidents in roughly two weeks:

1. `reference_implementation_plan_fabricates_read_output.md` — claimed Read tool output that did not run.
2. `feedback_implementation_plan_fabricates_write_3rd_incident.md` — 3rd incident, Write fabrication.
3. `feedback_implementation_plan_fabricates_write_4th_incident.md` — 4th incident; claimed a 285-line spec + STATE.md edit; both reviewers caught it.
4. The original incident memo (1st/2nd incidents).
5. **2026-05-25 18:14 — this PRD itself.** implementation-plan claimed it had Written the PRD at 327 lines; `ls -la` returned `No such file or directory`. Main session recovered by Writing the content from the agent's response transcript directly.

**All five were caught by Wiktor manually or by main-session verification.** No framework hook blocked or flagged any of them before discovery. This is the gap.

**Root cause (from `2026-05-25-framework-evaluation.md` §Findings):** every internal compliance metric measures conformance to the framework's own rules. The framework grades its own homework. There is no external calibration loop that would surface "the rule produced a bad output even when followed."

**Ensemble verdict (from `2026-05-25-ensemble-synthesis.md` §1):** confidence 0.82; "internally consistent, externally untested." All three cold-context lenses converged on this diagnosis.

**Thesis:** Closing the highest-incidence empirical gap (file-existence check on sub-agent Write claims) and opening the only loop-exit channel (Wiktor monthly spot-check) delivers more framework reliability per unit of effort than continuing 7-delta architecture work in isolation.

---

## §2 — Goals

| ID | Goal | Success Criterion | Time Horizon |
|----|------|-------------------|--------------|
| G1 | Reduce undetected fabrication incidents | Hook-detected fabrications ≥ Wiktor-discovered fabrications; Wiktor-discovered rate drops from 5/2-weeks (current) to ≤1/month. Measured by: `governance-log.jsonl` entry count per category. | 30 days post-Item-1 ship |
| G2 | Establish external calibration cadence | Presence of monthly calibration entry in `Projects/Agent-Governance-Research/calibration/` directory with scored artifacts. Wiktor performs 20–30 minute spot-check on 5–10 random QA-PASS artifacts. | First entry within 45 days of PRD merge |
| G3 | Close Delta-1 SKILL.md routing gap | `mcp-server-architect` and `mcp-developer` appear as explicit domain rows in BOTH `process-build/SKILL.md` and `process-planning/SKILL.md`. Registry regen confirms presence: `grep mcp-server-architect .claude/registry.json` returns ≥1 match. | 14 days post-PRD merge |
| G4 | Investigate actual classifier-block-vs-emission gap | EMPIRICAL CORRECTION 2026-05-25 round-1 review: `\bpm\b` against `pm-orchestrator` returns `True` (Python `re` confirmed; `-` is word boundary). Item 3 as originally scoped is a no-op fix. Restated G4: identify the actual cause of the 47-blocks-vs-42-emissions classifier ratio (candidates: dispatch-text `(.+)` capture truncation at line 114, multi-line MUST DISPATCH lines, or another regex). Success criterion: written diagnosis at `Projects/Agent-Governance-Research/work/2026-05-25-classifier-block-ratio-diagnosis.md` with reproducible failing input. | Diagnosis ships before any code change in classifier-field-check.py |
| G5 | Answer strategic investment question | Written decision (≥100 words) at `Projects/Agent-Governance-Research/calibration/sprint4-investment-decision.md` stating one of: continue deltas / shift to external instrumentation / hybrid with allocation split. | After Items 1–4 ship and first calibration entry exists |

---

## §3 — Non-Goals

- **The other 11 ensemble concerns** from the B3 concerns table (rows 1–3, 6–9, 11, 14, and others). Deferred to future sprints per Sprint-2 PM lean-PRD verdict.
- **Reorganizing or superseding the 7-delta architecture-v2 spec.** Items 1 + 2 intersect Deltas 1, 5, and 7. They complement; they do not replace.
- **Proposing changes to Wiktor-authored CLAUDE.md prose.** Any CLAUDE.md edit required by Item 2 is a routing-table/registry sync (derived/auto-maintained layer), not a prose change to CRITICAL RULE blocks or Working Philosophy.
- **Shipping Item-3 regex fix as a standalone commit.** Batched with Item 1.
- **Quantifying framework ROI in dollar terms.** Wiktor is on Claude Max 5x flat-rate; cost-summary.py is a usage proxy (`reference_wiktor_on_claude_max_5x_subscription.md`).

---

## §4 — User Stories

**US1 — Item 1: Sub-agent file-existence check.**
As Wiktor, I want the work-verification-check hook to detect when a sub-agent claims to have Written a file that does not exist on disk, so that fabricated Write claims are blocked by the framework rather than discovered manually during my review.

**US2 — Item 2: Delta-1 SKILL.md MCP routing rows.**
As Wiktor, I want `process-build/SKILL.md` and `process-planning/SKILL.md` to carry explicit MCP domain rows routing to `mcp-server-architect` and `mcp-developer`, so that these specialists are discoverable via skill routing tables and not only through the DISPATCHES.json fallback path.

**US3 — Item 3: `\bpm\b` regex fix in classifier-field-check.py.**
As Wiktor, I want the classifier-field-check hook to correctly recognize `pm-orchestrator` as a valid agent name rather than mis-matching it as a bare `pm` token, so that legitimate pm-orchestrator dispatches are not blocked or warned.

**US4 — Item 4: Action 0.1 external calibration protocol.**
As Wiktor, I want a documented calibration protocol with sample-selection script, scoring rubric, and monthly cadence reminder mechanism, so that I have a structured, low-overhead path to perform 20–30 minute spot-checks that close the external-calibration gap.

**US5 — Item 5: Closed-loop strategic investment question.**
As Wiktor, I want a clear written answer to whether further framework hardening (Deltas 2–7 of architecture-v2) is worth continued investment OR whether budget should shift to loop-exit instrumentation, so that I can make a single high-leverage allocation decision instead of approving 7 incremental deltas in isolation after 3 sprints inside the same loop.

---

## §5 — Acceptance Criteria

### US1 — File-existence check

**AC1.1** — A sub-agent response that includes text matching a Write-claim pattern (e.g., "I have written", "File saved at", "Written to disk") for a path that does not exist on disk → `work-verification-check.py` emits `FABRICATION_DETECTED` to stderr and exits with code 2 (block). Existing hook structure at `work-verification-check.py` lines 1–70 is the attachment point. Falsifier: submit a mocked sub-agent response with a fake Write claim; if hook does not block with exit code 2, AC fails.

**AC1.2** — A sub-agent that returns content inline (no Write tool call, no Write-claim language) → hook does not block. Check gates on explicit Write-claim language in the agent output text, NOT on Write-tool absence from the trace. Falsifier: dispatch a sub-agent configured to return inline only with no Write-claim language; if hook blocks it, AC fails.

**AC1.3** — Every `FABRICATION_DETECTED` event appends a JSON line to `Projects/Agent-Governance-Research/governance-log.jsonl` with fields: `timestamp`, `agent_type`, `claimed_path`, `actual_exists: false`, `detection_source: "work-verification-check"`. Falsifier: trigger the hook; inspect the log; if entry absent or missing fields, AC fails.

**AC1.4** — Commit containing the file-existence check also contains the `\bpm\b` regex fix (Item 3). Falsifier: inspect git log; if changes are in separate commits, AC fails.

### US2 — Delta-1 SKILL.md MCP routing rows

**AC2.1** — `process-build/SKILL.md` and `process-planning/SKILL.md` each contain a row in their agent routing tables with: domain `mcp`, specialist `mcp-server-architect`, notes referencing `mcp-developer` as implementation agent. Falsifier: `grep -i "mcp-server-architect" .claude/skills/process-build/SKILL.md` returns empty; AC fails.

**AC2.2** — After SKILL.md edits, `python .claude/scripts/generate_registry.py` runs without error and `grep "mcp-server-architect" .claude/registry.json` returns ≥1 match. Falsifier: grep returns empty; AC fails.

**AC2.3** — `allowed_specialists_via_process_exemption` array in `process-build/DISPATCHES.json` (which contains mcp-server-architect, mcp-developer + 7 others per Sprint 1 A4 work) remains unchanged. SKILL.md row is additive there. Falsifier: process-build/DISPATCHES.json no longer contains `mcp-server-architect`; AC fails.

**AC2.4 — EMPIRICAL CORRECTION 2026-05-25 round-1 review:** `process-planning/DISPATCHES.json`'s `allowed_specialists_via_process_exemption` array contains ONLY `[llm-architect, data-engineer]` — does NOT contain `mcp-server-architect` or `mcp-developer`. Item 2 scope expands: in addition to SKILL.md routing row, `process-planning/DISPATCHES.json` must add both `mcp-server-architect` and `mcp-developer` to its `allowed_specialists_via_process_exemption` array. Falsifier: `grep "mcp-server-architect" .claude/skills/process-planning/DISPATCHES.json` returns empty; AC fails.

### US3 — Classifier block-vs-emission ratio diagnosis (RESCOPED ROUND-1)

**EMPIRICAL CORRECTION:** Original Item 3 ("`\bpm\b` regex rejects pm-orchestrator") is a FALSE PREMISE. Python `re.search(r'\bpm\b', 'pm-orchestrator')` returns `True` because `-` is a non-word character creating a word boundary. The 47-blocks-vs-42-emissions classifier ratio (from synthesis §3) has a different root cause that has not been diagnosed.

**AC3.1** — Written diagnosis exists at `Projects/Agent-Governance-Research/work/2026-05-25-classifier-block-ratio-diagnosis.md` covering: (a) reproducible failing input (the exact text in the assistant turn that triggered a false block), (b) the specific code path through `classifier-field-check.py` that produced the false negative, (c) the actual fix or "no fix needed if signal is correct." Falsifier: diagnosis file absent, OR fails to identify a specific code path or claim "no actual bug."

**AC3.2** — If a fix lands, it ships with regression test against 10+ CLASSIFIER_AGENT values that includes `pm-orchestrator` explicitly. Falsifier: any previously-passing agent name blocks after fix.

**AC3.3** — If diagnosis concludes "no bug" (the ratio is correct signal, not noise), the PRD's Goal G4 is closed with that finding documented. Falsifier: diagnosis is ambiguous between bug and signal.

### US4 — Calibration protocol

**AC4.1** — `Projects/Agent-Governance-Research/calibration/protocol.md` exists and specifies all four required fields: (a) sample size 5–10 artifacts per session, (b) sample-selection script path or inline command, (c) scoring rubric with PASS/FAIL criteria for QA artifacts, (d) monthly cadence reminder mechanism. Falsifier: any of the four absent; AC fails.

**AC4.2** — A session-start check fires if no calibration entry exists in `Projects/Agent-Governance-Research/calibration/` dated within the last 35 days, surfacing last-calibration date and protocol document path. Pattern: model on `lint-cadence-trigger.py` + `.claude/hooks/_state/lint-cadence.json`. Falsifier: simulate >35-day gap; if no reminder fires, AC fails.

### US5 — Strategic investment question

**AC5.1** — `Projects/Agent-Governance-Research/calibration/sprint4-investment-decision.md` exists, ≥100 words, explicitly states one of: continue delta hardening (with rationale), shift to external instrumentation (with rationale), or hybrid with explicit allocation split. Falsifier: file absent or no stated direction; AC fails.

**AC5.2** — Decision document's `date` frontmatter ≥ Items 1–4 merge date AND references at least one calibration entry as evidence. Falsifier: decision predates Item 1 ship OR cites no calibration entry; AC fails.

---

## §6 — Risks

**R1 — Item-1 false-positive risk (HIGH probability, LOW severity).**
The hook fires on sub-agents that legitimately return content inline (research synthesizer returning a report in response text without Writing a file). Mitigation: gate the check exclusively on explicit Write-claim language patterns in the response text, not on Write-tool absence from the trace. Extend the existing pattern list in `work-verification-check.py` rather than adding a new detection branch.

**R2 — Item-4 cadence-decay risk (HIGH probability, MEDIUM severity).**
Wiktor commits to monthly calibration at protocol ship but cadence slips after 1–2 months. Historical precedent: `lint-cadence-trigger` was built precisely because cadence-decay is the documented failure mode for periodic review tasks in this vault. Mitigation: ship the session-start reminder (AC4.2) at the same time as the protocol document — do not ship protocol without reminder.

**R3 — Item-2 schema-mismatch risk (MEDIUM probability, HIGH severity).**
SKILL.md routing tables are read by `classifier-field-check.py`, `generate_registry.py`, and the skill loader. A row addition not matching the expected schema silently misroutes MCP work — no error, wrong specialist dispatched. Mitigation: post-edit, (a) run `generate_registry.py` and verify no parse errors, (b) grep `mcp-server-architect` in BOTH SKILL.md and registry.json, (c) run `classifier-field-check.py` against a test payload with `DOMAIN: mcp` and confirm no block.

**R4 — Closed-loop investment-bias risk (HIGH probability, HIGH severity — source: `2026-05-25-framework-evaluation.md` §Recommended Actions).**
3 sprints inside the framework. Continued hardening without loop-exit produces confident-but-untested rules. Ensemble synthesis confidence 0.82 cannot distinguish "we are right" from "we agree with ourselves." Mitigation: Item 5's strategic answer must be reached and documented BEFORE any further delta work starts. The decision document (AC5.1) gates Sprint 4 scope; if the answer is "continue deltas," that decision must cite calibration evidence, not framework-internal metrics.

**R5 — implementation-plan fabrication risk (CONFIRMED HIGH — 5 incidents in 2 weeks, this PRD = incident 5).**
This PRD itself was claimed-but-not-written by implementation-plan agent at 18:14. Until Item 1 ships, every downstream sub-agent dispatch is at risk of the same failure mode. Mitigation interim: main session manually runs `ls -la` after every sub-agent dispatch claiming file output. Mitigation permanent: Item 1 ship.

---

## §7 — Sequencing Recommendation

**Step 1 — Item 3 (regex fix).** Smallest blast radius; one-line change. Batched with Item 1 per §3 Non-Goals.

**Step 2 — Item 1 (file-existence check).** Bounded autonomous build; ~20–30 lines added to `work-verification-check.py`; fully reversible via `git revert`. Highest-urgency item: 5 fabrications caught manually, 0 by the framework. Ships in the same commit as Item 3 to satisfy AC1.4. Dependency: must run AFTER Item 3 commits to the same change-set so both land together.

**Step 3 — Item 2 (Delta-1 SKILL.md MCP routing rows).** Doctrine sync; requires registry regen. Lower urgency than Items 1+3 because the DISPATCHES.json fallback already provides minimum authorization. SKILL.md rows provide skill-level discoverability that DISPATCHES.json does not — additive, not emergency. Depends on Step 2 (Item 1) being stable so registry regen reflects clean state.

**Step 4 — Item 4 (calibration protocol).** Wiktor-gated. Protocol document drafted autonomously; monthly cadence is irreducibly human. Depends on Item 1 shipping so the protocol can reference actual governance-log entries. Session-start reminder ships with the protocol in the same PR.

**Step 5 — Item 5 (strategic question).** Answered after Items 1–4 ship so the answer reflects post-improvement state. Answering before means the strategic call is grounded in pre-improvement evidence, which defeats the purpose.

---

## §8 — Open Questions with Proposed Answers

### Q1 — Monthly spot-check commitment: will Wiktor actually do it?

**Source:** B3 concerns table row 4 · `2026-05-25-framework-evaluation.md` §Recommended Actions (Action 0.1)

**Question:** Action 0.1 proposes a monthly 20–30 minute Wiktor spot-check on 5–10 random QA-PASS artifacts. Does Wiktor commit to this cadence; and if cadence slips, what is the fallback?

**Proposed answer:** Commit, but do not depend on commitment holding. The session-start reminder (AC4.2, modeled on `lint-cadence-trigger.py`) is the enforcement layer. If cadence slips >35 days, framework surfaces it at next session start. If two consecutive months are missed, calibration cadence is downgraded to "on-demand" and the Q7 strategic answer defaults to "pause delta work until calibration resumes." Commitment is made explicitly in writing, not assumed by silence.

**What would falsify:** Evidence that session-start reminders are routinely dismissed without action. In that case a stronger gate (block Sprint start on missing calibration entry) is needed.

**Confidence:** medium · **Reversibility:** reversible

---

### Q2 — PM-suppression protocol: when should /pm suppress hook signals?

**Source:** B3 concerns table row 5

**Question:** pm-orchestrator may emit hook signals that conflict with or duplicate other hooks. When should /pm suppress these? Is there a defined protocol?

**Proposed answer:** No suppression protocol today; there should be one, scoped narrowly. Suppress in exactly one case: when Wiktor has explicitly issued a PM-halt instruction (`feedback_url_handoff_doesnt_auto_extend_research.md` — "URL handoff during PM-halt = ASK first"). Protocol: (a) check for active PM-halt flag in session state before emitting any hook signal, (b) if set, log the suppressed signal to `governance-log.jsonl` with `suppressed: true` but do not propagate. Suppression is auditable, not silent.

**What would falsify:** A case where the PM-halt flag is incorrectly set (e.g., by sub-agent misreading session state) and suppression silences a legitimate signal. If that mode is common, the trigger needs to be narrower.

**Confidence:** medium · **Reversibility:** reversible (governance-log captures suppressed entries — no data loss)

---

### Q3 — Wiki bootstrap pages: retroactive ratify or revert?

**Source:** B3 concerns table row 10 · `CLAUDE.md` §Karpathy LLM-Wiki Architecture (Bootstrap mode)

**Question:** How many bootstrap pages currently lack Wiktor ratification, and should they be retroactively ratified, reverted to raw layer, or held?

**Proposed answer:** Hold, do not retroactively ratify or revert. Retroactive ratification bypasses the review bootstrap mode was designed to enforce. Retroactive reversion is destructive. Correct resolution: (a) surface count of unratified bootstrap pages via process-lint, (b) Wiktor reviews ≤10 pages at a time, (c) passes promoted, failures moved to `archive/` with a note. ≥10-ratified threshold gates full LLM-authorship mode; it must not be reached through bulk unreviewed ratification.

**What would falsify:** Count ≥50 AND content already cited in downstream wiki pages — in that case, review cost may exceed value and a one-time bulk spot-check (rather than full review) might be warranted.

**Confidence:** high · **Reversibility:** reversible (no action taken; current state preserved)

---

### Q4 — dark-zone-check hook: deprecate or keep?

**Source:** B3 concerns table row 12

**Question:** The dark-zone-check hook is flagged as a deprecation candidate. What is its current function, and is there a replacement?

**Proposed answer:** Do not deprecate without a replacement. dark-zone-check enforces that sub-agents do not write to protected vault paths (CLAUDE.md, hook files) without explicit authorization — the only hook enforcing write-path governance. If deprecated, protection gap is immediate. Correct disposition: (a) verify current hit-rate in `governance-log.jsonl` over 30 days, (b) if zero hits, check whether protection is redundant with another hook before removing it, (c) if not redundant, the hook stays. Deprecation requires evidence of redundancy, not just low hit-rate.

**What would falsify:** Evidence of high false-positive rate generating noise or blocking legitimate writes — then targeted deprecation or rule narrowing is warranted.

**Confidence:** medium · **Reversibility:** reversible if deprecated; irreversible if protection gap exploited before restoration

---

### Q5 — Evaluative-reviewer Write tool reversal

**Source:** B3 concerns table row 13 · `2026-05-25-aw5-smoke-test-adversarial.md`

**Question:** AW-5 smoke-test found evaluative agents (adversarial-reviewer, architect-reviewer, code-reviewer) should NOT have Write tool — the grant lets a reviewer modify the artifact it is reviewing. Revoke Write from all evaluative-reviewer types?

**Proposed answer:** Yes, revoke Write from evaluative-reviewer agent types. Meta-evidence: the adversarial-reviewer that produced the reversal recommendation was itself dispatched with the new Write grant — it surfaced the reversal. The recursion is genuine evidence, not irony. The Write grant was added (`feedback_subagents_should_have_write_tool.md`) for sub-agents to produce review reports to disk — but the correct scope is path-scoped Write (write to `work/` for reports) NOT blanket Write that includes the artifact under review. Fix: per-agent path-scoped Write constraint OR explicit exclusion list in agent frontmatter, NOT blanket Write revocation (which would prevent report filing entirely).

**What would falsify:** A documented case where an evaluative agent needs Write access to the artifact under review for a legitimate purpose (e.g., inline annotation). None documented yet; until one is, revocation stands.

**Confidence:** high · **Reversibility:** reversible (Write can be re-granted; no data destroyed by revocation)

---

### Q6 — Doctrine-revision falsification gate

**Source:** B3 concerns table row 15 · `CLAUDE.md` §CRITICAL RULE: Self-Invoke /hookify

**Question:** Should every CLAUDE.md edit require a falsifier statement before merge — a sentence stating what evidence would make the proposed rule wrong?

**Proposed answer:** Yes, lightweight gate. Add one field to the `feedback_*.md` memo template: `falsifier:` — one sentence stating what evidence would make the rule wrong. Not a new approval step; a field added to the existing memo template. Cumulative value: in 6 months, the collection of falsifier statements is the first pass of a systematic review. Without falsifiers, every rule is defended by "we added it because of an incident" — not falsifiable by design.

**What would falsify:** If the falsifier field is consistently left blank (~25% compliance per CLAUDE.md Working Philosophy principle 2 on soft instructions) the field needs hook enforcement, not just documentation.

**Confidence:** medium · **Reversibility:** reversible (optional metadata)

---

### Q7 — Closed-loop strategic investment: delta hardening vs external instrumentation?

**Source:** B3 concerns table row 16 · `2026-05-25-ensemble-synthesis.md` §6 · `2026-05-25-framework-evaluation.md` §Recommended Actions

**Question:** Sprint 4 — continue architecture-v2 delta hardening (Deltas 2–7), OR shift to external instrumentation (calibration protocol, governance-log dashboarding, promptfoo Tier-3)?

**Proposed answer:** Sequential, not either/or. Ship Items 1+3 first (lowest cost, highest empirical incidence — 5 documented fabrications, 0 framework detections), then Item 4 (calibration protocol — the only proposed loop-exit), then re-evaluate. The architect lens (synthesis §3) treats remaining deltas as critical-path; the adversarial lens (synthesis §2) recommends Action 0.1 first. Resolution by sequencing: Items 1+3 close the most-documented gap; Item 4 opens the loop-exit; Q7 final answer (decision document AC5.1) is reached only after one calibration entry exists. If calibration data shows QA-PASS artifacts failing Wiktor's rubric at >20%, the deltas are not the priority — the QA process itself is broken. If <5%, deltas become the right next investment.

**Why not continue deltas immediately:** 5 fabrication incidents that triggered this sprint were NOT caught by any delta. Continuing delta work before closing the fabrication detection gap is building in the wrong direction.

**Why not abandon deltas entirely:** The architect lens identified real routing gaps (Delta-1 SKILL.md) and real schema risks (Delta-5 dual-emit). These have documented failure modes. They belong in post-calibration sprint, not the trash.

**What would falsify:** Calibration data showing QA-PASS artifacts are high-quality across the board AND fabrication incidents were outliers rather than a systemic rate. Then delta work IS the right next investment, with calibration as the justifying evidence.

**Confidence:** high (on sequencing) / medium (on post-calibration direction — depends on calibration evidence) · **Reversibility:** reversible at every step

---

## §9 — Round-1 Review Findings & Preserved Divergence

Both lenses returned NEEDS-CHANGES.

### Convergent findings (both reviewers, applied above)

1. **Item 3 regex premise false.** Empirical verification in Python confirmed `\bpm\b` matches `pm-orchestrator`. G4 restated to require diagnosis before fix. AC3.1–3.3 rewritten.
2. **DISPATCHES.json factual error.** process-planning has only `[llm-architect, data-engineer]`. AC2.4 added; Item 2 scope expanded.
3. **Item 4 cadence-decay mitigation weak.** Session-start reminder is the same soft-instruction class CLAUDE.md cites at ~25% compliance. Acknowledged below as preserved-disagreement item Q8.
4. **§7 unnamed human gate** between Item 4 ship and Item 5 start (first calibration entry needs Wiktor execution, not just protocol document). Acknowledged below; NOT silently closed.

### Divergent findings (per the surface-divergent-verdicts doctrine — preserved, NOT collapsed)

**Q8 — Incident-5 inference direction.**
- **architect lens** (Round-1, accepted): incident 5 supports Item 1 (hook is needed; 5 incidents, 0 hook detections).
- **adversarial lens** (Round-1, NOT accepted into PRD body): incident 5 supports main-session verification (every incident was caught; argues Item 1 is ergonomic automation of a working manual step, not closure of an open gap).
- **PRD position:** the two lenses agree Item 1 has value. They disagree on framing (closing-a-gap vs ergonomic-automation) and on the urgency multiplier. Reframing changes nothing in Item 1's implementation but changes the strategic argument for prioritizing it above Items 2-5. **Wiktor call required.** Default: ship Item 1 with adversarial's reframing acknowledged in §1 problem statement (it is an ergonomic automation of an already-working main-session verification — that's still a worthwhile build, not a closure of an unrecovered-failure gap).

**Q9 — Item 1 detection mechanism: language-pattern vs Write-tool-trace-absence.**
- **architect lens:** AC1.1 needs transcript-path architecture clarification (assistant block vs tool_result block); the existing parsing at lines 100-140 only handles `assistant` blocks, so sub-agent output requires SubagentStop hook or expanded parsing.
- **adversarial lens:** the correct signal is Write-tool-trace-absence + path-existence check, NOT language-pattern matching (which has structural false-positive problem because legitimate file-writing agents also produce Write-claim language). AC1.2 explicitly forbids the trace-based signal.
- **PRD position:** architect's transcript-path observation is technical; adversarial's signal-precision argument is structural. Both apply. **Implementation must use Write-tool-trace-absence as primary signal AND check tool_result blocks (not just assistant blocks).** AC1.1 + AC1.2 should be revised at implementation-plan time (not in this PRD) to reflect this combined approach. Flagged for the build-phase ticket.

**Q10 — Item 4 enforcement mechanism strength.**
- **architect lens:** cadence-decay risk acknowledged; AC4.2 reminder is sufficient mitigation.
- **adversarial lens:** AC4.2 is soft-instruction theater per CLAUDE.md's own ~25% compliance citation. The hook is dressed as enforcement but acts as a reminder.
- **PRD position:** acknowledged tension. Soft enforcement is the LIGHTEST viable mechanism; harder enforcement (e.g., block Sprint start on missing calibration entry) is a stronger fallback if AC4.2 proves insufficient. **Default: ship AC4.2; if cadence slips through 2 cycles, escalate to harder gate.** Flagged for re-evaluation at first calibration cadence audit.

**Q11 — Selection logic for Items 1-5 vs the 11 deferred concerns.**
- **architect lens:** Non-Goals section appropriately disclaims the 11 deferred concerns.
- **adversarial lens:** synthesis §6 ranks items 4 (`process-step-check.py` soft-to-hard, closes 53% MUST DISPATCH compliance gap), 5 (n8n routing block), 7 (PM checkpoint suppression), 8 (adversarial DISPATCHES reconciliation) HIGHER than Item 2 (Delta-1 routing rows). PRD deferred higher-ranked items without explanation — "lean" justification cites internal framework artifact, which is the closed-loop problem applied to scope selection.
- **PRD position:** adversarial's critique is correct on the data. Items 1-5 were selected by Sprint-2 PM verdict per the loop queue; the synthesis ranking suggests Items 1, 4 (Action 1.1 file-existence — covered by this PRD's Item 1) are highest empirical value but Items 2, 5 (current PRD's Item 2) are NOT the next-highest. **Wiktor call required on whether Sprint 4 should swap in synthesis §6 item 4 (process-step-check.py soft-to-hard) ahead of PRD Item 2.** Default: ship Items 1+3-diagnosis first (no change), surface this swap to Wiktor at sprint-3-boundary PM checkpoint.

**Q12 — Wiktor-decision overreach in §8 Q1-Q7.**
- **adversarial lens:** Q3, Q5, Q6 are Wiktor-gated per source concerns table; PRD's proposed-answer format with confidence ratings exceeds authorization.
- **PRD position:** acknowledged. The proposed answers stand as Claude's recommendation but are explicitly NOT Wiktor decisions until Wiktor reads §8 and confirms or overrides. The confidence ratings are Claude-internal; they do not bind Wiktor.

### Additional risks added (architect lens R6-R8)

- **R6 — Item 3-replacement regression risk.** A fix in `classifier-field-check.py` line 114 capture or elsewhere may widen blocks to substrings of canonical agent names. Mitigation: regression test set MUST include every agent name from `.claude/registry.json` plus all common false-positive patterns (`pm` as bare token in non-dispatch context).
- **R7 — governance-log.jsonl write contention.** Multiple hooks (classifier-field-check, work-verification-check, process-step-check) write the same file via plain `open(log_path, "a")` with no locking. Item 1 adds another writer. On Windows with concurrent sub-agent Stop hooks, file-lock contention is a real failure mode. Mitigation: add `fcntl` (POSIX) or `msvcrt.locking` (Windows) advisory lock OR migrate to a single writer-thread pattern. Lowest cost: keep current append behavior but add a corruption-detection script in `process-lint`.
- **R8 — Calibration sample-selection bias.** AC4.1(b) requires a sample-selection script path. The script MUST produce a cryptographically random sample (e.g., `random.SystemRandom().sample(qa_pass_entries, k=7)`) NOT a Wiktor-curated list. If Wiktor selects, the sample is not random, and the correlation measurement is degraded to noise. Mitigation: protocol document mandates `python -m secrets`-backed random selection; Wiktor can refuse to score specific samples (recused), but cannot pick them.

### Architect-flagged log-path conflict (AC1.3)

**Resolution:** The hook log SHOULD remain at `.claude/hooks/governance-log.jsonl` (existing path, all other hooks write here). AC1.3 corrected: `FABRICATION_DETECTED` events append to `.claude/hooks/governance-log.jsonl`, not to a project-local path. G1 measurement reads the same file.

---

## Appendix — Source Citations Index

| Claim | Source File | Section / Lines |
|-------|-------------|-----------------|
| 5 fabrication incidents (incident 5 = this PRD) | memory folder + main-session verification 2026-05-25 18:14 | Full memos + governance-log entry |
| "internally consistent, externally untested" | `2026-05-25-ensemble-synthesis.md` | §1 Convergent Verdicts |
| Ensemble confidence 0.82 | `2026-05-25-ensemble-synthesis.md` | §1 |
| Wave C PRD must-address items | `2026-05-25-ensemble-synthesis.md` | §6 |
| 16-row concerns table, 7 Wiktor-gated | `2026-05-25-framework-org-loop-queue.md` | §Ensemble Concerns Table |
| 7-delta architecture spec | `2026-05-25-agent-governance-architecture-v2.md` | Deltas 1–7 |
| Action 0.1, Action 1.1 | `2026-05-25-framework-evaluation.md` | §Recommended Actions |
| Framework grades own homework | `2026-05-25-framework-evaluation.md` | §Findings |
| Hook structure (Write event gating) | `.claude/hooks/work-verification-check.py` | Lines 1–70 |
| `\bpm\b` regex | `.claude/hooks/classifier-field-check.py` | ~Line 115 |
| process-build routing table | `.claude/skills/process-build/SKILL.md` | Routing table section |
| process-planning routing table | `.claude/skills/process-planning/SKILL.md` | Routing table section |
| DISPATCHES.json MCP fallback | `.claude/skills/process-build/DISPATCHES.json` + `process-planning/DISPATCHES.json` | `allowed_specialists_via_process_exemption` |
| Evaluative-reviewer Write reversal | `2026-05-25-aw5-smoke-test-adversarial.md` | Full file |
| Write grant rationale | `feedback_subagents_should_have_write_tool.md` | Full file |
| Bootstrap mode, ≥10 ratified threshold | `CLAUDE.md` | §Karpathy LLM-Wiki Architecture |
| Lint-cadence pattern | `.claude/hooks/lint-cadence-trigger.py` + `lint-cadence.json` | Session-start reminder pattern |
| PM-halt suppression case | `feedback_url_handoff_doesnt_auto_extend_research.md` | Full memo |
| Hookify + feedback memo requirement | `CLAUDE.md` | §CRITICAL RULE: Self-Invoke /hookify |
| ~25% compliance with soft instructions | `CLAUDE.md` | §Working Philosophy principle 2 |
| Adversarial lens: Action 0.1 first | `2026-05-25-ensemble-synthesis.md` | §2 |
| Architect lens: deltas critical-path | `2026-05-25-ensemble-synthesis.md` | §3 |
