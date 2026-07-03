import csv
from datetime import datetime
from collections import defaultdict

# Mapping pension payments to tax years
def get_tax_year(date_str):
    d = datetime.strptime(date_str, '%d/%m/%Y')
    # UK Tax Year: April 6th to April 5th of the following year
    if (d.month > 4) or (d.month == 4 and d.day >= 6):
        return f"{d.year}_{d.year+1}"
    else:
        return f"{d.year-1}_{d.year}"

# Read the data file correctly
file_path = '/home/openclaw/.openclaw/workspace/finlay/pension_data.csv'
tax_year_pensions = defaultdict(float)
monthly_breakdown = []

with open(file_path, mode='r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Date is in DD/MM/YYYY format
        try:
            # Handle possible date formats in file
            date_obj = datetime.strptime(row['Date'], '%d/%m/%Y')
        except ValueError:
            date_obj = datetime.strptime(row['Date'], '%d/%m/%y')
        
        gross = float(row['Gross Amount'].replace(',', ''))
        ty = get_tax_year(row['Date'])
        
        tax_year_pensions[ty] += gross
        monthly_breakdown.append({
            'date': date_obj,
            'amount': gross,
            'tax_year': ty
        })

print("YEARLY TOTALS:")
for ty, total in sorted(tax_year_pensions.items()):
    print(f"{ty}: {total:.2f}")
