# User Intuition Outperforms Engineered Prompts

## The Finding

When designing prompts or reasoning interventions for LLMs, a user's intuitive phrasing often outperforms research-engineered alternatives. Simple open-ended questions that invite reasoning beat structured mechanism-targeted questions.

## Evidence

In a classifier experiment, a user suggested "What does this prompt imply?" as a curiosity addition alongside 3 research-grounded variants:
- Agent naming (from ensemble convergence research)
- Premortem (from ProCo / loss aversion research)
- Directive detection (from meta-awareness research)

The intuitive question produced the richest, most context-aware reasoning. It was the only variant with 0/18 misclassifications. It worked equally on external tasks AND meta/continuation prompts — something no engineered variant achieved.

## Why This Happens

The intuitive question is how a human naturally guides thinking. RLHF-trained models are optimized to respond to natural human communication patterns, not to mechanism-targeted structured prompts. An open question like "What does this imply?" maps directly to how humans ask each other to think deeper.

Engineered questions presuppose the problem type and channel reasoning into specific tracks. The intuitive question lets the model discover what matters.

## The Design Principle

When designing reasoning interventions for LLMs:

1. **Ask the user for their intuitive phrasing FIRST** — before engineering from research
2. **Test the user's version alongside engineered ones** — not instead of them
3. **The user's question is a design input** — not just feedback to incorporate after the fact
4. **Simple, open-ended > complex, structured** — for routing unpredictable inputs

## Broader Implication

This suggests that the gap between "prompt engineering" and "just asking clearly" is smaller than the field assumes. The most effective prompts may be the ones closest to how a thoughtful human would naturally phrase the request.
