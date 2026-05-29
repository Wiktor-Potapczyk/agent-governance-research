---
date: 2026-05-26
updated: 2026-05-26
tags: [project/agent-governance-research, audit, analysis, wiki]
status: active
reviewer: adversarial-reviewer (sub-agent, W-D2 ensemble lens C 2026-05-26 01:08)
target: wiki active-use premise
---

# W-D2 Adversarial Lens — Challenge the Active Wiki-Use Premise

> Adapted from internal research workspace. Cross-references to vault-internal artifacts have been stripped or genericized.

Lens: adversarial-reviewer

**Recovery note:** sub-agent produced this content inline but its tool-list (frozen at session start per the agent-frontmatter-tools-require-session-restart reference) excluded Write. Substance recovered verbatim by main session.

## Findings

**[CRITICAL] Unstated Assumption — The auto-trigger pipeline has zero successful end-to-end completions in production.** W-D1 (`Projects/Agent-Governance-Research/work/2026-05-26-wiki-ingest-velocity-diagnose.md`, L111) states: "the empirical 'auto-trigger → ingest' path has 0 successes to date. The path is unproven in production." The entire active-use model presupposes a functioning supply pipeline. Without successful automated ingest, active querying returns a static snapshot from 2026-05-10 (INGEST-001) plus one manually triggered outlier (INGEST-002, 2026-05-25). Activating the query-side of a broken supply chain does not fix the supply chain — it surfaces stale content as current truth.

**[CRITICAL] Silent Failure Mode — Stale-wiki-query is worse than no-query because it carries authority framing.** Six Clippings/ files are unprocessed with the oldest 35 days stale against a 48-hour SLA (W-D1, L53). When qmd returns a result from a page synthesized from a 35-day-stale source, the session has no signal that the result is outdated. Memory files and training context at least have known provenance uncertainty; a wiki page with a `source:` field and a `sha256:` binding signals "verified, authoritative." A session that queries wiki and gets a stale answer has less epistemic uncertainty than the actual information warrants. Silence is epistemically cleaner than authoritative-but-stale.

**[CRITICAL] Compliance-Theater Risk — "Did you query the wiki?" is structurally isomorphic to the closed-loop measurement problem already diagnosed as the framework's primary flaw.** The framework evaluation (`Projects/Agent-Governance-Research/work/2026-05-25-framework-evaluation.md`, L42–48) documents: `qa_fails: 0` on dates spanning documented fabrication incidents; every framework metric describes conformance to its own rules, not output correctness. A wiki-query compliance check adds another self-referential signal: "wiki queried = TRUE" in the governance log does not distinguish "wiki queried, result accurate" from "wiki queried, result stale/wrong." The compliance log cannot record the semantic quality of the query result. This is the same closed-loop failure mode, instantiated again.

**[WARNING] Counterargument — The genuine-value surface is 1 ratified non-MOC content page.** `Resources/KB/index.md` (L35–45) shows: 12 ratified pages, 11 of which are MOCs (navigation layers, not knowledge). The one ratified non-MOC knowledge page is `karpathy-claudemd-insights.md`. INGEST-002 (`cmdb-vault-setup.md`) is bootstrap-status, not ratified. Of the sampled pages: (a) `karpathy-claudemd-insights.md` — covers Karpathy's four coding principles. Claude's training context covers these directly; the principles appear verbatim in public writing from both Karpathy and forrestchang's GitHub adaptation. Wiki-query here is pure duplication of training context. (b) `moc-n8n-patterns.md` — a navigation index pointing at vault work files. Not knowledge; not synthesized content. Querying this returns a file list. (c) `cmdb-vault-setup.md` — 41-skill / 33-agent / 40-hook structural inventory of THIS vault. Training context cannot cover this; it is vault-specific. Genuine value example. Score: 1 of 3 sampled pages provides non-duplicative value. The break-even case requires active-use overhead to be justified by the 1-page genuine-value surface.

**[WARNING] Cost/Benefit Gap — Per-turn query cost has no measured break-even rate.** The vault-framework-usage-audit (`Projects/Agent-Governance-Research/work/2026-05-24-vault-framework-usage-audit.md`, L21) records 0 process-query invocations ever across the vault's operational history. There is therefore no empirical denominator for "turns per session that would benefit from a wiki query over training context." Without that denominator, "add active use" assigns a cost (qmd round-trip, context window tokens for the result, false-positive query on pages whose content is covered by training) to a benefit that has never been measured. The break-even analysis is not missing — it is zero because the benefit side of the calculation has no data.

**[WARNING] Wiki-Rot Ratchet — Ingest cadence cannot sustain an active-use model.** Log.md (L32, L99) shows 2 ingest entries across 15 days. W-D1 (L96) confirms the Inbox channel had zero qualifying ingest triggers in that window, and the Clippings channel has no auto-trigger at all (hook scope-gapped against CLAUDE.md spec). Extrapolating: at 2 ingests per 15 days against 6+ qualifying inputs accumulating per 15 days, the wiki is net-falling-behind. At 90 days: ~12 ingests vs. ~36 qualifying inputs. Every active-use query against a decaying knowledge layer returns an answer that is less correct than it appeared on ingest day. The active-use model requires the supply chain to keep pace with decay; empirically it does not.

**[GAP] Missed Alternative — Memory-first lookup already covers the genuine-value subset without ingest overhead.** The memory collection (333 one-fact files indexed in qmd per CLAUDE.md Memory Recall section) contains vault-specific operational facts that training context does not cover: n8n failure modes, fabrication incident records, API behaviors, agent dispatch patterns. The cmdb-vault-setup.md wiki page synthesizes content that the memory files cover individually at finer granularity. The wiki's claimed advantage — synthesis and cross-linking — would only be an advantage over memory once enough ratified synthesis pages exist. At 1 ratified non-MOC page, that advantage does not exist. Memory-first lookup is a lower-overhead path to the same genuine-value subset.

**[GAP] Evidence Gap — qmd dependency failure mode is not addressed in the active-use premise.** CLAUDE.md (Memory Recall section) acknowledges: "If no mcp__qmd__* tools are present, the qmd MCP server failed to start — fall back to Grep/Read on the memory folder and flag it." The memory fallback path (Grep/Read) exists. No equivalent fallback path is specified for wiki queries if qmd returns stale embeddings or fails. A session that relies on wiki-first lookup and encounters qmd failure has no degradation path to verify whether the fallback (Grep on Resources/KB/) returns current content or a stale cached read. Silent degradation under qmd failure is not addressed.

**[NOTE] Genuine-value carve-out — where active use clearly earns its cost.** The adversarial position is not "kill the wiki." It is: at current scale (1 ratified non-MOC page, 0 process-query entries ever, ingest cadence below input velocity), the active-use overhead exceeds the marginal benefit. The carve-out that genuinely earns active-use cost: vault-specific structural knowledge that is expensive to reconstruct and changes slowly — the CMDB pattern (`cmdb-vault-setup.md`) is the live example. If ingest velocity increased to match qualifying input accumulation, and if 10+ synthesis pages covered vault-specific patterns (agent dispatch contracts, hook interaction maps, cross-project n8n anti-pattern instances), the break-even case would invert. The argument strengthens only when the supply chain functions and the synthesis layer grows. Neither condition currently holds.

## Verdict

The active-use premise is flawed at current wiki scale and ingest cadence: 1 ratified non-MOC content page, 0 successful auto-trigger-to-ingest completions in production, 6 Clippings inputs sitting 35 days stale, and a compliance-theater failure mode structurally identical to the one the framework evaluation already identified as the vault's primary governance problem. The correct model at current state is **ARCHIVE with targeted active-use for vault-specific structural knowledge only (CMDB-class pages)**, NOT a session-wide query habit. **Confidence: 0.82.**

## Key evidence anchors

- `Projects/Agent-Governance-Research/work/2026-05-26-wiki-ingest-velocity-diagnose.md` — L53 (6 stale Clippings files), L111 (0 successful auto-trigger completions), L96 (Inbox channel zero qualifying triggers)
- `log.md` — L32 (INGEST-001, 2026-05-10), L99 (INGEST-002, 2026-05-25)
- `Projects/Agent-Governance-Research/work/2026-05-24-vault-framework-usage-audit.md` — L21 (0 query entries), L52–56 (Gap D diagnosis)
- `Projects/Agent-Governance-Research/work/2026-05-25-framework-evaluation.md` — L42–48 (closed-loop measurement failure)
- `Resources/KB/index.md` — L35–45 (12 ratified pages, 11 MOCs, 1 non-MOC ratified)
- `Resources/KB/karpathy-claudemd-insights.md` — content analysis (training-context duplication)
- `Resources/KB/cmdb-vault-setup.md` — L1–20 (vault-specific structural knowledge, genuine-value example)
- CLAUDE.md Memory Recall section (qmd fallback path exists for memory, not for wiki)
