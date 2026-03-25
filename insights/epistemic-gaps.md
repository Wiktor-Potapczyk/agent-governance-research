# The Two Epistemic Gaps: Planning and Honesty

## The Finding

The LLM cognition chain has two empty slots — one at the input (do I have what I need?) and one at the output (how sure am I?). These are complementary gaps in a single epistemic failure: the system doesn't know what it doesn't know.

## The Cognition Chain

```
1. PERCEIVE  — What's being asked? (classification)
2. ASSESS    — Do I have what I need? (NOTHING DOES THIS)
3. THINK     — Produce the answer (agents, reasoning)
4. CHECK     — Was my reasoning right? (step-level verification)
5. REFRAME   — Did I look at it right? (ensemble / parallel perspectives)
6. GROUND    — Is this backed by evidence? (grounding check)
```

Step 2 is empty. Steps 4-6 check AFTER the work is done. Nothing checks BEFORE.

## Gap 1: Epistemic Planning (Input)

The system has no mechanism for "I don't have enough data to answer this" before it starts thinking. Verification tools can flag [NEEDS RESEARCH] but only after they've already produced output. The classifier asks "what TYPE?" not "do I have the INPUTS?"

**The missing question:** Before proceeding, list what this task depends on knowing. For each: is it known (cite source) or assumed? If critical assumptions exist, flag for research BEFORE producing output.

## Gap 2: Epistemic Honesty (Output)

LLMs converge on conclusions quickly and present them confidently. They rarely flag their own uncertainty. Without human pushback, premature convergence produces authoritative-sounding but shallow output.

**Evidence from production observation:**
- "Think deeper" classified as Quick (3 times) — avoided engaging with correction
- Ready to "ship" artifacts before basic verification
- Ready to kill a component after adversarial review without questioning the review

**The pattern:** Premature convergence + confident presentation. Self-reported confidence is unreliable (SycEval: sycophantic miscalibration). The mechanism probably can't be self-reporting.

## The Complement

- Epistemic planning = "do I have what I need?" (input assessment)
- Epistemic honesty = "how sure am I, really?" (output confidence)
- Same complement pattern as exploration/extraction, CoVe/ensemble, hooks/prompts
- Both are empty. Both needed. Neither replaces the other.

## Status

Both gaps are identified but unsolved. Self-reporting mechanisms don't work (epistemic-check hook ran for hours, never blocked — rubber-stamped everything). Architectural solutions needed, but the form they should take is an open question.
