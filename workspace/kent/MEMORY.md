# MEMORY.md

## Research Output Blueprint (Kent)
Stephen and I have finalized the structural and technical blueprint for all future research tasks. These instructions are also codified in my `SOUL.md`.

### 1. Structure & Tone
- **Tone:** Academic and objective. British English is mandatory. High-fidelity technical dossiers (minimum 1,000 words per PART).
- **Architecture:** 
  - Dynamic Master Key / slug generated for each report.
  - Hub-and-spoke Notion structure: A new Master Page **nested under** the "Kent's Research" Notion hub (Parent Page ID: `3326a781-d358-80e6-91c9-c37613e9d914`).
  - "PART" sub-pages nested under the report's Master Page.
  - No raw markdown: All elements (bold, italics, bullets) must be converted to native Notion rich-text blocks.
  - Em-dashes (—) are forbidden; use " - " instead.

### 2. Citations & Archiving
- **Style:** Modified IEEE format with inline short codes.
- **Zotero Hierachy:** All sources archived to Zotero prior to synthesis. Nested sub-collection named with the Master Key created under the "Kent" parent collection (`UHTSJAET`).
- **Trust Labels:** Every source must carry a categorical Trust Label (`[Trusted: Primary]` or `[Trusted: Secondary]`) in Extra metadata, Tags, and the Notion Citation Table.
- **Final Archive:** A consolidated .PDF of the final report generated and uploaded to Zotero upon completion.

### 3. Technical Stack
- **Models:** OpenRouter (`OPENROUTER_API_KEY`).
- **Engines:** 
  - Discovery/Extraction: Perplexity Sonar Pro and Tavily (Treated as RAW SOURCES only).
  - Heavy Synthesis: Google Gemini Pro handles all final report synthesis, native formatting, and professional composition.
- **Orchestration:** ClawFlow to manage state, multiplexing, and verifiable Notion delivery.

### 4. Notifications
- **Channel:** Signal (`agent:main:signal:direct:+447738375172`).
- **Protocol:** Real-time milestone updates (Initialization, Discovery, Synthesis, Publication, Archive).

### 5. Final Publication Audit Rule
To prevent missing elements on the Master Page (such as omitted Executive Summaries, missing Navigation sections, or incomplete Citation Tables), I must perform a **Pre-Flight Validation**:
- The IEEE Citation Table count must perfectly match the number of sources archived to Zotero.
- The Master Page payload must explicitly include the Executive Summary and Report Navigation native blocks.
- **Header Block & Table Forcing:** The Master Page MUST begin with a native Notion `paragraph` block containing the metadata (Master Key, Researcher, Client, Status) styled correctly. The IEEE Reference & Trust Table MUST be built using native Notion `table` and `table_row` JSON payloads, explicitly banning raw markdown `| :--- |` strings.
- **Header Block & Table Forcing:** The Master Page MUST begin with a native Notion `paragraph` block containing the metadata (Master Key, Researcher, Client, Status) styled correctly. The IEEE Reference & Trust Table MUST be built using native Notion `table` and `table_row` JSON payloads, explicitly banning raw markdown `| :--- |` strings.

### 6. Post-Incident Procedural Corrections (April 2026)
Following an execution fault on MK-CFE-2026, the following strict operational directives are now permanently in effect:
- **Execution Continuity (No Premature Yielding):** Upon completion of a sub-agent extraction phase, I must immediately chain the synthesis and Notion payload generation within the same operational loop. I am forbidden from yielding the turn with a "promise to act" status update.
- **Citation Mapping Verification:** Before generating the native Notion blocks for the Part sub-pages, I must explicitly map all extracted sources to an IEEE citation array (1 through N). These `[n]` citations must be injected into the markdown drafts *prior* to Notion JSON conversion.
- **Pre-Flight Validation Enforcement:** The Master Page payload must be constructed simultaneously with the Executive Summary and the full native Notion IEEE Reference Table. Pushing a bare Master Page is strictly prohibited.
- **Synthesis Engine Override:** OpenRouter is permanently stripped from the synthesis pipeline. I must exclusively utilise the direct Google Gemini API for all drafting phases.
- **Extraction Link Mandate:** Sub-agent extraction prompts must explicitly mandate the return of all raw source URLs. This ensures URLs are available for the Zotero archive and IEEE tables without requiring secondary discovery searches.
- **PowerPoint Archival Mandate:** All generated PowerPoint presentations (.pptx) must be explicitly uploaded to the associated Zotero sub-collection for the active Master Key. They should be structured as 'presentation' items with the file attached.

## Promoted From Short-Term Memory (2026-04-22)

<!-- openclaw-memory-promotion:memory:memory/2026-04-17.md:48:51 -->
- - Candidate: Reflections: Theme: `reflections` kept surfacing across 24 memories.; confidence: 1.00; evidence: memory/2026-04-17.md:9-9, memory/2026-04-17.md:18-18, memory/2026-04-17.md:18-21; note: reflection - confidence: 0.00 - evidence: memory/2026-04-17.md:48-51 - recalls: 0 [score=0.817 recalls=0 avg=0.620 source=memory/2026-04-17.md:3-6]
<!-- openclaw-memory-promotion:memory:memory/2026-04-17.md:52:55 -->
- - Candidate: Reflections: Theme: `1.00` kept surfacing across 22 memories.; confidence: 1.00; evidence: memory/2026-04-17.md:18-21, memory/2026-04-17.md:22-25, memory/2026-04-17.md:26-29; note: reflection - confidence: 0.00 - evidence: memory/2026-04-17.md:52-55 - recalls: 0 [score=0.817 recalls=0 avg=0.620 source=memory/2026-04-17.md:8-11]
<!-- openclaw-memory-promotion:memory:memory/2026-04-17.md:64:67 -->
- - Candidate: Reflections: Theme: `kept` kept surfacing across 19 memories.; confidence: 1.00; evidence: memory/2026-04-17.md:26-29, memory/2026-04-17.md:30-33, memory/2026-04-17.md:34-37; note: reflection - confidence: 0.00 - evidence: memory/2026-04-17.md:64-67 - recalls: 0 [score=0.817 recalls=0 avg=0.620 source=memory/2026-04-17.md:13-16]
<!-- openclaw-memory-promotion:memory:memory/2026-04-17.md:70:70 -->
- - Candidate: Possible Lasting Truths: No strong candidate truths surfaced. [score=0.817 recalls=0 avg=0.620 source=memory/2026-04-17.md:18-18]
