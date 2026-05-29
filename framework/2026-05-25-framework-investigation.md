---
date: 2026-05-25
tags: [project/agent-governance-research, analysis, audit, unclassified-pending]
status: active
---

> Adapted from internal research workspace. Cross-references to vault-internal artifacts have been stripped or genericized.

# Framework Investigation — Unified Canonical Document (2026-05-25)

Two parallel investigations merged here. The mapping lens (empirical e2e, cold-context) produced Sections A, B, C, E, F. The counter-bias lens produced Section D and bias-audits of prior-session work products. Where the two lenses agree, cited once. Where they diverge or one corrects the other, explicit **CORRECTION** callout naming what the prior view claimed vs. what the new evidence shows.

All file-path and line-number citations from both source documents are preserved.

---

## Opening Summary — Top Findings (8 bullets)

1. **Stop-chain overload:** The Stop hook event carries 11 hooks (10 in `settings.local.json` + 1 in `settings.json`). Every other event type has 1–3 hooks. The governance design is maximally rear-loaded — enforcement happens at response boundary, not mid-turn.

2. **`session-start-log.py` hidden dependency:** This file is not registered in either settings file, yet `session_start` events reliably appear in `governance-log.jsonl`. It runs as a side-effect of `session-start-orientation.py` → `_daily_aggregate.py`. If `session-start-orientation.py` fails, governance-log silently loses session boundary markers.

3. **CORRECTION TO PRIOR SESSION — Ghost-agent miscount:** The prior session claimed 5 agents were "ghost-promised" (api-designer, mcp-developer, mcp-server-architect, n8n-workflow-architect, workflow-orchestrator). The counter-bias investigation found only 2 are genuine ghosts (mcp-developer, mcp-server-architect). The other 3 have implicit dispatch paths in skill routing tables or explicit imperative references. The prior session's CMDB strict-grep parser missed domain detection tables.

4. **Deprecated routing live in production:** `workflow-orchestrator` was deprecated for n8n design on 2026-05-05, but `task-classifier/SKILL.md` line 88 and `process-analysis/SKILL.md` line 64 still route n8n tasks to it. Every n8n workflow task processed through these skills is directed to a deprecated agent alias.

5. **DC regression figure is tentative, not confirmed:** The reported −23 pp drop in dispatch-compliance resolution rate (47% → 24%) is confounded by schema drift mid-window. The `declared`/`missing` fields used in the baseline measurement no longer consistently appear on current block events. The caveat is in the re-measurement document but does not adequately revise the headline framing.

6. **Wiki layer structurally complete, operationally inert:** 3 enforcement layers protect a 1-page synthesis corpus (INGEST-001 on 2026-05-10, INGEST-002 on 2026-05-25 = 2 total ingests in 15 days). Ingest velocity is below productive threshold. The enforcement overhead exceeds the protected content by a wide margin.

7. **AGR still in Phase 2 (Build):** The overnight loop (ITER 1–7) closed but the morning architecture re-examination opened new action items. Three proposed actions await Wiktor's GO/NO/REFRAME. PM checkpoint for the morning session was blocked (`pm` declared but not invoked per governance-log). Phase 3 prerequisites are unmet.

8. **One highest-leverage change available:** Fix the `workflow-orchestrator` → `n8n-workflow-architect` routing divergence in two skill files. A 2-file edit that closes a routing bug active since 2026-05-05. Full acceptance criteria in §Architectural-Judgment.

---

## §A — Process Chains End-to-End

*Source: mapping doc §A. No counter-bias corrections apply to this section.*

### A.1 Routing Table

Source: `task-classifier/SKILL.md` lines 222–231.

| TYPE | Process Skill Invoked | Source Line |
|---|---|---|
| Quick | None — inline response | SKILL.md L226 |
| Research | `process-research` | SKILL.md L222 |
| Analysis | `process-analysis` | SKILL.md L223 |
| Content | `process-research` (if needed) → `content-marketer` terminal | SKILL.md L224 |
| Build | `process-build` | SKILL.md L225 |
| Planning | `process-planning` | SKILL.md L226 |
| Compound | `process-analysis` (Decomposition mode) | SKILL.md L227 |

The classifier also defines two **mandatory compounds** that apply to ALL non-Quick primitives (`task-classifier/SKILL.md` lines 66–74):
- QA compound: `process-qa` in MUST DISPATCH
- PM compound: `pm` (pm-orchestrator) in MUST DISPATCH

### A.2 Per-Primitive Process Chain Tables

#### Quick
| Attribute | Value |
|---|---|
| Classifier output | TYPE: Quick, MUST DISPATCH: omitted |
| Process skill | None |
| Agents dispatched | None |
| Hooks at transition | UserPromptSubmit fires (`user-prompt-submit.py` + `user-prompt-state-inject.py`); Stop chain fires but dispatch-compliance skips (no contract found); `classifier-field-check` emits partial event |
| Work artifact path | None — inline response only |

#### Research
| Attribute | Value |
|---|---|
| Classifier output | TYPE: Research, MUST DISPATCH: process-research, process-qa, pm |
| Process skill | `process-research` (`process-research/SKILL.md`) |
| Agents dispatched — MUST DISPATCH | `process-research` owns routing; dispatches one of: `research-analyst` (web/multi-source), `technical-researcher` (code/docs), both in parallel (SKILL.md L76–84), or `research-orchestrator` (4+ sub-questions) |
| Synthesis gate (MANDATORY if 2+ agents) | `research-synthesizer` — SKILL.md L86–95 explicitly states "You MUST dispatch research-synthesizer if Step 3 dispatched 2 or more agents. Skipping synthesis when multiple agents contributed is a process violation caught by the Stop hook." |
| Terminal writer | `report-generator` — SKILL.md L99 |
| Compounds | process-qa (Step 6 quality check), pm (task-classifier mandatory) |
| Work artifact path | `Projects/[Name]/work/YYYY-MM-DD-[topic]-research.md` |
| Advisory routing (prose-only, no MUST DISPATCH binding) | Ralph Loop path (SKILL.md L46–53): Step 3A recommends `architect-loop` skill, but this is a path choice, not a separate MUST DISPATCH item |

#### Analysis
| Attribute | Value |
|---|---|
| Classifier output | TYPE: Analysis, MUST DISPATCH: process-analysis, process-qa, pm |
| Process skill | `process-analysis` (`process-analysis/SKILL.md`) |
| Mode routing | Evaluation / Investigation / Decomposition — SKILL.md L10–16 |
| Agents dispatched — subject-based (SKILL.md L56–65) | `prompt-engineer` (LLM prompts), `architect-reviewer` (code), `debugger` (runtime errors), `api-designer` (API), `data-engineer` (schema), `workflow-orchestrator` (n8n — **see CORRECTION in §D**), `api-security-audit` (security) |
| Synthesis gate (MANDATORY if 2+ agents) | `research-synthesizer` — SKILL.md L77–82 |
| Final writer | `report-generator` (complex multi-agent only) — SKILL.md L88 |
| Advisory routing (prose-only) | "For architecture-level planning, also consider delegating to llm-architect or data-engineer in parallel" (process-planning/SKILL.md L62 — referenced from Analysis Decomposition mode; no MUST DISPATCH binding) |

#### Content
| Attribute | Value |
|---|---|
| Classifier output | TYPE: Content, MUST DISPATCH: process-research (if needed), then content-marketer |
| Process skill | `process-research` for research phase; then `content-marketer` as terminal writer — `task-classifier/SKILL.md` L224 |
| Agents dispatched | content-marketer is the terminal writer; research chain agents if research needed |
| Note | Content is described as "a domain specialization of Build, not a primitive" — `task-classifier/SKILL.md` L199 |

#### Build
| Attribute | Value |
|---|---|
| Classifier output | TYPE: Build, MUST DISPATCH: process-build, architect-reviewer, process-qa, pm |
| Process skill | `process-build` (`process-build/SKILL.md`) |
| Step 1 | Scope block definition |
| Step 2 — MUST DISPATCH | `implementation-plan` agent — SKILL.md L47 |
| Step 3 — MUST DISPATCH | `blueprint-mode` agent — SKILL.md L58 |
| Step 4 — MUST DISPATCH (MANDATORY) | `architect-reviewer` — SKILL.md L76: "You MUST dispatch architect-reviewer. Skipping review is a process violation caught by the Stop hook." Also: `prompt-engineer` if artifact includes LLM prompts — SKILL.md L84 |
| Mandatory compounds | QA (process-qa) + PM (pm) |
| Advisory routing | `debugger` if runtime errors surface in Step 5 — SKILL.md L97 (prose guidance, no MUST DISPATCH) |
| Work artifact path | `Projects/[Name]/work/YYYY-MM-DD-[artifact-name].[ext]` |

**Note on Build step routing:** `process-build/SKILL.md` line 27 (Gotchas) explicitly names `n8n-workflow-architect` as the required agent for n8n workflow design tasks. Source: counter-bias doc §D.1.

#### Planning
| Attribute | Value |
|---|---|
| Classifier output | TYPE: Planning, MUST DISPATCH: process-planning, architect-reviewer, process-qa, pm |
| Process skill | `process-planning` (`process-planning/SKILL.md`) |
| Step 2 — conditional research | Routes through `process-research` skill if research needed (SKILL.md L38–41: "H10 fix: route through process-research, not downstream researchers directly") |
| Step 3 — MUST DISPATCH | `implementation-plan` agent — SKILL.md L53; optionally `llm-architect` or `data-engineer` in parallel (L62, advisory) |
| Step 4 — MUST DISPATCH (MANDATORY) | `architect-reviewer` — SKILL.md L65: "You MUST dispatch architect-reviewer." |
| Step 4 — conditional | `prompt-engineer` if plan involves LLM prompts (L74); `adversarial-reviewer` for high-stakes plans (L76, MUST) |
| Step 5 | Revision loop: `implementation-plan` again if issues found |
| Mandatory compounds | QA (process-qa) + PM (pm) |
| Advisory routing (prose-only, no MUST DISPATCH binding) | "also consider delegating to llm-architect … or data-engineer … in parallel" — SKILL.md L62 |

**Ambiguity note:** process-planning/SKILL.md lines 77–78 mandate `adversarial-reviewer` for "high-stakes plans" but provide no operationalizable threshold for "high-stakes." This creates a soft instruction embedded in a hard-enforcement framework. Hooks cannot resolve it. Source: counter-bias doc §AJ.1.

#### Compound
| Attribute | Value |
|---|---|
| Classifier output | TYPE: Compound, MUST DISPATCH: process-analysis (Decomposition), process-qa, pm |
| Process skill | `process-analysis` in Decomposition mode |
| Agent routing | Decomposition breaks into sub-tasks; each sub-task invokes its own process skill; max 1 level deep — SKILL.md L51 |
| Mandatory compounds | QA (process-qa) + PM (pm) |

### A.3 Advisory Routings Flagged (Prose-Only, No MUST DISPATCH Binding)

Routing recommendations found in skill prose bodies that are NOT enforced by MUST DISPATCH and therefore not verifiable by the dispatch-compliance Stop hook:

1. **`llm-architect` / `data-engineer` for architecture-level Planning** — `process-planning/SKILL.md` L62. No MUST DISPATCH binding.

2. **`debugger` in Build failures** — `process-build/SKILL.md` L97. Advisory, not mandatory.

3. **`prompt-engineer` for plans/builds WITH LLM prompts** — `process-build/SKILL.md` L84 and `process-planning/SKILL.md` L74. Written as mandatory but conditional on the artifact including LLM prompts. Dispatch-compliance hook cannot verify whether LLM prompts were present, so effectively unenforced.

4. **Ralph Loop path (process-research)** — `process-research/SKILL.md` L46–53. Dispatch-compliance hook does not distinguish which path was chosen.

5. **`api-designer`, `mcp-server-architect`, `mcp-developer` in Planning specialist paths** — mentioned in `CLAUDE.md` delegation section and `.claude/registry.json`, but NOT referenced in `process-planning/SKILL.md` MUST DISPATCH or skill body. See §D for revised ghost-agent assessment.

### A.4 Dispatch Concentration — Revised Bucket Analysis

*Source: counter-bias doc §D.4. Corrects the CMDB's "5 of 41" framing.*

| Bucket | Count | Skills |
|---|---|---|
| HAS_MUST_DISPATCH | 5 | process-analysis, process-build, process-planning, process-research, task-classifier |
| HAS_IMPLICIT_DISPATCH | 3 | maintain ("Always spawn an agent" — mandatory prose), process-qa (tool-execution delegation), verification-gated-research (worker-agent loop) |
| META | 1 | task-classifier (also HAS_MUST_DISPATCH; primary role is router) |
| NO_DISPATCH | 33 | All apify-* (12), all n8n-technical (7), architect-loop, ensemble, index, jira-ticket, n8n-review, n8n-reviewer, pm, process-ingest, process-lint, process-pentest, process-query, save, vault-maintain, verify |

**More accurate framing than "5 of 41":** 5 skills enforce delegation via canonical contract; 3 additional skills mandate delegation via prose; 33 skills are inline execution guides.

Note on `maintain/SKILL.md` line 8: "CRITICAL: Delegate the entire maintenance task to an agent." This is mandatory prose dispatch. The CMDB's parser did not capture it because the `MUST DISPATCH:` literal is absent. Source: counter-bias doc §D.3.

---

## §B — Hook Event Coverage Matrix

*Source: mapping doc §B. Stop-chain overload and session-start-log hidden dependency findings are lead items.*

### B.1 Settings Files Active

Two settings files:
- `.claude/settings.json` (project-level) — 5 events wired, 75 lines
- `.claude/settings.local.json` (user-level) — 8 events wired, 451 lines

When both define hooks for the same event, they run in parallel (per CC hook architecture).

### B.2 Event Coverage Table

#### SessionStart

**settings.json** (L12–31):
- `matcher: startup` → `session-start.sh`
- `matcher: compact` → `restore-compact.sh`

**settings.local.json** (L183–213):
- `matcher: startup` → `session-start-orientation.py` (timeout 5s) + `lint-cadence-trigger.py` (timeout 5s)
- `matcher: resume` → `session-start-orientation.py` (timeout 5s) + `lint-cadence-trigger.py` (timeout 5s)

**`session-start-orientation.py` behavior:**
- Input: stdin CC hook payload (`transcript_path`, `session_id`)
- Detects active project via `.claude/active-project.txt` override, then most-recently-modified `Projects/*/STATE.md`, then fallback to "Agent-Governance-Research"
- Reads STATE.md + open task_plan.md items + last 3 decisions
- Emits `hookSpecificOutput.additionalContext` with plain-English orientation summary
- Never blocks

**`lint-cadence-trigger.py` behavior:**
- Reads `.claude/hooks/_state/lint-cadence.json`
- Emits advisory "consider running /process-lint" if >7 days since last run
- Never blocks

**CRITICAL FINDING — `session-start-log.py` hidden dependency:**
`session-start-log.py` is NOT wired to SessionStart in either settings file, yet `session_start` events reliably appear in `governance-log.jsonl` (e.g., `{"ts": "2026-05-25 10:10:32", "event": "session_start", "hook": "session-start-log"}`). The call path: `session-start-orientation.py` (registered) → internal try-block at lines 66–99 calls `_daily_aggregate.write_aggregate()` → which in the session-start-log code path writes the `session_start` event. If `session-start-orientation.py` fails silently, governance-log loses session boundary markers.

Source: `.claude/hooks/session-start-log.py` (full read) + governance-log.jsonl tail.

#### UserPromptSubmit

**settings.local.json** (L215–229):
- `user-prompt-submit.py` — no matcher
- `user-prompt-state-inject.py` (timeout 5s) — no matcher

**`user-prompt-submit.py` behavior:**
- Reads transcript tail (100KB)
- Detects model, computes context fill percentage from token counts
- Emits context bar reminder if task-classifier not yet seen this session
- Enforces task-classifier reminder via `additionalContext`
- Never blocks

**`user-prompt-state-inject.py` behavior (inferred from name + settings registration):**
- Injects STATE.md context into prompt — StateInjection pattern

#### PreToolUse

**settings.local.json** (L230–295) — 6 hooks in order (all Python, all blocking-capable):

| Matcher | Hook | Blocks on |
|---|---|---|
| `Skill` | `skill-routing-check.py` | Incorrect skill routing |
| `Bash` | `bash-safety-guard.py` | Dangerous patterns: rm -rf, force-push, credential exposure, git-hook bypass, --no-verify |
| `Agent` | `agent-dispatch-check.py` | Unknown agent type (warn-downgrade for general-purpose substitution) |
| `Write` | `memory-dedup-check.py` | Duplicate memory file content |
| `Write\|Edit` | `check_forbidden_tokens.py` (in `.claude/scripts/`) | Forbidden token patterns |
| `Write\|Edit\|MultiEdit` | `config-protection.py` (timeout 5s) | Writes to protected config files without authorization |
| `mcp__.*` | `mcp-circuit-breaker.py` (timeout 5s) | MCP call rate limiting |

**Note:** `settings.json` has NO PreToolUse hooks. All PreToolUse is in `settings.local.json`.

**CMDB discrepancy noted by counter-bias lens:** `check_forbidden_tokens.py` appears in the CMDB event map under PreToolUse but is absent from the CMDB's hooks inventory section. The CMDB inventories 40 hooks but 41 are in the event map. Source: counter-bias doc §A (Bias-Audit).

#### PostToolUse

**settings.json** (L43–52):
- `matcher: Bash|Agent|WebFetch|WebSearch|mcp__.*` → `checkpoint.py` — emits 5-minute save reminder via `additionalContext`; never blocks

**settings.local.json** (L297–365) — 8 hooks in order:

| Matcher | Hook | Behavior |
|---|---|---|
| `Skill` | `skill-step-reminder.py` | Reminds Claude to follow skill steps; advisory, non-blocking |
| `Write\|Edit` | `memory-schema-check.py` | Verifies memory file frontmatter schema; warns on violation |
| `Write` | `vault-structure-check.py` (timeout 5s) | Checks vault structural invariants after file writes |
| `Write\|Edit` | `wiki-citation-check.py` (timeout 5s) | Enforces source: field on #wiki-tagged files; blocks `SOURCE_DRIFT` |
| `Write\|Edit` | `inbox-auto-ingest.py` (timeout 5s) | Auto-triggers process-ingest on Inbox/ writes |
| `Write\|Edit` | `tag-variant-check.py` (timeout 5s) | Rejects non-canonical tag variants |
| `Write\|Edit` | `raw-frontmatter-check.py` (timeout 5s) | Enforces R3 frontmatter requirements on raw-layer files |
| `mcp__.*` | `mcp-circuit-breaker-record.py` (timeout 5s) | Records MCP call metrics for circuit-breaker state |

#### Stop — CRITICAL FINDING: 11-hook chain

**settings.json** (L54–62):
- `ralph-stop-hook.ps1` (PowerShell) — ralph-loop plugin Stop hook

**settings.local.json** (L391–435) — 10 hooks in order:

| Hook | Blocks on | Monitoring only |
|---|---|---|
| `classifier-field-check.py` | Missing MUST DISPATCH on non-Quick; incomplete classification block | No |
| `dispatch-compliance-check.py` | Declared items in MUST DISPATCH not actually invoked | No |
| `verifier-gate-check.py` | `verification-gated-research` skill invoked but no verifier agent dispatched post-skill | No |
| `governance-log.py` | Never blocks — logs `turn_summary` event | Yes |
| `process-step-check.py` | QA SCOPE/REPORT blocks missing when process-qa was invoked; checks skill step compliance | No |
| `task-plan-auto-sync.py` (timeout 10s) | Advisory — checks task_plan.md sync status | Yes |
| `dark-zone-check.py` | Never blocks — logs agent utilization ratio | Yes |
| `work-verification-check.py` | Blocks if QA REPORT filed with zero real tool calls; emits WARN for behavioral claims in response | No |
| `proactivity-check.py` | Checks proactivity signals | Yes/No |
| `token-breakdown.py` | Never blocks — logs token cost breakdown | Yes |

**Structural implication:** Stop chain carries 11 hooks (10 local + 1 project) vs. 1 for SubagentStop, 1 for SessionEnd, 1 for PreCompact. Enforcement design is maximally rear-loaded — nearly all governance decisions happen at response boundary, not mid-turn. A session can spend significant time in a non-compliant state before being stopped.

Source: `.claude/settings.json` + `.claude/settings.local.json` (full read).

#### SubagentStart

**settings.json** (L64–73):
- `bias-guard.py` — examines agent prompt for anchored hypotheses; blocks if proposed causes present

**settings.local.json** (L367–380):
- `subagent-governance.py` — writes governance context as `additionalContext`; never blocks. Emits the "AGENT GOVERNANCE: Use multiple perspectives ... Blind analysis rule" text visible in the system-reminder of this session.
- `agent-registry-check.py` — advisory warn-downgrade for general-purpose agent dispatched when specialist exists; does not block

#### SubagentStop

**settings.local.json** (L381–390):
- `subagent-quality-check.py` — structural quality check on agent output (format compliance, minimum content); can block

#### SessionEnd

**settings.local.json** (L438–448):
- `mon-v2-session-end-probe.py` (timeout 5s) — records whether SessionEnd event fires, payload shape, transcript reachability; non-blocking; built in the 2026-05-22 loop iteration 5 as a probe

#### PreCompact

**settings.json** (L32–41):
- `pre-compact.py` (timeout 30s) — collects STATE.md files + task_plan.md In Progress sections + recent transcript context; writes to `~/.claude/pre-compact-recovery.md`; never blocks

**Note:** `settings.local.json` has NO PreCompact entry — only `settings.json` has it.

### B.3 Unwired Hook Analysis

Five hooks present in `.claude/hooks/` but not registered in either settings file:

#### `context-fill-log.py` — INTENTIONAL_STUB
Module docstring lines 1–29: explicit `STATUS: DEFERRED TO ITERATION 4` and `DO NOT REGISTER THIS HOOK. It's a stub — running it does nothing useful.` The `main()` function only reads stdin and returns. References monitoring roadmap v3 Iteration 4 candidates. No implementation.

#### `epistemic-check.py` — DEAD_CODE (deliberately deregistered)
Full implementation present — reads transcript, calls Haiku API with eval prompt, blocks on overconfidence. Deliberately deregistered. Per AGR STATE.md L45: "spec line 57 explicitly classifies it as 'performative compliance, never blocked.'" Additionally, the hook calls `claude -p --model haiku` via subprocess — the `-p` flag bills the Agent SDK credit pool, explicitly classified off-limits (AGR STATE.md L258). Proposed action to archive to `.claude/hooks/_archive/` listed as "autonomously-executable" (STATE.md L48–51) but unexecuted as of this investigation. Not currently causing harm (not registered), but misleading to a developer reading the hooks directory.

Source: `.claude/hooks/epistemic-check.py` (full read) + AGR STATE.md L45, L258.

#### `session-start-log.py` — IMPORT_LIBRARY (runs indirectly)
Full `main()` implementation; writes `session_start` events to governance-log.jsonl. Runs as side-effect of `session-start-orientation.py`. Evidence: `session_start` events appear with `hook: session-start-log` in governance log while the file is not registered. Confirmed in `session-start-log.py` L62–99.

#### `sidecar_loader.py` — IMPORT_LIBRARY
Exports `load_dispatches()`, `mandatory_agent_names()`, `all_allowed_agent_names()`. Imported by `dispatch-compliance-check.py` at lines 61–64. A library module, not a registered hook.

#### `weekly-usage.py` — STANDALONE_SCRIPT
Imports `from claude_monitor.data.reader import load_usage_entries` and `from claude_monitor.core.models import CostMode` — external library dependencies not available in the hook execution environment. Prints formatted weekly usage table to stdout. Cannot function as a hook: no stdin-read, no JSON output, requires `claude_monitor` package not installed in vault Python environment.

### B.4 Hook Coverage Gaps

Events with NO wired hooks:
- **PostCompact** — no hooks registered (referenced in CC Week-19 hook events per `reference_claude_code_hook_events_2026_w19.md` but absent from both settings files)
- **SessionStart `clear` source** — neither settings file registers a hook for `matcher: clear`

**Double-registration latent bug (counter-bias doc §A):** `settings.json` and `settings.local.json` both register `session-start-orientation.py` and `lint-cadence-trigger.py` for SessionStart. These hooks would fire twice per event. The CMDB's deduplicated count of 2 is the correct framing but does not flag the double-registration.

---

## §C — (section removed in public version)

Vault-instance project-state inventory and AGR phase-transition narrative removed from the public version of this investigation. The original section described per-project status snapshots (status, phase, milestone, current activity, transition trigger) and an AGR Phase 2→3 transition assessment. Removed because the content is workspace-specific operational state, not framework theory. Source workspace retains the full version.

---

## §D — Dispatch Contracts vs Prose Contracts

*Source: counter-bias doc §D. Contains the primary CORRECTION TO PRIOR SESSION findings.*

### D.1 — CORRECTION TO PRIOR SESSION: Ghost-Agent Miscount

**Prior-session claim:** api-designer, mcp-developer, mcp-server-architect, n8n-workflow-architect, workflow-orchestrator appear in zero MUST DISPATCH blocks across all 41 skills — all 5 labeled "ghost-promised."

**What the counter-bias investigation found:**

The strict-grep finding (zero `MUST DISPATCH:` literal matches) is correct. But the ghost label is partially wrong for three of the five agents. Implicit dispatch evidence:

| Agent | Finding | Verdict |
|---|---|---|
| `api-designer` | `.claude/skills/task-classifier/SKILL.md` line 95 (Domain Detection table: "API design/behavior → api-designer"); `.claude/skills/process-analysis/SKILL.md` line 62 (Step 2 specialist table). Both are routing tables that direct dispatch to this agent — functionally equivalent to MUST DISPATCH for the relevant domain. | **NOT a ghost** — ADVISORY via domain detection |
| `n8n-workflow-architect` | `.claude/skills/process-build/SKILL.md` line 27; `.claude/skills/n8n-review/skill.md` line 19; `.claude/skills/n8n-reviewer/skill.md` line 19; CLAUDE.md n8n Two-Phase section (5 imperative references). Most heavily referenced agent in the framework. | **NOT a ghost** — the prior session's largest factual error in this section |
| `workflow-orchestrator` | `.claude/skills/task-classifier/SKILL.md` line 88 and `.claude/skills/process-analysis/SKILL.md` line 64 still route to it. **But:** its agent definition marks it DEPRECATED as of 2026-05-05. Two active routing paths point to a self-described deprecated alias. | **STALENESS BUG** — not a ghost; a live routing error |
| `mcp-developer` | No SKILL.md routing table includes it. CLAUDE.md Delegation Examples only (one active recommendation). No skill routing. | **CONFIRMED GHOST** for dispatch purposes |
| `mcp-server-architect` | Same evidence profile as mcp-developer. CLAUDE.md Delegation Examples only. | **CONFIRMED GHOST** for dispatch purposes |

**Root cause of miscount:** The CMDB's strict-grep parser looked for `MUST DISPATCH:` literals only. Domain detection tables and specialist assignment tables do not use this literal. The parser missed all implicit dispatch paths.

### D.2 — CLAUDE.md Agent Recommendations: Category Disambiguation

CLAUDE.md lines 227–248 (Agent Registry + Delegation Examples):

**Agent Registry inventory** (lines 227–237): Inventory lists, not recommendations. Listing an agent in "Specialized:" or "Vault:" is NOT the same as recommending it for a task. The prior session counted these as "hits" without distinguishing enumeration from recommendation.

**Delegation Examples** (lines 241–248): Six concrete if-then statements. Active recommendations:
- "Unfamiliar API → api-designer then blueprint-mode" — active recommendation for api-designer
- "MCP server → mcp-server-architect then mcp-developer" — active recommendation for both mcp agents (one recommendation each, not 2 as prior session claimed by conflating listing with recommending)

**n8n Two-Phase Orchestration section** (lines 347 onward): "dispatch `n8n-workflow-architect`" appears 5 times in prescriptive imperative form. This is the most explicit recommendation in CLAUDE.md. The prior session's "2 CLAUDE.md hits" count for n8n-workflow-architect understated it by a factor of 3–4.

### D.3 — CORRECTION TO PRIOR SESSION: maintain vs. vault-maintain Attribution

**Prior architect-review claim:** "vault-maintain/SKILL.md line 8 says CRITICAL: Delegate the entire maintenance task to an agent."

**Counter-bias finding:**

`maintain/SKILL.md` line 8 DOES read: "CRITICAL: Delegate the entire maintenance task to an agent. File maintenance requires reading every file in the work directory, which trashes the main session context. Always spawn an agent to do the work — never read work files inline." This text is accurate for `maintain`.

`vault-maintain/SKILL.md` line 8 reads: "this skill uses `date`/`type`/`tags`/`status` (vault-note convention) instead of the `name`/`description` skill convention." That is a frontmatter note, not a delegation directive.

`vault-maintain` is an inline execution skill (four phases executed by the main session: tag scan, MOC freshness, link integrity, summary fill). No delegation. The CMDB's "(none)" entry for vault-maintain dispatch is correct.

**Verdict:** The prior architect-review claim attributed `maintain/SKILL.md` line 8 to `vault-maintain/SKILL.md`. The prior QA that reportedly falsified this was correct. The CMDB's "(none)" for vault-maintain is accurate. The architect-review framing was wrong about the file.

### D.4 — Ghost Agent Verdicts and Recommended Actions

**api-designer**
- Evidence: present in two domain detection tables (task-classifier, process-analysis)
- Verdict: **ADVISORY** — domain detection routing is sufficient for its narrow use case. Adding MUST DISPATCH would be overreach; api design tasks are infrequent. The right fix is noting in CLAUDE.md that api-designer is dispatched via domain detection, not as a standalone MUST DISPATCH target.

**mcp-developer**
- Evidence: CLAUDE.md Delegation Examples only. No skill routing table.
- Verdict: **ADVISORY** — MCP server work is rare in this vault (Wiktor's stack is n8n/Python). Adding a MUST DISPATCH binding would require a dedicated process-mcp skill that doesn't exist. Label "advisory for MCP build tasks" in a CLAUDE.md comment.

**mcp-server-architect**
- Same evidence profile as mcp-developer.
- Verdict: **ADVISORY** — bind only if MCP server work becomes a recurring task type.

**n8n-workflow-architect**
- Evidence: 5 imperative CLAUDE.md references + 3 skill routing table entries.
- Verdict: **Already bound via prose contracts and domain detection.** The right fix is replacing `workflow-orchestrator` in the task-classifier domain detection table. The binding already exists functionally; it needs a cleanup, not a new binding.

**workflow-orchestrator**
- Deprecated since 2026-05-05; two active routing paths still name it.
- Verdict: **REMOVE the routing** — update `task-classifier/SKILL.md` domain detection table (line 88) and `process-analysis/SKILL.md` Step 2 specialist table (line 64) to replace `workflow-orchestrator` with `n8n-workflow-architect`. The agent file can remain as alias safety net. This is the highest-leverage architectural change — see §Highest-Leverage.

---

## §E — Memory + Wiki + QMD Layer Flow

*Source: mapping doc §E.*

### E.1 MEMORY.md Status

File: `~/.claude/projects/<vault-project-id>/memory/MEMORY.md`

Per the system context loaded at session start: "MEMORY.md is 334 lines and 46.9KB. Only part of it was loaded." Compressed from 120KB to 64KB in the 2026-05-21 Path D build (AGR STATE.md L138), then further culled to 326 lines / 46KB in the 2026-05-21/22 setup-improvement increment (Vault-Maintenance STATE.md L6). Structure: one-line index entries pointing to topic files. 333 topic files indexed in qmd `memory` collection.

### E.2 Memory-Log JSONL — Finding: Does Not Exist

No `memory-log.jsonl` was found in the memory folder. Memory files are written by AI turns and tracked by git, not by an append-only log. The governance-log.jsonl at `.claude/hooks/governance-log.jsonl` is the operational log; memory operations are not separately journaled.

### E.3 log.md — Ingest/Lint/Extract Operations

File: `Vault/log.md` — 113 lines.

| Operation ID | Date | Type | Status |
|---|---|---|---|
| META-001 | 2026-05-10 21:30 | META | SUCCESS — initialization |
| INGEST-001 | 2026-05-10 22:00 | Ingest | SUCCESS — `karpathy-claudemd-insights.md` |
| EXTRACT-001 | 2026-05-10 22:25 | Extract | SUCCESS — 3 Templates from INGEST-001 |
| LINT-001 | 2026-05-10 23:30 | Lint | SUCCESS — errors=0, warnings=1, resolve_rate=0.857 |
| LINT-002 | 2026-05-11 21:49 | Lint | SUCCESS — errors=2, warnings=24 |
| LINT-003 | 2026-05-21 00:00 | Lint | SUCCESS — errors=6, warnings=25, citations=1.000 |
| INGEST-002 | 2026-05-25 01:30 | Ingest | SUCCESS — `cmdb-vault-setup.md` (bootstrap) |

**Finding:** Only 2 Ingest operations in 15 days. The 15-day gap confirms Gap D from the framework usage audit (`2026-05-24-vault-framework-usage-audit`). See also §Bias-Audit for a root-cause refinement on this gap.

### E.4 Inbox/ Analysis — Is Process-Ingest Keeping Pace?

Inbox/ contains exactly 3 files (all TSB digests):
- `team-signal-digest-2026-05-24.md` — created 2026-05-24 23:23
- `team-signal-brief-2026-W21.md` — created 2026-05-24 23:30
- `team-signal-digest-2026-05-25.md` — created 2026-05-25 10:13

All three are Team-Signal-Brief automated digests — operational artifacts, not research clippings. Per AGR STATE.md L52–53: "Inbox/ currently has TSB digests (vault-log type, not clippings) — would need Wiktor to drop research clippings into Inbox/ OR re-route to Clippings/ existing files."

**Verdict:** Process-ingest is not keeping pace with Inbox/ writes, but the Inbox/ files are not appropriate ingest candidates. The `inbox-auto-ingest.py` hook fires on every Write to Inbox/ but these TSB digests presumably do not meet the ingest conditions (vault-log type, not clipping/article/raw-research type). The ingest gap is a **content problem** (no research clippings being dropped in), not a hook malfunction.

### E.5 Resources/KB/index.md — Wiki Layer State

| Category | Count | Notes |
|---|---|---|
| MOCs (ratified, M4 batch 2026-05-10) | 5 | moc-agent-governance, moc-agent-skill-registry, moc-example-automation, moc-example-product, moc-n8n-patterns |
| MOCs (ratified, Wave-4 doctrine pass 2026-05-11, promoted 2026-05-22) | 6 | moc-active, moc-cross-project, moc-decisions, moc-life, moc-people, moc-research-findings |
| Wiki pages (ratified) | 1 | `karpathy-claudemd-insights.md` — from INGEST-001 |
| Wiki pages (bootstrap, pending Wiktor review) | 1 | `cmdb-vault-setup.md` — from INGEST-002, 2026-05-25 |
| **Total ratified entries** | **12** | 11 MOCs + 1 wiki page — threshold of 10 crossed 2026-05-22 |
| M3 threshold status | CROSSED | Full LLM-authorship mode unlocked as of 2026-05-22 |

### E.6 QMD MCP Status

QMD available in this session (tools `mcp__qmd__status`, `mcp__qmd__query`, `mcp__qmd__get`, `mcp__qmd__multi_get`). Collections: `memory` (333 docs) and `agr-kb` (14 docs). The qmd infrastructure was verified end-to-end in the 2026-05-21 session (AGR STATE.md L117): "confirmed `mcp__qmd__status` → 347 docs / 2 collections and `mcp__qmd__query` returns ranked memory bodies."

---

## §F — Compliance + Observability Spine

*Source: mapping doc §F. The DC regression schema-drift caveat from the counter-bias bias-audit belongs here — the −23 pp number is NOT the headline finding.*

### F.1 Daily Aggregate Files

Location: `.claude/hooks/aggregates/daily/`
Date range: 2026-03-24 through 2026-05-24
Total files: 33 JSON files

Most recent 3:

**2026-05-24.json:**
```
sessions: 4, classifications: 9, quick_count: 8, non_quick_count: 1,
quick_ratio: 0.889, classifier_blocks: 1, qa_fails: 0,
agent_warn_downgrades: 0, agent_dispatches: 16
alerts: ["1 classifier block(s) today"]
```

**2026-05-23.json:**
```
sessions: 12, classifications: 1, quick_count: 1, non_quick_count: 0,
quick_ratio: 1.0, classifier_blocks: 0, qa_fails: 0,
agent_warn_downgrades: 0, agent_dispatches: 2, alerts: []
```

**2026-05-22.json:**
```
sessions: 3, classifications: 12, quick_count: 8, non_quick_count: 4,
quick_ratio: 0.667, classifier_blocks: 1, qa_fails: 0,
agent_warn_downgrades: 0, agent_dispatches: 39
alerts: ["1 classifier block(s) today"]
```

**Fields consistently present:** `date`, `generated_at`, `sessions`, `classifications`, `quick_count`, `non_quick_count`, `quick_ratio`, `classifier_blocks`, `qa_fails`, `agent_warn_downgrades`, `agent_dispatches`, `alerts`

**Fields absent (require direct governance-log.jsonl queries):** dispatch-compliance pass/block counts, PM format compliance counts, turn_summary breakdown, dark-zone severity distribution, token costs.

**`qa_fails: 0` on all 3 sampled dates** — governance-log for 2026-05-25 shows `{"event": "qa_fail_reported", "fail_count": 1}` entries, so the mechanism exists. The field appears to count session-days with failures; those 3 days may genuinely have had 0 QA fails.

### F.2 Governance Log — Recent State

Total entries: 7,367 lines as of 2026-05-25.

Event counts from 2026-05-18 through 2026-05-25 (7 days):

| Event | Count |
|---|---|
| token_breakdown | 272 |
| session_end | 271 |
| agent_dispatched | 217 |
| dark-zone | 94 |
| session_start | 56 |
| block | 47 |
| classification_emitted | 42 |
| turn_summary | 42 |
| dashboard_alert | 36 |
| pass | 32 |
| allow_process_skill_exemption | 18 |
| deny | 17 |
| classifier_field_missing | 9 |
| override | 4 |
| qa_fail_reported | 3 |
| warn | 3 |
| h11_sidecar_fallback_activated | 2 |
| breaker_blocked | 1 |

**Current schema fields (sampled from tail entries):**

`turn_summary`: `ts, schema(2), event, session, type, effort_level, implies, domain, must_dispatch, agents[], skills[], agent_count, skill_count`

`agent_dispatched`: `ts, schema(2), event, session, environment, agent_type, skill_context[], exempted_via_registry, warn_downgrade, outcome`

`block` (dispatch-compliance): `ts, event, hook, session, declared[], missing[], schema(2)` — NOTE: no `reason` or `task_type` field on recent blocks (confirmed from governance-log tail). Schema drift confirmed here.

`classification_emitted`: `ts, schema(2), event, session, environment, type, is_quick, implies, domain, approach, missed, must_dispatch_raw, missing_fields[], complete`

`session_end`: `ts, schema(2), event, hook(work-verification-check), session, environment, turn_count, approx_tokens, duration_sec, heartbeat`

`token_breakdown`: `ts, schema(2), event, hook, session, environment, turn_total_tokens, main_session{input_tokens, output_tokens, cache_read_input_tokens, cache_creation_input_tokens}, main_session_by_model{}, by_subagent[], tool_calls{}, turn_cost_usd, cost_by_model{}, subagent_cost_usd_estimated, price_rates_as_of, task_type`

`dark-zone`: `ts, event, hook, session, agents[], agent_count, citation_count, files_written, ratio, severity, effort_level, schema(2)` — includes `effort_level` added in 2026-05-22 loop iter 7

### F.3 Dispatch-Compliance Hook Analysis

File: `.claude/hooks/dispatch-compliance-check.py`

**What it enforces (SKILL.md-anchored):**
1. Reads last 200KB of transcript
2. Finds last MUST DISPATCH field in a classification block
3. Scans for Skill and Agent tool_use blocks after the contract
4. Blocks if any declared item was not invoked
5. H3 fix: also blocks if MUST DISPATCH is empty on non-Quick tasks
6. H11 fallback: if no classification block found but a process-* skill was invoked, loads DISPATCHES.json sidecar as fallback contract

**Schema drift confirmed:** The dispatch-compliance `block` events in the current 7-day window (47 blocks) carry inconsistent fields depending on the block path:
- Empty MUST DISPATCH on non-Quick: emits `reason: "empty_must_dispatch_on_non_quick"`, `task_type`
- Missing items: emits `declared[]`, `missing[]` (no `reason` field)
- General-purpose substitution warning: emits `warning` field, `task_type`, `declared[]`, `missing[]`

This inconsistency creates schema heterogeneity within a single `event: block` type, complicating downstream analytics.

### F.4 Dark-Zone Hook Analysis

File: `.claude/hooks/dark-zone-check.py`

**What it monitors:**
1. Counts agent dispatches per turn
2. Counts citation patterns in response text (7 regex patterns including `QA REPORT`, `Per [agent]:`, synthesis references)
3. Files written count as citations (proxy for "agent output used")
4. Logs utilization ratio with severity: high (zero citations), medium (<0.5 ratio), low (adequate)
5. **Never blocks** — monitoring only

**Emits:** `dark-zone` event with `agents[]`, `agent_count`, `citation_count`, `files_written`, `ratio`, `severity`, `effort_level`

94 dark-zone events in 7 days = ~13/day. Severity distribution not in daily aggregates — requires direct governance-log queries.

### F.5 DC Resolution Rate — SCHEMA DRIFT CAVEAT IS LOAD-BEARING

**Reported metric:** DC resolution rate fell from 47% (baseline) to 24% (current window). The −23 pp figure appears in the re-measurement document as a headline finding.

**Counter-bias finding (counter-bias doc §C):** This comparison is tentative, not confirmed.

- Baseline measurement used `declared`/`missing` fields on dc-block events to determine "did the correct agent get dispatched after being flagged as missing."
- Current schema: `declared`/`missing` fields are present on some blocks but absent on others; `reason` field added but inconsistently populated.
- The `h11_sidecar_fallback_activated` path may have changed pass-emission semantics mid-window.
- The surviving comparable metric (pass/(block+pass) ratio) measures a fundamentally different thing: "did a block event get followed by a pass event," not "was the missing agent eventually dispatched."

**The re-measurement document correctly identifies this in a caveat section but does not revise the Findings section framing.** The −23 pp figure should be labeled "tentative pending schema verification," not presented as a confirmed regression.

**Metrics that are working and comparable (math verified correct by counter-bias doc §C):**

| Metric | Baseline | Current | Delta | Confidence |
|---|---|---|---|---|
| PM format compliance | 54% | 61% | +7 pp | High (41/67 = 61.2% — verified) |
| Any-dispatch on non-Quick turns | 43% | 58% | +15 pp | High (11/19 = 57.9% — verified) |
| No-classification agent share | 59% | 44% | −15 pp (improved) | High (187/428 = 43.7% — verified) |
| DC resolution rate | 47% | 24% | −23 pp | **LOW — schema drift confound** (15/63 = 23.8% — arithmetic correct; comparison validity uncertain) |

**Unflagged methodological gap (counter-bias doc §C):** The PM compliance denominator is 67 (41 allow + 26 format_blocks). But the `pm_disp` column sums to 116 total dispatches. 49 PM dispatches are unaccounted for — likely `outcome=no_classification` orphans. The 61% figure may be correct within its measured subset (67 dispatches), but that subset represents only 58% (67/116) of all PM dispatches in the window. The re-measurement document acknowledges PM orphans at baseline (65% no_classification) but does not reconcile the 116 vs. 67 discrepancy.

---

## §Bias-Audit Recap

*Source: counter-bias doc §Bias-Audit. Explicit list of corrections to prior-session work products.*

### Prior-session work products examined

1. `2026-05-25-vault-cmdb.yaml` + `.md`
2. `2026-05-24-vault-framework-usage-audit.md`
3. `2026-05-25-must-dispatch-compliance-remeasurement.md`

### CMDB Corrections

- **10-record sample:** 9/10 correct. api-designer description is an accurate compression (not fabrication). workflow-orchestrator DEPRECATED status correctly recorded. Hook event map counts all match live settings (9/9 events verified). No fabricated fields in sampled records.

- **CORRECTION — check_forbidden_tokens.py omission:** Hook appears in the CMDB event map under PreToolUse but is absent from the CMDB's hooks inventory section. 40 hooks inventoried, 41 in the event map. Minor inconsistency; the unlisted hook fires in PreToolUse.

- **CORRECTION — SessionStart double-registration:** `settings.json` and `settings.local.json` both register `session-start-orientation.py` and `lint-cadence-trigger.py`. These would fire twice per SessionStart event. The CMDB's deduplicated count of 2 is correct but does not flag the double-registration as a latent bug.

### Usage Audit Corrections

- **Gap A (must-dispatch compliance unmeasured):** Correctly diagnosed. Evidence real. Severity calibrated correctly.

- **CORRECTION — Gap B (dark-zone recurrence label overstated):** The evidence cites 2026-04-27 (27 dispatches, 0 classifications) and 2026-05-09 (19 dispatches, 0 classifications) as "recurrence" events. The audit itself acknowledges: "these sessions may predate `dark-zone-check.py` deployment — deployment date not confirmed." The "recurrence" label implies ongoing post-deployment failures when the data cannot distinguish pre-deployment from post-deployment events. Mild calibration overstep, not fabrication.

- **Gap C (work-verification-check.py allows Read-only QA):** Correctly diagnosed. Evidence anchored to specific lines (153–174, 162, 173–174). Intentional design per code comment. Accurately scoped.

- **CORRECTION — Gap D (root-cause conflation):** "Operationally stalled" conflates two separate root causes: (a) ingest triggered by inbox writes but Wiktor does not write to Inbox regularly; (b) `process-query` deliberately deferred in CLAUDE.md ("Query (v2, deferred)"). The "stalled" label applies to (a). (b) is intentionally not running — not stalled, designed as deferred. A more accurate statement: ingest velocity is below productive threshold; query is still deferred by design.

- **Gap E (loop queue files outside canonical task_plan.md):** Correctly diagnosed. Best-evidenced gap. Root cause ("autonomous loop output is durably tracked in queue files but does not propagate") accurate and not overstated.

### Re-Measurement Corrections

- **Arithmetic:** All 6 headline metrics verified correct (15/63=24%, 8/17=47%, 41/67=61%, 8/19=42%, 11/19=58%, 187/428=44%). No arithmetic errors.

- **CORRECTION — DC regression framing:** The −23 pp figure is presented as a headline finding. The schema-drift caveat is real and load-bearing but buried in the Caveat section without revising the Findings framing. The comparison is tentative. See §F.5 for full treatment.

- **CORRECTION — PM denominator gap (unflagged by prior session):** 116 total PM dispatches in the window vs. 67 in the compliance denominator. 49 unaccounted dispatches. The 61% figure is correct within its subset but the subset represents 58% of all PM activity. This gap was not flagged in the re-measurement document.

---

## §Architectural-Judgment

*Source: counter-bias doc §Architectural-Judgment. No mapping-lens counterpart — this section is counter-bias lens only.*

### AJ.1 — Is the Framework's Complexity Earning Its Keep?

**Where complexity is earning its keep:**

The 2026-03-21 architecture spec (`archive/2026-03-21-process-network-architecture.md`) documents the empirical evidence base: 25% → 90% skill activation improvement from the UserPromptSubmit hook (spec line 38), and 0/18 misclassification rate for Q4 ("What does this imply?") vs. 2/18 baseline (spec line 57). Real outcomes attributed to specific mechanisms.

The governance-log + daily aggregate pipeline is the vault's only mechanism for detecting behavioral drift over time. The infrastructure's value is visible precisely when it reveals a gap (Gap A shows what happens when measurement stops for 15 days).

**Where complexity is not clearly earning its keep:**

The Karpathy wiki layer has processed one ingest in its entire operational history (INGEST-001, 2026-05-10). Three enforcement layers (skill-level, hook-level, lint-level) protect a 1-page synthesis corpus. Enforcement overhead exceeds protected content by a wide margin. Not wasted investment if ingest volume grows, but at current velocity: substantial design cost with near-zero utilization.

The `adversarial-reviewer` mandate for "high-stakes plans" (process-planning/SKILL.md lines 77–78) provides no operationalizable threshold for "high-stakes." This is a soft instruction embedded in a hard-enforcement framework. The resulting behavior is either always-dispatch (overhead) or never-dispatch (gap).

**Net assessment:** The process/hook layer earns its keep. The wiki layer does not yet. Complexity produces value in routing discipline and drift detection; it does not yet produce value in knowledge management.

### AJ.2 — Did the 2026-03-21 Spec's Predictions Hold?

**CMDB as deferred increment:** The spec named CMDB as "not yet built" (Philosophy §7, line 50). It shipped 2026-05-25 as ITER-3 overnight loop output. Prediction held.

**System-as-neural-network claim (spec line 50):** "Four layers of assets form interdependent networks. A hook enforces a skill which routes to an agent which uses tools." Architecturally accurate for the present system. The task-classifier → process-skill → agent → tool chain is exactly this pattern. Held.

**"Compounds fire dynamically" claim (spec line 46):** Partially held. The Quick fast path and Explicit Imperative path were added empirically. But the dispatch-compliance hook now contradicts this by requiring `process-qa` and `pm` in MUST DISPATCH for all non-Quick regardless of IMPLIES depth. The spec's dynamic-compounds vision has been overridden by categorical mandates. The evolution is defensible (empirical calibration revealed soft-dispatch was insufficient), but the spec's original framing no longer describes the runtime.

**"Process skills should NOT call each other" constraint (spec line 32):** Partially eroded. process-planning now calls process-research via the Skill tool (`SKILL.md` lines 38–50), and process-research was given a mandate to route through itself before dispatching downstream researchers. The spec's "no recursive process-skill calls" constraint has been pragmatically violated to close audit-flagged bypass paths. The violation is functionally justified but is divergence from the spec.

### AJ.3 — CLAUDE.md Drift vs. CMDB: Authoritative Source

**Option (a) — derive CLAUDE.md from CMDB (CMDB authoritative):** This would make CLAUDE.md a generated document. CLAUDE.md is loaded as context and read by the model; it needs to be human-readable and intentional, not auto-generated. This vault has explicit memory of `implementation-plan` and `main-session` fabrication incidents with generated artifacts. CLAUDE.md as a generated document would be harder to reason about when it drifts.

**Option (b) — keep CLAUDE.md as source of truth, add enforcement:** Current nominal approach. Gap: nothing verifies CLAUDE.md's agent list against the agents directory at session start. A session-start hook reading CLAUDE.md's agent list and diffing against `.claude/agents/` would close the drift detection loop with advisory (not block) emissions when out of sync.

**Option (c) — accept drift, lower CLAUDE.md authority:** Not viable. CLAUDE.md's authority comes from being loaded at session start as the behavioral spec. Lowering its authority without a replacement mechanism would reintroduce soft-instruction failures.

**Verdict: (b), operationalized.** CLAUDE.md remains source of truth; a lightweight session-start hook flags drift between CLAUDE.md agent mentions and the `.claude/agents/` directory.

---

## Highest-Leverage Architectural Change

*Verbatim from counter-bias doc §AJ.4.*

**Fix the workflow-orchestrator → n8n-workflow-architect routing divergence in skill tables.**

The workflow-orchestrator agent's own description calls it DEPRECATED for n8n design since 2026-05-05. Yet `task-classifier/SKILL.md` line 88 and `process-analysis/SKILL.md` line 64 still route n8n workflow tasks to it via the domain detection table. Every n8n workflow task that goes through task-classifier or process-analysis gets directed to a deprecated agent. The n8n-workflow-architect (the intended replacement) is the most heavily used agent in the vault for n8n work, but new sessions following the domain detection table will land on the wrong agent.

**Acceptance criterion:** (1) `task-classifier/SKILL.md` Domain Detection table row for "n8n workflows" reads `n8n-workflow-architect (design) / n8n-workflow-builder (implementation)`, not `workflow-orchestrator`. (2) `process-analysis/SKILL.md` Step 2 specialist table row for "n8n workflow logic, branching, error recovery" reads `n8n-workflow-architect`, not `workflow-orchestrator`. (3) `grep -c "workflow-orchestrator" .claude/skills/task-classifier/SKILL.md` and `.claude/skills/process-analysis/SKILL.md` each return 0 after the change. (4) `workflow-orchestrator` remains in the agent file as alias safety net (unchanged). This is a 2-file edit, takes under 5 minutes, and closes a routing bug that has been active since the deprecation date.

---

Hub: agent-governance research repo
