---
date: 2026-03-22
tags: [#research, #idea, #project/agent-suite]
insight_number: 18
---

# TaskCreate = The Increment Institution

## The finding

Claude Code's native task list (TaskCreate/TaskUpdate) IS the project increment. No new infrastructure needed. The terminal checkmarks are the visual institution. "All tasks completed" = increment boundary = pentest trigger.

The tool already exists. The insight is recognizing it as the lifecycle mechanism, not just a progress tracker.

## Evidence

- **Session observation (2026-03-22):** When executing P0-P4, the task list displayed as checkmarks in the terminal. Each `[completed]` marked a Tier 1 QA pass. When all 5 went `[completed]`, the increment was done — pentest fired.
- **PM lifecycle playbook:** Defines increments as "pull shaped item → build → review → done." The task list maps directly: TaskCreate = shape, in_progress = build, completed = done.
- **User observation:** "I've seen you marking checks on a list of tasks — this basically is completing an increment. And the checklist is the institution of the increment."

## What it changes

```
User gives work
  → Classifier decomposes into TaskCreate list (= increment defined)
  → Each task: classify → process skill → QA → TaskUpdate: completed
  → All tasks completed (visible as all checkmarks)
  → Pentest the increment before reporting back
  → Report to user
```

The lifecycle applies at every scale:
- **Task level:** classify → scope → execute → QA (already automated)
- **Increment level:** TaskCreate list → execute each → pentest (new, triggered by all-done)
- **Milestone level:** multiple increments → eval (human-triggered, promptfoo)

## The constraint

Hooks cannot read task state. TaskCreate/TaskList are session-internal tools — no hook payload exposes them. The increment boundary is therefore **soft-enforced** (classifier Step 6 instructs it, /pm checkpoint detects it) not hard-enforced (no hook can verify it).

This is acceptable because the increment boundary is a coordination concept, not a correctness check. The hard enforcement happens at the task level (hooks verify QA) and at the pentest level (hooks verify PENTEST REPORT).

## Connection to other insights

- **#15 (Recursive execution pattern):** Same 6-step pattern at every depth. TaskCreate makes the increment depth explicit and visible.
- **#16 (Two-layer hook purpose):** Compliance hooks work per-task (hard). QA hooks work per-increment (soft trigger, hard verification once invoked).
- **#17 (QA is Popperian falsification):** Each completed task = one falsification attempt. All completed = full increment falsification surface ready for Tier 2.
