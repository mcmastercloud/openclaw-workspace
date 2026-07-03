# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

### 🗄️ Wiki & Vault Management
- **Wiki Vault (`memory-wiki`):** The primary knowledge repository for curated, provenance-aware pages. Use `wiki_search`, `wiki_get`, and `wiki_apply` for retrieval and metadata updates.
- **Obsidian Integration:** Use the `obsidian-notesmd-cli` skill (`/home/node/.openclaw/workspace/skills/obsidian-notesmd-cli`) for managing Markdown-based notes in the Obsidian-compatible vault structure.
- **Durable Documentation:** All merged strategic business objectives are maintained in `agents/nathaniel/Business Objectives.md` within the wiki vault. Perform deduplication and merging periodically to maintain a clean source of truth.

### 🧠 Memory Management (Layered Approach)
- **Local:** `MEMORY.md` and `memory/*.md` for agent-specific work context.
- **Shared:** `/home/node/.openclaw/memory-shared` for reusable organizational standards and runbooks.
- **Wiki:** Curated enterprise/strategic knowledge.
- **Ontology (Skill):** For typed entities and explicit relationship mapping.

### 🔄 Memory Retrieval Strategy
- Always favor `memory_search` for environment-specific recall, and `wiki_search`/`wiki_get` for curated strategic knowledge.
- If an index failure occurs (embedding model discord), perform file-based inspection of `MEMORY.md` as a fallback truth source until re-indexing is confirmed.
