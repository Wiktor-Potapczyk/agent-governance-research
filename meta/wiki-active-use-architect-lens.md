---
date: 2026-05-26
tags: [project/agent-governance-research, planning, spec, wiki]
status: active
---

# Wiki Active-Use Process — Architect Design

> Adapted from internal research workspace. Cross-references to vault-internal artifacts have been stripped or genericized.

Lens: architect-reviewer

---

## §1 — Process Diagram

```
SESSION START
     │
     ▼
[session-start-orientation.py]
 → appends WIKI STATUS BLOCK to additionalContext
   (stale page count, last ingest age, backlog count)
     │
     ▼
USER TURN RECEIVED
     │
     ▼
[user-prompt-submit.py — classification gate]
 CLASSIFY prompt intent:
   ├── Doctrine question?  ─────────────────────────────────┐
   ├── Architecture decision? ──────────────────────────────┤
   ├── Research synthesis request? ─────────────────────────┤
   └── (none of the above) → skip wiki query               │
                                                            ▼
                                             WIKI QUERY (mcp__qmd__query)
                                              collection: "agr-kb"
                                              sub-queries: lex + vec
                                              intent: prompt text
                                                            │
                                                            ▼
                                             ANSWER WITH CITATIONS
                                              surface hit pages + snippets
                                              pre-load into main-session context
                                                            │
                                                            ▼
                                             ANSWER DELIVERED
                                              ├── wiki was sufficient → done
                                              └── wiki was insufficient
                                                    │
                                                    ▼
                                             INGEST-BACK? (optional)
                                              if research produced new synthesis
                                              → dispatch process-ingest on
                                                work/ artifact as raw source
                                                stores new wiki page with SHA
                                                citation; compounds wiki value

MAINTENANCE CADENCE (parallel, asynchronous)
     │
     ├── [lint-cadence-trigger.py] at SessionStart
     │    → surfaces reminder when last process-lint > 7 days
     │
     ├── [inbox-auto-ingest.py] (extended to cover Clippings/)
     │    → PostToolUse Write|Edit on Inbox/ OR Clippings/ paths
     │    → dispatches process-ingest when qualifying tags present
     │
     └── STALE PAGE SWEEP (weekly, via process-lint)
          → flags pages with last_modified > 30 days + low score
          → produces STALE / ORPHAN_CITATION / WEAK_CITATION report
          → Wiktor approves archive or refresh
```

---

## §2 — Trigger Conditions

Wiki query should auto-fire on CLAUDE main session turns that match ANY of:

**Category A — Doctrine questions**
Prompt contains phrases targeting CLAUDE.md content or framework rules:
- "should I", "is it correct to", "what does the framework say about", "which pattern applies",
  "which approach", "how does X work in this vault", "best practice for"

**Category B — Architecture decisions**
Prompt targets system design with implications across components:
- keywords: "design", "architect", "refactor", "component", "dependency", "boundary",
  "schema", "hook", "skill routing", "agent dispatch", "workflow design", "n8n"
- OR task-classifier emits primary=Planning or primary=Analysis with compound Architecture

**Category C — Research synthesis**
- task-classifier emits primary=Research, OR prompt includes "research", "synthesize",
  "what do we know about", "find patterns in", "prior art"
- Raw-source items newly ingested since last session (detected via log.md delta read)

**NOT a trigger (reduces noise):**
- Quick-class tasks (single-field edits, move/rename, typo fix)
- Conversational one-liners (yes/no/ok/proceed — already filtered in user-prompt-submit.py)
- Prompts with no doctrinal or architectural surface

**Classification method:** regex scan on the prompt text inside `user-prompt-submit.py`
additionalContext injection, OR a dedicated `wiki-query-trigger.py` PreToolUse hook
(see §3 for the placement decision).

---

## §3 — Active-Use Mechanism

### Where does the trigger fire?

Two candidate placements; this design recommends **Option B** for latency and simplicity:

**Option A — UserPromptSubmit hook injection (currently used by user-prompt-submit.py)**
- Pro: fires before any Claude turn; additionalContext arrives with the prompt
- Con: qmd MCP is not callable from a Python hook; the hook can only inject a *reminder*
  ("this prompt is wiki-eligible — call qmd before answering"), not the actual result
- Verdict: works as a prompt-shaping signal but cannot pre-load wiki results

**Option B — CLAUDE.md policy (main-session inline, no hook)**
- Mechanism: add a rule to CLAUDE.md §Memory Recall (qmd MCP) section that governs
  when main-session Claude calls `mcp__qmd__query` before answering
- The rule fires as Claude reads the prompt and reaches the response step
- Pro: Claude has MCP access; can call qmd directly and incorporate results into the answer
- Con: policy compliance (~25% per CLAUDE.md Working Philosophy #2); needs an enforcement
  layer to reach ~90%

**Option C — Hybrid (recommended):**
1. `user-prompt-submit.py` — add prompt-category detection; when Category A/B/C matched,
   inject a high-priority additionalContext line:
   `[WIKI GATE] This turn is wiki-eligible. Call mcp__qmd__query (collection: agr-kb) before answering. Required fields: intent, searches=[lex+vec sub-queries].`
2. CLAUDE.md §Memory Recall — add binding: "When a [WIKI GATE] signal is present in
   additionalContext, the wiki query is mandatory, not optional."
3. `governance-log.py` (PostToolUse) — log `wiki_query_fired: true/false` per turn to
   `.claude/hooks/aggregates/wiki-query-log.jsonl`; this feeds the measurement axis (§5)

This three-layer binding mirrors the ~90%-compliance hook model already proven in the vault.

### Ingest-back path

After any non-Quick research session that produces a `Projects/*/work/` artifact:
- Main session checks whether the artifact qualifies as an ingest source
  (contains `#research` or `#analysis` in tags, OR is a synthesis/findings file)
- If yes: dispatch `process-ingest` on the artifact path
- This is the "compounding" mechanism — each research turn that produces a work artifact
  can feed back into the wiki layer within the same session

The `inbox-auto-ingest.py` hook covers Inbox/ + Clippings/ channels (after the W-D1-FIX
scope extension). Projects/work/ ingest-back requires explicit main-session dispatch
because the hook cannot distinguish routine work files from synthesis artifacts by path alone.

---

## §4 — Maintenance Cadence

### Ingest backlog (Clippings/ channel)

**Current state:** 6 files stale, oldest 35 days. After W-D1-FIX extends hook scope to
Clippings/, future Clippings/ writes auto-trigger process-ingest within the session.

**Backlog drain process:**
- At next session start, `session-start-orientation.py` detects Clippings/ files where
  last-modified date is >48 h before any INGEST log entry referencing that path
- Surfaces: `[INGEST BACKLOG] N Clippings/ files exceed 48-hr SLA. Dispatch process-ingest?`
- Main session dispatches process-ingest on each qualifying file (up to 3 per session
  to stay within token budget; remainder queued to next session)

**Implementation:** extend `session-start-orientation.py` to read `log.md` ingest entries
and cross-reference against `Clippings/` directory mtime. ~30 lines of Python.

### Stale wiki page detection

A wiki page is stale if:
- `last_modified` frontmatter is >30 days old AND
- its primary source file has been modified since ingested_at (detected via mtime vs
  `source[0].ingested_at`), OR
- the page has received 0 qmd query hits in the last 30-day window (unused + stale = archive candidate)

Detection runs inside `process-lint` Pass A (already implemented). The stale-page report
output format should include an `ACTION: REFRESH | ARCHIVE | KEEP` recommendation per page.

**Refresh policy:**
- Source document materially updated (new content section added) → re-run process-ingest
  on the source, update the wiki page in place
- Source document unchanged, wiki page outdated by new related sources → manual Edit
  to add cross-links + new source entries

**Archive policy:**
- Page last_modified >60 days, 0 qmd hits in window, source document archived or deleted
  → tag with `wiki_status: archived`, move to `Resources/KB/archive/`
- Archive is reversible; do not delete

### Ratification cadence

Bootstrap pages accumulate when process-ingest fires but Wiktor hasn't reviewed yet.
`session-start-orientation.py` should surface: `[WIKI RATIFY] N bootstrap pages pending review.`
when count >0. Wiktor reviews and promotes `wiki_status: bootstrap → ratified` via Edit.

This keeps the bootstrap queue visible without adding a separate calendar reminder.

---

## §5 — Measurement (G0-W axis)

**G0 — Query utilization rate**

Definition: `wiki_query_turns / wiki_eligible_turns` over a rolling 7-day window.

Where:
- `wiki_eligible_turns` = turns where `user-prompt-submit.py` emitted a `[WIKI GATE]` signal
- `wiki_query_turns` = subset where `governance-log.py` recorded `wiki_query_fired: true`
  (detected by `mcp__qmd__query` appearing in PostToolUse tool_name)

Target: ≥70% (same compliance floor as other must-dispatch rules)
Current baseline: 0% (no qmd query calls against agr-kb in production sessions to date)

**G1 — Ingest cadence**

Definition: `ingest_count / days_in_window` over rolling 30-day window

Target: ≥1 ingest per 7 days (implies ~4/month for a vault receiving weekly Clippings drops)
Current: 2/15 days = 0.13/day (well below 0.14/day target)

**G2 — Stale page ratio**

Definition: `stale_pages / total_wiki_pages` where stale = last_modified >30 days AND
not a static Dataview-driven MOC

Target: <20%
Current: unmeasured (process-lint Pass A data needed)

**Measurement infrastructure:**
- `governance-log.py` already exists; add `wiki_query_fired` field to its per-turn emission
- `_daily_aggregate.py` already exists; add G0/G1/G2 to its daily roll-up
- Weekly routine (via `CronCreate`): run `process-lint` + emit G0/G1/G2 to
  `Resources/Observability/wiki-health-weekly.md`

**How you know active-use is actually happening (concrete test):**
1. Open `.claude/hooks/aggregates/wiki-query-log.jsonl`
2. Count rows with `wiki_query_fired: true` where `wiki_eligible: true`
3. If count ≥ 5 across last 7 days of eligible turns → G0 is live

If G0 stays at 0 after 2 weeks with the CLAUDE.md policy + UserPromptSubmit hook in place,
the compliance mechanism is insufficient → escalate to a hard-block PreToolUse hook that
blocks the first non-tool response on a Category A/B/C turn until a qmd call is recorded.

---

## §6 — Failure Modes + Mitigations

**FM-1: qmd MCP not loaded (server failed to start)**

Symptom: `mcp__qmd__*` tools absent from tool listing.
Detection: main session checks at session start (already noted in CLAUDE.md §Memory Recall).
Mitigation: fall back to `Grep` on `Resources/KB/` + Read on `index.md`. Document the
fallback in CLAUDE.md so it fires automatically when qmd is absent, not only when Claude
notices the absence.

**FM-2: Wiki query fires but returns low-relevance results**

Root cause: sparse wiki (13 pages for a vault covering 10+ projects) → BM25 fails on
sparse vocabulary.
Mitigation: ingest-back path (§3) is the structural fix; each session that ingests a
work artifact grows coverage. Short-term: qmd hyde sub-query generates a hypothetical
document that expands coverage. Include `type: 'hyde'` in the default query shape.

**FM-3: WIKI GATE signal fires on too many turns (noise → compliance collapse)**

Root cause: regex over-broad; triggers on routine quick tasks.
Detection: G0 denominator (wiki_eligible_turns) grows faster than it should.
Mitigation: tune Category A/B/C regex against 20-turn sample of typical prompts before
deploying. Add an explicit Quick-class short-circuit: if user-prompt-submit.py already
classified the turn as Quick (presence of quick-class skip_list match), skip WIKI GATE.

**FM-4: Ingest-back creates low-value wiki pages (noise in agr-kb)**

Root cause: every work/ artifact gets promoted regardless of synthesis quality.
Mitigation: process-ingest Step 4 citation gate already prevents fabrication. Additional
filter: only ingest-back files tagged `#research`, `#analysis`, or `#wiki` — operational
files (STATE.md, task_plan.md) are excluded. The `process-ingest` skill's Do-NOT-use-when
clause covers this but needs explicit mention of "work/ files without research/analysis tags."

**FM-5: Bootstrap queue grows faster than Wiktor reviews**

Root cause: process-ingest fires frequently, Wiktor reviews rarely.
Detection: bootstrap count in index.md grows >3 pages over 14 days.
Mitigation: `session-start-orientation.py` surfaces the count at every session. If count
>5, add an explicit block suggestion: "Bootstrap queue has N pages pending. Consider
ratifying or archiving before adding more."

**FM-6: Wiki layer becomes stale relative to doctrine changes (CLAUDE.md updates)**

Root cause: CLAUDE.md changes don't trigger process-ingest because CLAUDE.md is schema
layer, not raw layer.
Mitigation: when CLAUDE.md is edited via Edit tool, `wiki-citation-check.py` (PostToolUse)
checks whether any wiki page has `source.path = "CLAUDE.md"` — if yes, those pages are
flagged as potentially stale (SOURCE_DRIFT adjacent). Add this cross-check to
`_wiki_citation_logic.py`.

---

## §7 — Out of Scope

This process explicitly does NOT address:

1. **process-query (V2)** — wiki-to-answer synthesis with query-result stored back as a
   wiki page. That is a separate operation (per CLAUDE.md: "Query (V2, deferred)").
   This design governs active RETRIEVAL of existing wiki pages, not new query-artifact synthesis.

2. **Multi-collection qmd queries** — queries spanning both `agr-kb` and `memory`
   collections simultaneously. The active-use trigger described here targets `agr-kb`.
   `memory` collection queries remain governed by §Memory Recall as written.

3. **Wiki page authoring quality** — the process-ingest skill's citation gate (Steps 4-6)
   governs what gets written. This document governs WHEN ingest fires and HOW wiki is read.
   Content quality improvement is process-ingest's remit.

4. **Automatic ratification** — promotion from `bootstrap` to `ratified` remains
   Wiktor-only. This design keeps him in the loop via session-start surfacing without
   requiring his intervention to initiate ingest or query.

5. **Cross-session query result persistence** — query results are consumed within the
   session. If a query result warrants permanent wiki storage, the ingest-back path (§3)
   is the mechanism; that is intentional and not a gap in this design.

6. **Clippings/ backlog drain timeline** — the 6-file backlog should be drained manually
   in the next available session. This document designs the forward-steady-state process;
   it does not specify the catch-up schedule for the existing debt.
