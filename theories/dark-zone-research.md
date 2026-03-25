# The Dark Zone: Output Integration Across Multi-Agent Frameworks

When an LLM agent system dispatches a specialist agent, the agent produces output. The main session receives that output. Then what? Every framework solves making agent output *available*. None solve ensuring it is actually *used*. This gap -- between availability and utilization -- is the Dark Zone. It parallels RAG faithfulness failures, where systems achieve high answer relevancy while ignoring the retrieved context entirely.

## Core Finding

**Every framework solves data AVAILABILITY. None solve data UTILIZATION.** Making agent output accessible != ensuring it's used. The same phenomenon appears in RAG faithfulness failures (40% hallucination despite correct retrieval).

## Academic Grounding

- **Lost in the Middle** (Liu et al. TACL 2024): 30%+ performance drop for mid-context information. Agent outputs in context may be ignored due to positional bias.
- **MAST taxonomy** (Cemri et al. 2025, arXiv:2503.13657): FM-2.5 = "Ignored other agent's input." 41-86.7% overall failure rates in multi-agent systems.
- **RAG faithfulness**: Systems can have high answer relevancy but low faithfulness -- answering correctly while ignoring provided context.

## How Frameworks Handle It

| Framework | Approach | Solves availability? | Solves utilization? |
|-----------|----------|---------------------|-------------------|
| MetaGPT | Artifact workspace, structured deliverables | Yes | No |
| ChatDev | Long-term memory bridges phases | Yes | No |
| LangGraph | State graphs, reducers | Yes | No |
| CrewAI | Pydantic output schemas | Yes (structure) | No |
| ICM (arXiv:2603.16021) | **Folder structure AS architecture. One agent per stage. Files = only communication.** | Yes | **Partially -- eliminates orchestrator entirely** |
| Anthropic research system | Artifact storage + lightweight references + CitationAgent | Yes | Partially (post-hoc verification) |

## Key Patterns

1. **ICM pattern** -- folder structure as architecture. Eliminates orchestrator. One agent per stage, files are the only communication. Systems using file-based agent output already approximate this.

2. **Citation format** -- require `Per [agent-name]: ...` in responses. Pattern-matchable without LLM judgment. Deterministic check.

3. **Independent judge agent** -- separate agent reads both agent output AND main response, verifies coverage. Reports suggest 1.5-7x accuracy improvement.

4. **Position mitigation** -- place critical agent outputs at beginning/end of context (not middle) to resist lost-in-the-middle effect.

5. **File-based communication** -- if agents write to files and the main session must Read those files, the access is observable via hooks (e.g., PostToolUse on Read). Reading != using, but NOT reading is definitively NOT using.

## What Can Be Built

Three-layer enforcement:
1. Agent writes structured findings to a work directory with section headers
2. A PostToolUse hook confirms the file was Read by the main session
3. A Stop hook checks the response cites findings (citation format pattern-match)

This doesn't prevent the Dark Zone but makes it **detectable**. Combined with QA enforcement (verify claims against the source file), it forces engagement with agent output.

## Sources

ICM (arXiv:2603.16021), MAST (arXiv:2503.13657), Lost in the Middle (arXiv:2307.03172), AIGNE AgentFS (arXiv:2512.05470), Anthropic multi-agent blog, Augment Code guide, RAGAS metrics.
