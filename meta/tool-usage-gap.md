# The Tool Usage Gap -- Core Meta-Problem

LLM agents consistently fail to use available tools and specialist agents proactively, despite rules, hooks, and classifiers mandating delegation. This is the central meta-problem of any agent governance framework. More rules do not fix a structural problem.

---

## The Pattern

The AI has 28 agents, 30 skills, hooks, and a classifier -- but consistently does work inline that should be delegated. Rules exist and are skipped. The pattern repeats:

```
Rule exists -> Agent skips it -> User catches it -> Another rule is added -> repeat
```

## Root Cause Hypotheses

The task classifier maps types to approaches, but the agent still fails to follow through. Several structural factors may contribute:

- **Agent registry too large** -- 28 agents create a selection burden
- **Configuration file too long** -- critical routing rules buried in 188 lines
- **Context attention problem** -- instructions degrade as context grows
- **Gap between classification and action** -- knowing the type does not guarantee using the right tool

## Proposed Quick Fix

Strengthen the classifier's type-to-orchestrator mapping so classification DIRECTLY triggers the right entry point. When the classifier says "Research," it should immediately point to the research orchestrator -- not leave the agent to figure out the delegation chain.

## Deeper Question

Why does an LLM agent fail to use tools it knows about? This is not a knowledge problem (the tools are documented) or a capability problem (the tools work when invoked). It is a behavioral problem: the agent optimizes for quick inline responses over the overhead of delegation.

**Key insight:** The bottleneck has shifted from AI quality to AI self-direction. The tools exist. The rules exist. The compliance is inconsistent. More rules will not fix this -- only structural interventions (hooks that block, routing that forces, architecture that constrains) change the behavior.

## Evidence

- 46% of agents never invoked across two major sessions
- General-purpose agent handled 84% of framework session dispatches
- Specialist routing worked at 97% when applied to domain work -- the routing infrastructure is sound, but the decision to engage it is unreliable
- HackerNoon case study: skill activation went from 25% to 90% after adding a UserPromptSubmit hook that forced evaluation before every response

## Implications for Framework Design

1. **Classification must map directly to entry-point agents** -- remove the gap between knowing and doing
2. **Hooks that block** are more effective than rules that advise -- the 25% to 90% improvement was from a hook, not a rule
3. **The agent registry should be smaller** -- 15 agents with clear trigger conditions vs 28 agents with overlapping scope
4. **Mandatory delegation checks at response time** (Stop hooks) catch failures the UserPromptSubmit hook misses
