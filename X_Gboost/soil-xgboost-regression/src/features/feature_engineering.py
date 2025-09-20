# Import necessary libraries
import pandas as pd
import numpy as np

def extract_features(df):
    """
    Extract and transform features from the soil dataset.

    Parameters:
    df (pd.DataFrame): The input DataFrame containing soil data.

    Returns:
    pd.DataFrame: A DataFrame with the extracted features.
    """
    # Example feature extraction: creating interaction terms or polynomial features
    df['Gravel_Sand_Interaction'] = df['SoilComposition.Gravel.(%)'] * df['SoilComposition.Sand.(%)']
    df['SiltClay_Sand_Ratio'] = df['SoilComposition.SiltClay.(%)'] / (df['SoilComposition.Sand.(%)'] + 1e-5)  # Avoid division by zero

    # Add more feature engineering steps as needed
    return df

def transform_features(df):
    """
    Transform features for modeling.

    Parameters:
    df (pd.DataFrame): The input DataFrame containing soil data.

    Returns:
    pd.DataFrame: A DataFrame with transformed features.
    """
    # Example transformation: scaling or encoding
    # Here you can add scaling or encoding logic as required
    return df

def prepare_data(df):
    """
    Prepare the dataset for modeling by extracting and transforming features.

    Parameters:
    df (pd.DataFrame): The input DataFrame containing soil data.

    Returns:
    pd.DataFrame: A DataFrame ready for modeling.
    """
    df = extract_features(df)
    df = transform_features(df)
    return df