# LLM-Judge Variance Without Anchored Rubrics Is a Noise Source, Not a Gate

A rubric field scored by an LLM judge is only as stable as the anchor behind it. Where the rubric gives the judge a checklist, it can hold steady across repeated runs. Where it gives the judge a one-line description and asks for a number, it invents the number fresh almost every time, and the invention looks exactly like a real score.

## The Finding

An external practitioner ran an open-source, LLM-scored resume-screening system on one identical resume, unchanged, across roughly 100 runs, using a small local model at a low sampling temperature (gemma3:4b, temperature 0.1). The composite score ranged from 66 to 99 out of 100.

Read as a single range, that looks like ordinary judge noise. Read by field, a sharper pattern appears:

| Rubric field | Anchor | Behavior across about 100 runs |
|---|---|---|
| Technical Skills | Checklist-style, concrete | 8 out of 10 in 98 of 100 runs, effectively fixed |
| Work Experience | Brief description, no anchor | 25 out of 25 in every run, always maxed, never discriminated |
| Projects | Brief description, no anchor | Large variation, in the practitioner's own words |

The composite instability came almost entirely from the two unanchored fields, one of which never moved and told the pipeline nothing, and one of which moved by tens of points on identical input. The practitioner's own framing of the consequence: a cutoff score of 85 would fail the same resume roughly two thirds of the time, purely on luck.

## Why the Cause Is the Rubric, Not the Model

The obvious diagnosis is a small, unreliable model. The field-level split argues against that being the whole story. The same model, on the same input, in the same run, held to within one point on one field and swung wildly on another. What differed was not the model, it was how much interpretive room the prompt left it to fill in. A checklist gives the model a decision procedure. A one-line rubric description gives it a blank canvas and still asks for a number, and an LLM asked for a number on a blank canvas produces one, confidently, every time, and a different one on the next pass.

This is consistent with the established literature on LLM-as-judge bias (Zheng et al., "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena," arXiv:2306.05685), which documents position bias, verbosity bias, and self-enhancement bias in judge models generally. This finding adds a concrete, field-level measurement of where that instability lands when the rubric is the only thing that changes between fields.

## The Rule

An LLM-judge gate is only as reliable as its least-anchored field, and a composite score hides which field that is. Two design consequences follow:

- **Anchor every field the judge scores**, with the same concreteness as a checklist: enumerate what earns each point rather than describing a scale in prose. A field the judge cannot discriminate on (always maxed, like Work Experience above) is not contributing signal, it is contributing false confidence to the composite.
- **Temperature 0 is a partial fix, not the fix.** It removes within-run sampling noise but leaves the deeper problem untouched: an unanchored rubric leaves room for a different, internally consistent interpretation on every run, and a deterministic judge is still free to land on a different interpretation whenever the surrounding context shifts even slightly.

A composite pass or fail threshold sitting on top of unanchored fields is not a quality gate. It is a noise source with a threshold drawn through it, and the practitioner's report is a direct measurement of what a real cutoff line does when placed there.

## Related

- [Volatile-Source Citation Integrity](volatile-source-citation-integrity.md), the sibling problem of grading a check's binding tightness against what actually resists verification
- Primary source: danunparsed.com/p/hackerrank-open-source-ats (open-source ATS variance report, about 100 runs, gemma3:4b, temperature 0.1)
- Zheng et al., "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena," arXiv:2306.05685
