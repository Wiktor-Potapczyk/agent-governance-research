# Research Gatherers Reconstruct From Training Memory Unless a Live-Citation Gate Catches It

A research step asked to gather sources and a research step asked to write from memory produce output that reads identically. Both come back as prose with citations attached. Only one of them actually looked anything up, and nothing in the surface text tells you which.

## The Finding

Across at least three independent research runs, a web-research step returned a report styled as freshly gathered findings while citing zero live-fetched sources: a training-data reconstruction wearing the shape of research. The failure was not visible from reading the report. It read as sourced, organized, and confident.

In one of the three runs, the reconstruction did more than omit live sourcing, it actively misclassified reality. The first pass flagged three specific, real, publicly indexed academic papers (one from a corporate research lab, two from independent academic groups) as unverified or as newsletter-invented terminology with no underlying primary source. The model was not being careless. It was reasoning correctly from an incomplete premise: it could not find these papers in its own training data, and it could not distinguish "I do not recognize this paper" from "this paper does not exist," because both feel identical from inside a single forward pass with no tool call to settle the question.

A corrected pass, given live web access, fetched all three papers directly: working links, real authors, real venues, in one case a specific accepted conference. The papers were not obscure. They simply postdated what the reconstruction had to work with, and the reconstruction had no way to know that about itself.

## Why the Text Cannot Tell You

A fabricated citation and a real one are typed the same way. Formatting a claim as "Author et al., Title, Venue, Year" costs a model nothing whether or not it looked anything up, because the format is a pattern it can produce from either a real fetch or a plausible guess with equal fluency. The tell is not in the text. It is in whether a network call actually happened, and that is information the text itself does not carry unless something forces it to.

This is the same shape as a broader class of self-report failure: asking the generator to also report on its own reliability produces a report that is exactly as unreliable as the thing being reported on, because both come from the same process with the same blind spot.

## What Worked

Two mechanisms caught all three instances before the reports were used, and both operate on the artifact rather than on the model's account of itself:

- **A live-citation gate.** The research process rejects a report below a minimum count of citations demonstrated to be live-fetched, checked by requiring and verifying an actual retrieval event per claim rather than trusting a citation's presence in the text. This is a re-derivation check, not a re-read: it asks whether the fetch happened, not whether the report says it happened.
- **Per-claim provenance tags recorded in the artifact itself.** Marking each claim as live-verified, grounded in stable training knowledge, or unconfirmed turns a binary pass or fail into an auditable trail. A reviewer, human or automated, can then see exactly which conclusions rest on which sourcing tier, rather than inheriting a report's overall confidence as if it applied uniformly to every line in it.

## The Rule

Do not accept a research artifact's own account of how it was produced. A model asked to research a topic defaults to answering from what it already knows and presenting the answer in the shape of something retrieved, and the two are visually indistinguishable in the output. The only thing that distinguishes them is a check external to the generation itself: did a fetch actually occur, verified independently of the model's claim that it did.

## Related

- [State Derived From a Transcript Is Not State](state-derived-from-a-transcript-is-not-state.md), the same failure shape applied to a different self-report surface
- [A Recorded Ruling Is Only a Ruling If the File Quotes Them](a-recorded-ruling-is-only-a-ruling-if-it-quotes-them.md)
