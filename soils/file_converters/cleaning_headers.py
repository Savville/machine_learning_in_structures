import pandas as pd
import os

# Print current directory for debugging
print(f"Current working directory: {os.getcwd()}")
print(f"Files in directory: {os.listdir()}")

# Try to use the full path instead
file_path = r'c:\Users\User\Desktop\machine_learning\soils\flattened.csv'

# Check if file exists
if not os.path.exists(file_path):
    print(f"Error: File not found at {file_path}")
    # Try to find the file in the current directory
    current_dir = os.getcwd()
    for root, dirs, files in os.walk(current_dir):
        if 'flattened.csv' in files:
            file_path = os.path.join(root, 'flattened.csv')
            print(f"Found file at: {file_path}")
            break
    else:
        print("Could not find flattened.csv anywhere in the current directory")
        exit(1)

# Load the CSV
print(f"Loading file from: {file_path}")
df = pd.read_csv(file_path)

# Clean column names by removing the Unnamed parts
clean_columns = []
for col in df.columns:
    # Split by periods
    parts = col.split('.')
    # Keep only meaningful parts (not containing "Unnamed")
    meaningful_parts = [part for part in parts if "Unnamed" not in part]
    # Join with dots
    clean_name = '.'.join(meaningful_parts)
    clean_columns.append(clean_name)

# Apply the clean column names
df.columns = clean_columns

# Save the cleaned dataframe
df.to_csv('cleaned_MTRD_Soils_data500.csv', index=False)

# Print the new column names
print(df.columns.tolist())