import csv
from datetime import datetime
from collections import defaultdict

# Mapping pension payments to tax years (April 6th to April 5th)
def get_tax_year(d):
    if (d.month > 4) or (d.month == 4 and d.day >= 6):
        return f"{d.year}_{d.year+1}"
    else:
        return f"{d.year-1}_{d.year}"

# Data: Pension (from CSV) and Salary (from Payslip archive)
# Data source: CSV provided + Salary list (Monthly base: 10,106.60 for 23-24, 10,125.50 for 24-25, 16288.02 for 25-26/26-27)
pension_data = [
    ("2023-03-02", 1999.20), ("2023-04-04", 1999.20), ("2023-05-03", 1999.20), ("2023-06-02", 1999.20),
    ("2023-07-04", 2079.16), ("2023-08-02", 2079.16), ("2023-09-04", 2079.16), ("2023-10-03", 2079.16),
    ("2023-11-02", 2079.16), ("2023-12-04", 2079.16), ("2024-01-03", 2079.16), ("2024-02-02", 2079.16),
    ("2024-03-04", 2079.16), ("2024-04-03", 2079.16), ("2024-05-02", 2079.16), ("2024-05-31", 2079.16),
    ("2024-07-02", 2079.16), ("2024-08-02", 2079.16), ("2024-09-03", 2079.16), ("2024-10-02", 2079.16),
    ("2024-11-04", 2079.16), ("2024-12-03", 2079.16), ("2025-01-03", 2079.16), ("2025-02-04", 2079.16),
    ("2025-03-04", 2079.16), ("2025-04-02", 2079.16), ("2025-05-02", 2079.16), ("2025-05-30", 2079.16),
    ("2025-07-02", 3400.00), ("2025-08-04", 3400.00), ("2025-09-02", 3400.00), ("2025-10-02", 3400.00),
    ("2025-11-04", 3400.00), ("2025-12-02", 3400.00), ("2026-01-05", 3400.00), ("2026-02-03", 3400.00),
    ("2026-03-03", 3400.00), ("2026-04-02", 3400.00), ("2026-05-05", 3400.00), ("2026-05-29", 3400.00)
]

# Salary mapping
def get_salary(date):
    if date < datetime(2024, 4, 1): return 10106.60
    if date < datetime(2025, 4, 1): return 10125.50
    return 16288.02

yearly_totals = defaultdict(lambda: {"pay": 0.0, "pension": 0.0})

print("| Month | Tax Year | Taxable Pay | Pension Input |")
print("| :--- | :--- | :--- | :--- |")
for date_str, amount in sorted(pension_data, key=lambda x: x[0]):
    d = datetime.strptime(date_str, '%Y-%m-%d')
    ty = get_tax_year(d)
    if '2022' not in ty:
        pay = get_salary(d)
        yearly_totals[ty]["pay"] += pay
        yearly_totals[ty]["pension"] += amount
        print(f"| {date_str} | {ty} | £{pay:,.2f} | £{amount:,.2f} |")

print("\n### Annual Totals")
print("| Tax Year | Total Taxable Pay | Total Pension | Allowance | Unused |")
print("| :--- | :--- | :--- | :--- | :--- |")
for ty in sorted(yearly_totals.keys()):
    t = yearly_totals[ty]
    unused = 60000.00 - t["pension"]
    if ty == "2026_2027":
        unused = 34971.88 - t["pension"]
    print(f"| {ty} | £{t['pay']:,.2f} | £{t['pension']:,.2f} | £{60000 if '2026' not in ty else 34971.88:,.2f} | £{unused:,.2f} |")
