# PM Phase Transition Gates

## The Problem

In an AI agent PM lifecycle, phases represent fundamentally different modes of work (shaping vs building vs reviewing). Transitioning without a gate check risks carrying unresolved problems forward -- rabbit holes unmitigated, scope unchecked, quality unverified.

## The Gate Protocol

At every phase transition, answer one mandatory question:

> **Q6: Given what we now know, is this still worth the remaining appetite?**

- **YES** -- proceed to next phase
- **NO** -- kill the project or reshape (loop back to Phase 1)

This is a viability check, not a quality check. It asks whether the project should continue, not whether the work so far is good.

## Per-Transition Gates

| Transition | From -> To | What Q6 checks |
|-----------|-----------|----------------|
| 0 -> 1 | Intake -> Shape | Is the problem clear enough to invest shaping effort? |
| 1 -> 2 | Shape -> Build | Are rabbit holes mitigated? Is the solution sketch viable? |
| 2 -> 3 | Build -> Review | Did we deliver core value? Is remaining work worth remaining appetite? |
| 3 -> 4 | Review -> Close | Is the output good enough to ship (or should we polish/extend)? |

## Gate Failure Rules

- **Q6 fails at any gate** -> STOP. Escalate to human. Options: kill, reshape, or extend appetite.
- **The human must confirm kills.** The system recommends; the human decides.
- **Past effort is not a reason to continue.** The kill question is always forward-looking.

## Reviewer Roles at Gates

| Gate | Reviewer | What they check |
|------|----------|-----------------|
| 0 -> 1 | Human (implicit) | Pitch makes sense |
| 1 -> 2 | adversarial-reviewer | Challenge solution sketch before committing |
| 2 -> 3 | architect-review + pentest | Quality + can it be broken? |
| 3 -> 4 | Human | Ship/polish/extend/kill decision |

## Anti-Pattern: Gateless Transitions

Without gates, projects drift. The model starts building before shaping is complete ("we know enough to start"). Or it starts a new increment before reviewing the last one ("the next task is obvious"). Gates force the pause that prevents drift.
