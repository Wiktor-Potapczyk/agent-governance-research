# A Finding You Cannot Resolve Will Resurface Forever

A weekly governance miner emits recurring failure signatures from an audit log for an owner to review. By its third month the proposal artifact carried 15 signatures, and reading them closely showed the board had accumulated three kinds of entries whose premise was no longer true, with no mechanism for saying so.

## The Finding

All three shapes, from one real proposal artifact:

**Working-as-designed, flagged as regression forever.** Dispatches of certain agent types intentionally carry no classification context; that is the design. The signature family covering them had re-surfaced on every run for over two months, spreading across five agent types, because the resolution ledger had no way to record "accepted as designed, permanently resolved." Each new agent type crossing the same by-design path minted a fresh signature and a fresh "REGRESSION" label.

**Already dead, still reported.** A guard hook was removed by owner decision; its deny activity stopped exactly on the removal date, which the entry itself could see (all 20 events in the first half of the window, zero in the last 11 days). The signature surfaced anyway, because the miner has no concept of a retired writer: it mines a 30-day window, and a dead source keeps casting a shadow until the window slides past it.

**Stale burst, proposed as live.** 412 blocking events sat entirely inside an 8-day burst with zero occurrences in the 14 days since; the entry's own hypothesis text conceded "the burst may already be resolved upstream." It was still rendered as an open problem for the owner to action.

The meta-instance completes the picture: the highest-leverage unactioned proposal on the board, measured by recurrence, was the proposal to give the board permanent-resolution semantics, itself re-proposed across three consecutive runs without landing.

## Why This Decays the Board

Every premise-false entry charges the reader a re-derivation, "is this still real?", which is precisely the cost the board exists to amortize. After enough repeats the reader learns the board cries wolf and starts skimming, and skimming is indiscriminate: the two genuinely high-severity signatures in the same artifact get the same skim as the five by-design ones. A triage surface that cannot close items converges on being ignored, which is a worse end state than not existing, because it also absorbs the trust that a replacement would need.

Window-clipping compounds it: most signatures' first-seen timestamps sat exactly at the window's start, so the board cannot distinguish "new problem" from "old problem the window slid over." Age truncates into recency, and recency reads as urgency.

## The Rule

A recurring-signal system needs resolution semantics from day one, not as a follow-up: a ledger entry that can say "resolved forever, working as designed" and mean it across future runs; retirement awareness, so a signal whose writer no longer exists closes itself with a note instead of echoing; and staleness on the signal itself, so activity that ended weeks ago renders as historical rather than live. Without these, every run re-litigates settled questions, and the cost lands on the only genuinely scarce resource in the loop, the owner's attention. The board's first unresolvable finding is the beginning of the board's irrelevance.

## Related

- [A Miner That Proposes Loosening Must Fail Closed](a-miner-that-proposes-loosening-must-fail-closed.md), the same board's safety structure
- [Rubber-Stamp Enforcement](rubber-stamp-enforcement.md), the terminal state a decayed review surface converges toward
- [A Safety Gate's Own Audit Log Is Mostly Its Test Suite](safety-gate-logs-are-mostly-your-own-tests.md), why log-derived findings need interpretation before action
