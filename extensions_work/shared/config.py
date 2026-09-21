"""Shared local configuration for the extensions_work notebooks.

No secrets or data live in this file -- only paths and constants shared by
Extension 2 (causal heterogeneity) and Extension 3 (NFHS-4/NFHS-5 temporal
comparison). Local NFHS file locations can be overridden with environment
variables so that no absolute personal-computer path is ever hard-coded
into a notebook cell (per the handoff's "Definition of done" rule).

Usage from a notebook (e.g. extensions_work/02_causal_heterogeneity/notebook.ipynb):

    import sys
    from pathlib import Path
    sys.path.append(str(Path("../shared").resolve()))
    import config
    import utils
"""
import os
from pathlib import Path

# extensions_work/shared/config.py -> shared -> extensions_work -> repo root
REPO_ROOT = Path(__file__).resolve().parents[2]
EXTENSIONS_ROOT = Path(__file__).resolve().parents[1]

# --- Existing frozen V2 pipeline data/outputs (read-only reuse; never modified) ---
V2_PROCESSED_DATA_PATH = Path(
    os.environ.get("IPD_V2_PROCESSED_PATH", REPO_ROOT / "data" / "processed" / "df_model_v2.parquet")
)
V2_METADATA_DIR = REPO_ROOT / "outputs" / "metadata"
V2_FINAL_TABLES_DIR = REPO_ROOT / "outputs" / "final_tables"

# --- NFHS-4 inputs for Extension 3 -- never checked into version control ---
# Point IPD_NFHS4_BIRTH_RECODE_PATH at your own authorized local NFHS-4 Birth
# Recode copy (raw .DTA/.sav, or however you received it), or edit the
# default below. Nothing under data/ is tracked by git (see .gitignore).
NFHS4_BIRTH_RECODE_PATH = Path(
    os.environ.get("IPD_NFHS4_BIRTH_RECODE_PATH", REPO_ROOT / "data" / "raw" / "nfhs4_birth_recode.DTA")
)
NFHS4_PROCESSED_DATA_PATH = Path(
    os.environ.get("IPD_NFHS4_PROCESSED_PATH", REPO_ROOT / "data" / "processed" / "df_model_nfhs4.parquet")
)

# --- extensions_work output locations (auto-created; safe aggregate outputs only) ---
EXT02_DIR = EXTENSIONS_ROOT / "02_causal_heterogeneity"
EXT02_OUTPUTS_DIR = EXT02_DIR / "outputs"
EXT03_DIR = EXTENSIONS_ROOT / "03_nfhs4_nfhs5_temporal"
EXT03_OUTPUTS_DIR = EXT03_DIR / "outputs"

for _d in (EXT02_OUTPUTS_DIR, EXT03_OUTPUTS_DIR):
    _d.mkdir(parents=True, exist_ok=True)

# --- Constants inherited from the frozen V2 protocol (notebooks/v2/06, 07) ---
# These must stay identical to the frozen notebooks unless a documented,
# pre-specified harmonization change is required (see Extension 3's README).
RANDOM_STATE = 42
N_FOLDS = 5
CLIP_EPS = 1e-6
# TEMPORARY: lowered from 500 for a faster test run on slower hardware.
# Set this back to 500 before treating any results as final -- it only
# affects how precise/stable the bootstrap confidence intervals are, not
# the underlying point estimates (risk differences/ratios, top modifiers).
N_BOOTSTRAP = 100
BOOTSTRAP_SEED = 42

# Primary NFHS-5 confounder set -- identical to notebooks/v2/06_propensity_
# overlap_diagnostics.ipynb and notebooks/v2/07_aipw_primary_analysis.ipynb.
NUMERIC_CONFOUNDERS = ["birth_order", "wealth_index", "education_years"]
CATEGORICAL_CONFOUNDERS = ["residence", "religion", "social_group", "twin_order", "state"]
CONFOUNDER_COLS = NUMERIC_CONFOUNDERS + CATEGORICAL_CONFOUNDERS

EXPECTED_V2_ROW_COUNT = 201311
EXPECTED_ANALYTIC_ROW_COUNT = 200794  # public + private only, excludes 'other'
