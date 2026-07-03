# SOP: Morning Brief Workflow (Lobster)

## Objective
Provide a concise, data-driven morning brief via a robust Lobster pipeline.

## Procedure (Lobster Pipeline)

1. **Fetch Workout Data:**
   - Run `hevy workouts list` and save to `data/workout.json`.
   
2. **Summarize Workout:**
   - Use `llm_invoke` with the `workout_summary` prompt to process `workout.json`.
   - Save output to `data/final_workout.json`.

3. **Fetch Social Media:**
   - Run `inoreader.sh` for the "General Cloud" feed and save to `data/inoreader.json`.
   
4. **Analyze Social Media:**
   - Use `llm_invoke` with the `social_media_summary` prompt to process `inoreader.json`.
   - Save output to `data/final_social.json`.

5. **Combine & Format:**
   - Use `jq` to merge `final_workout.json` and `final_social.json` into `data/brief_combined.json`.
   - Use `llm_invoke` with the `morning_brief_formatter` prompt to generate the final human-readable brief.
   - The formatter MUST return the text inside a JSON object: `{"response": "..."}`.

## Execution Rules
- **Tooling:** Always use the `/opt/custom-tools/llm_invoke` wrapper.
- **Data Passing:** Use discrete files in `data/` for cross-step communication; never rely on raw stdout piping between complex LLM steps.
- **Pathing:** Always use absolute paths within the Lobster `.lobster` file.
