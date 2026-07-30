# Explainable Machine Learning Prediction of Cesarean Section Delivery in India

## Overview

This project aims to develop an explainable machine learning model for predicting whether an institutional delivery in India will result in a Cesarean section. The model is built using data from the National Family Health Survey-5 (NFHS-5) and emphasizes careful feature selection, data preprocessing, and SHAP-based model interpretability to understand the factors associated with Cesarean section delivery.

---

## Objectives

The main objectives of this project are:

- Predict the likelihood of Cesarean section delivery using maternal, socioeconomic, obstetric, antenatal care, and pregnancy-related factors.
- Identify the key predictors associated with Cesarean delivery.
- Build an interpretable machine learning model using SHAP.
- Compare the influence of demographic, clinical, and healthcare-related factors on the prediction.

---

## Dataset

This project uses the **National Family Health Survey-5 (NFHS-5) Birth Recode (BR) dataset**, which is provided through the DHS Program.

The original NFHS-5 dataset is **not included** in this repository because it is distributed under the DHS Program data usage agreement.

Anyone wishing to reproduce this work must request access to the dataset directly from the DHS Program and obtain the necessary permissions before downloading it.

---

## Project Structure

```text
├── data/               # Raw and processed data (ignored from Git)
├── notebooks/          # Jupyter notebooks
├── src/                # Python source code
├── outputs/            # Figures, plots, model outputs
├── docs/               # Proposal and references
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Methodology

The project follows the workflow below:

1. Data acquisition
2. Study population selection (institutional births)
3. Feature selection and variable verification
4. Data cleaning and preprocessing
5. Exploratory Data Analysis (EDA)
6. Feature engineering
7. Machine learning model development
8. Model evaluation
9. SHAP-based explainability
10. Interpretation of results

---

## Project Status

Current progress:

- Dataset loaded and verified
- Institutional births selected
- Feature selection completed
- Data cleaning rules finalized
- Building the final modeling dataset
- Exploratory Data Analysis (EDA)
- Machine learning model development
- SHAP explainability
- Research paper preparation

---

## Technologies

The project is being developed using:

- Python
- Pandas
- NumPy
- Pyreadstat
- Scikit-learn
- XGBoost
- SHAP
- Matplotlib
- Seaborn
- Jupyter Notebook

---

## Data Confidentiality

The NFHS-5 microdata is **not included** in this repository.

To reproduce this project, users must independently obtain access to the NFHS-5 Birth Recode dataset through the DHS Program and comply with all applicable data usage policies and terms of use.

---

## Future Work

The remaining work includes:

- Training multiple machine learning models
- Comparing model performance
- Performing hyperparameter tuning
- Generating SHAP explanations
- Interpreting the most important predictors of Cesarean section delivery
- Preparing the project for publication and reproducibility