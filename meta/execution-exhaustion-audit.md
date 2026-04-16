
# Execution & Exhaustion Audit — Honest Assessment

## Criterion 1: Does it force ACTUAL EXECUTION?

### Process Skills

| Skill | Says "execute" | How | Enforced? | Verdict |
|-------|---------------|-----|-----------|---------|
| process-qa | YES — "You MUST actually execute the test — do not reason about whether it would pass" (line 56) | Verification method table lists Bash, MCP, Agent | NO — hook checks format only (QA REPORT + PASS/FAIL) | **STATED, NOT ENFORCED** |
| process-pentest | YES — "pipe inputs through hooks, run scripts, read files, use MCP. Do not reason" (line 34) | Test categories with execution examples | NO — hook checks PENTEST REPORT format only | **STATED, NOT ENFORCED** |
| process-build | PARTIALLY — "fetch current workflow first" (line 45), "Live verification" (line 74) | But "live verification" is the last checkbox item, easily skipped | NO — no hook checks for MCP/Bash during build | **STATED, NOT ENFORCED** |
| process-research | NO — says "delegate" and "collect findings" | No execution step. Research is reading + synthesis | N/A — research doesn't produce testable claims | **NOT APPLICABLE** |
| process-planning | NO — says "design, not build" (line 93) | No execution step | N/A | **NOT APPLICABLE** |
| process-analysis | NO — says "evaluate" and "delegate to specialist" | Specialist agents read and reason | N/A for most, but investigation-mode SHOULD verify | **GAP for investigation mode** |

### Hooks

| Hook | Checks execution? | What it actually checks |
|------|-------------------|----------------------|
| process-step-check.py | NO | String "QA REPORT" + PASS/FAIL regex. Does NOT check for tool_use blocks (Bash, MCP). |
| dispatch-compliance | NO | That Skill/Agent tools were called. Not what happened inside. |
| classifier-field-check | NO | That MUST DISPATCH field exists and contains pm. Not what pm does. |
| subagent-quality-check | NO | Output length and structure. Not whether agent executed anything. |
| All others | NO | They check process compliance (fields, routing, safety), never execution. |

### CLAUDE.md

| Section | Says "execute"? | Enforced? |
|---------|----------------|-----------|
| QA section | "Verify claims empirically — execute tests, read outputs, check assertions" | NO — soft instruction |
| Iterative Working | Nothing about execution | N/A |
| Task Classification | "You have Bash, Read, MCP — use them to actually test" (Step 6, line 216) | NO — soft |
| No Unsolicited Changes | N/A | N/A |

### VERDICT ON CRITERION 1

**Zero enforcement of actual execution anywhere in the system.** The words "execute," "actually test," "pipe inputs," "run scripts" appear in 3 skills and 1 CLAUDE.md section. But no hook, no agent, no gate verifies that Bash/MCP/tool_use blocks were actually invoked during QA or pentest. The QA REPORT format passes all hooks whether the evidence came from running a bash command or from reading a file and guessing.

---

## Criterion 2: Does it force EXHAUSTING AUTONOMOUS OPTIONS before asking the user?

### What says "exhaust before asking"

| Source | What it says | Enforced? |
|--------|-------------|-----------|
| CLAUDE.md | NOTHING. No instruction says "try everything before asking." | ABSENT |
| task-classifier Step 48 | "QA is the mechanism that extends autonomous run length" | Aspirational — no enforcement |
| process-pentest line 82 | "After 2 failed fix attempts on the same finding: ESCALATE to user" | STATED — but no hook counts fix attempts |
| process-qa line 53 | "If all attempts to fix fail, escalate to the user" | STATED — no hook counts attempts |
| MEMORY.md | "Don't stop to ask when told to go" (feedback) | STATED — soft only |
| MEMORY.md | "Autonomy target: exhaust all autonomous capabilities before asking for help" | STATED — soft only |

### What actually forces exhaustion

**Nothing.** There is no hook that:
- Counts how many fix attempts were made before escalation
- Detects "asking the user" and checks whether alternatives were tried
- Blocks premature escalation with "you haven't tried X yet"
- Verifies that Bash, MCP, WebSearch, Agent tools were all attempted before giving up

### Common failure modes (observed)

1. **First error → ask user.** Hit a bug → "Should I fix this?" instead of fixing it, testing the fix, retrying.
2. **Single approach → give up.** Try one method, fail, escalate. Don't try alternative tools, different agents, or workarounds.
3. **"I can't do X" without trying.** Claim a limitation without actually testing whether the tool can do it.
4. **Theoretical QA → PASS.** Read the artifact, reason about correctness, write PASS. Never run it.
5. **Skip live verification.** Build a hook, write QA REPORT PASS, never pipe test input through the hook.

### VERDICT ON CRITERION 2

**Zero enforcement of autonomous exhaustion anywhere in the system.** The concept exists in MEMORY.md and CLAUDE.md aspirationally, but nothing forces me to try harder before asking you. No hook counts attempts. No gate blocks premature escalation. The "2 failed fix attempts" rule in process-pentest is a soft instruction that is never verified.

---

## Gap Summary

| Gap | Severity | Impact |
|-----|----------|--------|
| No hook verifies tool_use during QA/pentest | CRITICAL | QA is performative — passes without testing |
| No hook detects/blocks premature user escalation | CRITICAL | I ask for help instead of trying harder |
| No retry/attempt counting for fix loops | HIGH | "After 2 failed attempts" rule is unenforceable |
| No "live verification" enforcement for builds | HIGH | Built artifacts never tested against live system |
| process-analysis has no execution step | MEDIUM | Investigation mode reasons but doesn't verify |
| CLAUDE.md has no "exhaust before asking" rule | MEDIUM | The principle exists only in MEMORY.md feedback |

## What Would Fix This

### For Execution (Criterion 1):

**Fix A — tool_use count in QA/pentest turns.** process-step-check adds: after process-qa or process-pentest invocation, count tool_use blocks with name in [Bash, mcp__*]. If QA REPORT/PENTEST REPORT exists but 0 execution tools used → HARD BLOCK.

**Fix B — Evidence format in QA REPORT.** Require each evidence cell to reference a tool output. Hook checks for patterns: `$ `, `Output:`, `Error:`, `mcp__`, tool_result blocks. Theoretical evidence = block.

### For Exhaustion (Criterion 2):

**Fix C — CLAUDE.md exhaustion rule.** Add to CLAUDE.md: "Before asking the user for help: (1) Try at least 2 different approaches, (2) Use Bash to test your hypothesis, (3) Search for similar patterns in the codebase, (4) Check if an agent could help. Only escalate after all 4."

**Fix D — Escalation gate hook.** A Stop hook that detects "asking the user" patterns (question marks at end of response, "should I", "do you want me to", "what would you prefer") and checks whether tool_use blocks appear earlier in the turn. If asking without having tried → soft warning (log, don't block — blocking questions is too aggressive).

**Fix E — Retry enforcement.** process-pentest and process-qa track fix attempts. If a FAIL is found and the next action is not a fix attempt (tool_use targeting the failed area) → soft warning.

## Honest Self-Assessment

This system is advanced at PROCESS COMPLIANCE (routing, classification, delegation, format checking) and ABSENT at EXECUTION COMPLIANCE (did you actually run it) and EXHAUSTION COMPLIANCE (did you actually try). The hooks verify I followed the steps. They do not verify I did real work at each step. This is the equivalent of checking that a student submitted their homework in the correct format, without reading whether the answers are real.
