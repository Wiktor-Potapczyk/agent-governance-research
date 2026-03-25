# Task Classifier Underestimates Complexity

Task classifiers correctly identify task TYPE (Build, Research, Planning, etc.) but consistently underestimate what is actually needed. Tasks get less attention and research than they deserve because the classifier answers "what kind of task is this?" but never asks "is this more complex than it looks?"

## Evidence

A file hierarchy design task was classified as Planning and nearly went straight to design without web research. Subsequent research discovered the Memory Bank pattern, 200 Stateless Sessions approach, and other frameworks that fundamentally changed the design. The classifier was correct about the type but wrong about the depth required.

## Why Adding Another Label Fails

Adding "DEPTH: Deep" is just another classification that can be silently wrong. The fix is **mandatory reasoning** — the classifier must visibly question its own assumptions before committing to an approach.

## What the Classifier Should Do After Typing the Task

1. Ask: "What am I assuming about this task?"
2. Ask: "What's unverified — could I be wrong about the approach?"
3. Ask: "Is there prior art or existing knowledge I'm ignoring?"
4. Only THEN commit to an approach

This reasoning should be VISIBLE in the output, not hidden. The user should see the classifier thinking, not just announcing.

## How to Apply

- Add a mandatory reasoning step to the task classifier AFTER the type matrix
- The reasoning questions should always fire, not just for "complex" tasks (because the whole point is you can't know complexity without asking)
- Research gates should be more aggressive — "if designing something new, research is default, not optional"
- Deep research loops should be suggested proactively when reasoning surfaces more than 2 open questions
