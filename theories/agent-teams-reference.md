# Agent Teams: Multi-Session Coordination in Claude Code

Agent Teams are a mechanism for multiple Claude Code sessions to work as a coordinated team. One lead coordinates, teammates work independently with their own context windows. This is distinct from subagents (which run inside a parent session) and represents a fundamentally different execution model.

## Key Differences from Subagents

- **Subagents:** run inside parent session, report back only to parent, no inter-agent communication
- **Teams:** separate sessions, teammates message each other directly, shared task list

## Governance Hooks

- **TeammateIdle** -- fires when a teammate is about to go idle, can block (keep working)
- **TaskCompleted** -- fires when a task is marked done, can block (not actually done)
- **Plan approval gates** -- teammates must get lead approval before implementing

## Architectural Relevance

- A multi-role agent system maps to a team where each role is a teammate
- Inter-agent messaging = agents challenging each other (like ensemble but structural)
- Shared task list = coordinated pipeline execution
- Plan approval = the human-in-the-loop gate needed for high-stakes decisions

## Why Not Now

Experimental (requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` env var), heavyweight (separate Claude instances), higher token cost. Single-session subagent approaches work for current needs. But if Agent Teams become production-ready, the architecture changes from hub-and-spoke (main session dispatches individual subagents) to collaborative mesh (teammates communicate laterally).

## Enable

```json
{ "env": { "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1" } }
```
in settings.json.

**Source:** https://code.claude.com/docs/en/agent-teams
