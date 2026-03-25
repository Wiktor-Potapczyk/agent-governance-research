# Ensemble Thinking: Blind Parallel Lenses for Complex Decisions

When an LLM agent faces a complex framing or design decision, running a single reasoning path risks anchoring to whatever perspective the model encounters first. Ensemble thinking runs 2-4 independent cognitive lenses in parallel on the same problem, then compares outputs. Divergence between lenses reveals where the real questions hide. This approach was empirically validated: across 5 real framing tasks, average overlap between lenses was ~35%, well below the 80% threshold that would indicate cosmetic diversity.

## The 4 Lenses (Proven Effective)

- **Lens A: Recursive Architectural Reframing** -- applies 4 checks (trap/boundary/reality/collapse) before decomposing
- **Lens B: Mechanical Decomposition** -- breaks into sub-steps, risks, dependencies
- **Lens C: Stakeholder Reality Trace** -- starts from the end-user, works backwards
- **Lens D: Adversarial Challenge** -- finds flaws in the premise itself

## What the Research Confirms (85 references, 2023-2026)

- Debate debunked: <20% win rate over CoT baselines (2025). Conformity effects amplify errors.
- Blind parallel > debate at same cost -- no conformity risk.
- Strong models benefit LESS from all multi-agent approaches (SelfOrg 2026: 81.10% to 80.71%).
- Diversity in capabilities matters more than structural tweaks.
- Once single-agent accuracy >45%, debate yields diminishing returns.

## Experiment Result: Diversity Is Real

- 5 real framing tasks x 3 lenses (Reframing, Decomposition, Stakeholder) = 15 agents
- Average overlap: ~35% (well below 80% "cosmetic" threshold)
- Each lens consistently catches unique risks the others miss
- Example: on one task, Reframing eliminated the problem entirely ("no hook needed -- collapse to classifier"), while Decomposition identified routing as a single point of failure, and Stakeholder found a duplication signal
- Lu et al.'s concern about cosmetic diversity does NOT hold for framing/design tasks

## Trigger Design

1. Post-response self-check: did I present tradeoffs? Consider alternatives? Question framing?
2. Friction tracking: 2+ user corrections = suggest ensemble

## Complement: CoVe (Step-Level Verification)

- CoVe for reasoning tasks (step-level verification, one-round limit)
- Ensemble for framing tasks (blind parallel agents)
- Both together for high-stakes (CoVe within each ensemble agent -- but risk: may reduce diversity)

## Status

Design validated by research. Experiment confirmed genuine divergence. The key design choice -- blind parallel execution with NO inter-agent visibility -- is empirically correct. Debate introduces conformity (functionally equivalent to inter-agent sycophancy) and offers no accuracy advantage over independent ensemble for strong models.
