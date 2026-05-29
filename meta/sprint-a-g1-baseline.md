---
date: 2026-05-26
updated: 2026-05-26
tags: [project/agent-governance-research, meta, audit, unclassified-pending]
status: active
audit_date: 2026-06-25
---

# Sprint A — Goal G1 Measurement Baseline

> Adapted from internal research workspace. Cross-references to vault-internal artifacts have been stripped or genericized.

Sprint A decomposition: [[sprint-a-task-decomposition]] §SA-7 · PRD: [[2026-05-25-framework-improvement-prd]] §G1

Baseline file for the 30-day post-ship measurement of PRD Goal G1: **"Reduce undetected fabrication incidents from 5/2-weeks (current) to ≤1/month within 30 days post-Item-1 ship."**

## SA-4 ship reference

- **Hook commit:** 0f7346e (work-verification-check.py CHECK 4 added) at ~23:41 local 2026-05-25.
- **Test suite + defect fix commit:** 7be126f at ~23:53 local 2026-05-25.
- **Hook activation:** already wired into existing Stop chain via settings.local.json (the CHECK 4 block is INSIDE work-verification-check.py which is already registered — no separate hook registration needed).

## Baseline metrics (snapshot at 2026-05-26 00:02)

Values populated by main-session `wc -l` + Python read of `.claude/hooks/governance-log.jsonl` at SA-7 ship time. See iteration log in this turn for raw output.

- **governance-log.jsonl total lines:** 7661.
- **fabrication_detected entries at baseline:** 8 total (1 from SA-6 sentinel verification fired at 00:02 confirming log path operational; 7 from CHECK-4 development testing across Wave-α and Wave-β smoke fires). Operational confirmation: sentinel path matched and was logged correctly.
- **Wiktor-discovered fabrication memos at baseline:** 5 memo files in `~/.claude/projects/<vault-id>/memory/` matching `*implementation_plan_fabricates*` (the 5 documented incidents that drove the PRD).
- **Production-window start ts:** 2026-05-26 00:02 local — count entries with timestamp ≥ this for the 30-day window. Entries before this are dev-time fires and excluded from G1 measurement.

## Measurement rule (per PRD G1)

At audit (**2026-06-25, +30 days**), compare:
- **Hook-detected:** count `event=fabrication_detected` entries in `.claude/hooks/governance-log.jsonl` with `ts >= 2026-05-26`.
- **Wiktor-discovered:** count NEW `*implementation_plan_fabricates*` memo files dated after 2026-05-26.

**G1 passes if:** Wiktor-discovered rate drops to ≤1/month (i.e., ≤1 new memo) **AND** hook-detected ≥ Wiktor-discovered over the 30-day window.

**REVISION (2026-05-26 per a follow-up adversarial review of the G1 gate):** the second clause "hook-detected ≥ Wiktor-discovered" is structurally guaranteed to pass due to bidirectional measurement bias (deflated denominator from verbal-catch exclusion + inflated numerator from false-positive counting). At audit, replace the second clause with a **detection-overlap audit**:

1. Inventory all fabrication incidents in window: Wiktor-discovered memos + recalled verbal catches at audit prompt.
2. Inventory all `fabrication_detected` hook entries in window.
3. Pair-match: which incidents have a corresponding hook entry within ±2 turns? That overlap = recall numerator.
4. Pair-classify hook-detected set: which entries match a real incident vs which are false positives? That = precision.

**Revised G1 pass condition:** Wiktor-discovered rate ≤1/month AND hook recall ≥50% AND hook precision ≥70% (numbers tunable; structure is what matters). This measures detection fidelity, not log volume.

The original ratio clause is preserved above as historical context; the precision/recall audit is the operative gate at 2026-06-25.

## Known measurement caveats

1. **Asymmetric instrumentation (adversarial CR8 from PRD §9 review):** Wiktor-discovered count only captures verbal-or-memo Wiktor catches; verbal catches that don't generate a memo are missed. Mitigation: at audit, ask Wiktor to recall any fabrications he caught but didn't memo.
2. **False-positive inflation:** if hook fires on legitimate-Write-failure reports (FP guard 4 not perfect), hook-detected count inflates artificially. Mitigation: at audit, inspect each fabrication_detected entry's `claimed_path` + `snippet` for false-positive pattern.
3. **Hook-detection ≠ block:** Q8 framing chose WARN-only, not BLOCK. So G1's success means "Wiktor sees the warning early" not "fabrications cannot reach Wiktor." This is the ergonomic-automation framing per PRD §9 Q8.

## Audit checklist (run at 2026-06-25)

- [ ] Count `event=fabrication_detected` entries with ts ≥ 2026-05-26.
- [ ] Count new `*implementation_plan_fabricates*` memos dated after 2026-05-26.
- [ ] Inspect each fabrication_detected entry for false-positive pattern (legitimate Write failure misclassified).
- [ ] Ask Wiktor about verbal-only catches not in memos.
- [ ] Write audit verdict to a follow-up audit file.
- [ ] Update PRD §2 G1 success criterion with audit outcome.
