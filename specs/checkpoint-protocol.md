# PM Lifecycle Checkpoint Protocol

Synthesized findings from research into PM frameworks, LLM instruction formats, infrastructure mapping, and AI PM lessons. This defines a checkpoint protocol for AI agent project management -- the 5-question protocol, the instruction format that works for LLMs, the infrastructure mapping, and the gaps no existing AI PM system addresses.

---

## 1. The 5-Question Checkpoint Protocol

A "complete" PM framework must answer these 5 questions at every checkpoint. If any answer is missing or stale, the checkpoint fails.

| # | Question | What It Checks | Required Answer Format |
|---|----------|----------------|----------------------|
| Q1 | **What exists?** | Full inventory of scope, deliverables, artifacts | Flat ordered list derivable from ONE place |
| Q2 | **What matters most?** | Priority ranking with rationale | Top item + WHY it is top + what happens if delayed |
| Q3 | **What is happening?** | Active work, current phase, in-flight items | Current phase + active tasks + blockers |
| Q4 | **What changed?** | Deviations, new risks, scope changes, decisions | Delta since last checkpoint + decision rationale |
| Q5 | **What is done?** | Completed work against acceptance criteria | Completed items + DoD pass/fail + value delivered |

### Pass/Fail Criteria

Each question has three levels. Minimum passing = Level 2.

**Q1 (Inventory):**
- L1: "We have stuff" (items exist somewhere) -- FAIL
- L2: Single authoritative list, all items accounted for -- PASS
- L3: List with dependencies, groupings, and scope boundaries marked -- STRONG

**Q2 (Priority):**
- L1: "Everything is important" (no ranking) -- FAIL
- L2: Ordered list with top 3 explicit + WIP limit enforced -- PASS
- L3: Ordered with cost-of-delay reasoning and appetite per item -- STRONG

**Q3 (Status):**
- L1: "Working on it" (no specifics) -- FAIL
- L2: Current phase identified, active tasks named, blockers listed -- PASS
- L3: Phase + progress indicators + estimated remaining effort -- STRONG

**Q4 (Change):**
- L1: No change tracking -- FAIL
- L2: Key decisions logged with date and rationale -- PASS
- L3: Decisions + scope delta + risk register updated -- STRONG

**Q5 (Completion):**
- L1: "It is done" (no criteria) -- FAIL
- L2: DoD checklist passed + item archived -- PASS
- L3: DoD + stakeholder acceptance + value delivery confirmed -- STRONG

### Business Case Meta-Question (Q6 -- phase transitions only)

> "Should we still be doing this project?"

This is the PRINCE2 continued business justification check. It does NOT run at every checkpoint -- only at phase transitions and when Q4 reveals significant change.

---

## 2. LLM Instruction Format That Works

The playbook must use this structure, in this order:

```
1. ROLE DEFINITION       -- who you are, what you do/don't do
2. LIFECYCLE PHASES       -- decision tree for phase identification
3. PHASE-SPECIFIC ACTIONS -- what to do in each phase
4. CHECKPOINT PROTOCOL    -- 5 questions to answer at each checkpoint
5. ARTIFACT CONTRACTS     -- what files to maintain, format, update rules
6. DELEGATION RULES       -- which agents handle which work
7. ESCALATION RULES       -- when to ask the human
8. KILL CRITERIA          -- when to recommend stopping
```

### Critical Format Rules

| Rule | Rationale |
|------|-----------|
| **Decision trees, not guidelines** | "IF condition THEN action" beats "consider doing X" |
| **Questions, not descriptions** | "Has scope changed?" beats "Scope management is important" |
| **Contracts, not suggestions** | "STATE.md MUST be updated" beats "You might want to update STATE.md" |
| **Structured sections with headers** | Agents lose signals buried in prose paragraphs |
| **Explicit I/O per phase** | Define what the agent reads and writes for every phase |
| **Exploration before extraction** | "What is here?" prompts at checkpoint entry; "update X" at exit |

### Anti-Patterns (produce performative compliance)

| Anti-Pattern | Why It Fails | Replacement |
|---|---|---|
| Long prose descriptions | Attention degradation buries signals | Structured sections + headers |
| "Strive for quality" | Too vague; no behavioral effect | Concrete pass/fail criteria |
| Exhaustive checklists | Performative compliance | Minimal essential rules + exploration questions |
| "Always X unless Y" | Agents optimize for compliance, not judgment | Decision trees with explicit branches |
| "Check your own work" | Same-model bias; 78.5% error persistence | External review via different agent |
| "Think deeply about..." | Emotional framing has zero effect on LLMs | Architectural intervention (hook, review agent) |

### Key Insight: Govern Routing, Not Execution

Process skills are training wheels. The orchestrator should route work to the right agent with the right context, then validate outputs. It should NOT micromanage how agents do their work. MetaGPT's SOP lesson: defined I/O boundaries + handoff protocols outperform detailed step-by-step instructions within a phase.

---

## 3. Phase-to-Tool Infrastructure Map

| Lifecycle Phase | Primary Tool | Secondary Tool | Artifact Modified |
|---|---|---|---|
| **INITIATION** | Task classifier | PM orchestrator | Creates STATE.md + PROJECT.md |
| **PLANNING** | Implementation-plan agent | Planning process skill | Creates task_plan.md |
| **EXECUTION** | Specialist agents | Build/research/analysis process skills | Updates task_plan.md items |
| **MONITORING** | PostToolUse checkpoint hook | PM orchestrator checkpoint protocol | Updates STATE.md |
| **REVIEW** | Architect-reviewer + adversarial-reviewer | Prompt-engineer (for LLM outputs) | Produces review findings |
| **CLOSURE** | Save skill | Vault-keeper (archive movement) | Archives, updates STATE.md |

### Phase Detection Logic

```
IF no STATE.md exists for project
  -> Phase: INITIATION

IF STATE.md exists AND task_plan.md missing or empty
  -> Phase: PLANNING

IF tasks exist AND none started
  -> Phase: PLANNING (plan exists but execution not begun)

IF tasks exist AND some IN PROGRESS
  -> Phase: EXECUTION

IF all tasks DONE AND no review completed
  -> Phase: REVIEW

IF review passed AND not archived
  -> Phase: CLOSURE

IF appetite exceeded (time budget spent)
  -> Phase: CIRCUIT BREAKER (escalate to user)

IF business case invalidated
  -> Phase: KILL (recommend termination)
```

---

## 4. AI PM Lessons from Existing Systems

### What Works

| Approach | Evidence | Implication |
|---|---|---|
| SOPs with defined I/O | MetaGPT produces reliable output when each agent has clear inputs/outputs/handoffs | Every phase must specify: what the orchestrator reads, produces, hands off to |
| Role separation | ChatDev's reviewer-coder pairing catches errors self-review misses | Quality review must always be a DIFFERENT agent than the builder |
| Deterministic governance | Jules rules/ directory outperforms prompt-based guidance | Hooks and config rules are the right enforcement mechanism |
| Investigation budgets | Jules caps exploration before committing to action | The orchestrator should have an investigation budget per phase |
| Human review as quality gate | Devin submits PRs; Jules requires human approval | Human review is the FINAL gate before CLOSURE, not optional |

### What Fails

| Approach | Evidence | What to Avoid |
|---|---|---|
| Waterfall between phases | MetaGPT and ChatDev have no feedback loops | Support returning to earlier phases |
| No adaptive replanning | MetaGPT creates a plan once and never revises | Re-evaluate the plan at every checkpoint |
| No kill mechanism | No AI PM system implements circuit breakers | Build in appetite and enforce it |
| Self-review | Same-model bias: 78.5% error persistence | Never let the orchestrator review its own work |

### The Positioning Gap

Current AI PM tools fall into two categories:
1. **Role simulation** (MetaGPT, ChatDev): Full agent pipelines, but waterfall with no adaptation
2. **Tool augmentation** (Linear+AI, Taskade): AI assists humans, but no lifecycle management

What does NOT exist: **An adaptive, checkpoint-driven AI PM lifecycle with feedback loops, kill mechanisms, and governance hooks.**

---

## 5. Cross-Cutting Themes

**Exploration prompting IS the checkpoint mechanism.** The 5 questions are exploration prompts by design ("What exists?" "What changed?"). Exploration prompts outperform extraction prompts for status assessment.

**Architectural enforcement over prompt instructions.** Prompt-level instructions get ignored (attention degradation, performative compliance). Hooks and config rules enforce governance architecturally.

**Circuit breaker is the highest-priority gap.** Shape Up's circuit breaker is the strongest completion/kill pattern. No AI PM system implements it. Implementation: appetite field in STATE.md, checked at every checkpoint, escalate when exceeded.

**GTD + Personal Kanban is the solo operator base.** GTD's capture/clarify/organize/reflect/engage maps to inbox processing + task plan + state files + checkpoint + execution.
