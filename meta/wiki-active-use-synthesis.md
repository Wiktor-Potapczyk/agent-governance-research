---
date: 2026-05-26
updated: 2026-05-26
tags: [project/agent-governance-research, planning, spec, wiki, analysis]
status: active
---

# W-D2/W-D3 Synthesis — Wiki Active-Use Design

> Adapted from internal research workspace. Cross-references to vault-internal artifacts have been stripped or genericized.

Ensemble inputs: architect lens (325 lines, pro-active-use) · prompt-engineer lens (187 lines, drop-in implementation) · adversarial lens (ARCHIVE-with-carve-out, confidence 0.82)

Main-session synthesis per the opus-reasoning-main-session doctrine — Opus-level merge of 3 cold-context lenses. Divergent verdicts preserved per the surface-divergent-verdicts doctrine.

## 1. Convergent findings (all 3 lenses agree)

- **Wiki has SOME value.** No lens recommends deletion. The disagreement is over scope of active-use, not existence.
- **Ingest velocity is below input velocity.** Architect §5 (bootstrap queue grows unattended), Prompt-engineer §7 (well-queried sparse wiki still surfaces sparse results), Adversarial §wiki-rot-ratchet (2 ingests / 15 days < 6 inputs / 15 days). The supply chain is the binding constraint, not the read habit.
- **CLAUDE.md prose alone is insufficient compliance mechanism.** ~25% empirical rate per CLAUDE.md §Working Philosophy. Prompt-engineer §2 makes this explicit; Architect §4 implicitly assumes hook-layer enforcement; Adversarial §compliance-theater warns against relying on it.
- **Subagents lack qmd MCP access.** All 3 lenses cite the subagents-lack-MCP-access constraint. Any wiki-first rule is main-session only.
- **Compaction strips additionalContext.** SessionStart-injected wiki context dies at compaction. Prompt-engineer §2 makes this load-bearing; both other lenses concur implicitly.

## 2. Divergent verdicts (preserve, do not collapse)

| Question | Architect lens | Prompt-engineer lens | Adversarial lens |
|---|---|---|---|
| Should active-use be wide or narrow? | Wide — process design covers doctrine + research + architecture | Wide — 10 trigger pattern categories | Narrow — CMDB-class only; doctrine questions likely covered by training context |
| Implement now vs. wait? | Now — full process spec ready | Now — drop-in implementation provided | Wait — establish ingest velocity ≥ input velocity AND grow ratified-knowledge-pages count first |
| Compliance theater risk | FM-3 noted but mitigable | §7 failure modes addressed | Structurally isomorphic to framework's primary diagnosed flaw — high risk |
| Genuine-value surface | 11 MOCs + 1 ratified content page + growing | 10 trigger categories assume coverage | 1 page (cmdb-vault-setup); the rest are MOCs or duplicate training context |

## 3. Resolution (operative recommendation)

The adversarial lens makes the strongest empirical case: at **current scale** (1 ratified non-MOC content page, 0 process-query invocations ever, ingest 2/15-days), the architect+prompt-engineer's wide active-use design over-invests for an under-supplied wiki. BUT the adversarial's carve-out (vault-specific structural knowledge clearly earns active-use cost) provides the right scoping.

**Synthesized verdict:** ratify a **NARROW active-use rule scoped to vault-specific knowledge categories**, with explicit re-evaluation after 30 days of measurement. Don't deploy the wide-trigger design until ingest velocity stabilizes ≥ input velocity AND ratified-content-page count reaches ≥10 (currently 1).

**Confidence:** 0.78 (lower than adversarial's 0.82 because the synthesis adopts narrow scope, which the architect would consider under-ambitious; preserving adversarial's carve-out logic but adding implementation path).

## 4. Concrete next-iteration ship plan

### Phase 1 — Narrow rule + measurement (autonomous, ~30 min)

Implement what's empirically defensible NOW. Defer the broader design to Phase 2 (gated on Phase-1 data).

1. **CRITICAL RULE block in CLAUDE.md** (Memory Recall section, ~6 lines):

   > **Wiki-first for vault-specific knowledge categories.** Before answering questions about: (a) n8n node behavior / patterns, (b) vault hook behavior or doctrine, (c) agent dispatch contracts or governance findings, (d) CMDB-class structural inventory — call `mcp__qmd__query` against the `agr-kb` collection FIRST. If 0 results, proceed with training-context synthesis but note in response. Skip for Quick tasks and conversational follow-ups. Other categories (general research, architecture decisions) do NOT trigger this rule pending Phase 2 evaluation.

   Scope is deliberately narrow per adversarial §genuine-value carve-out. The 4 categories are where vault-specific knowledge demonstrably exceeds training-context coverage (n8n vault patterns / hook behavior / governance memos / structural inventory).

2. **Governance-log instrumentation** (extend `governance-log.py`):

   Add `wiki_queried: bool` field per Prompt-engineer §5. Detect `mcp__qmd__query` tool_use blocks. Establishes baseline compliance rate from Day 1.

3. **NO hook injection in Phase 1.** Adversarial's compliance-theater warning applies most strongly to hook-enforced compliance. Phase 1 is prose-rule-only at ~25% baseline compliance — that's a conservative test that the rule helps even at low compliance, AND it doesn't add the second self-referential metric the adversarial lens warned about. If after 30 days the rule shows <10% compliance with measurable accuracy lift on the 4 carve-out categories, escalate to Prompt-engineer §3 hook injection.

4. **Measurement window: 30 days.** Aligns with Action 0.1 calibration cadence ([[action-0-1-calibration-protocol]]) — Wiktor can include "did a sampled artifact involve a category where wiki-query would have helped, and did Claude actually query?" as a calibration sub-axis.

### Phase 2 — Wide-trigger gate (deferred, conditional)

Gated on Phase-1 evidence:
- **Gate A:** Ingest velocity ≥ input velocity over rolling 30-day window. (Empirical test: ingest count over window ≥ qualifying-input count over same window.)
- **Gate B:** Ratified non-MOC content pages ≥ 10. (Currently 1.)
- **Gate C:** Phase-1 narrow rule shows ≥30% compliance OR Wiktor calibration shows ≥30% of sampled artifacts in the 4 carve-out categories.

If all 3 gates pass → ship Prompt-engineer's full UserPromptSubmit hook + Architect's process flow. If any gate fails → keep Phase 1 narrow scope, surface the gating gap to next planning cycle.

### Phase 3 — Supply chain reinforcement (parallel with Phase 1)

The adversarial lens's strongest argument is that querying a decaying wiki amplifies stale-as-authoritative risk. The supply chain MUST be fixed in parallel:

- W-D1-FIX shipped this loop (Clippings/ now ingest-trigger). 7 stale Clippings to be ingested next iteration (§A1 of the improvements plan).
- process-ingest skill is functional + bootstrap-cap is past.
- Add a periodic "stale wiki detector" to process-lint (Pass D): for each #wiki page where last_verified > 60 days old, flag for refresh. Implementation: ~30 lines, fits in existing process-lint structure.

## 5. Out-of-scope (this synthesis explicitly does NOT specify)

1. **The full UserPromptSubmit hook regex** (Prompt-engineer §1) — deferred to Phase 2.
2. **Bootstrap → ratified workflow refinement** (Architect §5 FM-5) — separate ticket.
3. **CLAUDE.md source-drift detection** (Architect §FM-6) — separate ticket, can ship anytime.
4. **process-query V2 design** — explicitly out per CLAUDE.md.
5. **Clippings ingest backlog drain** — §A1 of improvements plan; mechanical work not requiring this synthesis to ship first.

## 6. Implementation order recommendation

This synthesis closes W-D2 + W-D3 + provides ship plan for W-V1 (narrow scope only):

1. **NOW (next loop iteration):** Phase 1 narrow rule + governance-log instrumentation. ~30 min autonomous.
2. **Parallel:** §A1 Clippings ingest backlog drain (supply chain).
3. **2026-06-25 (G1 audit day):** review Phase 1 compliance data + gates. Decide Phase 2 ship vs. defer.
4. **Phase 3 stale-wiki detector** — implementable any time; gates Phase 2 if Phase 1 data is ambiguous.

## 7. Failure modes (from synthesis, not lens-specific)

- **The narrow rule is too narrow + everyone agrees it's correct + compliance is high (90%+) but accuracy lift is undetectable** — the 4 carve-out categories may already be well-covered by Claude's habit of grepping Resources/KB/ before answering. Test: Action 0.1 calibration cadence at +30d should surface this if it happens.
- **The narrow rule expands by gradual scope-creep** — Claude or Wiktor adds a 5th category, then 6th. Without explicit Phase-2 gate evaluation, narrow rule becomes wide rule by drift. Mitigation: every category addition must cite empirical lift evidence; otherwise reject.
- **Adversarial gate B (≥10 ratified pages) never passes** — current cadence won't get there in 90 days. Phase 2 stays deferred forever. This is the synthesis equivalent of "decide later" — acceptable if Phase 1 narrow scope is genuinely sufficient; problematic if it leaves a real gap.

## 8. Related

- [[action-0-1-calibration-protocol]] — external calibration cadence (measurement integration)
- [[2026-05-25-framework-evaluation]] — closed-loop measurement problem (adversarial cited this)
