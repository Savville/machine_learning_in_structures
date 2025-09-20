def calculate_rmse(y_true, y_pred):
    """Calculate the Root Mean Squared Error (RMSE)"""
    return np.sqrt(np.mean((y_true - y_pred) ** 2))

def calculate_r2(y_true, y_pred):
    """Calculate the R² score"""
    ss_total = np.sum((y_true - np.mean(y_true)) ** 2)
    ss_residual = np.sum((y_true - y_pred) ** 2)
    return 1 - (ss_residual / ss_total)

def evaluate_model(y_true, y_pred):
    """Evaluate the model performance and return metrics"""
    rmse = calculate_rmse(y_true, y_pred)
    r2 = calculate_r2(y_true, y_pred)
    return {
        'RMSE': rmse,
        'R²': r2
    }