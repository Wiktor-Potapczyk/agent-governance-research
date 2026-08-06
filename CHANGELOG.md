# Changelog

All notable research additions and documentation changes.

## 2026-08-06 — Publishing a working system: seven new insights (INDEX #69-#75)

Findings from the publication pass that brought the framework repository back into step with the
private system it documents. The common thread is not new: it is that **four of the seven describe
a check that was passing while structurally unable to fail**, and every one of them was found by
running something rather than reading it.

### Added

- **[a-gate-that-cannot-fail-is-not-a-gate](insights/a-gate-that-cannot-fail-is-not-a-gate.md)** (Finding 69): three gates in one repository, all green, all checking nothing. Introduces arming the control as the verification discipline, plus the second-order trap that an armed control can itself no-op, with two worked instances of exactly that happening during the same audit.
- **[guarded-optional-import-is-two-programs](insights/guarded-optional-import-is-two-programs.md)** (Finding 70): a `try/except ImportError` forks the module, and the suite only ever runs the branch your machine has. The live defect: a fallback parser ignored indentation, inverting key precedence, so a hook reported valid input as invalid in the lowest-dependency configuration.
- **[running-ci-steps-locally-is-not-running-ci](insights/running-ci-steps-locally-is-not-running-ci.md)** (Finding 71): re-running a workflow's commands verifies the commands, not the environment. Enumerates what a local pass structurally cannot see, and the rule that an unreachable target platform makes CI the only oracle rather than a formality.
- **[token-scans-cannot-see-infrastructure-disclosure](insights/token-scans-cannot-see-infrastructure-disclosure.md)** (Finding 72): denylist scanning is blind to disclosure by shape. Includes the structural sweep that complements it, why a gate whose contents are the secret cannot ship with the artifact it guards, and the complication that an internal name used as matching logic cannot be renamed for free.
- **[deny-patterns-fail-on-command-spelling](insights/deny-patterns-fail-on-command-spelling.md)** (Finding 73): a regular expression over a command line blocks a spelling, and the operation has several. Sibling to Finding 68: that one is a pattern relaxed too far, this one is a pattern that was never wide enough.
- **[identity-is-two-fields-and-clone-copies-neither](insights/identity-is-two-fields-and-clone-copies-neither.md)** (Finding 74): author and committer are independent, tooling shows the first, and configuration silently fills the second. Also names the trap where a safeguard lives in a working copy rather than in the repository, so the clone made to work safely is the one without it.
- **[a-published-mirror-is-a-fork-not-a-copy](insights/a-published-mirror-is-a-fork-not-a-copy.md)** (Finding 75): the public tree is a sibling with its own deliberate edits, not a downstream snapshot. Measured refusal rate of 14 in 40 files, and the honest limit that marker checking verifies the transformation while only execution catches the semantic class.

### Changed

- **INDEX.md**: new section "Publishing a Working System: What the Gates Missed (August 2026)" carrying Findings 69 to 75.

## 2026-07-29 — Two-Gate Autonomy findings: two new insights (INDEX #67-#68)

### Added

- **[safety-gate-logs-are-mostly-your-own-tests](insights/safety-gate-logs-are-mostly-your-own-tests.md)** (Finding 67): a deny-gate's audit log was ~98.7% synthetic, written by the hook's own test suite into the production sink. Covers why this is worse than ordinary noise (test data is systematically unrepresentative, biasing exactly the frequency estimates calibration needs), why filtering a known placeholder value was insufficient, and the generalisation: decide at design time how a reader tells test records from real ones, and make the discriminator structural rather than a recognised value.
- **[narrowing-a-deny-pattern-opens-floor-holes](insights/narrowing-a-deny-pattern-opens-floor-holes.md)** (Finding 68): relaxing a deletion pattern under false-positive pressure un-blocked a strictly more dangerous case with no test failure. Documents the one-directional feedback asymmetry that erodes deny-lists over time, and the set-difference verification that forward assertions cannot substitute for.

### Changed

- **INDEX.md**: new thread "Two-Gate Autonomy: Licensing Agent Action (July 2026)" covering both findings and pointing at the framework repo's ADR-0007 and concept page for the model itself.

## 2026-06-11 — Workflow-enforcement adoption arc: two new insights (INDEX #65–#66)

### Added

- **insights/workflow-enforcement-first-contact-bugs.md** — Five engineering invariants that only surface when a prose process skill is first run as a deterministic workflow: args delivered as JSON string (object-only guards silently discard → degenerate ~400K-token runs; fix = parse-if-string + required-field HALT); named-workflow invocation resolves from session cache (mid-session edits invisible; rule = `scriptPath` always); resume is same-session-only; write-restricted agent types fabricate file paths (fix = default subagent + explicit FILE CONTRACT); enforcement gates derived verdicts from disk evidence through every failure, zero fabrication passed. Transferable to anyone wiring a deterministic workflow layer over LLM procedure. INDEX entry #65.
- **insights/skill-tool-only-hook-assumptions.md** — Hook-blindness bug class introduced when skills convert to workflows: three severity classes (hard misfire blocking legitimate dispatches — reproduced live twice; silent enforcement-gate dropout; benign name-list mention); audit method (grep hooks for skill names, classify by firing condition); fix pattern (treat Workflow tool_use resolving to a known process skill as semantically equivalent to that skill's Skill invocation at every detection point, but never arm sidecar-contract fallback from it — the workflow performs its dispatches internally). INDEX entry #66.
- **INDEX.md** — Entries #65 and #66 added under Core Discoveries.


## 2026-06-10 — Curation: 17 working-notes-grade files moved to archive/

### Changed

- **17 files moved to a new `archive/` directory** (from `patterns/` ×12, `framework/` ×3, `experiments/` ×2) per the curation pass: superseded working notes, operational checklists, and derivative summaries whose durable findings are carried by INDEX-cited research files. Verified before moving: zero inbound references from any other document (including the new INDEX entries #47–#64). Nothing deleted — git history and `archive/` preserve all content; an `archive/README.md` states the policy.


## 2026-06-10 — INDEX curation: 18 previously-unindexed research files indexed

### Added

- **18 new INDEX entries (#47–#64)** covering content that existed in the repo but had no INDEX entry:
  - **theories/** (7 entries): dark-zone-research, governance-depth-boundary, hook-enforcement-model, failure-modes-taxonomy, context-rot-research-directions, concern-implications, perplexity-synthesis
  - **theories/ (continued — agent teams)** (1 entry, dual-file): agent-teams-execution-model + agent-teams-reference
  - **patterns/** (5 entries): external-confidence, claude-code-patterns, routing-architecture, hook-signal-vs-cause, prompt-engineering-findings
  - **meta/** (3 entries): monitoring-points-analysis, suite-effectiveness-assessment, tool-usage-gap
  - **framework/** (1 entry): governance-landscape
  - **experiments/** (1 entry, dual-file): exploration-prompting-paper/README.md + exploration-prompting-research.md

- Archive-candidate moves were deliberately NOT applied — held for maintainer confirmation.
- Files classified as "covered-elsewhere" (19 files) and "leave" (9 files) also not touched.

## 2026-06-10 — ECC star count verified

### Fixed

- **`specs/ecc-broader-repo-adoption.md` + INDEX #37 note:** the long-flagged "192K stars — implausibly high, unverified" hedge resolved by querying the raw GitHub API (no summary-model in the path): 212,482 stars / 32,632 forks as of 2026-06-10. The original figure was accurate; the docs now state the verified number while keeping the verify-via-raw-API method caution.


## 2026-06-10 — Audit close-out: cross-reference, stale qualifiers, manifest comment

### Fixed

- **`.doc-consistency.json`:** removed a stale annotation claiming `insights/rubber-stamp-enforcement.md` was never created — the file exists on disk.
- **`insights/reconsideration-science.md`:** added the missing cross-reference to the fuller `theories/reconsideration-science.md` treatment.
- **`INDEX.md` Research Directions:** items 1 and 3 marked `(deferred; no active work planned)` — they read as active threads but have no ongoing work.


## 2026-06-10 — Flaw-audit fixes: dead vault-internal pointers, README currency

### Fixed

- **INDEX.md:** entry #20 and Research Directions item 4 pointed at five `research/...` working documents that were never part of this repo (vault-internal session artifacts; plain-text pointers, so the CI link check could not catch them). Annotated as vault-internal-not-included and re-pointed to the durable insight files that carry the conclusions.
- **README.md:** the research-layer narrative stopped at INDEX #40–#41; extended to cover #42–#46 (measure-then-gate, wrong-protocol-hook, workflow tool-surface engine proof, procedure-layer-as-workflows, documenting agent/skill/hook frameworks).
- **Correction note:** the 2026-05-26 entry below records `meta/ecc-broader-repo-adoption.md`; that file lives at `specs/ecc-broader-repo-adoption.md` (moved after the entry was written; per append-only changelog discipline the historical entry is left as written and corrected here).


## 2026-06-09 — Insight: documenting an agent / skill / hook framework

### Insights

- **insights/documenting-agent-skill-hook-frameworks.md** — Research distilled: the canonical documentation frameworks (Diátaxis, arc42/C4, ADR/MADR, Keep a Changelog, standard-readme, docs-as-code) all assume a conventional code library, leaving a real gap for a repo whose artifacts are agents/skills/hooks. The fill: compose those frameworks around the attributes-table-per-configurable-entity convention (Ansible/Terraform/CrewAI). States which frameworks transfer fully, partially, or not (SemVer does not — no pinned consumers), and the honest enforcement limit (automated layers check consistency not completeness; a runtime completeness hook was rejected as over-engineering). The derived standard ships in the framework repo. INDEX entry #46.

## 2026-06-09 — Procedure layer as workflows: engine proof + program spec + two conversion drafts

### Specs

- **specs/procedure-layer-as-workflows.md** — The program: convert the prose procedure layer (per-type process skills) into deterministic workflow scripts that make the dispatch sequence happen by construction (routing-as-code, not execution-as-code), collapsing the prose-skill + dispatch-contract + enforcement-hook triplication into one source. States the three reframes (routing-not-execution; gate-on-execution-evidence; conditional-not-mandatory), the engine proof, the adoption gate (human output-quality calibration), and what it explicitly does NOT fix (fabrication; dispatch-vs-integration gap; an as-yet-unvalidated success metric). INDEX entry #45.
- **specs/workflow-drafts/process-planning.draft.js** — worked routing-class conversion: scope+classify → optional research gate → design → mandatory parallel review (architect + adversarial + conditional prompt) → capped revise loop → execution-evidence quality gate. Judgment points are typed schema returns; the quality gate verifies the artifact on disk rather than trusting a self-reported pass.
- **specs/workflow-drafts/process-pentest.draft.js** — worked execution-class conversion: scope → typed attack-surface enumeration → parallel execute-agents that each run a real test and must return the literal tool output as proof (a finding with no real output is schema-invalid) → synthesis with a mandatory untested-surface and a code-derived (not self-reported) ship/fix recommendation.

### Insights

- **insights/workflow-subagents-have-full-tool-surface.md** — Sub-agents inside a workflow script have the complete tool surface (shell, file-read, dynamic tool-loading, every session-loaded MCP server) — unlike ordinary task-delegation sub-agents. Verified across two live runs against fabrication-resistant ground truth. Unblocks converting any process skill and enables gating on execution evidence rather than report-presence. INDEX entry #44.

## 2026-06-08 — Measure-then-gate + wrong-protocol-hook insights

### Insights

- **insights/measure-then-gate.md** — Blocking enforcement should be gated on a measured failure rate, not intuition. Across three decisions the blocking option was correctly declined/deferred once data was consulted: a tool-recall gate declined at a 2.7% forget-rate (4/149 turns); a constitution-blocker shipped opt-in rather than armed by default; a wrong-protocol guardrail found to have been a 14-day no-op. Enforcement is a cost — warn-first/instrument-first, gate only on evidence. Quantifies "hooks are floors not ceilings" + "low-false-positive only". INDEX entry #42.
- **insights/wrong-protocol-hook-silently-noop.md** — A PreToolUse hook emitting the SubagentStop `decision:block` shape is silently ignored by the runtime; it appears active in logs (self-logs a "blocked" event) while enforcing nothing, and can stay dead for weeks. Protocol/wire-format correctness is invisible to logic-only unit tests; verify a blocking hook by observing it block in a live run. INDEX entry #43.

## 2026-06-02 — Enforcement meta-verification + tool-adoption insights

### Insights

- **insights/enforcement-layer-needs-meta-verification.md** — Once a system enforces rules with hooks/gates, the enforcement layer is itself code with two silent failure modes: a BLOCK-class hook that blocks valid look-alike output (a block reads as success, so the false-positive is invisible), and an allow-list/registry reference that silently stops resolving on rename/add. Fix: verify the verifier — false-positive guards (assert each BLOCK hook stays silent on valid input) + structural resolution gates (warn on unresolved names). Measure the false-positive rate explicitly, not just true positives. INDEX entry #40.
- **insights/installed-is-not-adopted.md** — A tool (MCP server, skill, hook) is adopted only when something causes it to be used at the right moment, not when merely present. Incorporation and enforcement are independent axes; passive tools (call-graph, search index) have zero native pull. Sequence: incorporate, instrument whether it gets skipped when it would have helped, then gate only on evidence — don't force-bind prematurely. INDEX entry #41.

## 2026-06-01 — Volatile-source citation integrity insight

### Insight

- **insights/volatile-source-citation-integrity.md** — A SHA-256 citation binding has a blind spot for sources that legitimately change often; exempting them is correct for script-generated output but wrong for hand-edited doctrine (mis-citable). Resolution: enforce cited-anchor existence rather than file-content identity, graded by why the source resists hashing (`type: generated` path-only vs `type: schema-doctrine` path + anchor). Derived from a four-lens parallel analysis (the adversarial lens identified blanket exemption as an escape hatch and stale citations as the ignored failure) and web-grounded against external provenance practice (Trusty URIs, fragment identifiers, C2PA, SLSA, Memento). INDEX entry #39.

## 2026-05-26 — Framework evaluation + architecture v2 + ensemble methodology

### Framework architecture

- **framework/2026-05-25-framework-investigation.md** — Cold-context multi-lens empirical investigation of the framework's runtime state. Two parallel lenses merged. Key findings: Stop-chain overload (11 hooks vs. 1–3 elsewhere), session-start hidden dependency, ghost-agent miscount correction, deprecated routing still live in production, closed-loop measurement problem.
- **specs/agent-governance-architecture-v2.md** — 7-delta specification closing the gap between declared and runtime behavior. Resolves framing choice: CLAUDE.md stays authoritative; drift enforced via lint pass. Every claim traces to the framework investigation.

### Evaluation + PRD

- **meta/2026-05-25-framework-evaluation.md** — Multi-lens evaluation with five process diagrams. Architect verdict: DIVERGENT_AND_DEEP. Adversarial verdict: STRUCTURALLY FLAWED at the measurement layer. Synthesis: salvageable via deltas + external calibration. Confidence 0.88.
- **specs/2026-05-25-framework-improvement-prd.md** — Product requirements document for two shippable items: file-existence check on sub-agent write claims (closes highest-incidence empirical gap); external calibration protocol (the only loop-exit channel).
- **meta/2026-05-25-ensemble-synthesis.md** — Three-lens synthesis post-Wave-A. All three lenses independently find Wave A did not change any hook's detection behavior. One unresolved sequencing divergence preserved without collapse.

### Sprint A planning + review

- **specs/sprint-a-task-decomposition.md** — Full Sprint A task decomposition: seven named tasks, dependency graph, acceptance criteria, 10–14 hour estimate.
- **specs/sprint-a-review-architect.md** — APPROVE-WITH-NOTES (Round 1). Diagram contradicts dependency text; two acceptance criteria weak.
- **specs/sprint-a-review-adversarial.md** — NEEDS-CHANGES (Round 1, confidence 0.82). SA-1 gate may not need to block SA-4; SA-2 scope ceiling missing.

### Measurement + calibration

- **meta/must-dispatch-compliance-remeasurement.md** — 14-day re-measurement of must-dispatch compliance. Tentative decline from 47% baseline; confounded by mid-window schema drift.
- **meta/sprint-a-g1-baseline.md** — Baseline snapshot for 30-day G1 measurement (fabrication incident reduction target).
- **specs/action-0-1-calibration-protocol.md** — The one structural change unsolvable from inside: external calibration. Weekly cadence, three-axis rubric, aggregate measurement format, escalation criteria.

### Wiki active-use ensemble

- **meta/wiki-active-use-architect-lens.md** — Wide-scope process design for wiki active-use (10 trigger categories, session-start hook modification).
- **meta/wiki-active-use-adversarial-lens.md** — Challenge to the active-use premise. Verdict: ARCHIVE-WITH-CARVE-OUT. Two critical findings: supply pipeline has zero confirmed end-to-end completions; stale-wiki-query epistemically worse than silence.
- **meta/wiki-active-use-prompt-engineer-lens.md** — Drop-in implementation design. 10 trigger patterns, 7 failure modes addressed proactively.
- **meta/wiki-active-use-synthesis.md** — Main-session synthesis. Narrow active-use rule for four vault-specific knowledge categories. Confidence 0.78. Divergent verdicts preserved.

### Ecosystem research

- **meta/ecc-broader-repo-adoption.md** — Adoption research for external agent harness project. Verdict: SKIP full install (doctrine-conflict risk); INVESTIGATE FURTHER for selective security-scanner port.
- **meta/2026-05-25-news-adoption-candidates.md** — Week 21 framework ecosystem scan. Five items evaluated; cache-miss 12.5× finding is the immediate adoption recommendation.

### Documentation

- **INDEX.md** — 17 new entries (entries 22–38), numbered continuation from prior last entry.
- **README.md** — Three Research Threads table rows updated; new paragraph on 2026-05 evolution added.
