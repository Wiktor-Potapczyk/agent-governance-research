# The Implication Ordering Principle

## The Principle

In any multi-step process that routes inputs through categories, understand the input's meaning before categorizing it. Implication first, decomposition second.

## Why Order Matters

Decomposition without implication produces mechanical categorization. The system matches surface patterns ("the word 'build' is present → Build type") without engaging with what the input actually needs.

Implication without decomposition produces understanding without action. The system grasps the meaning but doesn't know what to do with it.

The correct sequence: implication discovers the problem's shape, then decomposition breaks it into actionable parts.

## Evidence

- **Classifier experiment:** Before adding the implication step, the classifier defaulted to Quick on prompts like "Why did X fail?" (looks simple, actually requires investigation). After adding "What does this prompt imply?" as Step 0, these misclassifications stopped — the implication step surfaced the investigative nature before the type matrix ran.

- **Exploration prompting research:** Open-ended questions ("What's here?") outperform extraction questions ("What type is this?") for unpredictable inputs. Implication is exploration constrained by logical consequence — it inherits the performance advantage.

## Application

This principle applies to:
- **Task classification:** imply → classify → route
- **Problem solving:** understand → decompose → solve
- **Code review:** "what is this doing?" → "is it doing it correctly?"
- **Research:** "what question are we really asking?" → "how do we answer it?"

The common mistake is jumping to decomposition because it feels productive. The implication step feels slow but prevents misrouting that wastes more time than the step costs.
