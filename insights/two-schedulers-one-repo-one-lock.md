# Two Schedulers, One Repository, One Lock

Two scheduled tasks maintained one git repository: a 30-minute rolling snapshot commit and a nightly backup that commits and pushes. For months they interleaved without incident. Then a morning catch-up run put them on the same second, the backup died on the repository's own `index.lock`, and the failure surfaced a five-day gap since the last successful backup. Git's index lock is a mutex, but it is a mutex that fails the loser instead of queueing it, and neither task had any policy for losing.

## The Finding

The fix was one shared lock with an explicit contention policy, and the numbers from proving it are the useful part.

The primitive: a lock directory in local application data, acquired by atomic directory creation (the one atomic primitive that needs no dependencies in a stock Windows PowerShell 5.1), holding an `owner.json` of `{pid, task, started}`. Staleness is judged in two parts, in order: dead-PID first (a holder whose process no longer exists is cleared immediately on the next acquire), then a 60-minute ceiling (a live holder past the ceiling is taken over). Contention policy is deliberately asymmetric: the light 30-minute task skips its cycle on contention, since another chance arrives in 30 minutes; the heavy nightly task retries 5 times at 30-second spacing and then fails loudly, naming the holder's PID and task in the log and status file.

The evidence, all from captured runs: a 5-process race produced exactly one winner and four losers; a replay harness reproducing the collision shape (both scripts starting at the same instant) serialized 10 rounds out of 10 with zero index-lock signatures, where one round of the same shape had produced the live collision. The detection tooling was armed before trust: the soak-check script was first pointed at the historical collision window and required to exit nonzero on the known failure, which it did.

Production then validated the staleness rule unprompted: a scheduled fire was hard-killed externally (exit status 0xC000013A, so its finally-release never ran), leaking the lock. The next scheduled fire cleared it via the dead-PID rule 11 minutes later, in plain text in the log. The ceiling was observed to fire exactly once, at 60.14 minutes of continuous hold, and provably not early: the acquire attempt at 57 minutes was still correctly suppressed.

## The Overstated Guarantee

The design originally claimed the light task holds the lock "only for seconds." Review forced the correction: typical holds are seconds, but the worst observed commit (a 1,464-file bulk snapshot) took about 3 minutes 40 seconds, which exceeds the heavy task's entire 2.5-minute retry budget. In that worst case the backup fails loudly by design and the next nightly fire retries. The honest resolution was to correct the claim and keep the budget, not to widen retries until the worst case passes silently: a loud bounded failure with a daily retry is a better property than an unbounded wait.

One fixture lesson worth carrying: the test environment killed spawned sleeper processes within minutes (plausibly endpoint security), so two attempts to observe a 60-minute hold died with their holders and were recorded as invalid attempts rather than massaged into evidence; the third attempt disclosed its scaffolding explicitly. Fixture failures are recorded as fixture failures, never as system behavior.

## The Rule

Two independent schedulers touching one resource are a distributed system, however small. Give them a single lock with an owner record, judge staleness by holder liveness before holding age, cap the worst case with a ceiling so PID reuse can only delay a takeover rather than corrupt anything, and make each loser's behavior an explicit decision, skip or retry-then-fail-loudly. A lock failure that is quiet is the original collision wearing a mutex.

## Related

- [A Gate That Cannot Fail Is Not a Gate](a-gate-that-cannot-fail-is-not-a-gate.md), the arm-the-control discipline this build applied to its own soak checker
- [Measure Then Gate](measure-then-gate.md), the before-measurement (a live collision and a five-day backup gap) that justified building enforcement at all
