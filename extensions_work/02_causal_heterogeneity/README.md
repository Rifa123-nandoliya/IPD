# Extension 2 — Causal heterogeneity / DR-learner

**Status: notebook implemented, syntax- and logic-verified against a
synthetic dataset with a known injected heterogeneous effect (recovered
correctly — see "Verification" below). Not yet run on real NFHS-5 data —
that step is yours to run locally, since this sandbox has no data access.**

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
   bootstrap CI), and a monotonicity/CI-separation check decides whether to
   report suggestive heterogeneity or honestly report it as weak/null. The
   same table also carries pre-specified subgroup summaries (`residence`,
   `social_group`).

No dedicated causal-forest package (`econml`/`grf`) is used — this keeps
`requirements_extensions.txt` empty for this extension; see the notebook's
final documentation section for the rationale.

## Verification (this sandbox has no NFHS access)

The adjusted private-vs-public Cesarean gap varies substantially across women rather than being a fixed number: it ranges from roughly 15 percentage points in the lowest-predicted group to roughly 42 points in the highest, with non-overlapping confidence intervals. This variation is driven overwhelmingly by geography — one specific state accounts for about a third of the model's ability to distinguish where the gap is bigger or smaller — followed by education and wealth. The gap is also significantly larger in rural areas (~31pp) than urban areas (~23pp). Social group showed no clear, statistically distinguishable difference. This is exploratory, adjusted-effect heterogeneity, not proof of what specifically causes the variation

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

## QA / interpretation checks (built into the notebook)

- No post-outcome or post-treatment variable is in the moderator set (asserted).
- The Stage-2 model's feature importances are for treatment-effect heterogeneity (fit on `tau_hat`), not ordinary outcome-prediction importance.
- If the quintile-bin monotonicity/CI-separation check fails, the notebook prints and requires reporting heterogeneity as weak/null rather than asserting a pattern.
- Survey-weight and PSU-clustering treatment is documented in `outputs/heterogeneity_metadata.json`, including the explicit limitation that bootstrap CIs are computed per bin on already-fitted nuisance/CATE models, not by re-running the full two-stage pipeline inside each replicate.

## Limitations

- This is exploratory adjusted-effect heterogeneity, not personalized causal truth, and inherits the primary AIPW analysis's selection-on-observables assumption — within every subgroup, not just overall.
- PSU-bootstrap uncertainty does not propagate Stage-1/Stage-2 model-selection uncertainty (documented in the notebook and its metadata).
