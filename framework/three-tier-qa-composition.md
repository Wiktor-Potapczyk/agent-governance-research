# Three-Tier QA Composition

## The Model

Quality assurance in an AI agent system operates at three scales, each with its own scope, cadence, and actor. The tiers compose upward — each tier's output is a prerequisite for the next.

| Tier | Name | Cadence | Scope | Actor | Output |
|------|------|---------|-------|-------|--------|
| 1 | QA (falsification) | Every task | Single task claims | The executing agent | QA REPORT: PASS/FAIL per claim |
| 2 | Pentest (exhaustive) | Per increment | Whole increment | The orchestrating session | PENTEST REPORT: findings + untested surface |
| 3 | Eval (systematic) | Per milestone | Whole component | Human with eval tooling | Eval results: pass rates against trap cases |

## Composition Rules

1. **Tier N is prerequisite for Tier N+1.** A missing Tier 1 QA REPORT on any task in an increment means that increment's pentest is incomplete by definition.

2. **Each tier increases falsification surface.** Tier 1 tests individual claims. Tier 2 tests interactions between components built in the increment. Tier 3 tests against known failure patterns across the whole component.

3. **No tier is optional once triggered.** Tier 1 fires on every non-trivial task. Tier 2 fires when all tasks in an increment complete. Tier 3 fires at milestone boundaries.

4. **Tiers don't replace each other.** A passing Tier 2 pentest doesn't make Tier 1 QA unnecessary for the next task. A passing Tier 3 eval doesn't make Tier 2 unnecessary for the next increment.

## The Foundational Constraint

All three tiers are Popperian falsification. A PASS at any tier means "could not break it during the test window." It does not mean "correct." The value is cumulative confidence, not proof.

## What Each Tier Catches

- **Tier 1 catches:** incorrect claims, failed executions, missing outputs, wrong field values
- **Tier 2 catches:** integration failures, regression, boundary violations, adversarial bypasses
- **Tier 3 catches:** systematic weaknesses, known trap cases, prompt drift over time

## Layer 4: QA-on-QA

Who verifies the QA was thorough? Partially automated: Tier 2 requires an explicit "Untested Surface" list naming what was NOT tested. Tier 3 uses predefined trap cases. But whether the untested surface is acceptable and whether the trap cases are the right ones is irreducibly human judgment. This is the design ceiling.
