# MCP Classification Tool -- Structural Fix for Transcript Scraping Brittleness

Current governance hooks parse free-form LLM text via regex to verify classification compliance. This is structurally brittle. The fix: make classification a structured MCP tool call with typed JSON input, enabling deterministic validation at the PreToolUse hook layer.

---

## The Problem

The Stop hook that checks classifier output (classifier-field-check) parses free-form LLM text via regex. This has proven brittle -- 5 bugs fixed and ordering issues persist. The fundamental issue: deterministic checks applied to probabilistic output format.

## The Proposed Fix

Build an MCP server with a `Classify` tool:

```json
{
  "implies": "User wants to evaluate...",
  "task_type": "Analysis",
  "domain": "general",
  "approach": "Dispatch architect-review",
  "missed": "Could miss...",
  "must_dispatch": ["process-analysis", "architect-review"]
}
```

A PreToolUse hook on this MCP tool reads typed JSON input -- no transcript scraping, deterministic validation. The classifier skill would call this tool instead of printing a text block.

## Why It Matters

- Current L0 exit gate is the most brittle hook -- 5 bugs fixed, still has ordering issues
- Critique: "transcript scraping is inherently brittle" points directly at this
- PreToolUse hooks on structured tool input are deterministic -- the strongest enforcement mechanism
- Moves L0 from post-check (Stop) to pre-constraint (PreToolUse) -- the direction governance should move across all layers

## Prerequisites

1. Build a minimal MCP server (local, stdio transport)
2. Register in MCP configuration
3. Update classifier skill to call the tool instead of printing text
4. Move classifier-field-check logic from Stop to PreToolUse on the MCP tool

## Status

Identified, not designed. This is an optimization to pursue after current enforcement stabilizes. The conceptual direction is sound: structured tool calls are inherently more validatable than free-text output.
