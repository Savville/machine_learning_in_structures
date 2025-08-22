import pandas as pd

# Read the Excel file, specifying header rows
df = pd.read_excel('Soils.xlsx', header=[0,1,2,3])

# Flatten the multi-index columns
df.columns = ['.'.join([str(i).replace(' ', '').replace('/', '') for i in col if str(i) != 'nan']) for col in df.columns]

# Save to CSV
df.to_csv('flattened.csv', index=False)