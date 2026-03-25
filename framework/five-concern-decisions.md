# Five Concern Decisions: Adversarial-Reviewed Design Choices

Governance frameworks generate many proposed improvements. This document records five concerns that were analyzed via parallel adversarial review agents, where in every case the reviewers recommended a simpler, more targeted fix than the original proposal.

## The Pattern

Every adversarial agent recommended a simpler, more targeted fix than the original proposal. This demonstrates the framework's adversarial process producing better answers than initial reactions.

## The Five Decisions

### 1. Dark Zone (Terminal Synthesizer)

**Proposal:** Build a terminal synthesizer agent to ensure agent outputs are used in the final response.

**Decision: DON'T BUILD.** Agents cannot return directly to users in the current platform — a synthesizer just adds a hop. Build a Stop hook structural presence check instead (~50 lines of code). Measure the base rate first.

### 2. MCP Classification Tool

**Proposal:** Replace regex-based transcript scraping with a typed tool call for classification.

**Decision: DEFER.** Harden the regex with four targeted fixes: (a) switch from byte-offset to last-assistant-entry parsing, (b) multiline dispatch pattern, (c) case sensitivity normalization across hooks, (d) fence-type anchor in classifier output. Each is 1-3 lines.

### 3. MECHANISM Field

**Proposal:** Wire the quality verification field to auto-route tasks to verification or ensemble skills.

**Decision: REMOVE FROM OUTPUT, keep as reasoning step.** Don't wire it (requires 5 process skill edits, amplifies classifier errors). Don't strip it entirely (zero usage does not prove zero value). The field was already superseded by compound detection.

### 4. Agent Tiering (L0/L1/L2)

**Proposal:** Organize agents into visibility tiers to save context tokens.

**Decision: DON'T TIER.** Agent registry is ~280 tokens on a 1M context window (0.028%). Real bloat is verbose descriptions. Right action: trim verbose descriptions, delete genuinely irrelevant agents, add new agents to registry.

### 5. Rules Directory

**Proposal:** Decompose the system instructions file into individual rule files.

**Decision: USE CONDITIONAL LOADING.** The platform auto-loads rule files. Unconditional rules load at startup (same as the main config). Conditional rules with path frontmatter load only when matching files are read. This is the real token optimization — not tiering.
