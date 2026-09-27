# Extensions work — executive summary

This folder holds this teammate's contribution to the IPD project's five
planned extensions, per the "IPD Extension Implementation Handoff." It lives
entirely alongside the frozen `notebooks/v2/` pipeline and modifies nothing
inside it, `outputs/final_tables/`, `outputs/final_figures/`, `outputs/metadata/`,
or `outputs/tables/`.

**Scope of this contribution:** Extensions 1, 2, 3, and 5. Extension 4
(health-system context linkage) is out of scope for this folder and is
expected to be contributed separately.

## Status

| Extension | Folder | Status | Notes |
|---|---|---|---|
| 1 — Quantitative bias analysis | `01_quantitative_bias/` | Complete (repaired 2026-09-27) | Fully executed for real. Status downgraded from "robust finding" to "illustrative scenario analysis — not evidence-calibrated" per external review: every parameter except the (sourced) multiparous fraction is an unsourced placeholder. Prior-Cesarean scenario now correctly scoped to the multiparous population. See folder README. |
| 2 — Causal heterogeneity / DR-learner | `02_causal_heterogeneity/` | **Reopened** — code repaired 2026-09-27, fresh run pending | An external review found a README transcription error, an unsafe merge, preprocessing leakage, and invalid CI-overlap "significance" claims. Architecture rebuilt (dev/test split, permutation importance, joint bootstrap); previously-saved outputs are now marked stale pending a fresh real-data run. See folder README/BLOCKED.md. |
| 3 — NFHS-4 → NFHS-5 temporal AIPW | `03_nfhs4_nfhs5_temporal/` | Partial | Real crosswalk/descriptives/overlap-balance outputs now saved (NFHS-4 harmonization in progress). Not yet reviewed against the external-review checklist applied to 1/2/5. |
| 5 — First-birth AIPW | `05_first_birth/` | Complete (repaired 2026-09-27) | Real run on actual NFHS-5 data: n=82,426, RD=28.9076pp, RR=2.4063. Fixed stale "not run" status text and an invalid CI-overlap "significance" claim per external review. Independent clean-run verification still pending. See folder README. |

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

No extension's data is included here. **Extension 1 needs no raw data at
all** — it runs entirely off already-committed frozen summary tables.
Extensions 2 and 5 need the same `data/processed/df_model_v2.parquet` used
by `notebooks/v2/06`–`07`. Extension 3 additionally needs an authorized
local copy of the NFHS-4 Birth Recode. All are referenced only through
`shared/config.py` local paths / environment variables and are excluded
from version control by the repository's `.gitignore`.

## How to run

Each extension's notebook is self-contained and can be run independently
once its data dependency (if any) is available locally:

```bash
pip install -r requirements.txt
pip install -r extensions_work/requirements_extensions.txt
jupyter notebook extensions_work/01_quantitative_bias/notebook.ipynb        # no data needed
jupyter notebook extensions_work/02_causal_heterogeneity/notebook.ipynb
jupyter notebook extensions_work/03_nfhs4_nfhs5_temporal/notebook.ipynb
jupyter notebook extensions_work/05_first_birth/notebook.ipynb
```

See `CHANGELOG.md` for methodological decisions and known unresolved issues,
`BLOCKED.md` for exactly what data/access is still needed and what to do
next, and each extension's own `README.md` for its question, method, final
estimates, QA checks, limitations, and files produced.
