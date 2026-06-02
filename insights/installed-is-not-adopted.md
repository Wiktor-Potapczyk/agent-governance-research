# Installed Is Not Adopted: A Tool Without an Enforcement Binding Is Inert

Adding a tool to an agent system — an MCP server, a skill, a hook — feels like adoption. It is not. A tool is adopted only when something causes it to be *used at the right moment*. Without that binding, the tool sits in the toolbox and the agent keeps reaching for the old habit. The install is the easy 10%; the adoption is the 90%.

## The Insight

A newly-added capability has two axes, and they are independent:

- **Incorporation** — it is present, loads, and is documented (the agent can see it and knows when it is meant to be used).
- **Enforcement** — something at runtime causes it to actually be reached for: a rule the agent follows, a hook that nudges, or a routing trigger.

Judge enforcement on the *right scale per tool type* — demanding a hard gate for everything is over-engineering:

| Tool type | Native enforcement | Adopted when… |
|---|---|---|
| Hook | self-enforcing — it fires whether or not anyone remembers it | present + registered |
| Skill | soft — the loader surfaces it when its description matches the task | description triggers reliably; documented |
| Passive tool (MCP query, search index, call-graph) | **none** — it is available but nothing makes the agent prefer it over its default move | a rule or nudge points to it at the decision point |

The dangerous case is the third row. A passive tool whose entire value depends on being consulted *proactively* (a code call-graph before an edit, a memory search before answering) has zero pull on its own. The agent will keep grepping, keep answering from context, keep doing the thing it already knew how to do — and the new tool, fully installed, contributes nothing.

## Why This Matters

This is a general law of tool adoption in agent systems. The install step produces a satisfying artifact (it shows up in the tool list, the server connects) that *feels* like done. But behavior doesn't change on availability — it changes on a binding. The contrast is sharp within a single system: a memory-search tool with a "search-first for these question categories" rule gets used; an identical-quality tool added without such a rule does not, even though both are equally "installed."

## The Counter-Trap: Don't Enforce Prematurely

The fix is not to slap a forcing hook on every new tool — that recreates the over-enforcement problem and clutters the system with rarely-hit rules. The disciplined sequence is **measure, then gate**:

1. **Incorporate first** — make the tool present and documented (close the easy gap honestly).
2. **Instrument** — log whether the tool gets skipped on turns where it would have helped.
3. **Gate only on evidence** — add the forcing binding once the data shows the habit isn't forming on its own. If usage forms naturally, the binding was never needed.

Enforcing a tool that has been used on zero real tasks is speculation, not adoption. "Installed but consciously left opt-in, pending a usage baseline" is a legitimate, honest end state — and is different from "installed and silently forgotten," which is the failure this insight names.

## The One-Line Test

> A tool you added but never built a reason-to-use for is not part of your system. It is a bookmark.
