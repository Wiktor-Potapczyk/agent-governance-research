# Narrowing a Deny Pattern Silently Opens Floor Holes

A safety gate that blocks too much generates pressure to relax it. Relaxing it is a one-character edit to a regex. Verifying that the relaxation removed only what you intended is a different and much less obvious task, and skipping it opened a hole in a gate that was still reporting itself as working.

## The Finding

The Gate-1 deny patterns for destructive deletion were firing on legitimate operations often enough to be a nuisance. The fix was to narrow one pattern so it matched deletions in the current directory rather than deletions generally.

The narrowed pattern did stop the false positives. It also stopped matching a parent-directory recursive delete, which nobody intended to un-block and which is strictly more dangerous than the case that motivated the edit.

Nothing failed. No test went red, because no test covered that case. The gate continued to load, continued to fire on the patterns it still matched, and continued to report itself as active. The only observable difference was an action that used to be denied and now was not, which is precisely the difference that produces no signal until it matters.

## Why Deny-Set Edits Are Not Ordinary Edits

For most code, "the tests pass" is a reasonable proxy for "the change was safe." For a deny-list, it is not, and the asymmetry is structural:

- **A too-broad pattern announces itself.** Every false positive is a visible, annoying block. The feedback is immediate and lands on the person best placed to fix it.
- **A too-narrow pattern is silent.** Its failure mode is an absence, an action that proceeds. There is no event, no log line, no annoyed operator. The gap is discovered when something irreversible happens, or never.

So the natural feedback pressure on a deny-list is **entirely one-directional**: toward narrowing. Every day of operation produces evidence for relaxing and no evidence for tightening. Left alone, a deny-list erodes.

## The Verification That Was Missing

The test that should have run is not "does the new pattern block the thing I want blocked?" It is a set-difference check:

> **Verify that NEW_DENY_SET equals OLD_DENY_SET minus exactly the intended un-blocks.**

Concretely, for a pattern edit:

1. Assemble a corpus of candidate commands covering the surface, including the cases the pattern was never specifically written for.
2. Evaluate the corpus against the old pattern and the new pattern.
3. Diff the two result sets.
4. Every command that moved from deny to allow must appear on the intended-un-block list. Anything else is a regression, regardless of what the test suite says.

Step 4 is the load-bearing one, and it is the step that "add a test for the new behaviour" does not cover. A new test asserts something about the new pattern. It says nothing about what the new pattern stopped doing.

## Generalisation

This applies to any allow/deny boundary that is edited under false-positive pressure: firewall rules, permission scopes, content filters, lint suppressions.

> **When you relax a safety boundary, the artifact under test is the difference between the old boundary and the new one, not the new boundary alone.** Compute the difference explicitly. A boundary edit verified only by forward assertions has been verified in the one direction that cannot fail silently.

A useful corollary: keep the corpus. The set-difference check is only cheap if the candidate corpus already exists. Building it during an urgent false-positive fix is exactly when it will be skipped.

## Related

- [safety-gate-logs-are-mostly-your-own-tests](safety-gate-logs-are-mostly-your-own-tests.md) — the calibration data that motivates narrowing may itself be synthetic
- [enforcement-layer-needs-meta-verification](enforcement-layer-needs-meta-verification.md) — enforcement code needs verification aimed at the enforcement property, not the feature
