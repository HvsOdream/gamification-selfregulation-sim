import json, numpy as np
from gamif_selfreg_sim import simulate, median_time, P
vals=[0.0,0.10,0.20,0.25,0.30,0.40]
out={'grid':[], 'rep_gamma0':{}}
for bv in vals:
    for bc in vals:
        row={'b_val':bv,'b_cost':bc}
        for c,seed in [('buffer_T1',102),('buffer_T2',103)]:
            ts,s=simulate(c, dict(P,b_val=bv,b_cost=bc), seed=seed)
            row[c]=median_time(ts,s); row[c+'_s30']=float(s[int(30/P['dt'])])
        out['grid'].append(row)
ts,s=simulate('control',P,seed=101); out['control']=median_time(ts,s)
# gamma=0 repeat 20 seeds vs control 20 seeds (same seeds)
g0=[];ct=[]
for sd in range(1000,1020):
    ts,s=simulate('double_T1', dict(P,gam=0.0), seed=sd); g0.append(median_time(ts,s))
    ts,s=simulate('control', P, seed=sd); ct.append(median_time(ts,s))
out['rep_gamma0']={'double_T1_gamma0':g0,'control':ct,'diff':[a-b for a,b in zip(g0,ct)]}
json.dump(out,open('../results/sens_support.json','w'),ensure_ascii=False,indent=1)
print('control',out['control'])
print('b_val\\b_cost', vals)
for bv in vals:
    print(bv, [next(r for r in out['grid'] if r['b_val']==bv and r['b_cost']==bc)['buffer_T1'] for bc in vals],
              [next(r for r in out['grid'] if r['b_val']==bv and r['b_cost']==bc)['buffer_T2'] for bc in vals])
d=out['rep_gamma0']['diff']; print('gamma0 diff T1-control: min',min(d),'max',max(d),'mean',round(sum(d)/20,2), 'n>0',sum(x>0 for x in d))
print('gamma0 T1 range',min(g0),max(g0),'control range',min(ct),max(ct))
