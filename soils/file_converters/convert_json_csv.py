import pandas as pd
import json
import os

# Print current directory to debug
print(f"Current working directory: {os.getcwd()}")

# List files in current directory
files = os.listdir()
print(f"Files in current directory: {files}")

# Try to find the JSON file
json_file = 'mtrd_soils_data.json'
full_path = os.path.join(os.getcwd(), json_file)

# Check if file exists
if not os.path.exists(full_path):
    print(f"File not found at: {full_path}")
    
    # Try looking in parent directory
    parent_dir = os.path.dirname(os.getcwd())
    parent_path = os.path.join(parent_dir, json_file)
    
    if os.path.exists(parent_path):
        print(f"Found file in parent directory: {parent_path}")
        full_path = parent_path
    else:
        # Ask user for correct path
        print("Please enter the full path to the JSON file:")
        user_path = input().strip()
        if os.path.exists(user_path):
            full_path = user_path
        else:
            print(f"File not found at: {user_path}")
            exit(1)

# Load the JSON file using the correct path
print(f"Loading file from: {full_path}")
with open(full_path, 'r') as file:
    data = json.load(file)

# Extract non-empty values
values = []
for item in data:
    if item[""] != "":
        values.append(item[""])

# The first value appears to be "Silt/ Clay" and second is "(%)";
# Let's combine these for the header and then use the rest as data
header = values[0] + " " + values[1]
percentages = values[2:]

# Create a DataFrame with one column
df = pd.DataFrame({header: percentages})

# Save to CSV
output_file = 'soil_silt_clay_percentages.csv'
df.to_csv(output_file, index=False)

print(f"Converted JSON to CSV with {len(percentages)} data rows")
print(f"Saved to: {os.path.join(os.getcwd(), output_file)}")