# Extension 2 — Causal heterogeneity / DR-learner

**Status: in progress — notebook not yet implemented.**

## Research question

Among observed patient and contextual characteristics, where does the
adjusted private-vs-public Cesarean contrast appear larger or smaller?

## Planned method

Honest DR-learner / causal forest on the same public/private analytic
cohort and confounder set as `notebooks/v2/07_aipw_primary_analysis.ipynb`,
using a pre-specified moderator set (see
`../shared/data_dictionary.md`), respondent-grouped cross-fitting, and
PSU-aware uncertainty where feasible.

## Inputs

- `data/processed/df_model_v2.parquet` (same cohort as Notebook 07)
- `notebooks/v2/06_propensity_overlap_diagnostics.ipynb` (confounder set)
- `notebooks/v2/07_aipw_primary_analysis.ipynb` (AIPW machinery reused via `../shared/utils.py`)
- `outputs/metadata/b4_aipw_metadata.json`

## Files produced (once complete)

- `notebook.ipynb`
- `outputs/heterogeneity_individual_or_binned_summary.csv`
- `outputs/heterogeneity_modifier_summary.csv`
- `outputs/heterogeneity_distribution.png`
- `outputs/heterogeneity_subgroups.png`

This README will be filled in with the final method, estimates, QA checks,
limitations, and interpretation once the notebook is implemented and run.
