# Extension 5 — Strong First-Birth AIPW Analysis

**Status: notebook implemented, syntax- and logic-verified against a
synthetic dataset with the required `age_at_first_birth` field. Not yet run
on real NFHS-5 data — that step is yours to run locally, since this
sandbox has no data access.**

## Research question

Does the adjusted public-private Cesarean gap remain among first births,
where prior Cesarean history is impossible by construction?

## Method

A dedicated first-birth-only AIPW model — not a post-hoc stratification of
the primary model:

1. **Cohort.** `birth_order == 1` (never `birth_index`). Records missing
   `age_at_first_birth` are excluded and counted, not backfilled with
   `maternal_age`.
2. **Confounder set.** The same 8-variable set as Notebooks 06/07, with
   `birth_order` dropped (constant in this cohort) and `age_at_first_birth`
   added in its place — exact age-at-birth by construction for this
   subgroup, unlike `maternal_age` (age-at-interview) project-wide.
3. **Diagnostics.** Overlap and covariate-balance (SMD before/after
   weighting) re-run within the first-birth cohort specifically.
4. **AIPW.** Respondent-grouped cross-fitted AIPW, identical architecture
   to Notebook 07, fit independently on this cohort (via
   `shared/utils.run_cross_fitted_aipw`) — not reusing Notebook 07's
   nuisance predictions, since those were fit with a live `birth_order`
   term that doesn't apply here.
5. **Comparison to the primary estimate.** Reported as side-by-side point
   estimates and CIs, deliberately **not** a formal joint difference test —
   see the notebook's Section 7 for why (first births are a *subset* of,
   not independent from, the full cohort, so naively pairing bootstrap
   replicates the way Extension 3 does for NFHS-4/NFHS-5 would be invalid
   here).

## Verification (this sandbox has no NFHS access)

Smoke-tested end-to-end against a synthetic dataset extended with a
realistic `age_at_first_birth` field (non-null only for `birth_order == 1`
records, with a small documented missingness rate). The full pipeline —
cohort construction, confounder-set assertions, balance diagnostics,
cross-fitted AIPW, and the comparison plot — ran without errors. No
synthetic data or its outputs are included in this folder or committed
anywhere.

**Final estimates, real QA results, and interpretation will be added to
this README once run on the actual NFHS-5 cohort.**

## Inputs

- `data/processed/df_model_v2.parquet` (same file as Notebooks 06/07)
- `outputs/final_tables/final_aipw_overall_table.csv` (frozen primary result, for the comparison step)
- `notebooks/v2/01_v2_data_audit_and_cohort.ipynb` (first-birth definition, `age_at_first_birth` documentation)
- `notebooks/v2/06_propensity_overlap_diagnostics.ipynb`, `notebooks/v2/08_risk_stratified_aipw.ipynb` (methodological precedent)

## Files produced

- `notebook.ipynb`
- `outputs/first_birth_cohort_summary.csv`
- `outputs/first_birth_overlap_balance.csv`
- `outputs/first_birth_aipw_summary.csv`
- `outputs/first_birth_bootstrap_summary.csv` — 500 PSU-cluster bootstrap replicates (safe aggregate, same schema as the frozen `b4_aipw_bootstrap_results.csv`)
- `outputs/first_birth_comparison_plot.png`
- `outputs/first_birth_metadata.json`

## QA / interpretation checks (built into the notebook)

- First-birth definition verified as `birth_order == 1`, explicitly not `birth_index`.
- `birth_order`'s constancy within the cohort is asserted before it's excluded as a predictor.
- Explicitly states: prior-Cesarean confounding is removed *by construction*, but other first-birth-specific unmeasured obstetric indications (fetal compromise, labor dystocia) are not.
- Explicitly does not claim novelty as "the first" such analysis in India.
- The comparison to the full-cohort primary is a side-by-side report, with the invalid-independence pitfall of a naive joint bootstrap explicitly documented rather than silently attempted.

## Limitations

- Nuisance models are refit from scratch on the first-birth subset (smaller n, likely wider CIs than the full-cohort primary) rather than borrowing strength from the full model.
- No formal statistical test for whether the first-birth estimate differs from the full-cohort primary — only a CI-overlap comparison (see Section 7's rationale).
- As with the primary analysis, this remains a selection-on-observables estimate; first-birth restriction addresses one specific confounding concern (prior Cesarean), not all unmeasured confounding.
