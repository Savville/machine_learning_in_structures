import pandas as pd

def load_data(file_path):
    """
    Load the soil dataset from a CSV file and return it as a DataFrame.
    
    Parameters:
    file_path (str): The path to the CSV file containing the soil data.
    
    Returns:
    pd.DataFrame: A DataFrame containing the loaded soil data.
    """
    try:
        data = pd.read_csv(file_path)
        print(f"Data loaded successfully from {file_path}.")
        return data
    except Exception as e:
        print(f"Error loading data from {file_path}: {e}")
        return None