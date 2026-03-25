# Architecture Document

This is the complete architecture reference for the governance framework — a deterministic enforcement layer built around an AI coding agent. It covers philosophy, components, processes, hooks, agents, enforcement layers, and how they connect. The framework replaces traditional team coordination structures (standups, handoffs, sprint reviews) with software enforcement for a solo operator leveraging AI as a full team.

---

## 1. Why This Exists

A solo practitioner using an AI coding agent as a full team needs the equivalent of organizational process — without the organization. The framework replaces team coordination with deterministic enforcement: hooks instead of standups, process skills instead of department handoffs, mandatory dispatch contracts instead of sprint commitments.

**The core problem it solves:** Soft instructions (system configuration rules, prompt-level mandates) decay within minutes in fresh sessions. A field marked MANDATORY in a skill was dropped during an autonomous research session despite the word "MANDATORY" appearing in the instructions. Only hooks enforce reliably. This is not a model quality problem — it is a structural architectural fact, validated by external research (12.4% reasoning-action mismatch, 78.5% persistence — MASFT arXiv:2503.13657, SycEval arXiv:2502.08177).

The framework answer: wrap the unpredictable language model in deterministic infrastructure. Hooks fire regardless of LLM compliance.

---

## 2. Philosophy

Seven principles with evidence grounding each one.

### 2.1 Soft instructions fail

Prompt-level rules decay within minutes in fresh sessions. Measured improvement: 25% to 90% skill activation rate after hook enforcement via a UserPromptSubmit hook.

**Implication:** If a rule is stated twice in any document, it belongs in a hook.

### 2.2 Hooks are QA, not oracles

Hooks verify that the process ran — not that the answer is correct. An epistemic check hook (now disabled) attempted semantic judgment: dispatch a small model to evaluate overconfidence in responses. It never blocked once in hours of operation — it rubber-stamped everything. QA asks "did you follow the process?", not "is the output true?"

**What hooks give you:** A visible trail. Every dispatch decision is exposed. The error correction mechanism is the user, but hooks ensure the data exists to do it. A wrong result from a full pipeline is more informative than a wrong result from a shortcut — the pipeline shows WHERE things went wrong.

### 2.3 Process skills are training wheels

A test agent (T5) skipped classification and all process skills entirely. It produced the best output of five tests: 4 lenses, 37 tool calls, cited research, structured output. The process codifies behavior for when the model would not do it naturally. When context is rich and the prompt is good, the model does it without ceremony.

**Implication:** Process skills govern the main session's routing decisions. They are not required inside subagents. Govern routing, not execution.

### 2.4 Govern routing, not execution

Enforce WHAT gets dispatched (main session). Let agents work freely once dispatched. The main session needs routing discipline. Subagents need execution quality — and they get it from startup governance injection and their own system prompts, not from having process skills layered on top of them.

The Jules framework (github.com/jonathanmalkin/jules) independently confirms this: "Push behavior toward determinism whenever the pattern works."

### 2.5 IMPLIES drives everything

The IMPLIES field ("What does this prompt imply?") determines not just the TYPE but the dispatch level. If IMPLIES reveals inline work is appropriate, MUST DISPATCH can be `none` even for non-trivial types. The depth of the response follows the depth of the implication.

IMPLIES uses exploration mode (not extraction): "What does this mean?" rather than "which category does this fit?" Exploration outperforms extraction for routing unpredictable inputs — the exploration question achieved 0/18 misclassification vs 2/18 for three research-engineered alternatives.

### 2.6 Pre-constraints are stronger than post-checks

PreToolUse hooks block wrong actions before they execute. Stop hooks catch violations after the full response is complete but can only force a retry. Pre-constraints prevent errors; post-checks surface them. Both are needed. Pre-constraints are the stronger mechanism.

Evidence from external frameworks: MetaGPT and ChatDev enforce compliance by structurally preventing wrong actions. PreToolUse hooks are the closest equivalent in AI coding agents.

### 2.7 The framework is a neural network

Four layers of assets (tools, skills, agents, hooks) form interdependent networks. A hook enforces a skill which routes to an agent which uses tools. A tool event triggers a hook which injects context into a skill. Each asset connects to assets in other layers.

This is not metaphor — it is the literal dependency graph.

---

## 3. The 5 Primitive Operations

Every task is a mixture of five irreducible operations. Content is a domain specialization of Build, not a separate primitive.

| # | Primitive | What it does |
|---|-----------|-------------|
| 1 | Research | Gather information from sources |
| 2 | Analysis | Reason about information — evaluate, diagnose, investigate WHY/HOW |
| 3 | Planning | Structure work — design, spec, sequence |
| 4 | Building | Produce artifacts — code, workflows, copy |
| 5 | QA | Verify claims empirically — does it actually work? |

**Mandatory compounds (floor rules enforced by classifier):**

| TYPE | Always-yes compound | Why |
|------|-------------------|-----|
| Build | Analysis | Every build needs post-build quality review |
| Planning | Analysis | Every plan needs challenge before committing |

**The compound detection matrix:** The APPROACH field in every classification forces a yes/no answer on all five primitives. If APPROACH only names one agent for a task that IMPLIES reveals has multiple dimensions, a compound was missed.

**Compounds are fractal:** "Analyze X" might be 60% Analysis + 30% Research + 10% Planning. Zoom into the Research sub-compound and it might itself be Research + Analysis. The pattern recurs dynamically as sub-tasks discover they need other compounds.

Inner processes within each role are fused — Research scoping IS planning+analysis fused inside the skill. Process skills do NOT call other process skills. Inner processes are compound, not recursive.

---

## 4. The Classifier (Activation Function)

The task classifier fires on every user message, enforced by a UserPromptSubmit hook. It is the activation function of the entire system — it determines which role fires, which agents dispatch, and what the enforcement contract looks like for that turn.

### Output format

```
IMPLIES: [one sentence — what does this prompt imply at depth?]
TASK TYPE: [Quick / Research / Analysis / Content / Build / Planning / Compound]
DOMAIN: [specialist domain, or "general" if none]
APPROACH: [Primary path + compound matrix — yes/no on all 5 primitives with agent names]
MISSED: [one sentence — what would I miss by handling it this way?]
MUST DISPATCH: [enforcement contract — comma-separated names or "none"]
MECHANISM: [None / CoVe / External / Ensemble / CoVe+Ensemble]
```

### Key fields

**IMPLIES** — Step 0 of classification. Applied before the type matrix. Forces engagement with meaning before categorizing. Uses exploration mode: "What does this prompt imply?" — not "which bucket does this fit?"

**MUST DISPATCH** — The enforcement contract. A Stop hook reads this field and verifies every listed item was actually invoked. If any declared item is missing, the response is blocked. Setting `none` explicitly allows inline work but still requires the full classification block.

**APPROACH** — Compound detection. Forces yes/no on all five primitives. Names specific agents per compound.

**MISSED** — Self-correction mechanism. After classifying TYPE and deciding APPROACH, answer: "What would I miss by handling it this way?" If the answer reveals a blind spot, the classification should change.

**MECHANISM** — Routes to quality verification: None, CoVe, External, Ensemble, or CoVe+Ensemble. **Current status: dormant.** The classifier outputs it but no process skill reads or routes based on it.

### Routing table (TYPE to process skill)

| TYPE | Process Skill |
|------|--------------|
| Research | process-research |
| Analysis | process-analysis |
| Content | process-build (Content = Build with DOMAIN: content) |
| Build | process-build |
| Planning | process-planning |
| Compound | process-analysis (Decomposition mode) |
| Quick | No skill — respond inline |

---

## 5. The 4-Layer Enforcement Architecture

Every layer has an entry gate (pre-constraint) and exit gate (post-check).

### Layer 0: Classifier

| Gate | Hook Event | What it does |
|------|------------|-------------|
| Entry | UserPromptSubmit | Context bar + mandatory classifier reminder injected on every message. Suppresses when classifier recently seen. Does NOT fire in subagents. |
| Exit | Stop | Reads transcript tail. Checks for IMPLIES, TASK TYPE, APPROACH, MISSED, MUST DISPATCH. Quick only requires IMPLIES + TASK TYPE. Blocks with structured reason if any required field missing. |

### Layer 1: Process Skill

| Gate | Hook Event | What it does |
|------|------------|-------------|
| Entry | PreToolUse (Skill) | Validates that the process skill being invoked matches the routing table for the last TASK TYPE. Non-process skills pass unconditionally. Blocks with reason if wrong process skill invoked. |
| Exit (A) | Stop | Finds last MUST DISPATCH contract. Tracks all Skill and Agent tool calls after the contract. Blocks if any declared item was not invoked. |
| Exit (B) | PostToolUse (Skill) | Fires after a process skill loads. Injects mandatory step reminders for that specific process skill. |

### Layer 2: Agent

| Gate | Hook Event | What it does |
|------|------------|-------------|
| Entry | SubagentStart | Injects behavioral guidance into every subagent context: multiple perspectives, cite evidence, blind analysis rule, flag uncertainty, structure output. |
| Exit | SubagentStop | Three structural checks: (1) empty output < 5 chars, (2) error/refusal < 100 chars matching error keywords, (3) unstructured output > 500 chars with no headers/bullets/tables/code blocks. Blocks with reason. |

### Layer 3: Tool

| Gate | Hook Event | What it does |
|------|------------|-------------|
| Entry | PreToolUse (Bash) | Blocks dangerous patterns: rm -rf on non-temp paths, git force-push, git reset --hard, reading credential files, sudo, chmod 777, kill -9, workflow deletion. |

---

## 6. Process Skills — Detailed Reference

### process-research

**Steps:**
1. RESEARCH SCOPE block — numbered questions, sources, deliverable format
2. Choose path — autonomous research loop (3+ open questions, bias risk) or Direct (1-2 questions)
3. Dispatch agents — research analyst (web/market), technical researcher (code/docs), both in parallel for mixed coverage, research orchestrator for 4+ sub-questions
4. MUST synthesize if 2+ agents — synthesis agent mandatory
5. Report — written to disk
6. Quality check — all questions answered or noted as unanswerable, no contradictions, sources cited

### process-analysis

**Three modes:** Evaluation (artifact against rubric), Investigation (diagnose causes), Decomposition (break Compound into sub-tasks)

**Steps:**
1. ANALYSIS SCOPE block — mode, subject, question/rubric, deliverable
2. Assign specialist from routing table based on subject matter
3. MUST synthesize if 2+ agents
4. Report
5. Quality check

### process-planning

**Steps:**
1. PLANNING SCOPE block — goal, constraints, inputs, deliverable
2. Research if needed (unfamiliar domain, multiple approaches, dependencies)
3. Design — implementation planning agent
4. MUST dispatch architecture reviewer
5. For high-stakes plans: MUST also dispatch adversarial reviewer
6. Revise based on review
7. Quality check

### process-build

**Steps:**
1. BUILD SCOPE block — if no spec/requirements exist, stop and route to Planning first
2. Plan — implementation planning agent
3. Build — builder agent (or domain specialist per DOMAIN)
4. MUST dispatch architecture reviewer; if LLM prompts: MUST also dispatch prompt engineer
5. Quality check — live verification for platform workflows

**Content domain:** Content is Build with DOMAIN: content. The builder agent becomes a content specialist.

### process-qa

**Distinction:** QA is NOT review. Review evaluates quality against criteria. QA tests whether claims are TRUE.

**Steps:**
1. QA SCOPE block — list every verifiable claim with how to test each
2. Choose verification method per claim
3. Execute verification — MUST actually run each test, never reason about whether it would pass
4. QA REPORT — table with claim, method, PASS/FAIL, evidence
5. Escalate failures — report expected vs found. Do NOT fix.

---

## 7. How It All Connects — Full Data Flow

Trace of a non-trivial task through the complete system:

```
User message arrives
  |
  +-> UserPromptSubmit fires
  |     - Context bar rendered (token count)
  |     - Classifier reminder injected
  |
  +-> Agent produces response
  |   - Invokes task-classifier skill
  |
  +-> PreToolUse fires
  |     - Validates skill = task-classifier (non-process skill, passes)
  |
  +-> task-classifier runs
  |     - Step 0: IMPLIES
  |     - Step 1: Type matrix
  |     - Step 1.5: Domain detection
  |     - Step 2: MISSED
  |     - Outputs: IMPLIES, TYPE, DOMAIN, APPROACH, MISSED, MUST DISPATCH
  |
  +-> Agent invokes matching process skill (e.g., process-build)
  |
  +-> PreToolUse fires
  |     - Validates process-build matches TYPE=Build — allow
  |
  +-> PostToolUse fires
  |     - Injects mandatory step reminders for process-build
  |
  +-> Process skill directs agent to dispatch specialists
  |   - implementation-plan dispatched (Planning compound)
  |   - builder agent dispatched (Build primary)
  |   - architecture reviewer dispatched (mandatory Analysis compound)
  |
  +-> Per-agent lifecycle (for each agent):
  |   |
  |   +-> SubagentStart fires
  |   |     - Behavioral guidance injected
  |   |
  |   +-> Agent executes
  |   |   - Has system instructions + startup context
  |   |   - Bash safety guard fires on any Bash tool calls
  |   |
  |   +-> SubagentStop fires
  |         - 3 structural checks on output
  |
  +-> Stop hooks fire (all, in order registered)
        |
        +-> Classifier field check
        |     - Verifies all required fields present — pass
        |
        +-> Dispatch compliance check
              - Verifies all MUST DISPATCH items were invoked — pass
              - If any missing: blocks, agent must retry
  |
  +-> Response delivered to user
```

**The Dark Zone:** The system verifies that agents were dispatched. It does NOT verify that their output was used in the final response. The agent can dispatch (satisfying the hook), receive agent findings, then write its own answer ignoring what it received. This is "procedural ritualism" — following the letter of the process while violating its spirit. No current hook addresses this.

---

## 8. Known Gaps and Deferred Items

### Integration gap (unfixed, structural)

The enforcement chain verifies: classify → dispatch. The dark zone is: dispatch → integrate → respond. The agent can fire all required specialists and then write its own answer ignoring their output. The 78.5% persistence finding (SycEval arXiv:2502.08177) means this is where inline bias most reliably corrupts output.

Structural fix (not yet built): verify agent output was structurally present in the response — a structural presence check, not semantic judgment.

### MECHANISM field dormant

The classifier outputs MECHANISM but nothing reads it. No process skill checks MECHANISM or routes to verification or ensemble skills based on it. Deferred until process skills are end-to-end tested.

### Context rot at ~650K tokens

Observed: at ~650K tokens, IMPLIES quality degrades — outputs become generic philosophical summaries instead of sharp actionable signals ("semantic averaging"). The classifier relies on IMPLIES quality as its activation function. If IMPLIES degrades, routing accuracy degrades, and the entire pipeline produces wrong outputs from a classification that looks correct.

Mitigation: compaction before degradation. Monitor IMPLIES outputs for generic drift as context grows.

### Inner process enforcement

Hooks can enforce handoffs between nodes (classifier → process skill → agent). They cannot enforce steps within a single response. Step reminder hooks partially address this with advisory injections, but these are not blocks. Fully solving inner process enforcement would require hooks inside single responses, which is not possible with current platforms.

---

## 9. External Validation

### Gemini peer review

Reviewed the process network architecture. Findings:

| Critique | Response |
|----------|---------|
| Transcript scraping brittleness (hooks parse free text) | Partly addressed — hooks match structured tool-use blocks. The MUST DISPATCH text field is the one fragile point. |
| v-infinity loops (agents calling other agents recursively) | Valid but irrelevant for v1 — linear pipeline, user manages transitions. |
| Inner compound soft enforcement | Strongest critique. Addressed by dispatch compliance check. Fully solving it requires hooks inside single responses — not possible. |
| QA grading own homework | Mostly addressed — subagents are isolated contexts. Blind analysis rule enforced via startup injection. |

### Jules framework (github.com/jonathanmalkin/jules)

Independent validation of the same architecture:
- Same philosophy: "Push behavior toward determinism whenever the pattern works"
- Same approach: hooks enforce, skills guide, agents work freely within tool constraints
- Additional patterns adopted: bash safety guard, investigation budget (deferred)

### Fresh session tests

Round 1 (Opus): 3/5 agents followed framework correctly.
Round 2 (Sonnet): 5/5 agents followed framework correctly.

T5 test finding: agent that skipped all process ceremony produced the best output. Confirms "govern routing, not execution" and "process skills are training wheels."

---

## 10. Fundamental Insights

### 1. Exploration vs extraction prompting

Two distinct prompting modes. Extraction asks "give me X" — competes with accumulated context. Exploration asks "what does this imply?" — leverages accumulated context. Exploration outperforms extraction for routing unpredictable inputs.

**Evidence:** The exploration question achieved 0/18 misclassification vs 2/18 baseline. Effect predicted to increase at high context. Gemini confirmed novelty relative to adjacent literature (Contextual Inertia, DiSRouter, Thought Propagation).

### 2. Inline bias is structural and prompt-unfixable

LLMs defaulting to inline text is the autoregressive baseline. 12.4% reasoning-action mismatch (correctly reasons to delegate, then answers inline). 78.5% persistence once inline mode starts. Adding more rules makes it worse.

**What works:** Hooks (25% → 90% activation), tool restriction, blind analysis, condition-masking questions (+6.8-14.1 accuracy), rejection-permission framing (+60%). What does not work: anti-sycophancy prompts, more rules, self-correction, multi-agent debate.

### 3. CoVe spectrum (8 levels)

Quality verification is not binary. 8 empirically grounded levels from actively harmful ("think again" — Huang et al. ICLR 2024, -37.7 points) to architecturally robust (blind ensemble). Same-model verification degrades with repetition (Lu et al. 2025 — cross-family >> self-verification).

### 4. Discovery over confidence

LLMs default to "I know the answer" when the right mode for complex/novel tasks is "I don't know, let's find out." Highest quality comes from matching the user's exploration energy rather than projecting confidence.

### 5. Recursive execution pattern

Every level of the system follows the same 6-step cognitive pattern: Classify → Decompose → Delegate → Work → QA → Report. The main session does it formally (classifier + hooks). Agents do it informally (natural reasoning). Projects do it over weeks (PM lifecycle phases). Same pattern, different timescale and formality.

**Important constraint:** Process skills do NOT call each other (not recursive in the software sense). The pattern recurs cognitively at every depth, but process skill execution is compound (fused), not recursive (chained).

---

## 11. Design Decisions Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-03-22 | All 4 layers fully gated (9 active hooks) | Entry+exit at every layer. Pre-constraints prevent errors; post-checks expose them. Both needed. |
| 2026-03-22 | Agent Override removed from all process skills | Redundant with compound dispatch contract. Redundancy created confusion about which mechanism was authoritative. |
| 2026-03-22 | process-qa built as 5th primitive | QA compound in APPROACH field had no corresponding process skill. Built to close the primitive set. |
| 2026-03-22 | PM orchestrator sits ABOVE classifier | PM lifecycle operates at project timescale (weeks). Classifier operates at task timescale (turns). Separate concerns. |
| 2026-03-22 | Bash safety guard built as L3 entry gate | Blocks 13 patterns. Jules framework had this; adopted. 10/10 test cases pass. |
| 2026-03-22 | SubagentStop quality gate built | 3 structural checks. Prevents empty/error/unstructured agent outputs from propagating. |
| 2026-03-21 | MUST DISPATCH field added | Enforcement contract. Allows compliance check to verify specific items invoked, not just that SOME agent was used. |
| 2026-03-21 | Compound detection (5-primitive yes/no matrix in APPROACH) | Forces explicit acknowledgment of all compounds per turn. |
| 2026-03-21 | Mandatory compounds (Build→Analysis, Planning→Analysis) | Floor rules. Classifier MUST mark these regardless of what the task looks like. |
| 2026-03-20 | IMPLIES field added as Step 0 | Exploration before extraction. Reduced misclassification from 2/18 to 0/18. |
| 2026-03-20 | Quick burden-of-proof inverted | Default was Quick if uncertain. Changed to: Quick must be actively proven. Cost of over-investigating is low; cost of under-investigating is high. |
| 2026-03-19 | Reconsideration = ensemble, not self-check | Socratic self-questioning produces performative compliance. Huang et al. ICLR 2024: "are you sure?" → -37.7 points. Blind architectural separation is the only surviving reconsideration mechanism. |
| 2026-03-19 | One-round CoVe limit | Lu et al. 2025: same-model verification degrades with repetition. |
| 2026-03-18 | Hooks as governance architecture | Soft instructions have 25% activation rate. Hooks brought it to 90%. Hooks are non-optional. |

---

## 12. Future Improvements

### From Gemini Review

| Item | Description |
|------|-------------|
| Dark Zone / Terminal Synthesizer | Main session can dispatch agents then ignore their output. Fix: structural presence check. |
| MCP Classification Tool | Classifier fields parsed via regex. Structured JSON tool call would be more reliable. |
| MECHANISM Field | Classifier outputs MECHANISM but nothing reads it. Either wire to routing or strip. |
| Context Rot Monitoring | IMPLIES degrades at ~650K tokens. Monitor for generic drift. |

### From Jules Comparison

| Item | Description |
|------|-------------|
| Rules directory | Decompose system instructions into individual rule files. Modular, better context management. |
| Bash output compression | PreToolUse hook reducing verbose output to save context tokens. |
| Governance logging | Session-level observability. Aggregate view of what happened across a session. |
