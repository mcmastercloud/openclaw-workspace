---
name: finance-sync-master
description: Orchestrator for financial data synchronisation between Starling Bank and Firefly III.
version: 1.0.0
author: Finlay
---
# Finance-Sync-Master

Orchestrator for the McMaster Finance System: Full financial synchronisation between Starling Bank and Firefly III.

## Core Governance
This skill implements a rigorous 10-step pipeline designed to maintain the "Sacred Vow of Double-Entry". It prioritises accuracy over expediency and strictly enforces ledger integrity via a mandatory "Check 3" verification.

### 🛡️ Critical Failsafes
These steps are performed by the Orchestrator, and are only included here for your information.
- **Stop on Error**: Every step is monitored by the Master Orchestrator. If any script exits with a non-zero code or a check fails, execution **MUST** halt immediately. Never attempt to "force" a sync if Check 3 is imbalanced.
- **Audit Preservation**: Raw bank data is preserved in staging; transformations (mappings) only occur during the final Upload preparation (Step 09).

## Execution Protocol

All operations are controlled via the Master Orchestrator:
`python3 src/00-Sync-Master.py [FULL_RUN | DUMMY_RUN]`

### Standard Sync Modes
1. **DUMMY_RUN (Prepare & Verify)**: Executes Steps 01 through 09.
   - Discovers accounts, downloads history, reconciles deltas, and performs the **Check 3 Balances Verification**.
   - Prepares `uploads/*.txt` files and triggers a remote DB backup.
   - **Use this mode** to review the proposed updates and ensure all mismatches are accounted for (e.g., pending transactions).
   
2. **FULL_RUN (Commit to Ledger)**: Executes Steps 01 through 10.
   - Performs all verification in Dummy mode, then proceeds to **Step 10 (Firefly Delta Loader)**.
   - **Only use this mode** once the Dummy Run's `sync_log.txt` has been verified and Check 3 balances (allowing for Pending transactions).

## The 10-Step Pipeline

| Step | Script | Logic |
| :--- | :--- | :--- |
| **01** | `01-starling-account-discovery.py` | Map accounts/spaces and capture bank balances. |
| **02** | `02-starling-transaction-download.py` | Download STARLING SETTLED + PENDING history. |
| **03** | `03-firefly-account-discovery.py` | Extract Starling GUIDs from Firefly metadata. |
| **04** | `04-firefly-cache-refresh.py` | Pull exhaustive Firefly transaction history for matching. |
| **05** | `05-cross-account-deduplication.py` | Filter internal transfers based on Account Precedence. |
| **06** | `06-delta-reconciliation.py` | Identify true missing items since the Anchor Date. |
| **07** | `07-check-3-verification.py` | **GATEKEEPER**: `Bank Balance == Firefly + Delta` check. |
| **09** | `09-prepare-upload-files.py` | Applies `category-mapping.json` to create Upload files. |
| **10** | `10-firefly-delta-loader.py` | **POST-FLIGHT**: Commit Uploads to the live ledger. |

## Maintenance & Restoration

### 🚨 Emergency Restore
If the ledger state becomes corrupted or out-of-sync, an emergency restore can be triggered manually:
`python3 src/99-restore-firefly.py <backup_filename.tar.gz>`
*Note: This is isolated from the main sync pipeline and should be used with extreme caution.*

### 🗺️ Account Mapping
Mappings between Starling GUIDs and Firefly Asset Account IDs are managed in `category-mapping.json`. This ensures "Stephen McMaster & Samuel Reid" (Starling) maps correctly to "Starling Joint" (Firefly ID 549) as a **Transfer**.

## Logging & Staging
Every run generates a unique GUID subdirectory in `finance-staging/`.
Review `sync_log.txt` in the staging folder for a complete timestamped audit trail of all script outputs and validation checks.

