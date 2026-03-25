# Claude Code Autonomous Agent Patterns

A survey of production Claude Code autonomous agent architectures, governance patterns, and community frameworks. Based on Perplexity Deep Research (March 2026).

## 1. Hook-Heavy Architecture (Blake Crosley)

Crosley treats Claude Code as **infrastructure**, not an IDE feature. His system: 84-95 hooks, 48 skills, 19 agents, wired into a hook-driven runtime for unattended development workflows. Hooks are attached to **17 lifecycle events**: `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `Stop`, `SubagentStart/Stop`, `PermissionRequest`, each receiving rich JSON context.[^9][^2][^10]

### Hook Type Ratio and Evolution

- **Initial ratio** of judgment to automation hooks: roughly **1:6**.
- After months of autonomous failures, shifted to approximately **4:5** as more validation/gating logic was added in response to incidents.[^10][^9]
- Judgment hooks nearly doubled relative to automation hooks over time — incident-driven evolution, not up-front design.

### Incident-Driven Hook Design

Every hook is justified by a specific failure incident:

| Hook | Incident that triggered it |
|------|---------------------------|
| `git-safety-guardian` | Force-push to `main` during autonomous run |
| Recursion guards | Uncontrolled subagent spawning |
| Blog quality gates | Low-quality content escaped to production |

### Global Configuration Files

Cross-cutting config files encode limits that hooks enforce:
- `recursion-limits.json` — depth limits, spawn budgets
- `circuit-breaker.json` — failure thresholds
- `consensus-profiles.json` — task-specific consensus requirements

Hooks consult these files at runtime rather than hardcoding thresholds.[^10]

### Architecture Layering

Hooks chain into dispatchers, dispatchers into skills, skills into agents, agents into workflows. This creates a **layered control plane** between the LLM and the filesystem. Hooks are the **deterministic control layer**; prompts are not trusted to enforce invariants.[^9]

### Autonomy Duration

- Multi-minute to multi-hour unattended refactors documented.
- Example: **47-file refactor in 9 minutes** — agents refactor, run tests, pass all linting gates before human review.[^11]

### What Breaks (Crosley's Failure Table)

| Failure mode | Trigger | Hook/mechanism | Limitations |
|---|---|---|---|
| Force-push or unsafe git ops | Model issues unsafe git commands | Deterministic `PreToolUse` command hooks that block specific commands | Cannot catch spec-level mistakes; only command-level safety |
| Infinite subagent spawning | Recursive planning/error-recovery loops | Recursion-guard hooks consulting limit configs (depth, spawn budgets, timeouts) | Thresholds are static; may prematurely stop legitimate long workflows |
| Quality regressions that pass tests | Missing domain-specific assertions | Agent-based `Stop` hooks spawn evaluator agents for deeper scenario-specific validations | Still limited by what evaluators test; cannot guarantee coverage of latent behavioral shifts |

### Key Insight: Specification Gaps

A payment retry strategy silently changed from exponential backoff to fixed-interval polling despite tests and linting passing. This was a **specification gap**, not a code-quality failure — tests were correct but didn't test the right thing.[^11]

### Design Principles from Crosley

1. Treat every new autonomous failure as justification to add/refine a hook (incident-driven evolution).
2. Distinguish **safety hooks** (deterministic, command-level) from **quality hooks** (prompt/agent-based).
3. Never use probabilistic hooks for hard safety boundaries.[^12]

---

## 2. Superpowers Plugin (obra/superpowers)

Exposes a large library of skills that enforce mandatory multi-stage workflows (brainstorming, TDD, two-stage review) when using Claude Code.[^14][^15]

### Orchestration Mechanism

- **SessionStart hook**: Loads a skill so every new session automatically enables the framework.[^16]
- **Skills system**: Skills are discovered and activated based on natural-language task descriptions, not explicit tool calls.[^16][^14]
- **Mandatory workflows**: When a relevant skill exists, Claude routes work through predefined phases: `brainstorm -> plan -> implement -> test -> review` instead of ad-hoc coding.[^15][^16]

### Significance

Existence proof that **skill-gated pipelines** wired via `SessionStart` and `UserPromptSubmit` hooks can reliably enforce brainstorm-plan-build-test-review sequences without continuous human steering.[^16]

---

## 3. Builder/Validator Pattern (Dotzlaw)

Formalizes **deterministic agent engineering** — builder/validator pattern enforced by system-level constraints, not prompts.[^13][^6]

### Three Hook Types (Deterministic Spectrum)

| Type | Mechanism | Use for |
|------|-----------|---------|
| **Command hooks** | Pure shell commands with exit codes | Safety boundaries. **Only these should enforce hard safety.** |
| **Prompt hooks** | Single-turn LLM evaluations (yes/no) | Semantic checks where probabilistic evaluation is acceptable |
| **Agent-based hooks** | Spawn full agents with tools for multi-turn verification | Deep review gates, adversarial evaluation |

### Builder/Validator Chaining

**Builder agent:**
- Tool access: full write/edit permissions.
- Hooks: `PostToolUse` hooks on Write/Edit trigger validators after every file modification.
- Failure handling: lint/type errors injected back as context, forcing builder to self-correct before proceeding.

**Validator agent:**
- Tool access: strictly read-only, implemented via `disallowedTools` in agent definitions.[^13][^6]
- Role: code review and verification against acceptance criteria; cannot change files.

**Orchestrator:**
- Sequence: assign task to builder, wait for completion, assign same task to validator.
- If validator reports failure: reassign to builder with validator feedback. Loop.

### Three Mechanistic Consequences

1. **File integrity safety** guaranteed by runtime (validator cannot write), independent of model compliance.
2. **Quality gates** (lint, types) enforced deterministically via command hooks on each write, independent of agent reasoning.
3. **Role specialization** emerges from tool restriction, not prompt instructions — same base model behaves as fundamentally different agents with different tool sets.

---

## 4. Agent Teams (Anthropic First-Party)

Anthropic's first-party mechanism to coordinate multiple Claude Code sessions on a shared project.[^8][^17]

### Team Architecture

- **Team lead**: creates team, spawns teammates, maintains shared task list, synthesizes results.
- **Teammates**: independent Claude Code instances with own context window, tools, skills. Do NOT inherit lead's conversation history but DO load project files and system instructions.
- **Mailbox**: direct inter-agent messaging; teammates can message each other without routing through lead.

### TeammateIdle and TaskCompleted Hooks

Two hook events beyond standard lifecycle hooks:

| Hook | Fires when | Exit code 2 behavior |
|------|-----------|----------------------|
| `TeammateIdle` | Teammate is about to go idle | Send feedback, keep teammate working |
| `TaskCompleted` | Task being marked complete | Block completion, enforce review |

### Worktree Isolation

- **Without worktrees**: agents share single filesystem; safe when agents work on disjoint files.
- **With worktrees**: each teammate in own git worktree; eliminates filesystem interference; orchestration merges branches at checkpoints.

---

## 5. Community Patterns

### Resin.ai Orchestrator
State-machine orchestrator governing SDLC phases with deterministic transitions. 5 domain-specific agents + 4 language skills. Tight integration as Claude Code plugin via MCP server.

### Claude-Flow Framework
Orchestration framework layering hooks on top of Claude Code. Pre-edit, post-edit, session-end hooks. Named agent types: queen, architect, coder, tester, analyst.

### Loki Mode (37 Agents)
37 specialized agents across product, growth, and review domains to autonomously build/launch a startup. Circuit breakers, dead-letter queues, state persistence.

---

## 6. Three Governance Traits of Reliable Autonomous Systems

1. **Deterministic inner loop**: command hooks gate destructive actions; agents cannot bypass via reasoning.
2. **Skill-gated workflows**: skills encode mandatory pipelines; auto-activated via SessionStart/UserPromptSubmit hooks.
3. **Event-driven outer loop**: orchestrators listen to Stop, TeammateIdle, TaskCompleted as state transitions, not natural-language negotiation.

---

## 7. Autonomy Ladder

| Level | Description | Achieved? |
|-------|-------------|-----------|
| L1: Single-task execution | One agent completes one bounded task | Yes |
| L2: Multi-step pipeline | Agent follows brainstorm-plan-build-test-review | Yes |
| L3: Self-correcting loops | Agent detects failures and self-corrects | Yes |
| L4: Multi-agent coordination | Multiple agents work on shared project | Yes |
| L5: Extended autonomy (hours) | Unattended runs lasting hours | Partial (quality degrades) |
| L6: Incident-driven self-improvement | System adds governance in response to failures | Manual only |
| L7: Full autonomy (days+, novel domains) | System operates independently across novel tasks | No |

---

## 8. Gaps: What's Missing for Full Autonomy

1. **Specification-level validation**: All current systems validate code quality but not specification correctness. Tests may be correct but test the wrong thing.
2. **Dynamic threshold adaptation**: Recursion limits, circuit breakers, spawn budgets are all static configs.
3. **Automated governance evolution**: Hook additions are manual after incidents. No system auto-generates governance from failure patterns.
4. **Long-horizon drift mitigation**: No production-grade solution beyond periodic resets.
5. **Cross-agent ground truth**: Downstream agents accept upstream outputs uncritically.
6. **Quantitative reliability data**: No published statistical analysis of long-horizon reliability.
7. **Safety-performance tradeoff**: No controlled work on the frontier between autonomy, safety, and speed.

---

## References

[^1]: Claude Code CLI: The Complete Guide — blakecrosley.com
[^2]: Hooks reference — code.claude.com/docs/en/hooks
[^6]: Building Effective Claude Code Agents — dotzlaw.com
[^8]: Orchestrate teams of Claude Code sessions — code.claude.com/docs/en/agent-teams
[^9]: Claude Code as Infrastructure — blakecrosley.com/blog/claude-code-as-infrastructure
[^10]: Claude Code Hooks: Why Each of My 95 Hooks Exists — blakecrosley.com/blog/claude-code-hooks
[^11]: Your Agent Writes Faster Than You Can Read — blakecrosley.com/blog/cognitive-debt-agents
[^12]: Claude Code Hooks: The Deterministic Control Layer — dotzlaw.com
[^13]: Building Effective Claude Code Agents — dotzlaw.com
[^14]: obra/superpowers — github.com/obra/superpowers
[^15]: This Is The Only Claude Code Plugin You'll EVER Need — YouTube (Better Stack)
[^16]: obra-superpowers/README.md — github.com
[^17]: Claude Code Agent Teams: The Complete Guide 2026 — claudefa.st
