# Governance Observability Map -- 23 Monitoring Points

A first-principles analysis of every observable event in an AI agent governance architecture. Maps what data the system generates, what is captured, and what is lost. The finding: 23 monitoring points exist, 0 are fully captured, and the most diagnostically valuable data is discarded.

---

## Key Findings

- **23 monitoring points, 0 fully captured.** Current governance logging covers 2 of 23 partially.
- **Block events not logged anywhere.** 3 hooks can block (classifier-field-check, dispatch-compliance, subagent-quality). None persist the block event. This is proof that enforcement catches violations -- thrown away.
- **IMPLIES text not logged.** The most diagnostically important field for context rot detection.
- **Subagent pass/fail not recorded.** Quality check log records output length but not whether the output passed or was blocked.

## Priority Fixes

| Priority | Fix | Effort | Value |
|----------|-----|--------|-------|
| P1 | Block event logging -- add disk write to deny/block paths of 3 hooks | 3-5 lines per hook | Direct proof enforcement catches violations |
| P2 | IMPLIES text -- add one regex to governance log | ~5 lines | Context rot indicator, classification quality signal |
| P3 | Subagent pass/fail -- add result field to quality check log line | 1 line | Which agents trigger quality gate blocks |
| P4 | Mandatory vs opportunistic dispatch -- compare dispatched vs MUST DISPATCH | ~5 lines | Are required agents being dispatched? |
| P5 | Session boundaries -- register SessionStart/SessionEnd hooks | New hooks | Per-session analysis, session grouping |

## 8 Gaps

1. IMPLIES text not logged (most diagnostically important)
2. No block events logged anywhere
3. Subagent pass/fail not recorded
4. Subagent governance log has no agent_id (cannot calculate duration)
5. No session boundary events
6. Skill routing denials not logged
7. Dark Zone has no detection
8. Context window size computed but not persisted

## Design Principle

P1-P3 are 1-5 line changes each. The most impactful observability improvements are often trivial to implement -- the gap is awareness, not engineering effort. Implement trivial monitoring fixes before building new governance features.
