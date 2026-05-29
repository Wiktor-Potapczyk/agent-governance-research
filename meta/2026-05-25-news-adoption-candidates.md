---
date: 2026-05-25
tags: [project/agent-governance-research, research, analysis]
status: active
---

> Adapted from internal research workspace. Cross-references to vault-internal artifacts have been stripped or genericized.

# News Adoption Investigation — 2026-05-25

Tier-2 deliverable from overnight loop ITER 6+, per Wiktor injection "if you are out of ideas, then go through the news and at least investigate what we can adopt or delve into more."

## Summary table

| # | Item | Verdict | One-line why |
|---|------|---------|--------------|
| 1 | agentmemory MCP | SKIP | Vault already has a superior stack (qmd BM25+vector + 333 file-based memory); agentmemory is a SQLite/embedding solution for sessions that have no persistent memory at all |
| 2 | task-observer | INVESTIGATE FURTHER | Mechanism (file-based observation logs + proposed updates) is compatible with hooks discipline, but auto-approval is a compliance risk requiring a closer read |
| 3 | Tom Dörr 106 skills | INVESTIGATE FURTHER | Repo not locatable on his GitHub profile under any skills filter; verify URL via W21 brief email link before evaluating content |
| 4 | Cache-miss 12.5x | ADOPT | 5 triggers fully enumerated from official docs; two directly hit the vault's overnight-loop pattern; actionable mitigations available now |
| 5 | Anthropic self-hosted sandboxes | SKIP | Both features require Anthropic's Managed Agents platform; tool execution is irrelevant to CLI-only Claude Code; MCP tunnels are research-preview with no self-hosted compute path |

---

## Per-item findings

### 1. agentmemory MCP

- **Verified URL:** https://github.com/rohitg00/agentmemory — 17.3k stars, Apache-2.0, v0.9.21 released 2026-05-19. 51 MCP tools, SQLite + in-memory vector index, auto-capture via 12 lifecycle hooks, 4-tier memory consolidation. 95.2% R@5 on LongMemEval-S.
- **What it solves:** sessions that start cold with no memory. Injects relevant compressed context from prior sessions.
- **Fit with current setup:** the vault already has qmd (BM25 + vector retrieval, 347 docs / 2 collections) plus 333 one-fact files providing structured persistent memory. agentmemory's value proposition is precisely what qmd + the file layer already covers — and the vault's approach is more structured (typed frontmatter, topic files, MEMORY.md index) vs agentmemory's unstructured observation compression. Running both would create a parallel, diverging memory substrate with no clear owner. No meaningful capability gap to fill.
- **Verdict: SKIP** — vault memory infrastructure is already mature and differentiated. agentmemory adds nothing that qmd + file-based layer doesn't provide; running both creates maintenance overhead.

---

### 2. task-observer (one-skill-to-rule-them-all)

- **Verified URL:** https://github.com/rebelytics/one-skill-to-rule-them-all — 585 stars, CC BY 4.0. Watches work sessions, writes observation logs to `skill-observations/`, proposes skill updates to `skill-updates/`. Self-reported: 600 improvements across 40 skills in 3 months.
- **What it does:** monitors corrections and gaps during sessions; proposes new skills and incremental updates to existing ones. Updates are proposed, not auto-applied — human review step exists.
- **Fit with hooks discipline:** CLAUDE.md Working Philosophy principle #2 states hooks achieve ~90% compliance vs ~25% for soft instructions. task-observer operates in the soft-instruction space (proposed updates, no enforcement). It surfaces patterns for manual promotion to hooks — but does not generate hooks itself. The human-in-loop review gate preserves the principle; the risk is that proposed-but-not-yet-hooked improvements sit inert in `skill-updates/` indefinitely (the ~25% compliance problem task-observer does not solve).
- **Open question:** does the observation log mechanism work when Claude Code's hooks are active simultaneously? No evidence of incompatibility but untested.
- **Verdict: INVESTIGATE FURTHER** — the proposed-updates flow is compatible in principle. Worth a 1-session pilot to verify: (a) observation log quality on vault-specific tasks, (b) whether proposed updates ever cross the threshold to become hooks, (c) no interference with the 44-hook enforcement layer. Do not adopt wholesale; pilot on one skill first.

---

### 3. Tom Dörr 106 Claude Code skills

- **Verification attempt:** GitHub profile `github.com/tom-doerr` (294 repos) — no repository matched a search for "skills" on his repositories tab. The 6 pinned repos are ZSH/Vim/codex tooling, none skills-related. W21 brief sourced this from an email link (Gmail internal) that cannot be WebFetched.
- **What the brief claims:** community catalogue spanning 15 professions, worth treating as a survey of skill-shape patterns for n8n automation, observability, and agent governance.
- **Adjacent skills confirmed in broader ecosystem:** the `awesome-claude-skills` catalogues (ComposioHQ, travisvn, BehiSecc) aggregate dozens of professions. Most relevant to this vault: automation/n8n, observability, research-assistant, and developer-workflow categories exist across community repos. The specific Dörr catalogue may be a fork or short-lived repo not surfacing in searches.
- **Verdict: INVESTIGATE FURTHER** — the W21 email link (Gmail) is the only path to the actual repo. Open that link manually, confirm the URL, then evaluate the 3-5 most vault-adjacent skills. Do not spend research time on the ecosystem catalogues as a proxy — they are not the cited source.

---

### 4. Cache-miss 12.5x finding

- **Source confirmed:** https://code.claude.com/docs/en/prompt-caching (official Anthropic Claude Code docs).
- **5 enumerated cache-invalidation triggers:**
  1. **Model switch** (`/model`) — each model has its own cache; switching resets from zero even with identical content. The `opusplan` setting triggers a switch on every plan-mode toggle.
  2. **MCP server connect/disconnect** — tool definitions sit in the system prompt layer; any change to the MCP tool set (server exits, HTTP session expires, auto-reconnect, dynamic tool update) invalidates everything.
  3. **Denying an entire tool** — bare tool deny rules (`Bash`, `WebFetch`, or `Bash(*)`) remove the tool from context entirely, invalidating the system prompt layer.
  4. **Compaction** (`/compact`) — replaces message history with a summary; invalidates conversation layer by design. The summarization call itself reuses the existing cache, so the cost is in the post-compaction rebuild, not the compact operation itself.
  5. **Claude Code upgrade** — new versions update the system prompt or tool definitions; first turn after upgrade rebuilds from scratch. Auto-update applies on next launch, not mid-session.
- **Cross-reference with vault overnight-loop pattern:** the loop pattern runs sustained multi-agent dispatches with subagents. Two triggers directly apply: (a) subagents use the 5-minute TTL even on a subscription (main session gets 1-hour TTL), so any subagent that idles > 5 minutes between turns rebuilds its cache; (b) if the loop uses `opusplan` for plan-mode toggling, each toggle is a model switch costing a full cache miss. The compaction trigger is also relevant — auto-compaction mid-loop invalidates the conversation layer at an unpredictable moment.
- **Actionable mitigations:** (a) pick model once at session start, avoid mid-loop `/model` calls; (b) connect all MCP servers before the first turn; (c) run `/compact` at deliberate break points, not mid-task; (d) for overnight loops, the 1-hour subscription TTL protects the main session cache through normal idle gaps — subagents do not inherit this, so keep subagent turns tight.
- **Verdict: ADOPT** — no build required. Update the loop-design checklist in the overnight-loop queue template with the 3 actionable mitigations above. The `/rewind` insight (truncates back to a cached prefix, no rebuild) is also worth noting: prefer `/rewind` over inline correction when a branch has gone wrong mid-loop.

---

### 5. Anthropic self-hosted sandboxes + private MCP tunnels

- **Source:** https://claude.com/blog/claude-managed-agents-updates. Self-hosted sandboxes in public beta; MCP tunnels in research preview (access by request).
- **What it actually is:** both features are part of the **Claude Managed Agents** platform — the orchestration loop stays on Anthropic's infrastructure; only tool execution (sandboxes) or MCP routing (tunnels) moves to the customer's perimeter. This is an API/managed-platform feature, not a Claude Code feature.
- **Environment constraints:** the target environment has WDAC application control blocking unsigned binaries, CPU virtualization disabled (no Docker/WSL2/Hyper-V/containers), and NDA constraints. The supported sandbox providers (Cloudflare, Daytona, Modal, Vercel) all require cloud-hosted compute — none are bare-metal Windows-only paths. Self-hosted sandboxes with a bring-your-own client would still require a container runtime or VM, both unavailable. MCP tunnels require deploying a "lightweight gateway" process — feasible in principle (pure Node or Python), but the feature is research-preview only and requires requesting access.
- **Verdict: SKIP** — both features target the Managed Agents API surface, not Claude Code CLI workflows. The sandbox providers all assume container runtimes unavailable in this environment. MCP tunnels are research-preview with an access-request gate. Neither addresses a current vault gap.

---


## Cross-cutting observations

- The W21 brief's open-source memory and skills items (agentmemory, task-observer, Dörr skills) all assume the *absence* of an existing memory/skills infrastructure. This vault has both, which flips the evaluation: the relevant question is not "does this solve a problem?" but "does this solve a problem the vault doesn't already solve?"
- Cache-miss item is the only one yielding immediate, no-build, no-risk value — it converts a cost-model understanding gap into 3 concrete loop-design rules.
- The Anthropic enterprise features (sandboxes, MCP tunnels) are directionally interesting but structurally blocked by the Windows enterprise environment for the foreseeable future; worth re-evaluating if the virtualization constraint changes.
