# Explainable Machine Learning Prediction of Cesarean Section Delivery in India

## Overview

This project develops an explainable machine learning model to predict whether an institutional delivery in India will result in a Cesarean section using data from the National Family Health Survey-5 (NFHS-5).

The project emphasizes careful feature selection, prevention of target leakage, respondent-level data splitting, exploratory data analysis, model comparison, hyperparameter tuning, and SHAP-based explainability.

The final selected model was a tuned XGBoost classifier.

## Objectives

The main objectives of this project are:

- Predict the likelihood of Cesarean section delivery using maternal, socioeconomic, obstetric, antenatal care, and pregnancy-related factors.
- Identify the most important predictors associated with Cesarean section delivery.
- Compare linear and tree-based machine learning models.
- Prevent respondent-level data leakage during model development.
- Optimize the strongest candidate models using grouped cross-validation.
- Explain global and individual model predictions using SHAP.
- Examine how healthcare, maternal, socioeconomic, and reproductive factors influence model predictions.

## Dataset

This project uses the **National Family Health Survey-5 (NFHS-5) Birth Recode dataset**, provided through the DHS Program.

The original NFHS-5 microdata is not included in this repository because it is distributed under the DHS Program data usage agreement.

Anyone wishing to reproduce this project must independently request access from the DHS Program and comply with all applicable data usage policies.

After restricting the analysis to institutional deliveries, the final modeling dataset contained:

- **201,311 delivery records**
- **158,429 unique respondents**
- **36 predictor variables**
- **22.23% Cesarean deliveries**
- **77.77% vaginal deliveries**

## Project Structure

```text
.
├── data/
│   ├── raw/                              # Original NFHS-5 data (ignored)
│   └── processed/                        # Processed datasets (ignored)
├── notebooks/
│   ├── 01_data_preparation.ipynb
│   ├── 02_exploratory_data_analysis.ipynb
│   ├── 03_machine_learning_preprocessing.ipynb
│   ├── 04_baseline_machine_learning_models.ipynb
│   ├── 05_hyperparameter_tuning.ipynb
│   └── 06_shap_explainability.ipynb
├── artifacts/                            # Saved models and analysis objects (ignored)
├── outputs/                              # Figures and report-ready outputs
├── src/                                  # Reusable source code
├── docs/                                 # Project documentation and references
├── requirements.txt
├── README.md
└── .gitignore
```

## Methodology

The project follows the workflow below:

1. Data acquisition
2. Metadata inspection and variable verification
3. Study population selection
4. Manual predictor selection
5. Target leakage analysis
6. DHS special-code cleaning
7. Final modeling dataset creation
8. Exploratory Data Analysis
9. Statistical comparison of predictors
10. Correlation and missing-value analysis
11. Respondent-level train-test splitting
12. Machine learning preprocessing
13. Baseline model development
14. Hyperparameter tuning with grouped cross-validation
15. Final model comparison and selection
16. SHAP-based global and local explainability
17. Calibration and threshold analysis
18. Final interpretation and reporting

## Data Preparation

The analysis was restricted to institutional deliveries using the NFHS-5 place-of-delivery variable.

Variables were manually reviewed using:

- DHS variable labels
- DHS value labels
- Observed values
- Missing-value patterns
- Special response codes
- Timing relative to delivery
- Potential target leakage

Variables describing events occurring during or after delivery were excluded from the predictor set.

The final dataset was saved locally as:

```text
data/processed/df_model_v1.parquet
```

This file is ignored by Git and is not distributed through the repository.

## Exploratory Data Analysis

The EDA phase included:

- Cesarean outcome distribution
- Maternal demographic analysis
- Socioeconomic analysis
- Obstetric-history analysis
- Maternal BMI analysis
- ANC timing and visit analysis
- ANC-provider analysis
- ANC-quality analysis
- Pregnancy counselling analysis
- Pregnancy-complication analysis
- Facility-type analysis
- Mann-Whitney U tests for numeric predictors
- Chi-square tests for categorical predictors
- Effect-size analysis
- Spearman correlation analysis
- Missing-value analysis

The EDA showed that Cesarean delivery was associated with several maternal, socioeconomic, reproductive, antenatal-care, and facility-related characteristics.

## Machine Learning Preprocessing

The final 36 predictors were grouped into:

- 10 numeric features
- 5 categorical features
- 21 binary features

Two preprocessing pipelines were created.

### Linear-model preprocessing

Used for Logistic Regression:

- Median imputation
- Numeric missing-value indicators
- Standard scaling
- One-hot encoding

### Tree-model preprocessing

Used for Decision Tree, Random Forest, and XGBoost:

- Median imputation
- Numeric missing-value indicators
- One-hot encoding
- No numeric scaling

The original 36 predictors expanded to **99 transformed features** after encoding and missing-indicator creation.

A respondent-level train-test split was used to ensure that multiple birth records from the same respondent were not divided between training and test sets.

Final split:

- Training set: **161,048 records**
- Test set: **40,263 records**
- Respondent overlap: **0**

## Baseline Models

The following baseline classifiers were trained:

- Logistic Regression
- Decision Tree
- Random Forest
- XGBoost

### Baseline performance

| Model | Accuracy | Precision | Recall | F1-score | ROC-AUC | PR-AUC |
|---|---:|---:|---:|---:|---:|---:|
| XGBoost | 0.7259 | 0.4325 | 0.7479 | 0.5481 | 0.8035 | 0.5333 |
| Logistic Regression | 0.7383 | 0.4443 | 0.7071 | 0.5457 | 0.7943 | 0.5109 |
| Random Forest | 0.7964 | 0.5866 | 0.2846 | 0.3833 | 0.7904 | 0.5040 |
| Decision Tree | 0.7229 | 0.3780 | 0.3821 | 0.3800 | 0.6012 | 0.2818 |

XGBoost achieved the strongest overall baseline performance.

## Hyperparameter Tuning

The three strongest candidate models were tuned:

- Logistic Regression
- Random Forest
- XGBoost

Hyperparameter tuning used:

- `GridSearchCV` for Logistic Regression
- `RandomizedSearchCV` for Random Forest
- `RandomizedSearchCV` for XGBoost
- `StratifiedGroupKFold` with three folds
- Respondent ID as the grouping variable
- PR-AUC (`average_precision`) as the primary optimization metric

### Best cross-validated PR-AUC

| Model | Best CV PR-AUC |
|---|---:|
| XGBoost | 0.5291 |
| Random Forest | 0.5204 |
| Logistic Regression | 0.5085 |

### Tuned model performance

| Model | Test Accuracy | Precision | Recall | F1-score | ROC-AUC | PR-AUC |
|---|---:|---:|---:|---:|---:|---:|
| XGBoost | 0.7248 | 0.4313 | 0.7471 | 0.5469 | 0.8033 | 0.5330 |
| Random Forest | 0.7383 | 0.4444 | 0.7101 | 0.5467 | 0.8002 | 0.5262 |
| Logistic Regression | 0.7384 | 0.4444 | 0.7073 | 0.5459 | 0.7943 | 0.5108 |

Random Forest showed the largest improvement after tuning, particularly in Cesarean recall.

XGBoost remained the strongest overall model based on Recall, F1-score, ROC-AUC, PR-AUC, and generalization performance.

## Final Model

The tuned XGBoost model was selected as the final predictive model.

### Final XGBoost performance

| Metric | Value |
|---|---:|
| Training accuracy | 0.7352 |
| Test accuracy | 0.7248 |
| Precision | 0.4313 |
| Recall | 0.7471 |
| F1-score | 0.5469 |
| ROC-AUC | 0.8033 |
| PR-AUC | 0.5330 |
| Best cross-validated PR-AUC | 0.5291 |

The small difference between training and test performance suggests good generalization with limited overfitting.

## SHAP Explainability

SHAP analysis was performed using a stratified sample of **5,000 unseen test observations**.

The SHAP sample preserved the test-set outcome distribution:

- Vaginal delivery: 77.78%
- Cesarean delivery: 22.22%

Global and local explanations were generated using:

- SHAP global bar plots
- SHAP beeswarm plots
- Original-variable importance aggregation
- Numeric dependence plots
- Individual waterfall plots
- High-risk and low-risk case comparisons
- False-positive and false-negative explanations

### Most influential original predictors

The leading predictors identified by SHAP were:

1. Facility type
2. Total children ever born
3. Maternal BMI
4. Wealth index
5. Age at first birth
6. Doctor-provided ANC
7. Years of education
8. Number of ANC visits
9. Social group
10. Preceding birth interval

Facility type was the most influential predictor in the final XGBoost model.

SHAP findings describe associations learned by the model and must not be interpreted as proof of causation.

## Technologies

The project uses:

- Python
- Pandas
- NumPy
- Pyreadstat
- PyArrow
- SciPy
- Scikit-learn
- XGBoost
- SHAP
- Joblib
- Matplotlib
- Seaborn
- Jupyter Notebook

## Reproducibility

To reproduce the project:

1. Clone the repository.
2. Create and activate a Python virtual environment.
3. Install the required packages.
4. Obtain the NFHS-5 Birth Recode dataset from the DHS Program.
5. Place the dataset inside the local `data/raw/` directory.
6. Run the notebooks in numerical order.

```bash
pip install -r requirements.txt
```

The original data, processed datasets, trained models, and serialized artifacts are not included in the repository.

## Data Confidentiality

NFHS-5 microdata is not included in this repository.

Users must independently obtain access through the DHS Program and comply with its data usage agreement.

The following are excluded from version control:

- Raw NFHS-5 data
- Processed record-level datasets
- Variable-mapping CSV files generated locally
- Serialized preprocessing objects
- Trained model files
- SHAP value arrays
- Other potentially large derived artifacts

## Project Progress

### Completed

- Project definition
- NFHS-5 dataset loading
- Metadata inspection
- Institutional-delivery selection
- Manual feature selection
- Target-leakage analysis
- DHS special-code cleaning
- Final modeling dataset creation
- Exploratory Data Analysis
- Statistical testing
- Correlation analysis
- Missing-value analysis
- Respondent-level train-test split
- Machine learning preprocessing
- Baseline model development
- Model evaluation
- Hyperparameter tuning
- Overfitting assessment
- Final model selection
- SHAP global explainability
- SHAP local explainability
- High-risk and low-risk case analysis
- False-positive and false-negative analysis

### Remaining Work

- Probability calibration
- Classification-threshold optimization
- Final results discussion
- Limitations and future-work analysis
- Research paper preparation
- Final presentation and project documentation