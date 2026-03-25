# Skills and Agents Lack Essential Cross-References

Process skills and agent prompts written in isolation reference only a subset of available tools. This creates a system that silently drowns in its own infrastructure — tools exist but aren't surfaced where they're needed.

## The Problem

The user has to manually remind the agent to use tools that exist in the system, because the skills and agents that should REFERENCE those tools don't mention them.

## Evidence

A research process skill had 7 research agents available but only mentioned 5. The query-clarifier and research-coordinator agents were invisible. The research-orchestrator was buried as a conditional option for "4+ sub-questions" instead of being the default entry point. This directly caused the agent to dispatch 2 individual agents instead of using the orchestrator — the skill TRAINED the wrong behavior.

## The Systemic Issue

This isn't limited to one skill. Every process skill, every agent prompt, and every skill written in isolation knows about only a subset of the system. They were written without cross-referencing the full agent/skill registry.

## The Deeper Point

Hooks enforce PROCESS (do you follow the steps?). But if the process itself is incomplete (doesn't mention all available tools), enforcement just makes you follow a broken process faster. Fix the process content FIRST, then enforce it.

## How to Apply

1. Audit ALL process skills for missing agent/tool references
2. Audit ALL agent prompts for missing cross-references to related agents
3. The classifier-to-process-skill-to-agent chain must be complete — no agent should be invisible at any step
4. Consider maintaining a single source of truth for agent capabilities that process skills reference, rather than each skill maintaining its own partial list
