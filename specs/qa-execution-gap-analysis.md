
# QA Execution Gap Analysis

## Problem

QA and pentest default to theoretical verification (reading files, reasoning about outcomes) instead of empirical execution (running bash commands, triggering hooks, executing workflows via MCP). The skills explicitly say "MUST actually execute" but nothing enforces it.

## Root Cause

The enforcement chain checks QA FORMAT but not QA METHOD:
- process-step-check.py checks: "QA REPORT" string + PASS/FAIL regex → PASS
- dispatch-compliance checks: process-qa Skill was invoked → PASS
- Neither checks: were Bash/MCP tools actually used during verification?

A QA REPORT that says "PASS — read the file and it looks correct" passes all hooks identically to "PASS — ran bash command, observed correct output."

## Evidence

- process-qa SKILL.md line 56: "You MUST actually execute the test — do not reason about whether it would pass"
- process-pentest SKILL.md line 34: "pipe inputs through hooks, run scripts, read files, use MCP. Do not reason about what would happen"
- process-step-check.py line 58-59: `if "QA REPORT" in text and re.search(r'(?:PASS|FAIL)', text)` — format-only check

## Fix Options

| Option | Mechanism | Enforcement | Complexity |
|--------|-----------|-------------|------------|
| A — Hook checks for tool_use during QA | process-step-check verifies Bash/MCP tool_use blocks exist in QA turn | Hard | Medium |
| B — Evidence format requirement | Require command output in Evidence column | Medium (regex) | Low |
| C — Structural separation | Test plan → Execute → Report as separate steps | Hard (process change) | High |
| D — Minimum tool_use count | Count Bash/MCP calls after process-qa invocation, block if 0 | Hard | Low |

## Recommendation

Option D (minimum tool_use count) is the simplest and most reliable. After process-qa is invoked, the hook counts tool_use blocks with name matching Bash or mcp__*. If QA REPORT exists but zero execution tools were used → block with "QA REPORT present but no empirical verification detected. Execute tests before reporting."

Same logic for process-pentest.

Exception: claims that can only be verified by reading (e.g., "file exists", "config is registered") use Read/Grep — these should count too. So the check should be: at least 1 tool_use with name in [Bash, Read, Grep, Glob, mcp__*] after process-qa invocation. This allows Read-based verification while still blocking zero-tool QA.
