# Monitoring Points Analysis

A first-principles analysis of every observable event in the governance framework architecture. This identifies what data the system generates, what is captured, and what is lost. The finding: 23 monitoring points exist, none are fully captured, and the most diagnostically valuable data is discarded.

---

## Key Numbers

- **23 monitoring points identified**
- **0 fully captured**
- **6 partially captured**
- **17 not captured at all**

## Priority Ranking

| Priority | Monitoring Points | Fix Effort | Diagnostic Value |
|----------|------------------|-----------|-----------------|
| P1 | Block event logging (MP-03, MP-07, MP-13) | 3-5 lines per hook | Direct proof enforcement catches violations |
| P2 | IMPLIES text in governance log (MP-02, MP-22) | ~5 lines | Context rot indicator, classification quality signal |
| P3 | Subagent pass/fail result (MP-11, MP-13) | 1 line change | Which agents trigger quality gate blocks |
| P4 | Mandatory vs opportunistic dispatch (MP-09) | ~5 lines | Are required agents being dispatched? |
| P5 | Session boundary events (MP-16, MP-18) | New hooks | Per-session analysis, session grouping |
| P6 | Skill routing deny log (MP-04) | 3 lines | Misclassification signal |
| P7 | Context size persistence (MP-01, MP-22) | Medium | Implication text vs context size correlation |
| P8 | Bash block events (MP-14) | 3 lines | Security signal |

## 8 Gaps Identified

1. **IMPLIES text not logged** -- the most diagnostically important field for context rot detection
2. **No block events logged anywhere** -- 3 hooks can block (classifier-field-check, dispatch-compliance, subagent-quality). None persist the block event. This is literally proof enforcement catches violations -- thrown away.
3. **Subagent pass/fail not recorded** -- quality check log has length but not whether output passed or was blocked
4. **Subagent governance log: no agent_id** -- cannot calculate agent duration without matching start/stop events
5. **No session boundary events** -- cannot group monitoring data by session
6. **Skill routing denials not logged** -- misclassification signal lost
7. **Dark Zone has no detection** -- the gap between subagent output and final response is unobserved
8. **Context window size computed but not persisted** -- cannot correlate context usage with quality

## Analysis

The governance framework has hooks that block violations, check compliance, and gate subagent quality. But the observability layer captures almost none of this. The current governance log covers 2 of 23 monitoring points partially.

The most actionable finding: **P1-P3 are 1-5 line changes each.** Block event logging, IMPLIES text capture, and subagent pass/fail recording require trivial code changes but provide high diagnostic value. These should be implemented before any new governance features.

P4-P8 require more design work but address real observability gaps. Session boundaries (P5) are prerequisites for any meaningful longitudinal analysis.
