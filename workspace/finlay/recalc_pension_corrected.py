import datetime
from collections import defaultdict

# Pension data from the provided image/data (YYYY-MM-DD format as seen in the image)
data = [
    ("2026-05-29", 3400.00), ("2026-05-05", 3400.00), ("2026-04-02", 3400.00),
    ("2026-03-03", 3400.00), ("2026-02-03", 3400.00), ("2026-01-05", 3400.00),
    ("2025-12-02", 3400.00), ("2025-11-04", 3400.00), ("2025-10-02", 3400.00),
    ("2025-09-02", 3400.00), ("2025-08-04", 3400.00), ("2025-07-02", 3400.00),
    ("2025-05-30", 2079.16), ("2025-05-02", 2079.16), ("2025-04-02", 2079.16),
    ("2025-03-04", 2079.16), ("2025-02-04", 2079.16), ("2025-01-03", 2079.16),
    ("2024-12-03", 2079.16), ("2024-11-04", 2079.16), ("2024-10-02", 2079.16),
    ("2024-09-03", 2079.16), ("2024-08-02", 2079.16), ("2024-07-02", 2079.16),
    ("2024-05-31", 2079.16), ("2024-05-02", 2079.16), ("2024-04-03", 2079.16),
    ("2024-03-04", 2079.16), ("2024-02-02", 2079.16), ("2024-01-03", 2079.16),
    ("2023-12-04", 2079.16), ("2023-11-02", 2079.16), ("2023-10-03", 2079.16),
    ("2023-09-04", 2079.16), ("2023-08-02", 2079.16), ("2023-07-04", 2079.16),
    ("2023-06-02", 1999.20), ("2023-05-03", 1999.20), ("2023-04-04", 1999.20)
]

def get_tax_year(date_str):
    d = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    # UK Tax Year: April 6th to April 5th
    if (d.month > 4) or (d.month == 4 and d.day >= 6):
        return f"{d.year}-{d.year+1}"
    else:
        return f"{d.year-1}-{d.year}"

# Aggregating
yearly_pension = defaultdict(float)
monthly_breakdown = []

for date_str, amount in data:
    ty = get_tax_year(date_str)
    yearly_pension[ty] += amount
    monthly_breakdown.append((date_str, amount, ty))

# Print Results
print("YEARLY TOTALS:")
for ty in sorted(yearly_pension.keys()):
    print(f"{ty}: {yearly_pension[ty]:.2f}")

print("\nMONTHLY BREAKDOWN:")
for date, amount, ty in sorted(monthly_breakdown):
    print(f"{date} | {amount:.2f} | {ty}")
