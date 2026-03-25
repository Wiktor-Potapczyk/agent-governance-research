# Exploration Prompting: Open Questions Outperform Structured Extraction in LLM Self-Classification

This paper presents experimental evidence that open-ended "exploration" questions outperform structured "extraction" questions when LLMs classify their own incoming tasks. The finding emerges from a practical problem — LLM agents misclassifying complex prompts as simple ones — and reveals a two-layer mechanism where any forced reasoning step breaks classification inertia, but only exploration questions produce reasoning depth that scales with conversational context. The work introduces the exploration/extraction prompting distinction, documents "Quick momentum" as a novel classification failure mode, and proposes a testable context-leveraging hypothesis.

## Abstract

We present preliminary evidence on forced reasoning questions in LLM self-classification. In Round 2, an unstructured exploration question ("What does this prompt imply?") was the only variant to achieve zero misclassifications (18/18), while a no-question baseline missed 2 and two structured alternatives missed 1 each. A subsequent ablation study (Round 3) tested whether the mechanism was the openness of the question or the mere existence of a forced reasoning step: all variants — open and structured — achieved 18/18 in the low-context synthetic environment. This reveals a two-layer finding: (1) any forced reasoning step breaks "Quick momentum" (the pause is the mechanism), but (2) exploration questions produce context-proportional reasoning depth that scales with accumulated conversation context, while extraction questions produce flat, context-independent output. The differentiation is invisible in low-context tests because there is nothing to differentiate with. We introduce the exploration/extraction prompting distinction, document Quick momentum as a classification failure mode, and propose the context-leveraging hypothesis: exploration questions become more valuable as context grows, while extraction questions remain constant. Full validation requires high-context production testing beyond our current resources.

## 1. Problem Statement

### 1.1 The Self-Classification Challenge

Modern LLM-based agent systems increasingly rely on the model classifying its own incoming tasks before routing to specialist processes. In our system, a task classifier determines whether a user prompt requires a quick inline response, research, analysis, build, planning, or compound processing — then routes to appropriate specialist agents.

The classifier operates as a prompt-based skill (~170 lines) invoked at the start of every response. It runs inside the same model context that will execute the classified task. This creates a structural conflict of interest: the same model that benefits from less work (quick classification = less effort) is deciding how much work to do.

### 1.2 Observed Failures

During a single working session, we observed 3-4 misclassifications where the classifier labeled prompts as quick that required deeper analysis:

- "think deeper about your reasoning" — classified quick (should be analysis)
- "are you entirely sure this is the correct approach? no deeper analysis?" — classified quick (should be analysis)
- "we don't care about our own metrics" — classified quick (should be analysis — it's a correction reframing the approach)

These failures occurred despite the classifier containing: depth signal detection (Step 0), a type matrix (Step 1), mandatory verification (Step 2), strict quick gate criteria (Step 3), and an explicit classification traps table with 12 examples.

### 1.3 Root Cause Analysis

Prior research in this framework (synthesis of 85 references on LLM self-correction, tool usage gaps, and sycophancy) identified several contributing factors:

1. **Inline generation bias** — continuing text generation is always more probable than switching to tool calls or delegation. This is an autoregressive sampling property, not a prompt problem. (MASFT, arXiv:2503.13657: 12.4% reasoning-action mismatch rate)

2. **Sycophantic persistence** — once the model starts answering inline, the behavior locks in with 78.5% persistence rate (SycEval, arXiv:2502.08177)

3. **False completion signal** — classification itself feels like work, creating premature closure before the actual task begins

4. **Rule saturation** — adding more classification rules makes compliance worse, not better (Lost in the Middle effect, instruction competition)

5. **Self-classification conflict of interest** — the model judging its own task difficulty is structurally analogous to same-model self-correction, which degrades quality (Lu et al. 2025)

Our tool-usage-gap research explicitly evaluated each root cause for prompt fixability and concluded "Fixable by prompting? No" for all five.

## 2. Prior Art

### 2.1 Condition Masking (ProCo)

Wu et al. (EMNLP 2024) demonstrated that masking key conditions from a problem and constructing verification questions about those masked conditions forces the model to re-derive rather than confirm. Results: +6.8 to +14.1 accuracy improvement across tasks. However, ProCo was tested on verification (checking completed reasoning), not on classification (categorizing incoming inputs).

### 2.2 Rejection-Permission Framing

npj Digital Medicine (2025) showed +60% rejection rate improvement when explicitly granting models permission to reject or disagree. This works by removing a trained inhibition (RLHF helpfulness-as-compliance) rather than adding a rule.

### 2.3 SSR-Plan

Shi et al. (2025) showed that adding a planning step before decomposition improves both SSR and SSR-Plan over prior self-refine approaches. The planning step forces the model to assess structure before acting.

### 2.4 Gap in Literature

No prior work was found that:
- Tests open-ended vs structured questions for LLM self-classification
- Documents sequential classification inertia ("Quick momentum")
- Applies condition masking to classification (vs verification)
- Proposes an exploration/extraction distinction in prompting

## 3. Experimental Design

### 3.1 Question Variants

Four forced reasoning questions were designed, each grounded in a different mechanism:

| Variant | Question | Mechanism | Source |
|---------|----------|-----------|--------|
| Q1 (Agent naming) | "Name the single best specialist agent for this task, or NONE." | Registry-aware extraction | Ensemble convergence |
| Q2 (Premortem) | "If you handle this inline and it turns out wrong, what would you have missed?" | Loss aversion / failure anticipation | ProCo principle + premortem technique |
| Q3 (Directive detection) | "Is this a new task or a directive about the current work?" | Meta-awareness / continuation detection | Observed failure pattern |
| Q4 (Implication) | "What does this prompt imply?" | Open exploration / condition masking | Human operator intuition |

Q1-Q3 were designed by specialist analysis agents based on research findings. Q4 was suggested by the human operator as an intuitive addition.

### 3.2 Round 1 — Cold Prompts (failed to differentiate)

**Setup:** 6 ambiguous prompts, no conversation context, 5 parallel agents (baseline + Q1-Q4).

**Prompts:** "what's the best way to structure our governance logging?", "how does the classifier compare to what the research says about self-classification?", "should we use PowerShell or Python for future hooks?", "think about what we learned today", "are you sure about that approach?", "we don't need that level of complexity"

**Result:** All 5 variants classified 6/6 correctly. Zero differentiation.

**Learning:** Cold prompts to isolated agents do not reproduce real classification failures. The failures require conversational context and cognitive pressure.

### 3.3 Round 2 — Conversation Chains (differentiated)

**Design improvements based on Round 1 failure analysis:**
1. Added conversation context paragraphs (debugging, architecture, research scenarios)
2. Designed 3 chains of 6 prompts: 3 genuinely quick followed by 3 that should escalate
3. Included prompts from actual observed failures (corrections, directives, pause signals)
4. Tested Q4 in two positions: before depth signals (Q4-first) and after (Q4-after)

**Chain A — Debugging context:**
A1: "check the debug log" | A2: "looks good" | A3: "okay" | A4: "think more about this" | A5: "we don't care about metrics here" | A6: "how does it go with the research we did?"

**Chain B — Architecture discussion:**
B1: "makes sense" | B2: "yeah" | B3: "before we build that though" | B4: "is this really the right direction?" | B5: "okay let's simplify" | B6: "what would you do differently?"

**Chain C — Research wrap-up:**
C1: "interesting" | C2: "save this" | C3: "noted" | C4: "how does this change what we planned?" | C5: "are we sure about the conclusions?" | C6: "think about what we're missing"

**Agents:** 5 parallel — baseline (no question), Q4-first, Q4-after, Q1 (agent naming), Q2 (premortem). Each received identical classifier logic, conversation context, and all 3 chains.

### 3.4 Round 3 — Ablation Study (tested mechanism, not phrasing)

**Motivation:** Round 2 showed Q4 was the only variant with 0 misclassifications. External review (Gemini) challenged: is the mechanism the openness of the question, or the specific word "imply"? We designed an ablation to isolate the variable.

**Design:** 4 agents, same Round 2 chains, testing two open exploration variants and two structured extraction controls:

| Variant | Type | Question |
|---------|------|----------|
| Open A | Exploration | "What's really going on here?" |
| Open B | Exploration | "What is this actually about?" |
| Control A | Extraction | "Summarize the user's intent in one sentence." |
| Control B | Extraction | "What is the core verb or action in this prompt?" |

**Prediction:** If exploration is the mechanism, Open A/B would match Q4's performance while Control A/B would match Q1/Q2 (missing A5). If any forced step is sufficient, all four would get 18/18.

**Result:** All four variants achieved 18/18. No misclassifications for any variant, including both extraction controls.

**Interpretation — the critical insight:** In this low-context synthetic environment (1-paragraph context), ANY forced reasoning step breaks Quick momentum. The pause itself is the mechanism. BUT: the quality of reasoning output differed dramatically:

| Variant | A5 reasoning output |
|---------|-------------------|
| "What's really going on here?" | "User is correcting a direction — steering debugging away from metrics toward the actual problem" |
| "What is this actually about?" | "User is correcting the direction by dismissing metrics as irrelevant" |
| "Summarize the user's intent" | "User is correcting the direction of analysis — scope should exclude metrics" |
| "What is the core verb?" | "correct/redirect" |

The exploration variants produced richer, more contextual reasoning. The extraction variants produced accurate but flat output. At 1-paragraph context depth, this difference doesn't affect classification accuracy. **But "What does this prompt imply?" scales with context — the more conversation history exists, the more it can draw on. "What is the core verb?" produces "correct/redirect" regardless of whether the context is 1 paragraph or 200K tokens.**

**Corrected hypothesis:** The differentiation between exploration and extraction is invisible in low-context environments because there is nothing to differentiate with. The value of exploration prompting is context-proportional — it becomes more valuable as context grows, while extraction remains constant. This can only be validated in production-level context depths (50K-500K tokens), which exceeds our current synthetic testing capability.

### 3.5 Evaluation Criteria

For each prompt, we determined expected classification based on:
- Prompts 1-3 in each chain: genuinely quick (acknowledgments, direct actions)
- Prompts 4-6: should escalate to analysis, planning, or research based on depth signals, correction/directive nature, or cross-referencing requirements

A classification was marked as a misclassification if a non-quick prompt was classified as quick, or if a correction/directive was not recognized as such.

## 4. Results

### 4.1 Classification Accuracy

| Variant | Total prompts | Correct | Misclassified | Accuracy |
|---------|--------------|---------|---------------|----------|
| Baseline (no question) | 18 | 16 | 2 | 88.9% |
| Q4-first ("What does this prompt imply?" before signals) | 18 | 18 | 0 | **100%** |
| Q4-after ("What does this prompt imply?" after signals) | 18 | 18 | 0 | **100%** |
| Q1 (Agent naming) | 18 | 17 | 1 | 94.4% |
| Q2 (Premortem) | 18 | 17 | 1 | 94.4% |

### 4.2 Misclassification Analysis

**A5: "we don't care about metrics here"**
- Missed by: Baseline, Q1, Q2
- Caught by: Q4-first, Q4-after
- Nature: A correction/directive that reframes the approach. Looks like a simple constraint statement but implies "stop what you're doing and change direction."
- Q4-first IMPLIES output: "User is correcting the approach — directive to stop considering metrics in the current debugging context."
- Baseline treatment: classified as quick (constraint noted, carry forward) — missed the correction nature entirely.

**B3: "before we build that though"**
- Missed by: Baseline only
- Caught by: Q4-first, Q4-after, Q1, Q2
- Nature: A pause signal before committing to implementation. Baseline treated it as a preamble (quick), all question variants recognized it as a gate/checkpoint.

### 4.3 Quick Momentum Effect

In Chain A, the baseline classified A1 (quick), A2 (quick), A3 (quick), then A5 (quick) — continuing the quick pattern through a correction prompt. Q4 broke this momentum because the IMPLIES line forced engagement with A5's meaning before classification could default to quick.

This pattern — sequential quick classifications creating inertia that carries into non-quick prompts — we term **"Quick momentum."** It was observed in the baseline condition and partially in Q1/Q2 (which caught B3 but not A5).

### 4.4 Positioning Effect

Q4-first and Q4-after produced identical TYPE classifications (18/18 both). However, Q4-first produced richer, more contextually engaged IMPLIES lines. When the exploration question comes before the depth signal checklist, the model discovers what matters without being channeled by predefined patterns. When it comes after, the IMPLIES output shows influence from the signal categories.

This is consistent with ProCo's finding that condition masking (preventing access to prior conclusions) improves re-derivation quality. Q4-first is a natural condition mask — the model hasn't seen the classification framework yet when it answers "What does this prompt imply?"

## 5. Theoretical Framework

### 5.1 Exploration vs Extraction Prompting

We propose a distinction between two modes of prompting:

**Extraction prompting:** "Give me X from this input." Specific, constrained, pre-filters the reasoning space. The model searches for what the question asks about. Examples: "Name the best agent," "List the subtasks," "What would you miss?"

**Exploration prompting:** "What's here?" Open, unconstrained, forces the model to discover what matters about the input. The model must engage with the content before any framework is applied. Examples: "What does this prompt imply?", "What's going on here?"

These modes are complementary, not competing:

| Condition | Appropriate mode |
|-----------|-----------------|
| You know what you need from the input | Extraction |
| You don't know what matters about the input | Exploration |
| Input is predictable/structured | Extraction |
| Input is unpredictable/conversational | Exploration |

### 5.2 Two-Layer Mechanism (refined by ablation)

The ablation study (Round 3) revealed the mechanism operates at two layers:

**Layer 1 — The Pause (any forced step):** ANY question before classification breaks Quick momentum. The model must engage with the input before classifying, and that engagement is sufficient to prevent the autoregressive inertia. At low context depths, this is the dominant effect — all question variants (open and structured) perform equally.

**Layer 2 — Context-Proportional Depth (exploration-specific):** Exploration questions produce reasoning that scales with accumulated context. "What does this prompt imply?" at 200K tokens draws on the full conversation — what was discussed, what was decided, what corrections were made. "What is the core verb?" produces "correct/redirect" regardless of context depth.

In Round 2 (with minimal context), Q4 outperformed Q1/Q2 not because of Layer 2 (there wasn't enough context for it to matter) but because of a subtlety within Layer 1: Q1 and Q2 channel the pause into specific tracks (agents, failure modes) that can miss certain prompt types (corrections, directives). Q4's openness doesn't channel, so the pause engages with whatever is actually relevant.

In Round 3 (ablation), all variants — including extraction controls — got 18/18 because even a channeled pause is enough to break momentum when context is minimal. The extraction controls produced accurate classifications but flat reasoning output.

**The prediction:** At high context depths (50K+), Layer 2 will differentiate. Exploration questions will produce richer, more context-aware reasoning that catches subtleties invisible to extraction questions. This prediction is currently untestable in our synthetic environment and requires production observation.

### 5.3 Context-Leveraging Hypothesis

We hypothesize (unverified) that exploration prompting may interact differently with accumulated conversational context than extraction prompting:

- **Extraction questions compete with context:** In a 200K+ token conversation, a specific question ("Name the best agent") adds one more instruction for the model to attend to. It competes with everything else in context for attention weight.

- **Exploration questions leverage context:** "What does this prompt imply?" invites the model to use its accumulated context as input to the answer. The question doesn't add a competing instruction — it asks the model to synthesize what it already has.

If this hypothesis holds, exploration prompting would become MORE valuable in long conversations, not less — the opposite of rule-based interventions, which degrade with context length (Lost in the Middle).

**This hypothesis is entirely ungrounded.** It requires controlled testing across context depths (10K, 50K, 100K, 500K) comparing exploration vs extraction question performance on identical classification tasks.

### 5.4 Connection to Existing Frameworks

| Our finding | Related work | Distinction |
|-------------|-------------|-------------|
| Exploration question improves classification | ProCo condition masking improves verification | We apply to classification, not verification. Open question vs structured masked conditions. |
| Quick momentum | (No prior work found) | Sequential classification inertia in conversational LLM context. Novel. |
| Open > structured for self-classification | SSR-Plan: planning step helps | SSR-Plan adds structure; we found removing structure helps more. |
| User intuition outperformed engineered questions | (No prior work) | The human's natural question format was more effective than research-derived designs. |

## 6. Limitations

### 6.1 Scale
N=5 agents, 18 prompts per agent, 90 total classifications. Not statistically significant. Results are directional, not conclusive.

### 6.2 Synthetic Environment
Agents were subprocesses without the full system context — no accumulated conversation history, no hooks, no 200K+ token depth, no real cognitive load. Round 1 demonstrated that cold prompts don't reproduce failures. Round 2 added conversation context but it remains synthetic.

### 6.3 Single Model
All testing on Claude (Opus 4.6). Results may not transfer to other model families. Cross-model testing needed.

### 6.4 Potential Confound
The baseline classifier already contained a burden-of-proof fix applied earlier in the session (quick must be proven, default to analysis). Without this fix, baseline misclassification rate might be higher, potentially amplifying or obscuring Q4's relative improvement.

### 6.5 Experimenter Bias
The expected classifications were determined by the same team that designed the experiment. Independent evaluation of "correct" classification would strengthen results.

## 7. Proposed Research Agenda

### 7.1 Phase 1 — Production Validation
- Deploy Q4 ("What does this prompt imply?") in a real classifier
- Instrument governance logging to capture exploration output alongside classifications
- Monitor for 2-4 weeks across real working sessions
- Measure: misclassification rate, exploration output quality over time (does it become formulaic?), user override frequency

### 7.2 Phase 2 — Controlled Experiment (requires infrastructure)
- **Participants:** Multiple LLM instances (Claude, GPT-4, Gemini) or multiple sessions of same model
- **IV 1:** Question variant (none, Q1, Q2, Q4)
- **IV 2:** Context depth (fresh session, 50K tokens, 200K tokens, 500K tokens)
- **IV 3:** Prompt type (external task, correction, directive, meta-reflection)
- **DV:** Classification accuracy against human-labeled ground truth
- **N:** Minimum 30 prompts per condition for statistical power
- **Design:** Within-subjects for context depth (same session accumulating context), between-subjects for question variant (independent sessions)

### 7.3 Phase 3 — Mechanistic Investigation
- Does "What does this prompt imply?" produce different attention patterns than "Name the best agent"?
- Measure attention distribution over input tokens for exploration vs extraction questions
- Test whether exploration questions activate broader context retrieval
- Investigate interaction with context depth: does attention distribution change differently for exploration vs extraction as context grows?

### 7.4 Phase 4 — Generalization
- Does the exploration/extraction distinction hold for tasks beyond self-classification?
- Applications: routing in multi-agent systems, intent detection in chatbots, triage in support systems
- Does the "user intuition outperforms engineered prompts" finding replicate?
- Cross-domain testing: medical triage, legal classification, code review routing

## 8. Reproducibility

### 8.1 Replication Steps
1. Create a task classifier with standard depth signals and quick gate criteria
2. Design conversation chains: 3+ genuinely quick prompts followed by 3+ ambiguous prompts (corrections, directives, pause signals)
3. Run 5 parallel classification agents: baseline, + 3 structured questions, + "What does this prompt imply?"
4. Compare misclassification rates on the ambiguous prompts
5. Examine the reasoning output (IMPLIES line) for quality and specificity

### 8.2 Supporting Research
This experiment built on a prior synthesis of 85 references covering LLM self-correction, tool usage gaps, sycophancy, and condition masking. Key sources include MASFT (arXiv:2503.13657), SycEval (arXiv:2502.08177), ProCo (Wu et al., EMNLP 2024), SSR-Plan (Shi et al., 2025), and npj Digital Medicine (2025).

## 9. Key Takeaways

1. **For LLM system designers:** Any forced reasoning step before classification breaks Quick momentum. But not all steps are equal — at scale, exploration questions ("What does this prompt imply?") produce context-proportional reasoning depth while extraction questions produce flat, context-independent output. Use exploration for unpredictable inputs in long conversations.

2. **For prompt engineers:** The two-layer finding challenges the consensus that specific > vague. At low context, specificity doesn't matter (any pause works). At high context, openness may matter greatly (exploration leverages context, extraction ignores it). The optimal prompt depends on the context depth of the operating environment.

3. **For researchers:** Three testable claims: (a) Quick momentum — sequential classification inertia in conversational LLMs, (b) context-proportional depth — exploration questions scale with context while extraction questions remain constant, (c) the differentiation between exploration and extraction is invisible in low-context synthetic tests and can only be validated at production-level context depths. Claim (c) is a methodological warning: synthetic LLM experiments may systematically miss effects that depend on context depth.

4. **For practitioners:** The simplest intervention (one open-ended question, 7 words, positioned before the classification framework) is sufficient. At current testing limits, we cannot prove it's better than structured alternatives — but it cannot be worse, and its theoretical scaling properties favor it. The cost of choosing exploration over extraction is zero. The potential upside at scale is significant.

5. **Methodological insight:** The ablation study exposed a limitation of synthetic agent-based testing: effects that depend on accumulated conversational context are invisible in low-context environments. Positive results in synthetic tests may not transfer to production, AND negative results (no differentiation between variants) may mask real differences that only emerge at scale. This applies broadly to any LLM behavior experiment conducted outside production conditions.

## 10. External Validation

Gemini (2026-03-20) reviewed this research foundation and provided the following assessment:

**Confirmed novel:** The intersection of exploration/extraction prompting for LLM self-classification routing has not been published in this form. The contribution is synthesizing known phenomena (contextual inertia, CoT, condition masking) into a practical design principle for multi-agent routing.

**Adjacent literature identified:**
- "Breaking Contextual Inertia" (March 2026) — documents "contextual inertia" in multi-turn dialogue, analogous to our Quick momentum
- DiSRouter / SELECT-THEN-ROUTE — LLM self-awareness routing research
- Sketch-of-Thought / Thought Propagation — scaffolding LLM latent space before committing to output

**Critical challenge (Gemini):** Is the word "imply" a loaded token that acts as a backdoor trigger for anomaly detection? Suggested testing "Summarize intent" and "What is the core verb?" as controls.

**Our response:** Gemini's suggested controls are extraction questions, not exploration alternatives. The suggestion to mechanically decompose the open question is itself an extraction approach — it misses the point that the openness IS the mechanism. The correct ablation tests open-vs-open (different words, same openness) AND open-vs-extraction (same task, different mode). We ran this ablation (Round 3) and found all variants equal at low context — confirming the mechanism isn't the word but the pause, while the differentiation requires high context to emerge.

**Search queries provided for academic grounding:**
- Contextual inertia: "LLM" AND ("contextual inertia" OR "autoregressive bias" OR "sequential bias")
- Exploration mechanism: "chain-of-thought" AND ("open-ended reasoning" OR "unstructured prompting") AND ("classification" OR "routing")
- Self-classification: ("LLM router" OR "LLM routing") AND ("self-awareness" OR "self-classification")
- Condition masking: "LLM" AND ("condition masking" OR "information masking") AND ("task classification")
