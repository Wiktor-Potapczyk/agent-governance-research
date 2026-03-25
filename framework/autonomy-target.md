# Autonomy Target: Exhaust Capabilities Before Asking for Help

Autonomous AI agent systems need a clear definition of what "autonomy" means in practice. This document defines the target as maximizing autonomous run length through structured QA, and describes the three-tier model that enables it.

## The Autonomy Target

Not "no user needed." The target is: **exhaust all autonomous capabilities before asking for help.**

## Three-Tier QA Model

| Tier | Cadence | What | Escalation |
|------|---------|------|------------|
| QA (falsification) | Every non-trivial task | Test own claims | Stuck → ask user |
| Pentest (exhaustive) | Per increment | Try to break the whole increment | Stuck → ask user |
| Eval (systematic) | Per milestone | Evaluation suite with trap cases | Results → iterate |

**Composition rule:** Tier N is prerequisite for Tier N+1. Tiers compose upward.

**QA is Popperian falsification.** A PASS means "could not break it," not "it is correct." The asymmetry is fundamental.

## Non-Trivial Tasks Get Lifecycle Treatment

Every non-trivial task gets full lifecycle treatment:

1. Classify → decompose into task list (defines the increment)
2. Execute each task: process skill → agent → QA (Tier 1)
3. All tasks completed (visible as checkmarks)
4. Pentest the increment (Tier 2) before reporting back
5. Report to user

The task list IS the increment. The AI platform's native task system is the institution. The visual checkmarks are the representation. No new infrastructure needed.

## Two-Layer Hook Purpose

**Compliance hooks minimize errors.** The classifier fires, the right skill loads, agents are dispatched.

**QA hooks maximize autonomous run length.** Verify before completing, pentest before shipping.

Layer 1 keeps the system on the rails. Layer 2 keeps it running longer.

## Enforcement Split

| Level | Enforcement | Mechanism |
|-------|-------------|-----------|
| Per-task QA | HARD (hooks) | Dispatch compliance + process step checks verify QA REPORT |
| Task list creation for multi-step work | SOFT (prompt) | Classifier instructions, cannot enforce via hooks |
| Increment boundary | SOFT (prompt + PM checkpoint) | PM checkpoint detects all-tasks-done |
| Pentest execution | HARD once invoked | Process step check verifies PENTEST REPORT |
| Pentest quality | NOT ENFORCEABLE | Untested Surface list → human judgment (Layer 4) |

**Why hooks cannot enforce increment boundaries:** Task creation and task list tools are session-internal. No hook payload exposes task state.
