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

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

## Related

- [Agent workspace](/concepts/agent-workspace)
