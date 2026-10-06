# -*- coding: utf-8 -*-
"""
자기조절 실패 × 게이미피케이션 계산 모형 시뮬레이션 (v1.0, 2026-10)
기회비용 모델(Kurzban 2013; Agrawal 2022) + 문턱(Dang 2025) + 과정 모델의 주의 전환(Inzlicht & Schmeichel 2012)
을 최소 파라미터로 구현하고, 요소 유형(지지/자극) × 투입 시점(T1 예방/T2 반응적) 2×2 조건의 이탈 곡선을 생성한다.
"""
import numpy as np, json, sys
rng = np.random.default_rng(20260907)

# ---------- 기본 파라미터 (분 단위) ----------
P = dict(
    T=60, dt=0.5, N=4000,
    V0=1.00,      # 과제의 기본 가치
    A0=0.35,      # 대안 활동의 기본 가치
    drift=0.006,  # 대안 가치의 시간 증가율 (지루함 신호, Agrawal 2022)
    kappa=0.020,  # 기회비용(피로) 누적 기울기 (분당)
    theta=0.0,    # 이탈 문턱: 순가치 U < theta 이면 이탈 위험 급증
    tau=0.08,     # 위험 함수의 온도 (문턱의 날카로움)
    h0=0.004,     # 기저 위험 (분당)
    # 지지 요소
    b_val=0.25,   # 과제 내부 가치 상승 (진행 표시·즉시 피드백·의미 서사)
    b_cost=0.25,  # 피로 누적 기울기 감소 비율 (노력-결과 간격 축소)
    # 자극 요소
    r0=0.45,      # 외적 보상의 초기 가치 (포인트·배지·경쟁·스트릭)
    lam=0.06,     # 보상 습관화(가치 감가) 속도 (분당)
    gam=0.60,     # 기대-보상 격차에 대한 민감도 (보상이 기대 아래로 떨어질 때의 벌점)
    alt_up=0.10,  # 대안 활동 가치 환기 (알림·경쟁의 부작용)
    # 반응적 투입(T2) 트리거: 누적 기회비용이 문턱의 일정 비율에 도달했을 때
    t2_frac=0.60,
    # 개인차 (로그정규 분산)
    het=0.25,
    # 전환 반응 변형(shift): 전환이 시작된(누적비용≥트리거) 학습자에게 외적 보상의 효력이 감소하고 격차 벌점이 증폭
    model='base',  # 'base'(기본 변형) | 'shift'(전환 반응 변형)
    rho=0.30,   # 전환 후 외적 보상 효력 배율 (주의가 이미 보상 단서로 이동)
    gap_amp=2.0, # 전환 후 격차 벌점 증폭
)

def simulate(cond, P, seed=None):
    """cond in {'control','buffer_T1','buffer_T2','double_T1','double_T2'} -> survival array over time"""
    r = np.random.default_rng(seed)
    N, T, dt = P['N'], P['T'], P['dt']
    steps = int(T/dt)+1
    ts = np.arange(steps)*dt
    # 개인차
    V0 = P['V0']*np.exp(r.normal(0,P['het'],N))
    A0 = P['A0']*np.exp(r.normal(0,P['het'],N))
    kap = P['kappa']*np.exp(r.normal(0,P['het'],N))
    alive = np.ones(N, bool)
    cost = np.zeros(N)
    t_in = np.full(N, np.inf)           # 요소 투입 시점
    if cond.endswith('_T1'): t_in[:] = 0.0
    # 개인별 T2 트리거 기준: 통제 조건의 전형적 이탈 시 누적비용 근사 (V0-A0)의 t2_frac
    c_trig = P['t2_frac']*np.maximum(V0-A0, 0.05)
    surv = np.zeros(steps)
    kind = 'buffer' if cond.startswith('buffer') else ('double' if cond.startswith('double') else None)
    for i, t in enumerate(ts):
        surv[i] = alive.mean()
        if not alive.any(): surv[i:] = 0; break
        # T2 트리거
        if cond.endswith('_T2'):
            trig = alive & np.isinf(t_in) & (cost >= c_trig)
            t_in[trig] = t
        active = alive & (t >= t_in)
        el = np.where(active, t - t_in, 0.0)     # 요소 노출 경과 시간
        # 가치 항
        V_task = V0.copy()
        V_alt  = A0 + P['drift']*t
        k_eff  = kap.copy()
        if kind == 'buffer':
            V_task = np.where(active, V_task*(1+P['b_val']), V_task)
            k_eff  = np.where(active, k_eff*(1-P['b_cost']), k_eff)
        elif kind == 'double':
            R = P['r0']*np.exp(-P['lam']*el)                  # 습관화된 보상 가치
            gap = P['r0'] - R                                 # 기대 대비 격차
            if P['model'] == 'shift':
                shifted = cost >= c_trig                       # 동기·주의 전환이 시작된 상태
                R = np.where(shifted, R*P['rho'], R)
                gap = np.where(shifted, gap*P['gap_amp'], gap)
            V_task = np.where(active, V_task + R - P['gam']*gap, V_task)
            V_alt  = np.where(active, V_alt + P['alt_up'], V_alt)
        # 기회비용 누적
        cost = cost + k_eff*dt
        U = V_task - cost - V_alt
        # 위험 함수: 문턱 아래로 내려갈수록 급증 (자기조절 문턱)
        haz = P['h0'] + (1/(1+np.exp((U-P['theta'])/P['tau'])))*0.25
        drop = alive & (r.random(N) < 1-np.exp(-haz*dt))
        alive &= ~drop
    return ts, surv

def median_time(ts, surv):
    idx = np.where(surv <= 0.5)[0]
    return float(ts[idx[0]]) if len(idx) else float('inf')

CONDS = ['control','buffer_T1','buffer_T2','double_T1','double_T2']
LABEL = {'control':'통제','buffer_T1':'지지·T1','buffer_T2':'지지·T2','double_T1':'자극·T1','double_T2':'자극·T2'}

if __name__ == '__main__':
    SEED = {'control':101,'buffer_T1':102,'buffer_T2':103,'double_T1':104,'double_T2':105}
    res = {}
    for model in ['base','shift']:
        res[model] = {}
        for c in CONDS:
            ts, s = simulate(c, dict(P, model=model), seed=SEED[c])
            res[model][c] = dict(ts=ts.tolist(), surv=s.tolist(), median=median_time(ts,s), s30=float(s[int(30/P['dt'])]), s60=float(s[-1]))
    json.dump(dict(P=P, res=res), open('../results/sim_results.json','w'), ensure_ascii=False)
    for model in res:
        print(f"[{model}] 조건별 중앙 생존시간(분) / 30분 잔존율 / 60분 잔존율")
        for c in CONDS: print(f"  {LABEL[c]:12s} {res[model][c]['median']:6.1f}  {res[model][c]['s30']:.3f}  {res[model][c]['s60']:.3f}")
