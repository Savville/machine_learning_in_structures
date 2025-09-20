# Updated training code to use physical files
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# FIX TCL ERROR - Set matplotlib backend BEFORE importing pyplot
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend to avoid TCL issues
import matplotlib.pyplot as plt
import seaborn as sns

# Set plotting style
plt.style.use('default')
sns.set_palette("husl")

# Updated paths for files moved to soils/data_splits folder
def train_model_from_files(train_file, test_file, split_name):
    """Train model using physical train/test files in soils/data_splits folder"""
    
    # CORRECTED file paths - now pointing to data_splits folder
    train_path = f'C:\\Users\\User\\Desktop\\machine_learning\\soils\\data_splits\\{train_file}'
    test_path = f'C:\\Users\\User\\Desktop\\machine_learning\\soils\\data_splits\\{test_file}'
    
    # Load the split data
    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)
    
    print(f"\n{'='*50}")
    print(f"TRAINING WITH {split_name.upper()} SPLIT")
    print(f"{'='*50}")
    print(f"Training samples: {len(train_df)}")
    print(f"Testing samples: {len(test_df)}")
    
    # DEBUG: Check data types and identify problematic columns
    print("\nData types in training set:")
    for col in train_df.columns:
        dtype = train_df[col].dtype
        if dtype == 'object':
            unique_vals = train_df[col].unique()
            print(f"  {col}: {dtype} - Unique values: {unique_vals}")
        else:
            print(f"  {col}: {dtype}")
    
    # Check sample continuity for sequential split
    if split_name == 'sequential':
        train_samples = sorted(train_df['SampleNo.'].tolist())
        test_samples = sorted(test_df['SampleNo.'].tolist())
        
        print(f"Training sample range: {min(train_samples)} to {max(train_samples)}")
        print(f"Testing sample range: {min(test_samples)} to {max(test_samples)}")
        
        # Check if sequential order is maintained
        if train_samples == list(range(min(train_samples), max(train_samples) + 1)):
            print("✅ Sequential training order maintained")
        else:
            print("⚠️ Sequential training order disrupted")
            
        if test_samples == list(range(min(test_samples), max(test_samples) + 1)):
            print("✅ Sequential testing order maintained") 
        else:
            print("⚠️ Sequential testing order disrupted")
    
    # Prepare features and target
    target_col = 'CBR.4daysSoak.(%)'
    cols_to_drop = ['SampleNo.', target_col]
    
    # Check if Dosage is present and should be excluded
    if 'Dosage.%' in train_df.columns:
        cols_to_drop.append('Dosage.%')
    
    # HANDLE CATEGORICAL COLUMNS PROPERLY
    # Identify categorical columns (object dtype or string values)
    categorical_cols = []
    for col in train_df.columns:
        if col not in cols_to_drop:
            if train_df[col].dtype == 'object' or any(isinstance(val, str) for val in train_df[col].dropna()):
                categorical_cols.append(col)
                print(f"Found categorical column: {col}")
    
    # Create copies for processing
    train_processed = train_df.copy()
    test_processed = test_df.copy()
    
    # Encode categorical columns
    label_encoders = {}
    for col in categorical_cols:
        le = LabelEncoder()
        
        # Combine train and test values to ensure consistent encoding
        combined_values = pd.concat([train_processed[col], test_processed[col]]).dropna().astype(str)
        le.fit(combined_values)
        
        # Transform both train and test
        train_processed[col] = le.transform(train_processed[col].fillna('Unknown').astype(str))
        test_processed[col] = le.transform(test_processed[col].fillna('Unknown').astype(str))
        
        label_encoders[col] = le
        print(f"Encoded {col}: {dict(zip(le.classes_, le.transform(le.classes_)))}")
    
    # Extract features and target
    X_train = train_processed.drop(cols_to_drop, axis=1)
    y_train = train_processed[target_col]
    X_test = test_processed.drop(cols_to_drop, axis=1)
    y_test = test_processed[target_col]
    
    print(f"\nFeatures: {X_train.shape[1]}")
    print(f"Feature names: {X_train.columns.tolist()}")
    print(f"Target range - Train: {y_train.min():.1f} to {y_train.max():.1f}")
    print(f"Target range - Test: {y_test.min():.1f} to {y_test.max():.1f}")
    
    # Convert all features to numeric (in case there are any remaining issues)
    X_train = X_train.apply(pd.to_numeric, errors='coerce')
    X_test = X_test.apply(pd.to_numeric, errors='coerce')
    
    # Fill any NaN values that might have been created
    X_train = X_train.fillna(0)
    X_test = X_test.fillna(0)
    
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
    
    print(f"RMSE: {rmse:.2f}")
    print(f"R²: {r2:.3f}")
    
    return rf_model, scaler, r2, label_encoders

# Updated file names in soils/data_splits folder
splits = [
    ('soil_train_random.csv', 'soil_test_random.csv', 'random'),
    ('soil_train_stratified.csv', 'soil_test_stratified.csv', 'stratified'),
    ('soil_train_sequential.csv', 'soil_test_sequential.csv', 'sequential'),
    ('soil_train_custom.csv', 'soil_test_custom.csv', 'custom')
]

results = {}
encoders_dict = {}

for train_file, test_file, split_name in splits:
    try:
        model, scaler, r2, label_encoders = train_model_from_files(train_file, test_file, split_name)
        results[split_name] = r2
        encoders_dict[split_name] = label_encoders
    except FileNotFoundError as e:
        print(f"⚠️ File not found for {split_name} split: {e}")
        print(f"Expected files in data_splits folder: {train_file}, {test_file}")
    except Exception as e:
        print(f"⚠️ Error processing {split_name} split: {e}")
        print(f"Error type: {type(e).__name__}")

print(f"\n{'='*50}")
print("SPLIT COMPARISON RESULTS")
print(f"{'='*50}")
for split_name, r2 in results.items():
    print(f"{split_name.capitalize()} split R²: {r2:.3f}")

# Check if sequential effect impacted performance
if 'sequential' in results and 'random' in results:
    seq_performance = results['sequential']
    random_performance = results['random']
    diff = abs(seq_performance - random_performance)
    
    print(f"\nSequential vs Random Performance:")
    print(f"Random split R²: {random_performance:.3f}")
    print(f"Sequential split R²: {seq_performance:.3f}")
    print(f"Difference: {diff:.3f}")
    if diff > 0.05:
        print("⚠️ Significant difference - check if sequential order was maintained")
    else:
        print("✅ Similar performance - sequential order likely preserved")

# Verification function for sequential split
def verify_sequential_split():
    """Verify that sequential split maintains proper order"""
    try:
        train_df = pd.read_csv('C:\\Users\\User\\Desktop\\machine_learning\\soils\\data_splits\\soil_train_sequential.csv')
        test_df = pd.read_csv('C:\\Users\\User\\Desktop\\machine_learning\\soils\\data_splits\\soil_test_sequential.csv')
        
        train_samples = sorted(train_df['SampleNo.'].tolist())
        test_samples = sorted(test_df['SampleNo.'].tolist())
        
        print(f"\n{'='*50}")
        print("SEQUENTIAL SPLIT VERIFICATION")
        print(f"{'='*50}")
        print(f"Training samples: {train_samples[:5]}...{train_samples[-5:]}")
        print(f"Testing samples: {test_samples}")
        
        # Check if training samples come before test samples
        if max(train_samples) < min(test_samples):
            print("✅ Sequential order maintained: training samples < test samples")
        else:
            print("⚠️ Sequential order disrupted: overlapping sample ranges")
            
    except FileNotFoundError as e:
        print(f"⚠️ Sequential files not found: {e}")

# Run verification
verify_sequential_split()

def plot_predictions_comparison(results, encoders_dict):
    """Create comprehensive plots comparing all split predictions"""
    
    # Store predictions for plotting
    all_predictions = {}
    all_actuals = {}
    all_residuals = {}
    
    # Re-run models to get predictions for plotting
    for train_file, test_file, split_name in splits:
        try:
            train_path = f'C:\\Users\\User\\Desktop\\machine_learning\\soils\\data_splits\\{train_file}'
            test_path = f'C:\\Users\\User\\Desktop\\machine_learning\\soils\\data_splits\\{test_file}'
            
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            
            # Process data (same as in your function)
            target_col = 'CBR.4daysSoak.(%)'
            cols_to_drop = ['SampleNo.', target_col]
            if 'Dosage.%' in train_df.columns:
                cols_to_drop.append('Dosage.%')
            
            # Handle categorical columns
            train_processed = train_df.copy()
            test_processed = test_df.copy()
            
            categorical_cols = []
            for col in train_df.columns:
                if col not in cols_to_drop:
                    if train_df[col].dtype == 'object' or any(isinstance(val, str) for val in train_df[col].dropna()):
                        categorical_cols.append(col)
            
            # Encode categorical columns
            for col in categorical_cols:
                le = LabelEncoder()
                combined_values = pd.concat([train_processed[col], test_processed[col]]).dropna().astype(str)
                le.fit(combined_values)
                train_processed[col] = le.transform(train_processed[col].fillna('Unknown').astype(str))
                test_processed[col] = le.transform(test_processed[col].fillna('Unknown').astype(str))
            
            # Extract features and target
            X_train = train_processed.drop(cols_to_drop, axis=1)
            y_train = train_processed[target_col]
            X_test = test_processed.drop(cols_to_drop, axis=1)
            y_test = test_processed[target_col]
            
            # Convert to numeric and handle NaN
            X_train = X_train.apply(pd.to_numeric, errors='coerce').fillna(0)
            X_test = X_test.apply(pd.to_numeric, errors='coerce').fillna(0)
            
            # Standardize and train
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
            rf_model.fit(X_train_scaled, y_train)
            
            # Get predictions
            y_pred = rf_model.predict(X_test_scaled)
            
            # Store for plotting
            all_predictions[split_name] = y_pred
            all_actuals[split_name] = y_test.values
            all_residuals[split_name] = y_test.values - y_pred
            
        except Exception as e:
            print(f"Error processing {split_name} for plotting: {e}")
    
    # Create comprehensive plots
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Soil CBR Prediction Comparison Across Different Data Splits', fontsize=16, fontweight='bold')
    
    # 1. Actual vs Predicted scatter plots
    colors = ['blue', 'red', 'green', 'orange']
    
    for i, (split_name, color) in enumerate(zip(all_predictions.keys(), colors)):
        if split_name in all_predictions:
            ax = axes[0, 0]
            ax.scatter(all_actuals[split_name], all_predictions[split_name], 
                      alpha=0.7, label=f'{split_name.capitalize()}', color=color, s=50)
    
    # Perfect prediction line
    min_val = min([min(all_actuals[k]) for k in all_actuals.keys()])
    max_val = max([max(all_actuals[k]) for k in all_actuals.keys()])
    axes[0, 0].plot([min_val, max_val], [min_val, max_val], 'k--', alpha=0.8, linewidth=2)
    axes[0, 0].set_xlabel('Actual CBR (%)')
    axes[0, 0].set_ylabel('Predicted CBR (%)')
    axes[0, 0].set_title('Actual vs Predicted CBR')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # 2. R² comparison bar plot
    ax = axes[0, 1]
    split_names = list(results.keys())
    r2_values = list(results.values())
    bars = ax.bar(split_names, r2_values, color=colors[:len(split_names)], alpha=0.7, edgecolor='black')
    ax.set_ylabel('R² Score')
    ax.set_title('Model Performance Comparison')
    ax.set_ylim(0, 1)
    
    # Add value labels on bars
    for bar, r2 in zip(bars, r2_values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{r2:.3f}', ha='center', va='bottom', fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    
    # 3. Residuals plot
    ax = axes[0, 2]
    for i, (split_name, color) in enumerate(zip(all_residuals.keys(), colors)):
        if split_name in all_residuals:
            ax.scatter(all_predictions[split_name], all_residuals[split_name], 
                      alpha=0.7, label=f'{split_name.capitalize()}', color=color, s=50)
    ax.axhline(y=0, color='black', linestyle='--', alpha=0.8)
    ax.set_xlabel('Predicted CBR (%)')
    ax.set_ylabel('Residuals (Actual - Predicted)')
    ax.set_title('Residuals vs Predicted')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 4. Distribution of actual values per split
    ax = axes[1, 0]
    for i, (split_name, color) in enumerate(zip(all_actuals.keys(), colors)):
        if split_name in all_actuals:
            ax.hist(all_actuals[split_name], alpha=0.5, label=f'{split_name.capitalize()}', 
                   color=color, bins=15, edgecolor='black')
    ax.set_xlabel('CBR (%)')
    ax.set_ylabel('Frequency')
    ax.set_title('Distribution of Actual CBR Values by Split')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    # 5. Box plot of residuals
    ax = axes[1, 1]
    residual_data = [all_residuals[split] for split in all_residuals.keys()]
    split_labels = [split.capitalize() for split in all_residuals.keys()]
    box_plot = ax.boxplot(residual_data, labels=split_labels, patch_artist=True)
    
    # Color the boxes
    for patch, color in zip(box_plot['boxes'], colors[:len(box_plot['boxes'])]):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    ax.axhline(y=0, color='red', linestyle='--', alpha=0.8)
    ax.set_ylabel('Residuals')
    ax.set_title('Distribution of Residuals by Split')
    ax.grid(True, alpha=0.3, axis='y')
    
    # 6. RMSE comparison
    ax = axes[1, 2]
    rmse_values = []
    for split_name in all_predictions.keys():
        if split_name in all_predictions:
            rmse = np.sqrt(np.mean(all_residuals[split_name]**2))
            rmse_values.append(rmse)
    
    bars = ax.bar(split_labels, rmse_values, color=colors[:len(rmse_values)], 
                  alpha=0.7, edgecolor='black')
    ax.set_ylabel('RMSE')
    ax.set_title('Root Mean Square Error Comparison')
    
    # Add value labels on bars
    for bar, rmse in zip(bars, rmse_values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{rmse:.2f}', ha='center', va='bottom', fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig('soil_cbr_prediction_comparison.png', dpi=300, bbox_inches='tight')
    print("✅ Saved: soil_cbr_prediction_comparison.png")
    
    # Additional detailed plot for each split
    create_individual_split_plots(all_predictions, all_actuals, all_residuals, results)

def create_individual_split_plots(all_predictions, all_actuals, all_residuals, results):
    """Create individual detailed plots for each split"""
    
    n_splits = len(all_predictions)
    fig, axes = plt.subplots(n_splits, 3, figsize=(15, 4*n_splits))
    
    if n_splits == 1:
        axes = axes.reshape(1, -1)
    
    colors = ['blue', 'red', 'green', 'orange']
    
    for i, (split_name, color) in enumerate(zip(all_predictions.keys(), colors)):
        if split_name in all_predictions:
            # Actual vs Predicted
            axes[i, 0].scatter(all_actuals[split_name], all_predictions[split_name], 
                              alpha=0.7, color=color, s=60, edgecolors='black', linewidth=0.5)
            
            # Perfect prediction line
            min_val = min(all_actuals[split_name])
            max_val = max(all_actuals[split_name])
            axes[i, 0].plot([min_val, max_val], [min_val, max_val], 'k--', alpha=0.8, linewidth=2)
            axes[i, 0].set_xlabel('Actual CBR (%)')
            axes[i, 0].set_ylabel('Predicted CBR (%)')
            axes[i, 0].set_title(f'{split_name.capitalize()} Split: Actual vs Predicted (R² = {results[split_name]:.3f})')
            axes[i, 0].grid(True, alpha=0.3)
            
            # Residuals vs Predicted
            axes[i, 1].scatter(all_predictions[split_name], all_residuals[split_name], 
                              alpha=0.7, color=color, s=60, edgecolors='black', linewidth=0.5)
            axes[i, 1].axhline(y=0, color='black', linestyle='--', alpha=0.8)
            axes[i, 1].set_xlabel('Predicted CBR (%)')
            axes[i, 1].set_ylabel('Residuals')
            axes[i, 1].set_title(f'{split_name.capitalize()} Split: Residuals vs Predicted')
            axes[i, 1].grid(True, alpha=0.3)
            
            # Histogram of residuals
            axes[i, 2].hist(all_residuals[split_name], bins=10, alpha=0.7, color=color, 
                           edgecolor='black', density=True)
            axes[i, 2].axvline(x=0, color='red', linestyle='--', alpha=0.8)
            axes[i, 2].set_xlabel('Residuals')
            axes[i, 2].set_ylabel('Density')
            axes[i, 2].set_title(f'{split_name.capitalize()} Split: Residuals Distribution')
            axes[i, 2].grid(True, alpha=0.3, axis='y')
            
            # Add statistics text
            rmse = np.sqrt(np.mean(all_residuals[split_name]**2))
            mae = np.mean(np.abs(all_residuals[split_name]))
            axes[i, 2].text(0.05, 0.95, f'RMSE: {rmse:.2f}\nMAE: {mae:.2f}', 
                           transform=axes[i, 2].transAxes, verticalalignment='top',
                           bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('individual_split_analysis.png', dpi=300, bbox_inches='tight')
    print("✅ Saved: individual_split_analysis.png")

def create_performance_summary_table(results):
    """Create a summary table of model performance"""
    
    print(f"\n{'='*80}")
    print("DETAILED PERFORMANCE SUMMARY")
    print(f"{'='*80}")
    
    # Create summary DataFrame
    summary_data = []
    for split_name in results.keys():
        summary_data.append({
            'Split Type': split_name.capitalize(),
            'R² Score': f"{results[split_name]:.3f}",
            'Performance Level': 'Excellent' if results[split_name] > 0.9 else 
                               'Very Good' if results[split_name] > 0.8 else
                               'Good' if results[split_name] > 0.7 else
                               'Fair' if results[split_name] > 0.6 else 'Poor'
        })
    
    summary_df = pd.DataFrame(summary_data)
    print(summary_df.to_string(index=False))
    
    # Best performing split
    best_split = max(results, key=results.get)
    worst_split = min(results, key=results.get)
    
    print(f"\n🏆 Best performing split: {best_split.capitalize()} (R² = {results[best_split]:.3f})")
    print(f"📉 Worst performing split: {worst_split.capitalize()} (R² = {results[worst_split]:.3f})")
    print(f"📊 Performance spread: {results[best_split] - results[worst_split]:.3f}")

# Add these function calls at the end of your existing code
if results:  # Only plot if we have results
    print("\n" + "="*50)
    print("CREATING PREDICTION PLOTS...")
    print("="*50)
    
    plot_predictions_comparison(results, encoders_dict)
    create_performance_summary_table(results)
    
    print("\nPlots saved:")
    print("- soil_cbr_prediction_comparison.png")
    print("- individual_split_analysis.png")
else:
    print("No results to plot - check if data files are accessible")