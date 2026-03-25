"""Compute variance/stability analysis.
Source: R1 DeepSeek exploration + Variance run + Expanded DeepSeek exploration (first 120).
Output: calculations-variance.json

Measures run-to-run stability at temperature=0 on identical prompts.
"""
import json, os, datetime

BASE = os.path.dirname(os.path.abspath(__file__))

DATASET = "Variance"
VARIANT_MAP = {
    "classifier-baseline.txt": "base",
    "classifier-exploration.txt": "expl",
    "classifier-extraction.txt": "extr",
    "classifier-baseline-gated.txt": "gated",
    "classifier-extraction-v2.txt": "extr2",
    "classifier-exploration-v2.txt": "expl2",
    "classifier-exploration-v3.txt": "expl3",
}

TRAP_IDX = set(range(120))

def load_results(fname, variant_filter=None):
    with open(os.path.join(BASE, fname)) as f:
        data = json.load(f)
    nested = data["results"]["results"]
    d = {}
    for r in nested:
        label = r.get("prompt", {}).get("label", "")
        vkey = label.split(":")[0].strip()
        vshort = VARIANT_MAP.get(vkey)
        if vshort is None:
            continue
        if variant_filter and vshort != variant_filter:
            continue
        tidx = r.get("testIdx", -1)
        d[tidx] = r.get("success", False)
    return d

# Load 3 runs of DeepSeek exploration on same 120 trap prompts
r1_expl = load_results("results-deepseek-run1.json", "expl")
var_expl = load_results("results-deepseek-variance.json", "expl")
exp_expl = load_results("results-expanded-deepseek.json", "expl")

# Count Type II errors per run
runs = {
    "R1 (results-deepseek-run1.json)": r1_expl,
    "Variance (results-deepseek-variance.json)": var_expl,
    "Expanded (results-expanded-deepseek.json)": exp_expl,
}

run_errors = {}
for run_name, d in runs.items():
    errs = sum(1 for i in TRAP_IDX if i in d and not d[i])
    total = sum(1 for i in TRAP_IDX if i in d)
    run_errors[run_name] = {"type2_errors": errs, "type2_total": total}

# Find flips: prompts that differ between any pair of runs
flips = []
for i in TRAP_IDX:
    results = {}
    for run_name, d in runs.items():
        if i in d:
            results[run_name] = d[i]
    values = list(results.values())
    if len(set(values)) > 1:
        flips.append({"prompt_idx": i, "results": {k: v for k, v in results.items()}})

# Cross-run stability for ALL models (R1 vs Expanded, first 120 traps)
# This measures how much temp=0 results vary across separate API calls
cross_run_stability = {}
r1_files = {
    "DeepSeek": "results-deepseek-run1.json",
    "Gemini Flash": "results-gemini-flash.json",
    "Claude Haiku": "results-claude-haiku.json",
    "Claude Sonnet": "results-claude-sonnet.json",
}
exp_files = {
    "DeepSeek": "results-expanded-deepseek.json",
    "Gemini Flash": "results-expanded-gemini-flash.json",
    "Claude Haiku": "results-expanded-claude-haiku.json",
    "Claude Sonnet": "results-expanded-claude-sonnet.json",
}
r2_files = {
    "DeepSeek": "results-new-deepseek.json",
    "Gemini Flash": "results-new-gemini-flash.json",
    "Claude Haiku": "results-new-claude-haiku.json",
    "Claude Sonnet": "results-new-claude-sonnet.json",
}

for model in r1_files:
    cross_run_stability[model] = {}

    # R1 variants vs Expanded
    for v in ["base", "expl", "extr"]:
        r1_d = load_results(r1_files[model], v)
        exp_d = load_results(exp_files[model], v)
        r1_err = sum(1 for i in TRAP_IDX if i in r1_d and not r1_d[i])
        exp_err = sum(1 for i in TRAP_IDX if i in exp_d and not exp_d[i])
        n_flips = sum(1 for i in TRAP_IDX if i in r1_d and i in exp_d and r1_d[i] != exp_d[i])
        cross_run_stability[model][f"R1_vs_EXP_{v}"] = {
            "r1_errors": r1_err,
            "exp_errors": exp_err,
            "diff": abs(r1_err - exp_err),
            "n_flips": n_flips,
        }

    # R2 variants vs Expanded
    for v in ["gated", "extr2", "expl2", "expl3"]:
        r2_d = load_results(r2_files[model], v)
        exp_d = load_results(exp_files[model], v)
        r2_err = sum(1 for i in TRAP_IDX if i in r2_d and not r2_d[i])
        exp_err = sum(1 for i in TRAP_IDX if i in exp_d and not exp_d[i])
        n_flips = sum(1 for i in TRAP_IDX if i in r2_d and i in exp_d and r2_d[i] != exp_d[i])
        cross_run_stability[model][f"R2_vs_EXP_{v}"] = {
            "r2_errors": r2_err,
            "exp_errors": exp_err,
            "diff": abs(r2_err - exp_err),
            "n_flips": n_flips,
        }

# Summary stats
max_diff = 0
max_flips = 0
total_comparisons = 0
for model, comps in cross_run_stability.items():
    for comp_name, comp in comps.items():
        total_comparisons += 1
        max_diff = max(max_diff, comp["diff"])
        max_flips = max(max_flips, comp["n_flips"])

output = {
    "metadata": {
        "dataset": DATASET,
        "purpose": "Measure run-to-run stability at temperature=0",
        "deepseek_exploration_runs": {
            "R1": "results-deepseek-run1.json",
            "Variance": "results-deepseek-variance.json",
            "Expanded": "results-expanded-deepseek.json",
        },
        "computed_at": datetime.datetime.now().isoformat(),
        "script": "compute-variance.py",
    },
    "deepseek_exploration_3runs": run_errors,
    "deepseek_exploration_flips": flips,
    "cross_run_stability": cross_run_stability,
    "summary": {
        "total_cross_run_comparisons": total_comparisons,
        "max_error_count_diff": max_diff,
        "max_prompt_flips": max_flips,
        "note": "All comparisons on first 120 trap prompts (shared between R1/R2 and Expanded)",
    },
}

outpath = os.path.join(BASE, "calculations-variance.json")
with open(outpath, "w") as f:
    json.dump(output, f, indent=2)

print(f"Written: {outpath}")
print(f"\nDeepSeek exploration across 3 runs (Type II /120):")
for run, data in run_errors.items():
    print(f"  {run}: {data['type2_errors']}")
print(f"\nFlips (prompts with different results across runs): {len(flips)}")
for flip in flips:
    print(f"  idx {flip['prompt_idx']}: {flip['results']}")
print(f"\nCross-run stability (max diff={max_diff}, max flips={max_flips}):")
for model, comps in cross_run_stability.items():
    diffs = [c["diff"] for c in comps.values()]
    flips_list = [c["n_flips"] for c in comps.values()]
    print(f"  {model}: diffs={diffs}, flips={flips_list}")
