# PM Lifecycle Model Justification: Why Shape Up Hybrid

This document synthesizes research into PM lifecycle models and justifies the specific hybrid chosen for the governance framework — Shape Up cycles with Kanban flow mechanics, PRINCE2 viability gates, and Lean PDCA improvement loops. It explains what was borrowed from each framework, what was rejected, and why.

## Why Not a Pure Framework

Every framework studied was designed for a team context (minimum 3 people). A solo operator + AI agents has a fundamentally different constraint profile:

| Constraint | Team assumption | Solo + AI reality |
|---|---|---|
| Communication overhead | Grows with team size | Near-zero (agents are stateless, invoked on demand) |
| Coordination | Needs meetings, ceremonies | Orchestrated by playbook rules |
| Context switching | Destructive for humans | Destructive for the ONE human; agents don't care |
| Planning fidelity | Shared understanding needed | Only one brain needs to understand the plan |
| Governance | Protects against organizational dysfunction | Protects against losing the thread across sessions |

This means: strip all team-ceremony overhead, keep structural discipline.

## The Hybrid: What Comes from Where

| Component | Source | Why this one wins |
|---|---|---|
| Fixed-time cycles with variable scope | Shape Up | Solo operator can't extend deadlines. Appetite > estimate. Circuit breaker prevents zombie projects. |
| Shaping before building | Shape Up | Pre-work de-risking maps to "default mode is research, not building." Shaping IS the research phase. |
| Continuous flow within cycles | Kanban | No sprints inside cycles. Work is pulled, not pushed. WIP limit = 1 active focus. |
| Business case viability gate | PRINCE2 | At every phase boundary: "Is this still worth doing?" PRINCE2 is the only framework that makes this MANDATORY and explicit. |
| PDCA for improvement | Lean | Universal. Applies at task, phase, and project scales. |
| Hill charts for progress | Shape Up | Uncertainty-aware tracking. Better than % complete for knowledge work. |
| Double-loop learning | Argyris | Single-loop: "Are we building it right?" Double-loop: "Are we building the right thing?" The orchestrator must operate at double-loop. |

## What Gets Explicitly Rejected

| Element | Rejected because |
|---|---|
| Scrum events (Daily Scrum, Sprint Planning, Review, Retro) | No team to synchronize. Solo reflection replaces ceremonies. |
| PMBOK 6 process groups as lifecycle | 49 processes is performative overhead for a solo operator. |
| SAFe anything | Designed for 50-125 people. Negative value at solo scale. |
| Persistent backlog | Shape Up's "no backlog" is correct — if something matters, it gets re-pitched. Stale backlogs are inventory waste (Lean). |
| Formal change control board | One person. Decision authority is inherent. |

## Phase Definitions

### Phase 0: Intake
**Purpose:** Capture the project idea. Decide if it deserves shaping.
**Artifact:** One-paragraph pitch (problem + why now + appetite).
**Kill here if:** Problem is vague AND operator can't articulate value in one sentence.

### Phase 1: Shape
**Purpose:** De-risk before committing. Research, not building.
**Artifact:** Shaped pitch document (problem, appetite, solution sketch, rabbit holes, no-gos, agent plan).
**Kill here if:** Research reveals problem unsolvable within appetite, or value doesn't justify cost.

### Phase 2: Build
**Purpose:** Execute. Deliver working increments. Pull work from the shaped pitch.
**Mechanics:** Kanban board, WIP limit: 1, hill chart tracking, increments delivered as completed.
**Circuit breaker:** If appetite exhausted without core value → STOP. Default is death.

### Phase 3: Review
**Purpose:** Evaluate what was built. Capture lessons. Decide: Ship / Polish / Extend / Kill.

### Phase 4: Close
**Purpose:** Formal closure. Archive, update indexes, free capacity.

## Feedback Loop Design

Three-layer hybrid:

### Layer 1: Flow-based (continuous, within Build phase)
- Visual board state, WIP limit, blocked items flagged immediately
- Source: Kanban

### Layer 2: Cadence-based (periodic, between increments)
- STOP after each increment. PDCA micro-cycle. Weekly zoom-out check.
- Source: Scrum Retrospective + Shape Up Cooldown + PDCA

### Layer 3: Gate-based (at phase transitions)
- Explicit viability question at every boundary: "Given what we now know, is this project still worth the remaining appetite?"
- Source: PRINCE2

## Kill Mechanism

### Circuit Breaker (automatic)
Fires when project hits appetite without delivering core value. Project STOPS. Default is death. Continuing requires active justification.

### Governed Kill (at gates)
Fires when viability check at any phase transition returns negative.

### Anti-Sunk-Cost Measures
1. Appetite set BEFORE work begins
2. No persistent backlog — killed projects don't lurk
3. Viability question is forward-looking: "Is REMAINING work worth REMAINING appetite?"
4. Lessons always captured — killing produces value

## Key Design Decisions Summary

| Decision | Choice | Primary Evidence |
|---|---|---|
| Base framework | Shape Up hybrid | Best solo-operator fit; fixed-time variable-scope matches real constraints |
| Flow mechanics | Kanban | Highest solo-operator value with lowest overhead |
| Viability gates | PRINCE2 | Strongest formal viability check |
| Improvement loop | Lean PDCA | Universal, any-scale, any-frequency |
| Kill mechanism | Circuit breaker + governed kill | Automatic default-to-death is strongest |
| Progress tracking | Hill charts | More honest than % complete for knowledge work |
| Feedback philosophy | Three-layer hybrid (flow + cadence + gate) | Each layer serves a different purpose |
| Backlog | None (Shape Up style) | Persistent backlogs are inventory waste |
| Learning loop level | Double-loop (Argyris) | Orchestrator must question assumptions, not just track progress |
