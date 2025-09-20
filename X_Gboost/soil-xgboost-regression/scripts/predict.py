import pandas as pd
import joblib
import numpy as np
from src.data.data_loader import load_data
from src.models.xgboost_regressor import XGBoostRegressor
from src.config.settings import MODEL_PATH

def make_predictions(input_data):
    # Load the trained model
    model = joblib.load(MODEL_PATH)

    # Make predictions
    predictions = model.predict(input_data)
    return predictions

if __name__ == "__main__":
    # Load the dataset
    data = load_data()

    # Preprocess the data as needed (this should be defined in your preprocessor)
    # Assuming the preprocessor returns a DataFrame ready for prediction
    input_data = data.drop(columns=['CBR.(%)'])  # Adjust based on your target column

    # Make predictions
    predictions = make_predictions(input_data)

    # Output predictions
    print("Predictions:", predictions)