name: diary
args:
  date: string

steps:
  - id: clean_temp
    run: |
      rm -rf /home/node/.openclaw/workspace/data/diary
      mkdir -p /home/node/.openclaw/workspace/data/diary

  - id: check_existing_diary
    run: |
      TARGET_DATE="$LOBSTER_ARG_DATE"
      [ -z "$TARGET_DATE" ] && TARGET_DATE=$(date +%Y-%m-%d)
      YEAR=$(echo "$TARGET_DATE" | cut -d'-' -f1)
      MONTH=$(echo "$TARGET_DATE" | cut -d'-' -f2)
      DAY_NAME=$(date -d "$TARGET_DATE" +%A)
      
      DIARY_DIR="/home/node/.openclaw/wiki/agents/sebastian/Diary/$YEAR/$MONTH"
      DIARY_PATH="$DIARY_DIR/$TARGET_DATE - $DAY_NAME.md"
      
      if [ -f "$DIARY_PATH" ]; then
        sed '1,/---/d; /---/d' "$DIARY_PATH" > "/home/node/.openclaw/workspace/data/diary/existing_diary.md"
      else
        echo "" > "/home/node/.openclaw/workspace/data/diary/existing_diary.md"
      fi

  - id: fetch_hevy
    run: |
      TARGET_DATE="$LOBSTER_ARG_DATE"
      [ -z "$TARGET_DATE" ] && TARGET_DATE=$(date +%Y-%m-%d)
      /opt/venv/bin/hevy workouts list --page-size 5 --format json | jq --arg today "$TARGET_DATE" '[.[] | select(.start_time | startswith($today))]' > "/home/node/.openclaw/workspace/data/diary/workout.json"

  - id: summarize_workout
    run: /opt/custom-tools/llm_invoke "Summarize workout." "diary/workout.json" "workout_summary" > "/home/node/.openclaw/workspace/data/diary/final_workout.json"

  - id: fetch_withings_workouts
    run: |
      TARGET_DATE="$LOBSTER_ARG_DATE"
      [ -z "$TARGET_DATE" ] && TARGET_DATE=$(date +%Y-%m-%d)
      python3 /home/node/.openclaw/workspace/skills/withings-family/scripts/withings.py stephen workouts 1 > "/home/node/.openclaw/workspace/data/diary/withings_workouts.json"

  - id: summarize_withings_workouts
    run: /opt/custom-tools/llm_invoke "Summarize Withings workouts (runs)." "diary/withings_workouts.json" "workout_summary" > "/home/node/.openclaw/workspace/data/diary/final_withings_workouts.json"

  - id: fetch_withings
    run: |
      TARGET_DATE="$LOBSTER_ARG_DATE"
      [ -z "$TARGET_DATE" ] && TARGET_DATE=$(date +%Y-%m-%d)
      python3 /home/node/.openclaw/workspace/skills/withings-family/scripts/withings.py stephen sleep 1 > "/home/node/.openclaw/workspace/data/diary/sleep.json"

  - id: summarize_sleep
    run: /opt/custom-tools/llm_invoke "Summarize sleep." "diary/sleep.json" "sleep_summary" > "/home/node/.openclaw/workspace/data/diary/final_sleep.json"

  - id: combine_diary
    run: |
      TARGET_DATE="$LOBSTER_ARG_DATE"
      [ -z "$TARGET_DATE" ] && TARGET_DATE=$(date +%Y-%m-%d)
      jq -n \
        --slurpfile workout /home/node/.openclaw/workspace/data/diary/final_workout.json \
        --slurpfile sleep /home/node/.openclaw/workspace/data/diary/final_sleep.json \
        --slurpfile withings_workouts /home/node/.openclaw/workspace/data/diary/final_withings_workouts.json \
        --arg existing "$(cat /home/node/.openclaw/workspace/data/diary/existing_diary.md)" \
        --arg date "$TARGET_DATE" \
        '{date: $date, health: {sleep: $sleep[0].json, workout: $workout[0].json, withings_workouts: $withings_workouts[0].json}, existing_content: $existing}' > "/home/node/.openclaw/workspace/data/diary/diary_combined.json"

  - id: format_diary
    run: /opt/custom-tools/llm_invoke "Merge and format. Remove H1 title." "diary/diary_combined.json" "diary_formatter" > "/home/node/.openclaw/workspace/data/diary/formatted_diary.json"

  - id: save_to_vault
    run: |
      TARGET_DATE="$LOBSTER_ARG_DATE"
      [ -z "$TARGET_DATE" ] && TARGET_DATE=$(date +%Y-%m-%d)
      YEAR=$(echo "$TARGET_DATE" | cut -d'-' -f1)
      MONTH=$(echo "$TARGET_DATE" | cut -d'-' -f2)
      DAY=$(echo "$TARGET_DATE" | cut -d'-' -f3)
      DAY_NAME=$(date -d "$TARGET_DATE" +%A)
      
      DIARY_DIR="/home/node/.openclaw/wiki/agents/sebastian/Diary/$YEAR/$MONTH"
      DIARY_PATH="$DIARY_DIR/$TARGET_DATE - $DAY_NAME.md"
      mkdir -p "$DIARY_DIR"
      
      CONTENT=$(jq -r '.json.response // .response // empty' "/home/node/.openclaw/workspace/data/diary/formatted_diary.json")
      
      if [ -n "$CONTENT" ]; then
        echo "---" > "$DIARY_PATH"
        echo "type: diary" >> "$DIARY_PATH"
        echo "date: $TARGET_DATE" >> "$DIARY_PATH"
        echo "month: $MONTH" >> "$DIARY_PATH"
        echo "day: $DAY" >> "$DIARY_PATH"
        echo "tags:" >> "$DIARY_PATH"
        echo "  - journal" >> "$DIARY_PATH"
        echo "  - diary" >> "$DIARY_PATH"
        echo "banner: https://images.unsplash.com/photo-1483546363825-7ebf25fb7513?ixlib=rb-4.1.0&q=85&fm=jpg&crop=entropy&cs=srgb&w=6000" >> "$DIARY_PATH"
        echo "---" >> "$DIARY_PATH"
        echo "" >> "$DIARY_PATH"
        echo "$CONTENT" >> "$DIARY_PATH"
      else
        exit 1
      fi

  - id: sync_to_signal
    run: |
      TARGET_DATE="$LOBSTER_ARG_DATE"
      [ -z "$TARGET_DATE" ] && TARGET_DATE=$(date +%Y-%m-%d)
      YEAR=$(echo "$TARGET_DATE" | cut -d'-' -f1)
      MONTH=$(echo "$TARGET_DATE" | cut -d'-' -f2)
      DAY_NAME=$(date -d "$TARGET_DATE" +%A)
      DIARY_PATH="/home/node/.openclaw/wiki/agents/sebastian/Diary/$YEAR/$MONTH/$TARGET_DATE - $DAY_NAME.md"
      
      if [ -f "$DIARY_PATH" ]; then
        CONTENT=$(cat "$DIARY_PATH")
        /opt/custom-tools/message_invoke "signal:+447738375172" "$CONTENT"
      fi

  - id: output
    run: cat /home/node/.openclaw/workspace/data/diary/formatted_diary.json