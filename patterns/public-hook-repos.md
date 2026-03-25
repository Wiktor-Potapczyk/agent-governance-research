# Public Claude Code Hook Repositories

A survey of confirmed public repositories with working hook implementations for Claude Code. These represent the state of the art in community-built governance infrastructure as of March 2026.

## Reference Implementations

| Repo | Language | What | Key Pattern |
|------|----------|------|-------------|
| disler/claude-code-hooks-mastery | Python (UV) | Stop hook + PostToolUse linting + transcript conversion | Most complete public example. Builder/validator. |
| blader/taskmaster | Bash | Stop hook scanning for TASKMASTER_DONE token | Machine-checkable completion tokens > LLM self-assessment |
| GowayLee/cchooks | Python | SDK with StopContext class | Abstracts payload parsing + exit code semantics |
| fongandrew gist | Bash | stop-hook.sh | Single-file example |
| vinicius91carvalho/.claude | Unknown | Full personal .claude config | Community example |

## Critical Bugs to Be Aware Of

- Stop hooks in SKILL.md files never fire (issue #19225)
- Stop hooks with exit 2 fail via plugins, work in .claude/hooks/ (issue #10412)
- /clear corrupts transcript_path (issue #3046)
- Stale session_id after --continue (issue #9188)

## Key Insight

The Taskmaster pattern (machine tokens in transcript) is more reliable than LLM self-assessment for completion checking. A deterministic token scan ("did the agent output DONE_TOKEN?") beats asking the model "are you done?"

## Gap

All public examples are bash/Python. No PowerShell examples exist. Windows users must adapt patterns from Unix implementations.
