# Learnings

Corrections, insights, and knowledge gaps captured during development.

**Categories**: correction | insight | knowledge_gap | best_practice

---

## [LRN-20250619-001] best_practice

**Logged**: 2025-06-19T17:15:00Z
**Priority**: medium
**Status**: pending
**Area**: config

### Summary
Must create `.learnings/` directory with `folder_create` before writing files with `file_write`.

### Details
When initialising the self-improvement skill, `file_write` for `.learnings/LEARNINGS.md`, `.learnings/ERRORS.md`, and `.learnings/FEATURE_REQUESTS.md` all returned ENOENT because the directory did not exist. The folder tool (`folder_create`) was not initially available, blocking setup until Stephen granted access. Once the directory existed, all three files wrote successfully.

### Suggested Action
In setup workflows that create files in new directories, always create the directory first via `folder_create` (or `mkdir -p`) before writing files.

### Metadata
- Source: error_recovery
- Related Files: .learnings/LEARNINGS.md, .learnings/ERRORS.md, .learnings/FEATURE_REQUESTS.md
- Tags: setup, tooling, filesystem

---

