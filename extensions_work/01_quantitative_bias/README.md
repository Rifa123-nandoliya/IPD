# Extension 1 — Quantitative Bias Analysis (QBA)

**Status: complete. Fully executed for real (not synthetic) in this
environment, since it only depends on already-frozen, already-committed
files (`outputs/final_tables/final_aipw_overall_table.csv`) — no raw NFHS
data needed.**

## Research question

How robust is the 28.47 pp adjusted private-vs-public Cesarean risk
difference to plausible unmeasured clinical confounding — especially prior
Cesarean history and unmeasured obstetric-severity indications?

## Method

Uses the same bias-factor formula that underlies this project's own
E-value (VanderWeele & Ding, 2017): for an unmeasured confounder with a
given sector prevalence gap and a given confounder→outcome risk ratio,
there's a closed-form maximum bias factor on the observed risk ratio. This
notebook evaluates that formula across a **grid** of scenarios (not just
one worst-case number) for two confounder classes:

1. **`prior_cesarean_history`** — genuinely unmeasured in NFHS-5 beyond a
   limited recall window (documented in `notebooks/v2/01`).
2. **`obstetric_severity_unmeasured`** — a placeholder class for clinical
   severity/indications beyond NFHS-5's coarse `s434`/`s435` items.

It reports: a deterministic scenario grid, a Monte Carlo distribution over
plausible parameter ranges, representative mild/moderate/strong scenarios,
the exact "tipping point" (how extreme a confounder would need to be to
erase the finding entirely), and a cross-check against the project's
existing E-value.

**⚠️ Critical caveat, repeated from the notebook: the specific numeric
ranges used for confounder prevalence and strength are illustrative
placeholders — no literature search was performed to source them.** See
"What still needs to happen" below.

## Results (real, from the actual frozen primary estimate)

**Locked reference:** RD = 28.4698 pp, RR = 2.7260 (95% CI 2.6566–2.8035), n = 200,794.

### 1. E-value cross-check — confirms the method is implemented correctly

Recomputed E-value from this notebook's own formula: **4.8951** for the
point estimate, **4.7544** for the CI bound closest to the null. The
handoff document independently reports **4.90** for this project's
E-value — matching almost exactly, confirming this notebook's bias-factor
implementation is mathematically consistent with the project's existing
E-value calculation.

### 2. The finding is robust across a wide range of plausible-looking scenarios

| Confounder | Scenario | Prevalence gap | Effect (RR) | Adjusted RD |
|---|---|---:|---:|---:|
| Prior Cesarean history | Mild | +5 pp | 2.0× | 26.55 pp |
| Prior Cesarean history | Moderate | +12 pp | 4.0× | 19.06 pp |
| Prior Cesarean history | Strong | +20 pp | 6.0× | 11.18 pp |
| Obstetric severity (unmeasured) | Mild | +3 pp | 1.5× | 27.83 pp |
| Obstetric severity (unmeasured) | Moderate | +8 pp | 2.5× | 24.12 pp |
| Obstetric severity (unmeasured) | Strong | +15 pp | 3.5× | 17.76 pp |

Even the "strong" scenarios — a confounder that's 20 percentage points more
common in private facilities *and* multiplies C-section risk 6-fold — only
attenuates the gap from 28.47 pp down to about 11-18 pp. It doesn't come
close to erasing it.

### 3. What it would actually take to erase the finding (tipping point)

- **Prior Cesarean history:** even at the *most extreme* prevalence gap
  tested (+30 pp — i.e., private-sector patients being 30 percentage points
  more likely to have a prior C-section), the confounder would need to
  multiply C-section risk by **~19.6×** to bring the adjusted gap to zero.
- **Obstetric severity:** at its most extreme tested prevalence gap
  (+20 pp), it would need to multiply risk by **~28.9×**.

Both are far outside any biologically plausible single-confounder risk
ratio for this outcome — real prior-Cesarean effects on repeat-Cesarean
risk, while strong, are not remotely 20-30× effects.

### 4. Monte Carlo summary (20,000 draws per confounder, over the placeholder ranges)

| Confounder | Median adjusted RD | 95% range | % draws RD > 0 | % draws RD > 10pp |
|---|---:|---|---:|---:|
| Prior Cesarean history | 18.56 pp | [6.30, 28.17] | 100% | 86.8% |
| Obstetric severity (unmeasured) | 23.36 pp | [13.50, 28.35] | 100% | 100% |

Across every one of the 20,000 random draws per confounder (spanning the
full stated placeholder ranges), the adjusted risk difference **never**
crossed zero.

### Headline conclusion

Under the parameter ranges tested here — which are wide enough to include
what would already be considered fairly extreme, clinically implausible
unmeasured confounders — the 28.47 pp private-vs-public adjusted gap does
not get explained away. It takes a confounder several times stronger than
anything in the tested range (prevalence gap and risk ratio both) to bring
the estimate to zero. This is consistent with, and quantitatively extends,
the project's own E-value finding (4.90).

## ⚠️ What still needs to happen before this is publication-ready

The prevalence and effect-size ranges above (`p0_baseline`, `delta_p_grid`,
`rr_ud_grid` in the notebook's Section 2) are **illustrative placeholders**,
not sourced from any literature search. Before reporting these results as
final:

1. Find published, ideally India-specific, estimates of:
   - prior-Cesarean prevalence among institutional deliveries (and, if
     available, split by facility sector)
   - the risk ratio of repeat Cesarean given a prior Cesarean
   - analogous figures for the "obstetric severity" class, or narrow that
     class to specific named conditions with known prevalence/effect data
2. Update `CONFOUNDER_SPECS` in the notebook's Section 2 and the `source`
   column of `assumptions_sources.csv` — no other code changes are needed.
3. Re-run the notebook; the grid, Monte Carlo, and tipping-point numbers
   will update automatically.

## Inputs

- `outputs/final_tables/final_aipw_overall_table.csv` (frozen primary estimate — the only required input)
- `notebooks/v2/01_v2_data_audit_and_cohort.ipynb` (documents why prior-Cesarean is unmeasured)
- `notebooks/v2/07_aipw_primary_analysis.ipynb`, `notebooks/v2/09_sensitivity_analyses.ipynb` (methodological context, E-value)

## Files produced

- `notebook.ipynb`
- `outputs/qba_scenario_results.csv` — full deterministic grid (550 rows: 2 confounders × their prevalence-gap × risk-ratio grids)
- `outputs/qba_summary.csv` — representative scenarios, tipping points, and Monte Carlo summary stats
- `outputs/qba_heatmap.png` — bias-adjusted RD across the grid, per confounder, with the RD=0 tipping-point contour and representative-scenario markers
- `outputs/assumptions_sources.csv` — every bias parameter with its assumed range, rationale, and a `source` column (currently `TODO: cite...`)

## QA / interpretation checks

- **Reproduces the primary estimate exactly at no unmeasured confounding** (`delta_p=0` or `rr_ud=1`) — asserted in the notebook, passed.
- **E-value cross-check passed** (4.8951 recomputed vs. 4.90 reported) — confirms correct implementation.
- Results are reported as scenario-dependent ("under these assumptions..."), never as proof unmeasured confounding is absent.
- The placeholder nature of the parameter ranges is flagged in the notebook, this README, and `assumptions_sources.csv` — not silently presented as sourced.

## Limitations

- Assumes the confounder's effect on the outcome is constant across sectors (standard simplifying assumption for this class of bias-factor sensitivity analysis; not separately tested).
- The two confounder classes are treated independently — a combined "both confounders operating simultaneously" scenario is not modeled (would require a joint bias formula and additional assumptions about their correlation).
- As stated above, the specific numeric ranges are placeholders pending a real literature search.
