import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import os

# Load your soil data
df = pd.read_csv('C:\\Users\\User\\Desktop\\machine_learning\\soils\\cleaned_MTRD_Soils_data.csv')

# Create data splits directory
os.makedirs('data_splits', exist_ok=True)

# Method 1: Random Split (80/20)
def create_random_split():
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42, stratify=None)
    
    # Save to separate files
    train_df.to_csv('data_splits/soil_train_random.csv', index=False)
    test_df.to_csv('data_splits/soil_test_random.csv', index=False)
    
    print(f"Random split created:")
    print(f"Training: {len(train_df)} samples")
    print(f"Testing: {len(test_df)} samples")

# Method 2: Stratified Split by CBR Range
def create_stratified_split():
    # Create CBR bins for stratification
    df['CBR_Bin'] = pd.cut(df['CBR.4daysSoak.(%)'], 
                          bins=[0, 10, 30, 100, float('inf')], 
                          labels=['Low', 'Medium', 'High', 'Very_High'])
    
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42, 
                                        stratify=df['CBR_Bin'])
    
    # Remove the temporary column
    train_df = train_df.drop('CBR_Bin', axis=1)
    test_df = test_df.drop('CBR_Bin', axis=1)
    
    # Save files
    train_df.to_csv('data_splits/soil_train_stratified.csv', index=False)
    test_df.to_csv('data_splits/soil_test_stratified.csv', index=False)
    
    print(f"Stratified split created:")
    print(f"Training: {len(train_df)} samples")
    print(f"Testing: {len(test_df)} samples")

# Method 3: Sequential Split (good for time-series or ordered data)
def create_sequential_split():
    # First 80% for training, last 20% for testing
    split_point = int(0.8 * len(df))
    
    train_df = df.iloc[:split_point].copy()
    test_df = df.iloc[split_point:].copy()
    
    train_df.to_csv('data_splits/soil_train_sequential.csv', index=False)
    test_df.to_csv('data_splits/soil_test_sequential.csv', index=False)
    
    print(f"Sequential split created:")
    print(f"Training: {len(train_df)} samples (Samples 1-{split_point})")
    print(f"Testing: {len(test_df)} samples (Samples {split_point+1}-{len(df)})")

# Method 4: Custom Split by Sample Groups
def create_custom_split():
    # Example: Use specific sample ranges for testing
    test_samples = [10, 20, 30, 40, 50, 60, 70, 80, 89]  # Every 10th sample roughly
    
    test_df = df[df['SampleNo.'].isin(test_samples)].copy()
    train_df = df[~df['SampleNo.'].isin(test_samples)].copy()
    
    train_df.to_csv('data_splits/soil_train_custom.csv', index=False)
    test_df.to_csv('data_splits/soil_test_custom.csv', index=False)
    
    print(f"Custom split created:")
    print(f"Training: {len(train_df)} samples")
    print(f"Testing: {len(test_df)} samples")
    print(f"Test samples: {test_samples}")

# Execute all splitting methods
print("Creating physical data splits...")
print("="*50)

create_random_split()
print()
create_stratified_split()
print()
create_sequential_split()
print()
create_custom_split()

print("\nFiles created in 'data_splits/' folder:")
print("- soil_train_random.csv / soil_test_random.csv")
print("- soil_train_stratified.csv / soil_test_stratified.csv") 
print("- soil_train_sequential.csv / soil_test_sequential.csv")
print("- soil_train_custom.csv / soil_test_custom.csv")