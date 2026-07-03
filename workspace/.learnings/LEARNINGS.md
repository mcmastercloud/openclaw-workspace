# Learnings Log

- [2026-06-03] Signal: Avoid running competing Signal daemons on different servers for the same account; it causes identity key clashes.
- [2026-06-03] Ontology: Always use `scripts/ontology.py` rather than manual file operations to ensure schema validation and proper JSONL line structure (`{"op":"...", "entity":{...}}`).
- [2026-06-03] Tools: Use `message_invoke` for Signal notifications within Lobster flows; it simplifies proactive messaging from the shell.
