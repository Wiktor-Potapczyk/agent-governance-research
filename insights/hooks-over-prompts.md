# Hooks > Prompts for Governance

## The Finding

Deterministic hook enforcement beats soft prompt instructions by 3.6x for governance compliance. Hooks fire regardless of whether the LLM follows instructions. Prompt rules decay within minutes in fresh sessions.

## Evidence

- **Before hooks:** 25% skill activation rate from system instructions alone
- **After UserPromptSubmit hook:** 90% skill activation — the hook fires on every message and injects a reminder
- **IMPLIES field:** Dropped within minutes during a long autonomous loop despite MANDATORY language in the skill definition. Hook reminder restored it.
- **Epistemic-check hook (oracle attempt):** Tried to use a hook to judge output quality — never blocked once. Failed because hooks can verify compliance (did you follow the process?), not correctness (is the output right?).

## The Paradigm

Hooks are not debugging utilities — they are the organizational nervous system. In Claude Code, hook events cover the entire interaction lifecycle: session start, user input, pre/post tool use, subagent start/stop, compaction, session end. That's a complete governance infrastructure.

**The reframing:** Instead of "which hook should we add to fix a behavior," ask "what kind of organization are we building, and which hooks implement its governance?"

## The Critical Distinction

**Hooks verify compliance, not correctness.**

A wrong result from a full process pipeline is more informative than a wrong result from a shortcut. The pipeline leaves a visible trail — every decision exposed. The error correction mechanism is the human, but hooks ensure the data exists to do it.

When a hook tried to judge correctness (epistemic-check using a cheap model), it rubber-stamped everything. Compliance checking works. Oracle checking doesn't.

## The Design Principle

If a rule is restated twice because the LLM keeps forgetting it, it belongs in a hook, not in a prompt. System instructions are guidance for mid-response reasoning. Hooks are enforcement for structural compliance. Build governance on the mandatory infrastructure, not the advisory one.
