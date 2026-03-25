# Checkpoints Must Delegate, Not Reason Inline

When running project checkpoints or status reviews, agents that answer from memory reproduce their own biases. Dispatching separate agents to read the actual files finds ground truth.

## The Principle

When running a checkpoint (status review, "where are we?" assessment), dispatch agents to read the actual files and report findings. Do NOT answer the questions from conversation context or memory.

## Evidence

A checkpoint was run inline — the agent produced a nice table by reasoning about what it remembered, not what the files actually said. Separate agents found real discrepancies: hook count wrong, agent count wrong, architecture doc stale. Inline reasoning reproduces your own biases. Agent reads find ground truth.

## How to Apply

Any checkpoint, status review, or "where are we?" request = dispatch agents to read status files, configuration files, and source of truth files. Report from agent findings, not from context.

This is the same principle as the "live system over specs" pattern applied to self-assessment: the checkpoint exists to catch drift, so running it from the same context that might have drifted defeats the purpose.
