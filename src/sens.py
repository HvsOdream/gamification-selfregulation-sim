import numpy as np, json
from gamif_selfreg_sim import simulate, median_time, P
lams = np.linspace(0.0, 0.12, 13); gams = np.linspace(0.0, 1.0, 11)
N = 4000                                   # 기본 실행과 동일
ts, s = simulate('control', dict(P, N=N), seed=101); ctrl = median_time(ts, s)
out = {}
for cond in ['double_T1','double_T2']:
    g = np.zeros((len(gams), len(lams)))
    for gi,ga in enumerate(gams):
        for li,l in enumerate(lams):
            ts, s = simulate(cond, dict(P, lam=l, gam=ga, N=N), seed=70000+gi*100+li)
            g[gi,li] = median_time(ts,s) - ctrl
    out[cond] = g.tolist()
json.dump(dict(lams=lams.tolist(), gams=gams.tolist(), ctrl=ctrl, N=N, **out), open('../results/sens.json','w'))
g = np.array(out['double_T1'])
print(f"통제 중앙 생존시간 {ctrl}분 (기본 실행과 동일 N={N})\n")
print("λ(1/분)  γ에 따른 통제 대비 차이(분)   부호")
for li,l in enumerate(lams):
    col = g[:,li]; sign = "모두 +" if col.min()>0 else ("모두 −" if col.max()<0 else "혼재")
    print(f"  {l:.2f}   {col.min():+5.1f} ~ {col.max():+5.1f}        {sign}")
