# State Derived From a Transcript Is Not State

If a governance check reconstructs "what happened this turn" by scanning the conversation log, it is running an unmanaged projection over an unbounded, append-only stream, from a cold subprocess, with no persisted read offset. That design has a characteristic failure: it does not degrade, it returns empty. And empty reads exactly like compliant.

## The Finding

Five enforcement gates in one harness recovered turn state by regular expression over the raw transcript file. Measured on a single long session:

| Quantity | Measured |
|---|---|
| Transcript size | 386.7 MB, 119,128 lines |
| Window each gate reads | 200 KB, which is 0.05 percent of it |
| Transcript-coupled code across the five gates | 2,193 lines |
| Task-creation blocks in the file | 308 |
| Task-creation blocks inside the window | **0** |

The gate responsible for checking that project-management review had run could not see a single one of the 308 events it existed to check. It had never failed, because a gate that finds nothing to object to reports success.

This is not a bug in the regular expression. Every pattern was correct. The gate was blind **by construction**: a fixed-size window at the end of a file that grows without bound will, past a certain length, contain none of what you are looking for. The check silently converted from an enforcement mechanism into a no-op somewhere in the middle of the session, and nothing marked the transition.

## The same root cause, three times, independently

The window failure was not an isolated mistake. Two sibling bugs in the same codebase turned out to share its shape, and neither was found by looking for it:

- A competence counter read a 1 MB tail of a 26 MB log to fill a 50-event window. **It ran backwards**, reporting five, then three, then zero, for agents that had completed fifty runs. No code changed between readings. A byte-bounded read of a text stream had silently become a 30-minute time window.
- Seventeen of eighteen hooks derived session identity from the transcript **filename** instead of reading the `session_id` field that was present in their own input payload the entire time. Downstream, a falsy session value coerced to the literal string `unknown`, and the test-session filter matched on `unknown`. Result: 43,601 of 77,534 governance records mislabelled as synthetic. More than half the corpus, wrong, for months.

Three instances, one cause: **the structured thing was already there, and the code went looking for it in the prose instead.**

## Why it is worth naming

There are established names for each face of this. Edge-triggered consumption of a stream with no persisted offset, versus the level-triggered reconciliation that distributed systems settled on. An unmanaged read-model projection with no checkpoint and no idempotency, which is why it returns empty rather than stale: there is no accumulated state to degrade from. And a Correlation Identifier violation in the Hohpe and Woolf sense, where identity comes from an ambient convention rather than a field in the message.

Naming it matters because the instinct on discovering the 0-of-308 result is to widen the window. That fixes this session and reintroduces the same failure at the next order of magnitude.

## What actually distinguishes the fixable half

The five gates split cleanly once you ask a different question: not "is this text or is this typed," but **does an emission point exist at all?**

- Two of the five check only for tool markers, with zero prose assertions. Those are fully relocatable to structured hook events on the tool call itself, reading the tool input directly and never touching a transcript.
- The rest check whether the assistant *wrote* something: a classification block, a quality report, a review verdict. There is no structured event for "a model asserted a thing in prose," so there is nothing to relocate to. For those, the fix is not a better schema, it is a better read: consume the documented complete-message primitive at end of turn instead of a windowed regular expression.

That second half is the useful part of the lesson. The failure was widely described internally as text-versus-typed. It was not. The read strategy discarded structure that was already present. One of the two halves genuinely has no structure to move to, and pretending otherwise produces a migration that cannot finish.

## The caveat that outranks the finding

Fixing extraction and fixing adoption are different problems, and this one only touches extraction.

The convention these gates were built to enforce had attached to 7 of 368 steps after ratification, against a target of at least 40 percent. Perfect extraction over a 1.9 percent adoption rate produces an accurate measurement of almost nothing. A mechanism that reads correctly and a mechanism that anyone writes for are separate builds, and shipping the first one feels like progress in a way that is easy to mistake for the second.

## How to apply

- **If a check reads a log to find out what happened, ask what fraction of the log it reads.** If the answer is a fixed byte window over a growing file, the check has an expiry date it does not know about.
- **Ask what the check does when it finds nothing.** If the answer is "passes," a blind check and a clean run are indistinguishable in your data, retroactively, forever.
- **Before parsing prose for a fact, grep your own input payload for it.** The transcript-filename bug survived across eighteen files because nobody checked whether the field was already being handed to them.
- **Migrating changes the measurement regime.** There is no replay, so records gathered by scanning and records gathered by emission are not comparable. Tag new records with their source mechanism, or the two regimes get silently averaged and the discontinuity is read as a trend.
