# Blocked items

## Extension 2 — Causal heterogeneity / DR-learner

**Status: notebook complete, not run on real data.**

**Blocker:** this development environment has no access to
`data/processed/df_model_v2.parquet` or any NFHS-5 microdata — by design,
per the handoff's own data-access rule (NFHS microdata must never be
uploaded into a shared/cloud session or committed to GitHub).

**What's needed next:** run `extensions_work/02_causal_heterogeneity/notebook.ipynb`
locally, in an environment where `data/processed/df_model_v2.parquet`
already exists (the same file `notebooks/v2/06`–`07` use). If
`outputs/tables/b4_aipw_row_level_nuisance.csv` also exists locally (i.e.
Notebook 07 has already been run there), the notebook will automatically
reuse its exact nuisance predictions; otherwise it refits identical
machinery itself. Once run, fill in the final estimates/QA results into
`02_causal_heterogeneity/README.md`.

The notebook's logic has been verified end-to-end against synthetic,
schema-matching data with a known injected heterogeneous effect, which the
DR-learner correctly recovered (see that folder's README).

## Extension 3 — NFHS-4 → NFHS-5 temporal comparison

**Status: notebook complete, not run on real data. Additional blockers beyond Extension 2's.**

**Blockers:**
1. Same NFHS-5 data-access constraint as Extension 2, plus:
2. No authorized local copy of the **NFHS-4 Birth Recode** is available in
   this environment, and NFHS-4 needs its own harmonization pass before this
   notebook can run — there is no existing `df_model_nfhs4`-equivalent file
   anywhere in this repository to reuse (unlike NFHS-5, which already has
   `notebooks/v2/01`'s frozen output).
3. Two of the eight primary confounders — `state` (v024) and `social_group`
   (s116) — have **unverified cross-round harmonization** (state/UT boundary
   changes between 2015-16 and 2019-21; unconfirmed NFHS-4 `s116` coding).
   The notebook's crosswalk (`outputs/nfhs4_nfhs5_variable_crosswalk.csv`)
   flags both explicitly and automatically excludes them from the reduced/
   sensitivity confounder set rather than assuming they harmonize cleanly.

**What's needed next:**
1. Obtain an authorized local copy of the NFHS-4 Birth Recode.
2. Run `extensions_work/03_nfhs4_nfhs5_temporal/notebook.ipynb` Section 3's
   `harmonize_nfhs4_raw()` helper against it, and save the result to
   `shared/config.NFHS4_PROCESSED_DATA_PATH` (or set the
   `IPD_NFHS4_PROCESSED_PATH` environment variable to point elsewhere).
3. Before trusting the primary (full 8-confounder) result: check the NFHS-4
   recode manual to confirm `s116` is coded identically to NFHS-5, and build
   an explicit state/UT crosswalk if a pooled `state` effect is wanted. Until
   then, treat the **reduced-confounder-set (sensitivity) result** in
   `temporal_change_summary.csv` as the more defensible one.
4. Run the notebook, then fill in the final estimates/QA results into
   `03_nfhs4_nfhs5_temporal/README.md`.

The notebook's logic — crosswalk, harmonization sensitivity, per-round
cross-fitted AIPW, and the paired-bootstrap change estimator — has been
verified end-to-end against synthetic NFHS-4/NFHS-5-shaped datasets with a
known injected change in effect size, which it correctly recovered (see
that folder's README).
