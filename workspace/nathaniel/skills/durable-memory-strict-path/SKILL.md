---
name: "durable-memory-strict-path"
description: "Mandatory directive: all durable knowledge and agent memory MUST be stored/retrieved from ~/wiki/agents/nathaniel."
---

# Durable Memory Protocol

## Directive
All agent durable memory, wiki knowledge, and project documentation MUST be stored, retrieved, and managed exclusively within the dedicated agent subfolder:
`/home/node/.openclaw/wiki/agents/nathaniel/`

## Implementation
1. **Scope Restriction:** Do not store or look for documentation in the wiki root (`/home/node/.openclaw/wiki/`) or orphaned subfolders.
2. **Search:** All `wiki_search`, `wiki_get`, and `wiki_apply` operations must be scoped/contextualized to this path.
3. **Exceptions:** None. If relevant information is found elsewhere, it must be migrated to `~/wiki/agents/nathaniel/` and verified.

This ensures all strategic business objectives, leadership feedback, and project assets are centralized and discoverable.
