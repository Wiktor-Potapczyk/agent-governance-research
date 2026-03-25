# Mandatory Exploration Degrades Quality — Use Conditional Triggers

Forced exploration and verification on every task produces performative compliance ("confidence laundering"), not genuine insight. The mechanism looks trustworthy without being more correct.

## Evidence

Four independent analytical lenses unanimously agreed that mandatory forced exploration on every task is harmful:

1. Same-model "reconsideration" produces performative compliance, not genuine insight
2. Approval gates without criteria become rubber stamps (a Haiku-based check ran for hours and never blocked once, then was disabled)
3. Forced alternatives on straightforward tasks create artificial complexity
4. Each gate compounds into "confidence laundering" — output looks more trustworthy without being more correct

## The Design Principle

**Conditional > mandatory.** Trigger exploration/verification when:

- Uncertainty is detected (hedging markers absent on complex tasks)
- User has been correcting frequently (behavioral pattern)
- Task is ambiguous (short prompt, no clear domain)
- Decision is irreversible

Don't trigger on:
- Clear domain + clear type
- Direct actions (read file, save)
- Simple acknowledgments

## How to Apply

When building new verification mechanisms, ask: "What triggers this?" If the answer is "every response" — redesign. Find the signal that distinguishes "needs checking" from "obviously fine."
