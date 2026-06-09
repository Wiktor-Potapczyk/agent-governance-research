# Fundamental Insights — Index

Original discoveries and research-backed findings from the Agent Suite project (March–April 2026). These insights emerged from iterative experimentation with LLM agent systems, validated against published research (85+ references) and cross-model review (Gemini).

## Core Discoveries

### 1. Exploration vs Extraction Prompting
**The finding:** Two complementary prompting modes exist. Exploration ("What does this imply?") leverages accumulated context. Extraction ("Name the agent") competes with it. Exploration outperforms extraction for routing unpredictable inputs.

**Evidence:** Classifier experiment — open question Q4 outperformed 3 research-engineered variants. All got 18/18 at low context (Layer 1: forced pause). Differentiation predicted at high context (Layer 2: context-scaling depth).

**Adjacent literature:** Contextual inertia (March 2026), DiSRouter, Thought Propagation. Gemini confirmed novelty.

**Novelty validated (2026-03-23):** No existing LLM routing framework requires explicit implication articulation before categorization. Nearest: Huang et al. 2025 (latent predictions), Furniturewala et al. 2024 (System 2 activation for debiasing). See [novelty-validation-findings](experiments/novelty-validation-findings.md).

**Deeper findings (2026-03-25, paper V5.1):**
- expl2 ("What's really going on here?") → 1.25% Type II error; extr2 ("Summarize intent") → 3.12%. McNemar p=0.00073, CMH p=0.0013 (Bonferroni-corrected).
- R3 mechanism ablation: "Think carefully" achieves 1.0% — not significantly different from exploration (p=0.77). Mechanism is forced attention, not open-ended framing specifically.
- Structured yes/no detection catastrophically harms Claude models (Haiku +330% errors). Binary choices offer a defaultable "no."
- **Complementary failure modes:** Exploration forces committed implication statements (rescues 5/8 think failures). Think-carefully uses consequence framing (rescues 7/10 exploration failures). Neither has universal advantage — different trap subtypes.
- **Recognition without commitment:** Sonnet under "think carefully" writes "this violates change management policy" → still classifies Quick. Under exploration, same model identifies same violation → escalates. The commitment mechanism is the qualitative differentiator.
- **Difficulty-scaling hypothesis (falsifiable, untested):** Exploration advantage should emerge on harder tasks / higher context, where content-free nudges are insufficient for task-specific representation-building.
- Per-model: DeepSeek p=0.031, Haiku p=0.016. Flash and Sonnet individually non-significant. Pooled result is exploratory.

**19 limitations explicitly stated in paper.** Key: post-hoc expansion, gate confound not fully isolated, label circularity (Sonnet generated labels AND was tested), single author, pooled exploratory.

**Open:**
- High-context experiment (>100K tokens) — tests difficulty-scaling hypothesis
- Second rater for 50 expanded prompts — strongest methodological improvement
- Within-dataset ablation (all 8 variants in one API run)
- Open-weight models (Llama/Mistral)

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
**The finding:** An intuitive "What does this prompt imply?" outperformed 3 research-engineered alternatives. Simple open-ended questions that invite reasoning beat structured mechanism-targeted questions. User intuition about LLM thinking is a first-class design input.

- Source: [user-intuition-outperforms](insights/user-intuition-outperforms.md) (memory)

### 9. Context-Aware Classification
**The finding:** Classification quality comes from conversational CONTEXT, not prompt content alone. A prompt that looks Quick in isolation may require deep analysis given what was discussed 50 messages ago. The classifier needs what the conversation knows, not just what the message says.

**Implication:** Potential Step 0.5 — require CONTEXT USED field. Connects to epistemic planning (input availability).

- Source: [context-aware-classification](insights/context-aware-classification.md) (memory)

### 10. Hooks > Prompts for Governance (Hooks = QA, Not Oracles)
**The finding:** Deterministic hook enforcement beats soft instructions by 3.6x (25%→90% skill activation with UserPromptSubmit hook). Soft instructions decay within minutes in fresh sessions. Hooks fire regardless of LLM compliance. This is the core architectural insight: wrap the unpredictable function in deterministic infrastructure.

**Critical distinction (2026-03-21):** Hooks are QA infrastructure — they verify the process ran, not that the answer is correct. QA asks "did you follow the process?" not "is the output true?" The process roles (Research, Analysis, etc.) are responsible for producing quality. Hooks are responsible for forcing transparency so the user can see WHERE things went wrong. Conflating QA with correctness checking is how you get hooks trying to judge LLM output (epistemic-check) — which rubber-stamps everything.

**The value of compliance hooks:** A wrong result from a full pipeline is more informative than a wrong result from a shortcut. The pipeline leaves a visible trail — every decision exposed. Error correction mechanism is the user, but hooks ensure the data exists to do it.

**Evidence:** IMPLIES field dropped within minutes in session despite MANDATORY language. Hook reminder restored it. Epistemic-check (correctness oracle attempt) never blocked once — failed because QA can't judge quality, only compliance.

- Sources: [hooks-as-governance](framework/hooks-as-governance.md) (memory) + [inline-bias-research](insights/inline-bias-is-structural.md) (memory)
- External validation: [gulli-agentic-patterns-comparison](meta/gulli-agentic-patterns-comparison.md) — Gulli (Google) confirms 7 of our patterns; identifies 3 gaps (trajectory scoring, loop detection, state rollback)
- Enforcement gap audit: [execution-exhaustion-audit](meta/execution-exhaustion-audit.md) — honest assessment of stated vs enforced execution requirements

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
- Enforcement gap: [qa-execution-gap-analysis](specs/qa-execution-gap-analysis.md) — QA format enforcement ≠ QA method enforcement; "read the file" passes hooks identically to "ran bash command"

### 18. TaskCreate = The Increment Institution
**The finding:** Claude Code's native task list (TaskCreate/TaskUpdate) IS the project increment. The terminal checkmarks are the visual institution. "All tasks completed" = increment boundary = pentest trigger. No new infrastructure needed — the tool already exists. The insight is recognizing it as the lifecycle mechanism.

**Evidence:** Session observation (2026-03-22) — P0-P4 executed as checklist, all `[completed]` = increment done = pentest fired. User identified the pattern: "the checklist is the institution of the increment."

**Constraint:** Hooks can't read task state (session-internal). Increment boundary is soft-enforced (classifier + /pm), not hard-enforced.

- Source: [taskcreate-is-the-increment](insights/taskcreate-is-the-increment.md) (insight file)

### 19. Sidecar Files for Post-Compaction Enforcement
**The finding:** Governance hooks that read the conversation transcript for enforcement contracts silently bypass after context compaction — the contract falls outside the read window and the hook finds nothing. Placing a machine-readable sidecar file (`DISPATCHES.json`) beside the human-readable skill spec (`SKILL.md`) — and having the hook read the sidecar as fallback when the transcript scan yields nothing — closes the bypass without changing the source of truth.

**Novel element:** Terminal-skill exclusion. Skills that are verifiers rather than orchestrators (QA, pentest) have empty mandatory contracts; letting them overwrite the "current skill" tracker in the fallback silently nullifies enforcement for earlier orchestrator skills in the same session. The fix is excluding terminal skills from overwriting the tracker.

**Prior art:** Sidecar-file contracts widely used (pre-commit, Conftest, Terraform state, Microsoft agent-governance-toolkit). File-based fallback for state externalization well-established in infrastructure. The combination — sidecar contract + compaction-bypass motivation + terminal-skill exclusion in an AI agent governance context — does not appear in the public literature surveyed.

**Evidence:** H11 integration shipped 2026-04-19. 4/4 behavioral tests PASS (fallback fires on missing mandatory dispatches; Quick-like session silent; contract-present path unchanged; planning-then-qa regression confirms Q4 fix holds).

- Source: [sidecar-files-for-post-compaction-enforcement](insights/sidecar-files-for-post-compaction-enforcement.md) (insight file)

### 20. Infrastructure Audit — Five Systemic Fragility Patterns (2026-04-18)
**The finding:** A full infrastructure audit across five surfaces (hooks, agents, skills, CLAUDE.md/MEMORY.md, cross-component deps) revealed 11 HIGH, 13+ MED, and 9 LOW findings. The fragility is not incidental — it follows five architectural patterns:

1. **Accretion without pruning** — components added, never removed; dead code accumulates.
2. **Multi-source truth with manual sync** — registry.json, SKILL.md files, CLAUDE.md Agent Registry, MEMORY.md, and hook alias tables all encode the same agent list; manual sync breaks silently.
3. **Prose contracts / code enforcement mismatch** — SKILL.md says "do X"; hook checks for a different marker; gap is invisible until pentest.
4. **Fail-open on missing context** — when the hook's transcript read window misses the classification block, enforcement silently passes.
5. **Bidirectional contract gaps** — classifier declares what skills produce; skills assume what the classifier dispatched. Neither checks the other's actual output.

**Opus 4.7 additions beyond Sonnet discovery:**
- Post-compaction enforcement blind spot (H11) — hooks' 200KB tail-read may miss classification block after transcript compaction.
- Singular-vs-gerund naming drift is a pattern, not one-off — `architect-review` is case study; same risk at `research-analyst`, `prompt-engineer`, `workflow-orchestrator`.
- Composed bypass attacks — B1, B2, B3 are not independent; together they form a complete enforcement escape.
- A+B fix alignment — the 2026-04-18 patch extends accretion pattern rather than closing it; design debt, not immediate bug.
- Reachability metadata gap — registry tracks existence but not usage; orphan detection requires separate analysis.

**Key fix:** H3 (reject `MUST DISPATCH: none` on non-Quick tasks) is the lowest-effort, highest-impact fix — breaks the composed B1+B2+B3 bypass.

- Source: research/2026-04-18-infrastructure-audit-findings.md (entry point)
- Opus synthesis: research/2026-04-18-infrastructure-audit-s6-synthesis.md (architectural patterns)
- Pentest report: research/2026-04-18-infrastructure-audit-s9-pentest.md (empirical verification)
- RCA methodology: research/2026-04-14-research-orchestrator-bypass-rca.md (dual-stream investigation pattern)

### 21. Rubber-Stamp Enforcement Gaps
**The finding:** Hooks that check output text but not real dispatch create silent bypass paths. The pattern: `if has_output and not has_real_invocation: BLOCK`. Two instances found in the 2026-04-18 audit — `check_pm_checkpoint_report` (verified report text but not agent dispatch) and `work-verification-check` CHECK 1 (required BOTH conditions simultaneously, missing the skipped-skill-entirely case). Invoke-side verification complements output-side verification; AND/OR logic matters.

**Generalization:** For any governance hook, ask: "What would this miss if the agent faked the output?" Design invoke-side + output-side checks together, not independently.

- Source: [rubber-stamp-enforcement](insights/rubber-stamp-enforcement.md) (insight file)

---

### 22. Framework Investigation — Cold-Context Multi-Lens Empirical Map (2026-05-25)
**The finding:** A cold-context empirical investigation of the framework's runtime state — two independent investigation lenses merged into one canonical document. Key discoveries: (1) Stop hook event carries 11 hooks vs. 1–3 for every other event type — enforcement maximally rear-loaded; (2) session-start log runs as a hidden side-effect of another hook, creating an unregistered dependency that silently breaks governance-log boundaries on failure; (3) the prior session's ghost-agent count was overcounted — only 2 genuine ghosts confirmed (the rest had implicit dispatch paths the strict-grep parser missed); (4) a deprecated routing alias active since weeks prior still receives live n8n task dispatches through two skill files; (5) internal compliance metrics measure rule conformance, not output quality — a closed-loop measurement problem no internal instrumentation can resolve.

**Evidence:** Two parallel lenses (empirical e2e mapping + counter-bias investigation) reaching independent conclusions on the same findings, with explicit CORRECTION callouts where the second lens corrected the first. Covers hook registration state, agent dispatch contracts, wiki layer velocity, governance-log schema drift, and project phase status.

**Connects to:** Finding 20 (Infrastructure Audit five patterns), Finding 23 (Architecture v2 delta spec), Finding 27 (Must-Dispatch compliance remeasurement).

- Source: [framework/2026-05-25-framework-investigation.md](framework/2026-05-25-framework-investigation.md)

---

### 23. Agent-Governance Architecture v2 — Delta Spec (2026-05-25)
**The finding:** Seven concrete deltas required to close the gap between the framework's declared architecture and its runtime behavior. The spec resolves a three-way framing choice — (a) derive CLAUDE.md from a runtime inventory, (b) keep CLAUDE.md authoritative and enforce drift via a lint pass, (c) accept drift as natural — in favor of option (b), with the clarification that the Agent Registry block (mechanical enumeration) is the primary drift-detection target, while narrative sections carry lower severity. The "neural network" metaphor from the prior architecture spec is preserved as a mental model only; compliance trend data falsifies its behavioral prediction.

**Seven deltas:** (1) bind 2 genuine ghost agents via explicit dispatch markers; (2) Stop-chain rebalance investigation; (3) session-start hidden dependency surface-or-eliminate; (4) replace wiki ingest cadence target with input-availability trigger; (5) doctrine-drift lint pass for the Agent Registry block; (6) schema dual-emit for compliance events; (7) deprecated routing cleanup in two skill files.

**Evidence:** Every claim traces to a section of the companion framework investigation document (Finding 22). Adversarial counter-argument on framing choice (a) acknowledged and addressed narrowly.

- Source: [specs/agent-governance-architecture-v2.md](specs/agent-governance-architecture-v2.md)
- Companion evidence base: [framework/2026-05-25-framework-investigation.md](framework/2026-05-25-framework-investigation.md)

---

### 24. Framework Evaluation — Multi-Lens Verdict with Process Diagrams (2026-05-25)
**The finding:** Parallel evaluation of the framework across two lenses — architect (implementation alignment) and adversarial (framing soundness) — converging on a unified verdict: the framework is architecturally salvageable via incremental deltas, but has a closed-loop measurement problem that no internal instrumentation can solve. Headline verdicts: architect lens DIVERGENT_AND_DEEP (confidence high); adversarial lens STRUCTURALLY FLAWED at the measurement layer (confidence 0.85); synthesis SALVAGEABLE VIA DELTAS + external calibration (confidence 0.88).

**The closed-loop diagnosis:** every internal compliance metric (dispatch compliance rate, PM format compliance, QA pass rate) measures conformance to the framework's own rules. The framework grades its own homework. Five documented agent fabrication incidents in roughly two weeks were each caught by human review — no framework hook blocked or flagged any before discovery. This gap is not addressable from inside the framework.

**The one loop-exit:** an external calibration protocol (periodic human spot-check of QA-PASS artifacts against actual correctness) is the only channel that crosses the closed-loop boundary. Five process diagrams included.

**Evidence:** Three-source synthesis (architect lens, adversarial lens, framework investigation). Confidence 0.88 reflecting agreement between independent lenses.

- Source: [meta/2026-05-25-framework-evaluation.md](meta/2026-05-25-framework-evaluation.md)

---

### 25. Framework Improvement PRD — Fabrication Detection + External Calibration (2026-05-25)
**The finding:** A product requirements document translating the framework evaluation's highest-confidence findings into two shippable work items. The thesis: closing the highest-incidence empirical gap (file-existence verification on sub-agent write claims) and opening the only loop-exit channel (Wiktor periodic spot-check of QA artifacts) delivers more reliability per unit effort than continuing architecture work in isolation.

**Root cause addressed:** five documented agent fabrication incidents all followed the same pattern — an agent claimed to have written a file; the file did not exist; no hook detected this. The PRD specifies a file-existence check as the minimum viable detector for this class of failure.

**Goals:** (G1) reduce undetected fabrication incidents from 5 per two weeks to ≤1 per month within 30 days post-ship; (G2) establish baseline external calibration signal within 30 days; (G3) close the three Delta-1 ghost-agent binding gaps.

**Note:** The PRD documents its own genesis — implementation-plan fabricated a prior draft (5th incident), confirmed by `ls -la` returning "No such file or directory." Main session recovered by writing from the agent's response transcript directly.

- Source: [specs/2026-05-25-framework-improvement-prd.md](specs/2026-05-25-framework-improvement-prd.md)

---

### 26. Wave B Ensemble Synthesis — Post-Wave-A Framework State (2026-05-25)
**The finding:** Three parallel cold-context lenses (architect, adversarial, prompt-engineer) evaluated the framework's state after Wave A organizational improvements. All three reached the same structural finding independently: Wave A improved scaffolding and documentation but did not change what any hook actually checks, what condition produces a block, or what constitutes a QA pass. None of the Wave A changes affected enforcement behavior.

**Three convergent sub-findings (all three lenses, independent evidence citations):**
1. Delta-1 is half-complete and creates an active contract split — DISPATCHES.json lists both agents; the routing table in the skill file has no corresponding rows.
2. Delta-5 Tier A (doctrine-drift lint pass) is absent from disk — Wave A's cleanup has no preventing-recurrence mechanism.
3. The closed-loop measurement problem persists unchanged — governance-log emits `qa_fails: 0` on dates when documented fabrication incidents occurred.

**One unresolved divergence preserved:** Delta-5 Tier A sequencing vs. Action 1.1 sequencing. Architect lens (architecture-v2 critical path) and adversarial lens (empirical incident frequency) make internally consistent but contradictory sequencing recommendations. Surfaced as deliberate prioritization choice, not collapsed.

**Confidence:** 0.82 on convergent findings.

- Source: [meta/2026-05-25-ensemble-synthesis.md](meta/2026-05-25-ensemble-synthesis.md)

---

### 27. Must-Dispatch Compliance Re-measurement (2026-05-25)
**The finding:** Systematic re-measurement of must-dispatch compliance over a 14-day window (12 days with data), using the same methodology as the 2026-05-10 baseline. Finds the dispatch-compliance resolution rate dropped from 47% at baseline to approximately 24% in the re-measurement window — a tentative −23 percentage point decline, though confounded by schema drift mid-window (the `declared`/`missing` fields used for the baseline measurement no longer consistently appear on current block events). The re-measurement document carries this caveat but the headline framing in surrounding documents does not adequately reflect it.

**Key data:** Window 2026-05-11 through 2026-05-24. Sessions, classifications, non-quick turns, zero-dispatch non-quick turns, dispatch-compliance blocks, PM dispatches, and PM format compliance tabulated per day.

**Methodological note:** The confound (schema drift mid-window) means the reported decline should be treated as directionally informative but not as a confirmed regression figure.

- Source: [meta/must-dispatch-compliance-remeasurement.md](meta/must-dispatch-compliance-remeasurement.md)

---

### 28. Sprint A — Task Decomposition (2026-05-25)
**The finding:** Full task decomposition for Sprint A of the framework improvement plan. Sprint scope: three items — (1) classifier block-vs-emission ratio diagnosis (shipped first, gates batch commit), (2) file-existence check in the work-verification hook, (3) evaluative-reviewer write-reversal doctrine surface. Seven named tasks (SA-1 through SA-7) with owners, estimates, acceptance criteria, and dependency graph.

**Sprint window:** 2026-05-26 through 2026-06-08. Appetite: 10–14 working hours autonomous plus a kickoff session.

**Key acceptance criteria:** SA-4 (the file-existence check) requires three independent verification methods; SA-6 (integration test) must cover the "agent claims file written, file does not exist" case with a confirmed hook block in the governance log.

- Source: [specs/sprint-a-task-decomposition.md](specs/sprint-a-task-decomposition.md)

---

### 29. Sprint A Task-Decomposition Review — Architect Lens (2026-05-25)
**The finding:** APPROVE-WITH-NOTES (Round 1 of 2) from the architect reviewer on the Sprint A task decomposition. Four substantive findings: (1) ASCII dependency diagram contradicts the text — SA-4 is a parallel input to SA-6, not a sequential predecessor, as the diagram shows; (2) SA-5 acceptance criteria are weak — baseline test count not recorded, so "passes existing tests" cannot be verified; (3) SA-7's "scheduled" acceptance criterion is not equivalent to "will fire"; (4) SA-2 hypothesis H2 is too vague, H3 lacks a decision rule.

**Effect:** notes addressed in the decomposition's round-1-applied revision. Restores integrity of inline cross-references between this review and the decomposition document.

- Source: [specs/sprint-a-review-architect.md](specs/sprint-a-review-architect.md)

---

### 30. Sprint A Task-Decomposition Review — Adversarial Lens (2026-05-25)
**The finding:** NEEDS-CHANGES (Round 1 of 2, confidence 0.82) from the adversarial reviewer on the Sprint A task decomposition. Primary challenge: SA-1's Wiktor-gated architectural decisions (Q8, Q9) should not block SA-4 implementation — the file-existence check design can be finalized from empirical evidence alone without waiting for framing decisions. Secondary: SA-2 scope may expand once the regex is fixed; the decomposition should specify a scope-ceiling or the task becomes unbounded.

**Confidence framing:** 0.82 reflects genuine uncertainty about whether the SA-1 gate is strictly necessary; the reviewer acknowledges the architect lens may have information about Q8/Q9 dependencies not visible at the adversarial review point.

- Source: [specs/sprint-a-review-adversarial.md](specs/sprint-a-review-adversarial.md)

---

### 31. Sprint A — Goal G1 Measurement Baseline (2026-05-26)
**The finding:** Baseline snapshot file for the 30-day post-ship measurement of PRD Goal G1 (reduce undetected fabrication incidents to ≤1 per month within 30 days). Records the hook commit reference, governance-log line count, fabrication-detected entry count at baseline, and production-window start timestamp. Establishes the measurement rule and the denominator for the G1 success criterion.

**Baseline state:** governance-log total lines 7661; fabrication_detected entries at baseline 8 (1 operational confirmation + 7 from development testing — excluded from production window); Wiktor-discovered fabrication memos at baseline 5 (the documented incidents that drove the PRD). Production window starts at the baseline snapshot timestamp.

- Source: [meta/sprint-a-g1-baseline.md](meta/sprint-a-g1-baseline.md)

---

### 32. Action 0.1 — External Calibration Protocol (2026-05-26)
**The finding:** The one structural change the framework meta-evaluation identified as unsolvable from inside. Every internal compliance metric measures conformance to the framework's own rules; external calibration is the only channel that crosses the closed-loop boundary. This document specifies the protocol: cadence (weekly primary, optional mid-week secondary), sampling procedure, three-axis rubric, aggregate measurement format, and escalation criteria.

**Rubric axes:** (1) substantive correctness — does the artifact's claim hold under independent inspection?; (2) internal-vs-external gap — did the framework's QA report match the calibrator's verdict?; (3) process-cost ratio — was the ceremony proportionate to the artifact's value?

**Tooling:** a sampler script emits 5–10 randomly-sampled QA-PASS artifacts from the past N days with claimed deliverable, QA report block, and linked commit. Calibrator records verdicts in a weekly file.

**Escalation trigger:** two consecutive weeks with ≥2 DIVERGE verdicts triggers a framework-wide hypothesis: closed-loop problem has worsened, not improved.

- Source: [specs/action-0-1-calibration-protocol.md](specs/action-0-1-calibration-protocol.md)

---

### 33. Wiki Active-Use Design — Architect Lens (2026-05-26)
**The finding:** The architect reviewer's process design for active wiki-use within the governance framework. Proposes a wide trigger scope — 10 categories covering doctrine questions, n8n node behavior, hook behavior, agent dispatch contracts, and architectural decisions. Includes a session-start hook modification (inject a WIKI STATUS BLOCK into additional context with stale-page count, last-ingest age, and backlog count) and a pre-response verification step before any synthesis that falls into a wiki-applicable category.

**Key design premise:** the five categories where vault-specific knowledge demonstrably exceeds training-context coverage justify active query overhead even at low wiki population — the relevant pages are specialized enough that a single correct retrieval is worth the round-trip cost.

**Diverges from adversarial lens** on scope (wide vs. narrow) and readiness (now vs. after supply-chain stabilizes). Divergence preserved in synthesis document (Finding 36).

- Source: [meta/wiki-active-use-architect-lens.md](meta/wiki-active-use-architect-lens.md)

---

### 34. Wiki Active-Use Design — Adversarial Lens (2026-05-26)
**The finding:** A challenge to the active wiki-use premise from a cold-context adversarial reviewer. Two critical findings: (1) the auto-trigger pipeline has zero confirmed end-to-end completions in production — the active-use model presupposes a working supply pipeline that does not yet exist empirically; (2) a stale-wiki-query is epistemically worse than no query because the wiki's `source:` field and SHA binding signals "verified, authoritative" — a session retrieving a 35-day-stale answer has less uncertainty than warranted, which is a harder failure mode than silence.

**Verdict:** ARCHIVE-WITH-CARVE-OUT. The adversarial lens recommends deferring wide active-use until ingest velocity meets input velocity and ratified-content-page count is meaningful. Carve-out: vault-specific structural knowledge (CMDB-class: agent/hook/skill counts, event registrations) clearly earns active-use cost because training context cannot have this data.

**Contribution:** the carve-out logic becomes the operative scope boundary in the synthesis (Finding 36).

- Source: [meta/wiki-active-use-adversarial-lens.md](meta/wiki-active-use-adversarial-lens.md)

---

### 35. Wiki Active-Use Design — Prompt-Engineer Lens (2026-05-26)
**The finding:** A drop-in implementation design for wiki active-use trigger detection. Catalogs 10 trigger-pattern categories matched against prompt shape, then proposes the implementation as a hook modification and CLAUDE.md CRITICAL RULE block. Identifies 7 failure modes: (1) compliance theater (queries ritual, no genuine retrieval); (2) stale wiki surfaced as authoritative; (3) subagents lacking MCP access bypassing the rule; (4) context compaction stripping injected wiki context; (5) over-triggering on Quick tasks; (6) false negatives on vault-specific questions phrased as general questions; (7) bootstrap-period sparse wiki producing sparse results.

**Addresses failure modes proactively** rather than discovering them post-deployment. Aligns with the adversarial lens on the compaction and subagent constraints; diverges on the readiness threshold.

- Source: [meta/wiki-active-use-prompt-engineer-lens.md](meta/wiki-active-use-prompt-engineer-lens.md)

---

### 36. Wiki Active-Use Design — Synthesis (2026-05-26)
**The finding:** Main-session synthesis of three parallel cold-context lenses on wiki active-use design. Convergent findings across all three lenses: (1) the wiki has some value — no lens recommends deletion; (2) ingest velocity is below input velocity — supply chain is the binding constraint; (3) CLAUDE.md prose alone is insufficient compliance mechanism (~25% empirical rate); (4) subagents lack MCP access; (5) context compaction strips injected wiki context.

**Synthesized verdict:** ratify a narrow active-use rule scoped to four vault-specific knowledge categories, with explicit re-evaluation after 30 days of measurement. The adversarial carve-out logic (vault-specific structural knowledge) provides the scope boundary. Wide-trigger design deferred until ingest velocity stabilizes and ratified-content-page count reaches a meaningful threshold.

**Confidence:** 0.78 (lower than the adversarial lens's 0.82 because the synthesis adopts narrow scope, which the architect lens would consider under-ambitious). Divergent verdicts preserved without collapse.

- Source: [meta/wiki-active-use-synthesis.md](meta/wiki-active-use-synthesis.md)
- Lens inputs: [meta/wiki-active-use-architect-lens.md](meta/wiki-active-use-architect-lens.md), [meta/wiki-active-use-adversarial-lens.md](meta/wiki-active-use-adversarial-lens.md), [meta/wiki-active-use-prompt-engineer-lens.md](meta/wiki-active-use-prompt-engineer-lens.md)

---

### 37. External Ecosystem Scan — Broader Agent Harness Adoption Research (2026-05-25)
**The finding:** Research into a publicly available agent harness project (affaan-m/ecc — "The agent harness performance optimization system") as a potential adoption source. Three adoption shapes evaluated: (A) full plugin install, (B) selective port of specific components, (C) architectural read-only. Verdict: SKIP full install (catastrophic namespace collision risk; doctrine layer would conflict with framework's own CLAUDE.md, which is the source of truth for behavior); INVESTIGATE FURTHER for selective port of the security scanner component and token-optimization tools; adopt read-only pattern for architectural inspiration.

**Key risk finding for full install:** five agent fabrication incidents in the prior two-week session arc demonstrate the framework is operating near the edge of doctrine-control already. Adding a parallel CLAUDE.md-bearing stack would create a doctrine conflict with no clear resolution mechanism.

**Note:** star/fork counts from WebFetch summary were flagged as unverified (192K stars for a 4-month-old repo is implausibly high). Architectural claims treated as plausible based on predecessor repo's structure; counts explicitly marked for separate verification.

- Source: [specs/ecc-broader-repo-adoption.md](specs/ecc-broader-repo-adoption.md)

---

### 38. Framework Ecosystem News Scan — 2026 Week 21 (2026-05-25)
**The finding:** Investigation of five framework-adjacent items from the week's technology coverage. Verdicts: (1) agentmemory MCP — SKIP (the vault's existing retrieval-augmented memory stack already covers the same use case more structurally); (2) task-observer — INVESTIGATE FURTHER (mechanism compatible with hooks discipline but auto-approval is a compliance risk); (3) external skills collection ("106 skills") — INVESTIGATE FURTHER (repo not locatable at the expected URL; verify before evaluating content); (4) cache-miss cost research (12.5× penalty finding) — ADOPT (five documented triggers, two directly relevant to overnight-loop patterns, actionable mitigations available); (5) self-hosted sandbox feature — SKIP (requires a managed-agents platform, not available to CLI-only users).

**Highest-value item for immediate adoption:** the cache-miss 12.5× finding. Five trigger categories fully enumerated from primary documentation; two triggers (session restarts, context compaction) directly match the overnight-loop pattern.

- Source: [meta/2026-05-25-news-adoption-candidates.md](meta/2026-05-25-news-adoption-candidates.md)

---

### 39. Volatile-Source Citation Integrity — Anchor-Existence Beats Hash-Pinning (2026-06-01)
**The finding:** A SHA-256 citation binding (anti-fabrication) has a blind spot for sources that legitimately change often. Exempting them from hashing is correct for script-generated output but wrong for hand-edited doctrine, which is genuinely mis-citable. The resolution is a third granularity — enforce that the cited section *anchor* exists, dropping only the volatile whole-file hash. A four-lens analysis found "full-hash vs exempt" to be a false binary; the adversarial lens identified blanket exemption as an escape hatch and stale citations as the ignored risk. Web-grounded against external provenance practice (content addressing, immutable snapshots, version-ID pinning, canonicalization, fragment/anchor-scoped hashing, signed attestations) — fabrication-resistance and maintenance burden move together.

**Design principle:** grade a source exemption by *why* it resists hashing — `type: generated` (not fabricable → path-existence only) vs `type: schema-doctrine` (mis-citable → path + cited-anchor existence, stricter). An exemption must be narrower than "inconvenient to verify," and should restore a proportionate check rather than remove verification wholesale.

- Source: [volatile-source-citation-integrity](insights/volatile-source-citation-integrity.md) (insight file)

### 40. The Enforcement Layer Needs Its Own Meta-Verification (2026-06-02)
**The finding:** Once a system enforces rules with hooks/gates, it has created a second system that can be wrong — and its errors are quieter than the agent's. A BLOCK-class hook eventually blocks a *valid* output that resembles the failure it guards (a short negative finding read as a refusal; an unfenced `Label: value` report read as "no structure"), and a block reads as success so no one notices. An allow-list reference silently stops resolving when an asset is renamed/added, and the stale pass reads as clean. Fix: verify the verifier — **false-positive guards** (assert each BLOCK hook stays silent on valid look-alike input) and **structural resolution gates** (warn when any referenced name no longer resolves to a live asset).

**Design principle:** measuring enforcement by how much it catches counts only true positives; an enforcer that catches everything and blocks valid work looks like strictness but is broken. Measure the false-positive rate explicitly. Keep the resolution gate advisory until its own FP-rate is proven.

- Source: [enforcement-layer-needs-meta-verification](insights/enforcement-layer-needs-meta-verification.md) (insight file)

### 41. Installed Is Not Adopted — A Tool Without an Enforcement Binding Is Inert (2026-06-02)
**The finding:** A tool (MCP server, skill, hook) is adopted only when something causes it to be used at the right moment — not when it is merely present. Incorporation (present + documented) and enforcement (a runtime pull toward use) are independent axes. Judge enforcement per tool type: hooks self-fire; skills soft-trigger on description match; **passive tools (a code call-graph, a search index) have zero native pull** — without a rule or nudge at the decision point, the agent keeps reaching for its default move and the fully-installed tool contributes nothing.

**Design principle:** don't force-bind every new tool (that recreates over-enforcement). Sequence it — incorporate, instrument whether it gets skipped when it would have helped, then gate only on evidence. "Installed but consciously opt-in pending a usage baseline" is a legitimate end state; "installed and silently forgotten" is the failure.

- Source: [installed-is-not-adopted](insights/installed-is-not-adopted.md) (insight file)

### 42. Measure-Then-Gate — Blocking Enforcement Needs a Measured Failure Rate, Not Intuition (2026-06-08)
**The finding:** Across three enforcement decisions, the *blocking* option was correctly declined or deferred once real data was consulted — and the recurrence is the signal. A blocking gate to force a tool-recall habit was declined after the actual forget-rate measured 2.7% (4 of 149 instrumented turns); a constitution-blocker hook was built but shipped opt-in/unregistered rather than armed by default (blast radius on the highest-traffic files); a guardrail found emitting the wrong hook-protocol had been a silent no-op for 14 days. Enforcement is a cost (false positives, friction, blast radius), so the blocking variant must clear an evidence bar before it ships armed. Warn-first / instrument-first, then gate only if the data demands it. Quantifies the older "hooks are floors not ceilings" and "low-false-positive only" rules into a decision procedure.

- Source: [measure-then-gate](insights/measure-then-gate.md) (insight file)

### 43. A Wrong-Protocol Hook Silently No-Ops (2026-06-08)
**The finding:** A PreToolUse hook that emits the SubagentStop block-protocol shape (a `decision:block`) is silently ignored by the runtime — the edit proceeds, yet the hook appears active in logs (it even self-logs a "blocked" event). It can stay dead for weeks because nothing surfaces the gap. Protocol/event-type correctness is invisible to unit tests that check the hook's logic but not its wire-format against the actual event contract. Verify a blocking hook by observing it actually block in a live run, not just by its tests.

- Source: [wrong-protocol-hook-silently-noop](insights/wrong-protocol-hook-silently-noop.md) (insight file)

### 44. Workflow Sub-Agents Have the Full Tool Surface (2026-06-09)
**The finding:** Sub-agents spawned *inside a deterministic workflow script* have the complete tool surface — shell, file-read, dynamic tool-loading, and every MCP server the session has loaded. The "sub-agents cannot reach MCP" rule holds for ordinary task-delegation sub-agents but is **false for the workflow harness**. Verified across two live runs against fabrication-resistant ground truth. This unblocks converting *any* process skill (including execution-heavy ones) to a workflow, and lets a workflow gate on **execution evidence** (a command was really run) rather than report-presence — enforcement by construction. Caveat: a workflow agent only reaches servers the session has loaded, and the fabrication residue (a plausible "raw output" string without a real call) is mitigated by schemas, not eliminated.

- Source: [workflow-subagents-have-full-tool-surface](insights/workflow-subagents-have-full-tool-surface.md) (insight file)

### 45. Procedure Layer as Workflows (2026-06-09)
**The finding:** The framework's procedure layer (per-type process skills) is currently *prose the model is asked to follow*. The active direction converts each skill into a **deterministic workflow script** that makes the dispatch sequence happen by construction — routing-as-code, not execution-as-code — collapsing the prose-skill + dispatch-contract + enforcement-hook triplication into one executable source. Engine proven (entry #44); two worked conversion drafts built (one routing-class, one execution-class); adoption gated on a human output-quality calibration baseline, because dispatch-by-construction makes "did we dispatch?" tautological and useless as a metric. Explicitly does NOT fix fabrication or the dispatch-vs-integration gap.

- Source: [specs/procedure-layer-as-workflows.md](specs/procedure-layer-as-workflows.md) — with worked drafts at [specs/workflow-drafts/process-planning.draft.js](specs/workflow-drafts/process-planning.draft.js) and [specs/workflow-drafts/process-pentest.draft.js](specs/workflow-drafts/process-pentest.draft.js)

### 46. Documenting an Agent / Skill / Hook Framework (2026-06-09)
**The finding:** The established documentation frameworks (Diátaxis, arc42/C4, ADR/MADR, Keep a Changelog, standard-readme, docs-as-code) all assume a conventional code library. A framework whose primary artifacts are *agents, skills, and hooks* falls into a real gap with no cross-tool standard — and the way to fill it is to compose those frameworks around one borrowed convention: the **attributes-table per configurable entity** (the dominant pattern in config-heavy repos: Ansible modules, Terraform variables, CrewAI concepts). The composition: Diátaxis routing + an attributes-table reference schema (the unit of reference) + a MADR decision log with a single-authority rule that prevents competing "why" stores + date-based changelog. The honest limit: automated checks verify *consistency of what exists*, not *completeness of what's required* — completeness rests on a human publish-time gate, and trying to enforce it with a runtime hook was rejected as over-engineering. The live standard ships in the framework repo's `docs/documentation-standard.md`.

- Source: [documenting-agent-skill-hook-frameworks](insights/documenting-agent-skill-hook-frameworks.md) (insight file)

---

## Supporting Analysis (April 2026)

- [google-labs-catalog](meta/google-labs-catalog.md) — 12+ Google Labs tools mapped; Jules architecture comparison, Stitch MCP integration, Opal agent memory patterns
- [monitoring-baseline](meta/monitoring-baseline.md) — Iteration 0 KPI baselines from 815 governance log entries across 17 sessions (DAR 45.5%, tool usage patterns, MCP ratios)
- [prompt-compression-research](theories/prompt-compression-research.md) — Token footprint analysis (243K total, 8.6K always-on) and compression technique survey (caveman-speak, academic methods, Anthropic guidance)

---

## Research Directions (Deferred)

1. **Context rot vs exploration prompting** — does exploration resist degradation as context grows? Observed: at 650K tokens, response quality degrades ("semantic averaging" per Gemini).
2. **Mechanistic question** — what does exploration do to attention patterns? Does it activate different retrieval than extraction?
3. **Prompt analysis** — 169 messages analyzed from prior sessions. Phase 1 complete. Phase 2: compare with Agent Suite patterns.
4. **Observability v2** — design-complete (2026-04-19). Catalogs 35 events (P0–P3), prescribes 4-tier aggregation strategy, lists 9 derivable conclusions. Two hooks (session-start-log, pre-compact) must be wired before P0 capture. See research/2026-04-19-observability-design-plan.md.
