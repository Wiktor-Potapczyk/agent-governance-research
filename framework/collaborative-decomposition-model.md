# Collaborative Decomposition Execution Model

The current subagent model in AI coding agents has a hard depth limit: subagents at depth 1 (D1) cannot spawn specialist agents. This document specifies a collaborative team execution model that replaces hub-and-spoke dispatch with lateral communication, and describes a two-phase approach (decompose then execute) that guarantees convergence.

## Problem Statement

When a D1 agent discovers its task requires a compound operation (e.g., research needs adversarial review), it either does it poorly inline or silently drops it. Neither produces quality output. The escalation protocol (soft governance) has ~48% chain probability — unreliable.

## Proposed Model

Replace hub-and-spoke subagent dispatch with collaborative team execution. The main session (D0) spawns a team of specialists. Team members communicate laterally via a shared task list. They collectively decompose their work until all tasks are single-primitive operations, then build from the ground up.

## Execution Flow

```
1. D0 classifier produces APPROACH with compound matrix:
     Research: yes (technical-researcher)
     Analysis: yes (adversarial-reviewer)
     Building: yes (builder agent)
     Planning: no
     QA: no

2. D0 spawns Agent Team with one teammate per yes-primitive
     + synthesizer/team-lead role

3. Team begins execution. Each agent works its primary scope.

4. Research agent discovers: "findings need challenge before proceeding"
     → adds to shared task list: "analysis needed: challenge research findings"
     → adversarial reviewer picks up the task

5. Adversarial reviewer discovers: "challenge reveals data gap"
     → adds to shared task list: "research needed: investigate gap Y"
     → technical researcher picks up the task

6. Chain continues until all tasks resolve to single-primitive operations

7. Agents work resolved primitives from the ground up

8. Team lead assembles final output from all team contributions

9. Single return to D0
```

## Core Assumptions

| # | Assumption | Status |
|---|-----------|--------|
| A1 | Teammates can ADD tasks to the shared list | Partially confirmed — lead creates; workaround: teammate messages lead |
| A2 | Messages between teammates include structured content | Confirmed — peer-to-peer messaging with content field |
| A3 | Teammates can read each other's outputs | Confirmed — direct messaging |
| A4 | Task list is ordered or prioritizable | Confirmed — tasks support dependencies |
| A5 | Task completion is observable | Confirmed — TaskCompleted hook fires |
| A6 | Decomposition terminates (finite) | Unaddressed — no built-in cycle detection |
| A7 | D0 can extend team dynamically | Confirmed — lead can spawn/shutdown mid-execution |
| A8 | Team-level synthesis avoids the Dark Zone | Partial — no built-in mechanism; lead manually synthesizes |

## Two-Phase Execution

Separate decomposition from execution to guarantee convergence.

### Phase 1: DECOMPOSE (collaborative, bounded)

```
Team examines task from each primitive lens:
  Research specialist: "what do we need to find out?"
  Analysis specialist: "what needs evaluation?"
  Planning specialist: "what needs sequencing?"
  Building specialist: "what needs producing?"
  QA specialist: "what needs verifying?"

  → Specialists challenge each other's decompositions laterally
  → Output: complete shared task list of primitive operations + dependencies
  → Plan approval gate: lead (or user) approves before Phase 2
```

### Phase 2: EXECUTE (bottom-up, no new tasks)

```
Work the task list from leaves (no dependencies) to root:
  → Each primitive task assigned to its specialist
  → No new compound discoveries expected (decomposition was exhaustive)
  → If a new compound emerges: brief Phase 1 re-entry for that sub-task only
  → Synthesizer assembles as primitives complete
```

### Why This Works

- **Convergence guaranteed:** Phase 1 only FINDS primitives, does not do work. Bounded by task scope.
- **Plan approval built-in:** Phase 1 output = plan. The platform has plan approval gates.
- **No interleaving:** Separating discovery from execution prevents infinite discover → work → discover cycles.
- **Re-entry is bounded:** If Phase 2 discovers a missed compound, Phase 1 re-entry is scoped to that one sub-task.

## What This Solves

| Problem | How |
|---------|-----|
| Dark Zone | Team synthesizer has only team outputs, no conversational bloat |
| D1 can't spawn | Lateral communication replaces hierarchical spawning |
| Escalation protocol unreliable | No soft escalation needed — team handles compounds laterally |
| Depth boundary | D1 becomes collaborative mesh, not isolated silos |

## What This Does NOT Solve

- **Context rot** — each teammate has its own context window, but long-running teams may still degrade
- **Classification quality** — D0 classifier still determines initial APPROACH; wrong APPROACH = wrong team
- **Token cost** — separate instances per teammate is more expensive than subagents
- **Governance at D1** — hooks exist but enforcement within team is untested

## Platform Limitations

- No built-in synthesis — lead is manual assembler
- No cycle detection — convergence mechanism must be built
- Teammates cannot spawn sub-teams — only lead manages team
- Leadership is fixed — cannot transfer lead role
- Experimental — requires environment flag
- Cost — each teammate is a separate instance

## Open Questions

1. Can teammates call task creation tools? (Undocumented pattern)
2. What is the token/cost model for multi-agent teams?
3. Can existing governance hooks integrate with team execution?
4. Is the platform stable enough for production use?
5. What happens when teammates disagree?
6. How does the team lead decide when decomposition is "done"?
