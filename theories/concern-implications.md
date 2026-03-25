# Concern Implications Analysis: Dual-Surface Review of 27 Architectural Concerns

When building a governance framework for LLM agents, proposed solutions often look straightforward. This analysis examines 27 active architectural concerns on two surfaces: what each implies if left unaddressed, and what solving each as proposed actually requires. The analysis was synthesized from 3 parallel adversarial-reviewer batches. The result: many "simple" fixes are flawed, several concerns target the wrong layer entirely, and a handful of cross-cutting patterns dominate.

---

## Concern #1: Dark Zone (Presence Check False Confidence)

**If unaddressed:** The system has no way to detect when a model quotes context but then reasons from inline knowledge instead. Presence checks catch "didn't look" but not "looked and ignored" -- the more dangerous failure mode.

**If solved as proposed:** Adding a synthesizer to detect quote-then-ignore creates infinite regress -- the synthesizer itself is subject to the same dark zone. Any solution must be architectural (e.g., tool-gated data access), not another LLM layer.

**Verdict:** More research needed

**Critical finding:** The presence check creates FALSE CONFIDENCE -- it detects the easy failure and makes the hard failure invisible.

---

## Concern #2: Regex/Text-Parsing Fragility

**If unaddressed:** All hooks that parse classifier output from free text are brittle. A truncated observation window (e.g., 80KB tail) cannot see classifications made early in long sessions. Line-ending inconsistency on Windows can silently break any regex fix.

**If solved as proposed:** Targeted regex fixes reduce failure surface but don't eliminate the root cause: free-text parsing of LLM output. A structural solution (typed tool call, structured output) is needed eventually.

**Verdict:** Flawed solution (treats symptoms, not disease)

**Critical finding:** The observation window cannot see classifications at high token counts -- the hook literally cannot do its job in long sessions.

---

## Concern #3: Internal Routing Field Removal from Output

**If unaddressed:** A routing field stays visible in classifier output, consuming tokens and creating ambiguity about whether it's a routing signal or documentation.

**If solved as proposed:** Removing a field from output means no downstream consumer can ever read it without re-adding. Future wiring becomes permanently harder.

**Verdict:** Sound (with caveat: update all consuming components simultaneously)

---

## Concern #4: Agent Tiering (Visibility Levels)

**If unaddressed:** All agents remain visible in system instructions at negligible token cost (0.028% of 1M context).

**If solved as proposed:** The proposal conflates trimming verbose descriptions (useful) with tiering agent visibility (unnecessary).

**Verdict:** Flawed premise (the real problem is verbose descriptions, not agent count)

---

## Concern #5: System Instructions Decomposition

**If unaddressed:** The system instructions file remains monolithic but functional. Subagents receive the full file.

**If solved as proposed:** CRITICAL RISK. If the monolithic file is decomposed into a directory of rule files, it is undocumented whether subagents receive those files. Decomposition could silently break subagent governance with no error signal.

**Verdict:** More research needed

**Critical finding:** Subagent loading of decomposed rules is undocumented. This could silently break the governance layer everything else depends on.

---

## Concern #6: Unused Agents

**If unaddressed:** Some agents are allegedly unused, but the specific list is never identified. Unused agents consume zero runtime resources.

**If solved as proposed:** Deleting agents without identifying which ones are unused risks removing agents needed for rare but important tasks.

**Verdict:** Flawed premise (unspecified target, wrong diagnosis)

---

## Concern #7: Single-Type Integration Test

**If unaddressed:** The system remains untested against real work.

**If solved as proposed:** Testing with one task type (e.g., Build) does not exercise Research, Analysis, Planning, or QA code paths. Using it as "the integration test" creates false confidence.

**Verdict:** Flawed solution (insufficient coverage -- one task type cannot validate a multi-primitive system)

---

## Concern #8: Context Rot Monitoring

**If unaddressed:** Output quality degrades over long sessions with no detection mechanism.

**If solved as proposed:** "Monitor quality" requires manual inspection -- contradicting automation goals. Hooks detect syntax (field presence) not semantics (field quality). No automated semantic monitoring is feasible within current constraints.

**Verdict:** Permanently unresolvable (within current architecture)

**Critical finding:** Hooks detect syntax, not semantics. Context rot is a semantic problem. The tool doesn't match the problem.

---

## Concern #9: Recursion Documentation

**If unaddressed:** Recursion depth cap remains documented only in architecture docs, not enforced mechanically.

**Verdict:** Already resolved (documentation preference, not architectural gap)

---

## Concern #10: Simplicity Gap

**If unaddressed:** System complexity (hooks, skills, types, enforcement chains) remains high.

**If solved as proposed:** Reducing agent count doesn't simplify routing, enforcement, or hook chains -- those are the actual complexity drivers.

**Verdict:** Flawed premise (complexity lives in enforcement chain, not agent registry)

---

## Concern #12: Eval Framework Proxy Problem

**If unaddressed:** No automated testing of classifier behavior.

**If solved as proposed:** Testing raw API calls doesn't match the production delivery mechanism (skill-based delivery in an agent framework). A passing eval doesn't guarantee live behavior. No eval targets the critical failure mode: classification drift under conversational pressure in long sessions.

**Verdict:** Flawed solution (proxy doesn't match production path)

---

## Concern #13: Evaluation of Implication-to-Dispatch Chain

**If unaddressed:** No automated validation that implication analysis correctly produces dispatch entries.

**If solved as proposed:** The architecture explicitly allows "none" as a valid dispatch output. A rules-based eval against fixed expected outputs either over-constrains or under-constrains. Retrospective audit of real sessions produces better ground truth.

**Verdict:** Flawed solution (structural mismatch with architecture)

---

## Concern #14: Dark Zone A/B Testing

**If unaddressed:** No empirical measurement of dark zone failure frequency.

**If solved as proposed:** A/B testing in a test harness doesn't reproduce the production delivery mechanism (tool results vs. text input). The divergence threshold is arbitrary.

**Verdict:** More research needed

---

## Concern #16: Eval Framework Vendor Dependency

**If unaddressed:** The eval framework depends on a single vendor with potential lock-in.

**If solved as proposed:** No alternative frameworks were evaluated. The window to evaluate alternatives is before deep integration, not after.

**Verdict:** Sound (evaluate alternatives before committing)

---

## Concern #18: Block Event Logging

**If unaddressed:** When hooks block actions, the block event may not be logged. The governance log skips during retry cycles -- exactly when logging matters most.

**Verdict:** Sound (blocking hooks must self-log)

---

## Concern #19: Implication Field Logging

**If unaddressed:** Free-form prose with special characters is not reliably captured. Only the last turn's classification is logged.

**Verdict:** Sound (but depends on per-turn logging fix)

---

## Concern #20: Subagent Pass/Fail Logging

**If unaddressed:** No record of whether subagent output passed or failed quality checks.

**If solved as proposed:** NOT a trivial change. Requires restructuring script block paths and addressing encoding issues (UTF-8 with BOM from certain write methods corrupts log data).

**Verdict:** Sound (but implementation estimate is wrong)

---

## Concern #21: Mandatory vs Opportunistic Dispatch Tracking

**If unaddressed:** No way to distinguish required vs. optional agent dispatches.

**If solved as proposed:** Agent type strings may not normalize identically to declared dispatch entries. String normalization is the hidden complexity.

**Verdict:** Sound (with normalization caveat)

---

## Concern #22: Session Boundary Events

**If unaddressed:** No explicit session start/end markers in logs.

**If solved as proposed:** The proposed hook events may not exist in the SDK. Session boundaries are already inferrable from existing data.

**Verdict:** Flawed premise (events may not exist; workaround already available)

---

## Concern #24: Context Size Persistence

**If unaddressed:** Context size not tracked longitudinally.

**If solved as proposed:** The hook reads an 80KB tail of the transcript. The computed "context size" reflects the TAIL size, not total session context. Persisting this creates a false metric.

**Verdict:** Flawed solution (metric measures the wrong thing)

**Critical finding:** Every analysis built on this data would be wrong.

---

## Concern #25: Command Block Logging

**If unaddressed:** When a safety hook blocks a dangerous command, the full command is logged. If it contained credentials, the log becomes a credential store.

**Verdict:** Sound (security-critical, simple fix -- truncate before logging)

---

## Concern #28: D1 Agents Can't Spawn Specialists

**If unaddressed:** Platform constraint -- subagents cannot dispatch their own subagents.

**If solved as proposed:** Both mitigation paths fail. Escalation to D0 is soft governance with ~48% chain probability. Pre-decomposition at D0 defeats the purpose of specialist dispatch.

**Verdict:** Permanently unresolvable (platform constraint)

---

## Concern #29: Escalation Protocol (D1 to D0)

**If unaddressed:** Subagents that discover they need specialists have no reliable way to surface this.

**If solved as proposed:** CRITICALLY FLAWED. The proposal uses soft governance (instruction-following) to solve a problem the framework's own research proves soft governance cannot reliably solve. Three sequential soft compliance steps at 78.5% compliance each yields ~48% chain success probability.

**Verdict:** Flawed solution (contradicts own theory)

---

## Summary Table

| # | Concern | Verdict | Priority |
|---|---------|---------|----------|
| 1 | Dark Zone false confidence | More research needed | High |
| 2 | Regex fragility | Flawed solution | High |
| 3 | Field removal | Sound | Low |
| 4 | Agent tiering | Flawed premise | Low |
| 5 | Instructions decomposition | More research needed | CRITICAL |
| 6 | Unused agents | Flawed premise | Low |
| 7 | Single-type integration test | Flawed solution | Medium |
| 8 | Context rot monitoring | Permanently unresolvable | High |
| 9 | Recursion docs | Already resolved | None |
| 10 | Simplicity gap | Flawed premise | Medium |
| 12 | Eval proxy problem | Flawed solution | High |
| 13 | Implication-dispatch eval | Flawed solution | Medium |
| 14 | Dark Zone A/B testing | More research needed | Medium |
| 16 | Eval vendor dependency | Sound | Medium |
| 18 | Block event logging | Sound | High |
| 19 | Implication logging | Sound (depends on #30) | Medium |
| 20 | Subagent pass/fail | Sound | Medium |
| 21 | Dispatch tracking | Sound | Medium |
| 22 | Session boundaries | Flawed premise | Low |
| 24 | Context size persistence | Flawed solution | High |
| 25 | Command block logging | Sound | High |
| 28 | D1 can't spawn | Permanently unresolvable | Informational |
| 29 | Escalation protocol | Flawed solution | High |

## Cross-Cutting Patterns

### 1. The Observation Window Problem (#2, #8, #19, #24, #30)

Five concerns independently surface the same root limitation: hooks operate on a truncated tail of the transcript. Classifications made early in long sessions become invisible. Context size computations measure the window, not the session. Per-turn logging captures recent events but loses history. This is the single most impactful architectural constraint.

**Implication:** Any governance feature requiring full session history is fundamentally limited.

### 2. Proxy/Environment Mismatch (#12, #13, #14)

Three eval concerns share a structural flaw: the test environment doesn't reproduce the production delivery mechanism. All three would produce results that don't transfer to production behavior.

**Implication:** Retrospective audit of real sessions may be more valuable than synthetic testing.

### 3. Soft Governance Contradiction (#1, #8, #28, #29)

The framework's own research demonstrates soft governance (instruction-following) has a ceiling around 78.5% per step. Yet multiple proposed solutions rely on multi-step soft compliance chains. Solutions must be architectural, not instructional.

### 4. Implementation Estimate Errors (#20, #30, #31)

Multiple concerns are estimated as trivial but conceal encoding issues, loop restructuring, unverified prerequisites, and schema design requirements. Governance infrastructure carries hidden complexity. Budget 3-5x the initial estimate.

### 5. Flawed Premise Pattern (#4, #6, #10, #22)

Four concerns target the wrong layer or propose solutions for problems that don't exist as described. Not all concerns are valid. Adversarial review serves as a necessary filter against concern inflation.

### 6. One-Way Doors (#3, #5, #16)

Three concerns involve decisions that are difficult to reverse: removing a field, decomposing system instructions, committing to an eval framework. These warrant disproportionate scrutiny relative to their apparent simplicity. The question isn't "is this easy to do?" but "is this easy to undo?"
