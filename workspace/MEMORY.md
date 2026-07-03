# Sebastien's Memory File

## Agent Communication Protocol (A2A)
When Stephen instructs me to communicate with other agents (nathaniel, nathan, finlay, archer, or kent), I MUST use the Agent-to-Agent (A2A) messaging capability. I am FORBIDDEN from using Signal or other external channels to communicate with these agents.

- **Agents:** nathaniel (or nathan), finlay, archer, kent.
- **Protocol:** Use `sessions_send` or appropriate orchestration tools (e.g., `clawflow`) to interact with these identities internally.
- **Exceptions:** Never attempt to call these names as external messaging targets.

## Operational Preferences
- **Lobster Orchestration:** Lobster MUST be used for all multi-step tasks where possible. When executing a flow, you **MUST** provide the full absolute path to the `.lobster` file (e.g., `/home/node/.openclaw/workspace/flows/diary/diary.lobster`) as the `pipeline` argument. (Updated: 2026-06-06)
- **Memory Governance:** Following `SOP_MEMORY_POLICY.md`. Ontology handles the "What/Who/How" (structured), while LanceDB handles the "Why/Context" (semantic). (Logged: 2026-06-02)
- **Workspace Hygiene:** Temporary scripts go in `patch/`, JSON/data files go in `data/`. The workspace root must stay clutter-free. (Added: 2026-06-13)

## Stephen McMaster: Personal & Preference Insight
- **Operating Rhythm:** Morning thinking blocks (uninterrupted, no inbox access), 9:00 PM hard cut-off with gym session (weights/treadmill) as circuit breaker. If evening commitments exist, pull gym to 06:00 AM. 12+ hour cognitive days enabled by mid-week travel (not cannibalizing partner time).
- **Interests/Values:** Stephen is a 'people person' - he values objectives that provide personal fulfillment and positive human impact (e.g., NOW Group, PROUD, leading S&A) even if they don't perfectly align with the metrics of his partner case.

## Health
- Withings watch does not record REM sleep; it only captures sleep duration and deep sleep.
- **Purpose**: Create, update, and manage daily diary entries with integrated health/sleep data.
- **Creation Flow**: `diary.lobster` — generates or updates the daily diary entry by pulling health data and combining it with existing content.
  - Path: `/home/node/.openclaw/workspace/flows/diary/diary.lobster`
  - Args: `{"date": "YYYY-MM-DD"}` (defaults to current date if omitted)
  - Timeout: 30,000ms
- **Append Flow**: `append.lobster` — appends new content to an existing diary entry for a specific date.
  - Path: `/home/node/.openclaw/workspace/flows/diary/append.lobster`
  - Args: `{"date": "YYYY-MM-DD", "content": "Text to append"}`
  - Timeout: 30,000ms
- **Skill File**: `~/.openclaw/workspace/skills/diary/SKILL.md` — Master Diary SOP with full protocol.
- **Storage**: Entries are mastered in the Wiki Vault: `/home/node/.openclaw/wiki/agents/sebastian/Diary/`.
- **Protocol**: Always use absolute paths for pipelines. Never omit `timeoutMs: 30000`. Dates in `YYYY-MM-DD` format.

## Diary Patching Protocol
When performing bulk operations on diary entries:
- **Location**: Use `/home/node/.openclaw/workspace/patch/` for scripts/logs.
- **Reference**: See `memory/diary_patching.md` for full SOP.

## Memory Promotion
- **Memory Promotion (2026-06-05):** Added dream diary entry for June 5th, 2026, marking the conclusion of today's memory promotion cycle.

## Promoted From Short-Term Memory (2026-06-10)

<!-- openclaw-memory-promotion:memory:memory/2026-06-03.md:3:6 -->
- Diary Entry - 2026-06-03: Met with client Jamie today and had a great conversation about Product Operating Models for delivery.; My flight was, unfortunately, delayed by almost 3 hours and I have just landed this minute.; I spoke to a team member - Ian - he is struggling because he thinks he has been thrown under the bus by a senior colleague. I think I have settled him down - I have suggested that he, his people lead, and I sit down to discuss his career plan at Deloitte.; Overall, a good day. However, I have a tonne of meetings tomorrow!! [score=0.835 recalls=0 avg=0.620 source=memory/2026-06-03.md:3-6]
<!-- openclaw-memory-promotion:memory:memory/2026-06-03.md:9:10 -->
- Health: Steps: Not tracked; Total Sleep: Not tracked [score=0.835 recalls=0 avg=0.620 source=memory/2026-06-03.md:9-10]

## Promoted From Short-Term Memory (2026-06-16)

<!-- openclaw-memory-promotion:memory:memory/2026-06-09.md:14:14 -->
- Work: Spent a lot of time working through pricing for the Qatar bid. [score=0.819 recalls=0 avg=0.620 source=memory/2026-06-09.md:14-14]
<!-- openclaw-memory-promotion:memory:memory/2026-06-09.md:17:18 -->
- Personal: Samuel made a lovely dinner of fish pie and chips.; Weather: It has been pouring today. [score=0.819 recalls=0 avg=0.620 source=memory/2026-06-09.md:17-18]
<!-- openclaw-memory-promotion:memory:memory/2026-06-09.md:21:22 -->
- News & Context: News reported a Sudanese immigrant tried to behead someone in Belfast on Monday night.; The people of Belfast are out in the streets rioting and burning immigrants' homes, cars, and a bus. Immigration has become a major flashpoint and people are ANGRY. [score=0.819 recalls=0 avg=0.620 source=memory/2026-06-09.md:21-22]
<!-- openclaw-memory-promotion:memory:memory/2026-06-09.md:25:27 -->
- Future Plans: Travelling to London tomorrow for work.; Two days in Cheltenham.; Saturday in Cardiff for Pride! [score=0.819 recalls=0 avg=0.620 source=memory/2026-06-09.md:25-27]

## Promoted From Short-Term Memory (2026-06-19)

<!-- openclaw-memory-promotion:memory:memory/2026-06-14-synology-task.md:1:1 -->
- Synology task completed: #8UAENA5KxgbqF1T [score=0.806 recalls=0 avg=0.620 source=memory/2026-06-14-synology-task.md:1-1]
