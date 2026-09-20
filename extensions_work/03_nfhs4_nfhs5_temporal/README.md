# Extension 3 — NFHS-4 → NFHS-5 doubly robust temporal comparison

**Status: in progress — notebook not yet implemented.**

## Research question

Did the adjusted private-vs-public Cesarean risk difference change between
NFHS-4 (2015–16) and NFHS-5 (2019–21)?

## Planned method

Harmonize a common eligibility/confounder set across rounds (see the
crosswalk in `../shared/data_dictionary.md`), run round-specific
survey-weighted descriptives and overlap diagnostics, then estimate a
pooled time-by-sector doubly robust estimand so the confidence interval for
*change* in the adjusted risk difference is estimated directly rather than
by subtracting two independent point estimates.

## Inputs

- Authorized local NFHS-4 Birth Recode (path set in `../shared/config.py`)
- `data/processed/df_model_v2.parquet` / NFHS-5 local V2 processed data
- `notebooks/v2/01_v2_data_audit_and_cohort.ipynb` (cohort logic)
- `notebooks/v2/06_propensity_overlap_diagnostics.ipynb` and
  `notebooks/v2/07_aipw_primary_analysis.ipynb` (propensity/AIPW logic, reused via `../shared/utils.py`)

## Files produced (once complete)

- `notebook.ipynb`
- `outputs/nfhs4_nfhs5_variable_crosswalk.csv`
- `outputs/temporal_descriptives.csv`
- `outputs/temporal_aipw_results.csv`
- `outputs/temporal_change_summary.csv`
- `outputs/temporal_forest_plot.png`

This README will be filled in with the final method, estimates, QA checks,
limitations, and interpretation once the notebook is implemented and run.
