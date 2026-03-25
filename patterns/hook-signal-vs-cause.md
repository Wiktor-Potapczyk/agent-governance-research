# Hook Signal vs Cause Analysis

Before building an enforcement hook, trace the failure to its root cause. The signal (what you observe) may not be the cause (why it happens). Building a hook against the signal catches symptoms, not the disease.

## Case Study: delegation-check

**Signal observed:** The model sometimes said "I should delegate this" in its reasoning but then answered inline instead of dispatching an agent.

**Hook built:** A Stop hook that scanned the response for delegation language ("delegate," "dispatch," "specialist agent") and blocked if no Agent tool_use followed.

**What happened:** The hook was killed after analysis revealed:
1. The "said delegate, didn't delegate" pattern was never actually observed in production logs
2. The real failure was classification quality — tasks were classified as Quick when they should have been Analysis
3. Fixing the classifier (better forced reasoning question) addressed the root cause
4. The hook caught false positives (discussion about delegation triggered it) more often than real violations

## The Method

Before building any enforcement hook:

1. **Document the observed failure** — what exactly went wrong? When? How often?
2. **Trace to root cause** — is this a classification error, a routing error, a process error, or an execution error?
3. **Check if the cause is already addressable** — does an existing hook/rule/process handle it?
4. **Build against the cause, not the signal** — if the cause is misclassification, fix the classifier. Don't build a delegation-checker.

## The Principle

Enforcement hooks are expensive (they fire on every response). A hook that catches a symptom instead of a cause will produce false positives forever. Spending 30 minutes on root cause analysis before building saves hours of false positive management after.
