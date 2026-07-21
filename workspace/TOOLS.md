### Diary Operations
- Use the `diary_*` plugin tools for all diary operations (create, read, replace sections, append sections, add sleep/exercise data).
- **Storage**: Entries mastered in `/home/node/.openclaw/wiki/agents/sebastian/Diary/`.

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
