# Context-Aware Classification

## The Finding

Classification quality comes from conversational CONTEXT, not prompt content alone. A prompt that looks trivial in isolation may require deep analysis given what was discussed earlier in the conversation. Classification systems that evaluate only the current message systematically underestimate complexity.

## Evidence

"Good, let's go" was correctly classified as Compound (multi-step complex task) despite having:
- Zero depth signals
- Zero type matrix matches
- Zero domain markers

The classification was correct because the model implicitly used full conversation context — knowing what "let's go" referred to (a multi-phase project plan discussed in prior messages).

## The Implication

The classifier operates on the current prompt. But classification quality comes from context. This creates an invisible dependency: classification accuracy degrades when context is lost (new sessions, compaction events, handoffs).

## Potential Mechanism

Require explicit context declaration in classifications:

```
CONTEXT USED: [what prior conversation state informed this classification]
```

- If CONTEXT USED is empty/generic → classification is shallow (likely wrong for continuation prompts)
- If it names specific prior decisions/artifacts/state → classification is grounded

This is the same principle as condition masking (ProCo): make implicit reasoning explicit so it can be verified. It doesn't trigger sycophancy — it asks "what evidence?" not "are you sure?"

## Connection to Epistemic Planning

Context-aware classification IS epistemic planning applied to the classification step: "Do I have the context I need to classify this correctly?" Without it, the classifier treats every message as if it arrived context-free, which is correct for first messages but wrong for everything after.

## Status

Identified as a potential improvement. Not yet implemented. The design question is where it lives: classifier Step 0.5, an addition to the output block, or a verification hook. Needs testing on real classifications to measure whether explicit context declaration catches misclassifications the current system misses.
