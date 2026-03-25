# Agent Body Content Delivery: Workarounds for Unreliable System Prompts

There is an unverified report (GitHub issue #13627) that agent body content (below the frontmatter in agent definition files) may not consistently reach the subagent. The frontmatter (name, description, tools, model) IS used for routing and configuration, but the body content (system prompt, output format, behavioral rules) may be silently dropped in some spawn paths.

**Status:** Unverified — possibly hallucinated by research agent. Official documentation says body IS the system prompt. However, systematic testing showed 0% exact format match rate across 11 sessions (issue #19739), suggesting format instructions in agent bodies are at minimum unreliable.

## Workarounds (Ranked by Reliability)

1. **Encode requirements in the delegation prompt** — the prompt parameter in the Agent tool call is the most reliable channel for delivering instructions to a subagent.
2. **SubagentStart hook injects additionalContext** — fires synchronously, confirmed reliable. Use this for behavioral guidance that should apply to all agents.
3. **SubagentStop hook validates output** — check the last_assistant_message and block if required sections are missing. Use the stop_hook_active guard to prevent infinite loops.

## Related Issues

- Issue #20625: No structured output API for subagents (CLOSED / NOT_PLANNED)
- Issue #8395: No rule propagation from system instructions to subagents (CLOSED / NOT_PLANNED)
- Issue #26923: PreToolUse exit code 2 doesn't block Task tool (open)

## Practical Implication

All agent body edits (anti-sycophancy blocks, output metadata, output format) may be ineffective. The agent description in frontmatter IS delivered and affects behavior. Consider moving critical instructions into the description field, the delegation prompt, or SubagentStart hooks.
