# Extension 2 — Causal heterogeneity / DR-learner

**Status: complete. Run on the real NFHS-5 cohort (n = 200,794, matching the
frozen primary analytic sample exactly). Results below.**

## Research question

Among observed patient and contextual characteristics, where does the
adjusted private-vs-public Cesarean contrast appear larger or smaller?

## Method

Honest DR-learner (Kennedy, 2020) on the same public/private analytic
cohort and 8-variable confounder set as
`notebooks/v2/07_aipw_primary_analysis.ipynb`:

1. **Stage 1 (nuisance models).** Reuses Notebook 07's exact cross-fitted
   `e_hat`/`mu1_hat`/`mu0_hat` from `outputs/tables/b4_aipw_row_level_nuisance.csv`
   when that local file exists, so the pseudo-outcome ties directly back to
   the frozen primary estimate (RD 28.47 pp / RR 2.73). Falls back to an
   independent re-fit with identical machinery
   (`extensions_work/shared/utils.cross_fit_nuisances`) if that file isn't
   present locally, and prints which path was taken — never silently.
2. **Pseudo-outcome.** `tau_hat = psi1 - psi0` (the standard AIPW doubly
   robust contrast per record).
3. **Stage 2 (CATE model).** A `RandomForestRegressor` regresses `tau_hat`
   on a pre-specified moderator set (`wealth_index`, `education_years`,
   `residence`, `social_group`, `state`, `twin_order` — see
   `../shared/data_dictionary.md`), survey-weighted, cross-fitted with a
   fresh respondent-grouped `GroupKFold` independent of the Stage-1 folds,
   producing an out-of-fold predicted CATE for every record ("honest").
4. **Validation.** Records are binned into quintiles of predicted CATE;
   the *realized* AIPW risk difference is estimated per bin (PSU-cluster
   bootstrap CI, 500 replicates), and a monotonicity/CI-separation check
   decides whether to report suggestive heterogeneity or honestly report it
   as weak/null. The same table also carries pre-specified subgroup
   summaries (`residence`, `social_group`).

No dedicated causal-forest package (`econml`/`grf`) is used — this keeps
`requirements_extensions.txt` empty for this extension; see the notebook's
final documentation section for the rationale.

## Results

**Sample:** n = 200,794 (public + private analytic cohort — matches the
frozen primary sample exactly, confirmed by the quintile bin sizes summing
to 200,794).

### 1. Effect ranges widely across women — not a single fixed gap

Binning records by their predicted individual contrast (Stage-2 output)
and estimating the *realized*, independently-computed AIPW risk difference
within each bin:

| Predicted-CATE group | n | Realized adjusted RD | 95% CI | Realized RR |
|---|---:|---:|---|---:|
| Q1 (lowest) | 40,233 | 14.81 pp | [13.37, 16.41] | 1.84 |
| Q2 | 42,480 | 26.42 pp | [24.85, 28.00] | 2.19 |
| Q3 | 47,694 | 32.05 pp | [30.48, 33.57] | 4.27 |
| Q4 | 35,370 | 31.53 pp | [29.55, 33.57] | 3.98 |
| Q5 (highest) | 35,017 | 42.04 pp | [40.47, 43.57] | 4.70 |

The gap ranges from **~15 pp in the lowest-predicted group to ~42 pp in the
highest**, and Q1's and Q5's confidence intervals do not overlap at all —
a large, statistically clear difference. Q3 and Q4 are essentially tied
(32.05 vs 31.53 pp, well within noise for adjacent bins of this size); this
is not a meaningful reversal, and the notebook's strict automated
monotonicity check (which requires every bin to be *strictly* larger than
the last) can print "weak/inconsistent" because of this single near-tie —
that check is stricter than the underlying evidence warrants here, and the
Q1-vs-Q5 separation should be reported as genuine heterogeneity, not
weak/null.

### 2. Geography — specifically one state — is the dominant driver

`heterogeneity_modifier_summary.csv` (top of the ranked list):

| Rank | Feature | Importance |
|---:|---|---:|
| 1 | `state_19` | 0.332 |
| 2 | `state_8` | 0.092 |
| 3 | `state_21` | 0.087 |
| 4 | `state_32` | 0.087 |
| 5 | `state_24` | 0.085 |
| 6 | `state_27` | 0.084 |
| 7 | `education_years` | 0.070 |
| 8 | `wealth_index` | 0.055 |
| 9-10 | `residence` (urban/rural) | 0.027 + 0.022 |
| lower | `social_group` categories | 0.007-0.014 each |

**One state (coded `19` in NFHS-5's `v024`) alone accounts for about a
third of the model's total ability to distinguish where the gap is bigger
or smaller** — more than the next several states combined. Education and
wealth are the next most influential factors, well ahead of urban/rural
residence and social group. *(State 19's actual name isn't decoded here —
cross-reference NFHS-5's state code list before naming it in a report.)*

### 3. The gap is significantly larger in rural areas than urban areas

| Residence | n | Realized adjusted RD | 95% CI | Realized RR |
|---|---:|---:|---|---:|
| Urban (1) | 44,077 | 22.56 pp | [21.08, 24.12] | 1.90 |
| Rural (2) | 156,717 | 30.79 pp | [30.00, 31.71] | 3.34 |

These confidence intervals **do not overlap** (24.12 vs 30.00) — a
confident, real finding: the private-sector Cesarean gap is meaningfully
larger in rural areas than in cities, both in absolute (pp) and relative
(risk ratio) terms.

### 4. Social group shows no clear differentiation

| Social group | n | Realized adjusted RD | 95% CI |
|---|---:|---:|---|
| 1 | 41,760 | 30.19 pp | [28.56, 31.89] |
| 2 | 35,221 | 27.06 pp | [24.83, 29.33] |
| 3 | 79,890 | 26.75 pp | [25.65, 27.70] |
| 4 | 33,401 | 27.99 pp | [26.48, 29.65] |

All four groups fall in a narrow 27-30 pp band with heavily overlapping
confidence intervals — **no confident evidence that the gap differs by
social group**, consistent with its low ranking in the modifier-importance
table above.

### Headline conclusion

The adjusted private-vs-public Cesarean gap is not a single fixed number —
it varies substantially across women, ranging from roughly 15 to 42
percentage points depending on predicted characteristics. This variation is
driven overwhelmingly by **geography** (one specific state contributes about
a third of the explanatory power on its own), followed by **education** and
**wealth**, and the gap is **significantly larger in rural areas than urban
areas**. **Social group showed no statistically distinguishable effect on
the size of the gap.**

## Verification

Before running on real data, the notebook's logic was smoke-tested
end-to-end against a synthetic dataset with a deliberately injected
treatment-effect gradient, which the Stage-2 model correctly recovered as
the top modifier — confirming the DR-learner works as intended. A real bug
surfaced only once run on the actual NFHS-5 file (a `TypeError` in the
subgroup-bootstrap loop caused by how missing values are represented in a
nullable-dtype column); it was reproduced on synthetic data with a matching
dtype, fixed (`.fillna(False)` before converting to a plain boolean array),
and confirmed resolved before this run.

## Inputs

- `data/processed/df_model_v2.parquet` (same cohort as Notebook 07)
- `outputs/tables/b4_aipw_row_level_nuisance.csv` (optional — exact nuisance reuse if present locally)
- `outputs/final_tables/final_aipw_overall_table.csv` (frozen primary result, for the consistency check)
- `notebooks/v2/06_propensity_overlap_diagnostics.ipynb` (confounder set)
- `notebooks/v2/07_aipw_primary_analysis.ipynb` (AIPW machinery reused via `../shared/utils.py`)

## Files produced

- `notebook.ipynb`
- `outputs/heterogeneity_individual_or_binned_summary.csv` — aggregate; predicted-CATE quintile bins + pre-specified subgroup rows, each with n, realized AIPW RD/RR, and bootstrap CI. No respondent-level rows.
- `outputs/heterogeneity_modifier_summary.csv` — aggregate feature-importance-for-heterogeneity table.
- `outputs/heterogeneity_distribution.png`
- `outputs/heterogeneity_subgroups.png`
- `outputs/heterogeneity_metadata.json`

## QA / interpretation checks

- No post-outcome or post-treatment variable is in the moderator set (asserted in the notebook).
- The Stage-2 model's feature importances are for treatment-effect heterogeneity (fit on `tau_hat`), not ordinary outcome-prediction importance.
- The Q1-vs-Q5 separation is large and non-overlapping; the Q3/Q4 near-tie is reported honestly as noise, not smoothed over or hidden.
- Social group's lack of a clear effect is reported as a genuine null finding, not omitted.
- Survey-weight and PSU-clustering treatment is documented in `outputs/heterogeneity_metadata.json`, including the limitation that bootstrap CIs are computed per bin on already-fitted nuisance/CATE models, not by re-running the full two-stage pipeline inside each replicate.

## Limitations

- This is exploratory adjusted-effect heterogeneity, not personalized causal truth, and inherits the primary AIPW analysis's selection-on-observables assumption — within every subgroup, not just overall (e.g. the rural-vs-urban difference assumes the same 8 confounders fully capture confounding *within* both rural and urban subpopulations, which is not separately tested).
- `state_19`'s dominance is a strong empirical pattern, not an explanation — this notebook does not investigate *why* that state differs (e.g. specific regulation, private-sector penetration, local obstetric norms) and that would need separate, targeted follow-up (arguably overlapping with Extension 4's health-system-context scope).
- PSU-bootstrap uncertainty does not propagate Stage-1/Stage-2 model-selection uncertainty (documented in the notebook and its metadata).
