import pandas as pd
import os

# Set and verify the correct working directory
os.chdir(r'C:\Users\User\Desktop\machine_learning\Soils')
print(f"Current working directory: {os.getcwd()}")

# List all files in the directory
print("Files in directory:")
for file in os.listdir():
    print(f"  - {file}")

# Look for Excel files in the directory
excel_files = [f for f in os.listdir() if f.endswith('.xlsx')]
print(f"\nExcel files found: {excel_files}")

# Try to find the target file or a similar one
target_file = None
exact_match = "MTRD SOILS STANDARD TESTS DATA 500 pts1.xlsx"

if exact_match in excel_files:
    target_file = exact_match
    print(f"Found exact match: {target_file}")
else:
    # Look for similar files
    for file in excel_files:
        if "MTRD" in file.upper() and "SOIL" in file.upper():
            target_file = file
            print(f"Found similar file: {target_file}")
            break

# If no file was found automatically, ask user
if not target_file:
    print("\nCouldn't automatically find the MTRD SOILS file.")
    print("Available Excel files:")
    for i, file in enumerate(excel_files):
        print(f"  {i+1}. {file}")
    
    choice = input("\nEnter the number of the correct file, or the full path: ")
    
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(excel_files):
            target_file = excel_files[idx]
        else:
            target_file = choice
    except ValueError:
        target_file = choice

# Final confirmation
print(f"\nWill use file: {target_file}")

# Check if file exists
if not os.path.exists(target_file):
    print(f"Error: File not found: {target_file}")
    exit(1)

# Read the Excel file with multi-index headers
try:
    print(f"Reading file: {target_file}")
    df = pd.read_excel(target_file, header=[0,1,2,3])
    
    # Flatten the multi-index columns
    df.columns = ['.'.join([str(i).replace(' ', '').replace('/', '') for i in col if str(i) != 'nan']) for col in df.columns]
    
    # Print sample of the data
    print("\nFirst 5 rows of data:")
    print(df.head())
    
    # Save to CSV
    output_file = 'flattened.csv'
    df.to_csv(output_file, index=False)
    print(f"\nSuccessfully saved to {output_file}")
    
except Exception as e:
    print(f"Error processing file: {e}")