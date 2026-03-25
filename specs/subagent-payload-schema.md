# SubagentStart and SubagentStop Hook Payload Schemas

Verified payload schemas for the two subagent lifecycle hooks in Claude Code. These hooks enable behavioral injection into subagents at spawn time and quality gating at completion time. Understanding the exact payload fields is critical for building governance infrastructure.

---

## SubagentStart Payload (verified)

```json
{
  "session_id": "string",
  "transcript_path": "string",
  "cwd": "string",
  "agent_id": "string",
  "agent_type": "string -- equals frontmatter name field, NOT filename",
  "hook_event_name": "SubagentStart"
}
```

**NOT present:** `prompt` field. Cannot inspect delegation content at SubagentStart.

### Output Format (verified working)

```json
{
  "hookSpecificOutput": {
    "hookEventName": "SubagentStart",
    "additionalContext": "text injected into agent context"
  }
}
```

Flat format (`{"additionalContext": "..."}`) does NOT work -- must use `hookSpecificOutput` wrapper. The injected text appears as a `<system-reminder>` in the subagent's context.

---

## SubagentStop Payload (from docs)

```json
{
  "session_id": "string",
  "transcript_path": "string",
  "cwd": "string",
  "permission_mode": "string",
  "hook_event_name": "SubagentStop",
  "stop_hook_active": "boolean -- true if already continuing from a previous stop hook",
  "agent_id": "string",
  "agent_type": "string",
  "agent_transcript_path": "string -- path to subagent's own transcript",
  "last_assistant_message": "string -- FULL TEXT of agent's final response"
}
```

### Key Fields

- `last_assistant_message` gives the agent's complete output without transcript parsing
- `stop_hook_active` prevents infinite loops (check this before deciding to block)
- `agent_transcript_path` allows deep inspection of the agent's full conversation

### Output Format (block)

```json
{ "decision": "block", "reason": "explanation -- agent reads this and continues" }
```

Exit 0 with no JSON = allow. Exit 2 = blocking error.

### Matcher

Agent type regex (e.g., `"Explore|Plan"` or custom agent names).

---

## Governance Applications

| Hook | Governance Use | Pattern |
|------|---------------|---------|
| SubagentStart | Inject blind analysis rules into evaluator agents | additionalContext with behavioral guidance |
| SubagentStart | Log agent spawning for provenance tracking | Write agent_id + agent_type to log |
| SubagentStop | Quality gate: block agents with empty/error output | Check last_assistant_message length + content |
| SubagentStop | Enforce output structure requirements | Regex check on last_assistant_message |
| SubagentStop | Log agent completion for duration tracking | Match with SubagentStart by agent_id |

**Note:** Custom agents (defined in agent configuration files) cannot be dispatched via `subagent_type` parameter -- only built-in agent types work. Custom agents are selected by the model's routing based on their description field.
