# Jules: A Production Claude Code Reference Implementation

Jules is a production autonomous Claude Code system built by a solo founder. It extends Claude Code into a 24/7 autonomous collaborator with interactive development on Mac, scheduled jobs in Docker, and Git-synchronized state.

**Source:** https://github.com/jonathanmalkin/jules

## Architecture

**6 layers:** Identity, State, Configuration, Infrastructure, Automation, Products

## What It Validates

- "Deterministic > Probabilistic" — hooks enforce, skills guide. Push behavior toward determinism whenever the pattern works.
- State management (a Terrain.md equivalent serves the same purpose as STATE.md)
- Layered enforcement (hooks, rules, skills)

## Actionable Patterns

1. **Rules directory** — decompose system instructions into individual files in a rules directory. The platform auto-loads all files. Cleaner and more modular than a single large instruction file.
2. **Investigation budget** — prevents endless research loops. Better than a circuit breaker (budget forces convergence, kill switch just stops).
3. **Bash safety guard** — PreToolUse hook blocking dangerous commands (rm, sudo, force-push). Deterministic safety boundary.
4. **Bash output compression** — PreToolUse hook reducing verbose Bash output to save tokens.
5. **Plan review enforcer** — PostToolUse hook gating implementation on plan approval. Similar to MUST DISPATCH but for the plan-to-build gate.

## Not Relevant for Interactive Use

- File communication / signal files — needed for scheduled/headless architecture, not interactive use
- Docker container infrastructure — local development doesn't need this
- Slack daemon, auth checks — different use case

## How to Apply

Use as reference when building new hooks or restructuring system instructions. The rules directory pattern is the most immediately useful.
