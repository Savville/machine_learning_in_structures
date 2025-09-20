import pytest
import pandas as pd
from src.models.xgboost_regressor import XGBoostRegressor

def test_xgboost_regressor_training():
    # Create a sample DataFrame for testing
    data = {
        'feature1': [1, 2, 3, 4, 5],
        'feature2': [5, 4, 3, 2, 1],
        'CBR.(%)': [10, 20, 30, 40, 50]
    }
    df = pd.DataFrame(data)

    # Split the data into features and target
    X = df.drop('CBR.(%)', axis=1)
    y = df['CBR.(%)']

    # Initialize the XGBoostRegressor
    model = XGBoostRegressor()

    # Train the model
    model.train(X, y)

    # Check if the model is trained
    assert model.model is not None, "Model should be trained and not None"

def test_xgboost_regressor_prediction():
    # Create a sample DataFrame for testing
    data = {
        'feature1': [1, 2, 3],
        'feature2': [3, 2, 1]
    }
    df = pd.DataFrame(data)

    # Initialize the XGBoostRegressor
    model = XGBoostRegressor()

    # Train the model with dummy data
    train_data = {
        'feature1': [1, 2, 3, 4, 5],
        'feature2': [5, 4, 3, 2, 1],
        'CBR.(%)': [10, 20, 30, 40, 50]
    }
    train_df = pd.DataFrame(train_data)
    X_train = train_df.drop('CBR.(%)', axis=1)
    y_train = train_df['CBR.(%)']
    model.train(X_train, y_train)

    # Make predictions
    predictions = model.predict(df)

    # Check if predictions are made
    assert len(predictions) == len(df), "Number of predictions should match the number of input samples"