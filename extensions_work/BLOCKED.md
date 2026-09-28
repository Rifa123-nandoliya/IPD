# Blocked items

## Extension 1 — Quantitative bias analysis

**Status: REOPENED — audited 2026-09-28; a fresh real-data run is required.**
The audit found the notebook diluted both sectors' scenario prevalence by
one *pooled* later-delivery share despite already computing that the
sectors' shares differ substantially — fixed to use each sector's own
share (see CHANGELOG), but not yet re-run against real data in this
environment. A literature search for real, citable prevalence/risk-ratio
parameters was attempted and **could not be completed**: full-text
verification (WebFetch) is blocked for every domain tested in this
session (PMC/NCBI, Springer, PLOS, medRxiv, ScienceDirect, general news,
and Wikipedia as a control) — reported as a transparent negative finding,
not filled with guessed values. See `01_quantitative_bias/README.md` for
the evidence table, unverified candidate sources, and unresolved
methodological decisions for a statistician. **Publication readiness is
explicitly not promised.**

**What's needed next:**
1. Re-run `notebook.ipynb` where `data/processed/df_model_v2.parquet` exists, to get real numbers under the sector-specific-dilution fix.
2. From an environment with normal (unblocked) web access, verify or refute the candidate sources listed in the README, or find better ones.
3. Resolve the "Unresolved decisions for a statistician" in the README before treating this extension as contributing to the paper's robustness claims.

## Extension 2 — Causal heterogeneity / DR-learner

**Status: REOPENED — code repaired 2026-09-27 following an external
implementation review; a fresh real-data run is now required.** The
notebook's architecture changed substantially (single development/test
split replacing two independently-folded stages; safe merge validation;
permutation importance; a genuine joint bootstrap for the headline
contrasts) — the previously-saved outputs in
`02_causal_heterogeneity/outputs/` come from the *old* architecture and
are marked stale (see `outputs/STALE_PENDING_RERUN.md`). See
`02_causal_heterogeneity/README.md` for the full list of what changed and
what a fresh run needs to reproduce.

**What's needed next:** run `extensions_work/02_causal_heterogeneity/notebook.ipynb`
locally, in an environment where `data/processed/df_model_v2.parquet`
already exists. Once run, replace the "historical results" section of
`02_causal_heterogeneity/README.md` with fresh numbers copy-checked
directly against the new CSVs, and delete `outputs/STALE_PENDING_RERUN.md`.

The repaired notebook's logic has been verified end-to-end against
synthetic data, including a constructed duplicate-`respondent_id` case with
a matching fake frozen-nuisance file lacking a birth-level key, confirming
the merge-safety fix correctly falls back to a local refit rather than
silently accepting an unsafe merge (see that folder's README).

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

## Extension 5 — First-birth AIPW

**Status: RESOLVED — real run completed on actual NFHS-5 data (n=82,426,
RD=28.9076pp). Repaired 2026-09-27 following an external implementation
review** (removed an invalid CI-overlap "significance" claim; explicitly
disclosed the bootstrap's fixed-nuisance scope). See
`05_first_birth/README.md` for final results.

**What's still open (non-blocking):** an independent clean-run
verification — re-run from a clean kernel and confirm the same n=82,426,
arm counts, RD, and RR are reproduced within numerical tolerance — has not
yet been performed.
