# Question De-biasing Process

When dispatching questions to parallel agents or ensemble analyses, the framing of the question carries the framer's biases. This 5-step process translates a personal or contextual problem into a maximally unbiased question suitable for blind agent dispatch or ensemble analysis.

## The Process

1. **Problem** — State your problem in one sentence
2. **De-self** — Remove every word that references YOUR situation (project names, tool names, infrastructure, history)
3. **De-direction** — Remove every word that implies an answer direction ("should we adopt X" → "what approaches exist for X")
4. **De-progress** — Remove temporal/progress framing ("what are we missing" → "what does X require")
5. **Stranger test** — Read it as someone with zero context. Would they answer differently than someone who knows your setup? If yes, it's clean.

## Why It Matters

Ensemble questions carry the framer's biases. If you built a 17-file structure then ask "is this decomposition good?", the question anchors every lens to your structure. A clean question ("how would you decompose X?") lets lenses produce independent answers comparable against yours.

## Evidence

- Ensemble 1: A draft question anchored to the existing implementation. A reframed version was pure definitional — produced 4 genuinely independent perspectives.
- Ensemble 2: A clean question ("how would you decompose PM lifecycle research?") with zero reference to the existing structure. All 4 lenses independently said the existing decomposition was too broad.
- Pattern: users naturally de-bias when phrasing questions intuitively. This process formalizes that instinct for systematic use.

## Application

Use before every ensemble dispatch or blind agent evaluation. Integrate into the ensemble workflow's framing step as a checklist before the approval gate.
