# Learnings - 2026-06-04

- **TaskFlow Orchestration:** Always use `taskflow_orchestrator.py` as the entry point for financial syncs. Avoid legacy scripts like `run_pipeline.sh`.
- **Environment Parity:** Financial scripts (11, 12) must accept `staging_dir` as a positional argument rather than relying on environment variables to maintain consistency with the pipeline's modular directory structure.
- **Symlink Management:** The `LATEST` symlink in `finance-staging/` is critical for cross-script discovery and should be updated automatically by the final loader step (Step 10).
- **Symbolic Link Resolution:** Shared configuration files like `USER.md` and `COMMON.md` are symlinks. If they appear "missing," they must be accessed via their explicit absolute paths or resolved targets.
- **API-First Operations:** Trigger database restores via the Docker Management API (`restore_firefly_api.py`) rather than direct SSH subprocesses to ensure consistent logging and authentication.
- **Look-back Window:** Reduced the default Starling transaction look-back buffer from 35 days to 7 days to improve reliability and reduce ingestion noise.
