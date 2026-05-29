---
date: 2026-05-25
tags: [project/agent-governance-research, architecture, spec, planning]
status: active
authorship_note: "Authored directly by main-session Opus 2026-05-25 after implementation-plan fabricated a prior attempt (4th documented incident). Adversarial-reviewer critique of the fabricated draft was used as design input; this version addresses the REVISE verdicts rather than papering over them."
---

> Adapted from internal research workspace. Cross-references to vault-internal artifacts have been stripped or genericized.

# Agent-Governance Architecture v2 — Delta Spec

## §0 — Status banner

- **Supersedes (partial):** `Projects/Agent-Governance-Research/archive/2026-03-21-process-network-architecture.md` — for items the 2026-03-21 spec deferred (CMDB) AND items the new investigation revised (ghost-agent definition, compliance schema). Items the 2026-03-21 spec resolved and the investigation did not touch (Working Philosophy principles, primitive set) stay valid as-is.
- **Companion (evidence base):** [[2026-05-25-framework-investigation]] (766 lines). Every architectural claim in this spec traces to a section of that doc; citations inline as `(investigation §X)`.
- **Active for:** the 7 deltas listed in §3. Out-of-scope items are §6.

## §1 — Premise + framing direction

**Decision:** **Option (b) — CLAUDE.md remains authoritative; runtime is enforced to match it via a lint-layer doctrine-drift pass.**

The investigation's §Architectural-Judgment (investigation L620–720) compared three framing options:

- **(a) Derive CLAUDE.md from CMDB** — generate the Agent Registry + Delegation Examples sections from runtime inventory. Pro: drift physically impossible. Con: LLM-derived prose has fabrication risk for non-mechanical sections (Working Philosophy, Communication Style); CLAUDE.md prose Wiktor authored would become read-only-from-Claude.
- **(b) CLAUDE.md authoritative + drift enforcement** — keep CLAUDE.md as human-authored doctrine; add a periodic check that diffs declared bindings vs. live state and surfaces drift findings.
- **(c) Accept drift as natural** — lower CLAUDE.md's authority claim; treat it as aspiration rather than contract.

**Adversarial counter (acknowledged):** the case for (a) is strongest for the Agent Registry section specifically (it's mechanical enumeration, not synthesis). The adversarial-reviewer argued that bundling the whole CLAUDE.md under (b) over-protects the inventory portion. The spec accepts this narrowly: Delta-5 (the doctrine-drift lint pass) treats the Agent Registry block as the primary target — drift findings there carry HIGH severity; drift findings in narrative sections carry LOW severity (informational only).

**Framing claim (one sentence):** CLAUDE.md is authoritative doctrine for behavioral principles, process descriptions, and policy; runtime alignment is enforced for mechanical claims (agent registry, hook event coverage, dispatch contracts) via Delta-5's lint pass.

**System-as-neural-network framing (preservation):** the 2026-03-21 spec's Nodes/Weights/Edges metaphor (task types as nodes; compound ratios as edge weights; agent activations as edges) survives as **mental model only**, not architectural claim. The investigation's compliance data (DC pass rate trending down, not up) falsifies the metaphor's "training improves accuracy" prediction. Drop the metaphor's behavioral prediction; keep the topology mental model.

## §2 — Scope boundary

### IN scope (7 deltas)

- **Delta-1** Bind 2 genuine ghost agents (mcp-developer, mcp-server-architect) via MUST DISPATCH or explicit advisory marker
- **Delta-2** Stop-chain rebalance — investigate and decide for 11-hook Stop event (structural finding)
- **Delta-3** Session-start hidden dependency — surface or eliminate the unregistered side-effect (structural finding)
- **Delta-4** Wiki ingest standard — replace cadence target with input-availability trigger
- **Delta-5** Doctrine-drift enforcement layer (lint Pass-C)
- **Delta-6** Schema-drift baseline replacement for dispatch-compliance-check
- **Delta-7** Deprecated-routing cleanup completion (DISPATCHES.json residuals)

### OUT of scope (deferred with reasoning)

- **CMDB v2 redesign** — current v1 has known parser limitations; redesign requires a separate scoped investigation. The investigation's CMDB miscount (60% false-positive on ghost agents) is a v1 known-bug, not an architecture flaw.
- **Karpathy wiki layer structural rework** — Delta-4 addresses the volume expectation; the 3-layer architecture itself is sound.
- **qmd MCP scope changes** — qmd is working for its 2 collections; no architecture issue surfaced.
- **AGR Phase 2 → Phase 3 transition criteria** — PM's domain; encoding in this spec would conflate delivery governance with system design.
- **DISPATCHES.json second-dispatch-mechanism semantics** — discovered in QA C3 grep; needs focused investigation before being codified. `[NEEDS DISCOVERY]`
- **Full CMDB re-scan with corrected methodology** — adversarial-reviewer flagged that other CMDB-derived claims (33 NO_DISPATCH skills, 40 hook inventory) inherit the strict-grep limitation. Re-scan is required eventually but is a separate workstream from the deltas listed here. Flagged in §6 as a follow-up.

## §3 — The 7 deltas

### Delta-1 — Bind genuine ghost agents

**Empirical finding (investigation §D + QA-C2 + QA-C3):** Two agents are genuine ghosts in the prose-vs-binding sense: `mcp-developer` and `mcp-server-architect`. Both are recommended in CLAUDE.md prose (Specialized agent registry block + Delegation Examples) but appear in zero SKILL.md MUST DISPATCH blocks. QA-C2 confirmed: `process-planning/SKILL.md` has zero matches for either name. The other 3 originally-suspected agents (api-designer, n8n-workflow-architect, workflow-orchestrator) are NOT ghosts — they appear in routing tables + DISPATCHES.json sidecars (QA-C3).

**Options:**
- **BIND (recommended):** add a `MCP servers/clients` domain row in `process-build/SKILL.md` + `process-planning/SKILL.md` routing tables (matching the existing api-designer pattern). MUST DISPATCH binds the design phase to mcp-server-architect, build phase to mcp-developer.
- **MARK ADVISORY:** annotate the CLAUDE.md recommendation line with `(advisory routing — not enforced via MUST DISPATCH)`. Cheaper but preserves the drift pattern.

**Recommendation: BIND.** Matches the existing pattern; closes the drift; reversible via single-commit revert.

**Acceptance criterion:** `grep -r "mcp-developer\|mcp-server-architect" .claude/skills/` returns ≥2 matches for each agent — at least one routing-table context per agent in `process-build/SKILL.md` or `process-planning/SKILL.md`. AND Delta-5's lint Pass-C run after Delta-1 ships reports 0 DOCTRINE_DRIFT findings for these two agents.

### Delta-2 — Stop-chain rebalance

**Empirical finding (investigation §B + QA-C4):** 11 hooks fire on Stop event (10 in settings.local.json + 1 in settings.json). Every other event has 1-3 hooks. Stop is maximally rear-loaded: a session can run non-compliant for many turns before being caught. (QA-C4 verified: `settings.local.json` Stop group contains exactly 10 hook entries.)

**Decision required:** REBALANCE vs. ACCEPT-AND-DOCUMENT.

REBALANCE means: read each of the 11 Stop hook implementations; identify which check a property of the LAST tool call (PostToolUse-compatible) vs. which require full-turn visibility (Stop-only). Move PostToolUse-compatible ones to PostToolUse so violations are caught on the offending tool call, not at response boundary.

ACCEPT-AND-DOCUMENT means: keep the rear-loading; record the architectural reasoning that Stop is the only event with full-turn observability and that mid-turn enforcement risks blocking incomplete work.

**Process for this delta (not a pre-baked recommendation):** dispatch a fresh agent to read all 11 Stop hooks, return a compatibility table (hook name | what it checks | needs full-turn? | PostToolUse-compatible?). Then decide based on the table. If ≥2 hooks are PostToolUse-compatible, REBALANCE for those. If 0 are compatible, ACCEPT-AND-DOCUMENT.

**Acceptance criterion:** either (a) ≥2 hooks moved from Stop to PostToolUse with a settings.local.json diff + the compatibility table recorded in this spec or a sibling artifact, OR (b) the compatibility table shows 0 candidates AND this spec is amended with an ACCEPT-AND-DOCUMENT paragraph in this delta naming each of the 11 hooks + the full-turn-visibility reason per hook.

### Delta-3 — Session-start hidden dependency

**Empirical finding (investigation §B):** `session-start-log.py` is unregistered in both `.claude/settings.json` and `.claude/settings.local.json`, yet `session_start` events reliably appear in `governance-log.jsonl`. The mechanism is a side-effect: `session-start-orientation.py` calls `_daily_aggregate.write_aggregate()` which writes the entry. If `session-start-orientation.py` fails silently (catch-all try-block, no error escalation), the governance-log loses session boundary markers entirely. This is a silent failure mode.

**Options:**
- **PROMOTE (recommended):** register `session-start-log.py` directly in `settings.local.json` SessionStart event. Removes the implicit dependency. The current `session-start-orientation.py` side-effect call becomes redundant and can be removed in a follow-up commit.
- **HARDEN:** keep the side-effect mechanism; add explicit error escalation to `session-start-orientation.py` so a silent failure becomes a loud one.
- **ACCEPT:** document the dependency; do nothing.

**Recommendation: PROMOTE.** Explicit registration > implicit side-effect for governance infrastructure; cheap and reversible.

**Acceptance criterion:** `session-start-log.py` appears in `settings.local.json` SessionStart hook list; subsequent SessionStart event in a fresh session produces a governance-log entry referencing the hook by name (verifiable via `grep "session-start-log" .claude/hooks/governance-log.jsonl`).

### Delta-4 — Wiki ingest standard

**Empirical finding (investigation §E):** 2 INGEST entries in 15 days. The fabricated-prior-attempt's recommendation of "≥1 ingest per 2 weeks" was Goodhart's-Law calibration (adversarial-reviewer flagged this — REVISE verdict). The investigation §E showed the actual gap is **input scarcity**: Inbox/ has been receiving TSB digest files (vault-log type, not research-grade) rather than research clippings. No volume target fixes the input problem.

**Options:**
- **INPUT-AVAILABILITY TRIGGER (recommended):** define the standard as "ingest within 48 hours of a research-grade item being added to Inbox/ or Clippings/." Research-grade = item carries `#research` or `#analysis` tag OR is a Clippings/ file. TSB digests don't trigger ingest because they're operational vault-log type. The existing `inbox-auto-ingest.py` hook handles the trigger; this delta documents the policy.
- **ARCHIVE the Karpathy layer:** rip out wiki-citation-check + lint cadence; demote MOCs to plain notes.
- **KEEP CADENCE TARGET (rejected per adversarial REVISE):** Goodhart's Law.

**Recommendation: INPUT-AVAILABILITY TRIGGER.**

**Acceptance criterion:** CLAUDE.md's Karpathy Operations section gains a one-line policy: "Ingest velocity is input-driven, not calendar-driven. Research-grade items in Inbox/ or Clippings/ trigger ingest within 48 hours; operational vault-log items do not trigger ingest." AND Delta-5's lint Pass-C run after Delta-4 ships does NOT flag wiki velocity as a finding when input availability is low.

### Delta-5 — Doctrine-drift enforcement layer (lint Pass-C)

**Empirical finding (investigation §F + Architectural-Judgment):** The drift pattern that produced the ghost-agent miscount (agents recommended in CLAUDE.md but never bound) is detectable mechanically. The investigation's recommendation: add a periodic check.

**Adversarial counter (acknowledged):** weekly advisory lint produces the same behavioral outcome as no check — Wiktor reads the report, files it, drift continues. The forcing function is missing.

**Resolution: split the pass into two enforcement tiers.**

**Tier A (BLOCKING) — Routing-table validation, PostToolUse hook:** runs on every Edit to `.claude/skills/*/SKILL.md` or `CLAUDE.md`. Checks: every agent named in a routing table OR Delegation Example exists in `.claude/agents/`; every agent name in MUST DISPATCH exists in `.claude/agents/`. Blocks the edit if validation fails. This catches the "rename deprecated agent in registry, leave routing tables referencing the dead name" pattern — the exact failure mode the workflow-orchestrator routing bug exemplified.

**Tier B (ADVISORY) — Doctrine drift, process-lint Pass-C:** runs on the existing weekly lint cadence. Checks: CLAUDE.md Agent Registry section matches `.claude/agents/` Glob; CLAUDE.md Delegation Examples are bound in at least one SKILL.md routing table or DISPATCHES.json sidecar; SKILL.md MUST DISPATCH entries reference agents that exist. Findings written to `Projects/Vault-Maintenance/work/YYYY-MM-DD-doctrine-drift-report.md`.

**Rationale for split:** Tier A is the forcing function the adversarial-reviewer correctly identified as missing — it blocks the edit that introduces drift, not the response that follows. Tier B handles drift forms that aren't tied to an edit event (e.g., an agent file being deleted manually). Together they close the loop.

**Acceptance criterion:** (Tier A) `.claude/hooks/routing-table-validation.py` exists, is registered on PostToolUse for `Edit` matching `.claude/skills/*/SKILL.md` or `CLAUDE.md` paths, and on a synthetic broken-routing edit (e.g., renaming an agent to a nonexistent name) the hook blocks the edit with a `ROUTING_BROKEN` exit-2 message. (Tier B) `process-lint/SKILL.md` has a Pass-C section; first run produces a report file; that report flags any genuine drift that exists at the time of run.

### Delta-6 — Schema-drift baseline replacement (dispatch-compliance-check)

**Empirical finding (investigation §F + bias-audit):** The −23pp DC regression headline (47%→24%) is partly an artifact of `declared`/`missing` field drift mid-window. The current schema is heterogeneous: some block events emit `declared[]`/`missing[]`, others emit `reason`/`task_type`, none emit both. No correlation ID links a block to its later resolution.

**Options:**
- **DUAL-EMIT (recommended):** emit both schemas in parallel for a 2-week transition window. Add a `schema_version` field. New schema includes a `correlation_id` linking block events to their resolution events in subsequent turns. Adversarial counter ("why not cut and recompute?") fails because the new schema needs to be defined+instrumented first; dual-emit window provides validation overlap.
- **CUT:** drop the old schema today; recompute baseline from scratch over the next 2 weeks.

**Recommendation: DUAL-EMIT.** Transition cost is low; validation cost is high without it.

**Acceptance criterion:** `dispatch-compliance-check.py` emits both schemas in every block event during the transition window; `schema_version: "v1"` and `schema_version: "v2"` fields present in respective emissions; `correlation_id` field present in v2 emissions; a `retirement_date: 2026-06-08` constant defined in the script. Compliance re-measurement run after 2026-06-08 uses v2-only.

### Delta-7 — Deprecated-routing cleanup completion

**Empirical finding (this session 11:10):** the primary 2-file routing fix landed in `task-classifier/SKILL.md` L88 and `process-analysis/SKILL.md` L64. QA-C3 grep surfaced 2 residuals: `.claude/skills/process-build/DISPATCHES.json` L35 and `.claude/skills/process-analysis/DISPATCHES.json` L26 both still list `workflow-orchestrator` as an authorized dispatch target.

**Options:**
- **REMOVE (recommended):** delete the `workflow-orchestrator` entries from both DISPATCHES.json files. Mechanical, reversible.
- **KEEP AS ADVISORY:** leave as dormant authorization records (no routing table routes there, so the entries are dead but legal).

**Recommendation: REMOVE.** Dormant authorization = confusion debt; consistency with the SKILL.md routing-table fix.

**State note (2026-05-25):** the SKILL.md portion of this delta already shipped earlier today (task-classifier L88 + process-analysis L64 routing-table edits). Only the DISPATCHES.json residuals remain.

**Acceptance criterion (revised post-architect-review):**
- (Already passing) `grep -r "workflow-orchestrator" .claude/skills/ --include="*.md"` returns 0 results
- (Remaining work) `grep -r "workflow-orchestrator" .claude/skills/ --include="*.json"` returns 0 results

Both must hold for Delta-7 to be marked complete.

## §4 — Sequencing + dependencies

Order of execution:

| Order | Delta | Rationale | Wiktor decision needed? | Reversible? |
|---|---|---|---|---|
| 1 | Delta-7 | Mechanical 2-file edit, no decision, unblocks clean grep baseline | No | Yes (git revert) |
| 2 | Delta-1 | Routing-table edits; depends on Delta-7 so the grep baseline is clean | No | Yes |
| 3 | Delta-3 | Single settings.local.json edit + SessionStart smoke test | No | Yes |
| 4 | Delta-6 | Script edit (dual-emit); Delta-2 measurement needs new schema in place | No | Yes |
| 5 | Delta-5 Tier A | Hook implementation + test; this is the forcing function the framework needs first | No | Yes |
| 6 | Delta-2 | Requires hook-implementation reading first; may escalate to Wiktor if 0 PostToolUse-compatible candidates | Conditional | Yes (rebalance) or doc-only (ACCEPT) |
| 7 | Delta-5 Tier B | process-lint extension; needs to exist before Delta-4's acceptance criterion can be checked | No | Yes |
| 8 | Delta-4 | One-line CLAUDE.md policy edit + verify Delta-5 Tier B doesn't false-flag | No | Yes |

**Parallel-eligible pairs:**
- Delta-1 ∥ Delta-3 ∥ Delta-7 (independent file domains)
- Delta-6 ∥ Delta-5 Tier A (independent scripts)
- Delta-4 ∥ Delta-5 Tier B (independent: CLAUDE.md policy line + process-lint skill extension)

**Critical path:** Delta-7 → Delta-1 → Delta-5 Tier A. Tier A is the forcing function; everything before it is reversible cleanup; everything after is incremental improvement.

## §5 — Enforcement layer details

Already specified in Delta-5 above. Summary of the architectural claim:

- **Authoritativeness preserved:** CLAUDE.md remains human-authored doctrine. The hooks/lint never WRITE to CLAUDE.md; they only flag drift.
- **Forcing function on the edit boundary:** Tier A PostToolUse hook blocks edits that introduce broken routing. This is the inverse of Stop-chain rear-loading (Delta-2) — catch the violation at the tool call that introduces it.
- **Advisory backstop:** Tier B weekly lint catches drift forms that aren't tied to an edit event (manual file deletion, registry.json regen, agent rename via mv).

**Counter to adversarial "Pass-C is theater" verdict:** the theater objection lands against Tier B alone. Tier A is the resolution — it's a hook, not a report file, and it blocks rather than warns.

## §6 — Out-of-scope deferrals

- **Full CMDB re-scan with corrected methodology** — adversarial-reviewer flagged that the 60% ghost-agent false-positive rate may propagate to other CMDB-derived claims (33 NO_DISPATCH skills, 40 hook inventory). Required eventually; not blocking the 7 deltas. Suggested follow-up workstream: build a CMDB v2 that uses both strict grep AND implicit-dispatch detection (routing tables, DISPATCHES.json, Agent-tool prose in skill bodies), then diff v1 vs v2.
- **CMDB v2 design** — see above; separate scoped investigation.
- **Karpathy wiki layer structural rework** — Delta-4 addresses the volume expectation; the architecture is sound.
- **qmd MCP scope changes** — no architecture issue surfaced.
- **AGR Phase 2 → Phase 3 transition criteria** — PM's domain.
- **DISPATCHES.json second-dispatch-mechanism semantics** — discovered in QA-C3; needs focused investigation before being codified. `[NEEDS DISCOVERY: read DISPATCHES.json consumer code to determine whether it drives dispatch or only authorizes it]`
- **Investigation `[GAP]` markers** — separate scoped investigations per gap.

## §7 — Open questions for Wiktor

The mechanical deltas (1, 3, 6, 7, both tiers of 5) ship without further input — they have clear recommendations and reversibility. Decoupled per adversarial REVISE.

**Question 1 (Delta-2 escalation path):** RESOLVED 2026-05-25 — Wiktor: "ok" (unilateral ACCEPT-AND-DOCUMENT authorized). If the compatibility table shows 0 PostToolUse-compatible candidates, the agent records the decision in this spec with the compatibility table as evidence; no separate sign-off needed.

**Question 2 (Delta-4 framing):** RESOLVED 2026-05-25 — owner direction: "since we have wiki, maybe we just need some process to maintain and actively use it?" KEEP + add maintenance/active-use process (NOT archive). Design task added to the project task plan as a new design ticket; the design itself will run through ensemble-protocol per the owner-decisions-go-through-ensemble doctrine.

**Question 3 (Delta-1 binding location):**
The 2 genuine ghosts (mcp-developer, mcp-server-architect) get bound where? Options: (a) `process-build` (MCP work is build-shaped); (b) `process-planning` (MCP design is upstream of build); (c) both. Default if no answer: both (matches the api-designer pattern that the investigation found in process-build + process-analysis).

## Appendix — Investigation section map

For traceability:

| Spec citation | Investigation section | Approx. lines |
|---|---|---|
| §B / hook event coverage | Analysis 1: Hook Event Distribution | L99–198 |
| §D / dispatch contracts | Analysis 2: Agent Binding Gaps | L200–380 |
| §E / wiki velocity | Analysis 3: Wiki Ingest Velocity | L380–500 |
| §F / compliance drift | Analysis 4: Dispatch Compliance Drift | L500–580 |
| Delta-7 / deprecated routing | Analysis 5: Deprecated Routing Cleanup | L580–620 |
| §1 / framing direction | Architectural Judgment: Framing Direction | L620–766 |

---

[[2026-05-25-framework-investigation]]
