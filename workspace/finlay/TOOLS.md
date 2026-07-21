# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## Notion Access
- Skill: Installed via `/usr/local/lib/node_modules/openclaw/skills/notion`
- Tooling: Primary use `ntn` CLI (requires `NOTION_API_TOKEN`).
- Scope/Red Line: **Restrict all operations strictly to the Finance dashboard (`https://www.notion.so/Finance-33f6a781d35880f1ab39d1d3ca6098cf?v=3a12f0a118e841838fba86b94553cfa3&source=copy_link`) and its child pages.** Do not traverse outside this organizational subtree. Ignore all other Notion pages.

## Ontology (Knowledge Graph)
- **Tool:** `/home/node/.openclaw/workspace/skills/ontology/scripts/ontology.py`
- **Use Case:** Use for structured state, tracking complex relationships, and entity management.
    - **Entity CRUD:** Person, Project, Task, Event, Account.
    - **Linking:** Relate tasks to projects, events to attendees, or accounts to services.
    - **Constraints:** Define schema in `memory/ontology/schema.yaml` to prevent invalid mutations.
    - **Multi-step Plans:** Map complex changes as graph transformations to ensure logical consistency and audit logging.
- **Rules:** Append-only modifications (`jsonl`). Validate constraints before committing changes.

## Firefly III
- **Skill Route:** The skill instructions are located at `/home/node/.openclaw/workspace/finlay/skills/firefly-iii/SKILL.md`. This is a set of documentation containing cURL commands, and should not be run natively as a shell command. Use standard bash with curl.

## Obsidian (notesmd-cli)
- **Binary:** `/home/openclaw/.local/bin/notesmd-cli` (v0.3.6) — note: it's `notesmd-cli`, not `nodesmd-cli`.
- **Usage:** Operates on the Obsidian vault directly on disk. Headless-friendly; Obsidian does not need to be running.
- **Quick Reference:**
  - `notesmd-cli set-default "<vault-name>"` — set default vault
  - `notesmd-cli print-default --path-only` — show default vault path
  - `notesmd-cli search` — interactive fuzzy note search
  - `notesmd-cli search-content "query"` — full-text content search
  - `notesmd-cli create "Folder/Note" --content "..."` — create note
  - `notesmd-cli daily` — open today's daily note
  - `notesmd-cli frontmatter "Note" --print` / `--edit --key "k" --value "v"` / `--delete --key "k"`
  - `notesmd-cli move "old/path" "new/path"` — rename with wikilink refactoring
  - `notesmd-cli delete "path/to/note"`
- **Skill File:** Available in the skill manifest at `.openclaw/sandbox-skills/skills/obsidian-notesmd-cli/SKILL.md` (accessible via `exec` cat on the sandbox path `/workspace/.openclaw/sandbox-skills/skills/obsidian-notesmd-cli/SKILL.md`).

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

## Related

- [Agent workspace](/concepts/agent-workspace)
\n\n## File Operations\nUse the  tool to avoid direct shell commands for file system interactions. This improves safety and enforces allowed path restrictions:\n\n* file ls\n* file read\n* file write\n* file append\n* file delete\nf file mkdir\n* file rmdir\nf file copy\n* file move\n* file rename\n* file insert\n\n## Example usage:\nfile ls /workspace --wide\n\n\n