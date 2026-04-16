
# Gulli "Agentic Design Patterns" — Comparison Findings

## Source
Antonio Gulli (Senior Google Engineer). "Agentic Design Patterns: A Guide to Building Intelligent Systems." 421 pages, 21 design patterns. Extracted via NotebookLM with our architecture.md, README.md, and research insights as context.

## Already Validated by Our Framework
- Modularity + separation of concerns → our 4-layer architecture, 29 specialist agents
- "Contractor model" with specifications → classifier IMPLIES + SCOPE blocks + acceptance criteria
- Context engineering over prompt engineering → SubagentStart hook injects CLAUDE.md + MEMORY.md + skills
- Escalation policies → "exhaust before asking" + work-verification-check
- Checkpointing → STATE.md + PreCompact hook
- Human-in-the-loop → hard blocks require human to unblock
- Positive instructions > negative constraints → matches our hooks-over-prompts finding (90% vs 25%)

## Actionable Gaps (Worth Stealing)

### 1. Evaluating Agent Trajectories (HIGH priority)
Our QA checks WHAT was produced but not HOW. Gulli says: evaluate the agent's trajectory — the exact sequence of thoughts, tool selections, and actions. Compare against expected "ground truth" trajectory using precision/recall.

**How it applies:** process-qa could add trajectory scoring — was the tool sequence efficient? Did it explore before concluding? Currently work-verification-check only counts tools crudely.

### 2. Loop/Stagnation Detection (MEDIUM priority)
Gulli describes asynchronous overseers that monitor for "pathological deviations, loops, or stagnation." Our Stop hooks are the equivalent mechanism but we don't detect loops or stagnation specifically.

**How it applies:** A Stop hook that detects repeated identical tool calls or extended periods without progress.

### 3. State Rollback on Failure (MEDIUM priority)
When our hooks block, the failed attempt's state remains in context. Gulli advocates state rollback — undoing recent changes to return to a stable state before retrying.

**How it applies:** A "clean retry" mechanism when hooks block. Currently the agent retries with the failed attempt still in context, potentially anchoring on the same bad approach.

### 4. Flexibility vs Predictability Tradeoff (LOW priority — validates existing design)
"When a problem is well-understood, constraining to a fixed workflow is more effective." Validates our process skills for known task types. Also suggests Quick tasks could be MORE constrained.

### 5. Scaling Inference Law (LOW priority — testable)
Smaller model + more thinking budget > bigger model. If Haiku gets a longer CoT budget, it might match Sonnet for classification. Testable with promptfoo.

## Not Actionable for Us
- **RAG/vector memory** — real problem but wrong solution for CLI. Our file-based memory + PreCompact fits the constraint.
- **Dynamic model routing** — Sonnet usage counts toward same limit. No cost savings.
- **A2A inter-agent protocol** — we're single-operator CLI, not network services.
- **Self-modification** — opposite of our philosophy. Agents editing own hooks defeats "process enforced, not suggested."
- **ToT/GoD reasoning** — needs Agent Teams (deferred) or Claude Code branching support.
- **Dynamic prioritization** — WIP=1 is deliberate (prevents context thrashing).

## Key Gulli Quotes
- "Agents require MORE deterministic support, not less" — confirms our hook architecture
- "Excessive reliance on negative constraints can confuse the model" — confirms positive-instruction approach
- "When a problem is well-understood, constraining to a fixed workflow is more effective" — validates process skills
- "Traditional pass/fail software testing is entirely insufficient for non-deterministic agents" — validates our Popperian QA approach
