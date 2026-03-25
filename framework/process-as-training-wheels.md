# Process Skills Are Training Wheels

AI agent governance frameworks face a tension: structured processes improve consistency but can become ceremony that adds overhead without value. This document presents evidence that process skills are a means to a behavior, not an end — and that governance should focus on routing decisions, not execution mechanics.

## The Discovery

During enforcement testing, a fresh-session test agent (T5, given the prompt "think more carefully about hook architecture") was supposed to test depth-signal classification. Instead, the agent:

- Skipped classification entirely (no task classifier invoked)
- Skipped the process-analysis skill
- BUT ran a 4-lens ensemble analysis (control theory, organizational governance, failure mode, information theory)
- Made 37 tool calls, read multiple files, cited research
- Produced the most insightful finding of the entire test session (the integration gap)

## The Insight

Process skills are a means, not an end. The actual goals are:

1. Right agents/tools get used
2. Multiple perspectives gathered
3. Evidence cited
4. Output structured

When the prompt is good and context is rich, the model does this naturally. Process skills codify the behavior for when the model WOULD NOT do it. Hooks enforce the process for when the model would SKIP it.

## Connection to Two-Layer Governance

- **Layer 1 (forced pause):** Ensures work happens — process skills provide this
- **Layer 2 (quality):** Emerges from good context, not process compliance

## Implication for Governance Design

Do not force process on subagents. Force it on the MAIN SESSION where routing decisions are made. Subagents do the work — let them work. The main session decides WHAT work to do — that is where enforcement matters.

## Design Principle

Subagent governance should focus on WHAT they receive (good prompts, right context) not HOW they work internally. Startup hooks should inject context, not process rules.

As the user observed: "It skipped the process but used the tools — exactly what we want to achieve with the process."
