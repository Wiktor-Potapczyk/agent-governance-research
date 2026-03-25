# Governance Depth Boundary and Escalation Protocol

AI agent systems that use subagents face a recursion problem: the primitive operations (Research, Analysis, Planning, Building, QA) are not truly atomic — each contains the others. This document examines the governance depth boundary and proposes an escalation protocol for subagents that discover compound needs.

## The Recursion Problem

The five primitive operations are NOT truly atomic. Each contains the others:

- Research contains Analysis (evaluating sources)
- Analysis contains Research (finding more data)
- Building contains Planning (implementation design) + Analysis (review)

If inner compounds recurse, it becomes infinite.

## Depth Boundary

| Depth | Executor | Governance | Can dispatch agents? |
|-------|----------|-----------|---------------------|
| D0: Main session | Classifier + process skill | Full (hooks, mandatory dispatch) | Yes |
| D1: Subagent | Specialist with system prompt | Soft (startup injection, quality gate) | NO — platform constraint |
| D2: Sub-subagent | Explore/general-purpose only | None (system instructions only) | NO |

**Rule:** Governance enforcement at D0. Behavioral guidance at D1. Trust at D2+.

## The D1 Problem

Subagents CANNOT spawn other named agents (platform constraint). When a D1 agent discovers it needs a compound operation (e.g., a research analyst needs an adversarial reviewer to challenge findings), it either:

1. Does it inline (poorly)
2. Silently drops it
3. Nobody knows it was needed

## Proposed Escalation Protocol

1. **Startup injection:** Add to governance guidance: "If your task requires another specialist agent you cannot dispatch, end output with ESCALATION block listing what you need and why."
2. **Stop detection:** A hook reads the agent's last message for `ESCALATION:` marker. Logs it. Optionally blocks with message to D0.
3. **D0 handles it:** Main session sees escalation, dispatches the requested agent, feeds result back.

This is soft governance (prompt + output scanning). Hard enforcement at D1 is impossible given platform constraints.

## Connection to the Broader Architecture

Without escalation, compound needs at D1 are silently lost. This connects to the integration gap (the "Dark Zone"), the monitoring points analysis, and the recursive execution pattern — the same cognitive pattern (Classify → Decompose → Delegate → Work → QA → Report) recurs at every depth level, but governance enforcement stops at D0.
