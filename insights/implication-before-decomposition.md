# Implication Before Decomposition

## The Finding

Mechanical decomposition assumes you understand the problem. Implication discovers the problem's shape. They are sequential: implication FIRST, decomposition SECOND.

"What does this imply?" forces engagement with meaning before categorizing. Without it, systems match surface patterns ("the word 'build' is present") without understanding what's actually being asked.

## Evidence

A task classifier was doing decomposition (type matrix: Research? Analysis? Build?) without first understanding what the prompt implies. Adding an implication step as Step 0 fixed misclassification of depth-signaling prompts. Examples:

- "Why did X fail?" — classified as Quick (factual lookup) without implication step; correctly classified as Analysis (investigation) with it
- "Think about this more carefully" — classified as Quick without implication; correctly escalated with it
- "I've noticed X behaves differently" — acknowledged without investigation; investigated with implication step

## The Ordering Principle

```
Wrong:  Input → Decompose into categories → Choose one
Right:  Input → "What does this imply?" → Decompose with understanding → Choose
```

This applies beyond classification:
- **Problem solving:** understand before decomposing
- **Code review:** "what is this doing?" before "is it correct?"
- **Research:** "what question are we really asking?" before "how do we answer it?"

## Why Implication Is Not a Third Mode

"What does this imply?" is not a separate prompting mode alongside exploration and extraction. It is exploration constrained by logical consequence. The word "imply" carries causal reasoning naturally — it forces not just engagement but sequential reasoning about consequences.

## Connection

The common mistake across AI systems is jumping to decomposition because it feels productive. Implication feels slow but prevents misrouting that wastes more time than the step costs.
