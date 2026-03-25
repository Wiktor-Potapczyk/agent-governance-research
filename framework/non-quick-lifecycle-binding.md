# Non-Quick Lifecycle Binding: Task Lists as Increment Institutions

## The Insight

In AI agent systems with native task management tools, the task list IS the project increment. No new infrastructure is needed to define increment boundaries — the tool's own completion state provides the signal.

## How It Works

When an AI agent receives a multi-step request:

1. **Decompose** the request into individual tasks (creating a checklist)
2. **Execute** each task with full lifecycle treatment (classify, process, QA)
3. **Mark complete** as each task finishes
4. **All tasks complete** = increment boundary = trigger for integration testing

The visual representation (checkmarks in a terminal, completed items in a task list) is the institution. "All boxes checked" has a clear, unambiguous meaning that both the agent and the human operator can see.

## Why This Matters

The increment boundary problem in autonomous agent systems is: how does the system know when a batch of work is done and ready for integration testing? Most frameworks solve this with explicit signals ("user says we're done") or time-based triggers ("end of sprint").

The task list solution is simpler: the agent defines its own increment when it decomposes the work. Completion is observable. No external signal needed.

## The Constraint

This only works if task state is observable. In systems where task completion is tracked internally (session-scoped, not persisted), enforcement hooks cannot verify it — they can't read task state. The increment boundary is therefore soft-enforced (the agent's instructions say to pentest after all tasks complete) not hard-enforced (no hook blocks if it skips pentesting).

Hard enforcement happens at the tier level: once pentesting is invoked, hooks verify the PENTEST REPORT is produced. The trigger is soft; the execution is hard.

## Design Principle

Match enforcement to observability. If the system can see a state change (PENTEST REPORT in output), enforce it hard. If the state change is internal (all tasks completed), enforce it soft. Don't build brittle infrastructure to make internal state observable — accept the enforcement split.
