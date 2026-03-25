# Forced Questions as Re-Derivation Mechanisms

## The Observation

When an LLM is asked "What does this prompt imply?" before classifying a task, it performs better than when given rules to follow. The question forces re-derivation from the input rather than pattern-matching against stored rules.

## Why Rules Fail

Rules are extraction prompts: "If X, then Y." The model scans for X, applies Y, moves on. This is fast but brittle -- the model matches surface patterns without engaging with meaning. A prompt that looks simple on the surface ("Update the config") may imply complex investigation that rules don't capture.

Adding more rules makes it worse. Each rule adds a pattern to match against, increasing the chance of a shallow match. The model finds a rule that fits and stops thinking.

## Why Questions Work

"What does this prompt imply?" is an exploration prompt. It forces the model to:

1. **Re-derive** -- reason from the input itself, not from stored categories
2. **Engage with meaning** -- what does the user actually need, beneath the literal words?
3. **Discover complexity** -- a question can surface implications that no rule anticipated

This is the condition-masking effect documented in ProCo research: by asking a question that requires the model to reason independently, you bypass the fast-path pattern matching that produces shallow answers.

## The Key Distinction

| Approach | Mode | What happens |
|----------|------|-------------|
| Rules ("If the task mentions code, classify as Build") | Extraction | Pattern match -> category |
| Questions ("What does this prompt imply?") | Exploration | Re-derivation -> understanding -> category |

The question produces a context-proportional response: simple prompts get simple answers, complex prompts get deep analysis. Rules produce uniform-depth responses regardless of input complexity.

## Evidence

- Classifier experiment: Q4 ("What does this prompt imply?") achieved 18/18 correct classifications across 6 prompts. Three engineered alternatives achieved 15-17/18.
- Quick momentum failure: without the forced question, the classifier defaulted to Quick on prompts that looked simple but implied investigation. The question broke the momentum.
- ProCo research: condition-masking questions improve reasoning by +6.8-14.1 percentage points across tasks.

## The Design Principle

Before any classification or routing step in an AI agent system, insert a forced exploration question. The question should be open-ended, require engagement with the input's meaning, and produce a written answer before the classification decision is made.
