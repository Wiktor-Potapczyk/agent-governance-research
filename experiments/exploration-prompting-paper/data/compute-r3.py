"""Compute all statistics for Round 3 (think-carefully) dataset ONLY.
Source: 1 result file x 311 prompts x 1 variant x 4 models.
Output: calculations-r3.json

This is a MECHANISM ABLATION experiment: tests whether a content-free
metacognitive instruction achieves the same effect as open-ended exploration.
"""
import json, os, datetime
from scipy.stats import binomtest

BASE = os.path.dirname(os.path.abspath(__file__))

DATASET = "R3"
SOURCE_FILE = "results-think-carefully.json"
VARIANT = "think"

# Load prompts
prompts = []
current = None
with open(os.path.join(BASE, "prompts-expanded.yaml"), "r", encoding="utf-8") as f:
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

EFFECTIVE_CATS = {"disguised-correction", "context-contradiction"}
EFFECTIVE_IDX = {i for i, p in enumerate(prompts) if p.get("category") in EFFECTIVE_CATS}
QUICK_IDX = {i for i, p in enumerate(prompts) if p.get("category") == "genuinely-quick"}
ALL_TRAP_IDX = {i for i, p in enumerate(prompts) if p.get("category") != "genuinely-quick"}
N_PROMPTS = len(prompts)
N_EFFECTIVE = len(EFFECTIVE_IDX)
N_QUICK = len(QUICK_IDX)

CATEGORIES = sorted(set(p.get("category", "unknown") for p in prompts))
cat_indices = {}
for cat in CATEGORIES:
    cat_indices[cat] = {i for i, p in enumerate(prompts) if p.get("category") == cat}

MODEL_MAP = {
    "openai:chat:deepseek-chat": "DeepSeek",
    "google:gemini-2.5-flash": "Gemini Flash",
    "anthropic:messages:claude-haiku-4-5-20251001": "Claude Haiku",
    "anthropic:messages:claude-4-sonnet-20250514": "Claude Sonnet",
}

# Load results
with open(os.path.join(BASE, SOURCE_FILE)) as f:
    data = json.load(f)

all_data = {}
for r in data["results"]["results"]:
    pid = r["provider"]["id"] if isinstance(r["provider"], dict) else r["provider"]
    short = MODEL_MAP.get(pid, pid)
    if short not in all_data:
        all_data[short] = {}
    all_data[short][r["testIdx"]] = r.get("success", False)

MODELS = list(MODEL_MAP.values())

# Error counts
error_counts = {}
for model in MODELS:
    d = all_data.get(model, {})
    eff_err = sum(1 for i in EFFECTIVE_IDX if i in d and not d[i])
    all_err = sum(1 for i in ALL_TRAP_IDX if i in d and not d[i])
    quick_err = sum(1 for i in QUICK_IDX if i in d and not d[i])
    error_counts[model] = {
        "effective_type2_errors": eff_err,
        "effective_type2_total": N_EFFECTIVE,
        "all_trap_type2_errors": all_err,
        "all_trap_type2_total": len(ALL_TRAP_IDX),
        "type1_errors": quick_err,
        "type1_total": N_QUICK,
    }

# Pooled
N_TOTAL_EFF = N_EFFECTIVE * len(MODELS)
eff_pool = sum(error_counts[m]["effective_type2_errors"] for m in MODELS)
t1_pool = sum(error_counts[m]["type1_errors"] for m in MODELS)
pooled = {
    "effective_type2_errors": eff_pool,
    "effective_type2_total": N_TOTAL_EFF,
    "effective_type2_pct": round(eff_pool / N_TOTAL_EFF * 100, 2),
    "type1_errors": t1_pool,
    "type1_total": N_QUICK * len(MODELS),
    "type1_pct": round(t1_pool / (N_QUICK * len(MODELS)) * 100, 2),
}

# Cross-variant McNemar: think vs EXP variants
# Load EXP data for comparison
EXP_FILES = {
    "DeepSeek": "results-expanded-deepseek.json",
    "Gemini Flash": "results-expanded-gemini-flash.json",
    "Claude Haiku": "results-expanded-claude-haiku.json",
    "Claude Sonnet": "results-expanded-claude-sonnet.json",
}
EXP_VARIANT_MAP = {
    "classifier-baseline.txt": "base",
    "classifier-exploration.txt": "expl",
    "classifier-extraction.txt": "extr",
    "classifier-baseline-gated.txt": "gated",
    "classifier-extraction-v2.txt": "extr2",
    "classifier-exploration-v2.txt": "expl2",
    "classifier-exploration-v3.txt": "expl3",
}

exp_data = {}
for model, fname in EXP_FILES.items():
    with open(os.path.join(BASE, fname)) as f:
        raw = json.load(f)
    exp_data[model] = {}
    for r in raw["results"]["results"]:
        label = r.get("prompt", {}).get("label", "")
        vkey = label.split(":")[0].strip()
        vshort = EXP_VARIANT_MAP.get(vkey)
        if vshort is None:
            continue
        tidx = r.get("testIdx", -1)
        if vshort not in exp_data[model]:
            exp_data[model][vshort] = {}
        exp_data[model][vshort][tidx] = r.get("success", False)

def mcnemar_cross(exp_variant, models=None):
    """McNemar comparing EXP variant vs R3 think-carefully.
    NOTE: This is a CROSS-DATASET comparison (EXP run vs R3 run).
    """
    if models is None:
        models = MODELS
    a_wins = b_wins = 0
    for model in models:
        d_exp = exp_data.get(model, {}).get(exp_variant, {})
        d_think = all_data.get(model, {})
        for idx in EFFECTIVE_IDX:
            a = d_exp.get(idx, True)
            b = d_think.get(idx, True)
            if a and not b:
                a_wins += 1
            elif b and not a:
                b_wins += 1
    n = a_wins + b_wins
    p = binomtest(min(a_wins, b_wins), n, 0.5).pvalue if n > 0 else 1.0
    return {
        "var_a": exp_variant,
        "var_b": "think",
        "a_wins": a_wins,
        "b_wins": b_wins,
        "n_discordant": n,
        "p_value": round(p, 6),
        "significant_005": bool(p < 0.05),
        "models": models,
        "n_models": len(models),
        "note": "CROSS-DATASET: EXP run vs R3 run. Same prompts, different API calls.",
    }

mcnemar_vs_exp = {
    "expl2_vs_think": mcnemar_cross("expl2"),
    "expl3_vs_think": mcnemar_cross("expl3"),
    "expl_vs_think": mcnemar_cross("expl"),
    "extr2_vs_think": mcnemar_cross("extr2"),
    "gated_vs_think": mcnemar_cross("gated"),
    "base_vs_think": mcnemar_cross("base"),
}

# Per-model McNemar: expl2 vs think
per_model_mcnemar = {}
for model in MODELS:
    per_model_mcnemar[model] = {
        "expl2_vs_think": mcnemar_cross("expl2", [model]),
        "extr2_vs_think": mcnemar_cross("extr2", [model]),
    }

# Category breakdown
category_breakdown = {}
for model in MODELS:
    category_breakdown[model] = {}
    d = all_data.get(model, {})
    for cat, indices in cat_indices.items():
        errs = sum(1 for i in indices if i in d and not d[i])
        category_breakdown[model][cat] = {"errors": errs, "total": len(indices)}

# Wilson CIs
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
for model in MODELS:
    ec = error_counts[model]
    wilson_cis[model] = wilson_ci(ec["effective_type2_errors"], ec["effective_type2_total"])

# Output
output = {
    "metadata": {
        "dataset": DATASET,
        "source_file": SOURCE_FILE,
        "n_prompts": N_PROMPTS,
        "n_effective_traps": N_EFFECTIVE,
        "n_quick": N_QUICK,
        "variant": VARIANT,
        "models": MODELS,
        "n_models": len(MODELS),
        "purpose": "Mechanism ablation: content-free metacognitive instruction vs open-ended exploration",
        "note": "Cross-variant comparisons with EXP are CROSS-DATASET (different API runs).",
        "computed_at": datetime.datetime.now().isoformat(),
        "script": "compute-r3.py",
        "prompt_file": "prompts-expanded.yaml",
    },
    "error_counts": error_counts,
    "pooled": pooled,
    "mcnemar_vs_exp": mcnemar_vs_exp,
    "per_model_mcnemar": per_model_mcnemar,
    "category_breakdown": category_breakdown,
    "wilson_cis": wilson_cis,
}

outpath = os.path.join(BASE, "calculations-r3.json")
with open(outpath, "w") as f:
    json.dump(output, f, indent=2)

print(f"Written: {outpath}")
print(f"Models: {len(MODELS)}, Variant: {VARIANT}, Effective traps: {N_EFFECTIVE}, Total N: {N_TOTAL_EFF}")
print(f"\nPer-model Type II (effective /200):")
for model in MODELS:
    ec = error_counts[model]
    print(f"  {model}: {ec['effective_type2_errors']} ({ec['effective_type2_errors']/200*100:.1f}%)")
print(f"Pooled: {pooled['effective_type2_errors']}/{pooled['effective_type2_total']} ({pooled['effective_type2_pct']}%)")
print(f"\nType I pooled: {pooled['type1_errors']}/{pooled['type1_total']} ({pooled['type1_pct']}%)")
print(f"\nMcNemar vs EXP variants (CROSS-DATASET):")
for k, t in mcnemar_vs_exp.items():
    sig = "***" if t["p_value"] < 0.001 else ("*" if t["p_value"] < 0.05 else "ns")
    direction = f"{t['var_a']} better" if t["a_wins"] > t["b_wins"] else f"think better" if t["b_wins"] > t["a_wins"] else "tied"
    print(f"  {k}: {t['a_wins']}:{t['b_wins']} p={t['p_value']} {sig} ({direction})")
print(f"\nPer-model expl2 vs think:")
for model in MODELS:
    t = per_model_mcnemar[model]["expl2_vs_think"]
    print(f"  {model}: {t['a_wins']}:{t['b_wins']} p={t['p_value']}")
