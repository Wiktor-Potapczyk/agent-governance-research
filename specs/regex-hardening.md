# Regex Hardening for Transcript Hooks

## The Problem

Hooks that read LLM conversation transcripts to enforce governance rules face four reliability challenges: window size limits, false matches on quoted content, case sensitivity drift, and multiline field values.

## The Four Fixes

### 1. Window Sizing (80KB to 200KB)

Transcript-reading hooks read the last N bytes of a JSONL conversation file. If the window is too small, the classification block from the start of a turn can fall outside it when agent outputs are large (each agent may return 5-10KB).

**Rule:** Size the window to cover the largest plausible turn. With 10+ agent dispatches per turn at ~10KB each, 200KB (204,800 bytes) covers the realistic maximum. 80KB fails with 3+ agents.

### 2. Fence Stripping

LLM responses often contain markdown code fences (` ``` `) with example classification text, quoted prior outputs, or documentation. A regex scanning for `TASK TYPE: Build` will match inside a code fence as readily as outside one.

**Fix:** Strip fenced code blocks before scanning: `re.sub(r'```[\s\S]*?```', '', text)`. This removes all content between triple backticks, leaving only the model's actual operational output.

**Assumption:** Real classification output is never inside code fences. This holds because classification blocks are operational output, not documentation. If the model starts wrapping classifications in fences, the hook design needs revisiting.

### 3. Case-Insensitive Matching

Field labels like `TASK TYPE:`, `MUST DISPATCH:`, `IMPLIES:` should match regardless of case. Models may output `Task Type:` or `task type:` depending on context. Using `re.IGNORECASE` on all field detection regexes eliminates this failure mode.

### 4. Multiline Field Capture

Fields like `MUST DISPATCH: process-analysis, architect-review, process-qa` may wrap across lines. A single-line regex (`r'MUST DISPATCH:\s*(.+)'`) captures only the first line.

**Fix:** Capture until the next known field label or end of text:
```
r'MUST DISPATCH:\s*(.*?)(?=\n\s*(?:IMPLIES|TASK TYPE|DOMAIN|APPROACH|MISSED)\s*:|\Z)'
```
With `re.DOTALL | re.IGNORECASE`. Then collapse whitespace: `re.sub(r'\s+', ' ', raw)`.

## When to Apply

Any hook that reads LLM-generated text from a conversation transcript and pattern-matches for structured fields. This is not specific to any particular governance framework -- it applies wherever deterministic checks are applied to probabilistic outputs.
