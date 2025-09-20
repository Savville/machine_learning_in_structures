# Import necessary libraries
import pandas as pd
from sklearn.preprocessing import StandardScaler

def preprocess_data(df):
    """
    Preprocess the soil dataset by handling missing values and scaling features.
    
    Parameters:
    df (pd.DataFrame): The input DataFrame containing the soil data.
    
    Returns:
    pd.DataFrame: The preprocessed DataFrame.
    """
    # Handle missing values
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    categorical_cols = df.select_dtypes(exclude=[np.number]).columns

    # Fill numeric columns with their means
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

    # Fill categorical columns with the most frequent value (mode)
    for col in categorical_cols:
        df[col] = df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else "Unknown")

    # Standardize numerical features
    scaler = StandardScaler()
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

    return df

def split_features_target(df, target_col):
    """
    Split the DataFrame into features and target variable.
    
    Parameters:
    df (pd.DataFrame): The input DataFrame containing the soil data.
    target_col (str): The name of the target column.
    
    Returns:
    X (pd.DataFrame): The features DataFrame.
    y (pd.Series): The target variable Series.
    """
    X = df.drop(columns=[target_col])
    y = df[target_col]
    return X, y