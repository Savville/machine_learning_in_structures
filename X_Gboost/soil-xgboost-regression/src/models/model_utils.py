def save_model(model, filename):
    import joblib
    joblib.dump(model, filename)

def load_model(filename):
    import joblib
    return joblib.load(filename)

def train_model(X, y, model_class, **kwargs):
    model = model_class(**kwargs)
    model.fit(X, y)
    return model

def evaluate_model(model, X_test, y_test):
    from sklearn.metrics import mean_squared_error, r2_score
    y_pred = model.predict(X_test)
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    r2 = r2_score(y_test, y_pred)
    return rmse, r2