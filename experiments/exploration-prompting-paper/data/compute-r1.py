"""Compute all statistics for Round 1 dataset ONLY.
Source: 5 R1 result files x 151 prompts x 3 variants.
Output: calculations-r1.json
"""
import json, os, datetime
from collections import Counter
from scipy.stats import binomtest

BASE = os.path.dirname(os.path.abspath(__file__))

# === Configuration (R1 only) ===
DATASET = "R1"
SOURCE_FILES = {
    "DeepSeek": "results-deepseek-run1.json",
    "Gemini Flash": "results-gemini-flash.json",
    "Gemini Pro": "results-gemini-pro.json",
    "Claude Haiku": "results-claude-haiku.json",
    "Claude Sonnet": "results-claude-sonnet.json",
}
VARIANTS = ["base", "expl", "extr"]
VARIANT_MAP = {
    "classifier-baseline.txt": "base",
    "classifier-exploration.txt": "expl",
    "classifier-extraction.txt": "extr",
}
TRAP_IDX = set(range(120))
QUICK_IDX = set(range(120, 151))
N_TRAPS = 120
N_QUICK = 31
N_PROMPTS = 151

# === Load prompts for category info ===
prompts = []
current = None
with open(os.path.join(BASE, "prompts.yaml"), "r", encoding="utf-8") as f:
    for line in f:
        s = line.strip()
        if s.startswith("- prompt:"):
            if current:
                prompts.append(current)
            current = {"prompt": s.replace("- prompt:", "").strip().strip('"')}
        elif current and s.startswith("category:"):
            current["category"] = s.replace("category:", "").strip()
if current:
    prompts.append(current)

CATEGORIES = sorted(set(p.get("category", "unknown") for p in prompts if prompts.index(p) < 120))
cat_indices = {}
for cat in CATEGORIES:
    cat_indices[cat] = {i for i, p in enumerate(prompts) if p.get("category") == cat and i < 120}

# === Load data ===
def load_results(fname):
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
        tidx = r.get("testIdx", -1)
        d[(tidx, vshort)] = r.get("success", False)
    return d

all_data = {}
for model, fname in SOURCE_FILES.items():
    all_data[model] = load_results(fname)

# === Compute error counts ===
error_counts = {}
for model in SOURCE_FILES:
    error_counts[model] = {}
    d = all_data[model]
    for v in VARIANTS:
        t2 = sum(1 for i in TRAP_IDX if (i, v) in d and not d[(i, v)])
        t1 = sum(1 for i in QUICK_IDX if (i, v) in d and not d[(i, v)])
        total_trap = sum(1 for i in TRAP_IDX if (i, v) in d)
        total_quick = sum(1 for i in QUICK_IDX if (i, v) in d)
        error_counts[model][v] = {
            "type2_errors": t2,
            "type2_total": total_trap,
            "type1_errors": t1,
            "type1_total": total_quick,
        }

# === Pooled error counts ===
pooled = {}
for v in VARIANTS:
    t2 = sum(error_counts[m][v]["type2_errors"] for m in SOURCE_FILES)
    t2_total = sum(error_counts[m][v]["type2_total"] for m in SOURCE_FILES)
    t1 = sum(error_counts[m][v]["type1_errors"] for m in SOURCE_FILES)
    t1_total = sum(error_counts[m][v]["type1_total"] for m in SOURCE_FILES)
    pooled[v] = {
        "type2_errors": t2,
        "type2_total": t2_total,
        "type2_pct": round(t2 / t2_total * 100, 2) if t2_total > 0 else 0,
        "type1_errors": t1,
        "type1_total": t1_total,
        "type1_pct": round(t1 / t1_total * 100, 2) if t1_total > 0 else 0,
    }

# === McNemar pairwise tests (pooled across models) ===
def mcnemar_pooled(var_a, var_b, models=None, idx_set=None):
    if models is None:
        models = list(SOURCE_FILES.keys())
    if idx_set is None:
        idx_set = TRAP_IDX
    a_wins = 0
    b_wins = 0
    for model in models:
        d = all_data[model]
        for idx in idx_set:
            a_ok = d.get((idx, var_a), True)
            b_ok = d.get((idx, var_b), True)
            if a_ok and not b_ok:
                a_wins += 1
            elif b_ok and not a_ok:
                b_wins += 1
    n = a_wins + b_wins
    if n == 0:
        p = 1.0
    else:
        p = binomtest(min(a_wins, b_wins), n, 0.5).pvalue
    return {
        "var_a": var_a,
        "var_b": var_b,
        "a_wins": a_wins,
        "b_wins": b_wins,
        "n_discordant": n,
        "p_value": round(p, 6),
        "significant_005": bool(p < 0.05),
        "models": models,
        "n_prompts_per_model": len(idx_set),
    }

mcnemar_tests = {
    "expl_vs_base": mcnemar_pooled("expl", "base"),
    "expl_vs_extr": mcnemar_pooled("expl", "extr"),
    "base_vs_extr": mcnemar_pooled("base", "extr"),
}

# Per-model McNemar
per_model_mcnemar = {}
for model in SOURCE_FILES:
    per_model_mcnemar[model] = {}
    for label, va, vb in [("expl_vs_base", "expl", "base"), ("expl_vs_extr", "expl", "extr")]:
        per_model_mcnemar[model][label] = mcnemar_pooled(va, vb, models=[model])

# === Category breakdown ===
category_breakdown = {}
for model in SOURCE_FILES:
    category_breakdown[model] = {}
    d = all_data[model]
    for cat, indices in cat_indices.items():
        category_breakdown[model][cat] = {}
        for v in VARIANTS:
            errs = sum(1 for i in indices if (i, v) in d and not d[(i, v)])
            category_breakdown[model][cat][v] = {
                "errors": errs,
                "total": len(indices),
            }

# === Wilson CIs ===
def wilson_ci(k, n, z=1.96):
    if n == 0:
        return {"lower": 0, "upper": 0, "point": 0}
    p_hat = k / n
    denom = 1 + z * z / n
    center = (p_hat + z * z / (2 * n)) / denom
    spread = z * ((p_hat * (1 - p_hat) / n + z * z / (4 * n * n)) ** 0.5) / denom
    return {
        "lower": round(max(0, center - spread) * 100, 2),
        "upper": round(min(1, center + spread) * 100, 2),
        "point": round(p_hat * 100, 2),
    }

wilson_cis = {}
for model in SOURCE_FILES:
    wilson_cis[model] = {}
    for v in VARIANTS:
        ec = error_counts[model][v]
        wilson_cis[model][v] = wilson_ci(ec["type2_errors"], ec["type2_total"])

# === Build output ===
output = {
    "metadata": {
        "dataset": DATASET,
        "source_files": SOURCE_FILES,
        "n_prompts": N_PROMPTS,
        "n_traps": N_TRAPS,
        "n_quick": N_QUICK,
        "variants": VARIANTS,
        "models": list(SOURCE_FILES.keys()),
        "n_models": len(SOURCE_FILES),
        "computed_at": datetime.datetime.now().isoformat(),
        "script": "compute-r1.py",
        "prompt_file": "prompts.yaml",
    },
    "error_counts": error_counts,
    "pooled": pooled,
    "mcnemar_tests": mcnemar_tests,
    "per_model_mcnemar": per_model_mcnemar,
    "category_breakdown": category_breakdown,
    "wilson_cis": wilson_cis,
}

outpath = os.path.join(BASE, "calculations-r1.json")
with open(outpath, "w") as f:
    json.dump(output, f, indent=2)

print(f"Written: {outpath}")
print(f"Models: {len(SOURCE_FILES)}, Variants: {len(VARIANTS)}, Prompts: {N_PROMPTS}")
t2_parts = [f"{v}={pooled[v]['type2_errors']}({pooled[v]['type2_pct']}%)" for v in VARIANTS]
t1_parts = [f"{v}={pooled[v]['type1_errors']}({pooled[v]['type1_pct']}%)" for v in VARIANTS]
print(f"\nType II pooled: {', '.join(t2_parts)}")
print(f"Type I pooled: {', '.join(t1_parts)}")
print(f"\nMcNemar (pooled):")
for k, t in mcnemar_tests.items():
    print(f"  {k}: {t['a_wins']}:{t['b_wins']} p={t['p_value']}")
