# n8n chainLlm Message Slot Behavior

Reference documentation for how the n8n Basic LLM Chain node (`@n8n/n8n-nodes-langchain.chainLlm`) handles multiple messages. Understanding these behaviors is critical when building LLM-powered workflows that inject context documents alongside system prompts and user queries. Tested on chainLlm v1.9, n8n 2.10.4.

---

## Message Slots

| Slot | Multiple supported? | Behavior with multiple entries |
|------|:-------------------:|-------------------------------|
| System messages | Yes | Each becomes a separate `SystemMessage` in LangChain ChatPromptTemplate. No merging. |
| AI/assistant message | Yes | Multiple entries get **merged into one** by n8n (not separate turns) |
| User message | Yes, but DO NOT | Multiple entries trigger **separate executions** (item fan-out) |
| Query field (`text` / promptType=define) | N/A | Always appended as the final HumanMessage. Separate from the messages array. |

## Key Rules

**Ordering rule (v1.9):** System messages MUST come first in the array. Adding a system message after an AI/user message throws: `"System message should be the first one"`. Reorder via workflow JSON if needed -- the UI has no drag-to-reorder.

**Multiple parallel runs cause:** Input items fan-out, NOT message array size. One item = one LLM call regardless of how many messages are in the array.

**Injecting multiple context documents:** Use expression concatenation or multiple AI message entries (they merge). Add section headers (`# SECTION NAME`) to help the model distinguish sources when merged.

**No native file reading:** chainLlm has no document loader sub-node. All context must be pasted as text or injected via n8n expressions referencing upstream node output.
