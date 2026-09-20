# Changelog — extensions_work (Extensions 2 & 3)

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

- Neither notebook has been run against real NFHS-5/NFHS-4 data — both are
  logic-verified against synthetic data only (see each extension's README,
  "Verification" section, and `BLOCKED.md`).
- Extension 3: `state` (v024) is not crosswalked across the 2015-16 → 2019-21
  state/UT boundary changes; excluded from the reduced/sensitivity
  confounder set until that crosswalk is built and verified.
- Extension 3: `social_group` (s116) coding in the NFHS-4 Birth Recode is not
  confirmed identical to NFHS-5's; same treatment as `state` above.
- Extension 3: `wealth_index` (v190) is treated as ordinal within-round only,
  not asserted as a continuously comparable scale across rounds, per DHS's
  own documented cross-round wealth-index methodology revisions.
