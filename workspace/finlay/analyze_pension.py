import csv
from datetime import datetime

# Define tax year ranges (UK: April 6 - April 5)
def get_tax_year(date_str):
    d = datetime.strptime(date_str, '%d/%m/%Y')
    if d.month >= 4:
        # If April, check if it's before the 6th
        if d.month == 4 and d.day < 6:
            return f"{d.year-1}-{d.year}"
        return f"{d.year}-{d.year+1}"
    else:
        return f"{d.year-1}-{d.year}"

# Data structure for aggregation
tax_years = {}

# Parse CSV
file_path = '/home/openclaw/.openclaw/workspace/finlay/pension_data.csv'
with open(file_path, mode='r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Normalize numbers
        gross = float(row['Gross Amount'].replace(',', ''))
        ty = get_tax_year(row['Date'])
        
        if ty not in tax_years:
            tax_years[ty] = 0.0
        tax_years[ty] += gross

print(tax_years)
