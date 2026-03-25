# Agent Teams as Compound Execution Model

The governance depth boundary (see `governance-depth-boundary.md`) creates a hard problem: subagents cannot spawn specialists, so compound tasks at D1 are silently dropped or done poorly inline. The escalation protocol (soft governance) has ~48% chain probability by the framework's own research. Agent Teams -- multi-session coordination with shared task lists -- offer an alternative execution model that solves the depth problem by going wider instead of deeper.

## The D1 Depth Problem

Subagents can't spawn specialists (platform constraint). Compound tasks at D1 are silently dropped or done poorly inline. The escalation protocol (soft governance) has ~48% chain success probability at 78.5% compliance per step across three sequential steps.

## Two Execution Models

### Model A -- Subagent Round-Trips (Current)
```
D0 dispatches research-analyst
  -> discovers "need adversarial review"
  -> reports back to D0 (escalation)
  -> D0 dispatches adversarial-reviewer
  -> reports back to D0
  -> D0 synthesizes
```
Multiple round-trips. D0 is bottleneck. Each trip costs context.

### Model B -- Agent Teams (Proposed)
```
D0 reads task compounds, spawns team
  -> shared task list
  -> agents work in parallel, hand off laterally
  -> team lead assembles final output
  -> one return to D0
```
One dispatch, one return. Compounds handled at D1 laterally.

## Key Insight: Task Classification = Team Roster

A task classifier's compound field already declares all 5 primitives as yes/no with agent names:
```
Research: yes (technical-researcher)
Analysis: yes (adversarial-reviewer)
Planning: no
Building: no
QA: no
```
This IS the team composition. D0 spawns one teammate per yes-primitive.

## Self-Healing Team Pattern

1. D0 spawns agents matching the declared compounds
2. Each agent works its scope, discovers sub-compounds
3. Matching teammate exists -> lateral handoff via shared task list
4. No matching teammate -> escalate to D0 to spawn one
5. **Idle agent picks up another agent's pending compound need** -- even outside its original scope
6. Graceful degradation: work gets done (imperfectly) rather than silently dropped

This is load balancing + graceful degradation at D1. The team self-organizes around the work.

## Collaborative Decomposition (Refined Model)

No duplicate agents needed. Existing team members reshape each other's scope:

```
D0 spawns team from compounds: [research, analysis, build]
  -> research discovers: "findings need challenge"
  -> extends analysis scope via task list
  -> analysis challenges, discovers: "gap in data"
  -> extends research scope via task list
  -> ... chain of implications until all sub-tasks are truly primitive
  -> agents work from ground up on resolved primitives
  -> synthesizer assembles
```

Key properties:
- **Scope is emergent, not pre-declared.** The initial compound declaration is a starting roster; actual scope is discovered through work.
- **No duplication.** Agents reshape each other's scope, not spawn copies.
- **Decomposition happens at D1, not D0.** The team collectively discovers primitives through negotiation.
- **Recursion is lateral, not hierarchical.** The recursive execution pattern happens in the shared task list, not in agent spawning depth.
- **Converges to finite primitives.** Chain of implications terminates when all tasks are single-primitive operations -- then work builds from ground up.

## What This Solves

- **D1 can't spawn** -- teammates communicate laterally, no spawning needed
- **Escalation protocol** -- no soft escalation needed if team handles it
- **Dark Zone** -- team lead assembles response from team output, not main session inline
- **Depth boundary** -- not deeper, but WIDER. D1 becomes collaborative, not isolated

## Prerequisites

- Agent Teams must be production-ready (currently experimental in Claude Code)
- Shared task list mechanism must support structured handoffs
- Team agents need enough shared context to understand each other's needs

This is the long-term execution model. If Agent Teams work, the fundamental architecture changes from hub-and-spoke to collaborative mesh at D1.
