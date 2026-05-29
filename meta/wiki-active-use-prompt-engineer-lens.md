---
date: 2026-05-26
tags: [project/agent-governance-research, planning, spec, wiki, hooks]
status: active
---

# Wiki Active-Use Trigger — Prompt-Engineer Lens

> Adapted from internal research workspace. Cross-references to vault-internal artifacts have been stripped or genericized.

Lens: prompt-engineer

---

## §1 — Trigger Detection Patterns

What prompt shapes carry genuine wiki-retrieval value? Patterns are ordered by specificity.

| Pattern shape | Example prompt | Signal |
|---|---|---|
| Doctrine/policy question | "How do we handle X in the vault?" | asks what the established rule is |
| Capability/constraint question | "Can n8n do Y?" or "Does our setup support Z?" | may have a `reference_*` memory page |
| Architecture or design decision | "What's the right approach for building W?" | architectural findings in wiki |
| n8n-pattern question | "How do I wire pairedItem?", "SplitInBatches output order?" | `reference_n8n_*` pages cover this exactly |
| "Why does X behave like Y?" | "Why does Set node leak passthrough?" | failure-mode docs in wiki |
| Historical precedent | "Did we solve this before?", "What did we find about Z?" | prior research artifacts ingested |
| Framework/skill design | "How should the process-X skill handle Y?" | `agr-kb` collection |
| API / environment behavior | "How does the Confluence API handle…?" | `reference_confluence_*` pages |
| Research synthesis prompt | "What do we know about X?" | direct wiki-query target |
| Task classifier type: Research or Analysis (non-Quick) involving an n8n node, a vault concept, or a framework component | "Analyze why the collector is missing events" | high wiki-hit probability |

**Anti-patterns (do NOT trigger):** "rename X", "move file Y to Z", "fix typo in line N", "delete V", single-field edits, conversational follow-ups ("ok", "proceed", "done"), git commit messages.

---

## §2 — Rule Placement Decision

Three candidate locations, evaluated honestly:

### Option A — CLAUDE.md prose rule (session-load)
**Mechanism:** CLAUDE.md is read at session start and re-injected post-compaction. A prose rule here becomes part of permanent behavioral context.
**Pro:** survives compaction; authoritative; aligned with how existing CRITICAL RULEs work; zero hook infrastructure required.
**Con:** prose rules achieve ~25% compliance (CLAUDE.md Working Philosophy §2 — empirically documented). A rule that says "query qmd before answering" competes with dozens of other rules; under time/token pressure it is skipped. Not detectable per-turn.

### Option B — SessionStart hook injection
**Mechanism:** `session-start.sh` emits `additionalContext` that's injected once at session open.
**Pro:** slightly more salient than buried CLAUDE.md text — arrives as a fresh injection.
**Con:** `additionalContext` is stripped on compaction (confirmed: `reference_compact_hooks_no_additionalcontext.md`). Provides no per-turn enforcement.

### Option C — UserPromptSubmit hook detection (recommended)
**Mechanism:** `user-prompt-submit.py` already reads the incoming prompt text and builds `additionalContext` per turn. Extend it to pattern-match trigger shapes (§1) and inject a targeted one-line reminder only when a trigger fires.
**Pro:** per-turn, pattern-specific, not a global broadcast. Fires silently — Wiktor sees no extra prose. Can log `wiki_query_triggered: true` per turn for compliance measurement. Survives compaction because it re-runs every turn.
**Con:** Python regex in the hook cannot look at full conversation context — only the current prompt text. Will miss some triggers where context matters. Regex maintenance needed as patterns evolve.

**Verdict: CLAUDE.md rule (Option A) as primary doctrine + UserPromptSubmit injection (Option C) as runtime enforcement.** The prose rule gives Claude the "why" and the right scope. The hook gives per-turn salience and logging. Neither alone is sufficient — same pattern as task-classifier enforcement already in the vault.

---

## §3 — Prompt Formulation

### 3a — CLAUDE.md prose rule (add to §Memory Recall section, after qmd paragraph)

```
## CRITICAL RULE: Wiki-First for Doctrine and Pattern Questions

Before synthesizing an answer to any non-Quick question that involves:
  - vault doctrine, framework rules, or CLAUDE.md policy interpretation
  - n8n node behavior, API quirks, or environment constraints
  - architecture decisions, design patterns, or "how do we" questions
  - prior research findings or "what did we find about X"

Call `mcp__qmd__query` FIRST with the relevant terms (collections: "agr-kb" and/or "memory").
Synthesize from wiki results + training context together. Do NOT skip the query and answer from
training context alone when wiki pages likely exist.

Skip the query for: Quick tasks, single-file edits, conversational follow-ups, git operations.
```

### 3b — UserPromptSubmit hook injection (added to `user-prompt-submit.py`)

When the prompt matches trigger patterns, append to `combined`:

```
WIKI QUERY REQUIRED: This prompt matches a doctrine/pattern/research shape. Call mcp__qmd__query (collections: agr-kb, memory) BEFORE answering. Do not answer from training context alone.
```

The injection is suppressed when prompt matches Quick/follow-up patterns (same skip_list logic already present).

---

## §4 — False-Positive Guardrails

The trigger must NOT fire on:

1. **Explicit Quick-class imperatives** — "rename", "move", "delete", "fix typo", "add line", "rerun". Detected by leading imperative + single named target, no uncertainty marker.
2. **Conversational acknowledgements** — the existing `skip_list` in `user-prompt-submit.py` already covers "yes/no/ok/proceed/continue/done/go/go ahead/sure/thanks/confirmed/got it/perfect/great/nice".
3. **Git operations** — "commit", "push", "stage", "git status" shapes.
4. **Follow-up turns on an already-answered question** — prompt is a direct continuation of a previous exchange (often starts with "and", "also", "what about", "can you also"). These rarely benefit from a fresh wiki query.
5. **Subagent prompts** — `user-prompt-submit.py` already sets `classifier_reminder = ""` for subagents (detected via `agent_id`/`agent_type` in payload). Apply the same gate to wiki injection.
6. **Prompts containing explicit wiki results already** — if the user pastes wiki content into the prompt, re-querying is redundant.

Implementation gate in hook: check `is_subagent` (already computed) and `p_lower in skip_list` (already computed) before appending wiki injection.

---

## §5 — Compliance Measurement

### What to measure

**Per-turn signal:** did `mcp__qmd__query` appear in the transcript on a turn where the task type was non-Quick?

### How to detect

Extend `governance-log.py` (Stop hook) to add one field:

```python
# In the tool_use block detection loop, alongside Agent/Skill tracking:
if name in ("mcp__qmd__query", "mcp__qmd__get", "mcp__qmd__multi_get"):
    wiki_queried = True
```

Add to `log_entry`:
```python
"wiki_queried": wiki_queried,  # bool — mcp__qmd__* called this turn
```

**Compliance query** (run against `governance-log.jsonl`):
```python
# Non-Quick turns where wiki_queried is False = compliance gap
non_quick = [e for e in entries if e.get("type") not in ("Quick", None)]
wiki_hit = [e for e in non_quick if e.get("wiki_queried") is True]
rate = len(wiki_hit) / len(non_quick) if non_quick else 0
```

**Target:** wiki consulted on ≥60% of non-Quick turns (baseline unknown — establish first, then set target after 1 week of data).

**Caveat:** governance-log.py only logs turns that contain a task-classifier output. Turns where Claude skips the classifier also skip wiki measurement. This is a pre-existing gap in the log; wiki compliance rate is a lower bound on true behavior.

### Immediate verification (no code change needed)

Grep `governance-log.jsonl` for `mcp__qmd__query` in the same JSON lines as non-Quick types — this works today without schema change, just less structured.

---

## §6 — Integration with Existing Doctrine

**Task-classifier interaction:** The wiki-query rule fires BEFORE synthesis, same tier as classifier invocation. Sequence: classifier identifies type → if non-Quick, wiki query fires → answer synthesized. The classifier's APPROACH field should note "wiki consulted: [page titles]" when relevant — but this is a soft expectation, not enforced.

**MUST DISPATCH interaction:** wiki query is not a substitute for MUST DISPATCH agents. If the question warrants `process-research` or `research-orchestrator`, those still fire. Wiki query is a pre-synthesis check, not a replacement for deep research delegation.

**process-research skill:** That skill has its own research pipeline. When dispatched, it should also call qmd as its first step — this rule applies to the orchestrating Claude, but the research-orchestrator agent running in a subagent context lacks qmd MCP access (`reference_subagents_lack_mcp_access.md`). The wiki-first rule therefore applies to main-session Claude only; subagents get whatever context the main session passes in their prompt.

**Memory Recall (qmd) section in CLAUDE.md:** The existing section already describes qmd as the tool for fetching memory file bodies. The new CRITICAL RULE extends the mandate from "use qmd for memory file bodies" to "use qmd proactively for doctrine + pattern questions." These are complementary, not overlapping.

---

## §7 — Failure Modes

### Too eager
**Symptom:** qmd query fires on Quick tasks, adding 300-500ms latency and token cost with zero benefit.
**Cause:** regex too broad (e.g., matching any question mark).
**Mitigation:** Quick-class imperatives are identifiable by leading verb + single named target + no uncertainty marker. The skip_list in the hook already handles conversational follow-ups. Add imperative-verb prefix check to the hook pattern.

**Symptom:** qmd query fires on every turn regardless of content.
**Cause:** CLAUDE.md rule phrased as blanket mandate instead of conditional.
**Mitigation:** Rule text (§3a above) is explicitly conditional — "Before synthesizing... when... involves...". Not a blanket "always query."

### Too lax
**Symptom:** Claude answers n8n node questions from training context, misses `reference_n8n_paireditem_required_for_new_outputs.md`.
**Cause:** hook pattern doesn't match the specific prompt shape; or Claude ignores the injection.
**Mitigation:** Broaden regex patterns (§1) over time as misses are observed. The CRITICAL RULE in CLAUDE.md is the backstop.

### Hook injection misfires
**Symptom:** wiki injection fires inside a subagent whose prompt happens to contain trigger keywords, causing the subagent to attempt qmd calls it cannot make (no MCP access).
**Cause:** subagent detection in `user-prompt-submit.py` relies on `agent_id`/`agent_type` in the hook payload — if those fields are absent for some subagent types, the gate doesn't fire.
**Mitigation:** Already handled — `is_subagent` check gates all `classifier_reminder` injection; apply same gate to wiki injection block.

### Rule survives compaction but wiki page list grows stale
**Symptom:** Claude queries qmd but the wiki hasn't been ingested recently (the core velocity problem from `2026-05-26-wiki-ingest-velocity-diagnose.md`). Query returns stale or sparse results.
**Mitigation:** This design does not solve ingest velocity — it solves query frequency. A well-queried sparse wiki still surfaces whatever exists. The ingest velocity fix is a separate workstream. These are not blocking each other.

---

## Drop-in implementation checklist

- [ ] Add `## CRITICAL RULE: Wiki-First for Doctrine and Pattern Questions` block to CLAUDE.md (§Memory Recall section, after qmd paragraph). Text verbatim from §3a.
- [ ] Extend `user-prompt-submit.py`: add wiki trigger regex block after the `skip_list` check; emit `WIKI QUERY REQUIRED: ...` as suffix to `combined` when triggered + not subagent + not skip-listed.
- [ ] Extend `governance-log.py`: add `wiki_queried` bool field to `log_entry` by detecting `mcp__qmd__*` tool_use blocks.
- [ ] Establish baseline compliance rate from first week of governance-log data with new field.
