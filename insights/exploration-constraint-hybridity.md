# Exploration-Constraint Hybridity

## The Theory

"What does this imply?" is not a third prompting mode alongside exploration and extraction. It is exploration constrained by logical consequence.

- **Pure exploration:** "What's interesting about this?" — unbounded, may go anywhere
- **Pure extraction:** "What type is this?" — bounded, retrieves a category
- **Implication:** "What does this imply?" — explores, but within the logical consequences of the specific input

## Why Implication Outperforms Both

Pure exploration is too open — the model may explore irrelevant dimensions. Pure extraction is too closed — the model retrieves a cached pattern without thinking. Implication finds the middle: explore the specific input's meaning while staying anchored to its logical consequences.

This explains why "What does this prompt imply?" outperformed three research-engineered alternatives in the classifier experiment:
- It's more focused than exploration (anchored to the specific prompt)
- It's more open than extraction (discovers meaning rather than matching patterns)
- It scales naturally — simple inputs have simple implications, complex inputs have deep ones

## The Ordering Principle

Implication must come BEFORE decomposition. The classifier was doing decomposition (type matrix: Research? Analysis? Build?) without first understanding what the prompt implies. Adding the implication step as Step 0 fixed misclassification of depth-signaling prompts because the model understood what was being asked before trying to categorize it.

```
Wrong order:  Prompt → Decompose into types → Choose one
Right order:  Prompt → "What does this imply?" → Decompose with understanding → Choose
```

## Generalization

This principle applies beyond classification. Any multi-step process that routes inputs through categories benefits from an implication step before the routing step. Understand the input's meaning before categorizing it.
