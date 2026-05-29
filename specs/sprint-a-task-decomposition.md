---
date: 2026-05-25
updated: 2026-05-25
tags: [project/agent-governance-research, planning, task-plan, meta]
status: active
sprint: A
window: "2026-05-26 → 2026-06-08"
appetite: "10-14 working hours autonomous + owner kickoff session"
---

> Adapted from internal research workspace. Cross-references to vault-internal artifacts have been stripped or genericized.

# Sprint A — Task Decomposition

Hub: agent-governance research repo · PRD: [[2026-05-25-framework-improvement-prd]]

---

## Scope (from sprint plan §Sprint A)

- **Item 3-rescoped** — classifier block-vs-emission ratio diagnosis (PRD AC3.1-3.3). Ships first because smaller; gates Item 1 batch commit.
- **Item 1** — file-existence check in `work-verification-check.py` (PRD AC1.1-1.4).
- **Q5 doctrine surface** — evaluative-reviewer Write reversal (PRD §9 Q5, moved from Sprint D per round-1 architect review).
- **Q8+Q9 architectural decisions** — incident-5 framing (Q8) + Item-1 detection mechanism (Q9), at sprint kickoff.

## Task list

### SA-1 — Sprint kickoff: Q5 + Q8 + Q9 surface to Wiktor

**Owner:** Wiktor-gated · **Estimate:** 15 min Claude prep + 15-30 min Wiktor session
**Type:** Decision

**Scope:** Surface three Q-items in one batched kickoff session so the sprint's build tasks have clean architectural decisions before code starts.

- Q5 (evaluative-reviewer Write reversal): proposed answer in PRD §9 Q5; confidence high; 15-min reversal if approved. Default: revoke blanket Write from adversarial-reviewer + architect-reviewer + code-reviewer; replace with path-scoped Write for report filing. Same-session smoke-test gated per the agent-frontmatter-tools-change-requires-session-restart reference.
- Q8 (incident-5 framing): proposed answer in PRD §9 Q8; ship Item 1 with adversarial's reframing acknowledged in §1 — "ergonomic automation of an already-working main-session verification."
- Q9 (Item 1 detection mechanism): proposed answer in PRD §9 Q9; combine Write-tool-trace-absence (primary signal) + path-existence check + tool_result-block parsing (architectural finding from architect-review round 1). NOT language-pattern-only (adversarial-lens flagged as structurally broken).

**Acceptance criteria:**
- Three Wiktor decisions captured in writing — file at `Projects/Agent-Governance-Research/calibration/sprint-a-kickoff-decisions.md` OR equivalent durable artifact OR STATE.md entry. (Calibration directory is created in Sprint C; for Sprint A use a work/-file pending that directory's creation.)
- Q5 outcome implemented same session if approved (15 min): revert agent frontmatter Write grants. Smoke-test deferred to next session per memo.
- Q8/Q9 outcomes recorded as inputs to SA-3 and SA-4.

**Dependencies:** none upstream. Gates SA-3 (Q9 informs the detection mechanism) and SA-4 (Q9 informs hook architecture).

**Falsifier:** Sprint-A kickoff session occurs but produces no written Wiktor verdict on at least one of Q5/Q8/Q9 — SA-1 fails; SA-3/SA-4 cannot start.

---

### SA-2 — Reproduce classifier block-without-emission case

**Owner:** autonomous · **Estimate:** 2-3 hours
**Type:** Investigation (Analysis primitive)

**Scope:** The PRD's original premise — `\bpm\b` rejects `pm-orchestrator` — was empirically falsified during PRD round-1 review (`re.search(r'\bpm\b', 'pm-orchestrator')` returns `True`). The 47-blocks-vs-42-emissions ratio (synthesis §3) therefore has a different cause. SA-2 finds the actual cause.

**Approach (sequenced sub-steps):**
1. Pull last 30 days of classifier-field-check entries from `.claude/hooks/governance-log.jsonl` — separate `blocked: true` from `blocked: false` records.
2. For each `blocked: true` where the actual MUST DISPATCH text contains `pm-orchestrator` (a false-positive block): capture the full dispatch text + the classifier-field-check.py code path that produced the block.
3. Hypothesis candidates:
   - **H1:** `dispatch_match.group(1)` at line 114 (`re.search(r'MUST DISPATCH:\s*(.+)', last_classifier_text, re.IGNORECASE)`) — the `(.+)` capture stops at newline. If the MUST DISPATCH line continues on a second line, only the first line is captured.
   - **H2:** Another regex elsewhere in classifier-field-check.py mis-classifies pm-orchestrator.
   - **H3:** No bug — the 47-vs-42 ratio reflects correct signal (some non-Quick classifications legitimately fail pm check).

**Acceptance criteria (AC3.1 from PRD):**
- File at `Projects/Agent-Governance-Research/work/2026-05-25-classifier-block-ratio-diagnosis.md` exists with: (a) reproducible failing input or "no failing input found", (b) specific code path producing any false negative, (c) verdict — bug-found / no-bug-documented / signal-is-correct.
- Falsifier: diagnosis file absent OR fails to identify a specific code path OR is ambiguous between "bug" and "signal."

**Dependencies:** none upstream. Gates SA-3.

---

### SA-3 — Apply Item-3 fix OR close G4 with "no-bug" verdict

**Owner:** autonomous · **Estimate:** 30 min (if no bug) — 2 hours (if bug + regression test)
**Type:** Build (conditional)

**Scope:** Based on SA-2 verdict:
- **If bug found:** implement the targeted fix in `classifier-field-check.py`. Likely candidates per H1: change `(.+)` capture to `(.+?)$` with `re.MULTILINE`, OR split capture from check (capture wider, check per-line).
- **If no bug:** document the signal-vs-noise determination in the diagnosis file; close PRD G4 with that finding.

**Acceptance criteria:**
- AC3.2 (if fix lands): regression test against ≥10 CLASSIFIER_AGENT values from `.claude/registry.json` INCLUDING `pm-orchestrator` as a required positive case; all 10 pass.
- AC3.3 (if no-bug): diagnosis document includes the determination — "no actual bug; 47-vs-42 ratio reflects [reason]."
- R6 mitigation: regression set also includes common false-positive substrings (`apm`, `pmsg`, etc.) — all blocked correctly.

**Dependencies:** SA-2. Conditional on diagnosis verdict.

**Falsifier:** If a fix lands and `re.search(<new_regex>, 'pm-orchestrator')` no longer returns True, OR any existing CLASSIFIER_AGENT value newly blocks — SA-3 fails.

---

### SA-4 — Build file-existence check in work-verification-check.py

**Owner:** autonomous · **Estimate:** 3-4 hours
**Type:** Build

**Scope:** ~20-30 LOC addition to `.claude/hooks/work-verification-check.py`. Per Q9 architectural decision from SA-1:
- **Primary signal:** Write-tool-trace absence — parse the assistant turn's `tool_use` blocks (Write + Edit invocations); collect set of paths actually written this turn.
- **Secondary signal:** path-existence check — for each Write-claim text pattern matched in the agent response, verify the claimed path exists on disk via `os.path.exists()`.
- **Parse both `assistant` blocks AND `tool_result` blocks** — sub-agent output appears in tool_result blocks per architect-review round 1 finding; current parsing at lines 100-140 only handles assistant blocks.
- **Detection trigger:** Write-claim text pattern matches (e.g., "wrote to", "file saved at", "created at", "written to disk") AND (path not in Write-tool-trace OR path does not exist on disk).
- **Emit:** `FABRICATION_DETECTED` to stderr + exit code 2 + append JSON entry to `.claude/hooks/governance-log.jsonl` per AC1.3 resolution.

**Acceptance criteria:**
- AC1.1: hook intercepts fabricated Write claim (mocked test case → exit 2).
- AC1.2: legitimate inline content (no Write claim language, no Write tool call) → no block.
- AC1.3: governance-log.jsonl entry with timestamp, agent_type, claimed_path, actual_exists, detection_source.
- AC1.4: batched same-commit with SA-3 outcome.

**Dependencies:** SA-1 (Q9 decision), SA-3 (single-commit batching).

**Falsifier:** any AC fails its mocked test case.

---

### SA-5 — Test suite for SA-4

**Owner:** autonomous · **Estimate:** 2 hours
**Type:** Build (test artifacts)

**Scope:** Add test cases to existing `test_work_verification_check.py`:
- **True-positive:** mock sub-agent response containing "I wrote the report to /tmp/fake.md" with no Write tool_use trace for that path → hook exits 2.
- **False-positive guard 1:** mock agent response with legitimate inline content + zero Write-claim language → hook does NOT block.
- **False-positive guard 2:** mock agent with Write tool_use trace for path X + response text mentioning X → hook does NOT block (the Write actually happened).
- **R6 regression sub-suite:** all canonical agent names from `.claude/registry.json` + common false-positive substrings (`apm`, `pmsg`) — confirm classifier-field-check still passes/blocks correctly.
- **R7 write-contention mitigation:** confirm governance-log.jsonl writes survive parallel hook invocation (acceptable: post-build process-lint corruption-detection alarm IF contention proves real).

**Acceptance criteria:**
- All new tests pass.
- Total test count vs prior baseline (whatever the current count is): higher.
- Existing tests still pass.

**Dependencies:** SA-4 (tests cover SA-4's code).

**Falsifier:** any test fails OR existing test regresses.

---

### SA-6 — Single-commit batch ship

**Owner:** autonomous · **Estimate:** 20 min
**Type:** Build (release)

**Scope:** Per PRD AC1.4, Item 1 + Item 3 fix (or no-bug closure) ship in ONE commit on `main`. Commit message:
- Subject: ≤72 chars, NDA-scrubbed.
- Body: lists both changes, references PRD §1 + §6 R5 problem-statement.

**Acceptance criteria:**
- One commit on `main` contains: `work-verification-check.py` changes (SA-4), `test_work_verification_check.py` additions (SA-5), classifier-field-check.py change-or-not (SA-3), `classifier-block-ratio-diagnosis.md` (SA-2).
- Git log shows ONE commit, not two.
- Pushed to origin (per the no-push-without-asking doctrine — ASK owner first; default to local commit only if owner absent from session).

**Dependencies:** SA-2, SA-3, SA-4, SA-5 all complete.

**Falsifier:** two commits OR commit landed on a feature branch OR commit message contains NDA-sensitive employer strings (per NDA scrub doctrine).

---

### SA-7 — Start G1 measurement window

**Owner:** autonomous (Sprint A close) + Wiktor (30-day audit point)
**Estimate:** 5 min setup, 30-day passive window
**Type:** Measurement

**Scope:** PRD G1 success criterion = hook-detected fabrications ≥ Wiktor-discovered fabrications over 30 days post-Item-1 ship.

**Approach:**
- At SA-6 commit time, record timestamp + governance-log line count to `Projects/Agent-Governance-Research/sprint-a-g1-baseline.md` (project root per Wiktor /loop directive — measurement-cadence file, not work-artifact).
- 30 days later (~2026-06-25): re-count governance-log `FABRICATION_DETECTED` entries vs new Wiktor-discovered fabrication memos in the memory folder.

**Acceptance criteria:**
- Baseline file exists at SA-6 commit time.
- Audit happens at +30d (manual reminder + entry in task_plan.md follow-ups track).

**Dependencies:** SA-6.

**Falsifier:** baseline file absent at SA-6 OR audit step not scheduled.

**SHIPPED 2026-05-26 00:03 (Wave-γ):** [[sprint-a-g1-baseline]] written at project root. Empirical baseline: governance-log.jsonl = 7661 lines; 8 fabrication_detected entries (1 from SA-6 sentinel verification confirming log path operational + 7 from CHECK-4 dev testing); 5 owner-discovered fabrication memos. Production-window start ts = 2026-05-26 00:02 — entries before this excluded from G1 measurement. Audit date: 2026-06-25.

---

## Sprint A task graph

```
SA-1 (kickoff: Q5/Q8/Q9)
  ├── (Q5 outcome → applied same session if approved)
  ├── (Q8 outcome → SA-4 §1 framing input)
  └── (Q9 outcome → SA-4 hook architecture)
       │
SA-2 (diagnose classifier ratio) ───┐
                                    ▼
                                 SA-3 (apply fix OR close G4)
                                    │
SA-4 (build file-existence check) ──┤
                                    ▼
SA-5 (tests for SA-4) ──────────────┤
                                    ▼
                                 SA-6 (single-commit ship)
                                    │
                                    ▼
                                 SA-7 (G1 baseline + 30d audit schedule)
```

## Risk cross-reference

| Risk (PRD source) | Mitigation in Sprint A | Owning task |
|-------------------|------------------------|-------------|
| R1 (Item 1 false-positive) | Combined Write-trace + path-check + tool_result parsing per Q9 | SA-4 + SA-5 |
| R5 (implementation-plan fabrication) | Sprint A handled inline per user override; `ls -la` after any sub-agent dispatch | All tasks |
| R6 (Item 3 regression) | Regression test set includes all canonical agent names + common false-positive substrings | SA-3 + SA-5 |
| R7 (governance-log write contention) | Post-build process-lint corruption-detection alarm | SA-5 |
| (R2, R3, R4, R8) | Out of Sprint A scope — owned by Sprint B/C/D respectively | — |

## Wiktor-gated decisions inside this sprint

- **SA-1 kickoff:** Q5 (Write reversal), Q8 (framing), Q9 (detection mechanism). Three decisions in one session.
- **SA-6 push:** push to origin requires owner approval per the no-push-without-asking doctrine — Sprint A defaults to local commit only if owner absent.

## Round-1 review revisions + preserved divergence

Both reviewers returned NEEDS-CHANGES (architect APPROVE-WITH-NOTES + adversarial NEEDS-CHANGES 0.82 confidence). Reports: [[sprint-a-review-architect]], [[sprint-a-review-adversarial]].

### Convergent fixes applied below

- **CR1 (architect) — SA-4 tool_result pre-step:** SA-4's first sub-task is now: inspect a real transcript JSONL containing an Agent tool call (target: `~/.claude/projects/C--Users-WiktorPotapczyk-Desktop-Vault/*.jsonl` recent files) — confirm `tool_result` content block structure carrying sub-agent text BEFORE writing parsing code.
- **CR2 (architect) — SA-2 H2 specifics:** H2 candidates are now: (a) `strip_fences` could eat a MUST DISPATCH inside a code fence; (b) `is_quick` check could fire before PM check causing skipped block. SA-2 enumerates these explicitly before exploring further.
- **CR3 (architect) — SA-5 baseline test count:** SA-5 records at start via `python -m pytest test_work_verification_check.py --collect-only -q | tail -1`. Falsifier "higher than baseline" becomes verifiable.
- **CR5 (architect) — SA-2 H3 decision rule:** If governance-log has <10 entries with `MUST DISPATCH` in triggering text, declare "insufficient live data" and fall back to synthetic test cases.
- **Architect bonus finding — PRD AC1.3 path:** SA-4 explicitly uses `.claude/hooks/governance-log.jsonl` (existing hook reality; PRD §9 resolved AC1.3 to this path). NOT `Projects/Agent-Governance-Research/governance-log.jsonl`.
- **Adversarial CRITICAL #1 — SA-5 FP guard for sub-agent reported Write failure:** SA-5 adds test case — sub-agent tool_result says "Write returned an error for X" with no Write trace + path absent → hook does NOT block (this is a legitimate failure report, not a fabrication). SA-4 detection logic must additionally check for negation/failure-language ("attempted", "tried", "returned an error", "failed") near the Write-claim pattern.
- **Adversarial WARNING — SA-7 baseline orphan-prevention:** SA-6 commit must add a wikilink to `sprint-a-g1-baseline.md` from this task-decomposition file's §Sprint A close section in the same commit. Compliance hook check enforced at commit time.

### Preserved divergence — Q-items for SA-1 kickoff agenda

Adversarial findings that resist convergent fix become SA-1 Wiktor-decision items added to the kickoff agenda alongside Q5/Q8/Q9:

**Q-A1 (NEW, from adversarial CRITICAL #3 + GAP):** Does Sprint A's scope (Item 1 + Item 3-rescoped) represent the highest-value investment, OR should it swap to synthesis §6 item 4 (`process-step-check.py` soft-to-hard upgrade — closes 53% MUST DISPATCH compliance gap)?
- **Proposed answer:** ship Sprint A as scoped because (a) 5 documented fabrication incidents have higher empirical incidence count than the 53% compliance rate (which is itself a soft-instruction baseline), (b) Item 1 has bounded scope and revert path, (c) the 53% gap closure is a Sprint B+ swap-in candidate per PRD §9 Q11.
- **What would falsify:** if a single calibration entry (Sprint C) shows hook-detected fabrications stayed flat or declined while MUST DISPATCH gaps remained unfixed AND drove >1 documented incident.

**Q-A2 (NEW, from adversarial CRITICAL #3):** Is the `ls -la` alternative (Wiktor's existing manual mechanism, formalized via bash alias + doctrine memo) sufficient — making SA-4+SA-5's 5-6h investment redundant?
- **Proposed answer:** SA-4 still adds value but the framing matters — it is "ergonomic automation of an already-working mechanism" (Q8 adversarial framing) NOT "closure of an unrecovered-failure gap." The hours are justified by removing manual `ls -la` friction across hundreds of future dispatches.
- **What would falsify:** if Wiktor judges the friction is low (e.g., he already has a `claude-ls` alias muscle memory) AND the 5-6h is better spent on Q-A1's synthesis §6 item 4.

**Q-A3 (NEW, from adversarial WARNING — SA-2 H3 retroactive):** If SA-2 returns H3 (no-bug, signal is correct), does the PRD's §3 framing get retroactively revised (synthesis §3 was wrong about Item 3's existence as a gap) OR does Sprint A close G4 with the no-bug verdict and move on without PRD revision?
- **Proposed answer:** close G4 with no-bug verdict; do NOT revise PRD §3 retroactively. The synthesis selected a candidate; the diagnosis surfaced no bug; that is a successful empirical verification, not a methodology failure.
- **What would falsify:** if multiple synthesis items, when investigated, also turn out to be no-bug — then the synthesis methodology itself is suspect and warrants meta-review.

**Q-A4 (NEW, from adversarial WARNING — SA-1 bundling):** Should Q5/Q8/Q9 be unbundled in the Sprint A kickoff session (one decision per turn) OR batched (efficient but risks Q8 framing question slipping past without resolution)?
- **Proposed answer:** batch with explicit Q8 resolution required BEFORE Q9 is approved. Q9's hook-architecture decision presupposes "yes, build the hook" — Q8 must be resolved first ("does SA-4 exist at all?"). Q5 stands alone with its own evidence.
- **What would falsify:** if Wiktor wants slower deliberation per Q; then unbundle.

### Adversarial findings deferred but not dismissed

- **CR4 (architect) — ASCII task graph:** diagram showing SA-2/SA-4 parallel after SA-1, converging at SA-6. The task graph in §Sprint A task graph above is updated:

```
SA-1 (kickoff: Q5/Q8/Q9/Q-A1-A4)
  ├── (Q5 → applied same session if approved)
  ├── (Q8 → SA-4 §1 framing input)
  ├── (Q9 → SA-4 hook architecture)
  └── (Q-A1..A4 → scope confirmation OR swap)
       │
       ├──> SA-2 (diagnose classifier ratio) ──> SA-3 (apply fix OR close G4)
       │                                              │
       └──> SA-4 (build hook + verify tool_result)    │
                  │                                    │
                  └──> SA-5 (tests for SA-4)           │
                              │                       │
                              └────────> SA-6 <───────┘
                                        (single-commit batch ship)
                                              │
                                              └──> SA-7 (G1 baseline + orphan link + 30d audit)
```

- **WARNING — Language-pattern load-bearing (adversarial):** acknowledged; mitigation deferred to Sprint A retrospective (post-30-day G1 audit). If verbatim-fabrication phrasings avoiding "wrote/saved/created" are observed in the 30-day window, SA-4 v2 widens the pattern set.

- **WARNING — SA-6 AC1.4 in no-bug branch:** acknowledged; if SA-3 is the no-bug branch, SA-6 batches the diagnosis `.md` with the SA-4 hook code in one commit (commit message must explicitly state "diagnosis-only + hook code — coupling preserved for revert atomicity even though no causal coupling exists").

- **NOTE — SA-7 orphan-prevention link:** baseline file at SA-6 commit time gets a wikilink from THIS task-decomposition file's §SA-7 task entry (added in the same commit). Compliance with stewardship rule preserved.

## Out of Sprint A scope

- Item 2 (SKILL.md MCP rows) — Sprint B.
- Item 4 (calibration protocol) — Sprint C.
- Item 5 (strategic decision) — Sprint D.
- AW-5 smoke-test re-verification — separate `Sub-agent Write-tool audit + fix` track in task_plan.
- Delta-5 + Action 0.1 + remaining 11 ensemble concerns — out of PRD scope.
- 30-day G1 audit re-measurement — scheduled in SA-7 but executes post-Sprint-A.
