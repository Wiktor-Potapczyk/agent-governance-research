# Mandatory Exploration Backfires

## The Finding

Forced exploration or verification on every task produces performative compliance, not genuine quality. The model generates exploration-shaped text without actually exploring. Conditional triggers (uncertainty signals, user corrections) work better than unconditional enforcement.

## Evidence

**Ensemble finding (4 lenses unanimously agreed):**
1. Same-model "reconsideration" produces performative compliance, not genuine insight
2. Approval gates without criteria become rubber stamps
3. Forced alternatives on straightforward tasks create artificial complexity
4. Each mandatory gate compounds into "confidence laundering" — output looks more trustworthy without being more correct

**Production evidence:**
- Epistemic-check hook (cheap model evaluating output quality) ran for hours across multiple sessions. Never blocked once. Every response was rubber-stamped as "sufficiently confident." Disabled.
- Classifier produced "IMPLIES: this is straightforward" on complex prompts when forced to answer for every single message — the exploration became a box-checking exercise.

## The Concept: Confidence Laundering

Forced exploration → human approves (can't meaningfully evaluate every check) → next stage treats as validated → false authority chain. Each gate adds apparent confidence without adding actual verification. The result is output that LOOKS more trustworthy without BEING more correct.

## The Design Principle

**Conditional > mandatory.** Trigger exploration/verification when:
- Uncertainty is detected (hedging markers absent on complex tasks)
- User has been correcting frequently (behavioral pattern)
- Task is ambiguous (short prompt, no clear domain)
- Decision is irreversible or high-stakes

Don't trigger on:
- Clear domain + clear type
- Direct actions (file operations, simple queries)
- Simple acknowledgments

**The test:** When building any verification mechanism, ask: "What triggers this?" If the answer is "every response" → redesign. Find the signal that distinguishes "needs checking" from "obviously fine."
