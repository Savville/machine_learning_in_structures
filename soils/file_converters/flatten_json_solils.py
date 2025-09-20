import json
import csv

# Load JSON data
with open('c:\\Users\\User\\Downloads\\tableConvert.com_kz4vyz.json', encoding='utf-8') as f:
    data = json.load(f)

# Transpose the data to get columns as rows
columns = []
for col in data:
    for k, v in col.items():
        columns.append(v)

# The first 3 rows are headers/subheaders/units
header_rows = columns[:3]
data_rows = columns[3:]

# Build flattened headers
flattened_headers = []
col_count = len(header_rows[0])
for i in range(col_count):
    parts = []
    for row in header_rows:
        val = row[i].strip() if i < len(row) else ''
        if val and val not in ['(mm)', '(%)', '( % )', '% ', '']:
            parts.append(val.replace('/', '').replace(' ', ''))
        elif val in ['(mm)', '(%)', '( % )', '% ']:
            parts.append(val.replace(' ', ''))
    flattened_headers.append('.'.join(parts))

# Remove empty headers (if any)
flattened_headers = [h if h else f'col{i+1}' for i, h in enumerate(flattened_headers)]

# Transpose data rows to get list of rows
rows = list(zip(*data_rows))

# Remove rows that are all empty or header rows
rows = [row for row in rows if any(cell.strip() for cell in row)]

# Write to CSV
with open('c:\\Users\\User\\Downloads\\flattened_output.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(flattened_headers)
    writer.writerows(rows[3:])  # skip the first 3 header rows

print("CSV file created: c:\\Users\\User\\Downloads\\flattened_output.csv")