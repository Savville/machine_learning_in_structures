class XGBoostRegressor:
    def __init__(self, params=None):
        import xgboost as xgb
        self.params = params if params is not None else {
            'objective': 'reg:squarederror',
            'eval_metric': 'rmse',
            'learning_rate': 0.1,
            'max_depth': 6,
            'n_estimators': 100,
            'random_state': 42
        }
        self.model = xgb.XGBRegressor(**self.params)

    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train)

    def predict(self, X_test):
        return self.model.predict(X_test)

    def save_model(self, file_path):
        self.model.save_model(file_path)

    def load_model(self, file_path):
        import xgboost as xgb
        self.model = xgb.XGBRegressor()
        self.model.load_model(file_path)