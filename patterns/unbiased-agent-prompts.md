# Keep Agent Prompts Unbiased for Open-Ended Questions

When dispatching agents for open-ended brainstorming or conceptual questions, pre-loading implementation constraints anchors every idea to a specific implementation. The conceptual question needs to run first, THEN the implementation analysis.

## The Principle

If the question is abstract/conceptual, dispatch the agent with NO implementation context. If the question is "how do we build X", include implementation context. When in doubt, ask: "Is this about the NATURE of something or the IMPLEMENTATION of something?"

## Evidence

The question was "design a question that induces second thoughts" — an epistemological question about the nature of reconsideration. The agent was anchored to specific tooling (hook runtime, scripting language, platform). It produced 14 useful but narrowly scoped ideas. A second, unbiased agent produced fundamentally deeper insights about the nature of reconsideration itself.

Implementation context biases the agent toward "how to build it" instead of "what should we build."

## How to Apply

- Abstract/conceptual question: dispatch agent with NO implementation context, NO tool access (don't search the web either — just reason)
- Implementation question: include implementation context
- Don't give broad or philosophical questions web search access — the agent will spiral endlessly on broad topics instead of reasoning from first principles
