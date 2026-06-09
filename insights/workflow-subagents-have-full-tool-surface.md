# Workflow Sub-Agents Have the Full Tool Surface

**The finding:** Sub-agents spawned *inside a deterministic workflow script* are not the same, capability-wise, as sub-agents spawned by the ordinary task-delegation tool. A workflow `agent()` call has the **complete tool surface** — shell, file-read, dynamic tool-loading, and every MCP server the session has loaded. The long-standing rule "sub-agents cannot reach MCP" holds for task-delegation sub-agents but is **false for the workflow harness**.

**Why it matters:** this was the single highest-risk assumption blocking the procedure-layer-as-workflows direction. If workflow agents could not reach the tools a converted skill needs (shell for verification, MCP for live-system queries, file-read for scope), then execution-heavy skills would be unconvertible and the program would collapse to a narrow subset. The opposite is true: *every* process skill is technically convertible. The remaining gates are design and quality, not capability.

**Evidence (two live workflow runs, fabrication-resistant):**

- A probe agent loaded an MCP server's tool schema dynamically and called its health-check, returning a genuine payload (version string, response-time, status) that it could not have guessed. → MCP is reachable from a workflow agent.
- A second probe, after a previously-unavailable MCP server reconnected, confirmed the full surface against known ground truth: shell (`python --version` → the real installed version), file-read (read a known file → its real frontmatter value), dynamic tool-loading, and a content-search MCP server (returned its exact collection manifest — document counts that match the server's real state).
- The first probe's MCP miss for one server was **not** a harness limitation — that server simply was not loaded in the session at the time (the main session could not see it either). Workflow agents reach the servers the *session* has loaded; a server that is down is invisible to them exactly as it is to the main session.

**Anti-fabrication bonus:** when a tool genuinely was not available, the probe agent reported "not reachable" with the exact reason and refused to invent a payload. The framework's anti-fabrication discipline survives into workflow sub-agents — relevant because schema-validated returns plus an execution-evidence gate are *harder to fake* than free text.

**The implication — enforcement by construction:** because a workflow agent can actually run the verifying tool, a workflow can gate on **execution evidence** (a command was really run; an artifact really exists on disk) rather than on the *presence of a correctly-formatted report*. That closes the gap where a process passes its checks "whether the evidence came from running a command or from reading a file and guessing." It is the structural intervention the framework's measured data keeps pointing to: making it impossible to behave incorrectly at the structural level beats adding another rule.

**Boundary / caveat:** a workflow agent only reaches MCP servers the *session* has loaded — not a guarantee that any given server is up. And the inherent fabrication residue remains: an agent can still return a plausible-looking "raw output" string without a real tool call. Schemas and prompts make that a violation; they do not mechanically eliminate it. Verify a blocking/gating behavior by observing it in a live run, not by trusting a self-report.

**Related:** [Procedure layer as workflows](../specs/procedure-layer-as-workflows.md) (the program this unblocks); enforcement-layer-needs-meta-verification; hooks-over-prompts; qa-is-popperian-falsification.
