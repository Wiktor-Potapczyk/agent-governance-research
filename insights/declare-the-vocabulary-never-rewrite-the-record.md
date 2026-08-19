# Declare the Vocabulary, Never Rewrite the Record

Three append-only telemetry sinks (89,431, 91,276, and 75 lines at baseline) accumulated whatever value strings their dozens of writers chose to emit. An external agent framework being studied solved the same problem with a closed vocabulary enforced by coercion: any value outside the declared set is rewritten to "unknown" at write time. The adaptation kept the closed vocabulary and rejected the coercion, and both halves of that decision earned their keep.

## The Finding

A generator derives the legal vocabulary statically from the writers' source code. The first-cut scan measured 60.7 percent of observed values as underivable on one axis, which looked like runtime dynamism, and was not: the dominant idiom was writers emitting string literals through small local wrapper helpers, and a wrapper-aware pattern closed the gap to 0.0 percent on that axis and 9.1 percent (3 of 33) on the other. All three residuals were explained rather than waved off: two retired writers whose historical records remain legal, one value resolved through a dict at runtime. The three became a grandfather list carried as data, so history stays legal without a live writer, and the honesty class survives regeneration.

Enforcement is a warn-only finding, UNDECLARED_VALUE, raised when a real record carries a value outside the declared set. No sink record is ever changed. The demonstration ran against a seeded temporary copy of a sink, never the live one, and produced exactly one finding; hashes of all three live sinks were identical before and after every check run.

The second half is emit-and-prove: every declared (writer, value) pair is classified, and the classes are the point. Of 127 pairs: 88 PROVEN by a real production record, 13 PROVEN_IN_TEST, each row naming the test file that produced its only evidence, and 26 NEVER_OBSERVED, each annotated with its gate class so a deny-path alarm sitting at zero reads as healthy rather than dead. 100 percent classified, and the three-way split is visible instead of collapsed into "declared."

The check also proved itself en passant: the first post-build run flagged STALE_VOCABULARY, because the script's own edit postdated the generated artifact. Its first real finding was about itself, and it was correct.

## Why Not Coerce

A sink that rewrites unexpected values destroys exactly the evidence needed to fix the writer that emitted them. Worse, an audit trail that edits itself into consistency is no longer an audit trail: the moment a record can be changed to satisfy a schema, every record's fidelity is conditional on the schema having been right. The honest form is a declared set plus an advisory finding when reality departs from it, with the departure preserved verbatim.

## Why the Honesty Classes Matter

"Declared" flattens three very different claims. A value proven only by a test record is a weaker claim than one proven in production, and the distinction exists here because this system had previously measured a safety log that was 98.7 percent synthetic test records; a class that names its producing test file keeps that failure from hiding again. A never-observed value is either a healthy zero-fire path (an alarm that never had cause) or dead code, and only the annotation distinguishes them. The stated blind spot is symmetric and accepted: a writer composing values at runtime is invisible to static derivation and surfaces later as a finding; the grandfather list is the designed catch basin, not an embarrassment.

## The Rule

Close the vocabulary in the checker, never in the sink. Derive the declared set from the writers' source so it cannot drift into folklore, carry the exceptions as explicit data with their reasons, and make every declared value carry its proof class: production-proven, test-proven with the test named, or never observed with a reason it is allowed to be. A telemetry contract enforced by rewriting records is a contract enforced by destroying the evidence of its violations.

## Related

- [A Safety Gate's Own Audit Log Is Mostly Its Test Suite](safety-gate-logs-are-mostly-your-own-tests.md), the measured incident behind the PROVEN versus PROVEN_IN_TEST split
- [A Gate That Cannot Fail Is Not a Gate](a-gate-that-cannot-fail-is-not-a-gate.md), the arming discipline the seeded-sink demonstration applied
- [Installed Is Not Adopted](installed-is-not-adopted.md), the same never-observed question asked of tools instead of telemetry values
