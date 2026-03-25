# Writing PM Instructions for LLM Agents

How to write project management instructions that LLM agents actually follow. Based on research into prompt engineering, inline bias, and practical experience with 28+ agent infrastructure.

## The Problem

A PM orchestrator agent needs instructions that cover lifecycle phases, field management (scope, risk, progress, etc.), governance, and feedback loops. The challenge: LLM agents have finite context, attention degradation, and tendency toward premature convergence.

## Key Background

1. **Process skills are training wheels**: Good prompts + rich context = quality work without ceremony. Govern routing, not execution.
2. **Inline bias is structural**: 12.4% reasoning-action mismatch, 78.5% persistence. Prompt rules alone can't fix it — only architectural interventions work.
3. **Exploration before extraction**: "What's here?" prompts leverage context better than "give me X" prompts.
4. **SOPs work for AI agents** (MetaGPT pattern): Defined inputs/outputs/handoffs produce reliable results.

---

## Format Principles

### 1. Structured Roles, Not Prose

**Bad:** "You are a project manager. Keep track of everything and make sure things go well."

**Good:**
```
## Your Role: PM Orchestrator
You manage project lifecycle phases. You do NOT execute work — you coordinate agents who execute.

## Inputs You Receive
- STATE.md (current project status)
- task_plan.md (task list with priorities)
- User requests (new work, status queries, direction changes)

## Outputs You Produce
- Updated STATE.md
- Task assignments to specialist agents
- Phase transition recommendations
- Risk alerts when blockers detected
```

### 2. Decision Trees, Not Guidelines

**Bad:** "Consider the project status and decide what to do next."

**Good:**
```
IF no STATE.md exists -> Phase: INITIATION
IF STATE.md exists AND task_plan.md is empty -> Phase: PLANNING
IF tasks exist AND some are in-progress -> Phase: EXECUTION
IF all tasks complete -> Phase: REVIEW
IF review passed -> Phase: CLOSURE
```

### 3. Checkpoints as Explicit Steps

**Bad:** "Periodically check if the project is still on track."

**Good:**
```
## Checkpoint: Run After Every Milestone
1. Read STATE.md — is the status current?
2. Read task_plan.md — are priorities still correct?
3. Ask: "Has anything changed that affects the business case?"
4. Ask: "Are any tasks blocked? What's the oldest blocked item?"
5. Ask: "Is the next step still the right next step?"
6. Update STATE.md with findings
7. If business case invalidated -> recommend PAUSE
```

### 4. Field Coverage via Questions, Not Descriptions

Rather than describing each PM field, encode them as questions the agent must answer:

```
## Status Assessment Questions (answer all at each checkpoint)
- SCOPE: What's in scope? Has scope changed since last check?
- PRIORITY: What matters most right now? Has priority shifted?
- PROGRESS: What's done? What's in progress? What's blocked?
- RISK: What could go wrong? Any new risks since last check?
- QUALITY: Does completed work meet acceptance criteria?
- CHANGE: What decisions were made? What changed and why?
- GOVERNANCE: Should we still be doing this? (business case check)
```

### 5. Artifacts as Contracts, Not Suggestions

**Bad:** "You might want to keep a STATE.md file updated."

**Good:**
```
## Required Artifacts (non-negotiable)
- STATE.md: MUST be updated after every milestone.
- task_plan.md: MUST reflect current tasks with status.

## Artifact Update Rules
- STATE.md is REWRITTEN (not appended) at each checkpoint
- task_plan.md items move through: TODO -> IN PROGRESS -> DONE
- Completed items move to archive/ with date prefix
```

---

## What LLM Agents Ignore (Anti-Patterns)

| Anti-Pattern | Why It Fails | Better Approach |
|---|---|---|
| **Long prose descriptions** | Attention degradation; buried signals | Structured sections with headers |
| **Aspirational guidelines** ("strive for quality") | Too vague to act on | Concrete checkpoints with pass/fail criteria |
| **Exhaustive process lists** | Performative compliance | Minimal essential rules + exploration prompts |
| **Conditional mandates** ("always X unless Y") | Agents optimize for compliance, not judgment | Decision trees with explicit conditions |
| **Emotional framing** ("be careful", "think deeply") | No behavioral effect | Architectural interventions (hooks, reviews) |
| **Self-monitoring instructions** ("check your own work") | Same-model bias; 78.5% error persistence | External review (different agent/model) |

---

## Instruction Architecture

Based on all research, the optimal structure:

```
1. ROLE DEFINITION (who you are, what you do/don't do)
2. LIFECYCLE PHASES (decision tree for phase identification)
3. PHASE-SPECIFIC ACTIONS (what to do in each phase)
4. CHECKPOINT PROTOCOL (questions to answer at each checkpoint)
5. ARTIFACT CONTRACTS (what files to maintain, format, update rules)
6. DELEGATION RULES (which agents handle which work)
7. ESCALATION RULES (when to ask the human)
8. KILL CRITERIA (when to recommend stopping)
```

### Key Design Decisions

| Decision | Recommendation | Rationale |
|---|---|---|
| Lifecycle model | Adaptive (inspect-and-adapt) | Predictive fails with AI agents (plans go stale) |
| Phase transitions | Question-driven checkpoints | LLM agents work better with exploration prompts than checklists |
| Governance | Circuit breaker + business case question | Automated governance > human-dependent governance |
| Feedback loops | Built into checkpoint protocol | External review via separate agent > self-review |
| Artifact format | Markdown with YAML frontmatter | Structured enough for parsing; flexible enough for content |

---

## Cross-System Lessons

| System | Key Lesson |
|---|---|
| **MetaGPT** | SOPs with defined I/O/handoffs produce reliable agent behavior |
| **Jules** | Rules directory (deterministic governance) > prompt suggestions |
| **ChatDev** | Agent-to-agent review catches errors that self-review misses |
| **Hooks systems** | Architectural enforcement (hooks) > prompt-level instructions |
| **Process skills** | Training wheels — useful for unfamiliar tasks, overhead for familiar ones |
| **Ensemble research** | Same-model self-correction is unreliable; use architectural separation |
