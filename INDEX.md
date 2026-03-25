# Fundamental Insights — Index

Original discoveries and research-backed findings from the Agent Suite project (March 2026). These insights emerged from iterative experimentation with LLM agent systems, validated against published research (85+ references) and cross-model review (Gemini).

## Core Discoveries

### 1. Exploration vs Extraction Prompting
**The finding:** Two complementary prompting modes exist. Exploration ("What does this imply?") leverages accumulated context. Extraction ("Name the agent") competes with it. Exploration outperforms extraction for routing unpredictable inputs.

**Evidence:** Classifier experiment — open question Q4 outperformed 3 research-engineered variants. All got 18/18 at low context (Layer 1: forced pause). Differentiation predicted at high context (Layer 2: context-scaling depth).

**Adjacent literature:** Contextual inertia (March 2026), DiSRouter, Thought Propagation. Gemini confirmed novelty.

**Novelty validated (2026-03-23):** No existing LLM routing framework requires explicit implication articulation before categorization. Nearest: Huang et al. 2025 (latent predictions), Furniturewala et al. 2024 (System 2 activation for debiasing). See [novelty-validation-findings](experiments/novelty-validation-findings.md).

- Source: [exploration-vs-extraction-prompting](insights/exploration-vs-extraction-prompting.md)
- Research draft: 2026-03-20-exploration-prompting-research-foundation (work file)

### 2. Implication Before Decomposition
**The finding:** Mechanical decomposition assumes you understand the problem. Implication discovers the problem's shape. Sequential: implication FIRST, decomposition SECOND. "What does this imply?" forces engagement with meaning before categorizing.

**Evidence:** The classifier was doing decomposition (type matrix) without implication (understanding). Adding Q4 as Step 0 fixed misclassification of depth-signaling prompts.

- Source: [exploration-vs-extraction-prompting](insights/exploration-vs-extraction-prompting.md) (section: "Implication before decomposition")

### 3. Quality Mechanism Spectrum (CoVe → Ensemble)
**The finding:** 8 empirically grounded levels of LLM reasoning quality, from actively harmful ("think again") to architecturally robust (blind ensemble). Same-model verification degrades with repetition.

**Evidence:** 85 references (2023-2026). Key: Huang et al. ICLR 2024 (-37.7 points for "are you sure?"), Lu et al. 2025 (cross-family >> self-verification), SelfOrg 2026 (strong models benefit less from multi-agent).

**Implemented as:** `/verify` skill (CoVe) + `/ensemble` skill (blind parallel) + MECHANISM field in classifier.

- Source: [cove-spectrum](theories/cove-spectrum.md) (memory)

### 4. Inline Bias Is Structural and Prompt-Unfixable
**The finding:** LLMs continuing text inline is the default autoregressive mode. 12.4% reasoning-action mismatch (reasons correctly to delegate, then answers inline). 78.5% persistence once started. Adding more rules makes it WORSE.

**Evidence:** MASFT (arXiv:2503.13657), SycEval (arXiv:2502.08177), tool-usage-gap research.

**What works:** Hooks (25%→90% activation), tool restriction, blind analysis, condition-masking (ProCo, +6.8-14.1), rejection-permission framing (+60%). What doesn't: anti-sycophancy prompts, more rules, self-correction, multi-agent debate.

- Source: [inline-bias-research](insights/inline-bias-is-structural.md) (memory)

### 5. Ensemble Diversity Is Real (for Framing Tasks)
**The finding:** Parallel cognitive lenses produce genuine divergence on framing/design questions. ~35% average overlap across 5 tasks x 3 lenses. Each lens catches unique risks others miss. Lu et al. concern about cosmetic diversity does NOT hold for framing tasks.

**Evidence:** 15-agent experiment (2026-03-20). Reframing eliminated problems entirely, Decomposition found SPOFs, Stakeholder traced user impact.

- Source: [ensemble-thinking](theories/ensemble-thinking.md) (memory)

### 6. The Epistemic Gaps (Planning + Honesty)
**The finding:** The cognition chain has two empty slots:
- **Step 2 (Planning):** "Do I have what I need to answer this?" — nothing checks input availability before thinking.
- **Step 5.5 (Honesty):** "How sure am I, really?" — Claude rarely flags uncertainty. Premature convergence + confident presentation. Self-reported confidence is unreliable (SycEval).

**Connected:** Both are the same complement pattern — input assessment vs output confidence.

- Sources: [epistemic-planning-gap](insights/epistemic-gaps.md) + [epistemic-honesty-gap](insights/epistemic-gaps.md) (memory)

### 7. Reconsideration Science
**The finding:** Genuine reconsideration cannot be caused, only invited. "Think again" produces compliance, not reconsideration. The ONE question: "Which of your assumptions, if it turned out to be wrong, would most change your answer?"

**Caveat:** Adversarial review scored 0.15 — useful heuristics for humans, NOT reliable for LLM mechanism design. For LLMs use architectural separation.

- Source: [reconsideration-science](insights/reconsideration-science.md) (memory)

### 8. User Intuition Outperforms Engineered Prompts
**The finding:** Wiktor's intuitive "What does this prompt imply?" outperformed 3 research-engineered alternatives. Simple open-ended questions that invite reasoning beat structured mechanism-targeted questions. User intuition about LLM thinking is a first-class design input.

- Source: [user-intuition-outperforms](insights/user-intuition-outperforms.md) (memory)

### 9. Context-Aware Classification
**The finding:** Classification quality comes from conversational CONTEXT, not prompt content alone. A prompt that looks Quick in isolation may require deep analysis given what was discussed 50 messages ago. The classifier needs what the conversation knows, not just what the message says.

**Implication:** Potential Step 0.5 — require CONTEXT USED field. Connects to epistemic planning (input availability).

- Source: [context-aware-classification](insights/context-aware-classification.md) (memory)

### 10. Hooks > Prompts for Governance (Hooks = QA, Not Oracles)
**The finding:** Deterministic hook enforcement beats soft instructions by 3.6x (25%→90% skill activation with UserPromptSubmit hook). Soft instructions decay within minutes in fresh sessions. Hooks fire regardless of LLM compliance. This is the core architectural insight: wrap the unpredictable function in deterministic infrastructure.

**Critical distinction (2026-03-21):** Hooks are QA infrastructure — they verify the process ran, not that the answer is correct. QA asks "did you follow the process?" not "is the output true?" The process roles (Research, Analysis, etc.) are responsible for producing quality. Hooks are responsible for forcing transparency so the user can see WHERE things went wrong. Conflating QA with correctness checking is how you get hooks trying to judge LLM output (epistemic-check) — which rubber-stamps everything.

**The value of compliance hooks:** A wrong result from a full pipeline is more informative than a wrong result from a shortcut. The pipeline leaves a visible trail — every decision exposed. Error correction mechanism is the user, but hooks ensure the data exists to do it.

**Evidence:** IMPLIES field dropped within minutes in Ralph Loop session despite MANDATORY language. Hook reminder restored it. Epistemic-check (correctness oracle attempt) never blocked once — failed because QA can't judge quality, only compliance.

- Sources: [hooks-as-governance](framework/hooks-as-governance.md) (memory) + [inline-bias-research](insights/inline-bias-is-structural.md) (memory)

### 11. Mandatory Exploration Backfires
**The finding:** Forced exploration on every task produces performative compliance, not genuine depth. The system generates exploration-shaped text without actually exploring. Conditional triggers (uncertainty signals, user corrections) work better than unconditional enforcement.

**Evidence:** Epistemic check hook ran for hours, never blocked — rubber-stamped everything. Classifier answered "IMPLIES: this is straightforward" on complex prompts when forced to answer every time.

- Source: [conditional-not-mandatory](insights/mandatory-exploration-backfires.md) (memory)

### 12. Question De-Biasing Process
**The finding:** 5-step process to remove self-bias from research questions: problem → de-self → de-direction → de-progress → stranger test. Wired into ensemble skill.

- Source: [question-debiasing-process](insights/question-debiasing-process.md) (insight file)

### 13. Discovery Over Confidence
**The finding:** LLMs default to "I know the answer" when the right mode is "I don't know, let's find out." Highest value from matching user's exploration energy.

- Source: [discovery-over-confidence](insights/discovery-over-confidence.md) (insight file)

### 14. Compound Task Neural Network
**The finding:** Tasks are not single types — they are mixtures of compounds. "Analyze X" might be 60% Analysis + 30% Research + 10% Planning. Each compound activates its own agents and tools. This is fractal: zoom into the Research sub-compound and it might itself be Research + Analysis. Compounds all the way down until atomic operations.

**The model:** Nodes = task types, weights = compound ratios per task, edges = agent/tool activations. The network fires dynamically at runtime as sub-tasks discover they need other compounds.

**What it changes:** Classifier would output compound ratios, not single labels. Routing activates multiple paths. Agents signal "I need compound X" at runtime.

**Novelty validated (2026-03-23):** No existing system classifies tasks as continuous mixture vectors over predefined cognitive primitives. Nearest: AT-MoE (continuous weights but model-defined groups), Jin et al. 2026 (named primitives but discrete), Fractals (fractal but no mixture modeling). See [novelty-validation-findings](experiments/novelty-validation-findings.md).

- Source: [compound-task-neural-network](insights/compound-task-neural-network.md)

### 15. The Recursive Execution Pattern
**The finding:** Every level of the system follows the same 6-step pattern: Classify → Decompose → Delegate → Work → QA → Report. Main session does it formally (classifier + hooks). Agents do it informally (natural reasoning). Projects do it over weeks (lifecycle phases). Same pattern, different timescale and formality.

**Connection:** The "compound, not recursive" constraint still holds — process skills don't call each other. But the COGNITIVE PATTERN recurs at every depth. This was not the initial design (which described enforcement structure, not execution flow) — it was recognized 2026-03-22 as the unifying principle.

- Source: [recursive-execution-pattern](insights/recursive-execution-pattern.md) (insight file)

### 16. Two-Layer Hook Purpose — Compliance Minimizes Errors, QA Maximizes Autonomous Run Length
**The finding:** Governance hooks serve two distinct complementary purposes. Compliance hooks (Layer 1) minimize errors — force process adherence, prevent shortcuts. QA hooks (Layer 2) maximize autonomous run length — verify claims before completing, reflect before escalating, exhaust capabilities before asking for help. Layer 1 keeps the system on the rails. Layer 2 keeps it running longer before needing the user.

**The autonomy target:** Not "no user needed." Exhaust all autonomous capabilities before asking for help. QA enforcement extends the interval between user touchpoints. This applies to all agent autonomy models — Jules, MetaGPT, ChatDev — not just this framework.

**The breaking mechanism:** Can't make the model want to explore. Can force the CONSEQUENCE of exploring — testing and breaking its own output. Build → try to break → if broken, fix → if unfixable, escalate. Compliance hooks reduce the space where mistakes happen. QA hooks force you to find the mistakes that remain.

**Implementation gap:** QA compound declared in APPROACH but not enforced. Stop hook needed to verify QA claims were tested when APPROACH declared `QA: yes`.

- Source: [two-layer-hook-purpose](insights/two-layer-hook-purpose.md) (insight file)

### 17. QA Is Popperian Falsification
**The finding:** QA proves absence of found bugs, not absence of bugs. A PASS means "could not break it." This asymmetry is fundamental. Every QA artifact must state what was tested AND what was not tested. The Untested Surface list shifts human judgment from "is this correct?" to "is what we didn't test acceptable?"

**Evidence:** Emerged from three-tier QA model design (2026-03-22). Adversarial-reviewer confirmed: "the pass gate is as reliable as the agent's severity calibration." Layer 4 (QA-on-QA) is irreducibly human.

- Source: [qa-is-popperian-falsification](insights/qa-is-popperian-falsification.md) (insight file)

### 18. TaskCreate = The Increment Institution
**The finding:** Claude Code's native task list (TaskCreate/TaskUpdate) IS the project increment. The terminal checkmarks are the visual institution. "All tasks completed" = increment boundary = pentest trigger. No new infrastructure needed — the tool already exists. The insight is recognizing it as the lifecycle mechanism.

**Evidence:** Session observation (2026-03-22) — P0-P4 executed as checklist, all `[completed]` = increment done = pentest fired. User identified the pattern: "the checklist is the institution of the increment."

**Constraint:** Hooks can't read task state (session-internal). Increment boundary is soft-enforced (classifier + /pm), not hard-enforced.

- Source: [taskcreate-is-the-increment](insights/taskcreate-is-the-increment.md) (insight file)

---

## Research Directions (Deferred)

1. **Context rot vs exploration prompting** — does exploration resist degradation as context grows? Observed: at 650K tokens, response quality degrades ("semantic averaging" per Gemini).
2. **Mechanistic question** — what does exploration do to attention patterns? Does it activate different retrieval than extraction?
3. **Prompt analysis** — 169 messages analyzed from Awards sessions. Phase 1 complete. Phase 2: compare with Agent Suite patterns.

