# Rubber-Stamp Enforcement Gaps

A governance hook that checks an agent's *output text* but never verifies the *real action behind it* creates a silent bypass path: the agent can satisfy the hook by producing the right-looking text without doing the work. This insight names the pattern and the design rule that closes it.

## The Insight

Hooks that check output text but not real dispatch create silent bypass paths. The vulnerable pattern is:

```
if has_output and not has_real_invocation: BLOCK
```

— which only fires when output is present. If the agent skips the step entirely (no output *and* no invocation), the condition is never met and the gap goes unnoticed.

Two instances were found in the 2026-04-18 infrastructure audit:

- **`check_pm_checkpoint_report`** — verified the PM checkpoint *report text* was present, but not that the PM agent was actually dispatched. Right-looking text alone passed the gate.
- **`work-verification-check` CHECK 1** — required BOTH conditions (output present AND no real invocation) simultaneously, which missed the case where the skill was skipped entirely.

The lesson: **invoke-side verification complements output-side verification.** Checking the artifact is not the same as checking that the action ran — and the AND/OR logic between those two checks determines which bypass cases are caught.

## Generalization

For any governance hook, ask: **"What would this miss if the agent faked the output?"**

Design invoke-side checks (did the agent actually dispatch / run the thing?) and output-side checks (does the artifact look right?) together, not independently. A hook that only inspects output is rubber-stamping the agent's claim that work happened; a hook that only inspects invocation can't judge whether the work was done well. Both surfaces need a check, and the boolean logic combining them must account for the skipped-entirely case, not just the faked-output case.

## Source

Documented in INDEX.md entry #21 (Rubber-Stamp Enforcement Gaps), from the 2026-04-18 infrastructure audit findings.
