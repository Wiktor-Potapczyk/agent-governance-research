# External Confidence Mechanisms for Closed-API LLM Agents

When working with closed-API LLM providers (no access to logits or internal probabilities), external confidence calibration requires different techniques than white-box approaches. This documents viable mechanisms and community governance practices discovered through structured research.

## Viable External Confidence Methods (Closed API, No Logits)

### Tier 1 — Usable Immediately

- **Linguistic hedge scanner** — regex/keyword scan on output for hedging markers. Absence of hedging on ambiguous input = overconfidence flag. Zero latency. Research finding: linguistic features capture uncertainty undetectable in token probabilities (different signal, not a noisier version).
- **Independent cheap-model checker** — classify blind with a second model (e.g., Haiku/GPT-4o-mini), compare. Trail of Bits uses this in production for anti-rationalization.
- **User correction pattern as calibration** — count recent overrides/pushbacks, raise uncertainty threshold when pattern detected (arXiv 2602.23005).

### Tier 2 — Available But Costly

- **Parallel sampling** — run classifier N=5 times at temp 0.7, measure semantic agreement. Best black-box method but 5x cost.
- **Behavioral consistency monitoring** — N=5 parallel instances, measure first-divergence-point. Tasks with <=2 unique sequences: 80-92% accuracy.

### Tier 3 — Not Applicable to Closed APIs

- DiSRouter (requires fine-tuning), CCPS/probing (white-box), CoCoA full (needs logits)

## Key Findings

- DiSRouter explicitly REJECTS external calibration — argues trained self-assessment (80%) beats external classifiers (56-71%). But requires fine-tuning access.
- Self-reported confidence is WORST method across every benchmark (confirmed by multiple papers)
- Best approach combines two independent sources: internal + external behavioral
- Behavioral divergence: 69% occurs at step 2 (first decision). First-step divergence is the strongest unreliability signal.

### Sources

DiSRouter (arXiv 2510.19208), Multi-Agent Uncertainty (arXiv 2602.23005), Collaborative Calibration (arXiv 2404.09127), LM-Polygraph (TACL 2024), Behavioral Consistency (arXiv 2602.11619), Routing Survey (arXiv 2502.00409)

---

## Community Governance Practices

### Hook Ecosystems Discovered

1. **Trail of Bits claude-code-config** — defense-in-depth. Anti-rationalization Stop hook uses Haiku: "Is this response deflecting?" Returns {decision: block|allow}. Credential blocklists. OS-level sandboxing.
2. **disler multi-agent-observability** — SQLite event store (WAL), WebSocket dashboard, Stop hook validators block completion until deliverables exist.
3. **ruvnet claude-flow** — swarm-oriented. Shared memory DB for cross-agent state. Hook chaining with parameter propagation.
4. **affaan-m everything-claude-code** — 28 agents, 150+ plugins, quality-gate command, multi-runtime harness abstraction.
5. **applied-ai claude-code-toolkit** — explore-plan-next-ship workflow with explicit artifact handoffs. 6+ months production.

### Key Patterns

- **Builder/Validator with capability restriction** — disallowedTools removes write access, not instructions. Deterministic.
- **Anti-rationalization Stop hook** (Trail of Bits) — Haiku reviews final response for deflection. Block + inject reason.
- **Context decay fix** — PostToolUse tracks tool count, flushes to state files at 40-75% context. Rule violations drop to near-zero.
- **Hooks don't share live state** — coordination via exit codes, file artifacts, additionalContext. Only exception: SQLite event stores.
- **Communicative dehallucination** (MetaGPT) — agents request clarification BEFORE acting on ambiguous input.
- **Two-tier hook classification solidifying** — command hooks (deterministic safety) vs prompt/agent hooks (semantic quality).

### Sources

Trail of Bits, disler, ruvnet/claude-flow, everything-claude-code, MetaGPT, claude-code-toolkit, Hackernoon governance, JI AI 86-session study, Dotzlaw, contextua.dev, Douglas RW context decay fix
