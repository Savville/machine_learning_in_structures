# Predicting Soil CBR Values using Machine Learning

This project develops a machine learning model to predict the California Bearing Ratio (CBR) of soils from their index properties, aiming to accelerate preliminary pavement design decisions.

## Machine Learning Process

The workflow is centered around a `RandomForestRegressor` model and involves the following steps:

1.  **Data Preprocessing:** The `cleaned_MTRD_Soils_data.csv` dataset is used. The process includes cleaning the data, imputing missing values, and standardizing numerical features using `StandardScaler`.

2.  **Modeling:** A Random Forest model is trained to predict the `CBR.4daysSoak.(%)` value based on soil properties like Atterberg limits, grading, and compaction characteristics.

3.  **Evaluation:** The model's performance is assessed using R-squared (R²) and Root Mean Squared Error (RMSE). It achieves an R² score of approximately 0.65.

4.  **Data Splitting Analysis:** The project analyzes the impact of different data splitting strategies (random, stratified, sequential) on model performance to ensure robustness and generalizability.

5.  **Interpretability:** Model predictions are explained using:
    - **Feature Importance:** To identify the most influential soil properties.
    - **SHAP (SHapley Additive exPlanations):** To understand how each feature contributes to the predictions.

## Key Results

- The model can predict CBR values with an R² of ~0.65.
- `Swell.(%)` is identified as the most significant predictor, followed by `AtterbergLimits.PI.%` and various grading properties.

## How to Run

The machine learning pipeline can be executed by running the `soils.ipynb` notebook for the core analysis or the `data_splits/modified_model.py` script for a more detailed analysis of data splitting techniques.