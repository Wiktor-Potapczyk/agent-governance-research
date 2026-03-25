# Quality Mechanism Spectrum: From Harmful to Robust

## The Finding

LLM reasoning quality mechanisms form a spectrum from actively harmful to architecturally robust. Empirically grounded by 85 academic references (2023-2026).

## The Spectrum

| Level | Mechanism | Verdict | Key Evidence |
|-------|-----------|---------|-------------|
| 1 | "Think again" / "Are you sure?" | **Harmful** | Huang et al. ICLR 2024: -0.8 to -37.7 points. CommonSenseQA collapsed from 75.8 to 38.1 |
| 2 | Single Socratic self-check | **Unreliable for LLMs** | Sycophancy flip rates up to 98%. Adversarial self-review scored 0.15 confidence |
| 2.5 | Condition-masked verification (ProCo) | **Promising** | Wu et al. EMNLP 2024: +6.8 to +14.1 across tasks |
| **3** | **Step-level verification (CoVe)** | **Effective for reasoning** | Dhuliawala: 2x precision, 77% hallucination reduction. Degrades with same-model repetition |
| 3+ | CoVe with external oracle | **Effective when available** | External verifier transforms self-correction from harmful to effective |
| 3.5 | Cross-family verifier | **Best but unavailable** | Lu et al. 2025: cross-family significantly outperforms self-verification |
| **4** | **Blind parallel ensemble** | **Effective for framing** | Debate debunked (<20% win rate). Blind parallel confirmed. 35% unique divergence |
| 5 | Multi-agent debate | **Harmful for strong models** | Wynn et al. 2025: agents flip correct to incorrect. More rounds can reduce accuracy |

## Critical Constraints

- **One round only** for same-model verification — chaining degrades quality (Lu et al. 2025)
- **CoVe for reasoning, ensemble for framing** — they serve different purposes and should not be substituted
- **Strong models benefit less** from all multi-agent approaches (SelfOrg 2026)
- **External verification** (execute code, search facts) is more reliable than any self-verification

## The Condition-Masking Insight

The most promising mechanism at Level 2.5 — ProCo — works by asking the model to re-derive an answer "without referencing your original reasoning." This breaks the self-reinforcement loop. The key: force independent derivation, not reconsideration of the same reasoning.

## Application

Match the mechanism to the task, not the other way around:
- Math/logic with verifiable steps → CoVe (Level 3)
- Framing/design/architecture → Blind ensemble (Level 4)
- Factual claims → External verification (Level 3+)
- Subjective judgment → CoVe + Ensemble combined
- Routine/clear tasks → None (mechanisms add overhead without value)
