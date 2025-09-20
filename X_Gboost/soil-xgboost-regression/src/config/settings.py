# Configuration settings for the XGBoost regression project

# File paths
DATA_DIR = '../data/'
RAW_DATA_PATH = DATA_DIR + 'raw/'
PROCESSED_DATA_PATH = DATA_DIR + 'processed/'
RESULTS_PATH = DATA_DIR + 'results/'

# Model parameters
XGBOOST_PARAMS = {
    'objective': 'reg:squarederror',
    'learning_rate': 0.1,
    'max_depth': 6,
    'alpha': 10,
    'n_estimators': 100,
    'random_state': 42
}

# Evaluation metrics
EVALUATION_METRICS = {
    'rmse': 'Root Mean Squared Error',
    'r2': 'R-squared'
}