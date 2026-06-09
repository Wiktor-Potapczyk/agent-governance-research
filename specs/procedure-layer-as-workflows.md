# Procedure Layer as Workflows

**Status:** pilot — engine proven, two skill-conversion drafts built, adoption gated on a human calibration step.
**Date:** 2026-06-09

## The idea

The framework governs work in three layers:

1. **Recognition** — a classifier reads each task and decides its type (Research / Analysis / Planning / Build / QA) and what must be dispatched.
2. **Procedure** — per-type "process skills" describe, in prose, the steps the model should follow (scope → research → design → review → revise → quality-check, etc.).
3. **Enforcement** — hooks that block or warn at tool-use and stop time.

Layer 2 is prose the model is *asked* to follow. Measured step-compliance with that prose sits well below 100% — the same gap every prose-instruction system has. The proposal: convert the procedure layer from *prose the model follows* into **deterministic workflow scripts that make the dispatch sequence happen by construction**. The recognition layer stays a model decision; the procedure becomes code.

This is **routing-as-code, not execution-as-code**. The script encodes *which* agents are dispatched, in *what* order, with *what* typed handoffs and *what* gates. Each dispatched agent still works freely inside its step. The script never scripts *how* an agent reasons — that would just be a slower way to follow a hollow process.

## Why this is the right next layer

The founding design principle of the framework is "govern routing, not execution — enforce what gets dispatched, let agents work freely once dispatched." A workflow script that encodes the dispatch sequence + handoffs + gates *is that principle implemented as code*. It attacks the three worst measured pain points at the root:

- **Dispatch-compliance gap** — when the dispatch is the script, it happens ~100% by construction rather than depending on the model remembering.
- **Step-compliance gap** — the step order is the control flow, not a suggestion.
- **Triplication** — today a procedure is stated three times (prose skill + a machine-readable dispatch contract + enforcement hooks). A workflow collapses these into one executable source. This is a *net simplification*, not a fourth representation.

## What it does NOT fix (stated plainly)

- **Fabrication.** Every documented fabrication incident in this framework was caught by a human, never by a hook. Making dispatch deterministic would not have caught any of them. (Partial mitigation: schema-validated returns and an execution-evidence gate are *harder to fake* than free text — a side benefit, not a solution.)
- **The dispatch-vs-integration gap.** Making a dispatch happen does not guarantee its output is *used*.
- **The success metric.** Dispatch-by-construction makes "did we dispatch?" tautologically yes — so it is a useless success metric for a converted skill. The real metric must be **output quality / output-use**, which requires a human-rated baseline that does not yet exist. This is why adoption is gated (below).

## Three reframes that shape the design

1. **Routing, not execution.** The workflow encodes routing/handoffs/gates only. Agents reason freely inside steps.
2. **Gate on execution evidence, not report-presence.** A verification node must check that real work happened (a tool was actually run, an artifact actually exists on disk) — not merely that a correctly-formatted report block is present. Gating on format alone scripts performative compliance into a fast pipeline.
3. **Conditional, not mandatory.** Forcing a step on *every* task produces "confidence laundering" — a check that runs constantly and rubber-stamps everything. The vast majority of tasks are trivial and must be gated *out* before any workflow runs; and inside a workflow, verification/ensemble nodes must be trigger-gated (uncertainty / irreversibility / correction-frequency), never flat-mandatory.

## Engine proof (the gating question, now answered)

The single highest-risk assumption was whether a workflow's sub-agents can reach the tools a converted skill needs. Two live workflow runs settled it empirically: a workflow sub-agent has the **complete tool surface** — shell, file-read, dynamic tool-loading, and every MCP server the session has loaded. (Detail and the falsified assumption: see [the tool-surface insight](../insights/workflow-subagents-have-full-tool-surface.md).) This unblocks converting *any* process skill, including execution-heavy ones; the remaining gates are design and quality, not capability.

A first durable workflow — a parallel fan-out that inventories the whole setup (agents / skills / hooks / plugins / MCP servers) and returns evidence-backed counts — was built and run. Five parallel probe-agents each derived their counts from real tool calls and flagged what they could not verify; an independent verification pass reproduced every count exactly, with zero fabrication. This validated the fan-out-and-synthesize pattern on a real, useful task (a rolling setup audit).

## The two conversion drafts (worked examples)

Two process skills were converted to draft workflow scripts as worked examples — deliberately chosen to span the two skill *classes*:

- **A routing-class skill** ([`process-planning.draft.js`](workflow-drafts/process-planning.draft.js)) — scope+classify → optional research gate → design → mandatory parallel review (architect + adversarial, plus a conditional prompt reviewer) → a capped revise loop → an execution-evidence quality gate. The judgment points (research-needed? high-stakes? prompts-involved? revise-or-stop?) are expressed as **typed schema returns**, not prose. The revise loop is bounded; the quality gate verifies the plan artifact exists and carries acceptance criteria rather than trusting a self-reported pass.

- **An execution-class skill** ([`process-pentest.draft.js`](workflow-drafts/process-pentest.draft.js)) — scope → enumerate a typed attack surface → **parallel execute-agents that each run a real test and must return the literal tool output as proof** (a finding with no real output is schema-invalid) → synthesize a report with a mandatory untested-surface section and a code-derived (not self-reported) ship/fix recommendation. This class is where reframe #2 (gate on execution evidence) is native: the raw output *is* the gate.

Both drafts are reviewed (an architecture reviewer found and the author fixed concrete defects — a silent "empty review set reads as convergence" bug; a capped-items-never-reach-the-untested-surface bug; recommendations that trusted a sub-agent's self-report instead of deriving the verdict in code). Neither is adopted.

## Adoption gate

Adoption — replacing a live prose skill with its workflow — is gated on a short **human calibration step**: a person rates a handful of past "QA-passed" artifacts against their own quality bar. Without that baseline, there is no way to tell whether a converted skill *improves output quality* or merely guarantees dispatch (which it does tautologically). A model rating its own outputs is the circular trap the whole effort exists to avoid. Until the baseline exists, the conversions stay drafts.

## Sequencing

1. Engine proof — **done.**
2. Build a durable utility workflow to exercise the pattern (the setup-audit fan-out) — **done.**
3. Draft one routing-class + one execution-class conversion as worked examples — **done.**
4. Human calibration step — **pending** (the only remaining dependency).
5. Adopt one converted skill behind the calibration baseline; measure output quality, not dispatch-presence.
6. If it holds, convert the rest and retire the prose/contract/hook triplication for those skills.

Keep the pilot small and measure output quality directly — the program runs on metrics that have not yet been validated against a human bar, so over-investing ahead of that validation is the main risk.
