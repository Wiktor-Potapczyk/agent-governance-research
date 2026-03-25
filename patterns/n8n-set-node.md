# n8n Pattern: Set Node for Multi-Consumer Data Views

When multiple LLM nodes in an n8n workflow need different subsets of the same data, use a Set node to hold the full JSON and let each consumer reference only the keys it needs. This eliminates projection logic, dual-file sync problems, and runtime overhead.

## The Pattern

1. One Set node holds the FULL JSON as its output
2. Each LLM node's prompt template references ONLY the keys it needs via `{{ $json.keyName }}`
3. Keys not referenced are simply invisible to that LLM — no stripping, no code node, no separate files

## Why This Works Better Than Alternatives

- No code node maintenance (projection logic)
- No dual-file sync problem (single source of truth)
- No runtime overhead (expressions resolve at template time)
- Easy to audit: read the prompt template to see exactly what each consumer gets

## Example

A Set node holds a verified data library with 17 sections. A scoring LLM references 14 sections via expressions. A drafting LLM references all 17 sections. The 5 drafting-only sections are invisible to the scoring LLM because its prompt simply doesn't reference them.

## When to Apply

This pattern applies when n8n has no external file storage and data lives inside the workflow. It's particularly useful when the same data feeds multiple LLM prompts that need different views of that data.
