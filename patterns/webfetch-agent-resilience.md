# Background Agent Resilience: URL Fetching Failures

Background research agents that fetch specific URLs are unreliable. Sites may block, timeout, or be slow, and background agents have no way to recover from a hung fetch. This pattern addresses designing resilient research agent architectures.

## Evidence

Three out of six background research agents got stuck trying to fetch specific URLs. Pattern: agent dispatches URL fetch, URL hangs, agent waits forever, never writes output file, becomes orphaned. One agent succeeded because it relied on topic-based web search instead of URL-specific fetching. The orphaned agents consumed significant compute with no output.

## The Principle

URL-specific fetching in background agents is unreliable. Design research agents to be resilient to network failures.

## How to Apply

- For online research: prefer purpose-built research tools (e.g., Perplexity Deep Research) over direct URL fetching
- If agents must search: instruct them to use topic-based web search, never URL-specific fetching
- Always instruct agents to write output files incrementally, not at the end — so partial results survive if the agent dies
- Track background agent IDs — orphaned agents burn compute silently
- Design for graceful degradation: if a fetch fails, the agent should continue with available information rather than hanging
