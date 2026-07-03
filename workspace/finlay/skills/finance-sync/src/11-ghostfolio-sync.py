import os
import sys
from datetime import datetime
from dependencies import firefly_api, ghostfolio_api

# McMaster Finance System: Step 11 - Ghostfolio Net Worth Sync
# Implements SOP: Ghostfolio Net Worth Synchronisation

def main(staging_dir):
    if not staging_dir:
        print("Error: Staging directory not provided.")
        sys.exit(1)
        
    ff_url = os.environ.get('FIREFLY_URL')
    ff_token = os.environ.get('FIREFLY_TOKEN')
    gf_url = os.environ.get('GHOSTFOLIO_URL')
    gf_token = os.environ.get('GHOSTFOLIO_API_TOKEN')

    if not all([ff_url, ff_token, gf_url, gf_token]):
        print("Error: Missing API configuration for Firefly or Ghostfolio.")
        sys.exit(1)

    print("Initiating Ghostfolio Net Worth Synchronisation...")

    # 1. Fetch Firefly Balances
    def get_ff_bal(account_id):
        resp = firefly_api.make_request(ff_url, ff_token, f"accounts/{account_id}")
        return float(resp.get('data', {}).get('attributes', {}).get('current_balance', 0))

    # Assets & Liabilities
    house_val = get_ff_bal(836)
    mortgage_bal = get_ff_bal(833) # Negative value
    ms_loan_bal = get_ff_bal(830) # Negative value
    
    # Starling Aggregation (IDs: 1, 2, 3, 4, 5, 6, 7, 549, 550, 772)
    starling_ids = [1, 2, 3, 4, 5, 6, 7, 549, 550, 772]
    total_cash = 0.0
    for sid in starling_ids:
        total_cash += get_ff_bal(sid)

    # 2. Logic: Home Equity
    home_equity = house_val + mortgage_bal
    print(f"Calculated Home Equity: £{home_equity:,.2f} (House: £{house_val:,.2f}, Mortgage: £{mortgage_bal:,.2f})")
    print(f"Calculated Total Cash: £{total_cash:,.2f}")
    print(f"Calculated Loans: £{ms_loan_bal:,.2f}")

    # 3. Update Ghostfolio
    # Account IDs in Ghostfolio (Retrived via investigation)
    # Home Equity: 'home-equity-uid'
    # Cash: 'cash-uid'
    # Loans: 'loans-uid'
    
    # FETCH GHOSTFOLIO ACCOUNTS TO MAP NAMES TO IDS
    gf_accounts = ghostfolio_api.get_accounts(gf_url, gf_token)
    if "error" in gf_accounts:
        print(f"Error fetching Ghostfolio accounts: {gf_accounts['error']}")
        sys.exit(1)

    account_data_map = {acc['name']: acc for acc in gf_accounts.get('accounts', [])}
    
    target_mappings = [
        ("Home Equity", home_equity),
        ("Cash", total_cash),
        ("Loans", ms_loan_bal)
    ]

    for name, bal in target_mappings:
        acc_data = account_data_map.get(name)
        if acc_data:
            print(f"Updating Ghostfolio Account '{name}' ({acc_data['id']}) to £{bal:,.2f}...")
            res = ghostfolio_api.update_account(gf_url, gf_token, acc_data, bal)
            if "error" in res:
                print(f"  Error updating {name}: {res['error']}")
        else:
            print(f"Warning: Ghostfolio Account '{name}' not found.")

    print("\nGhostfolio Synchronisation Complete.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 11-ghostfolio-sync.py <staging_dir>")
        sys.exit(1)
    main(sys.argv[1])
