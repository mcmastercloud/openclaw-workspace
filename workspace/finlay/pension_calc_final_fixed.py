import csv
from datetime import datetime
from collections import defaultdict

# Mapping pension payments to tax years (April 6th to April 5th)
def get_tax_year(date_str):
    # Try parsing both formats
    try:
        d = datetime.strptime(date_str, '%d/%m/%Y')
    except ValueError:
        d = datetime.strptime(date_str, '%Y-%m-%d')
    # If month is after April, or it's April and day is >= 6, it's the current year.
    if (d.month > 4) or (d.month == 4 and d.day >= 6):
        return f"{d.year}_{d.year+1}"
    else:
        return f"{d.year-1}_{d.year}"

# Read the provided CSV file
file_path = '/home/openclaw/.openclaw/workspace/finlay/pension_data.csv'
tax_year_pensions = defaultdict(float)
monthly_breakdown = []

with open(file_path, mode='r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        date_str = row['Date']
        gross = float(row['Gross Amount'].replace(',', ''))
        ty = get_tax_year(date_str)
        
        tax_year_pensions[ty] += gross
        monthly_breakdown.append({
            'date': date_str,
            'amount': gross,
            'tax_year': ty
        })

print("YEARLY TOTALS:")
# Sort by tax year
for ty in sorted(tax_year_pensions.keys()):
    print(f"{ty}: {tax_year_pensions[ty]:.2f}")

print("\nMONTHLY BREAKDOWN:")
# We need to sort by date, convert dates to sortable format
def sort_date(item):
    try:
        return datetime.strptime(item['date'], '%Y-%m-%d')
    except ValueError:
        return datetime.strptime(item['date'], '%d/%m/%Y')

for item in sorted(monthly_breakdown, key=sort_date):
    print(f"{item['date']} | {item['amount']:8.2f} | {item['tax_year']}")
