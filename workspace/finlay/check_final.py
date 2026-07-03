import datetime
from collections import defaultdict

# Raw CSV content provided by Stephen
csv_data = """Contributor,Date,Net Amount,Gross Amount
Employer payments,29/05/2026,3400.00,3400.00
Employer payments,05/05/2026,3400.00,3400.00
Employer payments,02/04/2026,3400.00,3400.00
Employer payments,03/03/2026,3400.00,3400.00
Employer payments,02/03/2026,3400.00,3400.00
Employer payments,05/01/2026,3400.00,3400.00
Employer payments,02/12/2025,3400.00,3400.00
Employer payments,04/11/2025,3400.00,3400.00
Employer payments,02/10/2025,3400.00,3400.00
Employer payments,02/09/2025,3400.00,3400.00
Employer payments,04/08/2025,3400.00,3400.00
Employer payments,02/07/2025,3400.00,3400.00
Employer payments,30/05/2025,2079.16,2079.16
Employer payments,02/05/2025,2079.16,2079.16
Employer payments,02/04/2025,2079.16,2079.16
Employer payments,03/04/2025,2079.16,2079.16
Employer payments,04/03/2025,2079.16,2079.16
Employer payments,04/02/2025,2079.16,2079.16
Employer payments,03/01/2025,2079.16,2079.16
Employer payments,03/12/2024,2079.16,2079.16
Employer payments,04/11/2024,2079.16,2079.16
Employer payments,02/10/2024,2079.16,2079.16
Employer payments,03/09/2024,2079.16,2079.16
Employer payments,02/08/2024,2079.16,2079.16
Employer payments,02/07/2024,2079.16,2079.16
Employer payments,31/05/2024,2079.16,2079.16
Employer payments,02/05/2024,2079.16,2079.16
Employer payments,03/04/2024,2079.16,2079.16
Employer payments,04/03/2024,2079.16,2079.16
Employer payments,02/02/2024,2079.16,2079.16
Employer payments,03/01/2024,2079.16,2079.16
Employer payments,04/12/2023,2079.16,2079.16
Employer payments,02/11/2023,2079.16,2079.16
Employer payments,03/10/2023,2079.16,2079.16
Employer payments,04/09/2023,2079.16,2079.16
Employer payments,02/08/2023,2079.16,2079.16
Employer payments,04/07/2023,2079.16,2079.16
Employer payments,02/06/2023,1999.20,1999.20
Employer payments,03/05/2023,1999.20,1999.20
Employer payments,04/04/2023,1999.20,1999.20
Employer payments,02/03/2023,1999.20,1999.20"""

def get_tax_year(d):
    # UK Tax Year: April 6th to April 5th of the following year
    if (d.month > 4) or (d.month == 4 and d.day >= 6):
        return f"{d.year}_{d.year+1}"
    else:
        return f"{d.year-1}_{d.year}"

# Parse data
rows = [row.split(',') for row in csv_data.strip().split('\n')[1:]]
data = []
for r in rows:
    data.append((datetime.strptime(r[1], '%Y-%m-%d'), float(r[3])))

print("| Date (YYYY-MM-DD) | Pension Input | Tax Year |")
print("| :--- | :--- | :--- |")
for d, amount in sorted(data, key=lambda x: x[0]):
    print(f"| {d.strftime('%Y-%m-%d')} | £{amount:,.2f} | {get_tax_year(d)} |")
