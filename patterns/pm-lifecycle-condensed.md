# PM Lifecycle Playbook for Solo Operator + AI Agents

A project management lifecycle designed for solo operators working with AI agent infrastructure. Combines Shape Up (fixed-time variable-scope cycles), Kanban (WIP limits, pull), PRINCE2 (viability gates), and Lean PDCA.

## 5 Phases

**Intake -> Shape -> Build -> Review -> Close.** Each has a kill exit except Close.

## 8 Fields (Compressed from 11)

Scope, breakdown, quality, progress, governance, risk, change, integration.

Dropped fields: scheduling (replaced by appetite), resources (replaced by agent routing), communication (replaced by async artifacts).

## 3 Artifacts

| Artifact | Purpose | Update Frequency |
|----------|---------|-----------------|
| PROJECT.md | Static scope — why this exists, what success looks like | Rarely |
| STATE.md | Dynamic status — current phase, decisions, blockers, next step | Per session/milestone |
| task_plan.md | Work items — incremental tasks with status | Every few messages |

## Core Loop: 5-Question Checkpoint

1. **What exists?** (Read STATE.md, task_plan.md — is the status current?)
2. **What matters?** (Are priorities still correct? Has anything changed?)
3. **What's happening?** (What's in progress, what's blocked, what's the oldest blocker?)
4. **What changed?** (Decisions made, scope changes, new risks)
5. **What's done?** (Does completed work meet acceptance criteria?)

Plus **Q6 at gates:** Is this still worth doing? (viability check)

## Circuit Breaker

Qualitative, not numeric. "Has this stalled with no value delivered?" not "did you exceed N days." Appetite is S/M/L sizing, not a time budget.

## Key Design Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Lifecycle model | Shape Up hybrid | Fixed-time variable-scope works for solo operators |
| Phase transitions | Question-driven, not deliverable-gated | LLM agents respond better to exploration prompts |
| Governance | Qualitative circuit breaker + business case question | Solo operators don't have fixed sprints |
| Feedback | Checkpoint protocol with agent delegation | External review (different agent) > self-review |

## Open Design Questions

- How does a PM orchestrator relate to the existing classifier-to-process-skill-to-agent chain? Options: (a) orchestrator replaces process skills, (b) sits above classifier as meta-layer, (c) invoked explicitly only.
- Cold-start: new users need jargon definitions
- Multi-project handling across shared resources
- Error recovery for failed agent dispatches
