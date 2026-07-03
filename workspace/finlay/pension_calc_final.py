import csv
from datetime import datetime
from collections import defaultdict

# Mapping pension payments to tax years (April 6th to April 5th)
def get_tax_year(date_str):
    d = datetime.strptime(date_str, '%Y-%m-%d')
    # If month is after April, or it's April and day is >= 6, it's the current year.
    # Otherwise, it belongs to the previous tax year.
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
        date_str = row['Date'] # YYYY-MM-DD
        gross = float(row['Gross Amount'].replace(',', ''))
        ty = get_tax_year(date_str)
        
        tax_year_pensions[ty] += gross
        monthly_breakdown.append({
            'date': date_str,
            'amount': gross,
            'tax_year': ty
        })

print("YEARLY TOTALS:")
for ty, total in sorted(tax_year_pensions.items()):
    print(f"{ty}: {total:.2f}")

print("\nMONTHLY BREAKDOWN:")
for item in sorted(monthly_breakdown, key=lambda x: x['date']):
    print(f"{item['date']} | {item['amount']:.2f} | {item['tax_year']}")
