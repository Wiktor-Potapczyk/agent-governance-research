# Live System Over Specifications

When documentation and the live system disagree, the live system is always right. AI agents that trust specification files over actual system state propagate stale claims into project documentation, creating "constitutional lies" that compound over time.

## The Principle

**Rule: live system > work files > memory.** Never invert this.

## Evidence

A work file described a Code Node Adapter component that was never deployed. The live workflow had no such node. The agent had both the work file content AND the live system topology — but trusted the work file and documented a component that doesn't exist.

## Why This Compounds

- State management systems write status files from conversation context. If the conversation included stale work file claims, these propagate into status files as if they were true.
- Maintenance routines classify work files as KEEP/ARCHIVE but don't verify their ACCURACY against the live system. A perfectly organized but factually wrong work file is worse than a messy but accurate one.
- Upstream documents inherit whatever gets promoted from status files. If stale claims reach upstream docs, they become "constitutional" lies that affect all downstream decisions.

## How to Apply

1. Before delegating documentation/report tasks: cross-reference work file claims against the live system (fetch actual data, read actual code). Flag discrepancies — don't silently pick one.
2. When writing "Built" items to status files: verify they actually exist in the live system, not just in work files.
3. When work files bundle multiple things, treat each component independently — one being deployed doesn't mean the other was.
4. **Discrepancy between spec and live = ASK, don't assume the spec is right.**
