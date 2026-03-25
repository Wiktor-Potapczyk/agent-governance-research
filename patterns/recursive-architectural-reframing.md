# Recursive Architectural Reframing

Before decomposing any task into sub-steps, challenge its fundamental framing and boundaries. Apply four checks recursively until you hit an atomic, undeniable constraint. This counters the anti-pattern of accepting task boundaries as given and producing engineering checklists without questioning whether the boundaries, dependencies, or framing are correct.

## Phase 1: Recursive Architectural Reframing (Do NOT decompose yet)

Before breaking down any task, challenge its fundamental framing and boundaries. Apply four checks:

1. **Trap Check (False Dichotomies):** Are we treating concepts as mutually exclusive (A vs B) when they might be layers, sequences, or subsets of each other?

2. **Boundary & Dependency Check:** Are the task boundaries drawn correctly? Do "sequential" tasks actually share a root dependency that requires them to be solved together?

3. **Reality Grounding:** Trace the task back to its ultimate environment (both the end-user workflow AND the system's backend/deployment reality). Does the proposed solution contradict an underlying constraint of that reality?

4. **The Collapse Point:** What is the single, deeper question that, if answered, renders multiple sub-tasks irrelevant or already solved?

**The Recursion Rule:**
Do not stop at the first reframe. Take your "Collapse Point" answer and run it through the four checks again. Continue this chain of reframing until you hit an atomic, undeniable technical constraint.

Example chain: "Do we need human-in-the-loop?" then "Where is HITL practically feasible?" then "Only at the final output stage, because it's the only stage that produces readable text" (atomic constraint — stopped here).

## Phase 2: Execution

Only after explicitly stating the final, root-level "Real Question" derived from recursive reframing, decompose the work. Map sub-steps and risks directly to the discovered root constraint, updating the original task definition if the reframing changed it.

## When to Apply

- Task decomposition (before breaking into sub-steps)
- Architecture decisions (before evaluating options)
- Planning sessions (before sequencing work)
- Any time the task plan feels like a mechanical checklist rather than a coherent design
