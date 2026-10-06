# 20-seed replication of the five baseline conditions (seeds 1000-1019), both variants.
import json
from gamif_selfreg_sim import simulate, median_time, P, CONDS
out = {'base': {}, 'shift': {}, 'seeds': list(range(1000, 1020))}
for model in ['base', 'shift']:
    for c in CONDS:
        out[model][c] = [median_time(*simulate(c, dict(P, model=model), seed=sd)) for sd in out['seeds']]
json.dump(out, open('../results/rep20.json', 'w'))
for model in out:
    if model == 'seeds': continue
    print(model, {c: (min(v), max(v)) for c, v in out[model].items()})
