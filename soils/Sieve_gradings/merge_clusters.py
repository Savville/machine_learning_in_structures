import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib
matplotlib.use('Agg')  # Fix for Tcl error - use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns

# 1. LOAD BOTH DATASETS
main_data = pd.read_csv(r'C:\Users\User\Desktop\machine_learning\soils\cleaned_MTRD_Soils_data.csv')
grading_clusters = pd.read_csv(r'C:\Users\User\Desktop\machine_learning\soils\soil_grading_clusters.csv')

print("Main data shape:", main_data.shape)
print("Grading clusters shape:", grading_clusters.shape)

# 2. MERGE THE GRADING CLUSTER LABELS WITH MAIN DATA
# Merge on SampleNo.
enhanced_data = main_data.merge(
    grading_clusters[['SampleNo.', 'GradingCluster']], 
    on='SampleNo.', 
    how='left'
)

print("Enhanced data shape:", enhanced_data.shape)
print("Grading cluster distribution:")
print(enhanced_data['GradingCluster'].value_counts().sort_index())

# 3. CREATE GRADING TYPE LABELS (MORE INTERPRETABLE)
def label_grading_type(cluster):
    """Convert cluster numbers to meaningful soil type names"""
    labels = {
        0: 'Medium_Graded',      # Moderate distribution
        1: 'Fine_Graded',        # High fine content
        2: 'Coarse_Graded',      # More coarse particles
        3: 'Well_Graded'         # Good distribution across sizes
    }
    return labels.get(cluster, 'Unknown')

enhanced_data['GradingType'] = enhanced_data['GradingCluster'].apply(label_grading_type)

print("\nGrading type distribution:")
print(enhanced_data['GradingType'].value_counts())

# 4. PREPARE FEATURES
grading_sieve_cols = [col for col in enhanced_data.columns if 'Grading.%PassingBSSieveSize' in col]

# Option 1: Features with clusters only
X_with_clusters = enhanced_data.drop(grading_sieve_cols + ['SampleNo.', 'CBR.4daysSoak.(%)'], axis=1)
grading_dummies = pd.get_dummies(enhanced_data['GradingType'], prefix='GradingType')
X_with_clusters = pd.concat([X_with_clusters.drop(['GradingCluster', 'GradingType'], axis=1), grading_dummies], axis=1)

# Option 2: Features with both sieves and clusters
X_with_both = enhanced_data.drop(['SampleNo.', 'CBR.4daysSoak.(%)'], axis=1)
grading_dummies_both = pd.get_dummies(enhanced_data['GradingType'], prefix='GradingType')
X_with_both = pd.concat([X_with_both.drop(['GradingCluster', 'GradingType'], axis=1), grading_dummies_both], axis=1)

y = enhanced_data['CBR.4daysSoak.(%)']

# 5. MODEL TRAINING AND EVALUATION
def train_and_evaluate_model(X, y, model_name):
    """Train RF model and return performance metrics"""
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Standardize features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train model
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train_scaled, y_train)
    
    # Evaluate
    y_pred = rf_model.predict(X_test_scaled)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    
    print(f"\n{model_name} Results:")
    print(f"RMSE: {rmse:.2f}")
    print(f"R²: {r2:.3f}")
    print(f"Number of features: {X.shape[1]}")
    
    return rf_model, scaler

print("="*50)
print("MODEL COMPARISON")
print("="*50)

# Original model (with individual sieve data)
X_original = main_data.drop(['SampleNo.', 'CBR.4daysSoak.(%)'], axis=1)
model_orig, _ = train_and_evaluate_model(X_original, y, "Original Model (Individual Sieves)")

# Model with clusters only
model_clusters, _ = train_and_evaluate_model(X_with_clusters, y, "Cluster Model (No Individual Sieves)")

# Model with both
model_both, _ = train_and_evaluate_model(X_with_both, y, "Combined Model (Sieves + Clusters)")

# 6. FEATURE IMPORTANCE (without plotting)
importances_combined = pd.DataFrame({
    'Feature': X_with_both.columns,
    'Importance': model_both.feature_importances_
}).sort_values('Importance', ascending=False)

print("\n" + "="*50)
print("TOP 10 MOST IMPORTANT FEATURES")
print("="*50)
print(importances_combined.head(10))

# 7. CBR STATISTICS BY GRADING TYPE
print("\nCBR Statistics by Grading Type:")
cbr_by_grading = enhanced_data.groupby('GradingType')['CBR.4daysSoak.(%)'].agg(['count', 'mean', 'std', 'min', 'max'])
print(cbr_by_grading)

# 8. SAVE RESULTS
enhanced_data.to_csv('enhanced_soil_data_with_grading_clusters.csv', index=False)
print(f"\nSaved enhanced dataset to 'enhanced_soil_data_with_grading_clusters.csv'")

print("\n" + "="*60)
print("RECOMMENDATION")
print("="*60)
print("Based on the model comparison above:")
print("- Compare R² values to determine best approach")
print("- Grading clusters provide simplified soil classification")
print("- Combined approach may offer best predictive power")