# The Science of Inducing Genuine Reconsideration

How do you get an LLM to genuinely reconsider its reasoning, rather than performatively agree or defensively double down? This question sits at the intersection of epistemology, cognitive science, and prompt engineering. The findings below synthesize research on genuine reconsideration -- but come with an important caveat: adversarial review scored these findings at 0.15 confidence for direct LLM application. They are useful heuristics for human-AI interaction design. For LLM-to-LLM verification, use architectural separation (blind parallel agents, condition masking) instead.

## The One Question

"Which of your assumptions, if it turned out to be wrong, would most change your answer?"

This works because it is:
- Metacognitive (asks about thinking, not conclusions)
- Specific without being directed (the thinker identifies the target)
- Presupposes revisability without asserting error
- Often reveals the thinker can't answer -- which IS the trigger

Runner-up: "If you're right, why would a thoughtful, well-informed person disagree?"

## Core Principles

1. **Genuine reconsideration cannot be caused, only invited.** The less invested the questioner is in changing the answer, the more likely reconsideration becomes.
2. **"Think again" produces compliance, not reconsideration.** It signals "you're wrong" and triggers defense. Target PROCESS, not CONCLUSION.
3. **Internal tension > external challenge.** Doubt discovered within one's own beliefs is harder to dismiss than doubt imposed from outside (Socratic elenchus).
4. **Productive doubt is local and specific. Paralyzing doubt is global and diffuse.** Never imply "you're bad at thinking" -- only "there's something interesting here you may have missed."
5. **Curiosity > threat.** Challenges framed as interesting puzzles produce exploration. Challenges framed as gotchas produce defense.
6. **The thinker must retain agency** over what to revise. Open space, don't steer.
7. **Brevity works** -- single-sentence prompts can induce reconsideration IF they're specific, internal, question-form, and genuinely open.
8. **Self-induced reconsideration is possible but limited** -- same apparatus that produced the answer is asked to challenge it. Hybrid (self + external) is most robust.
9. **Emotional safety is prerequisite** -- changing one's mind must feel like virtue, not weakness.

## The Formula

"Given what you've said about [X], what follows for [Y]?" -- where Y is an unexplored consequence of the thinker's own reasoning.

## How to Apply

When designing any self-check or reflection mechanism for AI agents, use invitation not correction. Ask the ONE question. Don't detect and fix -- surface and invite. The mechanism should ask, not assert.

**Critical limitation:** These principles describe how reconsideration works in human cognition. LLMs simulate these patterns but the underlying mechanism differs. The adversarial 0.15 confidence score means: do not design automated LLM-to-LLM verification based on these heuristics alone. Use architectural separation (different contexts, condition masking, blind parallel evaluation) for reliable machine verification.
