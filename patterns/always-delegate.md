# Always Delegate to Specialist Agents

AI agents doing complex work inline produces lower quality output than delegating to specialist subagents. The overhead of delegation is repaid by specialized focus, parallel execution, and cross-checking that inline work cannot provide.

## The Principle

Do not write specs, prompts, plans, or reviews inline. Always delegate to the matching specialist agent first. Agents are unbiased specialists — they don't share your context biases.

## Why

If you have built specialist agents for specific tasks, doing work inline wastes that infrastructure and produces lower quality output (no specialized focus, no parallel execution, no cross-checking). Inline work is shortsighted — the true power lives in using agents intelligently.

## Delegation Map

- Writing a prompt: prompt-engineer agent
- Planning architecture: planner agent
- Reviewing code/specs: reviewer agent
- Writing content/copy: content-marketer agent
- Research: research-orchestrator (NOT individual research agents — the orchestrator coordinates the team)
- Building code: builder agent
- LLM system design: llm-architect agent
- Only solve inline when NO agent matches the task type (simple edits, quick answers, file ops)
- When multiple agents apply, run them in parallel

## How to Apply

- **Before launching ANY research or complex work, inventory available agents/tools first.** Think about which agents fit, how to decompose the work, and what runs in parallel — BEFORE writing a single prompt.
- Task classification is mandatory before any substantive task — including presenting decision briefs, options, or tradeoffs. Skipping it to "just present options" is still inline analysis.
- When a task is complex or requires deep thinking, use deep research loops for independent work until every source of information is exhausted.
- Always loop: question, investigate, verify, review, improve. Never single-pass.
