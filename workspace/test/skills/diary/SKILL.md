---
name: "diary"
description: "Master Diary SOP: Absolute paths for lobster flows and mandatory 30s timeouts."
---

## Flows

### 1. Create/Re-run Daily Diary (diary.lobster)
Generates or updates the daily diary entry by pulling health data and combining it with existing content.
- **Pipeline Path:** `/home/node/.openclaw/workspace/flows/diary/diary.lobster`
- **Timeout:** Mandatory **30,000ms** (`timeoutMs: 30000`).
- **Command Template:**
```json
lobster(
  action="run",
  pipeline="/home/node/.openclaw/workspace/flows/diary/diary.lobster",
  argsJson='{"date": "YYYY-MM-DD"}',
  timeoutMs=30000
)
```

### 2. Update/Append Diary (append.lobster)
Appends new content to an existing diary entry for a specific date.
- **Pipeline Path:** `/home/node/.openclaw/workspace/flows/diary/append.lobster`
- **Timeout:** Mandatory **30,000ms** (`timeoutMs: 30000`).
- **Command Template:**
```json
lobster(
  action="run",
  pipeline="/home/node/.openclaw/workspace/flows/diary/append.lobster",
  argsJson='{"date": "YYYY-MM-DD", "content": "Text to append"}',
  timeoutMs=30000
)
```

## Protocol & Safety
- **Absolute Paths:** Always use the full absolute path for the `pipeline` argument.
- **Timeouts:** Never omit the `timeoutMs: 30000` parameter as these flows involve multiple LLM calls.
- **Date Format:** Dates must always be in `YYYY-MM-DD` format.
- **Storage:** Entries are mastered in the Wiki Vault: `/home/node/.openclaw/wiki/agents/sebastian/Diary/`.
