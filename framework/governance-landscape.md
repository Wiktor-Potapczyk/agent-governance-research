# Governance Landscape: Gap Analysis and Mechanism Matrix

This document presents the results of a two-pass analysis of 340 extracted governance mechanisms for AI agent systems. It identifies the three most actionable gaps, five unexpected findings ("surprises"), and catalogs ~180 unique governance-relevant mechanisms grouped by function.

## How to Read This

- **3 Gap Briefs** = what to build next (actionable)
- **5 Surprises** = mechanisms not previously considered
- **Matrix Appendix** = full catalog for reference

---

## Gap Brief 1: Tool-Usage Gap (Agent Skips Delegation)

**The failure:** The agent classifies correctly (TYPE + DOMAIN + APPROACH) then answers inline instead of delegating to the specified specialist. Root cause: "false completion signal after classification" — the agent treats classification as the work itself.

**Best mechanism: Stop Hook Delegation Verification**

A Stop hook checks whether the classifier's APPROACH named an agent AND whether the agent was actually dispatched via the Agent tool. If APPROACH says "delegate to specialist" but no Agent call was made, the hook blocks and forces delegation.

| Dimension | Value |
|-----------|-------|
| Evidence | Completion Gates: Stop hook blocks premature finishing. Quality Gates: Stop exit 2 enforces criteria. UserPromptSubmit: 25% → 90% skill activation via enforcement hook. |
| Build effort | Small — one script, regex matching on APPROACH line + Agent tool presence in transcript |

---

## Gap Brief 2: Classifier Drift (Over-classification as Quick)

**The failure:** Task classifier classifies as Quick when the task has depth signals (investigation, diagnosis, "why did X happen?"). Fixed significantly in v4 (Step 0 depth check, broadened Analysis, tightened Quick gate) but no enforcement that the classifier is followed correctly.

**Best mechanism: UserPromptSubmit Depth Signal Pre-Check**

Before the classifier runs, scan the user's message for depth signal patterns. If depth signals found AND the subsequent classifier output is Quick, inject context: "Depth signals detected. Verify Quick classification is correct."

| Dimension | Value |
|-----------|-------|
| Evidence | "Classification quality comes from conversational context, not prompt content." Epistemic planning gap: "system never assesses input before thinking." |
| Build effort | Small — add ~20 lines to existing hook |

---

## Gap Brief 3: Verification Gap (Build Step 5 Skipped)

**The failure:** The build process's live verification step sometimes skipped under time pressure. The model "forgets" to verify after building.

**Best mechanism: SubagentStop Quality Gate**

When a build agent finishes, SubagentStop fires. A prompt hook evaluates the last message: "Does the output contain evidence of live verification?" If not, the agent continues until verification is present.

| Dimension | Value |
|-----------|-------|
| Evidence | "SubagentStop quality gate — confirmed blocking capability but zero real-world implementations." |
| Build effort | Medium — new hook, needs prompt engineering for evaluation criteria, testing for false positives |

---

## 5 Surprises

### Surprise 1: Incident-Driven Hook Evolution

The most effective governance grew bottom-up from specific failure incidents, not top-down from research. One practitioner's governance grew from 1:6 judgment:automation to 4:5 — validation nearly matched automation in volume.

**Implication:** Don't design 10 hooks. Build the 3 gap briefs above. Wait for the next failure. Add a hook. Repeat.

### Surprise 2: Role Specialization from Tool Restriction

A builder/validator pattern works because the validator CANNOT write, enforced by tool restriction at the runtime level. "Same base model behaves as fundamentally different agents with different tool sets."

**Implication:** Consider tool restriction for specialist agents. A review agent that cannot write is structurally more trustworthy than one that is just told not to.

### Surprise 3: 17.2x Error Amplification in Multi-Agent Systems

Google/MIT research: naive multi-agent systems amplify errors up to 17.2x. Downstream agents accept upstream outputs uncritically.

**Implication:** Provenance tracking (who produced what) should be a medium-term goal.

### Surprise 4: Specification Gap (Tests Pass but Behavior Is Wrong)

A payment retry strategy silently changed from exponential backoff to fixed-interval — all tests passed. The specification was wrong, not the code. No current system detects "code is correct but implements the wrong thing."

**Implication:** Quality gates based on tests/linting are necessary but not sufficient. Domain-specific evaluator agents are the only mechanism found that addresses this.

### Surprise 5: PostToolUseFailure Recovery Injection

When tools fail, the error passes silently. A PostToolUseFailure hook could inject context explaining the error and recovery options. Currently unused.

**Implication:** Quick win — one hook, immediate value on every tool failure.

---

## Build Priority (Incremental)

| # | What | Effort | Gap Covered |
|---|------|--------|-------------|
| 1 | Stop hook: delegation verification | S | Tool-usage gap |
| 2 | PostToolUseFailure: recovery injection | S | Silent failures |
| 3 | UserPromptSubmit: depth signal pre-check | S | Classifier drift |
| 4 | SubagentStop: quality gate | M | Verification gap |
| 5 | Tool restriction for review agents | M | Role enforcement |
| 6 | SubagentStart/Stop logging | M | Provenance tracking |

---

## Matrix Appendix — Mechanism Categories

340 mechanisms extracted. After deduplication and filtering, ~180 unique governance-relevant mechanisms remain.

### Prevention (blocking bad things before they happen)

| Mechanism | Hook Event | Evidence Level |
|-----------|-----------|---------------|
| PreToolUse command safety gate | PreToolUse | Proven (multiple production) |
| Hard invariant enforcement (ABC) | PreToolUse | Tested (formal proof) |
| Coercive rule blocking (GaaS) | PreToolUse | Tested (red-team validated) |
| Recursion guard / circuit breaker | PreToolUse + state | Proven (production) |
| Blast radius classification | PreToolUse | Proven (production) |
| Skill-gated mandatory workflows | UserPromptSubmit + SessionStart | Proven (plugin) |
| Pipeline/SOP enforcement | Process skills | Proven (MetaGPT, ChatDev, Strands) |
| Tool restriction by role | Agent frontmatter (disallowedTools) | Proven (production) |
| Cascading permission revocation (MI9) | SubagentStart + state | Tested (simulation) |
| FSM conformance checking (MI9) | PreToolUse + state | Tested (formal) |
| Datalog reference monitor (PCAS) | PreToolUse + graph | Tested (formal proof) |
| Predictive enforcement (Pro2Guard) | PreToolUse + DTMC | Tested (simulation) |

### Detection (finding problems after they happen)

| Mechanism | Hook Event | Evidence Level |
|-----------|-----------|---------------|
| Stop hook completion verification | Stop | Proven (production) |
| SubagentStop quality gate | SubagentStop | Theoretical (zero implementations) |
| PostToolUse quality feedback | PostToolUse | Proven (production) |
| Drift detection (JSD, MI9) | PostToolUse window | Tested (simulation) |
| Trust factor scoring (GaaS) | PostToolUse cumulative | Tested (formal) |
| ARI risk scoring (MI9) | SubagentStart | Tested (static scoring) |
| Specification gap detection | Stop (evaluator agent) | Theoretical (no solution exists) |

### Correction (fixing problems when found)

| Mechanism | Hook Event | Evidence Level |
|-----------|-----------|---------------|
| PostToolUse context injection | PostToolUse | Proven (production) |
| PostToolUseFailure recovery injection | PostToolUseFailure | Theoretical |
| ABC soft invariant recovery | PostToolUse | Tested (formal) |
| Graduated containment (MI9) | Any violation | Tested (simulation) |
| Builder/validator loop | SubagentStop → rebuild | Proven (production) |
| Tool parameter modification (updatedInput) | PreToolUse | Theoretical (zero examples) |

### Monitoring (observing without intervening)

| Mechanism | Hook Event | Evidence Level |
|-----------|-----------|---------------|
| SessionStart context injection | SessionStart | Proven (production) |
| HTTP audit endpoint | PostToolUse HTTP | Proven (production) |
| ATS telemetry (MI9) | All hooks | Tested (simulation) |
| SubagentStart/Stop provenance logging | SubagentStart/Stop | Theoretical |
| SessionEnd cleanup/audit | SessionEnd | Theoretical |
| PreCompact state preservation | PreCompact | Proven (active) |
