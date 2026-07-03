import csv
from datetime import datetime
from collections import defaultdict

# Mapping pension payments to tax years
def get_tax_year(date_str):
    d = datetime.strptime(date_str, '%d/%m/%Y')
    if d.month >= 4:
        # If April, and on or after the 6th, it's the new tax year.
        if d.month == 4 and d.day < 6:
            return f"{d.year-1}-{d.year}"
        return f"{d.year}-{d.year+1}"
    else:
        return f"{d.year-1}-{d.year}"

# Data structure for aggregation
tax_year_pensions = defaultdict(float)

# Pension data from the image provided
pension_data = [
    # (Date, Gross Amount)
    ("29/05/2026", 3400.00), ("05/05/2026", 3400.00), ("02/04/2026", 3400.00),
    ("03/03/2026", 3400.00), ("03/02/2026", 3400.00), ("05/01/2026", 3400.00),
    ("02/12/2025", 3400.00), ("04/11/2025", 3400.00), ("02/10/2025", 3400.00),
    ("02/09/2025", 3400.00), ("04/08/2025", 3400.00), ("02/07/2025", 3400.00),
    ("30/05/2025", 2079.16), ("02/05/2025", 2079.16), ("02/04/2025", 2079.16),
    ("04/03/2025", 2079.16), ("04/02/2025", 2079.16), ("03/01/2025", 2079.16),
    ("03/12/2024", 2079.16), ("04/11/2024", 2079.16), ("02/10/2024", 2079.16),
    ("03/09/2024", 2079.16), ("02/08/2024", 2079.16), ("02/07/2024", 2079.16),
    ("31/05/2024", 2079.16), ("02/05/2024", 2079.16), ("03/04/2024", 2079.16),
    ("04/03/2024", 2079.16), ("02/02/2024", 2079.16), ("03/01/2024", 2079.16),
    ("04/12/2023", 2079.16), ("02/11/2023", 2079.16), ("03/10/2023", 2079.16),
    ("04/09/2023", 2079.16), ("02/08/2023", 2079.16), ("04/07/2023", 2079.16),
    ("02/06/2023", 1999.20), ("03/05/2023", 1999.20), ("04/04/2023", 1999.20)
]

for date_s, amount in pension_data:
    ty = get_tax_year(date_s)
    tax_year_pensions[ty] += amount

for ty, total in sorted(tax_year_pensions.items()):
    print(f"{ty}: {total:.2f}")
