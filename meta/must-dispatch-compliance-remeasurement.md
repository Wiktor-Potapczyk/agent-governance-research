---
date: 2026-05-25
tags: [project/agent-governance-research, audit, analysis]
status: active
baseline: archive/2026-05-10-self-audit-dispatch.md (47% resolution rate)
window: 2026-05-11 → 2026-05-24 (14 days, 12 with data)
---

# Must-Dispatch Compliance Re-measurement — 2026-05-25

> Adapted from internal research workspace. Cross-references to vault-internal artifacts have been stripped or genericized.

Closes the must-dispatch-compliance measurement gap from a prior framework-usage audit — compliance had not been re-measured in 15 days.

## Methodology (mirrored from baseline)

All counts from `.claude/hooks/governance-log.jsonl` filtered by `ts[:10]` to the 14-day window, matching the baseline's approach (`2026-05-10-self-audit-dispatch.md` L20-36).

- **Total turns** — `event=token_breakdown` rows, 1/turn (baseline L23, L25).
- **Non-Quick turns** — `event=turn_summary` rows where `type != "Quick"` and non-null (baseline L26).
- **Non-Quick turns with zero dispatch** — non-Quick `turn_summary` with `agent_count==0 AND skill_count==0` (baseline L27, L66).
- **DC blocks** — `hook=dispatch-compliance, event=block` (baseline L29-30, 35).
- **DC resolution rate** — `pass / (block + pass)` events on `dispatch-compliance` hook (baseline L30: "8/17 (47%) followed by a pass event").
- **PM dispatches** — `event=agent_dispatched, agent_type=pm-orchestrator`. Baseline-style denominator: `outcome=allow` + `pm-report-enforcement` blocks (baseline L80: "28 PM dispatches total (15 allow + 13 blocked)").
- **PM format compliance** — allow / (allow + pm-report-enforcement blocks) (baseline L30).
- **PM no_classification** — `pm-orchestrator` dispatches with `outcome=no_classification` (baseline L36, L96).

## Window data summary

| Date | sessions | classifications | non_quick_ts | zero_disp_nq | dc_blocks | pm_disp | pm_format_blocks | agent_disp |
|------|----------|-----------------|--------------|--------------|-----------|---------|------------------|-----------|
| 2026-05-11 | 11 | 19 | 2 | 1 | 6 | 16 | 3 | 103 |
| 2026-05-12 | 7 | 18 | 2 | 1 | 3 | 11 | 6 | 29 |
| 2026-05-13 | 5 | 2 | 0 | 0 | 8 | 6 | 3 | 30 |
| 2026-05-14 | 6 | 38 | 3 | 0 | 5 | 9 | 1 | 31 |
| 2026-05-15 | 3 | 4 | 1 | 1 | 10 | 10 | 3 | 36 |
| 2026-05-16 | — | — | — | — | — | — | — | — |
| 2026-05-17 | — | — | — | — | — | — | — | — |
| 2026-05-18 | 4 | 0 | 0 | 0 | 2 | 8 | 2 | 28 |
| 2026-05-19 | 11 | 7 | 2 | 2 | 4 | 5 | 0 | 16 |
| 2026-05-20 | 6 | 7 | 2 | 2 | 1 | 12 | 0 | 42 |
| 2026-05-21 | 16 | 5 | 2 | 1 | 1 | 20 | 4 | 56 |
| 2026-05-22 | 3 | 12 | 4 | 0 | 4 | 13 | 3 | 39 |
| 2026-05-23 | 8 | 1 | 0 | 0 | 0 | 0 | 0 | 2 |
| 2026-05-24 | 5 | 9 | 1 | 0 | 4 | 6 | 1 | 16 |
| **Total** | **85** | **122** | **19** | **8** | **48** | **116** | **26** | **428** |

Source files: `.claude/hooks/aggregates/daily/2026-05-{11..15,18..24}.json` (cross-checked counts); raw event source `.claude/hooks/governance-log.jsonl`.

## Computed metrics (window 2026-05-11 → 2026-05-24)

| Metric | Baseline (2026-05-03→05-10) | This window (05-11→05-24) | Delta |
|--------|------------------------------|---------------------------|-------|
| DC block resolution rate (pass / (block+pass)) | 8/17 = 47% | 15/63 = **24%** | **−23 pp** (regressed) |
| PM format compliance (allow / (allow + format-block)) | 15/28 = 54% | 41/67 = **61%** | +7 pp |
| Non-Quick turns with zero dispatch | 4/7 (57%) | 8/19 (**42%**) | −15 pp (improved) |
| Any-dispatch fired on non-Quick | 3/7 (43%) | 11/19 (**58%**) | +15 pp (improved) |
| PM no_classification share | 35/51 = 69% | 75/116 = **65%** | −4 pp |
| All-agent no_classification share | 79/135 = 59% | 187/428 = **44%** | −15 pp (improved) |
| Total DC blocks | 17 | **48** | +31 absolute (volume up; window 14d vs 8d) |
| Turns per day (mean) | 168 / 8 = 21 | 555 / 12 = **46** | +25 turns/day (activity ~2×) |

## Findings

- **Headline number regressed: DC resolution rate dropped 47% → 24%.** Block volume nearly tripled (17 → 48) while pass-after-block counts stayed flat (8 → 15). The hook fires more, gets resolved proportionally less.
- **Non-Quick dispatch behavior improved.** Any-dispatch rate on non-Quick turns climbed from 43% to 58%; absolute zero-dispatch incidents are flat (4 → 8) but as a fraction of a larger non-Quick population (7 → 19), they trend better.
- **PM format compliance improved modestly (54% → 61%)** despite 4× PM dispatch volume (28 → 116). pm-report-enforcement blocks scaled sub-linearly (13 → 26), suggesting the format gate is internalized more often.
- **no_classification share dropped 59% → 44% across all agents**, but pm-orchestrator's share barely moved (69% → 65%) — orphaned PM checkpoints remain the dominant pattern, consistent with baseline Finding 3.
- **Anomalies:** 2026-05-23 is near-dark (1 classification, 2 dispatches, 0 PM); 2026-05-16 and 2026-05-17 have no governance-log events at all (likely no sessions held); 2026-05-15 spike of 10 DC blocks against only 1 non-Quick turn_summary suggests classifier-vs-execution drift on heavy single-day work.

## Caveats

- **Schema drift — `declared`/`missing` fields gone from dc-blocks.** Baseline Finding 1 counted "declared==missing" cases at 11/17 (65%) using a `declared` and `missing` field on dc-block events (baseline L62-68). Current dc-block schema has only `reason` and `task_type` (`reason` is `empty_must_dispatch_on_non_quick` for 7/48; the other 41 have `reason=null`). The "declared==missing" pattern cannot be reproduced; "DC resolution rate" is the closest comparable measure.
- **Baseline counted dc-blocks at 17 total; current schema shows 48 in 14 days vs 17 in 8 days.** Hook may have widened its trigger set between windows — at ~3.4/day vs baseline's ~2.1/day. Treat the absolute-volume comparison as confounded; the rate-comparison (pass/(pass+block)) is the cleaner signal.
- **Missing days:** 2026-05-16 and 2026-05-17 have no governance-log events. Window is 14 calendar days but 12 data-bearing days. Per-day metrics use 12 as denominator where rates would otherwise distort.
- **Baseline used "process-qa missing" and "architect-reviewer missing" sub-metrics (baseline L31-32, 35)** derived from `declared`/`missing` arrays on dc-blocks. With those fields gone, these sub-metrics are unmeasurable from the current schema and are omitted.
- **TaskCreate/turn metric (baseline Finding 5) omitted** — `token_breakdown` rows in the window do not consistently carry the `tool_calls` dict the baseline used; reproducing that count requires a different source.
- **Hook deployment timeline:** `dispatch-compliance` hook's `pass`-event emission appears tied to a `h11_sidecar_fallback_activated` path that wasn't in the baseline; 3 such events appear in the window. If this fallback changed pass-emission semantics mid-window, the 24% resolution rate is artificially low. Confirming this requires reading the hook source — not done here.
- **Aggregate JSONs (`.claude/hooks/aggregates/daily/*.json`) lack the dispatch-compliance, PM format, and turn_summary fields entirely.** They expose only `sessions`, `classifications`, `quick_count`, `non_quick_count`, `classifier_blocks`, `qa_fails`, `agent_warn_downgrades`, `agent_dispatches`. The re-measurement is necessarily governance-log-based; daily aggregates serve only as cross-checks on session and dispatch totals.

