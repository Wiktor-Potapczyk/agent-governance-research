# Process Network Architecture

This document is the architecture specification for the process network — the interconnected system of roles, agents, enforcement hooks, and process skills that governs AI agent behavior. It describes how a solo operator leverages an AI coding agent as a full team, replacing team coordination with deterministic enforcement.

---

## Why This Exists

This is a framework for a **solo operator leveraging AI as a team**. One person, not an engineering org. The framework replaces team coordination with deterministic enforcement — hooks instead of standups, process skills instead of department handoffs, mandatory dispatch contracts instead of sprint commitments.

## How We Got Here

The framework emerged from comparing two families:

- **Agentic frameworks** (MetaGPT, ChatDev): Pipeline orchestration with typed agent handoffs. Strong on structure, weak on iteration and human judgment. No reprioritization, no "are we building the right thing?"
- **Enterprise frameworks** (Scrum, Agile): Sprint discipline, user stories, retrospectives. Strong on iteration and feedback, weak on automation. Designed for human teams, not AI agents.

Key finding: "They are actually closer than expected on the PIPELINE side." The gap is specifically: no iteration, no human judgment, no prioritization in agentic frameworks. Survey of 6 systems (MetaGPT, ChatDev, claude-flow, everything-claude-code, claude-code-toolkit, Osmani) found: "None of them have a lifecycle orchestrator agent."

**The decision:** Hybrid. Pipeline structure from agentic frameworks (typed handoffs, role matrices). Iteration discipline from Agile (review after every increment, user manages priorities). Enforcement from hooks (deterministic, not prompt-based).

**Architectural constraint:** Inner processes within each role are FUSED compound, not recursive calls to other process skills. Process skills should NOT call each other.

---

## Philosophy

### Core Principles

1. **Soft instructions fail.** Prompt-level rules decay within minutes. Only deterministic hooks enforce reliably. (25% → 90% skill activation with UserPromptSubmit hook.)

2. **Hooks are QA, not oracles.** Hooks verify the process ran — not that the answer is correct. Attempting semantic judgment rubber-stamps everything. Compliance checks = forced transparency so the user can see WHERE things went wrong.

3. **Process skills are training wheels.** A test agent skipped classification and process skills entirely but produced the best output — used 4 lenses, 37 tool calls, cited research. The process codifies behavior for when the model would not do it naturally.

4. **Govern routing, not execution.** Enforce WHAT gets dispatched (main session). Let agents work freely once dispatched. Jules framework independently confirms this pattern.

5. **IMPLIES drives everything.** The IMPLIES field determines not just the TYPE but the dispatch level. Exploration outperforms extraction for routing unpredictable inputs.

6. **Pre-constraints > post-checks.** MetaGPT/ChatDev enforce compliance by structurally preventing wrong actions. PreToolUse hooks are the closest equivalent.

7. **The framework is a neural network.** Four layers of assets (tools, skills, agents, hooks) form interdependent networks. Each asset connects to assets in other layers.

### What We Proved

| Insight | Evidence |
|---------|----------|
| Inline bias is structural, prompt-unfixable | 12.4% reasoning-action mismatch, 78.5% persistence (MASFT, SycEval) |
| Exploration outperforms extraction for routing | 0/18 misclassification vs 2/18 baseline |
| Mandatory exploration backfires | Epistemic check ran hours, never blocked. Performative compliance. |
| Same-model verification degrades | Lu et al. 2025: gains decrease with solver/verifier similarity |
| Ensemble diversity is real for framing | 35% avg overlap across 5 tasks x 3 lenses |
| User intuition outperforms engineered prompts | Exploration question beat 3 research-designed alternatives |

### External Validation

**Gemini peer review:** Praised hook-driven enforcement, role clarity, accuracy mechanisms (IMPLIES/MISSED). Strongest critique: inner compound soft enforcement — if soft instructions fail at the outer layer, they fail inside process skills too.

**Jules framework (github.com/jonathanmalkin/jules):** Same philosophy, same approach, additional patterns adopted (bash safety guard, investigation budget).

---

## Framework Principle

**Big picture → sequence → build → repeat with extended capability.**

Iterative incremental development applied to an agent system. Each iteration:
1. Understand the full picture
2. Sequence the work
3. Build the smallest increment
4. Review — does the plan still make sense?
5. Repeat with new capabilities

**Lifecycle phases (v1 linear):**
```
Research → Analysis → Planning → Build → Review → Iterate
```

---

## The 5 Roles (Nodes)

### Role 1: Research
**Purpose:** Answer open questions from source materials.

**Role matrix:**

| Complexity | Agents |
|-----------|--------|
| Single question, known source | Research analyst OR technical researcher |
| Multiple questions, multiple sources | Research orchestrator → parallel analysts → synthesizer |
| Deep unknowns, many open questions | Autonomous research loop (isolated session) |

### Role 2: Analysis
**Purpose:** Evaluate, diagnose, compare, reason about WHY/HOW.

**Modes:** Evaluation (artifact against rubric), Investigation (tracing causes), Decomposition (breaking compound tasks into sub-tasks), Comparison (parallel lenses).

### Role 3: Planning
**Purpose:** Convert requirements into architecture, sequenced implementation plans, specs.

**Mandatory steps:** architecture review (always), adversarial review (for non-trivial plans).

### Role 4: Build
**Purpose:** Translate specs into working code, workflows, scripts.

**Mandatory steps:** architecture review (always), prompt review (if LLM prompts involved).

### Role 5: QA (Cross-Cutting)
**Purpose:** Challenge assumptions, verify quality, catch errors. Not a standalone node — fires WITHIN other nodes at their review steps.

---

## The Connections (Edges)

### v1 — Linear Pipeline (Current)

```
User → Classifier → ONE role → output → User decides → Classifier → next role
```

### v-infinity — Fully Connected Network (Vision)

```
     Research ↔ Analysis
        |    \  /    |
     Planning ↔ Build
          |       |
           QA (inside each)
```

Every role can activate any other. Classifier fires BETWEEN every role transition. Path emerges from task. Requires circuit breaker for infinite loop prevention.

### Connection Matrix

| From \ To | Research | Analysis | Planning | Build |
|-----------|----------|----------|----------|-------|
| Research | - | "What does this finding mean?" | "How should we investigate?" | N/A |
| Analysis | "What data supports this?" | - | "Is this plan sound?" | "Is this correct?" |
| Planning | "What patterns exist?" | "Is this feasible?" | - | "Build this stage" |
| Build | "How does this API work?" | "Is this correct?" | "What next?" | - |

---

## Enforcement Architecture

### The 4-Layer Hook System

Every layer has an entry gate (pre-constraint) and exit gate (post-check).

| Layer | Entry | Exit |
|-------|-------|------|
| L0: Classifier | UserPromptSubmit (inject reminder) | Stop (verify all fields present) |
| L1: Process Skill | PreToolUse/Skill (validate routing) | Stop (verify dispatch compliance) |
| L2: Agent | SubagentStart (inject guidance) | SubagentStop (structural quality) |
| L3: Tool | PreToolUse/Bash (safety guard) | — |

### The Enforcement Boundary

The fractal problem: enforce the classifier → enforce the process skill → enforce the agent → enforce the tool → ... infinite.

**The practical boundary: enforce handoffs between nodes, not work inside nodes.**

- Classifier skipping fields → hurts (wrong routing) → **enforce**
- Process skill skipping steps → hurts (no review) → **enforce**
- Agent not following its prompt → doesn't hurt much (output checked by next step) → **trust**
- Tool producing wrong output → caught by tests/human → **trust**

### The Repeating Unit

Every process node follows the same structure:

```
SKILL:   Defines the steps + role matrix (what SHOULD happen)
HOOK:    Verifies the steps were followed (what DID happen)
MATRIX:  Determines which agents fire for this specific task complexity
```

---

## The Neural Network Metaphor

Four layers of assets form interdependent networks:

```
HOOKS ----enforce----> SKILLS ----route----> AGENTS ----use----> TOOLS
  |                      |                     |                   |
  |<---fire on events----|<---dispatch---------|<---trigger--------|
```

**This is not metaphor — it is literal architecture.** An asset inventory (CMDB, not yet built) would map every connection.

---

## The Integration Gap

**The enforcement chain:** classify [CHECKED] → dispatch [CHECKED] → integrate [DARK] → respond [DARK]

The system verifies that agents were dispatched. It does NOT verify that their output was USED in the response. The 78.5% persistence finding (SycEval) means this is exactly where inline bias most reliably corrupts output.

**This is "procedural ritualism"** — following the letter of the process while violating its spirit. The hooks ensure the ritual happened, not that it achieved anything.

**Hard ceiling vs soft gap:**
- **Hard ceiling (unfixable):** Hooks cannot enforce semantic compliance. Same-model verification fails (Lu et al. 2025).
- **Soft gap (addressable):** Integration verification (was agent output structurally present in response?), process artifact presence. All structurally checkable.

**The user is the error-correction mechanism.** Hooks force transparency. The user sees WHERE things went wrong.

---

## Deepening Markers

Areas identified but not designed. Each becomes an increment when the simpler version is stable.

- Integration check — verify agent output was structurally used in final response
- Investigation budget — prevent endless research loops
- Conditional enforcement — trigger checks on uncertainty signals, not every response
- Cross-model validation — use different model families to break convergence
- Agent output contracts — define what each agent MUST produce
- Inner process formalization — structured scoping output before agent dispatch
- Asset inventory (CMDB) — map all connections between agents, skills, hooks, tools
- Rules directory — decompose system instructions into individual files
- Agent teams — experimental multi-session coordination for v-infinity vision
