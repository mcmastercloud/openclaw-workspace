---
name: "monthly-diary-summary"
description: "SOP for generating monthly diary summaries including fitness, work, family, and tech themes."
---

# Monthly Diary Summary SOP

## Overview
Generate a narrative monthly summary on the 1st of each month for the preceding month.

## Format Requirements
- **Title**: `<Month Name> - Summary`
- **Structure (Front-matter + Narrative Sections)**:
  - `type: diary-summary`, `month: XX`, `year: YYYY`, `date: YYYY-MM-DD`
  - Narrative Sections (with emojis):
    1. **Work & Leadership**: Client focus, delegation, team support, leadership milestones.
    2. **Family & Personal**: Major events, home projects, personal updates, family health.
    3. **Fitness & Well-being**: Training cadence, key workouts, volume trends.
    4. **Technology & Infrastructure**: Technical upgrades, tool maintenance, infrastructure health.
- **Narrative tone**: Professional, introspective, structured, and comprehensive.

## Workflow
1. Fetch all `.md` files for the relevant month folder.
2. Extract highlights using targeted `grep` for headers (Work, Fitness, Personal, Family, Technology).
3. Synthesize content into the specified narrative sections.
4. Save file to `/home/node/.openclaw/wiki/agents/sebastian/Diary/YYYY/MM/<Month Name> - Summary.md`.
