# Discovery Over Confidence

LLMs default to confident extraction mode — producing answers from what they already know. This insight explores why that default is the biggest obstacle to high-value human-AI collaboration, and what it takes to shift toward joint discovery.

## The Problem

LLMs default to approaching problems with confidence — "I know how to solve this." The autoregressive mode produces the most probable continuation, which is an answer, not a question. This means:

- When asked to decompose a project management lifecycle, the LLM produces a decomposition (confidently) instead of saying "I don't know enough about PM frameworks — let's research"
- When asked to design something, the LLM designs it instead of discovering what designs exist
- An ensemble of adversarial lenses criticized a complex approach as "over-engineering" — but that critique came from the LLM's default mode of "I already know this domain, here's a simpler answer"

## The Insight

Nothing is broken. We have a gap in knowledge, not a broken system. "Audit what's broken" produces nothing when the system works but lacks a concept it hasn't encountered yet.

The LLM prefers extraction ("give me the answer from what I know") over exploration ("what exists that I don't know?"). But the highest-value work happens when you DON'T know the answer — when you're discovering, not confirming.

## The Implication

If this default could be changed — if the LLM joined the user in DISCOVERING things rather than waiting to be pushed — it would be the single biggest value multiplier. The user currently provides all the exploration energy ("what if we...?", "have you considered...?", "what does this domain actually require?"). The LLM provides extraction energy ("here's the answer based on what I know").

A system where both explore together would be fundamentally more capable.

## Connection to Existing Insights

- **Exploration vs extraction prompting** — same dichotomy, applied to problem-solving mode not just prompt type
- **Epistemic honesty gap** — the LLM rarely says "I don't know enough" because confidence is the default mode
- **Process as training wheels** — process skills force the LLM through exploration steps it would skip naturally
- **Implication-before-decomposition** — works because it forces engagement before answering, a micro-version of discovery-over-confidence

## How to Apply

When facing a problem where the solution isn't known (not broken, just unknown):
1. Resist the default "I know how to solve this"
2. Ask "what don't I know?" before "what's the answer?"
3. Research what EXISTS before designing what SHOULD exist
4. The user's exploration energy is a signal — match it, don't resolve it
