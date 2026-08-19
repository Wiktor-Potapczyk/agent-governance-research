# A Miner That Proposes Loosening Must Fail Closed

A weekly mining pass over a governance log already grouped recurring failure events into proposals for a human owner. The extension under build was more dangerous: also mine recurring warn-tier events, warnings agents read and then proceed past, for tuning candidates, patterns warned about so often and accepted so routinely that they may deserve to be quieter. That is a machine whose entire output is proposals to weaken guards. Two structural properties made it safe to build, and the safer one is the less obvious.

## The Finding

Property one, proposal-only forever: the miner has no auto-apply path, not even behind a flag, and its output is a section in a weekly artifact a human reads. This is the obvious property.

Property two is the load-bearing one: the miner's knowledge of the protected floor, the hard deny tier that must never receive a loosening proposal, is derived live at run time from the enforcement sources themselves, never from a private copy of the pattern lists. A test greps the miner's source and asserts that none of the deny-tier pattern strings appear in it as literals. If the derivation fails for any reason, the miner fails closed: zero candidates plus a sentinel flag, rather than proposals computed against an absent exclusion set.

The decisive test is the negative fixture: a synthetic warn event matching the irreversible surface must produce NOTHING, at event counts of 10, 50, and 500. Frequency must have no power over the floor.

The first real weekly emission then matched an independently pre-computed dry-run expectation exactly: one candidate, a push-warning pattern, 17 events over 4 days across 3 sessions, 64.7 percent of them in a single session. The acceptance proxy reported 16 of 17 warns accepted, published with a blindness disclaimer rather than as a green light: the log cannot see work abandoned after a warn, later regret such as a revert, or the different semantics of advisory versus action-gating warnings. And the candidate cleared the 3-session minimum with zero margin; instead of quietly tuning the threshold to make the result look robust, the proposal renders the concentration number so the human judges it.

## Why Derive, Not Copy

A copied exclusion list drifts the day the enforcement changes, and it drifts silently in the dangerous direction: the miner keeps excluding yesterday's surface while happily proposing against today's. Deriving from the enforcement source makes the enforcement the single authority, and failing closed converts "I could not read the authority" into silence instead of into output.

The negative fixture is load-bearing for the same asymmetry that erodes deny-lists generally. The positive path fails visibly when broken: an expected candidate does not render, someone notices. The exclusion failing produces one extra plausible-looking proposal in a list of proposals, an absence-shaped defect with no symptom, and the proposal it produces is by construction a suggestion to relax the most safety-critical pattern in the system. The one test that matters is the one asserting nothing appears.

## The Rule

Any system that generates proposals to weaken controls must be structurally unable to apply its own proposals, and structurally unable to propose against the floor, with the floor derived live from the enforcement itself and any derivation failure producing zero output. Then write the negative test first: the most protected pattern, at absurd frequency, yields nothing. If that test is not in the suite, the miner's safety is an intention, not a property.

## Related

- [Narrowing a Deny Pattern Opens Floor Holes](narrowing-a-deny-pattern-opens-floor-holes.md), the one-directional feedback asymmetry that makes loosening proposals dangerous in the first place
- [Deny Patterns Fail on Command Spelling](deny-patterns-fail-on-command-spelling.md), why the protected surface is defined by its source, not by anyone's paraphrase of it
- [A Finding You Cannot Resolve Will Resurface Forever](a-finding-you-cannot-resolve-will-resurface-forever.md), the sibling failure on the same proposal board
