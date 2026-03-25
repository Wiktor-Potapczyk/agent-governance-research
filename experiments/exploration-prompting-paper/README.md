# Forced Depth Consideration Reduces Type II Errors in LLM Self-Classification

**Paper:** [paper.pdf](paper.pdf) | **LaTeX:** [exploration-prompting.tex](exploration-prompting.tex)

## Summary

We test whether prepending a single question before an LLM's self-classification decision reduces Type II errors (classifying complex prompts as "Quick" when they require deeper processing). Using TaskClassBench (311 prompts, 200 effective traps) across 4 models from 3 families, we find:

1. **Forced depth consideration significantly reduces Type II errors** compared to no-question baselines and structured detection approaches (McNemar p = 0.00073, CMH p = 0.0013).
2. **A content-free metacognitive instruction** ("Think carefully about the complexity of this task") achieves a not-significantly-different error rate to open-ended exploration ("What's really going on here?"): 8/800 vs 10/800, p = 0.77.
3. **Structured extraction and detection approaches are significantly worse** — constraining or misdirecting the model's attention before classification harms performance.
4. **The two approaches have complementary failure modes**: exploration forces committed implication statements that anchor classification; think-carefully uses consequence framing that catches deferral-type traps. Neither has a universal advantage.

The difficulty-scaling hypothesis predicts that exploration's advantage over simple metacognitive nudges will emerge on harder classification tasks and higher context depths, where content-free instructions are insufficient to trigger task-specific representation-building. This prediction is stated as a falsifiable hypothesis for future work.

## Repository Structure

```
exploration-prompting.tex   # LaTeX source (V5.1)
paper.pdf                   # Compiled paper
figures/                    # Figures (PDF + PNG)
generate-figures.py         # Figure generation script
data/                       # Raw results + computed statistics
  prompts.yaml              # Original 151-prompt benchmark
  prompts-expanded.yaml     # Expanded 311-prompt benchmark
  results-*.json            # Raw promptfoo results (R1, R2, EXP, R3, Variance)
  calculations-*.json       # Computed statistics (one per dataset)
  compute-*.py              # Computation scripts (reproducible)
classifiers/                # All 8 classifier variant prompts
  classifier-baseline.txt
  classifier-exploration.txt
  classifier-extraction.txt
  classifier-baseline-gated.txt
  classifier-extraction-v2.txt
  classifier-exploration-v2.txt
  classifier-exploration-v3.txt
  classifier-think-carefully.txt
configs/                    # Promptfoo configurations
  config-expanded-deepseek.yaml
  config-think-carefully.yaml
```

## Reproducing Results

### Prerequisites

- Python 3.10+ with `scipy`
- [promptfoo](https://promptfoo.dev/) (`npx promptfoo`)
- API keys for: DeepSeek, Google Gemini, Anthropic Claude

### Verify computed statistics

```bash
cd data/
python compute-r1.py        # -> calculations-r1.json
python compute-r2.py        # -> calculations-r2.json
python compute-expanded.py  # -> calculations-expanded.json
python compute-r3.py        # -> calculations-r3.json
python compute-variance.py  # -> calculations-variance.json
```

### Re-run experiments (requires API keys)

```bash
export DEEPSEEK_API_KEY=your-key
export ANTHROPIC_API_KEY=your-key
export GOOGLE_API_KEY=your-key

cd configs/
npx promptfoo eval -c config-expanded-deepseek.yaml -o ../data/results-expanded-deepseek.json --no-cache
npx promptfoo eval -c config-think-carefully.yaml -o ../data/results-think-carefully.json --no-cache
```

## Datasets

| Dataset | Models | Variants | Traps | Purpose |
|---------|--------|----------|-------|---------|
| R1 | 5 (incl. Gemini Pro) | 3 (base, expl, extr) | 120 | Pilot (confounded) |
| R2 | 5 (incl. Gemini Pro) | 4 (gated, extr2, expl2, expl3) | 120 | Controlled (equal gates) |
| EXP | 4 (excl. Gemini Pro) | 7 (all) | 200 eff. | Primary evidence |
| R3 | 4 (excl. Gemini Pro) | 1 (think) | 200 eff. | Mechanism ablation |
| Variance | 1 (DeepSeek) | 1 (expl) | 120 | Stability measurement |

## Key Results

| Variant | Pooled Type II (/800) | Rate |
|---------|----------------------|------|
| think (R3) | 8 | 1.0% |
| expl2 (EXP) | 10 | 1.2% |
| expl (EXP) | 16 | 2.0% |
| expl3 (EXP) | 19 | 2.4% |
| extr2 (EXP) | 25 | 3.1% |
| base (EXP) | 41 | 5.1% |
| gated (EXP) | 84 | 10.5% |
| extr (EXP) | 93 | 11.6% |

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

See [LICENSE.txt](../../LICENSE.txt) in the repository root.
