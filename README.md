# Explainable Machine Learning Prediction of Cesarean Section Delivery in India

## Overview

This project develops an explainable machine learning model to predict whether an institutional delivery in India will result in a Cesarean section using data from the National Family Health Survey-5 (NFHS-5). The project emphasizes careful feature selection, rigorous data preprocessing, exploratory data analysis, and SHAP-based model interpretability to identify the factors associated with Cesarean section delivery.

---

## Objectives

The main objectives of this project are:

- Predict the likelihood of Cesarean section delivery using maternal, socioeconomic, obstetric, antenatal care, and pregnancy-related factors.
- Identify the most important predictors associated with Cesarean section delivery.
- Develop interpretable machine learning models using SHAP.
- Compare the influence of demographic, clinical, and healthcare-related factors on prediction performance.

---

## Dataset

This project uses the **National Family Health Survey-5 (NFHS-5) Birth Recode (BR) dataset**, provided through the DHS Program.

The original NFHS-5 dataset is **not included** in this repository because it is distributed under the DHS Program data usage agreement.

Anyone wishing to reproduce this work must request access directly from the DHS Program and comply with all applicable data usage policies.

---

## Project Structure

```text
.
├── data/
│   ├── raw/                  # Original NFHS-5 data (ignored)
│   └── processed/            # Processed datasets (ignored)
├── notebooks/
│   ├── 01_data_preparation.ipynb
│   └── 02_exploratory_data_analysis.ipynb
├── src/
├── outputs/
├── docs/
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Methodology

The project follows the workflow below:

1. Data acquisition
2. Study population selection (institutional deliveries)
3. Manual feature selection
4. Variable verification
5. Target leakage analysis
6. Data cleaning and preprocessing
7. Exploratory Data Analysis (EDA)
8. Statistical analysis
9. Correlation and missing-value analysis
10. Machine learning model development
11. Model evaluation
12. SHAP-based explainability
13. Interpretation of results

---

## Project Progress

### Completed

- Project definition
- NFHS-5 dataset loading and metadata verification
- Institutional delivery selection
- Manual feature selection
- Target leakage identification and removal
- Variable verification
- Data cleaning and preprocessing
- Anthropometric variable cleaning
- ANC variable cleaning
- Final predictor selection
- Final modeling dataset creation
- Dataset verification
- Data type conversion
- Processed Parquet dataset generation
- Exploratory Data Analysis (EDA)
- Statistical comparison of numeric variables
- Statistical comparison of categorical variables
- Correlation analysis
- Missing-value analysis

### Current Status

The data preparation and exploratory data analysis phases have been completed.

The next phase will focus on:

- Machine learning preprocessing
- Baseline model development
- Tree-based model development
- Model evaluation
- Hyperparameter tuning
- SHAP-based explainability

---

## Technologies

The project is being developed using:

- Python
- Pandas
- NumPy
- Pyreadstat
- PyArrow
- Matplotlib
- Seaborn
- SciPy
- Scikit-learn
- XGBoost
- SHAP
- Jupyter Notebook

---

## Data Confidentiality

The NFHS-5 microdata is **not included** in this repository.

Users wishing to reproduce this project must independently obtain access to the NFHS-5 Birth Recode dataset through the DHS Program and comply with all applicable data usage policies.

---

## Future Work

The remaining work includes:

- Machine learning preprocessing
- Logistic Regression baseline model
- Decision Tree model
- Random Forest model
- XGBoost model
- Hyperparameter tuning
- Model evaluation and comparison
- SHAP explainability
- Final model interpretation
- Research paper preparation