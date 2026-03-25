# The Governance Depth Boundary Problem

In multi-agent LLM systems, the operations that agents perform are not truly atomic. Research contains Analysis (evaluating sources). Analysis contains Research (finding more data). Building contains Planning and Analysis. If these inner compounds recurse freely, the system enters infinite decomposition. This document describes the depth boundary -- where governance enforcement stops -- and the unsolved problems that creates.

## The Recursion Problem

The 5 primitive operations (Research, Analysis, Planning, Building, QA) contain each other recursively. If inner compounds are allowed to recurse, depth is unbounded.

## Depth Boundary

| Depth | Executor | Governance | Can dispatch agents? |
|-------|----------|-----------|---------------------|
| D0: Main session | Classifier + process skill | Full (hooks, mandatory dispatch) | Yes |
| D1: Subagent | Specialist with system prompt | Soft (injected guidance, quality gate) | NO -- platform constraint |
| D2: Sub-subagent | General-purpose only | None (system instructions only) | NO |

**Rule:** Governance enforcement at D0. Behavioral guidance at D1. Trust at D2+.

## The D1 Problem

Subagents cannot spawn other named agents (a platform constraint in Claude Code and similar agent frameworks). When a D1 agent discovers it needs a compound operation -- for example, a research agent needs an adversarial reviewer to challenge its findings -- it either:

1. Does it inline (poorly -- same model, same context, same biases)
2. Silently drops it
3. Nobody knows it was needed

## Escalation Protocol (Proposed, Not Built)

1. **Injection at spawn:** Add to subagent guidance: "If your task requires another specialist agent you cannot dispatch, end output with an ESCALATION block listing what you need and why."
2. **Output detection:** A quality gate reads the subagent's final output for the ESCALATION marker. Logs it. Optionally blocks with a message to D0.
3. **D0 handles it:** The main session sees the escalation, dispatches the requested agent, feeds the result back.

This is soft governance (prompt instruction + output scanning). Hard enforcement at D1 is impossible given current platform constraints.

## Why This Matters

The depth boundary connects to several other open problems:
- **The Dark Zone** -- agent output integration is unobserved after D0 dispatches
- **Monitoring gaps** -- compound needs at D1 are silently lost without escalation
- **The recursive execution pattern** -- real work recurses through primitives, but governance cannot follow it past D0

Without escalation, the system operates under the assumption that every subagent task is single-primitive. When it isn't, quality degrades silently.
