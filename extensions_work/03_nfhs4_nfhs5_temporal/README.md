# Extension 3 — NFHS-4 → NFHS-5 doubly robust temporal comparison

**Status: notebook implemented, syntax- and logic-verified against synthetic
NFHS-4/NFHS-5-shaped datasets with a known injected change in effect size
(recovered correctly — see "Verification" below). Not yet run on real NFHS-4/
NFHS-5 data — that step is yours to run locally, since this sandbox has no
data access, and NFHS-4 also needs its own local harmonization step first
(Section 3 of the notebook).**

## Research question

Did the adjusted private-vs-public Cesarean risk difference change between
NFHS-4 (2015–16) and NFHS-5 (2019–21)?

## Method

1. **Variable crosswalk**, built and saved *before* any modeling
   (`outputs/nfhs4_nfhs5_variable_crosswalk.csv`). Two of the eight primary
   confounders — `state` and `social_group` — are flagged `verified = False`
   because state/UT boundary changes and NFHS-4's exact `s116` coding aren't
   confirmed in this sandbox; see `../shared/data_dictionary.md`.
2. **NFHS-4 harmonization helper** (`harmonize_nfhs4_raw()`, Section 3):
   reproduces the exact `m15 → facility_type` recoding and `s116`/`v133`
   special-code cleaning used in `notebooks/01_data_exploration.ipynb`,
   applied to a raw NFHS-4 Birth Recode. Run once locally against your
   authorized NFHS-4 copy and save the result to
   `shared/config.NFHS4_PROCESSED_DATA_PATH`.
3. **Round-specific survey-weighted descriptives and overlap/balance
   diagnostics**, computed independently per round with each round's own
   design variables.
4. **Round-specific cross-fitted AIPW** — identical architecture to
   `notebooks/v2/07_aipw_primary_analysis.ipynb`, fit *independently* within
   each round (not one pooled nuisance model with a round interaction — see
   the notebook's final documentation section for why).
5. **Change estimand with a directly computed CI.** Because NFHS-4 and
   NFHS-5 are independent samples, `Var(RD5 − RD4) = Var(RD5) + Var(RD4)`
   exactly, so pairing same-index PSU-cluster bootstrap replicates from each
   round's own bootstrap array (`change_b = RD5_reps[b] − RD4_reps[b]`)
   gives a formally valid percentile CI for the change — not a naive
   subtraction of two independently reported point estimates.
6. **Harmonization sensitivity analysis** (handoff step 29, required): the
   same pipeline is re-run with a *reduced* confounder set that automatically
   drops any crosswalk-flagged or empirically degenerate variable — driven by
   the crosswalk's own verification flags, not chosen after inspecting
   results.

## Verification (this sandbox has no NFHS access)

Smoke-tested end-to-end against synthetic NFHS-4-shaped and NFHS-5-shaped
datasets (same harmonized schema, ~5,000–6,000 records each) with a
deliberately larger injected private-sector effect in the synthetic
"NFHS-5" wave. The full pipeline — crosswalk, harmonization sensitivity,
per-round cross-fitted AIPW, and the paired-bootstrap change estimator —
ran without errors and correctly detected the injected increase (a positive
change in RD with a 95% CI excluding zero). No synthetic data or its
outputs are included in this folder or committed anywhere.

**Final estimates, real QA results, and interpretation will be added to
this README once run on the actual NFHS-4/NFHS-5 cohorts.**

## Inputs

- Authorized local NFHS-4 Birth Recode (raw), harmonized via Section 3's helper into `shared/config.NFHS4_PROCESSED_DATA_PATH`
- `data/processed/df_model_v2.parquet` (same NFHS-5 cohort as Notebook 07)
- `notebooks/01_data_exploration.ipynb` (source of the exact `m15`/`s116`/`v133` recoding reused for NFHS-4)
- `notebooks/v2/06_propensity_overlap_diagnostics.ipynb` and `notebooks/v2/07_aipw_primary_analysis.ipynb` (propensity/AIPW logic, reused via `../shared/utils.py`)

## Files produced

- `notebook.ipynb`
- `outputs/nfhs4_nfhs5_variable_crosswalk.csv`
- `outputs/temporal_descriptives.csv`
- `outputs/temporal_overlap_balance.csv` (supplementary; not one of the five minimum required outputs, kept for transparency)
- `outputs/temporal_aipw_results.csv`
- `outputs/temporal_change_summary.csv` — primary and harmonization-sensitivity (reduced confounder set) rows side by side
- `outputs/temporal_forest_plot.png`
- `outputs/temporal_metadata.json`

## QA / interpretation checks (built into the notebook)

- Every pooled-model variable's substantive meaning across rounds is checked against the crosswalk's `verified` flag (Section 11).
- Round-specific survey design (weights, PSU, stratum) is never pooled across rounds — each round is loaded, diagnosed, and bootstrapped independently.
- A formal CI for the change in adjusted RD is always reported, never omitted.
- The notebook explicitly states that a change (or lack of change) is not causal evidence of a specific policy effect unless a policy-identifying design (e.g. a genuine difference-in-differences around an identified shock) is separately implemented — which this notebook does not attempt.

## Known unresolved harmonization issues (documented, not silently patched)

- `state` (v024): state/UT boundary changes between 2015–16 and 2019–21 are not crosswalked to a common coding here — excluded from the reduced/sensitivity confounder set until that crosswalk is built and verified.
- `social_group` (s116): NFHS-4 coding not confirmed identical to NFHS-5's — excluded from the reduced/sensitivity confounder set until verified against the NFHS-4 recode manual.
- `wealth_index` (v190): DHS wealth-index construction has known cross-round methodology revisions; treated as ordinal within-round only, not asserted as a continuously comparable scale across rounds.

## Limitations

- Round-specific nuisance models are fit fully independently; this trades some statistical efficiency (vs. a pooled model that could borrow strength across rounds) for a materially simpler and more defensible design given the state/social-group harmonization risk above.
- The reduced confounder set is smaller than the primary set by construction whenever the crosswalk flags a variable — the sensitivity analysis's job is to show how much the change estimate moves as a result, not to declare either set "correct."
