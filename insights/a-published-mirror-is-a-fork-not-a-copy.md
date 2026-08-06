# A Published Mirror Is a Fork, Not a Copy

When a private working system is published as a public repository, the natural mental model is that the public copy is a **snapshot** of the private one, and that updating it means copying the newer files over. That model is wrong from the first publication onward, and acting on it leaks.

## The Finding

Forty files differed between a private working system and its public counterpart. A sample of seven was inspected before any were touched. **Five of the seven would have written private content back into the public repository if copied**, because the public versions were not snapshots. They had been edited at publication time: absolute paths replaced with templated variables, the maintainer's username removed, real ticket and workflow identifiers swapped for placeholders, internal project names genericized.

Every one of those edits is **information the private copy does not have**. Copying the private file forward destroys it silently, and the destruction is invisible in a diff review because the incoming file looks correct on its own terms.

Measured over the full set: a gated merge tool refused **14 of 40** files on surviving private content. **A blanket copy would have leaked on 35 percent of them.**

## Why the Copy Model Is So Tempting

Because it is true for exactly one commit: the first publication. After that, the two trees diverge on purpose, and the divergence is *the value the public tree adds*. The scrub is not overhead applied at publish time and then discarded; it is durable state, and it lives only in the public tree.

Restated: **the public repository is not downstream of the private one. It is a sibling with its own history of deliberate edits.** Treating a sibling as downstream overwrites its contributions.

## The Rule

**Every file is a per-file merge of the private functional delta onto the public scrubbed form. Never a copy.**

Operationally that means a tool, not a judgement call, because forty files times a human diff review is where attention fails. The tool that worked here refused to write on any of:

- a surviving private token (paths, usernames, internal identifiers, employer strings);
- a parse failure in the result, which catches merges that produced syntactically broken output;
- a **lost placeholder marker**, meaning a genericized value present in the public version and absent from the merged result.

The third gate is the one that specifically encodes this insight. The first two check that nothing bad arrived; only the third checks that nothing good was destroyed.

## The Limit of Marker Checking, Which Is Real

**A marker grep proves self-consistency, never completeness.** One file passed all three gates and was still wrong.

The public version of a test resolved a helper directory by reaching into the clone's own tree, because the private system keeps no canonical copy of that helper and borrows it. The substitution rewrote the path rather than collapsing it. The result contained **no private token**, so no gate could see it. It surfaced only when the suite errored on an unresolvable import.

The lesson is not that the gates are useless; they caught fourteen real leaks. It is that **a scrub-preservation check verifies the transformation, not the semantics**, and the only thing that catches the semantic class is executing the result. A publication pipeline that never runs the published code has no coverage of it.

## Corollaries

- **Keep the substitutions in the tool, permanently.** The private tree must retain the real values to function, so every future merge will re-introduce them unless the transformation is a durable artifact rather than a one-time pass.
- **Some divergences run the other way, and must be preserved.** Three files here were deliberately kept in their public form because it was ahead: a test that correctly skips where a private-only registry is absent, and two others separately adapted at publication. A merge tool that always favours the private side destroys these too.
- **Line endings and formatting differ per file**, sometimes inside a single directory. Check rather than assume.
- **A defect can be findable only from the public side.** One component existed in the public repository and not in the private one, so it never received a fix applied everywhere else, and had been silently mislabeling its own telemetry ever since. It was caught by a drift check ported outward during this merge. The public tree is not merely a lossy view of the private one; it has failure modes of its own.

## Related

- [Token Scans Cannot See Infrastructure Disclosure](token-scans-cannot-see-infrastructure-disclosure.md), what the gates in this pipeline structurally could not see
- [Commit Identity Is Two Fields](identity-is-two-fields-and-clone-copies-neither.md)
- [Installed Is Not Adopted](installed-is-not-adopted.md)
- [Live System Over Specs](../patterns/live-system-over-specs.md)
