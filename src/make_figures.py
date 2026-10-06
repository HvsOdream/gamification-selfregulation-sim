import json, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9, 'axes.unicode_minus': False})
GREY_H = '#8c8c8c'; BLACK = '#000000'; DARK = '#222222'

def hbox(ax, x, y, w, h, header, body, hh=0.36, fs=9, hfs=8.5, bold=False):
    """journal-style box: grey header band + white body, thin black border"""
    ax.add_patch(Rectangle((x, y), w, h, fc='white', ec=BLACK, lw=0.9))
    ax.add_patch(Rectangle((x, y + h - hh), w, hh, fc=GREY_H, ec=BLACK, lw=0.9))
    ax.text(x + w/2, y + h - hh/2, header, ha='center', va='center', fontsize=hfs, color='white')
    ax.text(x + w/2, y + (h - hh)/2, body, ha='center', va='center', fontsize=fs, color=DARK,
            linespacing=1.35, fontweight='bold' if bold else 'normal')

def arrow(ax, p, q, ls='-', lw=1.2, style='-|>', ms=11, conn=None):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=style, color=BLACK, lw=lw, ls=ls, mutation_scale=ms,
                                 shrinkA=0, shrinkB=0, connectionstyle=conn or 'arc3,rad=0'))

# ---------------- Fig. 1 ----------------
fig, ax = plt.subplots(figsize=(10.8, 4.6), dpi=300)
ax.set_xlim(0, 10.8); ax.set_ylim(0, 4.6); ax.axis('off')
w, h, y0 = 2.2, 1.25, 0.95
xs = [0.3, 3.0, 5.7, 8.4]
heads = ['Demand', 'Signal', 'Shift', 'Failure']
bodies = ['Sustained\nself-regulatory demand',
          'Change in\nfatigue / cost signals',
          'Shift in motivation\nand attention allocation',
          'Dropout, delay,\ntask switching\n(conflicting with goal)']
for x, hd, bd in zip(xs, heads, bodies):
    hbox(ax, x, y0, w, h, hd, bd, fs=8.8)
for i in range(3):
    arrow(ax, (xs[i] + w, y0 + h/2), (xs[i+1], y0 + h/2), lw=1.3)
# reciprocal (Signal <-> Shift) and direct path (Signal -> Failure), dashed, below
arrow(ax, (xs[1] + 0.5, y0 - 0.03), (xs[2] + w - 0.5, y0 - 0.03), ls=(0, (3, 2)), lw=0.9, style='<|-|>', ms=9)
ax.text((xs[1] + xs[2] + w) / 2, y0 - 0.2, 'reciprocal', ha='center', va='top', fontsize=7.5, color=DARK)
arrow(ax, (xs[1] + w/2, y0 - 0.03), (xs[3] + w/2, y0 - 0.03), ls=(0, (3, 2)), lw=0.9, ms=9, conn='arc3,rad=0.3')
ax.text((xs[1] + xs[3] + w) / 2, 0.12, 'direct path (to be examined)', ha='center', va='center', fontsize=7.5, color=DARK, bbox=dict(fc='white', ec='none', pad=1.5))
# moderator
gx, gy, gw, gh = 3.1, 3.05, 4.6, 1.15
hbox(ax, gx, gy, gw, gh, 'Moderator', 'Gamification\nsupporting / stimulating elements × timing of input', fs=8.8)
t1x = (xs[1] + w + xs[2]) / 2; t2x = (xs[2] + w + xs[3]) / 2
arrow(ax, (gx + 0.7, gy), (t1x, y0 + h + 0.02), lw=1.2)
arrow(ax, (gx + gw - 0.7, gy), (t2x, y0 + h + 0.02), lw=1.2)
ax.text(gx - 0.15, gy + 0.1, 'Preventive input (T1)\nbefore signs of shift', ha='right', va='center', fontsize=8, color=DARK, linespacing=1.3)
ax.text(gx + gw + 0.15, gy + 0.1, 'Reactive input (T2)\nafter signs, before failure', ha='left', va='center', fontsize=8, color=DARK, linespacing=1.3)
fig.savefig('../figures/Fig1_conceptual_structure.png', bbox_inches='tight', pad_inches=0.12)

# ---------------- Fig. 2 ----------------
fig, ax = plt.subplots(figsize=(8.8, 4.9), dpi=300)
ax.set_xlim(0, 8.8); ax.set_ylim(0, 5.1); ax.axis('off')
cw, ch = 2.8, 1.35; x1, x2 = 2.55, 5.65; yT, yB = 2.55, 1.0; hh = 0.55
# column headers (grey bands)
for x, t in ((x1, 'Preventive input (T1)\nbefore signs of shift'), (x2, 'Reactive input (T2)\nafter signs, before failure')):
    ax.add_patch(Rectangle((x, yT + ch + 0.15), cw, hh, fc=GREY_H, ec=BLACK, lw=0.9))
    ax.text(x + cw/2, yT + ch + 0.15 + hh/2, t, ha='center', va='center', fontsize=8.2, color='white', linespacing=1.3)
# row headers
for y, t in ((yT, 'Supporting elements\nraise the value of\nthe task itself'), (yB, 'Stimulating elements\nintervene through\nstimuli outside the task')):
    ax.add_patch(Rectangle((0.15, y), 2.15, ch, fc='#e8e8e8', ec=BLACK, lw=0.9))
    ax.text(0.15 + 2.15/2, y + ch/2, t, ha='center', va='center', fontsize=8.2, color=DARK, linespacing=1.35)
cells = [(x1, yT, 'Study 1', 'Does early input delay\nthe shift?', '(H2a)'),
         (x2, yT, 'Study 2', 'Does input after the signs\nsustain goal behavior?', '(H2a)'),
         (x1, yB, 'Study 3', 'Does the benefit fade or\nreverse with exposure?', '(H2b)'),
         (x2, yB, 'Study 4', 'Do rewards still work\nafter the shift?', '(H2c)')]
for x, y, s, q, hyp in cells:
    ax.add_patch(Rectangle((x, y), cw, ch, fc='white', ec=BLACK, lw=0.9))
    ax.text(x + cw/2, y + ch - 0.28, s, ha='center', va='center', fontsize=9, fontweight='bold', color=DARK)
    ax.text(x + cw/2, y + ch/2 - 0.05, q, ha='center', va='center', fontsize=8.4, color=DARK, linespacing=1.35)
    ax.text(x + cw/2, y + 0.22, hyp, ha='center', va='center', fontsize=8.2, color=DARK)
ax.text(4.4, 0.42, 'Common basis: same task and measures · goal-intention check · matched controls · timing separated from exposure time',
        ha='center', va='center', fontsize=7.6, color=DARK, bbox=dict(boxstyle='square,pad=0.45', fc='white', ec=BLACK, lw=0.8))
fig.savefig('../figures/Fig2_research_program.png', bbox_inches='tight', pad_inches=0.12)

# ---------------- Fig. 3 ----------------
plt.rcParams.update({'axes.spines.top': False, 'axes.spines.right': False, 'axes.edgecolor': '#888', 'axes.linewidth': 0.8})
R = json.load(open('../results/sim_results.json')); S = json.load(open('../results/sens.json'))
CONDS = ['control', 'buffer_T1', 'buffer_T2', 'double_T1', 'double_T2']
LAB = {'control': 'Control', 'buffer_T1': 'Supporting·T1', 'buffer_T2': 'Supporting·T2', 'double_T1': 'Stimulating·T1', 'double_T2': 'Stimulating·T2'}
STY = {'control': dict(color='#6b6b6b', ls='-', lw=2.2),
       'buffer_T1': dict(color='#1f5fa8', ls='-', lw=2.0), 'buffer_T2': dict(color='#1f5fa8', ls='--', lw=2.0),
       'double_T1': dict(color='#c8641e', ls='-', lw=2.0), 'double_T2': dict(color='#c8641e', ls='--', lw=2.0)}
fig = plt.figure(figsize=(10.5, 7.6), dpi=300)
gs = fig.add_gridspec(2, 2, hspace=0.42, wspace=0.42)
def survival_panel(ax, model, title):
    for c in CONDS:
        d = R['res'][model][c]; ax.plot(d['ts'], np.array(d['surv'])*100, label=LAB[c], **STY[c])
    ax.axhline(50, color='#bbb', lw=0.8, ls=':')
    ax.set_xlim(0, 60); ax.set_ylim(0, 100); ax.set_xlabel('Time on task (min)'); ax.set_ylabel('Survival (%)')
    ax.set_title(title, loc='left', fontsize=10, fontweight='bold'); ax.grid(axis='y', color='#eee', lw=0.6)
    ys = sorted([(R['res'][model][c]['surv'][-1]*100, c) for c in CONDS]); placed = []
    for y, c in ys:
        yy = y if not placed else max(y, placed[-1] + 7); placed.append(yy)
        ax.annotate(LAB[c], (60, y), xytext=(62, yy), textcoords='data', fontsize=7.5, color=STY[c]['color'], va='center',
                    arrowprops=dict(arrowstyle='-', color='#bbb', lw=0.6) if abs(yy - y) > 1 else None, annotation_clip=False)
    ax.set_xlim(0, 60)
ax1 = fig.add_subplot(gs[0, 0]); survival_panel(ax1, 'base', '(a) Baseline variant: survival by condition')
ax2 = fig.add_subplot(gs[0, 1]); survival_panel(ax2, 'shift', '(b) Shift-response variant: survival by condition')
ax3 = fig.add_subplot(gs[1, 0])
cells = CONDS[1:]; x = np.arange(len(cells)); w = 0.36
m_o = [R['res']['base'][c]['median'] for c in cells]; m_p = [R['res']['shift'][c]['median'] for c in cells]
ctrl = R['res']['base']['control']['median']
b1 = ax3.bar(x - w/2, m_o, w, color='#9ab6d8', edgecolor='white', label='Baseline variant')
b2 = ax3.bar(x + w/2, m_p, w, color='#1f5fa8', edgecolor='white', label='Shift-response variant')
ax3.axhline(ctrl, color='#6b6b6b', lw=1.4); ax3.text(1.5, ctrl + 0.8, f'Control {ctrl:.1f} min', fontsize=7.5, color='#6b6b6b', ha='center', bbox=dict(fc='white', ec='none', pad=1))
for bars in (b1, b2):
    for b in bars: ax3.text(b.get_x() + b.get_width()/2, b.get_height() + 0.5, f'{b.get_height():.1f}', ha='center', fontsize=7.5, color='#333')
ax3.set_xticks(x); ax3.set_xticklabels([LAB[c] for c in cells], fontsize=8); ax3.set_ylabel('Median survival time (min)'); ax3.set_ylim(0, 46)
ax3.set_title('(c) Median survival time by condition', loc='left', fontsize=10, fontweight='bold')
ax3.legend(frameon=False, fontsize=8, loc='upper right'); ax3.grid(axis='y', color='#eee', lw=0.6)
ax3.annotate('largest gap between variants', (x[3], max(m_o[3], m_p[3]) + 4), ha='center', fontsize=8, fontweight='bold', color='#c8641e')
ax4 = fig.add_subplot(gs[1, 1])
g = np.array(S['double_T1']); lams = np.array(S['lams']); gams = np.array(S['gams']); vmax = np.abs(g).max()
im = ax4.imshow(g, origin='lower', aspect='auto', cmap='RdBu', vmin=-vmax, vmax=vmax, extent=[lams[0], lams[-1], gams[0], gams[-1]])
cs = ax4.contour(lams, gams, g, levels=[0], colors='black', linewidths=1.2); ax4.clabel(cs, fmt={0: 'zero effect'}, fontsize=7.5)
ax4.plot([0.06], [0.60], marker='o', color='black', ms=5); ax4.annotate('default', (0.06, 0.60), xytext=(5, 5), textcoords='offset points', fontsize=7.5)
ax4.set_xlabel('Reward habituation rate λ (1/min)'); ax4.set_ylabel('Expectation–reward gap sensitivity γ')
ax4.set_title('(d) Baseline variant, Stimulating·T1: difference in median\n     survival time vs. control (min)', loc='left', fontsize=10, fontweight='bold')
cb = fig.colorbar(im, ax=ax4, fraction=0.046, pad=0.03); cb.set_label('delay (+) / acceleration (−)', fontsize=8)
ax4.text(0.005, 0.95, 'delay', fontsize=8, color='#1f5fa8'); ax4.text(0.088, 0.05, 'acceleration', fontsize=8, color='#b03a2e')
fig.savefig('../figures/Fig3_simulation_2x2.png', bbox_inches='tight')
print('saved')
