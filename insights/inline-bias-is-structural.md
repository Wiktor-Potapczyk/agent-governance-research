# Inline Bias Is Structural and Prompt-Unfixable

## The Finding

LLMs default to answering inline (continuing text generation) rather than using tools or delegating to specialists. This is not a prompting failure — it is a structural property of autoregressive generation. The bias is measured, persistent, and not fixable by adding rules.

## Evidence

- **12.4%** of multi-agent failures are reasoning-action mismatch — the model reasons correctly that it should delegate, then answers inline anyway (MASFT, arXiv:2503.13657)
- **78.5%** persistence rate — once inline behavior starts in a response, it locks in for the rest of the turn (SycEval, arXiv:2502.08177)
- Tool-usage-gap research explicitly answered "Fixable by prompting? No" for ALL identified root causes
- Adding more rules makes it WORSE — rule saturation, Lost in the Middle effect, instruction competition

## What Works

| Intervention | Effect | Why |
|-------------|--------|-----|
| Deterministic hooks | 25% → 90% activation | Fires regardless of LLM compliance |
| Tool restriction | Structurally prevents inline | Different agents have different tool sets |
| Blind analysis rule | Removes sycophancy target | No hypothesis = nothing to agree with |
| Condition-masking questions (ProCo) | +6.8 to +14.1 | Forces re-derivation via questions |
| Rejection-permission framing | +60% | Grants explicit permission to NOT answer inline |

## What Doesn't Work

| Intervention | Why it fails |
|-------------|-------------|
| Anti-sycophancy prompts | ~10pp improvement at best — model agrees with its own anti-sycophancy text |
| More rules in system prompt | Makes problem worse — rules compete for attention |
| Self-confidence reporting | Miscalibrated and sycophantic |
| "Think again" / naive self-correction | GSM8K: 75.9→74.7. Actively harmful. |
| Multi-agent debate | <20% win rate over chain-of-thought |

## The Design Principle

Wrap the unpredictable function (LLM reasoning) in deterministic infrastructure (hooks, tool restrictions). Don't try to make the LLM behave correctly — make it impossible to behave incorrectly at the structural level.
