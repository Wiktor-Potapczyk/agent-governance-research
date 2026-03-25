# PM Field Criticality Tiers for Solo Operator + AI Agents

Traditional project management defines 11 knowledge areas (PMBOK) or equivalent field groupings. This document synthesizes research across PM frameworks to determine which fields are load-bearing for a solo operator working with AI agents, which are important but lighter, and which collapse to near-zero value.

## Tier 1: LOAD-BEARING (Without these, the system collapses)

| Rank | Field | Why Critical |
|------|-------|-------------|
| 1 | **Scope Definition** | Everything downstream depends on knowing what's in/out. Prevents gold-plating, enables kill decisions. |
| 2 | **Work Breakdown + Prioritization** | Can't execute what you can't decompose. Can't focus without ordering. |
| 3 | **Quality / Completion Criteria** | Without "done" definition, work expands infinitely. Agents need explicit acceptance criteria. |
| 4 | **Progress Tracking** | Solo operator's biggest failure mode is tunnel vision. Must know: am I stuck? |
| 5 | **Governance / Decisions** | No one challenges you. Must create artificial friction: kill mechanisms, business case checks, agent-based review. |

## Tier 2: IMPORTANT (Meaningful value, lighter implementation)

| Rank | Field | Why Important |
|------|-------|--------------|
| 6 | **Risk Identification** | "What could blow this up?" prevents wasted time. Short cycles help, but explicit rabbit-hole thinking catches what cycles don't. |
| 7 | **Change Handling** | Not formal change control — it's asking "is this scope expansion worth it?" before saying yes. |
| 8 | **Integration** | The mechanism that connects all fields. For solo, the risk isn't fragmentation (team problem) but tunnel vision and context loss. |

## Tier 3: COLLAPSED (Real for teams, near-zero for solo + AI)

| Rank | Field | Why Collapsed | What Survives |
|------|-------|--------------|---------------|
| 9 | Scheduling / Sequencing | No resource contention. No team coordination. | Appetite (time budget) + simple dependency notes |
| 10 | Resource / Role Assignment | One human. Agent selection is routing, not resource management. | Classifier routing handles this |
| 11 | Communication Rhythm | No team to sync with. | Weekly self-review + async artifacts |

## Field Implementation (Tier 1 + Tier 2)

### F1: Scope Definition
- **Tool:** Shape Up pitch format (problem + appetite + no-gos)
- **Artifact:** PROJECT.md frontmatter
- **Kill mechanism:** Circuit breaker when appetite exhausted without core value

### F2: Work Breakdown + Prioritization
- **Tool:** Flat ordered list with MoSCoW tags
- **Artifact:** task_plan.md
- **Prioritization:** Simplified WSJF: "What's the cost of NOT doing this now?"

### F3: Quality / Completion Criteria
- **Tool:** Definition of Done checklist (project-level) + acceptance criteria (per deliverable)
- **Artifact:** DoD in PROJECT.md, acceptance criteria in task_plan.md items

### F4: Progress Tracking
- **Tool:** Hill chart thinking (uphill = figuring out, downhill = executing) + throughput count
- **Artifact:** STATE.md status field per active scope

### F5: Governance / Decisions
- **Tool:** Three mechanisms: (1) business case self-check at cycle boundaries, (2) adversarial reviewer for major decisions, (3) circuit breaker on all work
- **Artifact:** Decision log in STATE.md

### F6: Risk Identification
- **Tool:** "Rabbit holes" thinking at project start + proximity check
- **Artifact:** Rabbit holes section in PROJECT.md

### F7: Change Handling
- **Tool:** Three-question gate: (1) Does this fit the appetite? (2) What gets cut? (3) Does this still serve the original problem?
- **Artifact:** Changes logged as decision entries in STATE.md

### F8: Integration
- **Tool:** Weekly self-review touches ALL active fields
- **Artifact:** STATE.md as single source of truth
- **Binding mechanism:** The 5 checkpoint questions

## What to DROP Outright (Zero Value for Solo + AI)

| Practice | Source Framework | Why Drop |
|----------|-----------------|----------|
| Change Control Board | PMBOK 6 | You're the only decision-maker |
| RACI matrix | PMBOK 6 | One person = all roles |
| Earned Value Management | PMBOK 6 | Complex cost tracking for solo is absurd |
| Communications Management Plan | PMBOK 6 | No team to miscommunicate with |
| Multi-level reporting | PRINCE2 | No Board to report to |
| Gantt charts / CPM / PERT | PMBOK 6 | No resource contention |
| Sprint ceremonies | Scrum | Talking to yourself is not a ceremony |
| SAFe anything | SAFe | Designed for 50-125+ people |
| Story points / velocity | Scrum | Meaningful for teams calibrating together; solo: just track throughput |

## The Integration Pattern

All frameworks solve integration with ONE central artifact. For this playbook:

```
PROJECT.md (static)          STATE.md (dynamic)           task_plan.md (work items)
|-- Problem                  |-- Current status            |-- Ordered list
|-- Appetite                 |-- Progress (hill positions)  |-- MoSCoW tags
|-- No-gos (scope)          |-- Active risks               |-- Acceptance criteria
|-- Success criteria         |-- Recent decisions           |-- Dependencies
|-- DoD                      |-- Blockers
|-- Rabbit holes             |-- Next action
```

**Key insight from the research:** For solo + AI, the integration mechanism is NOT a process or role — it's the artifact (STATE.md) plus a rhythmic checkpoint (weekly review). The solo operator IS the integrator by default. The risk isn't fragmentation (team problem) but tunnel vision and context loss between sessions.

### How AI Agents Fit

| PM Function | Agent Role | Mechanism |
|-------------|-----------|-----------|
| Scope boundary enforcement | Hooks (classifier, dispatch check) | Automated — fires on every interaction |
| Quality verification | Architecture reviewer, prompt engineer | Delegated — invoked per deliverable |
| Decision challenge | Adversarial reviewer | Delegated — invoked for major decisions |
| Progress tracking | Save skill + STATE.md | Semi-automated — human triggers, agent writes |
| Prioritization assist | Classifier APPROACH field | Automated — suggests method per task |
| Risk surfacing | Research agents / autonomous loops | Delegated — invoked when uncertainty detected |
