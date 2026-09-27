# These CSVs/PNGs are STALE

The files in this folder (`heterogeneity_individual_or_binned_summary.csv`,
`heterogeneity_modifier_summary.csv`, `heterogeneity_distribution.png`,
`heterogeneity_subgroups.png`, `heterogeneity_metadata.json`) were produced
by a **previous version** of `../notebook.ipynb` — a full-cohort,
no-dev/test-split design with impurity-based feature importance.

The notebook has since been repaired (2026-09-27, following an external
implementation review) to use a development/test split, permutation
importance, and a proper joint bootstrap for the headline contrasts. These
files have **not yet been regenerated** under that repaired code.

Do not cite these numbers as current. Re-run `../notebook.ipynb` to
replace them, then update `../README.md` from the fresh output, then
delete this note.
