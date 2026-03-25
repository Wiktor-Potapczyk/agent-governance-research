# Lifecycle Implementation Analysis: Non-Quick Tasks Get Project Treatment

This document analyzes the infrastructure constraints and enforcement map for treating every non-trivial task as a mini-project with full lifecycle treatment — classification, decomposition, QA, and pentesting.

## Core Finding

The system has all pieces for lifecycle treatment of every non-trivial task. The gap is connecting them. Hooks can enforce per-task QA (Tier 1) but CANNOT enforce increment-level pentesting (Tier 2) because hooks cannot read task state. The increment boundary must be self-enforced via prompt instructions and PM checkpoints.

## Infrastructure Constraints

| Capability | Available to hooks? | Available to main session? |
|-----------|-------------------|--------------------------|
| Read transcript | Yes (all Stop hooks) | Yes |
| Detect tool-use blocks | Yes (dispatch compliance) | Yes |
| Read task creation/list state | **No** | Yes (native tools) |
| Count completed tasks | **No** (fragile transcript parsing) | Yes |
| Execute tools (Bash/Read) | **No** (hooks are check-only) | Yes |
| Block responses | Yes (Stop hooks) | N/A |
| Inject context | Yes (PostToolUse) | N/A |

## Enforcement Map

| Rule | Enforcement | Type | Mechanism |
|------|-------------|------|-----------|
| Non-trivial must classify with all fields | HARD | Hook | Classifier field check |
| MUST DISPATCH items must be invoked | HARD | Hook | Dispatch compliance check |
| Process skills must produce SCOPE blocks | HARD | Hook | Process step check |
| QA process must produce QA REPORT | HARD | Hook | Process step check |
| Multi-step tasks must use task creation | **SOFT** | Prompt | Classifier skill text |
| Increment boundary triggers pentest | **SOFT** | Prompt | Classifier + process skill text |
| Pentest must produce PENTEST REPORT | HARD (once invoked) | Hook | Process step check |
| Pentest tests the right things | **NOT ENFORCEABLE** | Human | Untested Surface list |

## What to Build (Priority Order)

### P0: Pentest process skill
New skill. The main session (not an agent) executes tests. Steps:
1. PENTEST SCOPE block (increment ID, artifacts to test)
2. Identify attack surface (what could break?)
3. Execute tests per category (boundary, adversarial, regression, failure modes, integration)
4. PENTEST REPORT with findings + severity + Untested Surface
5. Recommendation: SHIP / FIX / ESCALATE

### P1: Classifier rule addition
Add to classifier: "If non-trivial with 2+ steps: MUST create task list before executing. When all tasks completed, invoke pentest before reporting back."

### P2: Process step check update
Add pentest scope and report patterns to the step verification hook.

### P3: PM checkpoint enhancement
Add check: "Is there a task list? Are all tasks completed? If yes and no PENTEST REPORT → recommend pentesting."

## What NOT to Build

- No pentesting agent — main session has Bash/Read/MCP
- No hook for task creation enforcement — hooks cannot read task state
- No automated increment boundary detection — PM + self-enforcement is sufficient
- No cross-session task persistence beyond the task plan file

## Design Principle

Match enforcement to observability. Hard-enforce what hooks can see (PENTEST REPORT in output). Soft-enforce what hooks cannot see (all tasks completed). Accept the split.
