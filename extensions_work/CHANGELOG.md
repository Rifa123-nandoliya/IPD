# Changelog — extensions_work (Extensions 1, 2, 3 & 5)

## 2026-09-28 — Extension 1 statistician audit

A full audit (code inspection, literature search, evidence classification,
methodological verdict) of Extension 1, requested independently of the
2026-09-27 review below. Findings and fixes:

- **Real defect found and fixed:** the notebook already computed and
  *reported* that public/private later-delivery (parity) shares differ
  substantially, but still diluted both `p0` and `p1` by one **pooled**
  share. Hand-calculation using the notebook's own numbers shows this
  roughly halves the true sector-specific prevalence gap for the "mild"
  scenario. Fixed: each arm is now diluted by its own sector's share.
  Verified by a code-correctness smoke test against synthetic data (not
  real results); a real re-run is still required for updated numbers.
- **Literature search attempted, not completed.** WebFetch (full-text
  verification) was blocked for every domain tested in this environment
  (PMC/NCBI, Springer, PLOS, medRxiv, ScienceDirect, general news, and
  Wikipedia as a control). Candidate sources were identified via search
  snippets only and are listed in the README as unverified leads, not
  citations. Reported as a transparent negative finding rather than filled
  with unsourced guesses, per this audit's explicit decision rule.
- **Cleanup:** removed a stray `extensions_work.zip` committed at the repo
  root, duplicate/backup README and notebook files
  (`README.before_*.md`, `notebook.before_*.ipynb`, a duplicated
  `final_aipw_overall_table.csv` inside the extension folder), and
  consolidated three README variants into one canonical `README.md`.
- **Verdict:** publication readiness is not promised. Both the evidence
  gap (no sourced QBA parameters) and part of the bias-factor method's own
  validity conditions (independence/homogeneity of the unmeasured factor
  relative to the 8 measured confounders) remain open — see the README's
  "Unresolved decisions for a statistician."

## 2026-09-27 — Repairs following an external implementation review

An external review of the submitted `extensions_work.zip` and its saved
real-data outputs (Extensions 1, 2, 5) found real bugs and overclaiming
that are fixed as of this date. Full detail is in each extension's own
README; summary:

- **Extension 1:** prior-Cesarean scenario now correctly scoped to the
  multiparous population (was previously applied to the whole cohort
  despite being structurally impossible for first births); tipping-point
  search now reports "unattainable" instead of a large finite number when
  no finite risk ratio can close the gap; `assumptions_sources.csv`
  expanded to a 15-column schema with explicit `hypothetical / unsourced`
  labels; status downgraded from "robust finding" to "illustrative
  scenario analysis."
- **Extension 2:** fixed a README transcription bug (Q3/Q5 risk ratios);
  the optional reuse of Notebook 07's frozen nuisances now requires a
  verified birth-level key and a validated one-to-one merge instead of
  merging on `respondent_id` alone; rebuilt around a single development/
  test split (replacing two independently-folded stages) so test is
  genuinely never fit on; feature importance switched from in-sample
  impurity to held-out permutation importance; added a genuine joint/
  paired bootstrap for the two headline subgroup contrasts, replacing an
  invalid CI-overlap "significance" claim. Previously-saved outputs are
  from the old architecture and are marked stale pending a fresh run.
- **Extension 5:** fixed stale README/BLOCKED text that said "not run on
  real data" after a real run (n=82,426) had already produced saved
  results; removed an invalid CI-overlap "significance" claim from the
  full-cohort comparison; explicitly disclosed that the bootstrap holds
  nuisance predictions fixed per replicate (matching Notebook 07's own
  documented convention).

Extension 3 was not covered by this review and has not been checked
against the same checklist.

## Packages added

None. See `requirements_extensions.txt`.

## Data sources obtained

None yet in this environment. This development sandbox has no NFHS access
(see `BLOCKED.md`). Both notebooks were written and logic-verified against
synthetic, schema-matching data instead — no real NFHS microdata was ever
present in, or produced by, this environment.

## Methodological decisions

- **Reused, not re-derived, the frozen V2 confounder set and nuisance-model
  specification.** Both extensions inherit the exact 8-variable confounder
  set, survey-weighted LogisticRegression propensity model, and XGBoost
  S-learner outcome model from `notebooks/v2/06`–`07`, via
  `shared/utils.py`, instead of defining new ones.
- **Extension 2 uses a DR-learner (Kennedy, 2020) with a cross-fitted
  `RandomForestRegressor`, not a dedicated causal-forest package.** Keeps
  the extension dependency-free and transparent; see the notebook's own
  "Documentation" section for the full rationale.
- **Extension 2's second-stage cross-fitting folds are independent of the
  Stage-1 nuisance folds**, to avoid indirect leakage between a record's own
  outcome information and its predicted CATE via fold correlation.
- **Extension 2 reuses Notebook 07's exact row-level nuisance predictions
  when locally available** (`outputs/tables/b4_aipw_row_level_nuisance.csv`),
  falling back to an independent re-fit with identical machinery otherwise —
  and prints which path was taken, rather than silently treating the two as
  interchangeable.
- **Extension 3 fits fully independent nuisance models per survey round**,
  rather than one pooled model with a round interaction term, since facility-
  choice/outcome relationships plausibly differ structurally between 2015-16
  and 2019-21, and "round" is not a manipulable treatment for a given
  respondent.
- **Extension 3's change-in-RD confidence interval comes from a paired PSU-
  cluster bootstrap** (`change_b = RD5_reps[b] - RD4_reps[b]`), valid because
  NFHS-4 and NFHS-5 are independent samples — not from subtracting two
  independently reported point estimates or a delta-method formula.
- **Extension 3's harmonization sensitivity analysis (handoff step 29) is
  driven automatically by the variable crosswalk's own verification flags**
  (`state`, `social_group` currently marked unverified for NFHS-4), rather
  than being a separately hand-picked reduced set.

## Known unresolved issues

- Extension 2 has now been run on the real NFHS-5 cohort (n=200,794); see
  its README for final results. Running it uncovered a real bug: a
  `TypeError` in the subgroup-bootstrap loop, caused by how a nullable-dtype
  column (`social_group`/`residence`) represents missing values on the real
  parquet file — not reproduced by the synthetic test data originally used
  to verify the notebook's logic. Fixed with `.fillna(False)` before
  converting to a plain boolean array; reproduced the exact failure on
  synthetic data with a matching dtype to confirm the fix.
- Extension 3 has not been run against real NFHS-5/NFHS-4 data — still
  logic-verified against synthetic data only (see its README's
  "Verification" section and `BLOCKED.md`).
- Extension 3: `state` (v024) is not crosswalked across the 2015-16 → 2019-21
  state/UT boundary changes; excluded from the reduced/sensitivity
  confounder set until that crosswalk is built and verified.
- Extension 3: `social_group` (s116) coding in the NFHS-4 Birth Recode is not
  confirmed identical to NFHS-5's; same treatment as `state` above.
- Extension 3: `wealth_index` (v190) is treated as ordinal within-round only,
  not asserted as a continuously comparable scale across rounds, per DHS's
  own documented cross-round wealth-index methodology revisions.
