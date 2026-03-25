"""Generate figures for the Exploration Prompting paper — V2 with Round 2 data."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

FIGDIR = os.path.join(os.path.dirname(__file__), 'figures')
os.makedirs(FIGDIR, exist_ok=True)

# ── Data (Round 1 + Round 2, 4 models confirmed, Gemini Pro TBD) ─

models = ['DeepSeek', 'Gemini\nFlash', 'Claude\nHaiku', 'Claude\nSonnet']
models_short = ['DeepSeek', 'Gemini Flash', 'Claude Haiku', 'Claude Sonnet']

# Round 1 data
r1_baseline =    [7, 2, 5, 4]
r1_exploration = [0, 0, 1, 4]
r1_extraction =  [15, 2, 4, 6]

# Round 2 data
r2_base_gated = [3, 1, 17, 15]
r2_extr_v2 =    [2, 1, 4, 4]
r2_expl_v2 =    [1, 0, 0, 3]
r2_expl_v3 =    [0, 1, 2, 1]

N = 120

# Colors
C_BASE = '#5B7553'
C_EXPL = '#2C5F8A'
C_EXTR = '#B85C38'
C_GATED = '#8B6914'
C_EXTR2 = '#C4785B'
C_EXPL2 = '#4A82B0'
C_EXPL3 = '#6FA8D6'

# ── Fig 1: Round 1 vs Round 2 comparison (main result) ──────────

fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)

x = np.arange(len(models))
w = 0.22

# Left: Round 1
ax = axes[0]
ax.bar(x - w, r1_baseline, w, label='Baseline (no gate)', color=C_BASE, edgecolor='white')
ax.bar(x, r1_exploration, w, label='Exploration: "imply?"', color=C_EXPL, edgecolor='white')
ax.bar(x + w, r1_extraction, w, label='Extraction: "name agent"', color=C_EXTR, edgecolor='white')
for i, (b, e, x_) in enumerate(zip(r1_baseline, r1_exploration, r1_extraction)):
    for val, pos in [(b, x[i]-w), (e, x[i]), (x_, x[i]+w)]:
        if val > 0:
            ax.text(pos, val+0.3, str(val), ha='center', va='bottom', fontsize=8)
ax.set_ylabel('Type II Errors (missed traps / 120)', fontsize=10)
ax.set_xticks(x)
ax.set_xticklabels(models, fontsize=8.5)
ax.set_title('Round 1: Original Variants', fontsize=11, pad=10)
ax.legend(fontsize=7.5, loc='upper left')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_ylim(0, 20)

# Right: Round 2
ax = axes[1]
w2 = 0.18
ax.bar(x - 1.5*w2, r2_base_gated, w2, label='Baseline (gated)', color=C_GATED, edgecolor='white')
ax.bar(x - 0.5*w2, r2_extr_v2, w2, label='Extraction: "summarize intent"', color=C_EXTR2, edgecolor='white')
ax.bar(x + 0.5*w2, r2_expl_v2, w2, label='Exploration: "going on?"', color=C_EXPL2, edgecolor='white')
ax.bar(x + 1.5*w2, r2_expl_v3, w2, label='Exploration: "require?"', color=C_EXPL3, edgecolor='white')
for i in range(len(models)):
    for val, pos in [(r2_base_gated[i], x[i]-1.5*w2), (r2_extr_v2[i], x[i]-0.5*w2),
                     (r2_expl_v2[i], x[i]+0.5*w2), (r2_expl_v3[i], x[i]+1.5*w2)]:
        if val > 0:
            ax.text(pos, val+0.3, str(val), ha='center', va='bottom', fontsize=8)
ax.set_xticks(x)
ax.set_xticklabels(models, fontsize=8.5)
ax.set_title('Round 2: Controlled Variants', fontsize=11, pad=10)
ax.legend(fontsize=7.5, loc='upper left')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_ylim(0, 20)

plt.tight_layout()
plt.savefig(os.path.join(FIGDIR, 'fig1-round-comparison.pdf'), dpi=300, bbox_inches='tight')
plt.savefig(os.path.join(FIGDIR, 'fig1-round-comparison.png'), dpi=300, bbox_inches='tight')
plt.close()
print('Fig 1: Round comparison - DONE')

# ── Fig 2: Wording ablation (exploration variants only) ──────────

fig, ax = plt.subplots(figsize=(8, 4))

x = np.arange(len(models))
w = 0.22

ax.bar(x - w, r1_exploration, w, label='"What does this prompt imply?"', color='#1a4472', edgecolor='white')
ax.bar(x, r2_expl_v2, w, label='"What\'s really going on here?"', color='#2C5F8A', edgecolor='white')
ax.bar(x + w, r2_expl_v3, w, label='"What does this request actually require?"', color='#6FA8D6', edgecolor='white')

for i in range(len(models)):
    for val, pos in [(r1_exploration[i], x[i]-w), (r2_expl_v2[i], x[i]), (r2_expl_v3[i], x[i]+w)]:
        ax.text(pos, val+0.15, str(val), ha='center', va='bottom', fontsize=9)

ax.set_ylabel('Type II Errors / 120', fontsize=10)
ax.set_xticks(x)
ax.set_xticklabels(models, fontsize=9)
ax.set_title('Wording Ablation: Three Open-Ended Questions\nAll perform in 0-4 error range per model', fontsize=11, pad=12)
ax.legend(fontsize=8, loc='upper right')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_ylim(0, 6)

plt.tight_layout()
plt.savefig(os.path.join(FIGDIR, 'fig2-wording-ablation.pdf'), dpi=300, bbox_inches='tight')
plt.savefig(os.path.join(FIGDIR, 'fig2-wording-ablation.png'), dpi=300, bbox_inches='tight')
plt.close()
print('Fig 2: Wording ablation - DONE')

# ── Fig 3: Gate sensitivity (gated baseline vs original) ─────────

fig, ax = plt.subplots(figsize=(7, 4))

x = np.arange(len(models))
w = 0.3

ax.bar(x - w/2, r1_baseline, w, label='Original baseline (no gate)', color=C_BASE, edgecolor='white')
ax.bar(x + w/2, r2_base_gated, w, label='Gated baseline (+ depth signal check)', color=C_GATED, edgecolor='white')

for i in range(len(models)):
    ax.text(x[i]-w/2, r1_baseline[i]+0.3, str(r1_baseline[i]), ha='center', va='bottom', fontsize=9)
    ax.text(x[i]+w/2, r2_base_gated[i]+0.3, str(r2_base_gated[i]), ha='center', va='bottom', fontsize=9)

# Annotate direction
for i in range(len(models)):
    delta = r2_base_gated[i] - r1_baseline[i]
    color = 'green' if delta < 0 else 'red' if delta > 0 else 'gray'
    ax.annotate(f'{delta:+d}', xy=(x[i]+w/2, r2_base_gated[i]+1.5),
                fontsize=9, ha='center', color=color, fontweight='bold')

ax.set_ylabel('Type II Errors / 120', fontsize=10)
ax.set_xticks(x)
ax.set_xticklabels(models, fontsize=9)
ax.set_title('Gate Sensitivity: Adding depth-signal check to baseline\nHelps DeepSeek/Flash, hurts Claude models', fontsize=11, pad=12)
ax.legend(fontsize=8.5, loc='upper left')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_ylim(0, 20)

plt.tight_layout()
plt.savefig(os.path.join(FIGDIR, 'fig3-gate-sensitivity.pdf'), dpi=300, bbox_inches='tight')
plt.savefig(os.path.join(FIGDIR, 'fig3-gate-sensitivity.png'), dpi=300, bbox_inches='tight')
plt.close()
print('Fig 3: Gate sensitivity - DONE')

# ── Fig 4: Pooled CIs (exploration vs extraction-v2 vs gated base)

from statsmodels.stats.proportion import proportion_confint

fig, ax = plt.subplots(figsize=(6, 4))

# Pool across 4 models (480 traps each)
n_pool = 4 * 120  # 480
pooled = [
    ('Baseline (gated)', sum(r2_base_gated), n_pool, C_GATED),
    ('Extraction v2\n"summarize intent"', sum(r2_extr_v2), n_pool, C_EXTR2),
    ('Exploration (avg 3 wordings)', round(sum(r1_exploration+r2_expl_v2+r2_expl_v3)/3), n_pool, C_EXPL),
]

y_pos = np.arange(len(pooled))
for i, (name, err, n, color) in enumerate(pooled):
    rate = err/n * 100
    lo, hi = proportion_confint(err, n, alpha=0.05, method='wilson')
    lo *= 100; hi *= 100
    ax.barh(i, rate, 0.5, color=color, edgecolor='white')
    ax.errorbar(rate, i, xerr=[[rate-lo], [hi-rate]], fmt='none', ecolor='black', capsize=4, linewidth=1.2)
    ax.text(hi + 0.3, i, f'{rate:.1f}% [{lo:.1f}, {hi:.1f}]', va='center', fontsize=8)

ax.set_yticks(y_pos)
ax.set_yticklabels([d[0] for d in pooled], fontsize=9)
ax.set_xlabel('Type II Error Rate (%) with 95% Wilson CI', fontsize=9)
ax.set_title('Round 2: Pooled Error Rates (N=480, 4 models)', fontsize=10, pad=10)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_xlim(0, 12)

plt.tight_layout()
plt.savefig(os.path.join(FIGDIR, 'fig4-pooled-ci-r2.pdf'), dpi=300, bbox_inches='tight')
plt.savefig(os.path.join(FIGDIR, 'fig4-pooled-ci-r2.png'), dpi=300, bbox_inches='tight')
plt.close()
print('Fig 4: Pooled CIs Round 2 - DONE')

print('\nAll figures saved to', FIGDIR)
