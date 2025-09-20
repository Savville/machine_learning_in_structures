# Import required libraries
import pandas as pd
from src.data.data_loader import load_data
from src.data.preprocessor import preprocess_data
from src.features.feature_engineering import create_features
from src.models.xgboost_regressor import XGBoostRegressor
from src.evaluation.metrics import evaluate_model
import joblib

def main():
    # Load the dataset
    df = load_data('data/processed/cleaned_MTRD_Soils_data.csv')

    # Preprocess the data
    df_processed = preprocess_data(df)

    # Create features and target variable
    X, y = create_features(df_processed, target_col='CBR.(%)')

    # Initialize and train the XGBoost model
    model = XGBoostRegressor()
    model.train(X, y)

    # Save the trained model
    joblib.dump(model, 'data/results/xgboost_model.pkl')

    # Evaluate the model
    evaluation_results = evaluate_model(model, X, y)
    print(evaluation_results)

if __name__ == "__main__":
    main()