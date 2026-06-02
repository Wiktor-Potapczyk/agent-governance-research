# The Enforcement Layer Needs Its Own Meta-Verification

In a governed agent system, hooks and gates enforce the rules. But the enforcement layer is itself code — and it has two silent failure modes that no amount of enforcing the *agent* will catch. The fix is to verify the verifier: prove the enforcement layer fails safe, with the same empirical discipline applied to the work it governs.

## The Insight

Enforcement code fails in two directions, and both are silent:

**1. False positives — a BLOCK-class hook blocks valid work.**
A hook that blocks "errors" or "unstructured output" will, sooner or later, block a *correct* output that merely resembles the failure it guards against. Observed cases: a short negative finding ("I cannot reproduce the bug; it works on the main branch") blocked as a "refusal" because it contains a refusal keyword; a correctly-formatted `Label: value` report blocked as "no structure" because it lacks list/heading markup. The agent did the right thing and was punished for it. Because the block looks like enforcement working, no one notices the enforcement is wrong.

**2. Silent drift — an enforcement reference stops resolving.**
Compliance hooks often hold an allow-list (which agents may be dispatched, which skills exist). When an asset is renamed or added and the allow-list isn't updated, the hook keeps "passing" — it simply no longer recognizes the new name. The rule still fires; it just enforces an outdated world. A dispatch the system relies on can silently fall outside the recognized set.

## The Discipline: Verify the Verifier

Two cheap, repeatable mechanisms close these gaps:

**False-positive guards (boundary tests).** Every BLOCK-class hook carries named tests that feed it valid-but-superficially-suspicious input and assert it stays *silent*. This is the inverse of a normal test: not "does it catch the bad thing" but "does it leave the good thing alone." A BLOCK hook without FP-guards is unverified — its true-positive rate is tested, its false-positive rate is assumed.

**Structural resolution gates.** A periodic check that every name an enforcement hook references (every allow-list entry, every cited file path, every registered hook) still resolves to a live asset. Catches the rename/add drift before it becomes a silent gap. Keep it advisory (warn, don't block) until its own false-positive rate is proven — a gate that blocks on its own bugs is worse than the drift it guards.

## Why This Matters

This applies to any rule-enforced agent system, not one framework. The moment you add automated enforcement, you have created a second system that can be wrong — and its errors are *quieter* than the agent's, because a block reads as success and a stale allow-list reads as a clean pass. The enforcement layer earns trust the same way the work does: by being adversarially tested for the failure mode that matters. For a BLOCK gate, the failure that matters is blocking valid work. For an allow-list, it is silently not recognizing reality.

| Enforcement artifact | The assumed property | The silent failure | The meta-check |
|---|---|---|---|
| BLOCK-class hook | only blocks bad output | blocks valid look-alike output | false-positive guard (assert silent on valid input) |
| Allow-list / registry reference | every entry resolves | renamed/added asset unrecognized | structural resolution gate (warn on unresolved name) |
| Cited file / path in a hook | the path exists | file moved, hook reads stale/empty | existence gate at config-load |

## The Trap

The natural instinct is to measure enforcement by how much it catches. That measures only true positives. An enforcement layer that catches everything *and* blocks valid work is not strict — it is broken in a way that looks like strictness. Measure the false-positive rate explicitly, or you are flying with half the instrument.
