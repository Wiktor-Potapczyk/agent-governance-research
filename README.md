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
| Quality Mechanism Spectrum | 8-level hierarchy from "think again" to ensemble |
| Inline Bias | Autoregressive generation bias in classification (12.4% mismatch) |
| Hooks as Governance | Hooks achieve ~90% compliance vs ~25% for prompt rules |
| Epistemic Gaps | Input (planning) and output (uncertainty) gaps |
| Framework Architecture | 5-node recursive execution pattern |
| Agent Teams & Depth Boundary | D1 governance constraint and collaborative mesh |
| Observability & Monitoring | 35-event telemetry catalog + 4-tier aggregation + 15 derivable conclusions |

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
