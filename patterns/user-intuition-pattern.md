# User Intuition Outperforms Engineered Prompts

In experiments designing reasoning prompts for AI agents, a user's intuitive question outperformed three research-grounded question designs. Simple open-ended questions that invite reasoning beat structured mechanism-targeted questions.

## Evidence

In a classifier question experiment, four variants were tested:
- Q1: Agent-naming question (from ensemble convergence research)
- Q2: Premortem question (from ProCo/loss aversion research)
- Q3: Directive detection question (from meta-awareness research)
- Q4: "What does this prompt imply?" (user's intuitive suggestion)

Q4 produced the richest, most context-aware reasoning of all variants. It surfaced hidden prerequisites, engaged with meaning beneath the literal words, and worked equally well on external tasks AND meta/continuation prompts — something no other variant achieved.

## Why

"What does this prompt imply?" is open-ended and invites genuine reasoning. The engineered questions presuppose the problem type (agents, failure modes, task vs directive) and channel reasoning into specific tracks. The open question lets the model discover what matters.

This is consistent with the exploration-before-extraction principle: open-ended prompts that leverage context outperform specific prompts that compete with it.

## How to Apply

When designing prompts, classifier steps, or reasoning interventions — ask the user for their intuitive phrasing FIRST, before engineering alternatives from research. Test the user's version alongside engineered ones, not instead of them. The user's question may outperform because it's how a human naturally guides thinking, which is closer to what RLHF-trained models respond to.
