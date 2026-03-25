# Failure Modes and Limits of Autonomous Agent Systems

A comprehensive taxonomy of how autonomous LLM agent systems fail, compiled from Perplexity Deep Research covering academic papers, industry reports, and benchmark evaluations. This document maps failure modes to their triggers, detection methods, and mitigation strategies, with particular attention to which failures are addressable through hook-based governance.

## 1. AutoGPT / BabyAGI-Style Task Loop Failures

Early autonomous frameworks used simple loops -- `plan -> act -> observe -> re-plan` -- with minimal external governance.[^43][^44]

### Recurring Failure Patterns

| Failure | Description | Source |
|---------|-------------|--------|
| **Task decomposition failure** | Agents break problems into sub-tasks that are too vague or misaligned with tools -- flailing instead of progress | MGX 2025 review[^44] |
| **Infinite/unproductive loops** | Termination conditions ill-defined or absent -- repeated similar actions without converging | IBM, MGX[^43][^44] |
| **Context overflow and degradation** | Agents append every observation into single context window -- earlier decisions forgotten/misinterpreted -- "context rot" | MGX[^44] |
| **Hallucination cascading** | Agents hallucinate tasks or resources then act on them -- repeatedly reinforce false assumptions due to lack of validators | IBM[^45][^43] |

IBM's summary: AutoGPT "frequently becomes distracted by non-essential tasks, hallucinates facts, misinterprets data, and fails to complete assignments reliably."[^43]

**Implication:** Use explicit finite-state workflows and hard termination criteria rather than unbounded task loops.

---

## 2. Structured Failure Taxonomy (385 Real-World Faults)

### Characterizing Faults in Agentic AI (2026 arXiv)

Analysis of **385 real-world faults** across multiple agent frameworks (microsoft/autogen, crewAI, deepset haystack, SWE-agent). Taxonomy: **5 architectural fault dimensions, 13 symptom classes, 12 root cause categories**.[^4]

### Dominant Root Causes

| Root cause category | % of faults | Description |
|--------------------|-------------|-------------|
| Dependency and integration failures | ~19.5% | API evolution, schema drift, incompatible abstractions between agent framework and external services |
| Data and type handling failures | ~17.6% | Incorrect parameter schemas, encoding issues, mismatched types in tool calls |

### Recurring Execution Faults

- **Defective termination logic** -- infinite loops, uncontrolled resource consumption, or premature termination
- **Scheduler and task-routing bugs** -- agents don't execute assigned tasks or execute them out of order
- **API misuse and misconfiguration** -- persistent tool failures despite valid agent reasoning[^4]

**Key Insight:** Termination logic, schema/contract enforcement, and integration tests are as important as prompt engineering for reliable autonomous systems.

---

## 3. Execution Hallucinations and Tool-Selection Hallucinations

### Agent Hallucination Survey (2025)

Two hallucination types formalized in agent execution:[^46][^5]

**Execution hallucinations:**
- Agents invoke invalid or non-existent tools
- Mis-parameterize calls
- Assume solvability where none exists

**Tool-selection hallucinations:**
- Agents select wrong tools for a task based on shallow pattern matching

### Danger in Multi-Agent Settings

Execution hallucinations are particularly dangerous in autonomous/multi-agent settings where downstream agents treat previous outputs as ground truth. A fabricated API call from Agent A becomes "fact" for Agent B.

---

## 4. Role and Identity Drift

### 4.1 Agent Drift Framework (2026)

"Agent Drift" introduces a quantitative framework for behavioral degradation in multi-agent LLM systems over extended interactions.[^47]

#### Three Drift Types

| Type | Description |
|------|-------------|
| **Semantic drift** | Deviation from original task or intent |
| **Coordination drift** | Breakdown in consensus or protocol adherence across agents |
| **Behavioral drift** | Emergence of unintended strategies or workflows |

#### Agent Stability Index (ASI)

Composite metric across **12 dimensions**: response consistency, tool usage patterns, reasoning pathway stability, inter-agent agreement, and 8 additional dimensions.[^47]

#### Findings

- Unchecked drift leads to significant reductions in task accuracy
- Increased need for human intervention over time
- Mitigation strategies: episodic memory consolidation, drift-aware routing, adaptive behavioral anchoring[^47]

### 4.2 Identity Drift in Long Conversations

- Larger models experience greater persona drift in long multi-turn conversations[^48]
- Assigning explicit personas does not fully prevent this effect
- Model size correlates with drift magnitude; persona conditioning has weaker influence than model characteristics[^48]

**Implication:** Periodically reset or re-instantiate agents for long-running tasks. Use external state (files, feature lists, task boards) as grounding, not conversational memory alone.

---

## 5. Hallucination Cascading and Error Amplification

### 5.1 Cascading Hallucinations Formalized

- AI agent generates inaccurate information -- reinforced via memory, tool use, or multi-agent interactions -- amplified across multiple decision steps[^49]
- Single hallucinated fact from upstream agent propagates through analyzers, validators, decision agents -- becomes entrenched as "ground truth"[^50][^45]

### 5.2 Error Amplification Numbers

Google/MIT research: **up to 17.2x error amplification** when scaling naive multi-agent systems.[^51]

Key thresholds:
- Diminishing returns once single-agent accuracy exceeds ~45%
- Adding more agents without better coordination can reduce performance[^51]

### 5.3 Multi-Agent Debate: Mixed Results

**Beneficial:** Lin et al. (2024): multi-agent debate for multimodal hallucination mitigation.[^52][^53] Duan & Wang (2024): multiple agents + third-party models reduce hallucinations on arithmetic/reasoning.[^54][^55]

**Harmful:** Without explicit grounding or solvability checks, multiple agents can reinforce incorrect but plausible responses.[^5]

---

## 6. Maximum Autonomous Run Durations

### Long-Horizon Coding Agents

| System | Duration | Conditions | Source |
|--------|----------|-----------|--------|
| Claude Sonnet 4.5 | Up to 30 hours (claimed) | Enforced modular artifacts, persistent memory, planning loops | AI Daily Brief[^56] |
| GPT-5 Codex | 7 hours (claimed) | Benchmark comparison baseline | AI Daily Brief[^56] |
| Production hook-based system | Multi-minute to multi-hour | 95 hooks, evaluator gates, CI-style validation | Crosley blog[^11] |

### Coding Agent Benchmark Performance

| System | SWE-Bench Score | Real-World Score | Notes |
|--------|----------------|-----------------|-------|
| SWE-agent (GPT-4) | 12.29% initial | ~18-20% novel issues | Princeton NLP[^58][^59] |
| SWE-agent (Claude 3.5 Sonnet) | 33.6% | -- | Later configuration[^59][^71] |
| Mini-SWE-agent (~100 lines) | 65-74% Verified | ~18-20% novel | Simple well-structured agent[^60][^61][^62] |
| OpenHands SDK (Claude Sonnet 4.5) | 72% Verified | 67.9% GAIA | Docker isolation, CI-style eval[^63] |
| Devin | 13.86% Verified, 61.9% Lite | 15% (3/20 real tasks) | Answer.AI evaluation[^68][^69][^70] |

### Key Findings on Duration vs Quality

- Even state-of-the-art agents resolve only a minority of novel, uncurated issues without human intervention
- Failures consume disproportionate time and resources[^62][^64]
- Over-long runs: added tokens/time correlate with lower success -- longer trajectories increase error opportunities[^64]
- Real-world gap: curated benchmark scores (65-74%) vs novel issue resolution (~18-20%) reveals massive generalization gap

---

## 7. Safety Concerns and Adversarial Risks

### 7.1 Prompt Injection Attack Success Rates

| Model | Attack type | Failure rate |
|-------|------------|--------------|
| Claude-2 | Perturbation-based injection | Up to 88.1% |
| GPT-4 | Perturbation-based injection | ~32.1% |

[^65]

### 7.2 Constitutional Architecture (Multi-Agent Governance)

RFC on "multi-agent constitutional architecture" reports:[^67]

- **Empirical multi-agent failure rates: 41-86.7%** across 1,642 production traces
- **Up to 70% performance degradation** when adding agents to sequential tasks

Motivates a four-layer governance stack:
1. Foundational principles (system instructions / rules)
2. Behavioral archetypes (skills)
3. Operational protocols (hooks)
4. Amendment mechanisms (governance evolution)

Targets five structural failure modes:
1. Simultaneous action collision
2. Hallucination cascading
3. Context-window commons depletion
4. Split-brain inconsistency
5. Silent degradation under overload[^67]

---

## 8. Detailed Failure Patterns in Production Systems

### Devin (Cognition AI)

- 13.86% SWE-Bench Verified, 61.9% SWE-Bench Lite[^68][^69]
- **Answer.AI evaluation**: only 3 successes out of 20 tasks (~15%) in month-long trial
- Failure pattern: pursued impossible paths instead of recognizing fundamental blockers -- hallucination + lack of solvability awareness + poor termination logic[^70]

### Common Failure Modes Across Systems

| Failure | Description |
|---------|-------------|
| Incorrect patches passing partial tests | Code passes some tests but fails unseen conditions |
| Over-long runs correlating with failure | More tokens/time leads to lower success rate |
| Environment configuration errors | Tool/dependency misconfigurations that agents fail to recognize |
| Specification gap exploitation | Code technically correct but implements wrong behavior |

---

## 9. Master Failure Taxonomy

| Failure Mode | Trigger | Detection | Prevention/Mitigation |
|---|---|---|---|
| **Infinite loops / runaway execution** | Defective termination logic | Iteration counts, elapsed time, token usage tracking | Circuit breakers, forced termination at thresholds[^10][^4] |
| **Tool execution hallucinations** | Fabricated tools or mis-parameterized APIs | Validation against tool registry; schema mismatch detection | PreToolUse validation; failure classification (not blind retry)[^5][^41] |
| **Hallucination cascading** | Downstream agents accept upstream outputs uncritically | Cross-agent traceability, disagreement metrics | Provenance logging; re-grounding against source data[^50][^49][^73] |
| **Role/identity drift** | Long sessions, overgrown conversation history | Tool pattern tracking, periodic drift assessment | Bounded episodes; external state persistence; agent re-instantiation[^47][^48] |
| **Multi-agent coordination deadlocks** | Ambiguous responsibilities, shared state without locks | Stalled task states, idle agents with pending work | Structured task lists + idle detection hooks[^8][^22][^42] |
| **Task decomposition failure** | Vague or misaligned sub-tasks | Stalled progress, repeated similar actions | Structured decomposition pipelines[^44] |
| **Context rot** | Appending all observations into single context window | Inconsistent behavior, forgotten decisions | Bounded context per agent; external state persistence[^44] |
| **Specification gap** | Tests validate code quality but not intent | Technically correct but semantically wrong outputs | Domain-specific evaluator agents; behavioral assertions[^11] |
| **Prompt injection** | Malicious input in agent-processed data | Anomalous tool calls, unexpected behavior patterns | Input sanitization; deterministic command hooks[^65] |
| **Dependency/integration failures** | API evolution, schema drift | Persistent tool failures despite valid reasoning | Integration test suites; schema version checks[^4] |

---

## 10. Risk Assessment for Hook-Governed Architectures

### High Risk (Active Concern)

| Failure | Why it applies | Current mitigation | Gap |
|---------|---------------|-------------------|-----|
| **Hallucination cascading** | Multi-agent systems with chains of specialists | Blind analysis rule (no hypothesis in delegation) | No provenance logging, no disagreement metrics |
| **Role/identity drift** | Long sessions, complex tasks | External state file grounding | No stability monitoring, no automatic resets |
| **Specification gaps** | Build agents validate code quality not intent | Adversarial review agents exist | Not wired into automated gates |
| **Context rot** | Long research tasks, extended sessions | Compaction instructions in system config | No automatic context monitoring |

### Medium Risk

| Failure | Why it applies | Current mitigation | Gap |
|---------|---------------|-------------------|-----|
| **Coordination deadlocks** | Not using agent teams yet | Task classifier routes to single agent | No file-locking, no idle detection |
| **Tool execution hallucinations** | Agents have Bash access, MCP tools | PreToolUse validation hooks | No full tool registry validation |
| **Infinite loops** | Extended research tasks can blow out context | Documented reliability concerns | No circuit breaker config |

### Low Risk (Architecture Prevents)

| Failure | Why low risk | Protection |
|---------|------------|------------|
| **Task decomposition failure** | Task classifier + process skills enforce structure | Classification + domain routing |

---

## References

[^4]: "Characterizing Faults in Agentic AI" (2026) -- arXiv 2603.06847v1
[^5]: "LLM-based Agents Suffer from Hallucinations: A Survey" -- arXiv 2509.18970v2
[^8]: Orchestrate teams of Claude Code sessions -- code.claude.com/docs/en/agent-teams
[^10]: Crosley, "Claude Code Hooks: Why Each of My 95 Hooks Exists" -- blakecrosley.com
[^11]: Crosley, "Your Agent Writes Faster Than You Can Read" -- blakecrosley.com
[^22]: Worktrees: Parallel Agent Isolation -- agentfactory.panaversity.org
[^41]: "Tool-Use Hallucinations in LLM Agents" -- emergentmind.com
[^42]: "GitHub Reveals Why Multi-Agent AI Workflows Fail in Production" -- mexc.com
[^43]: "What is AutoGPT?" -- IBM
[^44]: "The BabyAGI-Style Task Loop" -- MGX
[^45]: "The hidden complexity tax: Problems with generalist multi-agent frameworks" -- corti.ai
[^46]: "LLM-based Agents Suffer from Hallucinations" -- arXiv 2509.18970v1
[^47]: "Agent Drift: Quantifying Behavioral Degradation" -- arXiv 2601.04170
[^48]: "Examining Identity Drift in Conversations of LLM Agents" -- arXiv 2412.00804v2
[^49]: "Governing in the era of agentic AI" -- Cognizant
[^50]: "Hallucinations in Multi-Agent Systems" -- LinkedIn
[^51]: AGI Dreams Podcast (Google/MIT research) -- YouTube
[^52]: Lin et al. (2024), "Interpreting and Mitigating Hallucination in MLLMs" -- arXiv 2407.20505
[^53]: Same -- HTML version
[^54]: "Enhancing Multi-Agent Consensus through Third-Party LLM" -- arXiv 2411.16189
[^55]: "Mitigating reasoning hallucination through Multi-agent Collaborative Filtering" -- ScienceDirect
[^56]: "Claude Sonnet 4.5 Can Code Autonomously for 30 Hours" -- YouTube
[^57]: "Enabling Claude Code to work more autonomously" -- anthropic.com
[^58]: SWE-agent overview -- princeton-nlp.github.io
[^59]: SWE-agent project overview -- swe-agent.com
[^60]: Live-SWE-agent Leaderboard
[^61]: "SWE-EVO: Benchmarking Coding Agents" -- arXiv 2512.18470v1
[^62]: "OpenHands vs SWE-Agent: Best AI Coding Agent 2026" -- localaimaster.com
[^63]: "The OpenHands Software Agent SDK" -- arXiv 2511.03690v1
[^64]: "Swe-Agent" -- giete.ma
[^65]: "Compromising Autonomous LLM Agents Through Malfunction" -- ACL Anthology
[^66]: "OpenHands Review 2026" -- aiagentslist.com
[^67]: synaptiai/multi-agent-constitutional-architecture -- GitHub
[^68]: "Devin AI Statistics: Data Reports 2026" -- WifiTalents
[^69]: "Devin AI or Cursor?" -- trickle.so
[^70]: "Devin struggles with basic tasks" -- theoutpost.ai
[^71]: "SWE-Agent: AI Agents Automatically Codes" -- YouTube
[^73]: "Evaluating autonomous AI agents" -- wandb.ai
