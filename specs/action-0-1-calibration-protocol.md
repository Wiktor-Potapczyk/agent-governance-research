---
date: 2026-05-26
updated: 2026-05-26
tags: [project/agent-governance-research, planning, spec, meta, audit]
status: active
cadence: weekly_or_twice_weekly
first_scheduled: 2026-06-01
---

> Adapted from internal research workspace. Cross-references to vault-internal artifacts have been stripped or genericized.

# Action 0.1 — External Calibration Protocol

Hub: agent-governance research repo · Driver: [[framework-evaluation]] §Recommended actions · Doctrine: closed-loop measurement problem per meta-evaluation

The ONE structural change the meta-evaluation identified as unsolvable from inside the framework. Every internal compliance metric (DC, PM-format, QA PASS rates, no-classification share) measures conformance to the framework's own rules — correlation with output quality has never been measured. Action 0.1 is the only thing that exits the closed loop.

**Owner cadence commitment (2026-05-26 00:30):** "weekly or twice a week" — supersedes the meta-evaluation's monthly recommendation. Higher cadence = faster detection of closed-loop drift, at cost of ~4-8x owner time investment.

## Cadence

- **Primary cadence:** weekly, every Monday morning. 20-30 minutes.
- **Optional secondary cadence:** mid-week supplemental on Thursday, 10-15 minutes (Wiktor discretion based on prior-week throughput).
- **First scheduled run:** Monday 2026-06-01 (next Monday from doctrine commitment).
- **Skip rule:** if the previous calibration was <72h ago AND throughput in the interim was <3 QA-PASS artifacts, skip the supplemental.

## Sampling procedure

Per session:
1. Run `python .claude/scripts/sample-qa-artifacts.py` (to be built — see §Tooling) — emits 5-10 randomly-sampled QA-PASS artifacts from the past N days (default N=7 for weekly cadence, N=3 for supplemental).
2. The script outputs: per-artifact path + claimed deliverable + QA REPORT block + linked PR/commit if any.
3. Wiktor opens each artifact in the vault, reads it, judges it against actual-correctness rubric (see §Rubric).
4. Wiktor records each artifact's calibration verdict in a single weekly file: `Projects/Agent-Governance-Research/calibration/YYYY-WW-calibration.md` (one file per ISO week).

## Rubric (what Wiktor judges)

For each sampled artifact, three axes:

| Axis | Question | Verdict scale |
|---|---|---|
| **Substantive correctness** | Does the artifact's claims hold under independent inspection? (Wiktor reads the source, the code, the live system — not the artifact's self-report.) | PASS / PARTIAL / FAIL |
| **Internal-vs-external gap** | Did the framework's QA report match Wiktor's verdict? (Specifically: QA-PASS-but-actually-wrong = the critical bias) | MATCH / DIVERGE |
| **Process-cost ratio** | Was the framework ceremony (skill dispatch + agent fan-out + QA + PM) proportionate to the artifact's value? | OK / OVERWEIGHT / UNDERWEIGHT |

Verdict format per artifact: `path | substantive | gap | process-cost | one-line note`.

## Aggregate measurement

End of each calibration session, append to `Projects/Agent-Governance-Research/calibration/aggregate.md`:

```
2026-06-01 (week 2026-W23): n=8 sampled
  substantive: PASS 6 / PARTIAL 2 / FAIL 0
  gap: MATCH 7 / DIVERGE 1  → 1 false-PASS (path-redacted-1)
  cost: OK 6 / OVERWEIGHT 1 / UNDERWEIGHT 1
  G0 alignment: 87.5% (7/8 MATCH)
```

The **G0 alignment number** (% of sampled artifacts where internal QA matched Wiktor's verdict) is the headline external metric. G0 = "framework's internal compliance correlates with actual quality."

Target: G0 alignment ≥ 80% sustained over rolling 4-week window. Below 80% → framework discipline is theatrical and a deeper structural change is needed.

## Tooling (separate ticket — to be built)

- **`sample-qa-artifacts.py`** — script that walks `Projects/*/work/` + `Projects/*/STATE.md`, identifies QA-PASS artifacts from past N days, returns random sample. Should also pull the QA REPORT block + PM CHECKPOINT REPORT block alongside each artifact for Wiktor's comparison. ~80 lines Python. Build as new ticket `CAL-1` in task_plan.
- **`Projects/Agent-Governance-Research/calibration/` directory** — created at first calibration run. Holds per-week files + aggregate.md.

## Failure mode handling

- **Wiktor skips a week:** mark the gap in aggregate.md (`2026-W24: SKIPPED`). Two consecutive skips → calibration cadence is failing, escalate to "every other week minimum" rather than abandoning entirely.
- **Sample contains 0 QA-PASS artifacts:** throughput is too low to calibrate; skip the session and note. If happens 2 weeks in a row, the project is in a building lull and calibration on lull weeks adds no signal.
- **G0 falls below 75%:** trigger a focused diagnosis loop — find the divergence patterns (which agent types, which task types) and surface to next planning cycle.

## Open questions Wiktor decides at first calibration run

1. Should `sample-qa-artifacts.py` weight sampling toward high-stakes artifacts (PRDs, sprint plans, architecture docs) over routine ones (n8n workflow tweaks, single-file edits)? Proposed default: uniform random; switch to weighted if first 4 sessions show all FAILs concentrated in one category.
2. Should DIVERGE outcomes auto-create a feedback memo, or stay confined to the calibration file? Proposed default: any FAIL or DIVERGE on a HIGH-stakes artifact (PRD/spec/architecture) auto-creates a feedback memo within the same calibration session.

## Sequencing

1. Build `sample-qa-artifacts.py` (CAL-1, ~30 min, autonomous).
2. Create `calibration/` directory + first-week template stub (5 min).
3. Wiktor runs first calibration Monday 2026-06-01.
4. After 4 calibration runs (~1 month), evaluate the cadence: is weekly the right rate, or should it back off to twice-monthly?

## Related

- [[framework-evaluation]] §Recommended actions — origin
- [[sprint-a-g1-baseline]] — internal 30-day fabrication detection measurement (closed-loop). Action 0.1 is the external complement.
- Adversarial finding that G1's internal gate is structurally guaranteed to pass — Action 0.1 is the external check that catches what G1's internal gate misses.
