# Two-Tier Routing Architecture

In a multi-agent governance framework, routing tasks to the right agent requires separating two concerns: WHAT process to follow (determined by task type) and WHO does the work (determined by domain). Conflating these creates inconsistent routing tables.

## The Architecture

The chain: Hook -> Classifier (TYPE + DOMAIN + APPROACH) -> Process Skill -> Agent

### Key Decisions

1. **Process skills are bound to TYPE, not DOMAIN.** They define HOW work flows (steps, sequence, quality checks), not WHO does it.
2. **Single source of truth for domain-to-agent mapping is the classifier.** The APPROACH line names the specialist agent explicitly. Process skills say "if APPROACH names agents, use those instead of defaults."
3. **Domain tables are stripped from process skills** to eliminate inconsistent duplicates.
4. **Compound tasks route through decomposition** — broken into sub-tasks, each classified independently, then routed to process skills in order. One-level nesting cap prevents recursion.

## Why

Process skills had inconsistent domain tables (one had 8 domains, another had 1, another had 3). Adversarial review correctly identified that the APPROACH line and domain tables were contradictory mechanisms — two ways to pick an agent, with no clear precedence. Stripping tables and relying on APPROACH resolves the contradiction with a single source of truth.

## How to Apply

When building or modifying process skills, never add domain-specific agent tables. Domain routing lives exclusively in the classifier. Process skills stay lean and type-focused.
