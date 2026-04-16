
# Prompt Compression Research — Synthesized Findings

## 1. Current Framework Token Footprint

| Component | Files | Chars | Est. tokens | Loading |
|---|---|---|---|---|
| CLAUDE.md | 1 | 14,880 | 3,720 | Always-on |
| MEMORY.md | 1 | 19,742 | 4,935 | Always-on |
| Skills | 84 | 726,685 | 181,671 | On-demand (per-invocation) |
| Agents | 30 | 210,160 | 52,540 | On-demand (per-spawn) |
| **TOTAL** | **116** | **971,467** | **~243K** | |

**Always-on overhead:** ~8,655 tokens/session (CLAUDE.md + MEMORY.md).
**Per-task overhead:** varies by skill/agent mix. A typical non-Quick task loads task-classifier (~4,770 tokens) + one process skill (~3K-5K) + dispatched agents.

**Top compression targets by size:**
1. n8n-code-javascript/COMMON_PATTERNS.md — 29,159 chars (7,289 tokens)
2. nosql-specialist.md — 23,325 chars (5,831 tokens)
3. MEMORY.md — 19,742 chars (4,935 tokens)
4. n8n-code-python/COMMON_PATTERNS.md — 19,301 chars (4,825 tokens)
5. task-classifier/SKILL.md — 19,080 chars (4,770 tokens)

## 2. What Caveman Actually Does

Caveman has TWO separate components that do different things:

### 2a. Output Style Injection (the `/caveman` skill)

A SessionStart hook injects SKILL.md as hidden system context. The LLM self-applies compression rules to its own **output only**. Does not reduce input tokens, reasoning tokens, or system prompt size.

Six levels:
- **lite**: Removes filler and hedging, preserves articles and complete sentences. Grammar intact.
- **full** (default): Drops articles, permits fragments, shorter synonyms.
- **ultra**: Abbreviates technical terms (DB/auth/fn/impl), strips conjunctions, arrows for causality.
- **wenyan-lite/full/ultra**: Classical Chinese variants.

Claimed savings: 22-87% output token range, 65% average. BUT:
- `benchmarks/results/` directory is EMPTY — no committed backing data for these numbers
- The 65% figure uses baseline "You are a helpful assistant" — does NOT isolate skill contribution from generic terseness
- No instruction-following quality benchmarks exist in the repo
- Eval uses tiktoken (OpenAI BPE approximation), not Claude's actual tokenizer

### 2b. File Compressor (`caveman-compress` / `/caveman:compress`)

A Python tool that sends files to Claude API for rewriting. Targets .md/.txt files only. Preserves code blocks, URLs, headings, dates, version numbers. Creates `.original.md` backup.

- ~46% input size reduction average
- NOT idempotent (aborts if backup exists)
- Max 500KB input, 8192 output tokens
- Uses claude-sonnet-4-5 by default (override via CAVEMAN_MODEL env)
- Explicitly produces grammatical fragments ("Fragments OK" is a design choice)

**Key distinction:** The output style injection (2a) is irrelevant to the user's stated goal of reducing input token consumption. The file compressor (2b) is the relevant component, but it produces broken grammar which the user explicitly rejected.

## 3. Technique Taxonomy

### Techniques That BREAK Grammar

| Technique | Mechanism | Compression | Grammar |
|---|---|---|---|
| LLMLingua (Microsoft) | Token deletion via perplexity scoring | Up to 20x | Broken by design |
| caveman-compress | LLM rewriting with fragment rules | ~46% | Fragments by design |
| caveman /full, /ultra | Output style enforcement | 22-87% output | Articles dropped |

### Techniques That PRESERVE Grammar

| Technique | Mechanism | Compression | Evidence |
|---|---|---|---|
| Style-Compress (EMNLP 2024) | LLM iterative rewriting in readable style | 50% at 0.5 ratio | Performance on par with original |
| SCOPE (arXiv 2508) | Semantic chunking + per-chunk rewriting | 2-5x, <3% degradation | Outperforms LLMLingua-2 at same ratio |
| Tiered/lazy loading | Load minimal triggers, fetch detail on-demand | 54% initial reduction | Production-validated in Claude Code |
| Semantic deduplication | Merge overlapping content | Varies | Part of lazy-loading case study |
| CompactPrompt n-gram | Replace recurring phrases with lossless placeholders | 53-58% | Lossless, grammar preserved |
| Structured reformatting | Tables/lists instead of prose, Markdown over XML | ~15% (format alone) | Up to 300% perf variation from format |
| Prompt caching (Anthropic) | Cache stable prefixes, 90% cost reduction on hits | 0% content reduction | Zero quality impact |

### caveman lite mode

Preserves grammar. Removes filler words and hedging only. This is the closest match to the user's stated preference ("not literally omit articles but something like this"). However, it only affects OUTPUT tokens, not the input prompt size that the user wants to reduce.

## 4. Critical Production Evidence

### Production RCT (arXiv:2603.23525, March 2026)

1,199 production task instructions, 358 analyzed trials:
- **50% retention (moderate):** 27.9% cost reduction, quality maintained
- **20% retention (aggressive):** Quality degraded AND output tokens INCREASED by 3% due to compensatory verbosity. Net cost INCREASE of 1.8%.
- **Recency-weighted compression:** Best quality-cost ratio (23.5% savings)

### Constraint Compliance Risk (arXiv:2512.17920)

Constraint compliance (following explicit directives) degrades FASTER than semantic accuracy under compression. This is directly relevant: system prompts full of behavioral rules and process directives are at HIGHER risk than factual content.

### Compression-Output Paradox

Aggressive compression increases output tokens, potentially negating input savings. The LLM compensates for missing context by generating more explanatory output.

### Format Effects (arXiv:2411.10541)

Format choice alone (Markdown vs JSON vs XML vs plain text) produces up to 300% performance variation independent of content. No universal best format — depends on model.

## 5. Confirmed vs Unconfirmed

### Confirmed (multiple sources or empirical)
- Caveman output style reduces output tokens (repo + eval snapshots exist)
- LLM-based rewriting preserves grammar while achieving 50%+ compression (Style-Compress, SCOPE)
- Lazy loading achieves 54% reduction with zero quality loss (production case study)
- Aggressive compression (>50%) degrades quality and can increase net cost (production RCT)
- Constraint compliance degrades faster than semantic accuracy (separate study)
- Prompt caching gives 90% cost reduction on stable prefixes (Anthropic docs)

### Unconfirmed
- Caveman's 65% savings figure (benchmarks/results/ empty, no committed data)
- Whether caveman-compress produces reliable output for instruction-heavy content (only tested on memory/context files)
- Whether Style-Compress or SCOPE work well on behavioral rule content (tested on QA/summarization, not system prompts)
- Quality impact of compressing this specific framework's hooks/skills/agents

## 6. What Applies to This Framework

**Always-on overhead (CLAUDE.md + MEMORY.md, ~8.7K tokens):** This is the highest-value compression target because it's loaded every session. Candidates: LLM-based rewriting (grammar-preserving), structured reformatting, semantic deduplication within MEMORY.md.

**Skills (~182K tokens, on-demand):** Only loaded when invoked. Compression value depends on invocation frequency. task-classifier is loaded on every non-Quick task (~4.8K tokens) — high value. n8n-code-* patterns loaded only for n8n tasks — lower frequency.

**Agents (~52K tokens, on-demand):** Only loaded when spawned. Compression value depends on spawn frequency. Each agent spawn loads ~60K context overhead (per CLAUDE.md) — the agent definition is a fraction of that.

**Prompt caching:** The framework's CLAUDE.md + MEMORY.md are stable across sessions. If prompt caching is active, the always-on ~8.7K tokens may already cost only 10% of normal rate on cache hits, making content compression less impactful for cost but still valuable for context window budget.

## Sources

- JuliusBrussee/caveman (GitHub, 2026)
- LLMLingua-2 (arXiv:2403.12968, Microsoft)
- Style-Compress (arXiv:2410.14042, EMNLP 2024)
- SCOPE (arXiv:2508.15813, August 2025)
- CompactPrompt (arXiv:2510.18043, ACM ICAIF 2025)
- Production RCT (arXiv:2603.23525, March 2026)
- Constraint Compliance (arXiv:2512.17920)
- Format Effects (arXiv:2411.10541)
- Anthropic Context Engineering Guide
- Anthropic Prompt Caching Docs
- Claude Code 54% Reduction Case (johnlindquist gist)
- Claude Tokenization Analysis (Sander Land)
