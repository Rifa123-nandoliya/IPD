# Extensions work — executive summary

This folder holds this teammate's contribution to the IPD project's five
planned extensions, per the "IPD Extension Implementation Handoff." It lives
entirely alongside the frozen `notebooks/v2/` pipeline and modifies nothing
inside it, `outputs/final_tables/`, `outputs/final_figures/`, `outputs/metadata/`,
or `outputs/tables/`.

**Scope of this contribution:** Extension 2 (causal heterogeneity) and
Extension 3 (NFHS-4/NFHS-5 temporal comparison) only. Extensions 1
(quantitative bias analysis), 4 (health-system context linkage), and 5
(first-birth AIPW) are out of scope for this folder and are expected to be
contributed separately.

## Status

| Extension | Folder | Status | Notes |
|---|---|---|---|
| 2 — Causal heterogeneity / DR-learner | `02_causal_heterogeneity/` | Complete | Run on the real NFHS-5 cohort (n=200,794). See folder README for final results: the gap ranges ~15-42pp across women, driven mainly by one state, then education/wealth; significantly larger in rural areas; no clear social-group effect. |
| 3 — NFHS-4 → NFHS-5 temporal AIPW | `03_nfhs4_nfhs5_temporal/` | Partial | Notebook complete and logic-verified against synthetic data. Additionally blocked on: (a) an authorized local NFHS-4 Birth Recode to run the harmonization helper against, and (b) verifying `state`/`social_group` harmonization against the NFHS-4 recode manual (see `BLOCKED.md`). |

## Shared infrastructure

- `shared/config.py` — local paths (NFHS-4/NFHS-5 file locations, overridable
  via environment variables) and constants shared by both notebooks. No
  secrets or data.
- `shared/utils.py` — reusable helpers reproducing the exact nuisance-model,
  cross-fitting, AIPW, and PSU-bootstrap conventions used in
  `notebooks/v2/06_propensity_overlap_diagnostics.ipynb` and
  `notebooks/v2/07_aipw_primary_analysis.ipynb`, so both extensions build on
  identical machinery instead of divergent copies.
- `shared/data_dictionary.md` — variables used by these two extensions,
  including Extension 2's pre-specified moderator set and Extension 3's
  NFHS-4/NFHS-5 variable crosswalk.

## Data access

Neither extension's data is included here. Extension 2 needs the same
`data/processed/df_model_v2.parquet` used by `notebooks/v2/06`–`07`.
Extension 3 additionally needs an authorized local copy of the NFHS-4 Birth
Recode. Both are referenced only through `shared/config.py` local paths /
environment variables and are excluded from version control by the
repository's `.gitignore`.

## How to run

Each extension's notebook is self-contained and can be run independently
once its data dependency is available locally:

```bash
pip install -r requirements.txt
pip install -r extensions_work/requirements_extensions.txt
jupyter notebook extensions_work/02_causal_heterogeneity/notebook.ipynb
jupyter notebook extensions_work/03_nfhs4_nfhs5_temporal/notebook.ipynb
```

See `CHANGELOG.md` for methodological decisions and known unresolved issues,
`BLOCKED.md` for exactly what data/access is still needed and what to do
next, and each extension's own `README.md` for its question, method, final
estimates, QA checks, limitations, and files produced.
