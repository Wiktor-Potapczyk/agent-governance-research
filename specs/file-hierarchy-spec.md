# Three-Level Project File Hierarchy Specification

This document specifies a three-level file hierarchy for managing project state in AI agent work sessions. It defines three files per project -- PROJECT.md, STATE.md, task_plan.md -- their contracts, templates, lifecycle rules, and the behavior of all automation that touches them. The design separates durable identity from volatile session state from ephemeral task scratch.

---

## 1. File Registry

| File | Level | Volatility | Loaded at session start | Who writes body |
|---|---|---|---|---|
| `PROJECT.md` | Identity (durable) | Changes rarely | On demand only | Human + save skill |
| `STATE.md` | Epoch (volatile) | Changes every session | Always | Save skill (body), Stop hook + PreCompact hook (frontmatter only) |
| `task_plan.md` | Scratch (ephemeral) | Changes during work | If present | Agent during work, PreCompact hook (snapshot) |

---

## 2. PROJECT.md

### Contract

PROJECT.md answers: "What is this project, and what has been built?"

It is the single source of truth for durable, constitutional information. Content placed here is treated as a stable reference that changes only when scope, architecture, or milestone completion warrants it. It is NOT a session log and NOT a status indicator.

**Write triggers:** Scope change, milestone completion, architectural decision becomes permanent, new key ID or external reference added, glossary term stabilized.

**Read triggers:** Agent or human needs project background not present in STATE.md, debugging requires original architecture, onboarding a new agent or reviewer.

**Classification tiebreaker:** If content might belong in either PROJECT.md or STATE.md, it goes to PROJECT.md.

### Sections

| Section | What goes here | Maintained by |
|---|---|---|
| `## Purpose` | One paragraph. Why this project exists. | Human |
| `## Success Criteria` | Numbered list. Measurable outcomes. | Human |
| `## Architecture` | System design, components, data flow. | Human + save skill |
| `## Built` | Cumulative completed features/milestones. Never deleted. | Save skill (promotes from STATE) |
| `## Key IDs and References` | Workflow IDs, API endpoints, external services. | Human + save skill |
| `## Glossary` | Domain terms specific to this project. | Human |
| `## Decisions` | Architectural decisions that are now constitutional. | Save skill (promotes from STATE) |

---

## 3. STATE.md

### Contract

STATE.md answers: "Where are we right now, and what is the next strategic move?"

It is always read at session start. It must contain enough context for the agent to resume work without reading PROJECT.md. It describes the current epoch -- the active milestone and its associated state. When a milestone closes, STATE.md is reset to reflect the next epoch; completed content is promoted to PROJECT.md.

STATE.md does not contain tactical steps. Those go in task_plan.md. STATE.md contains strategic WHAT -- direction, blockers, decisions made this epoch.

**Target size:** 60 lines or fewer.

### Staleness Rules

| Condition | Action |
|---|---|
| `updated` field >7 days from today at session start | Warn: "STATE.md may be stale -- last updated [date]. Verify before continuing." |
| `## Recent Decisions` entry older than 14 days | Flag for promotion to PROJECT.md or archival. |

### Sections

| Section | What goes here | Who maintains |
|---|---|---|
| `## Status` | One-line current state. | Save skill |
| `## Active Milestone` | Name, description, completion criteria. | Save skill |
| `## Next` | Strategic WHAT -- next 1-3 moves. Not tactical steps. | Save skill |
| `## Blocked` | Active blockers with date added. | Save skill |
| `## Recent Decisions` | Decisions made this epoch, not yet promoted. | Save skill |
| `## Built This Epoch` | Items completed since last reset. | Save skill |
| `## Work Files` | One-line index of active work files. | Maintain skill |

---

## 4. task_plan.md

### Contract

task_plan.md answers: "Exactly how do I complete the current task?"

It is created when work on a task begins, updated as steps are checked off, and deleted or archived when the task is complete. It is session-scoped scratch. If found at session start and it is older than 24 hours, the agent treats it as a previous session's artifact and reviews it before using or continuing it.

task_plan.md contains HOW -- specific steps, commands, acceptance criteria, intermediate notes, draft content. Nothing in task_plan.md is permanent.

### Sections

| Section | What goes here | Who maintains |
|---|---|---|
| `## Goal` | Single sentence. What done looks like. | Agent |
| `## Steps` | Numbered list. Specific, executable. Check off with `[x]`. | Agent |
| `## Acceptance Criteria` | Measurable conditions confirming completion. | Agent |
| `## Notes` | Intermediate findings, error output, drafts. Scratch pad. | Agent |
| `## Blockers` | Anything preventing progress. Temporary. | Agent |

---

## 5. Classification Test

Apply in order. Stop at the first match.

1. Would re-deriving this from scratch produce the wrong outcome? -> **PROJECT.md**
2. Does this describe current state that any session needs without reading PROJECT.md? -> **STATE.md**
3. Is this specific to the current work session and disposable after? -> **task_plan.md**
4. Is this a stable fact about environment, user, or tooling -- not project-specific? -> **MEMORY.md** (auto-memory)
5. **Tiebreaker:** if item matches multiple levels -> higher level wins

---

## 6. Promotion and Demotion Rules

### Promotion (upward -- to more durable)

| From | To | Trigger | Who |
|---|---|---|---|
| task_plan.md `## Steps` completed | STATE.md `## Built This Epoch` | Task completed | Save skill |
| STATE.md `## Built This Epoch` | PROJECT.md `## Built` | Milestone closed | Save skill |
| STATE.md `## Recent Decisions` | PROJECT.md `## Decisions` | Decision constitutional (>14 days or explicitly architectural) | Save skill |

### Archival

| From | To | Trigger |
|---|---|---|
| task_plan.md | `work/archive/` | Task completed or abandoned |
| STATE.md (full epoch) | `archive/snapshots/` | Milestone closed, epoch reset |

### No Demotion

Content never moves from a higher level to a lower level. If something in PROJECT.md needs to become STATE.md content, it means the classification was wrong to begin with.

---

## 7. Hook Specifications

### Stop Hook

Writes STATE.md frontmatter only (updated + last_action). Does NOT touch body. Derives last_action from last tool-use event (120 chars max). Non-blocking on failure.

### PreCompact Hook

Writes STATE.md frontmatter (same as Stop). Creates task_plan.md snapshot if none exists and active work is detectable. Does not overwrite existing task_plan.md.

### Save Skill Contract

The save skill is the only automation that writes STATE.md body content. Hooks write frontmatter only.

| Aspect | Stop/PreCompact hooks | Save skill |
|---|---|---|
| STATE.md body | Never touches | Rewrites |
| STATE.md frontmatter | updated + last_action | updated + last_action + status + milestone |
| PROJECT.md | Never touches | Appends selectively |
| task_plan.md | Snapshot if missing | Updates step completion |
| Trigger | Automatic | Manual invocation |

---

## 8. Session Lifecycle

1. **Session Start:** Read STATE.md. Check staleness. Check task_plan.md age.
2. **During Work:** Create task_plan.md for multi-step tasks before starting. Update as steps progress. Do NOT update STATE.md during work.
3. **Checkpoint (save):** Rewrite STATE.md body. Update frontmatter. Promote to PROJECT.md if criteria met.
4. **PreCompact:** Write frontmatter. Create task_plan.md snapshot if missing.
5. **Session End:** Write frontmatter only.

---

## 9. Error Recovery

| Scenario | Recovery |
|---|---|
| Hook failure | Stale `updated` field -> agent warns at next session -> manual save recovers |
| Corrupted STATE.md | Restore from snapshot. Apply known changes. Run save. |
| Sync conflict | Compare `updated` fields. Merge manually. Delete conflict copy. |
| Missing task_plan.md | Reconstruct from STATE.md `## Next` + session transcript |
| Missing PROJECT.md | Valid state (pre-migration or minimal project). STATE.md is sufficient for most sessions. |

---

## 10. Glossary

- **Epoch:** The period between milestone resets of STATE.md. One epoch = one major milestone.
- **Durable:** Content that survives epoch resets. Lives in PROJECT.md.
- **Volatile:** Content that changes every session. Lives in STATE.md.
- **Ephemeral:** Content disposable after the task ends. Lives in task_plan.md.
- **Checkpoint:** A point at which the save skill is invoked to curate STATE.md and promote content.
- **Promotion:** Moving content from a lower-level file to a higher-level file.
- **Constitutional:** A decision or fact that is now architectural -- defines the system, not expected to change.
- **Snapshot:** A copy of STATE.md made at epoch close or before migration.
