# Promptfoo Integration for Agent Governance Testing

Promptfoo is an open-source LLM evaluation framework that can systematically test agent governance prompts. This documents the integration strategy for testing task classifiers, scoring prompts, and other governance components.

**Note:** Promptfoo was acquired by OpenAI (March 2026) but remains MIT open-source.

## Configuration

Three keys: `prompts`, `providers`, `tests`. Cartesian product execution. Claude provider format: `anthropic:messages:claude-sonnet-4-6`.

## Assertion Types

| Level | Type | Examples |
|-------|------|---------|
| L1 Deterministic | regex, contains, is-json | "Output must contain TASK TYPE:" |
| L2 Logic | javascript custom | Custom validation functions |
| L3 Semantic | llm-rubric, context-faithfulness | "Does the classification match the expected reasoning?" |

## ROI Ranking of Prompts to Test

1. **Task classifier (HIGHEST)** — routes everything, has ground truth trap cases in the skill prompt
2. **Scoring prompts (HIGH)** — validated test rows, deterministic JSON, testable compliance rules
3. **Adversarial reviewer / Verification (MEDIUM)** — harder to define ground truth
4. **Process skills / Ensemble (LOWER)** — output is more subjective

## Phase 1 Plan

5-10 classifier trap cases, L1 regex assertions only (~1-2 hours). Proves the toolchain works before investing in complex assertions.

## Key Decision

Direct API testing, not webhook-based. Isolates the prompt from infrastructure concerns.
