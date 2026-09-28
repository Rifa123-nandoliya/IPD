# Extension 1 — Quantitative Bias Analysis (QBA)

**Status: illustrative scenario analysis, not evidence-calibrated, and not
publication-ready.** The primary AIPW estimate is held fixed and unedited.
The prevalence/risk-ratio inputs for both unmeasured-confounder classes
remain hypothetical and unsourced — a literature search was attempted
(2026-09-28 audit, see "Literature search" below) but could not be
completed to a citable standard in this environment. **The committed
output CSVs/PNG below are STALE**: they come from a pooled-dilution
version of the code; the current notebook uses a sector-specific dilution
fix (see "2026-09-28 audit" below) that has not yet been re-run on real
data.

## Question and inputs

How would the 28.47 percentage-point, survey-weighted, covariate-standardized
private–public Cesarean risk difference move under specified hypothetical
unmeasured-confounding scenarios? This is an associational contrast, not a
causal facility-switch effect, and this notebook does not change that.

The notebook reads:
- `outputs/final_tables/final_aipw_overall_table.csv` for the frozen primary estimate (no AIPW refitting).
- `data/processed/df_model_v2.parquet` for `facility_type`, `birth_order`, `twin_order`, `sample_weight_normalized` — used only to compute each sector's own survey-weighted later-delivery share.

Run `notebook.ipynb` from inside `extensions_work/01_quantitative_bias/` so its relative import of `../shared/config.py` resolves.

## 2026-09-28 audit — what changed

A statistician audit of the (then-current) notebook found one real
methodological defect and confirmed several things already labeled
correctly:

- **Fixed: pooled → sector-specific dilution.** The notebook already computed
  and *reported* that public and private later-delivery shares differ
  substantially, but still diluted both `p0` and `p1` by one **pooled**
  share. Using the notebook's own numbers, hand-calculation shows this
  pooling roughly **halves** the true sector-specific prevalence gap for
  the "mild" scenario (within-multiparous `p0=0.12`, `p1=0.17`: pooled-share
  delta ≈ 0.029 vs. sector-specific delta ≈ 0.014), and shifts the
  tipping-point ceiling (`p1/p0` as `RR_UY→∞`) from 3.50 down to ≈2.94 —
  much closer to the reference RR of 2.726. **Fixed**: `p0` is now diluted
  by the *public* share and `p1` by the *private* share, independently.
  This is a code-correctness fix, verified by a syntax/logic smoke test
  against synthetic data (not real results — see CHANGELOG) since this
  environment has no NFHS data. **A real re-run is required** to get the
  actual updated scenario/summary/heatmap numbers.
- **Confirmed correct, unchanged:** the twin-order adjustment when deriving
  "delivery order" from `birth_order` (correctly collapses a second/third
  twin back to the same delivery index as the first twin, so a multiple
  birth at a woman's *first* delivery is not miscounted as a later
  delivery); the bias-factor formula's two algebraic forms; the
  no-confounding reproduction check; the "unattainable" tipping-point logic.
- **Literature search attempted, not completed.** See below.

## Method (unchanged in substance from the prior revision)

`BF = [1 + p1 × (RR_UY − 1)] / [1 + p0 × (RR_UY − 1)]` — a specific
binary-confounder, constant-risk-ratio simplification (the same functional
form underlying the E-value's derivation; VanderWeele & Ding, 2017, DOI
10.7326/M16-2607), not a general identification result. `p0`/`p1` are
whole-cohort prevalences (built from within-multiparous assumptions diluted
by each sector's own later-delivery share, for the prior-Cesarean scenario
only). The notebook divides the primary risk ratio by `BF` and translates
the result to a risk difference by holding the primary public risk fixed —
an **illustrative fixed-public-risk translation**, not a separately
estimated corrected risk difference.

## Methodological verdict (see chat/audit record for full reasoning)

**Can this simple bias-factor formula validly modify a standardized,
survey-weighted AIPW association?** Conditionally, not unconditionally. The
formula requires the unmeasured factor to be (a) independent of the eight
measured confounders given exposure, and (b) to have a homogeneous risk
ratio across all their strata and across the two nuisance-model-derived
risk levels the AIPW estimate is built from. Neither assumption is tested
in this notebook. Treat any output as a hypothetical-scenario exploration,
not as a validated correction to the AIPW estimate.

**Is the parity-mix (later-delivery-share) scaling now defensible?** More
defensible than the pooled version, but still an approximation: it assumes
the *within-multiparous* prevalence gap itself (`delta_p`) is comparable
across sectors, and that later-delivery share is the only relevant parity
difference between sectors (twin-order aside). It is a reasonable
illustrative standardization, not an identified bias correction.

**Decision: do not promise publication readiness.** Both the evidence gap
(no sourced parameters) and part of the method's own validity conditions
(independence/homogeneity assumptions) are unresolved.

## Literature search (2026-09-28 audit)

A search for India-specific, sector-stratified prevalence and risk-ratio
estimates for (a) prior Cesarean history among multiparous institutional
deliveries and (b) an obstetric-severity composite was attempted using web
search. **Full-text verification (WebFetch) was blocked for every domain
tested in this environment** (PMC/NCBI, Springer, PLOS, medRxiv, ScienceDirect,
general news sites, and even Wikipedia, as a control) — this is an
environment-level egress restriction, not a judgment that no sources exist.
Search-snippet-only candidates identified (title/URL only; **content not
verified, do not cite without independently checking the source**):

- "Exploring the factors influencing repeated C-section deliveries in India: insights from the National Family Health Survey 2019–21" — *Discover Public Health* (Springer), https://link.springer.com/article/10.1186/s12982-025-01212-2 — population/time period matches this project exactly (NFHS-5); most promising lead, unverified.
- "High prevalence of cesarean section births in private sector health facilities — analysis of DLHS-4 of India" — https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5946478/ — DLHS-4 (not NFHS-5), sector-stratified overall CS rates; unverified whether it reports prior-CS prevalence specifically.
- "Trends in cesarean section rates in private and public facilities in rural eastern Maharashtra, India from 2010-2017" — PLOS ONE, https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0256096 — single-district, not nationally representative; unverified content.
- "Prevalence of Repeat Cesarean Section in a Tertiary Care Hospital" — https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7580334/ — single tertiary hospital, likely not sector-comparative or nationally representative; unverified content.

No candidate for the obstetric-severity composite was found even at the
search-snippet level with a matching population/definition — consistent
with this notebook's own framing of that scenario as an invented,
non-defensible composite rather than a named, literature-tracked condition.

**Outcome:** evidence unavailable to a verifiable standard in this
environment. This is reported as a transparent negative finding, per the
decision rule given for this audit, rather than filled with an unverified
guess.

## Evidence table

| Parameter | Confounder | Classification | Basis |
|---|---|---|---|
| Public/private later-delivery share | Prior Cesarean (dilution) | **Sourced** | Computed directly from `data/processed/df_model_v2.parquet` in-notebook (survey-weighted, twin-order-adjusted); not a literature estimate, a project-internal calculation. |
| `p0` within-multiparous prevalence (0.12) | Prior Cesarean | **Unsupported** | No verified source; one unverified candidate paper identified (NFHS-5 repeated-C-section study) but content not checked. |
| `delta_p` within-multiparous gap (0–0.30 grid) | Prior Cesarean | **Unsupported** | No sector-stratified, parity-restricted, NFHS-5-comparable estimate verified. |
| `RR_UY` (1–8× grid) | Prior Cesarean | **Unsupported** | No verified adjusted RR for repeat-Cesarean-given-prior-Cesarean in a comparable population; candidate hospital-based studies found but not content-verified, and hospital-based ORs/RRs from a single tertiary center would need explicit transportability justification before use here, not silent substitution. |
| `p0`, `delta_p`, `RR_UY` (severity composite) | Obstetric severity | **Unsupported by design** | This is an invented composite, not a named diagnosis; no search for a single matching estimate is expected to succeed, and none was found. |
| Primary AIPW estimate (RD 28.4698pp, RR 2.7260) | n/a — reference, not a QBA parameter | **Sourced** | Frozen, `outputs/final_tables/final_aipw_overall_table.csv`, unedited. |

## Files produced

- `notebook.ipynb`
- `outputs/qba_scenario_results.csv` — deterministic grid, now with per-arm (`p0_whole_cohort`, `p1_whole_cohort`) dilution columns (STALE — pooled-dilution version pending re-run)
- `outputs/qba_summary.csv` — representative scenarios, tipping points, Monte Carlo (parameter-distribution summaries, not confidence intervals) (STALE, pending re-run)
- `outputs/qba_heatmap.png` (STALE, pending re-run)
- `outputs/assumptions_sources.csv` — 15-column schema, every value sourced or literally `hypothetical / unsourced`

## Run checklist (for whoever has real NFHS-5 data access)

1. Confirm `data/processed/df_model_v2.parquet` and `outputs/final_tables/final_aipw_overall_table.csv` are present and unmodified.
2. Run `notebook.ipynb` top to bottom from a clean kernel, from inside its own folder.
3. Confirm Section 2 prints two **different** public/private later-delivery shares (if they print identical values, something regressed).
4. Confirm the QA cell (Section 3) prints both reference-test and no-confounding checks as PASSED.
5. Confirm the E-value cross-check (Section 7) still matches ≈4.90.
6. Re-derive this README's "Regenerated results" numbers directly from the new CSVs (copy-check every number, per the Extension 2 transcription-bug lesson) — do not hand-type from memory.
7. If any assumptions in `assumptions_sources.csv` have since been replaced with real citations, verify each citation resolves (DOI/URL) and matches the claimed population/sector/parity/time before treating results as evidence-calibrated.

## Unresolved decisions for a statistician

1. Is the independence/homogeneity condition for applying this bias-factor formula on top of an AIPW/doubly-robust estimate (rather than a simple adjusted RR) acceptable for this project's purposes, or does it need a formal sensitivity-analysis extension for the AIPW/TMLE setting specifically?
2. Is the sector-specific later-delivery-share dilution (now implemented) an adequate parity-mix standardization, or does it need to also account for other parity-correlated differences between sectors beyond the later-delivery share itself?
3. If no verifiable sourced parameter can be found for prior-Cesarean prevalence/RR in a matching population, should Extension 1 be reported as a purely illustrative/methods-demonstration exercise in the final paper, rather than a sensitivity analysis contributing to the paper's robustness claims?
4. Should the obstetric-severity composite be dropped entirely rather than retained as an invented, unsourced composite?

## Limitations

- Assumes each confounder's effect on the outcome is constant across sectors and across measured-confounder strata (unverified).
- The two confounder classes are treated independently, not jointly.
- Sector-specific dilution corrects one identified defect but does not itself make any parameter sourced.
- The Monte Carlo percentiles are parameter-distribution summaries over arbitrary, unsourced support — not confidence intervals, and they exclude the primary AIPW estimate's own sampling uncertainty.
