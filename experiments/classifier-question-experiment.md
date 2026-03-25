# Classifier Question Experiment

How different forced reasoning questions affect LLM task classification accuracy. Tested 4 question variants to find the best pre-classification step for an AI agent routing system.

## Setup

5 parallel agents, each with identical classifier logic plus one question variant (or baseline with no question). Each classified 6 ambiguous prompts: 3 external tasks + 3 meta/continuation directives.

## Variants Tested

| Variant | Question | Design Rationale |
|---------|----------|-----------------|
| Baseline | (none) | Control — classifier with no forced reasoning |
| Q1 | "Name the single best specialist agent for this task, or NONE" | Agent registry awareness — forces consideration of delegation |
| Q2 | "If you handle this inline and it turns out wrong, what would you have missed?" | Premortem reasoning — ProCo / loss aversion pattern |
| Q3 | "Is this a new task or a directive about the current work?" | Meta-awareness — distinguishes task from continuation |
| Q4 | "What does this prompt imply?" | Open implication — forces engagement with meaning |

## Results

All 5 variants (including baseline) classified 6/6 correctly as Analysis or Research. Zero Quick misclassification.

| Variant | Accuracy | Depth of reasoning | Upgrades detected |
|---------|----------|-------------------|-------------------|
| Baseline | 6/6 | Shallow | 0 |
| Q1 | 6/6 | Medium | 0 |
| Q2 | 6/6 | Medium-high | 1 (P2: Analysis → Research) |
| Q3 | 6/6 | Medium | 0 |
| Q4 | 6/6 | **Highest** | 1 (P2: Analysis → Research) |

Q4 produced the richest contextual reasoning. It surfaced hidden prerequisites and engaged with meaning beneath the literal words. It was the only variant that worked equally well on external tasks AND meta/continuation prompts.

## Key Finding

Quick misclassification doesn't manifest in fresh isolated agents — it happens under **conversation pressure** in real sessions (cognitive load, context saturation, momentum from prior messages). The experiment tested the mechanism (does the question change reasoning quality?) but not the failure condition.

**Round 2 validation:** Q4 was deployed in production and tested across 18 classifications under real conversation pressure. Result: 18/18 correct — the only variant with zero misclassifications in production conditions.

## Why Q4 Won

Q4 is the most open-ended — it doesn't presuppose the problem type (external vs meta, investigative vs constructive). It works for both "what's the best architecture?" and "think deeper about this." It forces engagement with meaning, not just labeling.

The engineered alternatives (Q1-Q3) each channel reasoning into pre-defined tracks. Q4 lets the model discover what matters about the specific input. This connects to the broader finding that exploration prompting outperforms extraction prompting for routing unpredictable inputs.

## Implications for AI Agent System Design

Before any classification or routing step, insert a forced open-ended question. The question should:
- Be open-ended (not presuppose the problem type)
- Require engagement with the input's meaning
- Produce a written answer before the classification decision

The forced question works via two mechanisms:
1. **Layer 1 (pause):** Any forced step breaks quick-response momentum. Dominant at low context.
2. **Layer 2 (depth):** Exploration questions produce context-proportional reasoning that scales with conversation length. Differentiation emerges at high context (50K+ tokens).
