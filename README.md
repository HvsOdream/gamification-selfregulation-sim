# gamification-selfregulation-sim

Computational example accompanying the manuscript

> Kim, M. (under review). *When Does Self-Regulation Failure Occur in Gamification?: An Integrative Research Model of Intervention Timing*. Journal of Korea Game Society.
> 김민철. 게이미피케이션에서 자기조절 실패는 언제 발생하는가: 개입 시점에 관한 통합 연구모형 제안. 한국게임학회 논문지 (심사 중).

The model is a Monte Carlo illustration of hypotheses in the paper (Section 4.5, Appendix A). It is **not** an empirical estimate: all parameters are author-specified example values, and the motivational–attentional shift is proxied by a cost trigger, not implemented as a state variable. Dropout is the only failure event generated.

## What is here

| path | content |
|---|---|
| `src/gamif_selfreg_sim.py` | model and baseline run (5 conditions × 2 variants, seeds 101–105) → `results/sim_results.json` |
| `src/sens.py` | λ × γ sensitivity grid for stimulating elements (13 × 11, fixed seed per cell) → `results/sens.json` |
| `src/sens_support.py` | b_val × b_cost grid for supporting elements (6 × 6) and paired 20-seed replication of the γ = 0 condition → `results/sens_support.json` |
| `src/rep20.py` | 20-seed replication (seeds 1000–1019) of the five baseline conditions, both variants → `results/rep20.json` |
| `src/make_figures.py` | Fig. 1–3 of the paper → `figures/` |
| `results/` | all result files reported in the paper |
| `figures/` | Fig1_conceptual_structure.png, Fig2_research_program.png, Fig3_simulation_2x2.png |

## Model summary (see Appendix A for the full specification)

For learner *i* at time *t* (Δt = 0.5 min, T = 60 min, N = 4,000 per condition):

- net value `U = V − C − A` (task value, accumulated cost `C += κΔt`, alternative value `A = A0 + drift·t`)
- hazard `h = h0 + 0.25 / (1 + exp((U − θ)/τ))`; dropout probability per step `p = 1 − exp(−hΔt)`
- individual differences: lognormal multiplicative noise (log-SD 0.25) on V0, A0, κ
- **supporting elements**: `V0 × (1 + b_val)`, `κ × (1 − b_cost)`
- **stimulating elements**: reward `R(e) = r0·exp(−λe)` added, gap penalty `γ·(r0 − R(e))` subtracted, `A += alt_up`, where *e* is exposure time; net contribution `ΔU(e) = (1+γ)r0·exp(−λe) − γr0 − alt_up`
- **T1** activates at t = 0; **T2** activates when accumulated cost reaches `t2_frac × (V0 − A0)` (proxy for shift signs)
- variants: `base` (no state dependence) and `shift` (after the trigger, reward efficacy × ρ and gap penalty × gap_amp)

Update order per step: record survival → trigger check → value calculation → cost update → dropout draw. Median survival time is the first grid time at which survival ≤ 0.5.

Defaults: κ = 0.020/min, V0 = 1.00, A0 = 0.35, drift = 0.006/min, θ = 0, τ = 0.08, h0 = 0.004/min, b_val = b_cost = 0.25, r0 = 0.45, λ = 0.06/min, γ = 0.60, alt_up = 0.10, t2_frac = 0.60, ρ = 0.30, gap_amp = 2.0.

Note: `θ` is the midpoint of the logistic hazard term (h(θ) = h0 + 0.125), not the point where risk starts to rise.

## Reproduce

```bash
pip install -r requirements.txt
cd src
python gamif_selfreg_sim.py     # ~1 min
python sens.py                  # ~15 min
python sens_support.py          # ~3 min
python rep20.py                 # ~5 min
python make_figures.py
```

All runs use fixed seeds; the numbers in the paper (medians at 0.5-min resolution, 30-min survival) should reproduce exactly on NumPy ≥ 1.17 (`default_rng`).

Expected baseline medians (min), variant `base` / `shift`:
control 24.5 / 24.5 · supporting·T1 38.5 / 38.5 · supporting·T2 32.5 / 32.5 · stimulating·T1 21.5 / 20.5 · stimulating·T2 28.0 / 24.0.

## Disclosure

Simulation code was written and run, and results were tabulated, with the assistance of a generative AI tool (Claude Fable 5.1, Anthropic). Model assumptions and parameters were set by the author; reported values were checked for reproducibility with fixed seeds.

## License

MIT (code). Result files and figures may be reused with attribution to the paper.
