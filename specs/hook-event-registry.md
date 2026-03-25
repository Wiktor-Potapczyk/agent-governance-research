# Hook Event Registry -- Governance Infrastructure Research

Deep research findings on using Claude Code hooks as governance infrastructure for AI agent systems. Covers the complete event map, production governance implementations, academic framework mappings, cross-tool comparisons, practical limits, and security-governance overlap. Based on 20+ sources including official docs, 5 academic papers, 8 production articles, and 2 open-source repos.

---

## Complete Hook Event Map

### Four Hook Types

| Type | Mechanism | Timeout | Blocking | Use Case |
|------|-----------|---------|----------|----------|
| **command** | Shell subprocess, JSON via stdin | 600s default | Yes (exit 2) | Safety gates, formatters, loggers |
| **http** | HTTP POST to endpoint | 30s default | No (fails silently on timeout) | Audit logging, external services |
| **prompt** | Single-turn LLM eval (Haiku default) | 30s default | Yes (ok:false) | Semantic validation requiring judgment |
| **agent** | Multi-turn subagent, Read/Grep/Glob tools | 60s default | Yes (ok:false) | Deep verification requiring file inspection |

**Key:** prompt/agent hooks use `{"ok": true/false, "reason": "..."}` format, NOT exit codes.

### All 22 Events

| # | Event | Fires When | Blocking? | Context Inject? | Key Governance Use |
|---|-------|-----------|-----------|-----------------|-------------------|
| 1 | **SessionStart** | Session begins/resumes | No | Yes | Behavioral initialization, state injection |
| 2 | **UserPromptSubmit** | User submits prompt | Yes (exit 2 = reject) | Yes | Process compliance enforcement |
| 3 | **InstructionsLoaded** | Config/rules file loads | No | No | Audit instruction loading |
| 4 | **PreToolUse** | Before tool executes | **YES -- only blocking tool hook** | Yes | Block/modify/allow any tool call |
| 5 | **PermissionRequest** | Permission dialog about to show | Yes | No | Auto-approve/deny permission dialogs |
| 6 | **PostToolUse** | After tool succeeds | No (decision:block = feedback) | Yes | Quality feedback, audit logging |
| 7 | **PostToolUseFailure** | After tool fails | No | Yes | Error recovery, alerting |
| 8 | **Notification** | Agent sends notification | No | Yes | Desktop alerts, routing |
| 9 | **SubagentStart** | Subagent spawned | No | Yes | Behavioral injection into subagents |
| 10 | **SubagentStop** | Subagent finishes | **Yes (exit 2 = continue)** | No | Quality gates on subagent outputs |
| 11 | **Stop** | Main agent finishes | Yes (exit 2 = continue) | No | Completion verification, loop control |
| 12 | **StopFailure** | API error ends turn | No | No | Alerting on API failures |
| 13 | **TeammateIdle** | Agent team member goes idle | Yes | No | Multi-agent team coordination |
| 14 | **TaskCompleted** | Task marked complete | Yes (exit 2 = block) | No | Task completion validation |
| 15 | **ConfigChange** | Settings file changes | Yes (policy cannot be blocked) | No | Prevent unauthorized config changes |
| 16 | **WorktreeCreate** | Worktree being created | Yes (non-zero = fail) | No | Custom isolation initialization |
| 17 | **WorktreeRemove** | Worktree being removed | No | No | Cleanup on worktree removal |
| 18 | **PreCompact** | Before context compaction | No | No | State preservation before compaction |
| 19 | **PostCompact** | After compaction completes | No | No | Verify/reinject state after compaction |
| 20 | **Elicitation** | MCP server requests user input | Yes | No | Auto-fill or block MCP input requests |
| 21 | **ElicitationResult** | User responds to MCP elicitation | Yes | No | Override/validate user MCP responses |
| 22 | **SessionEnd** | Session terminates | No | No | Cleanup, final audit, session logging |

### Critical Payload Details

**PreToolUse -- most governance-rich payload:**
```json
{
  "tool_name": "Bash",
  "tool_input": { "command": "rm -rf ..." },
  "tool_use_id": "..."
}
```
Return options:
- `permissionDecision: "allow"` -- skip interactive prompt
- `permissionDecision: "deny"` + `permissionDecisionReason` -- cancel with feedback
- `permissionDecision: "ask"` -- show prompt to user
- `updatedInput: {...}` -- **modify tool parameters before execution** (underused)
- `additionalContext` -- inject context

**SubagentStop payload (blocking + rich):**
```json
{
  "stop_hook_active": false,
  "agent_id": "...",
  "agent_type": "...",
  "agent_transcript_path": "...",
  "last_assistant_message": "..."
}
```

**SessionEnd timeout: 1.5 seconds** (override: `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS`)

### Common Output Fields (all hooks)
```json
{
  "continue": false,
  "stopReason": "reason",
  "suppressOutput": true,
  "systemMessage": "warning"
}
```

---

## Production Governance Implementations

### HackerNoon (RuoYi-Plus Codebase)

**The 25% to 90% metric:**
- Baseline: Skills were "available context, not a hard constraint" -- agent used skills only 25% of the time
- Fix: UserPromptSubmit hook with MANDATORY evaluation template
- Result: 90%+ because hook eliminates "optional compliance" at the earliest moment before reasoning begins

**Implementation -- 4 hooks:**
1. **SessionStart**: Git branch + uncommitted changes + open TODOs + available commands
2. **UserPromptSubmit** (core): Forces mandatory skill evaluation protocol
3. **PreToolUse**: Hard blocks via regex: `rm -rf /`, `DROP DATABASE`, `/dev/sd*`
4. **Stop**: File change summary + suggested next actions

### Blake Crosley (84-Hook System)

**Scale:** 84 total hooks across 17 events -- largest documented production deployment
- 35 judgment hooks (gates, guards, validators)
- 49 automation hooks (injectors, loggers, trackers)

**Blast radius classification:**
- Local ops (file writes, tests) -> auto-approve
- Shared ops (git commits) -> warn
- External ops (pushes, API calls, deployments) -> defer to async notification

**Results:** "340 hooks fired across 5-story autonomous run; ~12 seconds overhead prevented three credential leaks and two incomplete implementations"

### Dotzlaw -- Deterministic Agent Engineering

**Core principle:** "That gap between 'usually' and 'always' is where production systems fail."

**Builder/Validator Pattern:**
- **Builder agent**: Full write access + PostToolUse quality hooks (linter + type checker) -> feedback via additionalContext
- **Validator agent**: `disallowedTools: [Write, Edit]` -> read-only enforcement, reviews builder output

**Critical safety principle:** "Never use prompt-based or agent-based hooks for hard safety boundaries." Command hooks only for non-negotiable constraints.

### Pixelmojo -- CI/CD Equivalent Patterns

| Hook Event | CI/CD Stage | Pattern |
|-----------|-------------|---------|
| PreToolUse | Pre-commit / pre-merge gate | Block before code acceptance |
| PostToolUse | Post-commit quality check | Auto-format, lint, type check |
| Stop | Final pipeline validation | Full test suite, security scan |

**Measured outcomes:**
- 66% productivity tax reduction (PostToolUse catches errors at generation time)
- 41% code churn reduction (PreToolUse prompt hooks verify architectural patterns)
- 45% vulnerability rate mitigation (PreToolUse security hooks + PostToolUse scans)

---

## Academic Frameworks -- Mechanism Mapping

### AgentSpec (ICSE 2026) -- arXiv:2503.18666

DSL for agent safety rules with trigger/check/enforce semantics. Results: 90%+ unsafe execution prevention, 100% hazardous action elimination, ~1.42ms overhead.

| AgentSpec Mechanism | Hook Event | Feasibility |
|---------------------|-----------|-------------|
| `before_action` trigger | PreToolUse | HIGH |
| `stop` enforcement | UserPromptSubmit or PreToolUse | HIGH |
| `user_inspection` | PermissionRequest / PreToolUse | HIGH |
| `invoke_action` | PostToolUse (additionalContext directive) | MEDIUM |
| `agent_finish` trigger | Stop / SubagentStop | HIGH |

### Agent Behavioral Contracts -- arXiv:2602.22302

Contract structure (6-tuple): Preconditions, Hard Invariants, Soft Invariants, Hard Governance, Soft Governance, Recovery.

**Drift Bounds Theorem:** Enforced contracts have mean-reversion level D* = alpha/gamma (natural drift / enforcement rate). When gamma > alpha, drift is bounded. Design criterion: gamma >= alpha/D_tol.

| Contract Mechanism | Hook Event | Feasibility |
|-------------------|-----------|-------------|
| Preconditions | UserPromptSubmit (block if not met) | HIGH |
| Hard Invariants | PreToolUse (block violating actions) | HIGH |
| Soft Invariants + recovery | PostToolUse (inject recovery directive) | MEDIUM |
| Hard Governance | PreToolUse (deny with reason) | HIGH |
| Cross-agent compositionality | SubagentStop (validate before allowing stop) | MEDIUM |

### PCAS -- arXiv:2602.16708

DAG-based provenance model with Datalog policy language. Results: 48% to 93% compliance. Baseline failed because agents "reframe semantically" in prompt-only enforcement.

### Pro2Guard -- arXiv:2508.00500

DTMC-based predictive enforcement. Results: 40.63% to 2.60% unsafe outcomes; 12.05% token reduction vs reactive enforcement.

### MI9 -- arXiv:2508.03858

Agentic Telemetry Schema with FSM conformance engine and drift detection. Results: 99.81% detection rate vs 93.98% (OpenTelemetry) vs 68.52% (LangSmith).

**Key insight:** Claude Code's hook events map closely to MI9's ATS schema. SubagentStart = subagent.spawn, PreToolUse = tool.invoke pre-event, PostToolUse = tool.invoke result.

---

## Cross-Tool Comparison

| Capability | Claude Code | Kiro (Amazon) | Cursor | GitHub Enterprise |
|-----------|-------------|---------------|--------|------------------|
| Event count | 22 | ~5-7 (inferred) | ~3-5 (inferred) | Platform-level only |
| Blocking hooks | 9 events | Unknown | Unknown | No (policy level) |
| Context injection | 7 events | Unknown | Unknown | No |
| Prompt hooks | Yes | No (inferred) | No (inferred) | No |
| Agent hooks | Yes (multi-turn + tools) | No (inferred) | No (inferred) | No |
| Tool input modification | Yes (PreToolUse updatedInput) | Unknown | Unknown | No |
| Per-agent hooks | Yes (agent frontmatter) | No (inferred) | No | No |

**Features Claude Code lacks:** spec-driven enforcement (Kiro), native audit trail, cross-session provenance (PCAS), temporal FSM enforcement (MI9), trust scoring (Microsoft toolkit), multi-agent message bus.

---

## Practical Limits and Failure Modes

### Documented Limitations

| Limitation | Impact |
|-----------|--------|
| PostToolUse cannot undo actions | Cannot roll back file writes or bash commands |
| PermissionRequest does not fire in permissive mode | Use PreToolUse for automated permission decisions |
| SessionEnd timeout: 1.5 seconds | Cleanup code must be very fast |
| HTTP hooks fail silently | Audit endpoint down = silent data loss |
| Stop hook fires on every response | Rate-limited with stop_hook_active check |
| Hooks do not fire on user interrupts | Ctrl+C bypasses Stop hook |

### Performance Data

| Source | Measurement | Finding |
|--------|------------|---------|
| AgentSpec | Parse + evaluate | 1.42ms + 1.11-2.83ms |
| Pro2Guard | Per-decision overhead | 5-30ms |
| Blake Crosley | Full 5-story run (340 hooks) | ~12 seconds total |
| Microsoft toolkit | Policy Engine per action | <0.1ms |

**Conclusion:** Hook overhead on happy path is negligible relative to LLM latency.

---

## Security-Governance Overlap

```
SECURITY ONLY          | BOTH                    | GOVERNANCE ONLY
-----------------------|-------------------------|------------------
Secret scanning         | Audit logging           | Process sequence enforcement
PII filtering           | PreToolUse blocking     | Skill activation compliance
Credential leak detect  | Permission management   | Task completion gates
Supply chain (npm)      | Trust scoring           | State preservation
Ed25519 identity        | Policy enforcement      | Behavioral initialization
Cryptographic signing   | Managed settings        | Quality feedback loops
                        | HTTP audit endpoints    | Observability pipeline
```

### Security Patterns Worth Adopting for Governance

1. **Audit trail pattern** -- HTTP PostToolUse endpoint serves both security and governance compliance
2. **Trust scoring** -- compliance history informs enforcement aggressiveness
3. **Blast radius classification** -- local/shared/external maps to auto-approve/warn/defer
4. **Hard/soft constraint separation** -- command hooks for non-negotiable constraints, prompt hooks for judgment
5. **Managed settings as governance override** -- organization policies enforce both security and process
6. **Provenance tracking** -- SubagentStart/SubagentStop build causal chains for accountability

---

## Prioritized Governance Patterns

### Tier 1 -- High Impact, Low Effort

1. **PreToolUse safety gate** -- Block destructive commands. Evidence: HackerNoon, Dotzlaw, Pixelmojo all implement this as foundation.
2. **SubagentStop quality gate** -- Block subagents until output meets criteria. Currently unused despite HIGH blocking capability.
3. **PostToolUseFailure recovery injection** -- Inject actionable guidance on errors. Currently: failures pass silently.

### Tier 2 -- High Impact, Medium Effort

4. **SessionEnd mandatory state write** -- Force state update before session terminates (1.5s timeout constraint).
5. **ConfigChange blocker** -- Block unauthorized settings modifications during sessions.
6. **HTTP audit endpoint** -- PostToolUse HTTP hook for structured governance logging.
7. **PostCompact verification** -- Verify critical state was preserved after compaction.

### Tier 3 -- Medium Impact, High Effort

8. **Agent Behavioral Contract enforcement** -- ContractSpec YAML per agent with hard/soft invariants.
9. **Cross-agent provenance tracking** -- SubagentStart/Stop pairs building causal chains.
10. **MI9-style FSM for workflow conformance** -- Define finite state machines for critical workflows.

---

## Cross-References Between Findings

- PreToolUse's `updatedInput` field enables AgentSpec's `invoke_action` -- not just block, but redirect to safer alternative
- Blake Crosley's 12-second overhead across 340 hooks confirms: hook overhead is negligible even at scale
- Agent Behavioral Contracts' recovery mechanism explains WHY the HackerNoon hook achieved 25% to 90% improvement: enforcement rate exceeded natural drift rate
- MI9's ATS event schema maps almost exactly to Claude Code's 22-event taxonomy
- HTTP hook type is the native mechanism for security audit trails that also serve governance
