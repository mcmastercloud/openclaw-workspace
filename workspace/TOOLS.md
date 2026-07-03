### Lobster Flow LLM Standard
- **LLM Wrapper:** Always use the `/opt/custom-tools/llm_invoke` utility for LLM tasks within Lobster pipelines.
- **Usage:** `/opt/custom-tools/llm_invoke "<prompt_text>" "<data_file_in_data_dir>" "<prompt_file_in_prompts_dir>"`
- **Pipeline Architecture (Data Passing):**
    - **Isolation:** Each step should output its JSON result to a discrete file in the `data/` directory (e.g., `run: ... > "/home/node/.openclaw/workspace/data/step_result.json"`).
    - **Composition:** When a task requires inputs from multiple previous steps, use `jq` to combine those discrete files into a single structured JSON payload before calling `llm_invoke`.
    - **Structured Wrappers:** Ensure the final formatting LLM task returns its output inside a JSON container (e.g., a `"response"` key) to maintain pipeline stability.
- **Index Note:** When calling via `exec` or standardized shell wrappers, ensure positional arguments match the script's expected `argv` indexing (Prompt, Payload, PromptFile).
- **Lobster Integration:** In `.lobster` files, use the absolute path `/opt/custom-tools/llm_invoke`.

### Diary Skill & Lobster Flows
- **Skill File**: `~/.openclaw/workspace/skills/diary/SKILL.md` — Master SOP for diary creation and update flows.
- **Create/Re-run Daily Diary**: `lobster(action="run", pipeline="/home/node/.openclaw/workspace/flows/diary/diary.lobster", argsJson='{"date": "YYYY-MM-DD"}', timeoutMs=30000)` — generates/updates the daily entry by pulling health/sleep/workout data.
- **Append to Diary**: `lobster(action="run", pipeline="/home/node/.openclaw/workspace/flows/diary/append.lobster", argsJson='{"date": "YYYY-MM-DD", "content": "Text to append"}', timeoutMs=30000)` — appends content to an existing entry.
- **Storage**: Entries mastered in `/home/node/.openclaw/wiki/agents/sebastian/Diary/`.
- **Critical**: Absolute paths only. Never omit `timeoutMs: 30000`. Dates in `YYYY-MM-DD` format.

### Networking
- **DNS Lookups/IP Resolution:** `getent hosts <hostname>`

### Withings Family Health Tracker
- **CLI:** `python3 /home/node/.openclaw/workspace/skills/withings-family/scripts/withings.py`
- **Capabilities:** Fetches weight, body composition, activity, and sleep data for multiple users.
- **Usage Examples:**
  - `python3 scripts/withings.py <userId> weight`
  - `python3 scripts/withings.py <userId> body`
  - `python3 scripts/withings.py <userId> activity <days>`
  - `python3 scripts/withings.py <userId> sleep <days>`
- **Storage:** Tokens stored in `~/.openclaw/withings-family/tokens-<userId>.json`.

### Hevy Workout Tracker
- CLI: `hevy`
- Capabilities: Track workouts, manage routines, exercise templates, and progress history.
- Path: `/home/node/.openclaw/workspace/skills/hevy`
- Usage: Use when querying workout data, routines, or exercise history. See `SKILL.md` in the skill folder for full command details.

### Email Management (Himalaya)
- **CLI:** `himalaya`
- **Capabilities:** Manage business and personal email accounts (IMAP/SMTP).
- **Usage:**
  - List envelopes: `himalaya envelope list --account <business|personal> --folder <folder_path>`
  - Read message: `himalaya message read <id>`
