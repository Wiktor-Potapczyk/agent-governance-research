# Cross-Model Validation Requirement

When testing AI agent behaviors (classification accuracy, reasoning quality, compliance rates), testing on a single model family masks shared biases. If Claude classifies 18/18 correctly, is that because the classification system works or because Claude shares the same priors as the classification prompt (which was also written by Claude)?

## Evidence

- Classifier experiment: 8 agents x 4 prompt variants produced unanimous TYPE agreement. Could not distinguish "robust classification" from "shared family bias."
- Inline bias research: 12.4% reasoning-action mismatch was measured on Claude. Whether GPT or Gemini show the same pattern (structural autoregressive bias) or different patterns (different training) is unknown.
- Adversarial review scored 0.15 reliability — same-model adversarial review produces performative disagreement, not genuine challenge.

## The Requirement

Before claiming a finding is universal (applies to LLM agents in general, not just Claude):

1. **Test on at least one model from a different family** — GPT, Gemini, Llama, etc.
2. **If results converge** — the finding is likely about LLM architecture, not model-specific training
3. **If results diverge** — the finding is model-specific and should be labeled as such
4. **Document which models were tested** — a finding validated on Claude + Gemini is more credible than one validated on Claude alone

## What We Know

- Gemini confirmed the novelty of exploration vs extraction prompting (external validation of the concept, not the quantitative results)
- Same-model CoVe degrades with repetition (Lu et al. 2025) — cross-family is better but we haven't implemented it
- The 78.5% inline bias persistence number is Claude-only — no cross-model data

## Practical Limitation

Cross-model testing requires API access to multiple providers and equivalent prompting. For a solo operator, this is expensive. The pragmatic approach: label single-model findings honestly and invite cross-model validation as a contribution opportunity.
