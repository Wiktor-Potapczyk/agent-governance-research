
# Monitoring Baseline — Iteration 0

**Purpose:** Compute baseline values for all 9 KPIs from existing data. This is the reference point for Iteration 3 trend analysis.
**Data sources:** governance-log.jsonl (815 entries, 17 sessions) + 3 CC session JSONLs
**P0 fix applied:** must_dispatch parsing corrected (extract_dispatch_names) before DAR computation

---

## Governance Layer Baselines (from governance-log.jsonl)

### KPI-2: DAR (Dispatch Adherence Rate)

| Metric | Value |
|--------|-------|
| Entries with non-null must_dispatch | 45 (of 326 classifications) |
| Total declared items (after P0 fix) | 66 |
| Total matched items | 30 |
| **DAR (item-level)** | **45.5%** |
| DAR before P0 fix | 12.9% (artifact — 163 declared items included garbage) |

**Interpretation:** 45.5% is well below the 88% target. Primary cause: `process-qa` is the most frequently skipped dispatch — it appears in MUST DISPATCH but is not invoked in the same turn the classifier runs. This is partially a real compliance gap (QA genuinely skipped) and partially a measurement limitation: governance-log.py only captures dispatches from the classification turn, not subsequent turns where QA may actually be invoked.

**Known limitation:** DAR measures same-turn dispatch only. A classifier that emits MUST DISPATCH on turn N, with the actual dispatch happening on turn N+2 (after task decomposition), will show as a miss. This is a structural measurement gap, not a compliance gap. P2-B (dispatch pass events) will improve this.

### KPI-3: HSR (Hook Signal Rate)

| Metric | Value |
|--------|-------|
| Enforcement events (blocks + denies) | 77 (65 blocks + 12 denies) |
| Classification entries | 326 |
| **HSR** | **0.236** |

**Block breakdown by hook:**
| Hook | Count |
|------|-------|
| dispatch-compliance | 34 |
| subagent-quality-check | 16 |
| process-step-check | 9 |
| classifier-field-check | 6 |
| bash-safety-guard (deny) | 12 |

**Interpretation:** HSR of 0.236 means roughly 1 in 4 classified turns triggers an enforcement event. Target is convergence toward 0.05-0.10. The high rate reflects early framework development (hooks being tuned, processes being learned). dispatch-compliance is the dominant blocker.

### KPI-6: DZUR (Dark Zone Utilization Rate)

| Metric | Value |
|--------|-------|
| DZ entries with ratio field | 370 |
| Entries with ratio >= 1.0 | 244 |
| **DZUR** | **65.9%** |

**Severity distribution:** low: 268, high: 84, medium: 18

**Interpretation:** 65.9% is below the provisional 80% target. 84 high-severity entries (22.7%) indicate substantial non-utilization of agent output. However, dark zone detection uses heuristic citation matching — some "non-utilization" may be inline summarization that the regex doesn't detect.

### Classification Type Distribution

| Type | Count | % |
|------|-------|---|
| Quick | 280 | 85.9% |
| Analysis | 28 | 8.6% |
| Build | 15 | 4.6% |
| Compound | 2 | 0.6% |
| Planning | 1 | 0.3% |

**Note:** Quick dominates. DAR only applies to non-Quick tasks (46 entries). The small sample size for non-Quick types limits statistical confidence.

---

## Cost Layer Baselines (from 3 session JSONLs)

### Sessions Analyzed

| Session | Type | Duration | SC Total | SC Sub Ratio | Model |
|---------|------|----------|----------|-------------|-------|
| 27bd3370 (Logo Finder) | Build/MCP | ~5h | $296.90 | 1.0% | Opus only |
| 1b8cd93c (Paper) | Analysis | multi-day | $3,862.25 | 54.5% | Opus only |
| d977eafd (Monitoring) | Planning | multi-day | $3,866.60 | 43.4% | Opus + Sonnet |

### KPI-4: SC (Session Cost)

| Metric | Logo Finder | Paper | Monitoring |
|--------|-------------|-------|------------|
| Total | $296.90 | $3,862.25 | $3,866.60 |
| Main session | $294.04 | $1,755.84 | $2,189.76 |
| Subagent | $2.86 | $2,106.41 | $1,676.84 |
| Sub ratio | 1.0% | 54.5% | 43.4% |
| Subagent files | 11 | 56 | 190 |

**Interpretation:** SC varies enormously by session length and model. Logo Finder was a single-session Opus run. Paper and Monitoring were multi-day, multi-compaction sessions. Sub ratio exceeds the 35% target for Paper (54.5%) and is borderline for Monitoring (43.4%). Logo Finder's 1.0% reflects that Ralph Loop subagents run as Sonnet while main session was Opus.

**Baseline warning:** These are not representative of typical sessions — they are some of the longest and most expensive sessions in the corpus. Median session cost is likely $5-30 for normal tasks. These serve as upper-bound reference points, not typical baselines.

### KPI-5: HOR (Hook Overhead Ratio)

| Metric | Logo Finder | Paper | Monitoring |
|--------|-------------|-------|------------|
| Avg hook chain | 4,235ms | 4,392ms | 5,498ms |
| Avg turn duration | 226,705ms | 147,263ms | 226,471ms |
| **HOR** | **1.87%** | **2.98%** | **2.43%** |
| Samples | 39 | 313 | 648 |

**Interpretation:** All three sessions under the 3% median target. Hook overhead is consistent at 4-5.5 seconds per turn. The monitoring session's 5.5s chain is the highest — likely due to more hooks being active during that development period. No individual hook exceeding 1,500ms alert threshold observed in aggregate (per-hook breakdown requires deeper parsing).

---

## Work Patterns Layer Baselines (from 3 session JSONLs)

### WP-1: Tool Distribution Profile

| Tool | Logo Finder | Paper | Monitoring |
|------|-------------|-------|------------|
| Total | 340 | 1,344 | 2,931 |
| Top 1 | mcp__n8n-mcp__n8n_test_workflow (56) | Bash (466) | Bash (396) |
| Top 2 | mcp__n8n-mcp__n8n_update_partial_workflow (48) | Read (253) | Read (357) |
| Top 3 | Edit (35) | Edit (190) | Edit (280) |
| Top 4 | TaskUpdate (26) | Grep (152) | TaskUpdate (241) |
| Top 5 | Read (21) | Write (78) | Agent (205) |

**Interpretation:** Tool profiles are highly task-dependent. Logo Finder is MCP-dominated (n8n workflow operations). Paper is Bash-heavy (running experiments). Monitoring has the most Agent dispatches (205) reflecting heavy delegation patterns. Tool profiles can be used as session-type fingerprints.

### WP-2: UCR (User Correction Rate)

| Metric | Logo Finder | Paper | Monitoring |
|--------|-------------|-------|------------|
| Total "user" entries | 416 | 1,886 | 4,173 |
| userType: external | 416 | 1,886 | 4,173 |

**FINDING: userType: external does NOT distinguish real human turns from hook injections.** All user entries show userType: external. Content-based filtering is required (check for `system-reminder` tags, hook output patterns, or message length heuristics). Logo Finder had ~78 real human turns (from previous deep analysis), meaning 81% of "user" entries were hook injections.

**UCR baseline:** NOT COMPUTABLE with current data. Requires content-based human turn filter implementation in session-summary.py (Iteration 2).

### WP-3: MCP Operation Ratio

| Session | MCP calls | Total calls | Ratio |
|---------|-----------|-------------|-------|
| Logo Finder | 171 | 340 | **50.3%** |
| Paper | 0 | 1,344 | **0.0%** |
| Monitoring | 670 | 2,931 | **22.9%** |

**Interpretation:** MCP ratio is a clean task-type discriminator. MCP-heavy sessions (>30%) are n8n workflow work. Zero-MCP sessions are pure research/analysis.

### WP-4: APR (Artifact Production Rate)

| Session | File writes | Agent dispatches |
|---------|-------------|-----------------|
| Logo Finder | 49 | 11 |
| Paper | 268 | 52 |
| Monitoring | 403 | 205 |

**Interpretation:** File writes and agent dispatches scale with session length. Per-turn rates would be more comparable but require turn count (dependent on WP-2 fix for accurate turn counting).

---

## Iteration 0 Gate Assessment

**Gate question:** Can we compute at least 7 of 9 KPIs from existing data?

| KPI | Computable? | Notes |
|-----|-------------|-------|
| KPI-2 DAR | YES (with caveats) | 45.5% — same-turn measurement limitation documented |
| KPI-3 HSR | YES | 0.236 — stable, well-defined |
| KPI-4 SC | YES | $297-$3867 range — need more typical sessions for median |
| KPI-5 HOR | YES | 1.87-2.98% — under target, consistent |
| KPI-6 DZUR | YES | 65.9% — below target, heuristic-dependent |
| WP-1 Tool Profile | YES | Task-type dependent, descriptive |
| WP-2 UCR | NO | userType filter insufficient — needs content-based filter |
| WP-3 MCP Ratio | YES | 0-50.3% range — clean discriminator |
| WP-4 APR | PARTIAL | Raw counts yes, per-turn rates need WP-2 fix |

**Result: 7 of 9 computable (WP-2 blocked, WP-4 partial).** Gate PASSES.

---

## Key Discoveries

1. **P0 fix impact:** 97 garbage tokens removed from must_dispatch. DAR jumped from 12.9% (artifact) to 45.5% (real but low).
2. **DAR same-turn limitation:** governance-log.py only sees dispatches in the turn where classification happens. Multi-turn dispatch sequences are missed. P2-B (pass events) needed.
3. **userType: external is universal:** Does not distinguish hook injections from human input. Content-based filter needed for WP-2.
4. **Session cost range is extreme:** $297 (5h single session) to $3867 (multi-day). Per-hour or per-task cost would be more useful than per-session.
5. **HOR is consistently under 3%:** Hook overhead is not a concern at current scale.
6. **Quick dominates classifications (85.9%):** Non-Quick sample is small (46 entries). DAR/HSR trends for non-Quick tasks have limited statistical power.

---

## Baseline Stationarity Warning

These 17 sessions span a system that was changing during observation:
- Pre-2026-04-02: no work-verification hook (affects pass event count)
- Pre-P0 fix: must_dispatch had parsing bug (DAR unreliable for historical data)
- Logo Finder: governance-dark (Ralph Loop session)
- Hook count changed from ~12 to ~18 during the period

Treat all baselines as provisional anchors from a non-stationary system, not as benchmarks.
