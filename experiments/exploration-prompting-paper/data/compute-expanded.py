"""Compute all statistics for Expanded benchmark dataset ONLY.
Source: 4 expanded result files x 311 prompts x 7 variants.
Output: calculations-expanded.json

IMPORTANT: This is a SEPARATE API run from R1/R2. Same prompts may produce
slightly different results (1-2 errors) due to temp=0 non-determinism.
Gemini Pro is NOT in this dataset (API rate limits).
"""
import json, os, datetime
from scipy.stats import binomtest

BASE = os.path.dirname(os.path.abspath(__file__))

DATASET = "Expanded"
SOURCE_FILES = {
    "DeepSeek": "results-expanded-deepseek.json",
    "Gemini Flash": "results-expanded-gemini-flash.json",
    "Claude Haiku": "results-expanded-claude-haiku.json",
    "Claude Sonnet": "results-expanded-claude-sonnet.json",
}
ALL_VARIANTS = ["base", "expl", "extr", "gated", "extr2", "expl2", "expl3"]
R1_VARIANTS = ["base", "expl", "extr"]
R2_VARIANTS = ["gated", "extr2", "expl2", "expl3"]
VARIANT_MAP = {
    "classifier-baseline.txt": "base",
    "classifier-exploration.txt": "expl",
    "classifier-extraction.txt": "extr",
    "classifier-baseline-gated.txt": "gated",
    "classifier-extraction-v2.txt": "extr2",
    "classifier-exploration-v2.txt": "expl2",
    "classifier-exploration-v3.txt": "expl3",
}

# Load expanded prompts
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

N_PROMPTS = len(prompts)
EFFECTIVE_CATS = {"disguised-correction", "context-contradiction"}
EFFECTIVE_IDX = {i for i, p in enumerate(prompts) if p.get("category") in EFFECTIVE_CATS}
QUICK_IDX = {i for i, p in enumerate(prompts) if p.get("category") == "genuinely-quick"}
ALL_TRAP_IDX = {i for i, p in enumerate(prompts) if p.get("category") != "genuinely-quick"}
N_EFFECTIVE = len(EFFECTIVE_IDX)
N_QUICK = len(QUICK_IDX)
N_ALL_TRAPS = len(ALL_TRAP_IDX)

# Category index map
CATEGORIES = sorted(set(p.get("category", "unknown") for p in prompts))
cat_indices = {}
for cat in CATEGORIES:
    cat_indices[cat] = {i for i, p in enumerate(prompts) if p.get("category") == cat}

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

# Error counts: effective traps only (primary), all traps, and quick
error_counts = {}
for model in SOURCE_FILES:
    error_counts[model] = {}
    d = all_data[model]
    for v in ALL_VARIANTS:
        eff_err = sum(1 for i in EFFECTIVE_IDX if (i, v) in d and not d[(i, v)])
        eff_total = sum(1 for i in EFFECTIVE_IDX if (i, v) in d)
        all_err = sum(1 for i in ALL_TRAP_IDX if (i, v) in d and not d[(i, v)])
        all_total = sum(1 for i in ALL_TRAP_IDX if (i, v) in d)
        quick_err = sum(1 for i in QUICK_IDX if (i, v) in d and not d[(i, v)])
        quick_total = sum(1 for i in QUICK_IDX if (i, v) in d)
        error_counts[model][v] = {
            "effective_type2_errors": eff_err,
            "effective_type2_total": eff_total,
            "all_trap_type2_errors": all_err,
            "all_trap_type2_total": all_total,
            "type1_errors": quick_err,
            "type1_total": quick_total,
        }

# Pooled (effective traps)
N_TOTAL_EFF = N_EFFECTIVE * len(SOURCE_FILES)  # 200 * 4 = 800
pooled = {}
for v in ALL_VARIANTS:
    eff_err = sum(error_counts[m][v]["effective_type2_errors"] for m in SOURCE_FILES)
    t1_err = sum(error_counts[m][v]["type1_errors"] for m in SOURCE_FILES)
    t1_total = sum(error_counts[m][v]["type1_total"] for m in SOURCE_FILES)
    pooled[v] = {
        "effective_type2_errors": eff_err,
        "effective_type2_total": N_TOTAL_EFF,
        "effective_type2_pct": round(eff_err / N_TOTAL_EFF * 100, 2),
        "type1_errors": t1_err,
        "type1_total": t1_total,
        "type1_pct": round(t1_err / t1_total * 100, 2) if t1_total > 0 else 0,
    }

# McNemar (effective traps, pooled across 4 models)
def mcnemar_pooled(var_a, var_b, models=None, idx_set=None):
    if models is None:
        models = list(SOURCE_FILES.keys())
    if idx_set is None:
        idx_set = EFFECTIVE_IDX
    a_wins = b_wins = 0
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
    p = binomtest(min(a_wins, b_wins), n, 0.5).pvalue if n > 0 else 1.0
    return {
        "var_a": var_a, "var_b": var_b,
        "a_wins": a_wins, "b_wins": b_wins,
        "n_discordant": n, "p_value": round(p, 6),
        "significant_005": bool(p < 0.05),
        "models": models, "n_models": len(models),
        "idx_set_size": len(idx_set),
    }

# Key comparisons
mcnemar_tests = {
    "expl2_vs_extr2": mcnemar_pooled("expl2", "extr2"),
    "expl3_vs_extr2": mcnemar_pooled("expl3", "extr2"),
    "expl2_vs_gated": mcnemar_pooled("expl2", "gated"),
    "expl2_vs_base": mcnemar_pooled("expl2", "base"),
    "extr2_vs_gated": mcnemar_pooled("extr2", "gated"),
    "expl2_vs_expl3_wording": mcnemar_pooled("expl2", "expl3"),
    # Missing from V3: expl(R1) vs expl2(R2) within Expanded — tests whether R1 wording differs from R2 wording
    "expl_vs_expl2_wording": mcnemar_pooled("expl", "expl2"),
    "expl_vs_expl3_wording": mcnemar_pooled("expl", "expl3"),
}

# Bonferroni correction: 8 pairwise comparisons -> alpha = 0.05/8 = 0.00625
BONFERRONI_ALPHA = 0.05 / len(mcnemar_tests)
bonferroni_results = {}
for k, t in mcnemar_tests.items():
    bonferroni_results[k] = {
        "p_value": t["p_value"],
        "bonferroni_alpha": round(BONFERRONI_ALPHA, 5),
        "significant_bonferroni": bool(t["p_value"] < BONFERRONI_ALPHA),
        "significant_005": bool(t["p_value"] < 0.05),
    }

# Excluding Sonnet (3 models)
models_3 = [m for m in SOURCE_FILES if m != "Claude Sonnet"]
mcnemar_excl_sonnet = {
    "expl2_vs_extr2": mcnemar_pooled("expl2", "extr2", models_3),
    "expl3_vs_extr2": mcnemar_pooled("expl3", "extr2", models_3),
}

# Per-model McNemar on key comparison
per_model_mcnemar = {}
for model in SOURCE_FILES:
    per_model_mcnemar[model] = {
        "expl2_vs_extr2": mcnemar_pooled("expl2", "extr2", [model]),
        "expl2_vs_gated": mcnemar_pooled("expl2", "gated", [model]),
        "expl2_vs_base": mcnemar_pooled("expl2", "base", [model]),
    }

# Category breakdown (effective + non-effective)
category_breakdown = {}
for model in SOURCE_FILES:
    category_breakdown[model] = {}
    d = all_data[model]
    for cat, indices in cat_indices.items():
        category_breakdown[model][cat] = {}
        for v in ALL_VARIANTS:
            errs = sum(1 for i in indices if (i, v) in d and not d[(i, v)])
            category_breakdown[model][cat][v] = {"errors": errs, "total": len(indices)}

# Wilson CIs (effective traps)
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
    for v in ALL_VARIANTS:
        ec = error_counts[model][v]
        wilson_cis[model][v] = wilson_ci(ec["effective_type2_errors"], ec["effective_type2_total"])

# Gate sensitivity (expanded data: base vs gated, effective traps)
gate_sensitivity = {}
for model in SOURCE_FILES:
    b = error_counts[model]["base"]["effective_type2_errors"]
    g = error_counts[model]["gated"]["effective_type2_errors"]
    gate_sensitivity[model] = {
        "baseline_errors": b,
        "gated_errors": g,
        "diff": g - b,
        "direction": "helped" if g < b else ("harmed" if g > b else "no change"),
    }

# === Cochran-Mantel-Haenszel (CMH) test ===
def cmh_test(var_a, var_b, models=None, idx_set=None):
    """CMH stratified by model. More principled than naive pooling."""
    if models is None:
        models = list(SOURCE_FILES.keys())
    if idx_set is None:
        idx_set = EFFECTIVE_IDX
    from scipy.stats import chi2

    tables = []
    for model in models:
        d = all_data[model]
        cw = wc = 0
        for idx in idx_set:
            a = d.get((idx, var_a), True)
            b = d.get((idx, var_b), True)
            if a and not b: cw += 1
            elif not a and b: wc += 1
        tables.append({"model": model, "cw": cw, "wc": wc})

    num_sum = sum(t["cw"] - t["wc"] for t in tables)
    den_sum = sum(t["cw"] + t["wc"] for t in tables)

    if den_sum == 0:
        return {"cmh_statistic": 0, "cmh_p_value": 1.0, "per_stratum": tables}

    cmh_stat = (abs(num_sum) - 1) ** 2 / den_sum
    p = float(1 - chi2.cdf(cmh_stat, 1))

    # Breslow-Day homogeneity test
    total_cw = sum(t["cw"] for t in tables)
    total_wc = sum(t["wc"] for t in tables)
    common_or = total_cw / total_wc if total_wc > 0 else float("inf")

    bd_stat = 0
    bd_valid = True
    active_strata = 0
    for t in tables:
        n_disc = t["cw"] + t["wc"]
        if n_disc == 0:
            continue
        active_strata += 1
        exp_cw = n_disc * common_or / (1 + common_or)
        exp_wc = n_disc - exp_cw
        if exp_cw > 0 and exp_wc > 0:
            bd_stat += (t["cw"] - exp_cw) ** 2 / exp_cw + (t["wc"] - exp_wc) ** 2 / exp_wc
        else:
            bd_valid = False

    bd_df = active_strata - 1
    bd_p = float(1 - chi2.cdf(bd_stat, bd_df)) if bd_valid and bd_df > 0 else None

    return {
        "cmh_statistic": round(cmh_stat, 4),
        "cmh_p_value": round(p, 6),
        "cmh_significant_005": bool(p < 0.05),
        "breslow_day_statistic": round(bd_stat, 4) if bd_valid else None,
        "breslow_day_p_value": round(bd_p, 6) if bd_p is not None else None,
        "breslow_day_homogeneous_005": bool(bd_p > 0.05) if bd_p is not None else None,
        "common_odds_ratio": round(common_or, 2) if common_or != float("inf") else "inf",
        "per_stratum": tables,
        "note": "CMH stratified by model. Breslow-Day tests homogeneity across strata.",
    }

cmh_tests = {
    "expl2_vs_extr2": cmh_test("expl2", "extr2"),
    "expl2_vs_gated": cmh_test("expl2", "gated"),
    "expl2_vs_base": cmh_test("expl2", "base"),
}

# Output
output = {
    "metadata": {
        "dataset": DATASET,
        "source_files": SOURCE_FILES,
        "n_prompts": N_PROMPTS,
        "n_effective_traps": N_EFFECTIVE,
        "n_all_traps": N_ALL_TRAPS,
        "n_quick": N_QUICK,
        "effective_categories": sorted(EFFECTIVE_CATS),
        "all_variants": ALL_VARIANTS,
        "models": list(SOURCE_FILES.keys()),
        "n_models": len(SOURCE_FILES),
        "note": "Gemini Pro NOT included (API rate limits). This is a SEPARATE run from R1/R2.",
        "computed_at": datetime.datetime.now().isoformat(),
        "script": "compute-expanded.py",
        "prompt_file": "prompts-expanded.yaml",
    },
    "error_counts": error_counts,
    "pooled": pooled,
    "mcnemar_tests": mcnemar_tests,
    "mcnemar_excl_sonnet": mcnemar_excl_sonnet,
    "per_model_mcnemar": per_model_mcnemar,
    "category_breakdown": category_breakdown,
    "wilson_cis": wilson_cis,
    "gate_sensitivity": gate_sensitivity,
    "bonferroni": bonferroni_results,
    "cmh_tests": cmh_tests,
}

outpath = os.path.join(BASE, "calculations-expanded.json")
with open(outpath, "w") as f:
    json.dump(output, f, indent=2)

print(f"Written: {outpath}")
print(f"Models: {len(SOURCE_FILES)}, Variants: {len(ALL_VARIANTS)}, Effective traps: {N_EFFECTIVE}, Total N: {N_TOTAL_EFF}")
print(f"\nEffective Type II pooled:")
for v in ALL_VARIANTS:
    print(f"  {v}: {pooled[v]['effective_type2_errors']} ({pooled[v]['effective_type2_pct']}%)")
print(f"\nMcNemar (4 models, effective traps):")
for k, t in mcnemar_tests.items():
    sig = "***" if t["p_value"] < 0.001 else ("*" if t["p_value"] < 0.05 else "ns")
    print(f"  {k}: {t['a_wins']}:{t['b_wins']} p={t['p_value']} {sig}")
print(f"\nExcl Sonnet (3 models):")
for k, t in mcnemar_excl_sonnet.items():
    print(f"  {k}: {t['a_wins']}:{t['b_wins']} p={t['p_value']}")
print(f"\nPer-model expl2 vs extr2:")
for model, tests in per_model_mcnemar.items():
    t = tests["expl2_vs_extr2"]
    print(f"  {model}: {t['a_wins']}:{t['b_wins']} p={t['p_value']}")
print(f"\nGate sensitivity (expanded, effective traps):")
for model, gs in gate_sensitivity.items():
    print(f"  {model}: base={gs['baseline_errors']}, gated={gs['gated_errors']}, diff={gs['diff']:+d} ({gs['direction']})")

print(f"\nBonferroni (alpha={BONFERRONI_ALPHA:.5f} for {len(mcnemar_tests)} comparisons):")
for k, b in bonferroni_results.items():
    surv = "SURVIVES" if b["significant_bonferroni"] else "does not survive"
    print(f"  {k}: p={b['p_value']} {surv}")

print(f"\nCMH tests (stratified by model):")
for k, c in cmh_tests.items():
    bd = f"BD p={c['breslow_day_p_value']}" if c.get("breslow_day_p_value") is not None else "BD N/A"
    homo = " (homogeneous)" if c.get("breslow_day_homogeneous_005") else " (HETEROGENEOUS)" if c.get("breslow_day_homogeneous_005") is False else ""
    print(f"  {k}: CMH chi2={c['cmh_statistic']}, p={c['cmh_p_value']}, {bd}{homo}")
    for s in c["per_stratum"]:
        print(f"    {s['model']}: cw={s['cw']}, wc={s['wc']}")
