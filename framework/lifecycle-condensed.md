# PM Lifecycle Playbook: Design Decisions

AI agent systems that manage multi-step projects need a lifecycle model — a way to track phases, enforce checkpoints, and know when to kill a project. This document summarizes the design decisions behind the lifecycle playbook used in this framework.

## Lifecycle Model

**Shape Up hybrid** — fixed-time variable-scope cycles + Kanban flow (WIP limits, pull) + PRINCE2 viability gates + Lean PDCA.

## Five Phases

| Phase | Name | Purpose | Kill Condition |
|-------|------|---------|----------------|
| 0 | Intake | Decide if project deserves shaping | Vague problem, can't articulate value |
| 1 | Shape | De-risk before committing | Unsolvable within appetite OR value < cost |
| 2 | Build | Deliver working increments | Appetite exhausted without core value |
| 3 | Review | Evaluate output, capture lessons | N/A (always completes) |
| 4 | Close | Archive, free capacity | N/A (always completes) |

## Eight Compressed Fields

11 traditional PM fields compress to 8 for a solo operator + AI agents. Three are collapsed:

- **Scheduling** → absorbed into appetite (scope) and dependency notes (breakdown)
- **Resource/Role Assignment** → absorbed into agent registry and classifier routing
- **Communication Rhythm** → absorbed into weekly self-review and async artifacts

## Three Artifacts

| Artifact | Type | Purpose |
|----------|------|---------|
| PROJECT.md | Static scope | Problem, appetite, no-gos, success criteria |
| STATE.md | Dynamic status | Current phase, hill chart, blockers, decisions |
| task_plan.md | Work items | Ordered list with MoSCoW tags and acceptance criteria |

## Core Checkpoint Protocol

Five questions answered at every increment and phase transition:

1. **What exists?** (single authoritative task list)
2. **What matters most?** (top 3 explicit, WIP limit enforced)
3. **What's happening?** (current phase, active tasks, blockers)
4. **What changed?** (key decisions logged with rationale)
5. **What's done?** (Definition of Done passed, items archived)

At phase transitions, add Q6: "Given what we now know, is this still worth the remaining appetite?"

## Circuit Breaker

Qualitative — "has this stalled?" not a numeric counter. Appetite is S/M/L sizing, not calendar days. When appetite is exhausted without core value, the project stops. Continuing requires an active, justified choice. The default is death.

## Open Design Question

How does the PM orchestrator relate to the existing classifier → process skill → agent chain? Options considered include the orchestrator replacing process skills, sitting above the classifier as a meta-layer, or being invoked explicitly only. Current approach: independent systems, with the user invoking PM at appropriate moments. Insufficient production data to decide on tighter coupling.
