---
date: 2026-04-19
tags: [#insight, #hooks-as-governance, #observability, #sidecar-files]
status: #active
purpose: Document the sidecar-file enforcement pattern used to close the post-compaction governance blind spot in Claude Code hooks
---

# Sidecar Files for Post-Compaction Enforcement

## The finding

When a governance hook enforces a dispatch contract by reading the conversation transcript, the contract can fall outside the hook's read window after context compaction. The hook then silently exits, bypassing enforcement. Placing a machine-readable contract file beside the human-readable skill specification — and having the hook read that file as a fallback — closes the bypass without changing the contract's source of truth.

Three components make the pattern work:

1. **Sidecar file** (`DISPATCHES.json`) next to the skill's `SKILL.md`, mirroring the prose contract in structured form.
2. **Fallback activation** in the hook — triggered only when the transcript scan yields no contract but a skill invocation is detected.
3. **Terminal-skill exclusion** — skills with empty mandatory contracts (like `process-qa`, `process-pentest`) must not overwrite the "current skill" tracker, or they silently nullify enforcement for earlier skills in the same session.

## The problem

The vault's `dispatch-compliance-check.py` hook (a Stop hook) reads the last 200 KB of the conversation transcript to find a classification block containing `MUST DISPATCH: [...]`. It then verifies that every declared skill and agent was actually invoked via the Skill or Agent tools during the turn. If items are declared but not dispatched, the hook blocks the turn.

After Claude Code compaction — where earlier messages are summarized — the classification block may no longer be in the 200 KB window. The hook's scan returns no contract. Its logic then does:

```python
if not found_contract:
    return
```

This is a silent bypass. Every turn that ran through compaction has no dispatch enforcement. The hook runs, finds nothing, and exits clean.

The bypass was documented as audit finding **H11** on 2026-04-18. A proof of concept was built the same day (a sidecar loader reading `DISPATCHES.json` beside `SKILL.md`) but not wired into the hook. That wiring is what 2026-04-19's H11 integration shipped.

## The fix

Three surgical edits to `dispatch-compliance-check.py` and five new `DISPATCHES.json` files.

### Hook edits

1. **Import the sidecar loader with graceful fallback.**
   ```python
   _HOOK_DIR = os.path.dirname(os.path.abspath(__file__))
   if _HOOK_DIR not in sys.path:
       sys.path.insert(0, _HOOK_DIR)
   try:
       from sidecar_loader import mandatory_agent_names
       _SIDECAR_AVAILABLE = True
   except ImportError:
       _SIDECAR_AVAILABLE = False
   ```

2. **Unconditional tool-use tracking.** The old code tracked dispatched agents only after `found_contract = True`. The new code tracks a parallel `all_dispatched` set (every Skill and Agent invocation, regardless of contract state) plus a `recent_process_skill` pointer (last-seen `process-*` invocation).

3. **Post-loop fallback block.** When the scan yields no contract but a process skill was invoked, the hook loads the skill's sidecar and treats its `mandatory_dispatches` as the contract:

   ```python
   if not found_contract and recent_process_skill and _SIDECAR_AVAILABLE:
       sidecar_mandatory = mandatory_agent_names(recent_process_skill)
       if sidecar_mandatory:
           must_dispatch = sidecar_mandatory
           dispatched = set(all_dispatched)
           found_contract = True
           task_type_str = "sidecar-fallback"
           # ... emit h11_sidecar_fallback_activated event ...
   ```

### Sidecar files

Six process skills each get a `DISPATCHES.json` file next to their `SKILL.md`. Schema example for `process-planning`:

```json
{
  "schema_version": 1,
  "skill": "process-planning",
  "mandatory_dispatches": [
    {"name": "implementation-plan", "role": "step-3-design", "required": true},
    {"name": "architect-reviewer",  "role": "step-4-review", "required": true},
    {"name": "adversarial-reviewer","role": "step-4-parallel-review", "required": true}
  ],
  "conditional_dispatches": [...],
  "allowed_specialists_via_process_exemption": [...]
}
```

Terminal skills (`process-qa`, `process-pentest`) have empty mandatory lists. They verify; they do not orchestrate.

## The subtlety — terminal-skill exclusion

An adversarial review of the fallback surfaced a real defect. The initial design tracked `recent_process_skill` as a simple "last seen" value: whichever process skill was invoked most recently in the window wins. That breaks when a session invokes two process skills in sequence:

- `process-planning` runs → dispatches planning's three mandatory agents → `recent_process_skill = "process-planning"`.
- `process-qa` runs next → `recent_process_skill = "process-qa"`.
- Hook fires at Stop → fallback loads `process-qa`'s sidecar → empty mandatory list → fallback condition `if sidecar_mandatory:` is false → falls through to `if not found_contract: return` → silent pass.

Planning's mandatory list is never checked. The enforcement gap H11 was meant to close reopens in any session that ends with a terminal skill invocation. Exploitable intentionally by running `process-qa` as the last invocation to nullify any earlier enforcement.

The fix is one line in the tracking block:

```python
if dispatched_name and (
    dispatched_name.startswith("process-")
    or dispatched_name == "task-classifier"
) and dispatched_name not in ("process-qa", "process-pentest"):
    recent_process_skill = dispatched_name
```

Terminal skills never overwrite the tracker. The last non-terminal skill wins, and its contract is the one the fallback enforces.

## Why this is a generalizable pattern

### Prior art — the sidecar file contract

Five well-known systems pair a machine-readable file with a human-readable spec as the enforcement ground truth:

1. **pre-commit framework** — `.pre-commit-config.yaml` sits beside human documentation; the pre-commit binary carries no state, the file is the contract.
2. **Conftest / OPA Rego** — `.rego` policy files are loaded at evaluation time; the file is the binding contract regardless of what the running process "remembers."
3. **Terraform state** — `terraform.tfstate` is the canonical source of truth for what infrastructure exists; the CLI re-reads it on every invocation.
4. **Microsoft agent-governance-toolkit** — YAML policy files are the enforcement contract for AI agent governance; the sidecar container reads the config at startup.
5. **Claude Code `CLAUDE.md` re-injection** — enforcement instructions in `CLAUDE.md` rather than conversation history, re-injected every turn so they survive compaction.

All five share structure: a file beside the primary artifact carries the machine-readable contract; the enforcement mechanism reads the file rather than relying on runtime or in-memory state.

### Prior art — post-compaction state externalization

Terraform's remote state file is the clearest infrastructure analog: contract always on disk, CLI stateless between runs, process loss doesn't destroy the contract. CI/CD pipelines mirror this — GitHub Actions caches, GitLab CI artifacts — to survive job boundaries.

In LLM agent frameworks the picture is less mature. LangGraph offloads large tool results to the filesystem, but this is a token-budget optimization, not enforcement-contract preservation. CrewAI's `respect_context_window` boolean triggers summarization that destroys the original. No framework surveyed stores enforcement contracts (i.e., "this skill requires these dispatches") as a persistent file re-read by hooks after compaction.

### What is actually novel

The specific combination — hook-based dispatch enforcement + per-skill JSON sidecar as fallback when conversation history is compacted + terminal-skill exclusion to prevent state-tracker overwrite nullification — does not appear in the public literature, tooling repositories, or framework documentation surveyed. The constituent parts all have precedent; the assembly as an enforcement mechanism within an AI agent orchestration context does not.

The terminal-skill exclusion specifically is the sharpest novel element. Sidecar-file contracts and file-based fallback are established patterns. Recognizing that "verifier skills must not overwrite orchestrator skills in a fallback tracker" is a design move without a direct analog in the systems surveyed.

## Evidence

- **Audit finding:** `work/infra-audit-2026-04-18/s6-synthesis.md` — H11 documented the post-compaction enforcement blind spot.
- **POC (2026-04-18):** `hooks/sidecar_loader.py` + `skills/core/process-build/DISPATCHES.json` shipped as reusable loader + one sidecar.
- **Integration (2026-04-19):** `hooks/dispatch-compliance-check.py` edited to call `mandatory_agent_names()` on fallback + 5 new sidecars for the remaining process skills.
- **Adversarial review:** 7/8 questions CLEAN, 1 real defect (Q4 — terminal-skill overwrite) found and fixed inline.
- **Behavioral tests:** 4/4 synthetic-transcript tests PASS — fallback fires on missing mandatory dispatches (BLOCK); Quick-like session silent pass; existing contract-present path unchanged; planning-then-qa regression test confirms Q4 fix holds.

## Sources consulted

- [pre-commit/pre-commit-hooks](https://github.com/pre-commit/pre-commit-hooks)
- [conftest.dev](https://www.conftest.dev/) / [open-policy-agent/conftest](https://github.com/open-policy-agent/conftest)
- [Gruntwork — How to manage Terraform state](https://blog.gruntwork.io/how-to-manage-terraform-state-28f5697e68fa)
- [microsoft/agent-governance-toolkit](https://github.com/microsoft/agent-governance-toolkit)
- [Middleware vs Sidecar — two ways to govern AI agents (DEV)](https://dev.to/fl7_93dc7dc638d86979/middleware-vs-sidecar-two-ways-to-govern-ai-agents-2pcb)
- [Context compaction in agent frameworks (DEV)](https://dev.to/crabtalk/context-compaction-in-agent-frameworks-4ckk)
