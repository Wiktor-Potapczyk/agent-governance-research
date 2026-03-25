# The Untested Surface Method

Every test suite has a coverage boundary. A PASS result tells you what was tested and survived. It tells you nothing about what was NOT tested. When QA reports "13/13 PASS," the natural human response is confidence. But the 13 tests might cover only 40% of the actual attack surface.

## The Method

After every test cycle (QA, pentest, or eval), produce an explicit **Untested Surface** list: what was NOT tested and why.

### Format

```
## Untested Surface
1. [What was not tested] — [Why: not applicable / could not reproduce / requires different environment / time constraint]
2. [What was not tested] — [Why]
3. [What was not tested] — [Why]
```

### Rules

1. **The list is mandatory.** Every test report must have one. "Nothing untested" is almost always wrong — name at least the categories you considered but skipped.

2. **Organize by test category.** For each category in your test plan (boundary, adversarial, regression, failure modes, integration), state what you did NOT test within that category.

3. **Name the reason.** "Not tested" is insufficient. "Not tested because this requires a multi-session scenario that the current session cannot produce" is actionable — it tells the next tester what to try.

4. **The human reviews the surface, not the results.** PASS/FAIL is deterministic. Whether the untested surface is acceptable is a judgment call. The Untested Surface list is the artifact that enables that judgment.

## Why This Matters

This is the closest automatable proxy for QA-on-QA (testing the tests). The system cannot verify that the right questions were tested. But it CAN force the tester to name what was skipped. This shifts human judgment from "is this correct?" (impossible to verify externally) to "is what we didn't test acceptable?" (reviewable with domain knowledge).

## Connection to Popperian Falsification

QA proves absence of found bugs, not absence of bugs. The Untested Surface list makes the gap between "found" and "all" visible. Without it, a PASS creates false confidence. With it, a PASS comes with an honest boundary.
