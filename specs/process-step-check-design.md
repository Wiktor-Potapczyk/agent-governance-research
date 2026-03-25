# Process Step Check -- L1 Exit Gate Design

A Stop hook that verifies process skill steps were followed correctly. Implements two-tier enforcement: hard blocks on clear violations, soft logging on judgment-dependent checks. Built and tested with 8/8 functional tests and 11/11 integration QA passing.

---

## Two-Tier Enforcement

### HARD blocks (clear violations)

- Missing SCOPE block (RESEARCH SCOPE, BUILD SCOPE, etc.) for the invoked process skill
- Missing QA REPORT with PASS/FAIL for QA process

### SOFT logging (judgment-dependent, data collection)

- Synthesis not dispatched when 2+ agents contributed
- Architect-review not dispatched for build/planning processes
- Zero agent dispatches for process skills that should delegate

All checks logged to governance log (`event: "block"/"warn"/"pass"`).

## Per-Process Verification Matrix

| Process | Hard checks | Soft checks |
|---------|------------|-------------|
| process-research | RESEARCH SCOPE present | synthesis if 2+ agents, agent dispatch count |
| process-build | BUILD SCOPE present | architect-review dispatch, agent dispatch count |
| process-analysis | ANALYSIS SCOPE present | synthesis if 2+ agents, agent dispatch count |
| process-planning | PLANNING SCOPE present | architect-review dispatch, agent dispatch count |
| process-qa | QA SCOPE + QA REPORT with PASS/FAIL | (none) |

## Design Rationale

Hard enforcement only on clear-cut violations (scope blocks are always required, QA report format is always required). Soft monitoring on judgment-dependent checks -- collect data before tightening. This avoids the "mandatory enforcement produces performative compliance" trap documented in the framework's research.

The principle: **collect data before tightening.** Start with hard enforcement only on unambiguous violations. Log everything else. After enough data, identify which soft violations actually correlate with quality problems -- then promote those to hard enforcement with evidence.
