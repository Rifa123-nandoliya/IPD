# Extension 5 — Strong First-Birth AIPW Analysis

**Status: real run completed on actual NFHS-5 data (n = 82,426). An
independent clean-run/reproducibility check is still pending** — this
README was previously left saying "not run / synthetic only" after a real
run had already produced these results; that inconsistency is fixed here.

## What changed in this revision (2026-09-27, following an external implementation review)

- **Stale status text fixed.** This README, `BLOCKED.md`, and the root
  status table said "not run on real data" while real, saved outputs
  already existed. They're updated below with the actual numbers.
- **Invalid "significance" language removed.** The comparison to the
  full-cohort primary previously stated the two estimates were
  "distinguishable at the 95% level" based on non-overlapping marginal
  CIs — not a valid test, since first births are a *subset* of the full
  cohort and their sampling variability is correlated with it. The
  notebook now shows both estimates and CIs side by side with no
  significance claim drawn from their overlap.
- **Bootstrap scope disclosed explicitly.** `shared/utils.run_cross_fitted_aipw`'s
  PSU-cluster bootstrap holds the fitted nuisance predictions fixed for
  every replicate (matching Notebook 07's own documented convention) — now
  stated plainly in the notebook rather than left implicit.

## Research question

Does the adjusted public-private Cesarean gap remain among first births,
where prior Cesarean history is impossible by construction?

## Real results (n = 82,426)

| | Private | Public |
|---|---:|---:|
| n | 23,987 | 58,439 |
| Adjusted risk | 49.4635% | 20.5559% |

**Adjusted risk difference:** 28.9076 pp (95% CI 27.8827–29.9511)
**Adjusted risk ratio:** 2.4063 (95% CI 2.3292–2.4811)
**Missing `age_at_first_birth`:** 0 (no exclusions needed for this run)

### Comparison with the full-cohort primary estimate

| Cohort | n | Adjusted RD | 95% CI |
|---|---:|---:|---|
| Full cohort (Notebook 07) | 200,794 | 28.4698 pp | [27.6720, 29.2443] |
| First births only (this notebook) | 82,426 | 28.9076 pp | [27.8827, 29.9511] |

**No significance test is applied to this comparison.** First births are a
subset of, not independent from, the full cohort, so their sampling
variability is correlated with it — treating CI overlap/non-overlap as a
formal test would be invalid (see the notebook's Section 7 for the
reasoning, and Extension 3's genuinely independent NFHS-4/NFHS-5 samples
for contrast with a case where that kind of test *is* valid). Descriptively,
the two point estimates are close (28.91 pp vs. 28.47 pp), which is at
least consistent with the gap not being an artifact of prior-Cesarean
history mixed into the full cohort — but that is an observation, not a
statistical claim.

### Method (unchanged from the prior revision, since the review found the core cohort/confounder-set logic correct)

A dedicated first-birth-only AIPW model — cohort defined by `birth_order == 1`
(never `birth_index`), confounder set swapping the now-constant
`birth_order` for `age_at_first_birth` (exact for this subgroup by
construction), independently cross-fitted nuisance models (not reused from
Notebook 07), and a PSU-cluster bootstrap whose scope is now explicitly
documented (see above).

## What still needs to happen

1. **Independent clean-run verification.** Re-run this notebook top to
   bottom from a clean kernel and confirm it reproduces n=82,426, arm
   counts 23,987/58,439, RD=28.9076 pp, and RR=2.4063 within numerical
   tolerance. If it doesn't, stop and trace the cohort/input version
   before trusting either run.
2. **NFHS `birth_order` logic double-check.** Confirm how NFHS-5 codes
   `birth_order` for multiple births (twins) at the index delivery, so
   "first birth" is verified to mean what this notebook assumes.
3. Fill in balance/overlap diagnostic details (tail-weight shares, full
   quantiles) into this README if a deeper positivity write-up is wanted —
   the current `first_birth_overlap_balance.csv` has the SMD table but not
   extended tail diagnostics.

## Inputs

- `data/processed/df_model_v2.parquet` (same file as Notebooks 06/07)
- `outputs/final_tables/final_aipw_overall_table.csv` (frozen primary result, for the comparison step)
- `notebooks/v2/01_v2_data_audit_and_cohort.ipynb` (first-birth definition, `age_at_first_birth` documentation)
- `notebooks/v2/06_propensity_overlap_diagnostics.ipynb`, `notebooks/v2/08_risk_stratified_aipw.ipynb`

## Files produced

- `notebook.ipynb`
- `outputs/first_birth_cohort_summary.csv`
- `outputs/first_birth_overlap_balance.csv`
- `outputs/first_birth_aipw_summary.csv`
- `outputs/first_birth_bootstrap_summary.csv`
- `outputs/first_birth_comparison_plot.png`
- `outputs/first_birth_metadata.json`

## QA / interpretation checks

- First-birth definition verified as `birth_order == 1`, explicitly not `birth_index`.
- `birth_order`'s constancy within the cohort is asserted before it's excluded as a predictor.
- Explicitly states: prior-Cesarean confounding is removed *by construction*, but other first-birth-specific unmeasured obstetric indications (fetal compromise, labor dystocia) are not.
- Explicitly does not claim novelty as "the first" such analysis in India.
- No significance inference is drawn from the full-cohort/first-birth CI comparison.
- The bootstrap's fixed-nuisance scope is now stated explicitly in the notebook.

## Limitations

- Nuisance models are refit from scratch on the first-birth subset (smaller n than the full-cohort primary) rather than borrowing strength from the full model.
- No formal statistical test for whether the first-birth estimate differs from the full-cohort primary — descriptive comparison only.
- Bootstrap CIs are conditional on the fitted nuisance models for this run, not a full refit-per-replicate uncertainty (matches Notebook 07's own convention).
- As with the primary analysis, this remains a selection-on-observables estimate; first-birth restriction addresses one specific confounding concern (prior Cesarean), not all unmeasured confounding.
