# Machine Learning and Data Science for Civil Engineering

This repository contains a collection of projects and scripts focused on applying machine learning, data analysis, and computational methods to solve problems in civil and structural engineering.

---

## Table of Contents

1.  [Soil CBR Prediction Projects](#1-soil-cbr-prediction-projects)
    -   [1.1 Random Forest Approach (soils/)](#11-random-forest-approach-soils)
    -   [1.2 XGBoost Approach (X_Gboost/)](#12-xgboost-approach-x_gboost)
2.  [Structural Engineering Simulations (Structural_monitoring/)](#2-structural-engineering-simulations-structural_monitoring)
    -   [2.1 Bridge Moving Load Simulation (bridge_car1/, bridge_car2/)](#21-bridge-moving-load-simulation-bridge_car1-bridge_car2)
    -   [2.2 Skyscraper Seismic Analysis (scy_scapper/)](#22-skyscraper-seismic-analysis-scy_scapper)
    -   [2.3 Structural Health Monitoring Analysis (analysis/)](#23-structural-health-monitoring-analysis-analysis)
3.  [Individual Engineering Scripts and Notebooks](#3-individual-engineering-scripts-and-notebooks)

---

## 1. Soil CBR Prediction Projects

This repository explores two different machine learning approaches to predict the California Bearing Ratio (CBR) of soils, a key parameter for pavement design.

### 1.1 Random Forest Approach (soils/)

-   **Description:** This project uses a `RandomForestRegressor` to predict soil CBR values from index properties like Atterberg limits, grading, and compaction data.
-   **Key Features:**
    -   In-depth analysis of data splitting techniques (random, stratified, sequential).
    -   Model interpretability using Feature Importance and SHAP (SHapley Additive exPlanations).
    -   The primary notebook for this analysis is `soils/soils.ipynb`.
-   **Performance:** Achieves an R-squared (R²) score of approximately 0.65.

### 1.2 XGBoost Approach (X_Gboost/)

-   **Description:** A more structured project that implements an XGBoost regression model to predict soil CBR.
-   **Key Features:**
    -   Well-organized project structure with clear separation of data loading, preprocessing, feature engineering, and model training.
    -   Uses `XGBoost` for potentially higher accuracy.
    -   Scripts for training (`scripts/train_model.py`) and prediction (`scripts/predict.py`) are provided.
-   **Details:** See the `X_Gboost/soil-xgboost-regression/README.md` for full setup and usage instructions.

---

## 2. Structural Engineering Simulations (Structural_monitoring/)

This section contains various structural analysis and simulation projects, primarily using the OpenSees finite element software.

### 2.1 Bridge Moving Load Simulation (bridge_car1/, bridge_car2/)

-   **Description:** Simulates the dynamic response of a simply supported bridge subjected to a moving vehicle load.
-   **Details:**
    -   `bridge_car2.tcl` uses a fine mesh and direct element loading to accurately capture the vertical acceleration at the bridge's midspan.
    -   The output is an acceleration time history (`accello.txt`) that can be used for frequency analysis (FFT) to assess the bridge's dynamic properties.
    -   `bridge_car1/` likely contains a different or earlier version of this simulation.

### 2.2 Skyscraper Seismic Analysis (scy_scapper/)

-   **Description:** This project appears to perform a seismic analysis of a skyscraper.
-   **Details:**
    -   Uses OpenSees (`.tcl` files) and Python scripts (`.py`) for the analysis.
    -   Includes earthquake data (`nairobi_eq.dat`), suggesting a simulation of the structure's response to a specific seismic event.

### 2.3 Structural Health Monitoring Analysis (analysis/)

-   **Description:** This project seems focused on structural health monitoring by comparing the dynamic characteristics of a structure in different states.
-   **Details:**
    -   Contains files for `baseline_frequencies.txt` and `damaged_frequencies.txt`, indicating an analysis of how damage affects a structure's natural frequencies.

---

## 3. Individual Engineering Scripts and Notebooks

The root directory contains several standalone Jupyter notebooks and Python scripts for various engineering tasks:

-   **`3D_+_BoQ.ipynb` & `3D_drawing.ipynb`:** Notebooks related to 3D modeling, drawing, and potentially generating a Bill of Quantities (BoQ).
-   **`structural_with_python.ipynb`:** A notebook exploring structural analysis concepts using Python.
-   **`Three_Moment_Theorem.ipynb`:** A notebook for analyzing indeterminate beams using the Three-Moment Theorem.
-   **`AutoCAD.py` & `ortho.py`:** Python scripts likely related to interacting with AutoCAD or performing geometric/orthographic calculations.

---

**Author:**
Williams Ochieng
August 2025