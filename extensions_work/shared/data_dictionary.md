# Data dictionary — Extensions 2 & 3

Scope: only the variables used by this teammate's two extensions
(`02_causal_heterogeneity/`, `03_nfhs4_nfhs5_temporal/`). For the full V2
variable dictionary see `data/processed/variable_dictionary_v2.csv`,
produced by `notebooks/v2/01_v2_data_audit_and_cohort.ipynb`.

## Inherited from the frozen V2 pipeline (do not redefine)

| Variable | Role | Notes |
|---|---|---|
| `facility_type` | exposure source | `public`/`private`/`other`; both extensions restrict to `public`/`private` (`exposure`: private=1, public=0), matching notebooks/v2/06–07. |
| `csection` | outcome | 0/no, 1/yes. |
| `respondent_id` | grouping key | Used for respondent-grouped cross-fitting (`StratifiedGroupKFold`), never split across train/held-out. |
| `cluster_number` | PSU | Used for PSU-cluster bootstrap, resampled within `sample_stratum_v022`. |
| `sample_stratum_v022` | sampling stratum | Bootstrap resampling stratum. |
| `sample_weight_normalized` | survey weight | `sample_weight / 1,000,000`. Applied as an outer multiplier on AIPW pseudo-outcomes, never inside the propensity term. |

**Primary confounder set (8 variables, identical to notebooks/v2/06–07):**
`birth_order`, `twin_order`, `wealth_index`, `education_years`, `residence`,
`religion`, `social_group`, `state`. See `shared/config.py` for the exact
list objects (`NUMERIC_CONFOUNDERS`, `CATEGORICAL_CONFOUNDERS`).

## Extension 2 — pre-specified effect-modifier (moderator) set

Pre-exposure variables available before facility choice/delivery, chosen
**before** inspecting any heterogeneity result (handoff Extension 2, step 15).
None of these duplicate the confounder set used inside the nuisance models
(a variable can be both a confounder and a candidate moderator; that is
expected and not a leakage issue — what is forbidden is a post-treatment
or post-outcome variable as a moderator).

| Variable | Type | Why it's a plausible effect modifier |
|---|---|---|
| `wealth_index` | ordinal (1–5) | Ability to pay may change how strongly facility sector predicts C-section. |
| `education_years` | continuous | Proxy for health literacy / bargaining power with providers. |
| `residence` | binary (urban/rural) | Private-sector supply and competition differ sharply by residence. |
| `state` | categorical | State-level regulation, private-sector penetration, and obstetric norms vary widely. |
| `social_group` | categorical | Documented equity dimension in the base project (NFHS social-group categories). |
| `maternal_age` | continuous | **Sensitivity/exploratory only** — same age-at-interview-vs-age-at-birth caveat as notebooks/v2/06–07; not part of the primary moderator set, may be reported as a secondary check. |
| `twin_order` | categorical | Already a confounder; retained as a candidate modifier since plurality could plausibly interact with sector-driven C-section risk. |

Explicitly **excluded** as moderators (same reasoning as the confounder
exclusions in notebook 06): all ANC/service-utilization variables (they are
mediators, not pre-exposure), `facility_type` itself, and any `risk_stratum_*`
/ `first_birth` derived column (these are V2-derived stratifiers built from
the outcome's target population, not baseline moderators for an
outcome-blind heterogeneity search).

## Extension 3 — NFHS-4 ↔ NFHS-5 crosswalk variables

Built and documented in `03_nfhs4_nfhs5_temporal/notebook.ipynb` itself
(`nfhs4_nfhs5_variable_crosswalk.csv`). Summarized here for quick reference;
the notebook's crosswalk table is the source of truth.

| Harmonized name | NFHS-5 source | NFHS-4 source | Harmonization note |
|---|---|---|---|
| `facility_type` (exposure) | `m15` (recoded) | `m15` (recoded) | Same DHS place-of-delivery variable exists in both rounds; recoding logic re-applied identically. |
| `csection` (outcome) | `m17` | `m17` | Present in both rounds. |
| `birth_order` | `bord` | `bord` | Direct match. |
| `twin_order` | `b0` | `b0` | Direct match. |
| `wealth_index` | `v190` | `v190` | Direct match; wealth-index construction methodology has known cross-round differences documented by DHS — flagged, not silently assumed comparable. |
| `education_years` | `v133` | `v133` | Direct match; special code 97 → missing in both. |
| `residence` | `v025` | `v025` | Direct match. |
| `religion` | `v130` | `v130` | Direct match. |
| `social_group` | `s116` | `s116` (if present in the NFHS-4 recode; verify before use) | **TODO in notebook**: confirm `s116` exists identically in the NFHS-4 Birth Recode before treating as harmonized; if absent, drop from the pooled confounder set and document the reduced set. |
| `state` | `v024` | `v024` | Direct match; state/UT boundary changes between 2015–16 and 2019–21 (e.g. new UTs) must be harmonized to a common coding — handled explicitly in the notebook's crosswalk step, not assumed away. |
| `respondent_id` | `caseid` | `caseid` | Round-specific; never pooled across rounds as if the same respondent. |
| `cluster_number` / `sample_stratum_v022` | `v001` / `v022` | `v001` / `v022` | Round-specific design variables; bootstrap resampling is done within round, not pooled across rounds. |
| `sample_weight_normalized` | `v005 / 1e6` | `v005 / 1e6` | Each round uses its own round-specific weight; never mixed. |
| `survey_round` | n/a (derived) | n/a (derived) | New column: `"NFHS-4"` / `"NFHS-5"`, used as the time indicator in the pooled time-by-sector estimand. |

Any variable that cannot be harmonized credibly (per the handoff's step 22)
is dropped from the pooled confounder set rather than guessed at, and the
drop is logged in the notebook and in `CHANGELOG.md`.
