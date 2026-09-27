# Extension 2 — Causal heterogeneity / DR-learner

**Status: code repaired following an external implementation review; a
fresh real-data run is now required.** The results below from the
previous run are kept for historical reference and are **stale** — they
came from an architecture this revision replaces. Do not cite the numbers
in this file as current until you re-run the notebook and this README is
updated from that fresh output.

## What changed in this revision (2026-09-27)

An external review of the submitted notebook and its saved outputs found
several real problems, fixed here:

- **README transcription bug (fixed immediately).** The previous README
  reported Q3 RR = 4.27 and Q5 RR = 4.70; the actual saved CSV had
  3.4271 and 3.4704. Going forward, README numbers should be copy-checked
  directly against the saved CSV, not retyped from memory.
- **Unsafe merge repaired.** The optional reuse of Notebook 07's frozen
  row-level nuisances merged on `respondent_id` alone — not safe, since a
  respondent can have multiple analytic births, making this a potential
  many-to-many merge that matching row counts didn't rule out. It now
  requires a verified birth-level key (e.g. `birth_index`) in **both**
  frames and a `pandas.merge(..., validate="one_to_one")` that actually
  succeeds; since the saved nuisance file doesn't currently carry such a
  key, this safely falls back to a local refit by default.
- **Architecture repaired: single dev/test split, not two independently
  folded stages.** The previous design fit Stage 1 (nuisances) and Stage 2
  (the CATE model) on *independent* fold partitions and called the result
  "honest" — not fully justified, since Stage 2's training targets could
  have come from Stage-1 models that also saw some of Stage 2's own
  held-out respondents. This version uses one respondent-grouped
  development/test split: Stage 1, preprocessing, Stage 2, and the
  quantile-bin thresholds are *all* fit on development only, and test is
  scored but never fit by anything — the "simpler, fully auditable"
  alternative the review explicitly endorses, at the cost of a smaller
  effective validation sample.
- **Preprocessing leakage repaired.** One-hot encoding and numeric
  imputation are now fit on development only and applied to test, not fit
  on the full cohort before any split.
- **Feature importance repaired.** Impurity-based importance (in-sample,
  and not a "percent of explained heterogeneity") is replaced with
  permutation importance evaluated on the untouched test set, aggregated
  back to each source variable across its one-hot dummies.
- **Invalid "significance" claims removed.** The previous version treated
  non-overlapping marginal CIs (rural vs. urban, Q5 vs. Q1) as evidence of
  a real difference — not a valid test, since both groups are drawn from
  the same dataset and their sampling variability is correlated. This
  version computes a genuine joint/paired bootstrap (one PSU resample per
  replicate, both groups computed from that same draw) for these two
  headline contrasts, giving a direct, valid CI for the difference itself.
- **Notebook verdict no longer overridden by the README.** If the
  monotonicity check reports the bins aren't strictly increasing, the
  README will report that plainly rather than asserting "convincing"
  heterogeneity anyway.

## Research question

Among observed patient and contextual characteristics, where does the
adjusted private-vs-public Cesarean contrast appear larger or smaller?

## Method (revised)

1. **Development/test split.** One respondent-grouped 60/40 split.
   Everything below is fit on development only; test is scored, never fit.
2. **Stage 1 (nuisance models).** Cross-fitted within development
   (identical specification to Notebook 07); a single propensity/outcome
   fit on all of development scores test directly.
3. **Pseudo-outcome.** `tau_hat = psi1 - psi0` for both splits.
4. **Stage 2 (CATE model).** `RandomForestRegressor` fit on development's
   `tau_hat`, with preprocessing (imputation/encoding) also fit on
   development only.
5. **Quantile bins.** Thresholds chosen from development's predicted
   distribution, applied to (never re-derived from) test.
6. **Validation.** Realized AIPW effects per bin/subgroup computed on test
   only. The two headline contrasts (rural vs. urban, Q5 vs. Q1) get a
   proper joint/paired PSU bootstrap for a direct difference CI.

No dedicated causal-forest package (`econml`/`grf`) is used.

## Historical results (STALE — from the previous full-cohort, no-split architecture)

These come from a real run of the *previous* code version (n = 200,794,
matching the frozen primary sample) and are kept only so the transcription
fix is visible in context. **They do not reflect the repaired architecture
above and must not be treated as current:**

| Predicted-CATE group | n | Realized adjusted RD | 95% CI | Realized RR (corrected) |
|---|---:|---:|---|---:|
| Q1 (lowest) | 40,233 | 14.81 pp | [13.37, 16.41] | 1.84 |
| Q2 | 42,480 | 26.42 pp | [24.85, 28.00] | 2.19 |
| Q3 | 47,694 | 32.05 pp | [30.48, 33.57] | **3.43** (was misreported as 4.27) |
| Q4 | 35,370 | 31.53 pp | [29.55, 33.57] | 3.98 |
| Q5 (highest) | 35,017 | 42.04 pp | [40.47, 43.57] | **3.47** (was misreported as 4.70) |

`heterogeneity_modifier_summary.csv` from that same old run reported
`state_19` at impurity-importance 0.332 — described at the time as "a
third of the model's explanatory power." That characterization is now
understood to be imprecise for two reasons (see "What changed" above):
impurity importance isn't a variance-explained share, and it wasn't
evaluated on held-out data. Whether `state_19` remains the top modifier
under permutation importance on a genuine test split is an open question
until the notebook is re-run.

## What still needs to happen

1. **Re-run this notebook** locally where `data/processed/df_model_v2.parquet`
   exists, to produce real output under the repaired dev/test-split
   architecture (expect a smaller effective test sample and wider CIs than
   the historical full-cohort numbers above).
2. **Update this README from that fresh output** — replace the "historical
   results" section with the new `heterogeneity_individual_or_binned_summary.csv`,
   `heterogeneity_modifier_summary.csv`, and `heterogeneity_headline_contrasts.csv`,
   copy-checked directly against the CSVs.
3. **Report the monotonicity/verdict exactly as printed**, without
   overriding it with more confident language than the check itself
   supports.
4. Decode `state_19` (or whichever state ranks top) against the actual
   NFHS-5 state code list before naming it in any report, and do not infer
   a health-system mechanism from a code alone.

## Verification

Smoke-tested end-to-end against synthetic data, including a deliberately
constructed case with a duplicated `respondent_id` (multiple analytic
births per respondent) and a matching fake frozen-nuisance file **without**
a birth-level key — confirming the merge-safety fix correctly falls back to
a local refit rather than silently accepting an unsafe merge. The full
dev/test pipeline, permutation importance, and joint bootstrap for the
headline contrasts all ran without errors. No synthetic data or its
outputs are included in this folder or committed anywhere.

## Inputs

- `data/processed/df_model_v2.parquet` (same cohort as Notebook 07)
- `outputs/tables/b4_aipw_row_level_nuisance.csv` (optional — only reused if a verified birth-level key validates a one_to_one merge)
- `outputs/final_tables/final_aipw_overall_table.csv` (frozen primary result, for context)
- `notebooks/v2/06_propensity_overlap_diagnostics.ipynb`, `notebooks/v2/07_aipw_primary_analysis.ipynb`

## Files produced

- `notebook.ipynb`
- `outputs/heterogeneity_individual_or_binned_summary.csv` — now test-set only
- `outputs/heterogeneity_modifier_summary.csv` — now permutation importance, aggregated by variable
- `outputs/heterogeneity_headline_contrasts.csv` — **new**: joint/paired bootstrap for rural-vs-urban and Q5-vs-Q1
- `outputs/heterogeneity_distribution.png`, `outputs/heterogeneity_subgroups.png`
- `outputs/heterogeneity_metadata.json`

## QA / interpretation checks

- No post-outcome or post-treatment variable is in the moderator set (asserted).
- Test set is never used to fit Stage 1, preprocessing, Stage 2, or bin thresholds — only to score them.
- Feature importance is permutation-based, evaluated on test, aggregated by source variable.
- The two headline contrasts have a genuine joint/paired-bootstrap CI for their difference, not an inference from marginal CI overlap.
- The printed monotonicity verdict is reported as-is, not overridden by more confident prose.

## Limitations

- Test-set-only evaluation trades sample size (and rare-category stability) for full auditability; results come from one split, not independently replicated across splits.
- The joint bootstrap for headline contrasts is conditional on the fixed, already-fitted Stage-1/Stage-2 models for this split — it does not refit the entire pipeline inside each replicate.
- Permutation importance sums independently-shuffled dummy importances per variable, which approximates but isn't identical to jointly permuting all of a variable's dummies at once.
- This remains exploratory adjusted-effect heterogeneity, not personalized causal truth, and inherits the primary AIPW analysis's selection-on-observables assumption.
