
# Google Labs — Research Findings

## What Is Google Labs?

Google Labs ([labs.google](https://labs.google/)) is Google's umbrella platform for AI experiments. Not a single product — a portfolio of 12+ experimental tools spanning creative, productivity, developer, and agent categories. Most are free, some waitlisted. Powered by Gemini model family (2.0, 2.5 Pro, 3 Flash).

## Full Tool Catalog

### Developer / Agent Tools

| Tool | What It Does | Model | Status | Relevance |
|------|-------------|-------|--------|-----------|
| **Jules** | Autonomous coding agent. Reads code, generates fixes, writes tests, multi-file changes. CLI (`jules-tools`) + API for CI/CD integration. Proactive mode scans repos for #todo improvements. | Gemini 2.5 Pro | GA (out of beta Aug 2025) | HIGH — direct Claude Code competitor. Architecture comparison opportunity. |
| **Stitch** | AI UI design canvas. Text-to-UI, voice commands, "vibe design" (intent → design directions). Has **MCP server** for Claude Code + SDK. Exports DESIGN.md (design system in agent-readable markdown). | Gemini | Live, free | HIGH — MCP server integrates directly with Claude Code. DESIGN.md format is a reusable pattern. |
| **Opal** | No-code AI mini-app builder with agentic workflow capabilities. Agent step with **memory** (via Sheets), **dynamic routing** (natural language conditions), **interactive chat** (gather missing info mid-workflow). | Gemini 3 Flash | Live | MEDIUM — n8n competitor for simple workflows. Memory + routing patterns worth studying. |
| **Mariner** | Web navigation agent. Chrome extension. Observe–Plan–Act loop on pixels. Handles 10 concurrent tasks. "Teach & Repeat" learns workflows. | Gemini 2.0 | Research prototype, limited access | MEDIUM — web automation alternative to Apify scrapers. 83.5% WebVoyager benchmark. |

### Creative Tools

| Tool | What It Does | Status |
|------|-------------|--------|
| **Flow** | All-in-one video/image production studio. Lasso editing, camera control, asset collections. Absorbed Whisk + ImageFX. | Live |
| **Pomelli** | AI marketing content generator. "Photoshoot" feature turns product photos into studio shots. | Live |
| **Mixboard** | AI ideation/concepting board for visual exploration. | Live |
| **ProducerAI** | Music creation with DeepMind models. Text-to-song. | Live |
| **Music AI Sandbox** | Agentic music partner — lyrics, melodies, genre invention. | Live |

### Productivity

| Tool | What It Does | Status |
|------|-------------|--------|
| **Disco** | AI browser. Analyzes open tabs, builds **GenTabs** — interactive dashboards synthesizing multi-tab research. | Waitlist (macOS first) |
| **CC** | Gmail AI agent. Morning email briefings, email-based task assistant. | Experimental |
| **Learn Your Way** | Transforms content into personalized learning experiences. | Experimental |

### Gaming/Other

| Tool | What It Does | Status |
|------|-------------|--------|
| **Project Genie** | Generate and explore infinite game worlds. | Experimental |

## Deep Dives

### Jules — Autonomous Coding Agent

- **Architecture:** Cloud VM execution, Gemini 2.5 Pro, asynchronous (queues tasks, returns results)
- **Interface:** GitHub integration, CLI (`jules-tools`), API (trigger from Slack/CI/CD)
- **Proactive mode:** "Suggested Tasks" — scans repos, proposes improvements starting with #todo comments. Enabled on up to 5 repos (AI Pro/Ultra subscribers).
- **Next:** "Jitro" (internal codename for Jules V2) — bigger task scope
- **Comparison to Claude Code:** Jules is async/cloud-based vs Claude Code's synchronous local execution. Jules has no hook/governance system visible. Claude Code has richer tool ecosystem (MCP, hooks, skills).

### Stitch — AI Design Canvas with MCP

- **MCP server:** [github.com/davideast/stitch-mcp](https://github.com/davideast/stitch-mcp) — CLI that bridges Stitch designs to dev workflow
- **MCP tools:** `build_site` (maps screens to routes, returns HTML), `get_screen_code` (retrieves screen HTML), `get_screen_image` (screenshot as base64)
- **DESIGN.md:** Agent-friendly markdown capturing full design system (colors, typography, spacing, component patterns). Exportable, reusable across tools.
- **Voice canvas:** Speak to the design agent for real-time critiques and modifications
- **Workflow:** Stitch (design) → MCP → Claude Code (implement) → deploy. End-to-end design-to-code.

### Opal — Agentic Workflow Builder

- **Agent step (February 24, 2026):** Turns static workflows into interactive agentic experiences
- **Memory:** Uses Google Sheets for cross-session persistence. Remembers preferences, lists, context.
- **Dynamic routing:** Define multiple workflow paths with natural-language conditions. Agent evaluates and transitions autonomously.
- **Interactive chat:** Agent can pause workflow to ask user for missing information before proceeding.
- **Tools:** Can invoke Web Search, Veo (video), other Google AI models within workflows.
- **Comparison to n8n:** Opal is simpler (no-code, mini-apps) but has native agentic primitives that n8n builds with sub-workflows + AI nodes. Opal's memory pattern (Sheets-backed) is simpler than n8n DataTables.

### Mariner — Web Agent

- **Architecture:** Observe–Plan–Act loop. "Pixels-to-action" — sees pages visually like a human.
- **Concurrency:** Up to 10 simultaneous web tasks
- **Teach & Repeat:** Learn a workflow once, replay across similar sites
- **Benchmark:** 83.5% on WebVoyager
- **Coming 2026:** Mariner Studio (visual task flow builder), cross-device sync, agent marketplace

## Relevance to Our Work

### Directly Useful

1. **Stitch MCP for Claude Code** — If we ever build UIs, this is a production-ready design-to-code pipeline. The DESIGN.md format is worth studying as a pattern for agent-readable specifications.

2. **Jules architecture comparison** — Jules is the closest Google equivalent to Claude Code. Comparing their approaches to agent governance (Jules: proactive suggestions on repos; us: hook-driven enforcement) could yield insights for the framework.

3. **Opal's agentic patterns** — Memory (Sheets-backed), dynamic routing (NL conditions), interactive chat (pause for human input). These are the same problems we solve differently with STATE.md, classifier routing, and "exhaust before asking."

### Worth Monitoring

4. **Mariner** — If it reaches production, could replace some Apify scraping workflows. The "Teach & Repeat" pattern is interesting for automation.

5. **Disco GenTabs** — Research synthesis tool. If it works well, could complement NotebookLM for multi-source analysis.

### Not Relevant

- Flow, Pomelli, ProducerAI, Music AI Sandbox — creative tools outside our domain
- CC — Gmail-specific, too narrow
- Learn Your Way — education-focused
- Project Genie — gaming

## Sources

- [Google Labs homepage](https://labs.google/)
- [Every Google AI Tool in 2026 guide](https://aiblewmymind.substack.com/p/google-ai-tools-2026-guide)
- [Complete List of Google AI Products 2026](https://hiringhello.com/blog/complete-list-of-google-ai-products-experiments-2026-summaries-launch-info)
- [Opal agent step announcement](https://blog.google/innovation-and-ai/models-and-research/google-labs/opal-agent/)
- [Stitch AI design platform](https://blog.google/innovation-and-ai/models-and-research/google-labs/stitch-ai-ui-design/)
- [Stitch MCP GitHub](https://github.com/davideast/stitch-mcp)
- [Jules autonomous coding agent](https://blog.google/innovation-and-ai/models-and-research/google-labs/jules/)
- [Jules Tools CLI](https://developers.googleblog.com/en/meet-jules-tools-a-command-line-companion-for-googles-async-coding-agent/)
- [Project Mariner — DeepMind](https://deepmind.google/models/project-mariner/)
- [Disco and GenTabs](https://blog.google/innovation-and-ai/models-and-research/google-labs/gentabs-gemini-3/)
- [Opal dynamic routing (VentureBeat)](https://venturebeat.com/ai/googles-opal-just-quietly-showed-enterprise-teams-the-new-blueprint-for)
- [Stitch MCP + Claude Code workflow](https://www.sotaaz.com/post/stitch-mcp-integration-en)
