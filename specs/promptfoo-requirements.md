# Promptfoo Integration Strategy -- Synthesized Requirements

Synthesized requirements for integrating promptfoo into an AI agent governance framework. Covers per-prompt evaluation strategies, ROI ranking, minimal viable first eval configuration, and Dark Zone measurement. Based on parallel research across promptfoo mechanics, workflow prompts, and agent/skill system prompts.

---

## 1. Per-Prompt Eval Strategy

### Task Classifier (HIGHEST ROI)

**Output structure:**
```
IMPLIES: [sentence]
TASK TYPE: Quick | Research | Analysis | Content | Build | Planning | Compound
DOMAIN: [10 domains + "general"]
APPROACH: [5 primitives breakdown]
MISSED: [sentence]
MUST DISPATCH: [comma-separated agent names or "none"]
```

**Assertion tiers:**

| Tier | Type | Assertion | Implementation |
|------|------|-----------|----------------|
| L1 | Structural | All 6 fields present | `regex` for each field label |
| L1 | Structural | TYPE is one of 7 valid values | `regex` with alternation |
| L2 | Logic | MUST DISPATCH lists exactly agents named in APPROACH | Custom `javascript` assertion |
| L2 | Logic | Compound TYPE has multiple primitives in APPROACH | Custom `javascript` assertion |
| L3 | Semantic | IMPLIES captures actual user need | `llm-rubric` with ground truth |
| L3 | Semantic | TYPE matches expected classification | `contains` (exact match) |

**Built-in ground truth:** The classifier prompt contains a 20-row "Classification Traps" table with WRONG vs RIGHT pairs -- ready-made test cases.

### Adversarial Reviewer (MEDIUM ROI)

Findings with severity (CRITICAL/WARNING/GAP/NOTE) + Verdict with confidence 0.0-1.0. Stochastic by design -- eval focuses on structural compliance and severity calibration rather than exact match.

### Verify / CoVe (MEDIUM ROI)

Per-step confidence ratings + independent re-derivation for medium/low confidence steps. The condition masking rule ("without referencing your original reasoning") is uniquely amenable to automated testing -- n-gram overlap between original and re-derivation can be measured with a custom JS assertion.

### Ensemble (LOWER ROI)

4 lens positions + divergence/convergence analysis. Too stochastic for deterministic assertions. Primary value requires LLM-as-judge.

---

## 2. ROI Ranking

| Rank | Prompt | ROI | Rationale |
|------|--------|-----|-----------|
| 1 | **Task Classifier** | HIGHEST | Routes everything; errors cascade; 20-case ground truth; deterministic fields |
| 2 | **Domain Fit Scoring** | HIGH | Validated rows with known outputs; deterministic JSON schema; compliance rules mechanically testable |
| 3 | **Adversarial Reviewer** | MEDIUM | Important quality gate; severity calibration measurable; stochastic limits precision |
| 4 | **Verify/CoVe** | MEDIUM | Condition masking uniquely testable; niche use |
| 5 | **Process Skills** | MEDIUM | Structural compliance testable; long outputs, low density |
| 6 | **Ensemble** | LOWER | Too stochastic; requires LLM-as-judge |

---

## 3. Minimal Viable First Eval

### Selection Rationale

**The task classifier is the clear first eval target.** Three factors converge:

1. **Cascade effect:** Every task is routed by the classifier. Misclassification cascades into wrong process, wrong agents, wrong quality mechanism.
2. **Ground truth exists:** 20-row Classification Traps table. Ready-made test cases requiring zero construction.
3. **Structural assertions are trivial:** 6 mandatory labeled fields with constrained value sets.

### Minimal Config

```yaml
# promptfooconfig.yaml -- MVP: Task Classifier Eval
prompts:
  - file://task-classifier-prompt.txt

providers:
  - id: anthropic:messages:claude-sonnet-4-6
    config:
      temperature: 0
      max_tokens: 1024

tests:
  # Trap Case 1: Quick-bias
  - vars:
      user_message: "Refactor the error handling in the scoring module"
    assert:
      - type: regex
        value: "IMPLIES:"
      - type: regex
        value: "TASK TYPE:"
      - type: regex
        value: "DOMAIN:"
      - type: regex
        value: "APPROACH:"
      - type: regex
        value: "MISSED:"
      - type: regex
        value: "MUST DISPATCH:"
      - type: regex
        value: "TASK TYPE:\\s*(Quick|Research|Analysis|Content|Build|Planning|Compound)"
      - type: contains
        value: "Build"

  # Trap Case 2: Compound detection
  - vars:
      user_message: "Research promptfoo, design eval strategy, build first config"
    assert:
      - type: regex
        value: "TASK TYPE:\\s*Compound"
      - type: javascript
        value: |
          const dispatch = output.match(/MUST DISPATCH:\s*(.+?)(?=\n|$)/)?.[1] || '';
          return dispatch !== 'none';
```

### Execution

```bash
npm install -g promptfoo
export ANTHROPIC_API_KEY=sk-...
npx promptfoo eval --config promptfooconfig.yaml
npx promptfoo view    # Opens HTML dashboard
```

---

## 4. Dark Zone Measurement

### What Is the Dark Zone?

The gap between what a subagent produces and what actually appears in the final response to the user. If an agent returns high-quality analysis but the orchestrating model ignores, garbles, or dilutes it, evaluating the subagent prompt alone misses this failure mode.

### A/B Testing Is Native

Promptfoo's multi-prompt capability enables direct Dark Zone measurement:

```yaml
prompts:
  - file://prompt-with-agent-context.txt     # Includes pre-computed agent output
  - file://prompt-without-agent-context.txt   # Same task, no agent output

# Same test cases run against both prompts
# Delta between pass rates IS the Dark Zone measurement
```

If both prompts produce equivalent quality, the agent output is not being utilized.

### Three Complementary Assertions

1. **`context-faithfulness`** -- checks output does NOT hallucinate beyond context (necessary but insufficient -- ignoring context also scores 1.0)
2. **Custom JavaScript** -- checks output DOES contain key elements from injected context (positive-direction check)
3. **`llm-rubric`** -- semantic judge: "Does the response substantively incorporate the analysis rather than generating a parallel response?"

### Critical Limitation

Promptfoo operates at the single API call boundary. It cannot observe live dispatch decisions, multi-turn agent interactions, or how the orchestrator processes agent output. Workaround: pre-compute agent outputs, inject as variables, test integration quality.

---

## 5. Phase Plan

| Phase | Target | Effort | Expected Outcome |
|-------|--------|--------|-----------------|
| 1 | Task Classifier -- 5-10 trap cases, L1 structural only | 1-2 hours | Proves toolchain works |
| 2 | Task Classifier -- expand to 20 cases, add L2 logic + L3 semantic | Half day | Full coverage; identifies bias patterns |
| 3 | Domain Fit Scoring -- 4 validated rows, compliance rules | Half day | Validates production prompt |
| 4 | Dark Zone A/B test -- 2-3 cases | 2-3 hours | Proves/disproves agent context utilization |
| 5 | Adversarial Reviewer + Verify -- structural + protocol checks | Half day | Extends eval to quality mechanisms |

### Key Implementation Decisions

- **Direct API, not webhook:** Test prompts in isolation. This is prompt evaluation, not workflow testing.
- **One config file per prompt:** Separate configs keep concerns separate.
- **Temperature 0 for evals:** Maximize reproducibility.
- **Store test data as files:** Large JSON inputs as separate files referenced by vars.

### Risk Factors

1. **Test data parsing** is a prerequisite for domain scoring evaluation
2. **llm-rubric cost** can escalate -- use deterministic assertions as primary gate
3. **Stochastic prompts** (ensemble, adversarial reviewer) will never achieve high pass rates on semantic assertions
4. **Prompt versioning** is not currently tracked -- eval configs must be updated in lockstep
