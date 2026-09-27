# Extension 1 — Quantitative Bias Analysis (QBA)

**Status: illustrative scenario analysis — NOT evidence-calibrated.** Revised
2026-09-27 following an external implementation review. Fully executed
for real (needs no raw data — runs off already-frozen
`outputs/final_tables/`), but every numeric parameter in Section 2 except
the multiparous fraction is an **unsourced hypothetical placeholder**. Do
not cite the numbers below as a finished, literature-calibrated sensitivity
analysis until real citations replace those placeholders (see
"What still needs to happen").

## What changed in this revision

An external review found the previous version overstated its own rigor.
Fixed here:

- **Structural-zero handling.** Prior Cesarean is *impossible* for first
  births (~41% of the cohort). The previous version applied a
  whole-cohort prevalence gap anyway. This version scopes the
  prior-Cesarean scenario to the multiparous population only, then dilutes
  its whole-cohort effect by the multiparous share — a real, sourced
  number (58.97%, from `notebooks/v2/01`'s own frozen output), not a guess.
- **Overstated framing.** "Robust finding" and "19-29x is biologically
  implausible" are removed. The bias-factor formula is now described
  precisely as a specific binary-U, constant-risk-ratio simplification —
  not "the general E-value framework" — and matching its arithmetic to the
  project's own E-value is now labeled a formula-consistency check, not
  input validation.
- **Tipping-point logic.** Previously could return a large-but-finite
  "tipping" risk ratio even when no finite risk ratio could actually close
  the gap. Now checks the analytic limit (`BF → p1/p0` as `RR_UY → ∞`) and
  reports **"unattainable"** when that limit doesn't reach the reference
  risk ratio.
- **Parameter bounds.** `bias_factor()` now asserts `0 ≤ p0, p1 ≤ 1` and
  `RR_UY > 0`, and rejects out-of-range inputs rather than silently
  computing with them.
- **`assumptions_sources.csv` schema.** Expanded to 15 columns (target
  population, association measure, source title/DOI/year/population,
  transportability note, analyst decision) with literal
  `hypothetical / unsourced` entries — no bare `TODO` disguised as sourced.
- **Heatmap honesty.** The RD=0 contour is only drawn when it actually
  falls inside the plotted grid; otherwise the plot says so explicitly
  instead of implying a tipping point that isn't shown.
- **Monte Carlo framing.** Explicitly labeled as scenario exploration over
  arbitrary, unsourced parameter support — not a confidence statement, and
  it excludes the primary AIPW estimate's own sampling uncertainty.

## Research question

How would the 28.47 pp adjusted private-vs-public Cesarean risk difference
move under stated, hypothetical unmeasured confounding — especially prior
Cesarean history and unmeasured obstetric-severity indications?

## Method

Same bias-factor formula underlying this project's own E-value
(VanderWeele & Ding, 2017, DOI 10.7326/M16-2607), applied as a grid rather
than a single worst-case number, for two confounder classes:

1. **`prior_cesarean_history`** — scoped to the multiparous population
   (`birth_order >= 2`), then diluted by the multiparous fraction
   (0.5897) to get its effect on the whole-cohort estimate.
2. **`obstetric_severity_unmeasured`** — explicitly labeled a single
   hypothetical composite, not a defensible combined diagnosis.

## Results (real, from the frozen primary estimate; parameters still hypothetical)

**Locked reference:** RD = 28.4698 pp, RR = 2.7260 (95% CI 2.6566–2.8035), n = 200,794.

### E-value formula-consistency check

Recomputed **4.8951** vs. the project's reported **4.90** — confirms this
notebook's formula is implemented correctly. **This does not validate any
of the prevalence/risk-ratio inputs used elsewhere in this notebook.**

### Representative scenarios (all parameters hypothetical)

| Confounder | Scenario | Δp (whole-cohort) | RR_UY | Adjusted RD (fixed-r0 translation) |
|---|---|---:|---:|---:|
| Prior Cesarean (multiparous-scoped) | Mild | +2.9 pp | 2.0× | 27.26 pp |
| Prior Cesarean (multiparous-scoped) | Moderate | +7.1 pp | 4.0× | 21.77 pp |
| Prior Cesarean (multiparous-scoped) | Strong | +11.8 pp | 6.0× | 14.83 pp |
| Obstetric severity (hypothetical composite) | Mild | +3 pp | 1.5× | 27.83 pp |
| Obstetric severity (hypothetical composite) | Moderate | +8 pp | 2.5× | 24.12 pp |
| Obstetric severity (hypothetical composite) | Strong | +15 pp | 3.5× | 17.76 pp |

### Tipping points (now correctly checked for attainability)

- **Prior Cesarean:** at the most extreme tested prevalence gap, would
  need **RR_UY ≈ 32.5** to bring the gap to zero — attainable within the
  (very wide) search range, but far outside any plausible single-confounder
  effect size.
- **Obstetric severity:** similarly, **RR_UY ≈ 28.9** at its most extreme
  tested gap.

### Monte Carlo (illustrative scenario exploration, not a confidence statement)

| Confounder | Median adjusted RD | Range (over stated support) | % draws RD > 0 |
|---|---:|---|---:|
| Prior Cesarean (multiparous-scoped) | 21.34 pp | [10.22, 28.28] | 100% |
| Obstetric severity (hypothetical) | 23.36 pp | [13.50, 28.35] | 100% |

These percentages describe the **chosen parameter support**, not
statistical confidence or clinical plausibility, and exclude the AIPW
estimate's own sampling uncertainty.

### Headline framing (revised)

Under the tested hypothetical parameter ranges, the adjusted gap
attenuates but does not reach zero within plausible-looking scenarios, and
the exact tipping points require confounder strengths (RR_UY ≈ 29-33×)
that are large. **This is not evidence that no such confounder exists** —
it describes how the estimate moves under stated, unsourced assumptions.

## ⚠️ What still needs to happen before this is publication-ready

Every row in `assumptions_sources.csv` currently reads
`hypothetical / unsourced`. Before reporting these results as final:

1. Find published, ideally India-specific, sector-stratified estimates for
   each parameter, matching NFHS-5's population, institutional-delivery
   denominator, parity restriction, and time period — record the exact
   citation (title, authors, year, DOI/URL) and whether it reports a
   crude RR, adjusted RR, odds ratio, or hazard ratio (do not silently
   substitute OR for RR).
2. Update `CONFOUNDER_SPECS` (notebook Section 2) and
   `assumptions_sources.csv`'s columns — no other code changes are needed.
3. Consider separating `obstetric_severity_unmeasured` into named
   individual conditions with their own sourced parameters, rather than
   one invented composite.
4. Re-run; the grid, Monte Carlo, and tipping-point numbers update
   automatically.

## Inputs

- `outputs/final_tables/final_aipw_overall_table.csv` (frozen primary estimate)
- `notebooks/v2/01_v2_data_audit_and_cohort.ipynb` (source of the multiparous fraction and the prior-Cesarean-unmeasured documentation)
- `notebooks/v2/07_aipw_primary_analysis.ipynb`, `notebooks/v2/09_sensitivity_analyses.ipynb` (methodological context, E-value)

## Files produced

- `notebook.ipynb`
- `outputs/qba_scenario_results.csv` — full deterministic grid (550 rows), now with `dilution_factor`/whole-cohort-vs-within-target-population columns
- `outputs/qba_summary.csv` — representative scenarios, tipping points (with attainability status), Monte Carlo summary
- `outputs/qba_heatmap.png` — bias-adjusted RD across the grid, only draws the RD=0 contour when it's inside the plotted domain
- `outputs/assumptions_sources.csv` — 15-column schema, every parameter labeled sourced or `hypothetical / unsourced`

## QA / interpretation checks

- Reference tests pass: `BF(p0,p0,rr)=1`, `BF(p0,p1,1)=1`, out-of-range `p0`/`p1` rejected.
- Reproduces the primary estimate exactly at no unmeasured confounding.
- E-value formula-consistency check passes (4.8951 vs. 4.90) — explicitly labeled as a formula check, not input validation.
- No sentence states unmeasured confounding is absent or gives an empirical probability that the true RD exceeds zero.

## Limitations

- The multiparous-dilution correction assumes a similar parity mix across
  sectors (not verified here) — a real sector-specific parity composition
  would refine this further.
- Assumes each confounder's effect on the outcome is constant across
  sectors (standard simplifying assumption for this bias-factor method).
- The two confounder classes are treated independently, not jointly.
- As stated throughout: every numeric parameter besides the multiparous
  fraction is a hypothetical placeholder pending a real literature search.
