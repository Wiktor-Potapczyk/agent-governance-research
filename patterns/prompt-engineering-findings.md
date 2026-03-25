# Prompt Engineering Research Findings

Key findings from a structured research loop on prompt engineering for Claude-family models, directly affecting agent prompt design. These findings are sourced from academic papers and official vendor documentation.

## Anti-Patterns for Current Claude Models (Anthropic Official)

- Do NOT use all-caps or "CRITICAL: You MUST..." — current models overtrigger. Use normal language.
- Do NOT use negative instructions ("do not X") — state the desired behavior instead.
- Do NOT over-prompt for thoroughness — current Claude models are already proactive; dial back aggressive guidance.

## System Prompt Structure

- Critical instructions buried in the MIDDLE of long prompts are underweighted (U-shaped curve, Liu et al. TACL 2024).
- Most important directives should be at the BEGINNING or END.
- Explain the "why" behind rules — Claude generalizes from the explanation.
- For subagents: each prompt must be FULLY SELF-CONTAINED — no parent context is inherited.
- Embed effort scaling rules explicitly in subagent prompts (agents cannot judge effort on their own).

## Role/Persona Prompting

- Task-relevant roles DO improve reasoning accuracy (Kong et al. NAACL 2024) — effect is real.
- Persona-heavy system prompts reduce instruction-following by up to 8.2% (arXiv:2512.14754).
- Anthropic: role assignment improves behavioral focus and tone, NOT accuracy.
- Keep role assignments minimal and task-relevant. Elaborate persona = worse instruction-following.

## Anti-Sycophancy — Instruction Prepending Is Unreliable

- ELEPHANT paper (2025): instruction prepending for sycophancy produces "either drastically low or high rates" — erratic, not calibrated.
- The most documented runtime intervention: combined rejection-permission + factual-recall (94% rejection rate in medical context).
- Larger models and instruction tuning INCREASE sycophancy (Google paper).

## Few-Shot Examples

- Exemplar ordering matters — avoid recency bias (alternate positive/negative).
- Example quality > quantity.
- Few-shot CoT consistently outperforms zero-shot for reasoning tasks (consensus across all sources).
