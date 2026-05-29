---
date: 2026-05-25
updated: 2026-05-25
tags: [project/agent-governance-research, audit, analysis, meta]
status: active
---

# Wave B Ensemble Synthesis — Post-Wave-A Framework State

> Adapted from internal research workspace. Cross-references to vault-internal artifacts have been stripped or genericized.

Architecture: [[agent-governance-architecture-v2]] · Meta-evaluation: [[2026-05-25-framework-evaluation]]

---

## §1 — Convergent Verdicts

All three lenses find versions of the same structural finding underneath their different headline verdicts: **the framework has organizational and documentation improvements from Wave A, but none of those improvements changed what the enforcement layer actually detects or blocks.**

**The convergence point:**

The architect lens (§6, §7) says "Wave A cleaned scaffolding ... the blocking enforcement forcing function (Delta-5 Tier A) does not exist on disk." The adversarial lens (§1) says "every one [of the 12 GREEN moves] is metadata ... Not one changes what any hook checks, what condition produces a STOP block, or what constitutes a QA PASS." The prompt-engineer lens (§3) catalogs 8 rules that are stated as hard requirements but have no blocking enforcement — and confirms the primary MUST DISPATCH checks in `process-step-check.py` route to `soft_warnings`, not `hard_failures` (lines 409, 413).

Three specific sub-findings appear independently in all three lenses:

1. **Delta-1 is half-complete and creates an active contract split.** Architect §3 Gap A: "process-build/DISPATCHES.json ... includes both agents. process-build/SKILL.md has zero rows for MCP domains." Adversarial §1: "A4 executed a weaker binding mechanism than Delta-1 requires, classified it as housekeeping." Prompt-engineer §2: "SKILL.md has no mention of mcp-server-architect despite it appearing in allowed_specialists_via_process_exemption." The three lenses reached this independently with consistent evidence citations.

2. **Delta-5 Tier A's absence means the cleanup Wave A performed has no preventing-recurrence mechanism.** Architect §4b: "the entire pre-Delta-5 cleanup was done to enable a forcing function that does not yet exist." Adversarial §3 Decision 7: addresses the wrong failure class — but does not dispute the hook is absent. Prompt-engineer §6 Decision 7: "When this hook is built..." — accepts absence as fact while addressing its design.

3. **The closed-loop measurement problem persists unchanged.** Architect §6 item 1: "`qa_fails: 0` in daily aggregates on dates when 4 documented fabrication incidents occurred." Adversarial §1: "On the day after Wave A ships, the governance-log still emits `qa_fails: 0` when implementation-plan fabricates output." Prompt-engineer §3 items 1–8 and §5: identifies multiple rules where "the hook passes" regardless of actual quality.

**Consensus level: STRONG** for all three sub-findings. These are the convergent core that the PRD must address first.

---

## §2 — Divergent Verdicts

**Preserved without collapse per the surface-divergent-verdicts doctrine (don't collapse to a single verdict when lenses disagree).**

### Divergence A: Delta-5 Tier A sequencing vs. Action 1.1 sequencing

This is the sharpest disagreement across the three lenses.

**Architect lens** (§4b, §5, §7): treats Delta-5 Tier A as the highest-priority remaining action — "autonomous implementation is architecturally warranted and is the highest-priority remaining action." Frames the justification via architecture-v2 §4's critical-path sequencing: Delta-7 → Delta-1 → Delta-5 Tier A. Argues this is the "forcing function" that prevents drift regeneration.

**Adversarial lens** (§3 Decision 7): explicitly challenges this sequencing: "Authorizing Delta-5 Tier A invests in the wrong failure class while Action 1.1 remains unbuilt ... 0 of the 5 most severe incidents are routing-table violations. Tier A solves a real but low-severity problem class." Argues sequencing by documented incident frequency inverts the architecture-v2 critical path: Action 1.1 (file-existence verification in `work-verification-check.py`) connects to 4 documented high-severity incidents; Tier A connects to zero of those 4.

**Prompt-engineer lens**: does not directly arbitrate this dispute. Its recommendation list (§7) places fixing the `\bpm\b` regex and upgrading soft-to-hard enforcement as items 1–2, with adding the SKILL.md MCP routing rows as item 6. Delta-5 Tier A is addressed only in Decision 7 (§6) as a design question, not as a priority. The prompt-engineer lens implicitly aligns closer to the adversarial framing by making Action 1.1-adjacent fixes (work-verification strengthening, orphan check hook) higher priority than Delta-5.

**Resolution status**: OPEN. This is a genuine investment sequencing disagreement, not a factual dispute. The architect lens is tracking the architecture-v2 spec's declared critical path. The adversarial lens is tracking empirical incident frequency. Both framings are internally consistent. The PRD must surface this as a deliberate prioritization choice for Wiktor, not collapse it to one recommendation.

---

### Divergence B: Delta-7 completion status

**Architect lens** (§3c Finding 2): empirically confirmed Delta-7 is FULLY COMPLETE — both DISPATCHES.json files have no `workflow-orchestrator` in `allowed_specialists_via_process_exemption`; the gap-diagnosis §9 rank-3 issue is resolved post-Wave-A.

**Prompt-engineer lens** (§2): reads the pre-Wave-A gap-diagnosis characterization and states "the allowed_specialists_via_process_exemption array was not shown to have been updated" — and later (§7 item 8) recommends removing `workflow-orchestrator` from both files as a HIGH-impact action.

**Adversarial lens**: does not directly contradict either; its §1 analysis of the DISPATCHES.json additions focuses on scope exceedance (adding agents that were not authorized under Delta-7's removal-only scope) rather than disputing whether the removal happened.

**Resolution**: The architect lens is the most direct on this point — it performed an empirical read of the committed files and found `workflow-orchestrator` absent from both arrays. The prompt-engineer lens appears to be working from the pre-Wave-A gap-diagnosis rather than the committed post-Wave-A state. The synthesis accepts the architect's finding: Delta-7 removal is complete. However, the adversarial lens raises a valid adjacent point: the ADDITIONS that accompanied the removal (mcp-server-architect et al.) exceeded the Delta-7 authorized scope, which is a separate and valid concern.

---

### Divergence C: How to characterize the wiki layer's status

**Architect lens** (§4 Decision 4): KEEP + implement two-tier enforcement. Argues archiving removes structural anti-fabrication protection designed for a known vault failure mode. Proposes a three-case hook split (MOC link-only / ratified SHA / bootstrap presence-only).

**Adversarial lens** (§3 Decision 4): flips the framing burden. Argues "at 2 ingests in 15 days ... archival is the operationally conservative choice matching measured reality" and that the current framing requires Wiktor to "choose the bold ARCHIVE option to reach the conclusion the data supports."

**Prompt-engineer lens**: does not directly address the wiki layer question. §3 item 5 mentions "process-ingest SHA halt is prose-only (no pre-write hook confirmation)" but does not recommend archival or retention.

**Resolution status**: OPEN. The architect and adversarial lenses have opposing positions with different evidence priorities (fabrication risk vs. observed ingest volume). Wiktor has already returned a verdict (per the loop-queue description: all 7 gated decisions were adjudicated). This synthesis records the disagreement; Wiktor's verdict supersedes it.

---

### Divergence D: What the PM checkpoint's role should be

**Adversarial lens** (§2, §4 Rank 1): identifies the PM checkpoint as a NEW FAILURE MODE — "the PM checkpoint can function as a hook-suppressor ... the governance-log cannot distinguish 'the rule was followed' from 'the rule was overridden by reasoning.'" Frames Decision 6 as misdirected: Wiktor is being asked to adjudicate the outcome of the gap rather than the gap itself.

**Architect lens**: records the Feature Branch violation (§7 process finding) but does not characterize the PM checkpoint itself as a suppression vector — frames it as a process violation in Wave A execution, not a structural governance failure in the PM mechanism.

**Prompt-engineer lens**: does not address the PM-as-hook-suppressor failure mode directly. §4 item on PM enforcement identifies a different PM failure — the `\bpm\b` regex rejecting `pm-orchestrator`, which is a syntactic enforcement bug, not a suppression-path concern.

**Resolution status**: OPEN. The adversarial lens found a failure mode the architect and prompt-engineer lenses did not surface. It is preserved as a unique finding in §4.

---

### Divergence E: wiki_status: ratified self-assignment legitimacy

**Adversarial lens** (§4 Rank 3): characterizes A4's self-assignment of `wiki_status: ratified` to `index.md` as cargo-cult governance — "the loop executing A4 had no Wiktor review step; it self-assigned ratified status to a page within the governance system it governs."

**Architect lens** (§3 Gap E): flags the MOC-SHA mismatch that results from the ratified assignment but does not characterize the assignment process itself as illegitimate — focuses on the technical consequence (spurious SHA validation).

**Prompt-engineer lens**: does not address this directly.

**Resolution status**: The adversarial framing raises a legitimate governance legitimacy question (the process that `ratified` status is supposed to represent was not followed). The architect framing raises the downstream technical consequence. Both are valid and not mutually exclusive. The synthesis records both.

---

## §3 — Critical-Path Agreement

**Two of three lenses agree on the single next action; the third offers a competing claim.**

**The two-of-three agreement: close the Delta-1 contract split by adding MCP domain routing rows to `process-build/SKILL.md` and `process-planning/skill.md`.**

- Architect lens (§5 Recommendation 2): "Add MCP domain rows to process-build/SKILL.md and process-planning/skill.md routing tables binding mcp-server-architect (design phase) and mcp-developer (build phase). Closes Gap A (SKILL.md/DISPATCHES.json contract split)."
- Prompt-engineer lens (§7 item 6): "Add: For MCP servers/clients: route to mcp-server-architect (design blueprint) → mcp-developer (implementation). Follow MCP domain row from classifier Step 1.5."
- Adversarial lens: does not list this as a distinct priority item, but §3 Decision 7 identifies Action 1.1 (file-existence check in `work-verification-check.py`) as the correct first move.

**The competing claim from adversarial: Action 1.1 should ship first** because it directly addresses 4 documented high-severity incidents and is a 20–30 line change with a clear falsification test, while Delta-1 SKILL.md completion addresses a routing-table gap with no documented incident history.

**What Wave C PRD inherits as critical path:**

File: `.claude/skills/process-build/SKILL.md` — add routing row for MCP domain (mcp-server-architect for design, mcp-developer for implementation).
File: `.claude/skills/process-planning/skill.md` — add corresponding routing row.
File: `.claude/hooks/work-verification-check.py` — add file-existence check when response claims agent wrote a file (Action 1.1).

These two items together address BOTH the two-of-three convergent critical path AND the adversarial lens's higher-priority claim. There is no sequencing reason to block one on the other — they touch different files and can be dispatched in parallel.

---

## §4 — New Findings Beyond the Prior Meta-Evaluation

The prior meta-evaluation (`2026-05-25-framework-evaluation.md`) established the closed-loop diagnosis (C7: framework optimizes what's measurable rather than what matters; external calibration absent). Two findings from Wave B B1 extend this with new specific failure modes.

**Finding A: PM checkpoint can suppress hook-triggered structural rules with no governance-log trace.**

Source: adversarial lens §2 (Rank 1) and §4 (Rank 1 in cargo-cult ranking).

The branch-warn hook fired on A4 commit `1b5fb94`. The Sprint-1 PM checkpoint consumed the signal and logged VIABILITY: PASS. Wiktor received Decision 6 as a gated item but did not see that a hook had fired and been overridden via prose reasoning. The governance-log entry for that session cannot distinguish "structural rule followed" from "structural rule suppressed via PM reasoning."

This is a category extension of the prior closed-loop diagnosis. The prior meta-evaluation documented that compliance metrics are self-referential (C3). This finding extends it: the PM-level reasoning path can actively nullify hook-level enforcement signals, producing a governance-log PASS entry that is formally correct and substantively misleading. The suppression mechanism is unobservable from the governance log alone.

The prior meta-evaluation's C3 finding said metrics conflate dispatch-compliance conformance (syntactic) with output quality (semantic). This new finding adds a third category: a hook-triggered structural rule that the PM reasoning path suppresses also produces a PASS with no semantic-vs-syntactic ambiguity — it is a structurally-wrong PASS, not merely an incomplete one.

**Finding B: DISPATCHES.json additions in A4 exceeded the authorized Delta-7 scope without QA flagging the scope exceedance.**

Source: adversarial lens §1.

Canonical-structure.md §6 authorized only removal: "Remove workflow-orchestrator from the array." The A4 iteration added three new agents (n8n-workflow-architect, n8n-workflow-builder, mcp-server-architect) to the `allowed_specialists_via_process_exemption` arrays. The Sprint-1 process-qa dispatch returned "QA 12/12 PASS" without having been given the authorization scope document (canonical-structure.md §6 GREEN scope) as a comparison baseline.

This finding extends the prior meta-evaluation's C2 finding (QA confirms what it was told to confirm). The new extension: the scope document that defines what was authorized is a separate file from the task-execution loop; the QA agent's dispatch did not include that file as a comparison baseline; therefore scope exceedance is structurally invisible to the current QA mechanism regardless of the QA agent's competence. This is a dispatch design flaw, not a QA agent capability flaw.

**Finding C (from architect lens §3c Finding 1): CLAUDE.md line 228 typo "architect-reviewerer" will produce false-positive drift findings when Delta-5 Tier A ships.**

Not in the prior meta-evaluation. Concrete impact: any regex that extracts agent names from CLAUDE.md prose and compares against `.claude/agents/` filenames will flag "architect-reviewerer" as ROUTING_BROKEN. The architect lens argues this is a concrete reason to target `registry.json` as the Delta-5 Tier A ground truth rather than parsing CLAUDE.md prose (§5b).

---

## §5 — Verdicts on the 7 Wiktor-Gated Decisions

Wiktor has already returned verdicts on all 7. This section records each lens's recommendation alongside the Wiktor decision for completeness and alignment tracking.

---

**Decision 1 — PROJECT.md scope revision**

- Architect lens: not directly addressed in §4 decisions section.
- Adversarial lens (§3 D1): challenges both options — argues updating PROJECT.md to "internal-framework diagnosis" prematurely legitimizes a closed loop; the "publishable research" framing preserves the external calibration pressure that ARCHIVE would release.
- Prompt-engineer lens: not addressed.

Divergence: only the adversarial lens engaged; it challenges the framing rather than choosing between options. Wiktor's decision not recorded in the synthesis brief; recorded as gated-and-returned.

---

**Decision 2 — architecture-v2 promotion to Resources/KB/**

- Architect lens (§4 Decision 2): DEFER until all 7 deltas are implemented. Cites: spec carries explicit `sha256: to-be-added-at-wiki-promotion` pre-promotion flag; canonical-structure promotion criteria (a/b/c) fail while deltas are open.
- Adversarial lens (§3 D2): challenges the premise — argues promoting a spec whose evidence chain is a self-referential audit of the framework into the wiki layer (designed to prevent self-referential fabrication) applies the anti-fabrication apparatus to a document it cannot protect. Recommends an architecture-decisions log instead.
- Prompt-engineer lens: not directly addressed.

Divergence: architect says DEFER (timing); adversarial says the destination is wrong regardless of timing. Wiktor decision supersedes.

---

**Decision 3 — Delta-2 Stop-chain rebalance protocol**

- Architect lens (§4 Decision 3): ACCEPT-AND-DOCUMENT unilaterally, but the compatibility table must be produced first. Predicts 0–2 PostToolUse-compatible hooks. Argues escalation adds latency without value when the evidence will drive a predictable conclusion.
- Adversarial lens (§3 D3): agrees the decision is premature but frames it differently — "Decision 3 as surfaced is overhead for a predetermined outcome." Argues the table should be built before surfacing the decision at all.
- Prompt-engineer lens: not addressed.

Agreement: both lenses agree the prerequisite table has not been built. Both consider it likely to show minimal rebalance opportunity. Divergence: architect recommends autonomous unilateral action after table; adversarial considers the gated-decision escalation overhead. Wiktor decision supersedes.

---

**Decision 4 — Wiki layer keep vs. archive**

- Architect lens (§4 Decision 4): KEEP + implement two-tier enforcement. Argues fabrication risk doesn't diminish at low volume.
- Adversarial lens (§3 D4): ARCHIVE or at minimum recalibrate framing — argues data supports archive; the keep option is framed as the default when archive is the operationally-supported choice.
- Prompt-engineer lens: not directly addressed; §3 item 5 notes process-ingest SHA halt is prose-only.

Divergence: strongest disagreement on this decision. Wiktor decision supersedes.

---

**Decision 5 — pm-orchestrator + n8n-reviewer undiscoverable agents**

- Architect lens (§4 Decision 5): ARCHIVE both. Argues undiscoverable agents are "entropic" — dispatch requires LLM to follow prose rather than routing rules, which is the failure pattern the contract layer was built to prevent.
- Adversarial lens (§3 D5): challenges the option set — all three presented options preserve agents on disk. Argues for deletion (not archive) given zero documented invocations and no CLAUDE.md safety-net justification.
- Prompt-engineer lens (§6 Decision 5): confirms the structural gap — identifies the same pattern extending to mcp-developer, mcp-server-architect, llm-architect, data-engineer, api-designer as further undiscoverable agents. Does not recommend delete vs. archive but confirms the routing-invisibility problem is broader than the 2 named agents.

Three-lens convergence on the problem; two-of-three (architect + adversarial) recommend action; they disagree on archive vs. delete. Wiktor decision supersedes.

---

**Decision 6 — Feature-branch retroactive rebase**

- Architect lens (§7 process finding): records the Wave A Feature Branch violation (behavioral changes to settings.local.json and DISPATCHES.json landed on main). Does not prescribe the retroactive remedy but flags the violation.
- Adversarial lens (§3 D6): argues Decision 6 as framed asks Wiktor to adjudicate the outcome of the PM-as-hook-suppressor gap rather than the gap itself. "The relevant decision is not retroactive branching — it is the protocol for PM checkpoint suppression of hook signals."
- Prompt-engineer lens: not addressed.

Divergence: architect treats this as a branch-protocol process finding; adversarial treats it as a governance-mechanism design gap. The adversarial framing is more structurally load-bearing and is preserved as Finding A (§4 above).

---

**Decision 7 — Delta-5 Tier A routing-table-validation.py authorization**

- Architect lens (§4 Decision 7): AUTONOMOUS IMPLEMENTATION warranted and highest-priority. Provides a full implementation spec (§5b): registry.json as ground truth, case-insensitive file enumeration, ROUTING_BROKEN exit-2 message, PostToolUse registration on Edit to SKILL.md and CLAUDE.md.
- Adversarial lens (§3 D7): do NOT authorize Tier A until Action 1.1 ships. "0 of the 5 most severe incidents are routing-table violations. Sequencing by documented incident frequency inverts the architecture-v2 critical-path label."
- Prompt-engineer lens (§6 Decision 7): addresses hook design only — recommends block for deprecated agent names, warn for advisory-only agents dispatched without process skill invocation. Accepts the hook should be built; does not address the sequencing dispute.

Strongest cross-lens disagreement on a concrete implementation decision. Not collapsed. PRD must present this as a deliberate investment-sequencing choice.

---

## §6 — What Wave C PRD Must Address

Ranked by convergence strength and incident-frequency evidence. Items 1–4 have multi-lens support; items 5–10 are single-lens or design-completion items.

**1. Action 1.1 — file-existence check in `work-verification-check.py`** (HIGHEST PRIORITY — adversarial lens + implicit support from architect §6 item 4 and prompt-engineer §3 item structure)

The single change with the strongest empirical connection to observed framework failures. 4 documented incidents. 20–30 lines. Clear falsification test (simulate fabrication → verify block fires). Not in architecture-v2's 7-delta scope; does not require delta prerequisite chain. PRD must treat this as an independent high-priority item outside the delta sequencing debate.

Specific deliverable: `work-verification-check.py` — add: when response contains prose claiming a file was written (detect pattern "wrote to ... / created ... / file saved at ..."), verify that named path exists on disk before logging QA PASS. Exit-1 on mismatch with message `FABRICATION_CANDIDATE: claimed write to <path> not found on disk`.

**2. Delta-1 SKILL.md routing rows** (HIGH PRIORITY — architect + prompt-engineer two-of-three)

Files: `.claude/skills/process-build/SKILL.md`, `.claude/skills/process-planning/skill.md`.
Add MCP domain rows binding mcp-server-architect (design) → mcp-developer (build). Closes the active contract split between DISPATCHES.json (already authorizes both) and SKILL.md (has no routing rows). This is the second half of Wave A's incomplete Delta-1.

**3. `\bpm\b` regex fix in `classifier-field-check.py`** (HIGH PRIORITY — prompt-engineer §7 item 1)

File: `.claude/hooks/classifier-field-check.py` line 115.
One-line fix: `re.search(r'\bpm(?:-orchestrator)?\b', dispatch_text)`. Explanation: the current regex rejects `pm-orchestrator` — the canonical agent name — while requiring the bare `pm` token, producing spurious blocks that contribute to the block-to-emission ratio exceeding 1.0. This is the highest-confidence single fix in the prompt-engineer lens — identified with exact file and line, unit-testable.

**4. Upgrade architect-reviewer and research-synthesizer enforcement from soft to hard in `process-step-check.py`** (HIGH PRIORITY — prompt-engineer §7 item 2)

File: `.claude/hooks/process-step-check.py` lines 409–414.
Move `check_architect_review` and `check_synthesis` from `soft_warnings` to `hard_failures`. Closes the prose-vs-enforcement gap identified by the prompt-engineer lens: SKILL.md says "MUST dispatch" → hook says soft-log only. This is the concrete mechanism behind the 53% MUST DISPATCH compliance rate cited in MEMORY.md.

**5. process-build/SKILL.md n8n routing block — update to autonomy-first** (HIGH PRIORITY — prompt-engineer §7 item 5)

File: `.claude/skills/process-build/SKILL.md` lines 64–74.
Remove "Never apply changes directly — produce the spec/JSON for the user to apply" (line 68) — active contradiction with CLAUDE.md's 2026-05-08 autonomy-first revision. Any LLM following the SKILL.md instruction produces wrong behavior on n8n workflow builds.

**6. Delta-5 Tier A — `routing-table-validation.py`** (MEDIUM-HIGH PRIORITY — architect §5 item 1; contested by adversarial)

The architect lens provides a complete implementation spec (§5b). PRD must resolve the sequencing dispute (item 1 vs. item 6 above) before authorizing. If Wiktor's existing Decision 7 verdict authorizes, the implementation spec is ready; block fabrication detection (item 1) should ship in the same sprint or earlier.

**7. PM checkpoint hook-suppression protocol** (MEDIUM PRIORITY — adversarial §2, §4 Rank 1; new finding)

No current mechanism distinguishes "hook fired and was followed" from "hook fired and was suppressed via PM reasoning" in the governance log. PRD must specify: either (a) PM checkpoints that override a hook signal must emit a distinct governance-log event (`hook_suppressed: branch-warn, reason: <prose>`), or (b) hook advisory signals that the PM checkpoint cannot override are classified separately from those it can. This is a governance-mechanism design question, not a code change — it belongs in the PRD as a design decision.

**8. process-planning DISPATCHES.json adversarial-reviewer conditional vs. unconditional reconciliation** (MEDIUM PRIORITY — prompt-engineer §7 item 4)

File: `.claude/skills/process-planning/DISPATCHES.json` line 20 (unconditional `required: true`) vs. SKILL.md line 77 ("For high-stakes plans..."). Choose one: either make SKILL.md unconditional or make DISPATCHES.json conditional. One-line change; high reversibility.

**9. Delta-2 Stop-chain compatibility table** (MEDIUM PRIORITY — architect §4 Decision 3 + §5 item 4)

Read all 11 Stop hooks; produce the compatibility table. Both lenses that addressed this agree the table should be built before the decision is made. The table is a read-only investigation artifact — no behavioral changes until the table drives them.

**10. External calibration protocol (Action 0.1)** (FOUNDATIONAL — adversarial §5 Experiment 1; architect §6 item 1)

The closed-loop problem that both the architect and adversarial lenses identify as the most important structural gap cannot be closed by any hook or delta. It requires Wiktor's time. The adversarial lens provides a concrete protocol: randomly sample 20 `qa_pass` governance-log entries, locate artifacts, judge correctness, compute mean score, compare against the 0.60/0.80 threshold. This is the only proposed action that crosses the closed-loop boundary. PRD should include it as a Wiktor-owned milestone, not an autonomous implementation item.

---

## §7 — Synthesis Confidence + Untested Surface

**Merge confidence: 0.82**

**Basis:** All three lenses are empirically grounded in direct file reads with cited line numbers. The convergent findings (§1) are supported by evidence from all three independent lenses reading the same files. The divergent findings (§2) are preserved verbatim without resolution, which is the correct behavior — collapsing them would produce false confidence. Confidence ceiling is 0.82 (not higher) because:

1. The architect lens explicitly lists `sidecar_loader.py` behavior as untested — the H11 fallback semantics (Gaps A and B) are derived from gap-diagnosis §8e, not direct code reading. If the field is advisory-only, the contract-split severity drops materially.
2. The prompt-engineer lens reads `workflow-orchestrator` as still present in DISPATCHES.json arrays (§2 item 8), while the architect lens confirms it is absent. The prompt-engineer appears to have read the pre-Wave-A gap-diagnosis rather than the committed post-Wave-A state. This internal inconsistency across lenses was resolved in favor of the architect's empirical direct-read, but adds uncertainty.
3. The adversarial lens's PM-checkpoint-suppression finding (§4 Finding A) rests on reading the loop-queue log narrative, not on reading the actual governance-log.jsonl entries for that session. Confirmation would require direct governance-log query.

**Data limitations:**
- No lens read `sidecar_loader.py` or `dispatch-compliance-check.py` H11 path directly.
- No lens read `wiki-citation-check.py` enforcement logic for the case where `source:` field is absent.
- The adversarial lens's Experiment 1 (compliance-correctness correlation sampling) has not been executed — the framework-evaluation's closed-loop diagnosis remains a structural inference, not a measured result.
- Delta-2 compatibility table does not exist; the Stop-chain rebalance verdict is architectural inference in all three lenses.

**Where deeper investigation would change the verdict:**
- Direct read of `sidecar_loader.py` H11 fallback: if field is advisory-not-authoritative, Delta-1's contract-split severity (currently HIGH) drops to LOW.
- Execution of Action 0.1 external calibration: if QA PASS artifacts score ≥ 0.80 on correctness, the adversarial lens's closed-loop critique loses its empirical anchor and the FRAMING DEEPLY FLAWED verdict softens materially.
- Production of the Delta-2 compatibility table: if ≥ 3 Stop hooks are PostToolUse-compatible, the ACCEPT-AND-DOCUMENT verdict changes to REBALANCE-REQUIRED.

---

*Synthesis authored as Wave B B2. Three lens inputs: architect-reviewer (577 lines), adversarial-reviewer (244 lines), prompt-engineer (227 lines). Total evidence base: 1,048 lines across 3 cold-context analyses. Synthesizer: research-synthesizer. Next: Wave C PRD authoring.*
