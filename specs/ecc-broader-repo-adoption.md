---
date: 2026-05-25
updated: 2026-05-25
tags: [project/agent-governance-research, research, claude-code, analysis]
status: active
type: research-finding
---

> Adapted from internal research workspace. Cross-references to vault-internal artifacts have been stripped or genericized.

# affaan-m/ecc — broader-repo adoption research

Hub: agent-governance research repo · Trigger: owner direction 2026-05-25 ~23:13 "btw maybe we can adopt this https://github.com/affaan-m/ecc"

## Disambiguation from prior vault research

Prior internal research had covered the **narrower sub-skill** `continuous-learning-v2` inside the predecessor repo `affaan-m/everything-claude-code` and recommended option (3) — no adoption — for the narrow scope, in favor of `/hookify`.

Today's URL `affaan-m/ecc` is the **broader umbrella project** (or the predecessor's renamed successor — the description matches: "The agent harness performance optimization system"). Different scope; the prior recommendation does NOT auto-apply.

## What it claims to be (per repo description + WebFetch)

> "The agent harness performance optimization system. Skills, instincts, memory, security, and research-first development for Claude Code, Codex, Opencode, Cursor and beyond."

Stated components (numbers per WebFetch summary — TREAT AS UNVERIFIED; the summary model may have hallucinated): 246 skills, 61 agents, 15 hook event types, 76 commands, MCP configs, multi-platform adapters (CC + Codex + OpenCode + Cursor + Copilot). MIT license. Repo created 2026-01-18, last push 2026-05-25 (today — actively maintained).

**Verified 2026-06-10 via the raw GitHub API** (`api.github.com/repos/affaan-m/ecc`, direct JSON — no summary-model in the path): **212,482 stars, 32,632 forks**, repo created 2026-01-18. The original 192K WebFetch figure was real, not hallucinated — the repo's growth is genuinely exceptional, and it has since grown further. Architecture claims remain assessed on the predecessor's structure.

## Adoption shapes (refreshed for broader scope)

**(A) Full plugin install** — `/plugin install ecc@ecc`. Adds the entire ECC stack on top of vault's existing 40 skills + 33 agents + 40 hooks.
- Pros: instant access to 246 skills, security scanner, token optimization tools, multi-platform adapters.
- Cons: catastrophic namespace collision risk; doctrine layer in ECC's CLAUDE.md will conflict with vault's CLAUDE.md (which is the source of truth for vault behavior). 5 fabrication incidents this session arc demonstrate vault is operating near the edge of doctrine-control already.

**(B) Selective port** — cherry-pick specific high-value items. Candidates from WebFetch summary worth investigating:
- **AgentShield security scanner** — if it's a hook, vault has no comparable security layer.
- **Token-optimization tools** — owner on Claude Max 5x flat-rate subscription; tokens are capacity, not cost, but cache-warming + context-window efficiency still matter.
- **Memory-optimization patterns** — vault has Karpathy LLM-Wiki + qmd; ECC has its own memory system. Comparison could yield improvements without full adoption.
- **Multi-platform adapter pattern** — irrelevant today (vault is CC-only) but useful if portability ever matters.

**(C) Architectural read-only inspiration** — read ECC's structure for ideas; don't install anything. This is the pattern vault already follows for Karpathy LLM-Wiki + Romuald Czlonkowski n8n patterns.

**(D) No adoption** — vault is far enough along its own track that bulk adoption would be disruption-for-disruption's-sake.

## Recommended next steps (not yet a recommendation on adoption)

Two cheap follow-ups would inform a real decision:

1. **Verify the WebFetch numbers** — fetch `https://github.com/affaan-m/ecc` (HTML page, not API) and look for the star/fork counts in the rendered metadata. If the actual count is more modest (say 2-10K), the social-proof argument for adoption weakens. If it really is 192K, that's substantial validation.

2. **Inspect the doctrine layer** — fetch ECC's CLAUDE.md (or equivalent root doc). If its doctrine conflicts substantially with vault's (e.g., different classification primitives, different MUST DISPATCH rules), shape (A) is off the table and (B)/(C) become the only viable options.

Total cost for both: 2 WebFetch calls, ~10 min. Could be done now or scheduled for next iteration.

## Caveats

- **WebFetch summary model can hallucinate** — the 192K-stars figure was initially the most suspicious data point; it was later CONFIRMED via the raw GitHub API (212K by 2026-06-10). The caution stands as method (verify via raw API, not summary output), even though this particular number proved accurate.
- **Prior internal research** was on `affaan-m/everything-claude-code` which may have been renamed to `affaan-m/ecc` — the repos may be the same project with a name change. If so, much of the prior research applies; if not, this is a fresh investigation.
- **No code-level inspection performed** — this note is based on README/description summary only. Any adoption shape (A) or (B) requires reading actual SKILL.md / hook source files.

## Verdict (preliminary)

Default recommendation: **(C) Architectural read-only inspiration** — same shape vault used for Karpathy + Czlonkowski. Cherry-pick patterns later if specific gaps in vault correspond to ECC strengths. Defer (A) and (B) pending the two verification follow-ups.

**Wiktor decision needed:** which follow-up should I run now (verify-numbers, doctrine-conflict-check, or both)? Or do you want me to defer ECC inspection entirely and continue with SA-4 file-existence hook build per the autonomous-loop trajectory?

---

## Verification supplement — 2026-05-25 23:18 (Wiktor picked option 3: both)

### Star count — VERIFIED REAL

Independent raw HTML page fetch of `github.com/affaan-m/ecc/stargazers` returned **192k** verbatim. The number is real, not summary-model hallucination. ECC is a genuine viral CC plugin in the top tier of community CC repos.

Implication: social proof is substantial. The repo's design choices have been pressure-tested at scale. Adoption shapes that draw on its patterns (B/C) gain validity.

### Doctrine conflict — SUBSTANTIVE DIFFERENCES (full plugin install ruled out)

Raw fetch of `https://raw.githubusercontent.com/affaan-m/ecc/main/CLAUDE.md` returned the file. Key extracts + analysis:

**ECC self-description:** "This is a Claude Code plugin - a collection of production-ready agents, skills, hooks, commands, rules, and MCP configurations."

**Architecture (verbatim):**
- `agents/` — planner, code-reviewer, tdd-guide, etc.
- `skills/` — Workflow definitions and domain knowledge (coding standards, patterns, testing)
- `commands/` — `/tdd`, `/plan`, `/e2e`, `/code-review`, `/build-fix`, `/learn`, `/skill-create`
- `hooks/` — JSON with matcher conditions
- `rules/` — Always-follow guidelines (security, coding style, testing requirements)
- `mcp-configs/` — MCP server configurations
- `scripts/` — Cross-platform Node.js utilities
- `tests/` — Test suite

**Direct comparison to vault:**

| Dimension | ECC | Vault |
|---|---|---|
| Hook runtime | JSON matcher + Node.js scripts | Python scripts (40+ hooks) |
| Skill schema | "When to Use / How It Works / Examples" | "Use-when / Do-NOT-use-when / Gotchas / Steps" |
| Commands focus | Software-engineering workflows (TDD, E2E, build-fix) | Process-primitive routing (process-research, process-build, task-classifier) |
| Doctrine layer | Defensive (prompt injection + dev conventions) | Operational (5 process primitives, CRITICAL RULEs, 50+ memos) |
| Test infrastructure | `tests/run-all.js` + per-component tests | None — work-verification-check.py hook is the closest analog |
| Skill placement | Curated in `skills/`; imports to `~/.claude/skills/` | All skills under `.claude/skills/` (no global/local split) |
| Memory model | Implicit (`/learn` skill extracts patterns from sessions) | Karpathy LLM-Wiki + qmd MCP + `memory/` folder |

**Conflict zones if full plugin install attempted:**
1. **Dual hook runtime** — ECC's Node.js + vault's Python both wired to same events. Either deduplication chaos or one runtime silently shadowed.
2. **Skill schema mismatch** — ECC's "When to Use" sections wouldn't follow vault's `task-classifier → process-* → Skill tool` dispatch chain. Bypasses the classifier-gating discipline that the framework rests on.
3. **Command namespace collision** — ECC's `/plan` would shadow vault's `process-planning` invocation patterns. `/code-review` may shadow vault's architect-reviewer dispatch.
4. **Skill-placement convention difference** — `~/.claude/skills/` global vs vault's `.claude/skills/` project-local creates a two-source ambiguity.

### Updated recommendation (post-verification)

**Stay with (C) architectural read-only inspiration.** Verification confirms:
- Stars are real (worth examining as a serious project) ✓
- Doctrine is substantively different (full install would conflict) ✓
- Architecture has cherry-pickable patterns (specific commands like `/learn`, `/skill-create`, `/tdd` are interesting; the `tests/` discipline is interesting; the JSON-matcher hook schema is NOT a fit for vault's Python+settings.local.json approach) ✓

**Concrete next actions if Wiktor wants to act on this:**

1. **Cherry-pick candidate: `/learn` command** — ECC's pattern-extraction-from-sessions skill conceptually overlaps with vault's manual `feedback_*.md` writing. Worth studying ECC's implementation to see if vault's pipeline can be sharpened.
2. **Cherry-pick candidate: `/skill-create` command** — "Generate skills from git history" is a discovery vault doesn't have. Worth a focused investigation.
3. **Cherry-pick candidate: ECC's `tests/` discipline** — vault has no test framework today (architect-review CR3 flagged this at SA-5 layer). ECC's per-component test pattern is a transferable structure even if the test runners differ.
4. **NOT-recommended cherry-pick: hooks/** — Node.js + JSON matcher conflicts with vault's Python + settings.local.json. The hook-event coverage is interesting as reference, but porting individual hooks doesn't work.

Wiktor decision: which (if any) of the 3 cherry-pick candidates to investigate further? Or close ECC investigation with this verification supplement as the durable record?
