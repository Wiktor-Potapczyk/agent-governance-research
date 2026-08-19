# Agent Governance Research

Research into governance patterns for multi-agent LLM systems — how to make AI agents reliably classify, route, and execute complex tasks.

This repository contains both empirical research (experiments, benchmarks, data) and architectural insights (patterns, theories, framework specs) developed through production use of [Claude Code](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview).

## Featured Paper

**Forced Depth Consideration Reduces Type II Errors in LLM Self-Classification**
*Wiktor Potapczyk, 2026*

LLM task classifiers systematically misroute prompts that look simple but require deeper processing. We test whether prepending a single question before the classification decision reduces this failure mode, and run a mechanism ablation to identify why.

Key findings:
- Open-ended exploration ("What's really going on here?") reduces Type II errors to 1.25%, significantly outperforming directed extraction at 3.12% (p < 0.001, Bonferroni-corrected)
- A content-free metacognitive instruction ("Think carefully") achieves 1.0% — not significantly different from exploration (p = 0.77) — suggesting the mechanism is forced attention to complexity, not open-ended framing specifically
- Structured yes/no detection catastrophically harms some models (Claude Haiku: 330% error increase)
- Qualitative analysis reveals complementary failure modes: exploration forces committed implication statements; the metacognitive directive catches different trap subtypes via consequence framing

Paper (PDF + LaTeX), benchmark, and all experimental data: [`experiments/exploration-prompting-paper/`](experiments/exploration-prompting-paper/)

## Research Threads

The full research index tracks 9 active threads: [`INDEX.md`](INDEX.md)

| Thread | Summary |
|--------|---------|
| Exploration Prompting | Step-0 framing for self-classification (paper above) |
| Compound Task Neural Network | Tasks as continuous mixtures of 5 primitives |
| Quality Mechanism Spectrum | 8-level hierarchy from "think again" to ensemble. Extended 2026-05-25: Three-lens parallel ensemble applied to framework evaluation itself; convergent finding (confidence 0.82) — Wave A metadata improvements did not change any hook's detection behavior. Ensemble methodology documented as a repeatable pattern. |
| Inline Bias | Autoregressive generation bias in classification (12.4% mismatch) |
| Hooks as Governance | Hooks achieve ~90% compliance vs ~25% for prompt rules. Extended 2026-05-25: Infrastructure audit + multi-lens ensemble evaluation reveal the closed-loop measurement problem — internal compliance metrics measure rule conformance, not output quality. External calibration protocol (Action 0.1) is the only loop-exit channel. |
| Epistemic Gaps | Input (planning) and output (uncertainty) gaps |
| Framework Architecture | 5-node recursive execution pattern (2026-03-21). Extended 2026-05-25: cold-context empirical investigation of runtime state → 7-delta architecture spec closing gap between declared and actual behavior. Key finding: Stop hook event carries 11 hooks vs. 1–3 for all other events; enforcement is maximally rear-loaded. |
| Agent Teams & Depth Boundary | D1 governance constraint and collaborative mesh |
| Observability & Monitoring | 35-event telemetry catalog + 4-tier aggregation + 15 derivable conclusions |

**2026-05 evolution:** A major evaluation and re-architecture pass in May 2026 produced the documents in `framework/`, `specs/`, and the new `meta/` batch. The central finding: the framework's instrumentation measures process conformance, not output quality — a closed-loop problem addressable only via external calibration. The architecture-v2 delta spec closes seven gaps between declared and runtime behavior. An ensemble methodology (parallel cold-context lenses, preserved divergent verdicts, main-session synthesis) is now used for evaluative work across the project. See [`specs/agent-governance-architecture-v2.md`](specs/agent-governance-architecture-v2.md) for the current architectural source of truth and [`specs/action-0-1-calibration-protocol.md`](specs/action-0-1-calibration-protocol.md) for the external calibration protocol.

**2026-06 addition:** two insights generalize this layer's lessons (INDEX #40–#41) — *the enforcement layer needs its own meta-verification* (a BLOCK-hook/allow-list enforcer is itself code with silent false-positive and drift failure modes — verify the verifier), and *installed is not adopted* (a tool is adopted only when something pulls it into use at the right moment; incorporation and enforcement are independent axes). Subsequent June work added INDEX #42–#46: *measure-then-gate* (measure a failure rate before installing a blocking gate), *wrong-protocol hooks silently no-op* (the block format is event-specific), the *workflow sub-agents have the full tool surface* engine proof, the *procedure-layer-as-workflows* program spec (with two worked conversion drafts), and *documenting an agent/skill/hook framework* (the composition that became the framework repo's documentation standard). A 2026-06-10 curation pass indexed eighteen previously-unindexed worthwhile files (#47-#64), and the 2026-06-11 migration that converted the whole procedure layer to enforced workflow scripts produced two further insights (#65-#66): *workflow-enforcement first-contact bugs* (args-as-string, session-cached named invocation, write-restricted agent fabrication - and the gates holding through all of it) and *Skill-tool-only hook assumptions* (governance hooks silently break when a skill becomes a workflow; audit method + fix pattern).

**2026-07/08 additions:** operating the two-gate autonomy model produced INDEX #67-#68 (a deny-gate's audit log that was 98.7% its own test suite; a narrowed deny pattern silently opening floor holes), and a publication pass that brought the public repositories back into step with the private system produced #69-#79 (gates green while structurally unable to fail, identity as two git fields, transcript-derived state, recorded rulings without quotes). An August wave of building and running new governance mechanisms then produced #80-#87: archived logs answering payload questions wrongly (80), a shared lock for colliding schedulers (81), telemetry vocabularies enforced without rewriting records (82), fail-closed mining of warn events (83), premise-false entries on recurring-signal boards (84), two-layer injection defense with stated guarantee classes (85), containment ordering under an automated committer (86), and a file-doubling splice defect that every validity gate passed (87). The through-line of the August findings: a mechanism's safety must be a structural property (derived exclusions, write ordering, shape checks), because intentions and archives both fail silently.

## Repository Structure

```
experiments/                    # Empirical work
  exploration-prompting-paper/  # Paper, benchmark, data, code
    paper.pdf                   # Compiled paper
    exploration-prompting.tex   # LaTeX source
    data/                       # Raw results + computation scripts
    classifiers/                # 8 classifier variant prompts
    configs/                    # Promptfoo configurations
framework/                      # Architecture documentation
insights/                       # Published research insights
theories/                       # Theoretical work
patterns/                       # Governance patterns
specs/                          # Technical specifications
meta/                           # Project metadata
```

## Contributing

Looking for:
- **Inter-rater validation**: Label ~50 trap prompts as Quick vs. requires-deeper-processing (~1 hour). This directly addresses the paper's biggest methodological limitation. Prompts are in [`experiments/exploration-prompting-paper/data/prompts-expanded.yaml`](experiments/exploration-prompting-paper/data/prompts-expanded.yaml).
- **Replication on open-weight models**: All current data is from commercial APIs. Would the pattern hold on Llama, Mistral, Qwen?
- **Methodological critique**: What did we miss?

## Citation

```bibtex
@article{potapczyk2026forced,
  title={Forced Depth Consideration Reduces Type {II} Errors in {LLM} Self-Classification: Evidence from an Exploration Prompting Ablation Study},
  author={Potapczyk, Wiktor},
  year={2026},
  note={Independent research. Code and data: \url{https://github.com/Wiktor-Potapczyk/agent-governance-research}}
}
```

## License

[Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE.txt)
