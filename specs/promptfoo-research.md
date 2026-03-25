# Promptfoo Research: Mechanics and Evaluation Strategy

Research findings on using promptfoo for systematic evaluation of AI agent governance components. Covers the complete configuration schema, execution model, provider setup, assertion types, multi-variable prompts, and multi-turn conversation support.

---

## 1. Configuration Format (promptfooconfig.yaml)

Three required top-level keys:

```yaml
prompts:    # Prompt templates with {{variable}} placeholders
providers:  # Model endpoints (anthropic:messages:claude-sonnet-4-6, etc.)
tests:      # Array of test cases, each with vars + assert
```

### All Top-Level Keys

| Key | Type | Required | Purpose |
|-----|------|----------|---------|
| `description` | string | No | Human-readable label for the eval run |
| `tags` | Record | No | Metadata tags for organizing test suites |
| `prompts` | string/string[] | Yes | Prompts (inline, file://, chat JSON, JS/Python functions) |
| `providers` | string/string[]/ProviderOptions[] | Yes | LLM APIs (aliased as `targets`) |
| `tests` | string/TestCase[] | Yes | Test cases inline or path to CSV/JSON/JSONL |
| `defaultTest` | Partial<TestCase> | No | Default properties merged into every test case |
| `outputPath` | string/string[] | No | Where to write results (csv, json, yaml, html, txt, xml) |
| `evaluateOptions` | object | No | maxConcurrency (4), repeat (1), delay (0ms), cache (true) |
| `extensions` | string[] | No | JS/Python hook files for eval lifecycle points |

### Execution Model

Five-phase test loop:

1. **Load config** -- reads YAML, resolves file references, loads extensions
2. **Expand test matrix** -- Cartesian product of (prompts x providers x test cases)
3. **Execute** -- render prompt with Nunjucks, call provider API, capture output + latency + tokens + cost
4. **Assert** -- run all assertions. Deterministic locally; model-graded via grading LLM; custom JS/Python inline.
5. **Report** -- generate output with pass/fail per assertion, scores, side-by-side comparison

Key details:
- Default concurrency: 4 parallel API calls
- Results cached to disk by default
- When `_conversation` variable is present, concurrency drops to 1 (sequential)
- All assertions must pass for a test to pass (unless using `assert-set` with threshold)

---

## 2. Provider Setup (Anthropic/Claude)

### Model IDs

```
anthropic:messages:claude-sonnet-4-6
anthropic:messages:claude-opus-4-6
anthropic:messages:claude-sonnet-4-5-20250929
anthropic:messages:claude-haiku-4-5-20251001
```

### Full Config Options

```yaml
providers:
  - id: anthropic:messages:claude-sonnet-4-6
    config:
      temperature: 0.0
      max_tokens: 1024
      top_p: 0.9
      thinking:
        type: adaptive    # adaptive | enabled | disabled
        budget_tokens: 16000
      tools: [...]
      output_format:
        type: json_schema
        schema: { ... }
```

### Model-Graded Assertions

If `ANTHROPIC_API_KEY` is set and `OPENAI_API_KEY` is NOT set, model-graded assertions automatically use Anthropic. Override explicitly:

```yaml
defaultTest:
  options:
    provider: anthropic:messages:claude-sonnet-4-6
```

**Note:** Promptfoo was acquired by OpenAI (March 2026) but remains open-source MIT. The tool is model-agnostic and eval logic runs locally.

---

## 3. Assertion Types

### Deterministic (string/structure)

| Type | What it checks |
|------|----------------|
| `equals` | Exact match |
| `contains` / `not-contains` | Substring present/absent |
| `icontains` | Case-insensitive substring |
| `contains-all` / `contains-any` | All/any substrings |
| `regex` | Regex match |
| `is-json` | Valid JSON (optional schema) |
| `starts-with` | Output begins with string |
| `levenshtein` | Edit distance below threshold |
| `rouge-n` | N-gram overlap score |
| `latency` | Response time under threshold (ms) |
| `cost` | API cost under threshold ($) |

**Negation:** Any type can be prefixed with `not-`.
**Weight:** `weight: 2` makes an assertion count double in scoring.

### Model-Graded (LLM-as-judge)

| Type | What it checks |
|------|----------------|
| `llm-rubric` | General-purpose: grades output against free-text rubric |
| `factuality` | Output is factually consistent with reference |
| `context-faithfulness` | Output only makes claims supported by context |
| `context-recall` | Ground truth appears in context |
| `answer-relevance` | Output is relevant to the query |
| `g-eval` | Chain-of-thought evaluation (G-Eval framework) |
| `select-best` | Compare multiple outputs, pick best |

### Custom Assertions

| Type | Mechanism |
|------|-----------|
| `javascript` | Inline JS or `file://path.js` |
| `python` | Inline Python or `file://path.py` |
| `webhook` | POST to URL, expects `{pass: true/false}` |

### JavaScript Assertion Context Object

```typescript
{
  prompt: string;
  vars: Record<string, any>;
  test: TestCase;
  config: any;
  provider: Provider;
  providerResponse: ProviderResponse;
}
```

Return type: `boolean | number | GradingResult` where GradingResult has `pass`, `score`, `reason`, `componentResults`.

---

## 4. Multi-Variable and Multi-Turn Support

### Multi-Variable

Variables defined in `vars` section, substituted via Nunjucks `{{variable}}` syntax:

```yaml
tests:
  - vars:
      role: 'customer service'
      question: 'How do I return a product?'
```

Array vars expand into separate test instances (Cartesian product). Loading from CSV, JSON, JSONL, and Python functions supported.

### Multi-Turn (4 methods)

1. **Chat format** -- JSON array with role/content objects
2. **`_conversation` variable** -- accumulates history across test cases (forces concurrency=1)
3. **`conversationId` metadata** -- parallel conversation streams
4. **`storeOutputAs`** -- capture output as variable for subsequent test
