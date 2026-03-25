# Three-Level Project File Hierarchy

AI agents need structured project state to maintain orientation across sessions. This three-level hierarchy separates concerns that otherwise get crammed into a single file that grows indefinitely.

## The Hierarchy

| Level | File | Purpose | Changes |
|-------|------|---------|---------|
| Project brief | `PROJECT.md` | Why this exists, what success looks like, helicopter view | Rarely |
| State | `STATE.md` | Current epoch — what's built, decisions, next milestone | Per session/milestone |
| Task plan | `task_plan.md` | Session working memory — open questions, small tasks, "what done looks like" | Every few messages |

## Key Insight

`task_plan.md` works when it's the OUTPUT of decomposition, not a manually written todo list. The pattern: decompose the problem (what questions persist? what do we need to answer? what do we need to do to answer them?) then that decomposition becomes the task_plan.md, then execute step by step.

## Why

Without separation, a single state file tries to do three jobs: long-lived project context, current session state, and granular task tracking. It keeps growing because it's doing three jobs. Separating these into purpose-specific files keeps each one focused and appropriately sized.

## How to Apply

Use decomposition to generate task_plan.md content. Don't write tasks manually — decompose the problem first, then the tasks write themselves. The hierarchy works when you front-load decomposition into planning.
