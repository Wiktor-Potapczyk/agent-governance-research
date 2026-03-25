# Autonomous Research Loop Reliability Issues

Documentation of confirmed reliability issues with autonomous multi-iteration research loops (specifically the Ralph Loop plugin for Claude Code). These issues affect any system that uses Stop hooks for loop continuation across sessions. The core problems are a cross-session hook scoping bug and context exhaustion on large loops.

---

## Cross-Session Stop Hook Bug (Confirmed)

**Verified by source code analysis + GitHub issues:**
- GitHub issue #15047 (Dec 2025, closed Not Planned)
- GitHub issue #26514 (Feb 2026, closed Not Planned)
- PR #606 (Mar 2026) submitted fix but closed -- repo rejects external PRs

**Root cause:** The setup script writes `session_id: ${CLAUDE_CODE_SESSION_ID:-}` but Claude Code never populates the `CLAUDE_CODE_SESSION_ID` environment variable. The state file gets an empty session_id. Guard logic that checks session ID is dead code because the check fails on an empty string.

**Impact:** Stop hooks fire globally across all sessions in the same project directory. A loop running in one session will intercept stop events from other sessions.

**Official docs confirm:** Hooks are NOT session-scoped. It is the plugin's responsibility to check session_id from the JSON payload.

## Context Exhaustion Pattern

Large research loops exhaust context before saving findings. Parallel agent results expand unpredictably. By iteration 15-20, compaction fires, and the loop loses accumulated findings.

## Additional Bug: Echo Corrupts JSON

`echo` corrupts JSON containing `\n` escape sequences (issue #394, unfixed). `jq` rejects the malformed JSON, the hook deletes the state file, and the loop dies after one iteration.

## Mitigations

1. Only run autonomous loops when NO other session is open in the same project directory
2. For multi-session work, ignore stop hook messages in non-loop sessions
3. For large loops: force incremental saves after each problem, or have agents write to separate files
4. Track background agent IDs to avoid orphaned agents
5. Git worktrees provide separate directories as a workaround (not available in all environments)
6. Local fix: patch cached stop-hook files so that the first invocation claims the session by writing its session_id to the state file. Other sessions then see a non-matching ID and exit. This fix is overwritten on plugin update.

## Design Implications

Any system using Stop hooks for loop continuation must:
- Implement its own session scoping (do not rely on the platform)
- Handle context exhaustion with incremental persistence
- Test shell escaping in hook JSON output
- Account for the 1.5-second SessionEnd timeout constraint
