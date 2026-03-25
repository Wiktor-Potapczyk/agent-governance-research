# The Quality Mechanism Spectrum: CoVe, Ensemble, and Everything Between

LLM agent systems need quality mechanisms -- ways to catch errors in reasoning before they propagate into action. Not all mechanisms are equal. Some are actively harmful, some help with specific task types, and only a few are empirically validated across broad conditions. This document presents a graded spectrum of quality mechanisms, ranked by evidence strength and applicable domain, derived from 85+ references spanning 2023-2026 literature.

## The Spectrum

| Level | Mechanism | Works for | Fails for | Cost | Evidence |
|-------|-----------|----------|-----------|------|----------|
| ~~1~~ | "Think again" / "Are you sure?" | NOTHING -- actively harmful | Everything | Free | Huang et al. (ICLR 2024): -0.8 to -37.7 points. CommonSenseQA: 75.8 to 38.1 catastrophic collapse. |
| ~~2~~ | Single Socratic question | Humans only | LLMs (sycophancy up to 98% flip rate) | Free | Adversarial review: 0.15 confidence. Prompt-level mitigation: ~10pp at best. |
| **2.5** | Condition-masked verification (ProCo) | Arithmetic, commonsense, open-domain QA | Untested on complex/framing tasks | ~$0.01 | ProCo (Wu et al., EMNLP 2024): +6.8 to +14.1 across tasks. |
| **3** | **CoVe / SSR (step-level verification)** | Logic, math, factual claims | Knowledge-heavy tasks (MMLU/GPQA). Degrades with same-model repetition. | ~$0.01-0.05 | Dhuliawala: 2x precision, 77% hallucination reduction. SSR: ~68%. **Lu et al. 2025: gains decrease with solver/verifier similarity.** |
| **3+** | CoVe with external oracle | Code, math, verifiable facts | Tasks without external ground truth | Low-med | SCORE (Zhang et al.): external verifier transforms correction from harmful to effective. |
| **3.5** | CoVe with cross-family verifier | All reasoning | Requires access to a different model family | Medium | Lu et al. 2025: cross-family >> self-verification. Cobbe et al.: 6B verifier > 175B generator. |
| **4** | **Blind architectural ensemble** | Framing, design, architecture | Routine/clear tasks. Same-model ceiling unknown. | ~$1.15 | Debate debunked: <20% win rate. Blind parallel confirmed. SelfOrg 2026: negative for strong models on clear tasks. |
| ~~5~~ | Multi-agent debate | Weak models only (<45% baseline) | Strong models -- conformity effects, sycophancy amplification | ~$2-5 | Wynn et al. 2025: agents flip correct to incorrect. More rounds can reduce accuracy. |

## The Verification Prompt (Implemented as a Reusable Skill)

```
For each major reasoning step above:
1. Rate your confidence (high / medium / low).
2. For each step rated medium or low:
   a. State the step's core claim in one sentence.
   b. Without referencing your original reasoning, independently derive
      whether that claim holds. Show your work from first principles.
   c. If your independent derivation contradicts the original step,
      flag the contradiction explicitly and revise.
3. After all verifications, check whether any revision requires
   changes to downstream steps. Propagate if needed.
```

## Critical Constraints

- **ONE ROUND ONLY** -- never chain CoVe self-verification (Lu et al. 2025: degrades)
- **NOT for knowledge tasks** -- verification requires same knowledge as generation
- **Route by task type**: a task classifier's MECHANISM field can route to CoVe/Ensemble/External/None automatically

## How to Apply

The MECHANISM field in a task classifier determines which quality mechanism fires:
- **CoVe** = invoke step-level verification
- **Ensemble** = blind parallel agents with different cognitive lenses
- **External** = execute code, run tests, or search for ground truth
- **None** = single agent, no mechanism (routine tasks where the model's baseline accuracy is sufficient)
