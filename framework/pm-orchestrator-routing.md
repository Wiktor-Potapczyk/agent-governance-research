# PM Orchestrator Routing Integration (Open Question)

## The Question

Where does the PM orchestrator sit in the classifier routing chain?

The task classifier routes every non-trivial task to a process skill (Research → research process, Build → build process, etc.). The PM orchestrator manages project lifecycle (phases, checkpoints, viability gates). These two systems currently operate independently.

## The Tension

- The classifier fires on every user message and routes to process skills
- The PM orchestrator fires at checkpoints (between increments, at phase transitions)
- There is no mechanism that connects them — the classifier does not know about project phases, and the PM does not influence classification

## Options Considered

**Option A: PM as a classifier type.** Add "PM Checkpoint" as a TYPE in the classifier. When the user asks "where are we?" or "what's next?", classify as PM and route to the orchestrator. **Problem:** PM checkpoints should also fire automatically between increments, not only when the user asks.

**Option B: PM as a post-increment hook.** Fire the PM orchestrator automatically when all tasks in an increment complete. **Problem:** Hooks cannot read task state (session-internal). The trigger would need to be soft-enforced.

**Option C: PM as a skill invoked by the classifier's execution rules.** The execution rules say "when all tasks completed, pentest before reporting back." Could add: "after pentest, run PM checkpoint." **Problem:** This conflates two concerns.

**Option D: Keep them independent.** The classifier routes tasks. The PM manages the project. The user (or the model following instructions) invokes the PM skill at appropriate moments. **Current approach.**

## Status

Unresolved. Option D is the current approach by default. The question is whether the lifecycle benefits enough from automatic PM integration to justify the coupling. Insufficient production data to decide — needs observation across multiple real projects.

## What Would Resolve It

Run 2-3 real projects through the full lifecycle. Observe: does the model naturally invoke the PM at the right moments? If yes, Option D is sufficient. If it consistently forgets or invokes at wrong times, Option A or B becomes necessary.
