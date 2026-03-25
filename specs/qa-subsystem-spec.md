# QA Subsystem Specification

This document defines a three-tier quality assurance taxonomy for AI agent governance, from per-task falsification through per-increment pentesting to per-milestone systematic evaluation. It addresses the fundamental question of how to verify AI agent output quality when the verifier is also an AI.

---

## Foundational Constraint

QA is Popperian falsification. A PASS means "could not break it during the test window." It does not mean "correct." No component claims proof of correctness.

---

## 1. Three-Tier Taxonomy

| Tier | Name | Cadence | Scope | Actor | Output | Trigger |
|------|------|---------|-------|-------|--------|---------|
| 1 | QA (falsification) | Every non-Quick task | Single task output | Orchestrating agent (inline) | QA REPORT (PASS/FAIL per claim) | Classifier marks QA compound |
| 2 | Pentest (exhaustive) | Per increment | Whole increment output | adversarial-reviewer via pentest process | PENTEST REPORT (findings + untested surface) | Increment complete |
| 3 | Eval (systematic) | Per milestone | Whole prompt/component | Human runs promptfoo CLI | Eval dashboard + pass rates | Milestone review |

**Composition rule:** Tier N is a prerequisite for Tier N+1. A missing Tier 1 QA REPORT on any task in an increment means that increment's pentest is incomplete by definition.

---

## 2. Layer QA Definitions

| Layer | QA Scope | Actor | Mechanism | Pass Criterion | Human Residual |
|-------|----------|-------|-----------|----------------|----------------|
| L0: Classifier | Schema followed? Fields present? | Field-check hook | Structural regex | All required fields present | Whether TYPE assignment is semantically correct |
| L1: Process | Correct skill invoked? Output blocks present? | Dispatch compliance + step check | Dispatch check + SCOPE/REPORT check | MUST DISPATCH invoked; SCOPE present; QA REPORT present | Whether SCOPE correctly described the task |
| L2: Agent | Substantive, structured, non-error response? | Quality check hook | 3 structural checks (empty/error/wall) | All 3 pass | Whether reasoning is sound, not just structured |
| L3: Tool | Tool call succeeded? Expected data shape? | Inline in process skills | Return value inspection | No error; shape matches contract | Whether the right tool was called for the goal |
| **L4: QA-on-QA** | **Was QA thorough? Right thing tested?** | **Partially: Tier 2 pentest + Tier 3 eval** | **Exhaustion criterion + trap cases** | **Untested surface documented; eval threshold met** | **Irreducibly human.** |

---

## 3. Pentest Process Definition

| Field | Value |
|-------|-------|
| Cadence | Once per increment, at increment completion |
| Actor | Orchestrating agent dispatches adversarial-reviewer |
| Input | Increment's primary output artifact(s) |
| Test categories | (1) Boundary inputs (2) Adversarial inputs designed to bypass (3) Regression (4) Failure modes (bad input, missing data) (5) Integration (composes with upstream/downstream?) |
| Exhaustion criterion | At least one test per applicable category + explicit "Untested Surface" list naming skipped categories with reason |
| Output | PENTEST REPORT: increment ID, findings table (category/input/expected/actual/severity), Untested Surface list, Recommendation (SHIP / FIX-THEN-SHIP / ESCALATE) |
| Pass | No HIGH severity findings, or all HIGH have accepted mitigations |
| Fail | Loop back to Build with findings as task input |

**Pentesting is NOT review.** It does not check style, structure, or best practices. Pentesting is adversarial execution: "I am trying to make this fail."

---

## 4. Process-Step-Check Scoping Fix

### Problem
Hook scans last 200KB of transcript for any process skill invocation. Finds stale invocations from prior turns. Re-triggers blocks on correct subsequent turns.

### Root Cause
No turn boundary concept. The hook treats the transcript as a flat string, not a sequence of turns.

### Fix Design
Walk transcript entries in reverse. Use `"type": "user"` entries as turn boundaries. Only check the assistant content between the last user message and the end of transcript (= current turn).

### Regression Tests
1. Turn with process skill + valid SCOPE + QA REPORT -> PASS
2. Turn with process skill + missing SCOPE -> BLOCK
3. Subsequent turn referencing prior skill (no new invocation) -> no trigger (PASS)

---

## 5. Implementation Priority

| Priority | Task | Risk if delayed | Effort |
|----------|------|-----------------|--------|
| P0 | Fix process-step-check scoping bug | Active false blocks in every session | 30 min |
| P1 | Write pentest process skill | No per-increment testing process | 1 hour |
| P2 | Patch lifecycle playbook (Build + Review phases) | Playbook omits testing | 15 min |
| P3 | Add pentest process to classifier MUST DISPATCH | No enforcement of pentesting | 15 min |

---

## 6. Layer 4 Honest Assessment

**What is automatable:**
- Tier 2 exhaustion criterion forces explicit "Untested Surface" list -- shifts burden to human
- Tier 3 promptfoo trap cases provide regression coverage
- Process-step-check verifies QA was invoked and produced a report

**What is irreducibly human:**
- Whether the untested surface is acceptable
- Whether the trap cases are the right trap cases
- Whether a PASS reflects actual absence of bugs or exhaustion of the tester's imagination

**Design ceiling:** The Tier 2 untested surface list is the closest automatable proxy for Layer 4. It does not solve the problem -- it makes the gap visible so a human can judge it. Do not claim to exceed this.
