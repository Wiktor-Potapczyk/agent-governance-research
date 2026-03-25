---
date: 2026-03-22
tags: [#insight, #project/agent-suite]
---

# The Recursive Execution Pattern

## Insight

Every level of the system follows the same 6-step cognitive pattern:

```
RECEIVE TASK
  1. Classify  — what primitives does this contain?
  2. Decompose — which compounds need separate work?
  3. Delegate  — dispatch each compound to the right actor
  4. Work      — execute (may recurse this same pattern)
  5. QA        — verify output before returning
  6. Report    — return to caller
```

This is not process skills calling each other (that's banned — "compound, not recursive"). It's the same COGNITIVE PATTERN repeating at each depth with different implementations:

## How it manifests at each level

| Level | Actor | Classify | Decompose | Delegate | Work | QA | Report |
|---|---|---|---|---|---|---|---|
| **Main session** | Claude + classifier | task-classifier skill (formal) | APPROACH compound checklist | Process skill + agents via dispatch contract | Process skill orchestrates | SubagentStop + dispatch-compliance hooks | Response to user |
| **Process skill** | Claude following skill | Scope block (informal) | Agent routing table | Agent tool calls | Agents work in parallel/sequence | Mandatory review step (architect-review etc) | Output saved to work/ |
| **Agent** | Subagent | Implied by prompt (informal) | Natural reasoning | Tool calls (Read, Grep, WebFetch) | Direct execution | Self-check (limited — 78.5% persistence) | Return to main session |

## Key observations

1. **The pattern is the same, the formality decreases with depth.** Main session has hooks enforcing every step. Agents have SubagentStart governance nudging the pattern. Sub-agents just have their prompt.

2. **QA is the step that closes each recursion level.** Without QA, work returns unchecked. At the main session level, hooks enforce QA. At the agent level, SubagentStop catches structural problems. At the sub-agent level, nothing — this is the weakest link.

3. **The "compound, not recursive" constraint still holds.** Process skills don't call each other. But the cognitive pattern recurs because classify-decompose-delegate-work-QA-report is how good work happens at any scale. The constraint prevents infinite loops. The pattern ensures thoroughness.

4. **This is what the PM lifecycle playbook describes for projects.** Intake (classify) → Shape (decompose) → Build (work) → Review (QA) → Close (report). The lifecycle IS this pattern applied to projects. The execution chain IS this pattern applied to tasks. Same pattern, different timescale.

## Lineage — this evolved, it wasn't invented today

1. **Architecture doc (2026-03-21):** "The Repeating Unit" — defined as enforcement structure (skill + hook + matrix per node). "The network emerges when each node has this enforcement."
2. **Gemini peer review:** Critique #3 — inner compound processes aren't enforced. Hooks catch dispatches but not scoping quality.
3. **4-layer enforcement tracing:** Mapped entry/exit gates per layer. Identified missing exit gates at L2 (agents) and L1 (inner process steps).
4. **Jules comparison:** Confirmed "govern routing, not execution" — same pattern at every depth.
5. **Today (2026-03-22):** Named the execution flow explicitly (classify→decompose→delegate→work→QA→report). Connected to 5 primitives and PM lifecycle. The enforcement structure and the execution flow are two views of the same recursive pattern.

The "compound, not recursive" constraint still holds — process skills don't call each other. But the COGNITIVE PATTERN recurs because classify-decompose-delegate-work-QA-report is how good work happens at any scale.

## Connection to other insights

- **Compound Task Neural Network (#14):** The 5 primitives are WHAT gets classified. This pattern is HOW each primitive executes.
- **IMPLIES / QA symmetry:** IMPLIES is step 1 (classify — explore before acting). QA is step 5 (verify before returning). Entry and exit of each recursion.
- **Iterative deepening (#13):** The Ralph Loop's phased iteration (foundation→fields→context→review) IS this pattern applied to research — classify the unknowns, decompose into phases, work each phase, review, report.
