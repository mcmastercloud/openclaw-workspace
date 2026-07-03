name: diary-append
args:
  date: string
  content: string

steps:
  - id: read_existing
    run: |
      TARGET_DATE="${LOBSTER_ARG_DATE}"
      [ -z "$TARGET_DATE" ] && TARGET_DATE=$(date +%Y-%m-%d)
      YEAR=$(echo "$TARGET_DATE" | cut -d'-' -f1)
      MONTH=$(echo "$TARGET_DATE" | cut -d'-' -f2)
      DAY_NAME=$(date -d "$TARGET_DATE" +%A)
      
      DIARY_DIR="/home/node/.openclaw/wiki/agents/sebastian/Diary/$YEAR/$MONTH"
      DIARY_PATH="$DIARY_DIR/$TARGET_DATE - $DAY_NAME.md"
      
      if [ -f "$DIARY_PATH" ]; then
        # Capture the frontmatter properly (all lines from first --- to second ---)
        awk '/^---/{count++; print; if(count==2) exit; next} count==1{print}' "$DIARY_PATH" > "/home/node/.openclaw/workspace/data/diary/existing_frontmatter.md"
        
        # Capture content AFTER the second ---
        awk 'BEGIN{count=0} /^---/{count++; next} count>=2{print}' "$DIARY_PATH" > "/home/node/.openclaw/workspace/data/diary/existing_diary.md"
      else
        echo "Error: No diary entry found for $TARGET_DATE in the vault."
        exit 1
      fi

  - id: prepare_payload
    run: |
      ACTUAL_CONTENT="$LOBSTER_ARG_CONTENT"
      [ -z "$ACTUAL_CONTENT" ] && ACTUAL_CONTENT="$LOBSTER_ARG_MESSAGE"
      
      jq -n \
        --arg existing "$(cat /home/node/.openclaw/workspace/data/diary/existing_diary.md)" \
        --arg input "$ACTUAL_CONTENT" \
        --arg date "$TARGET_DATE" \
        '{date: $date, existing_content: $existing, input: $input}' > "/home/node/.openclaw/workspace/data/diary/append_payload.json"

  - id: merge_content
    run: /opt/custom-tools/llm_invoke "Merge and append the new input to the journal section of the existing content. Return the full updated diary text without an H1 title." "diary/append_payload.json" "diary_appender" > "/home/node/.openclaw/workspace/data/diary/appended_diary.json"

  - id: save_to_vault
    run: |
      TARGET_DATE="$LOBSTER_ARG_DATE"
      [ -z "$TARGET_DATE" ] && TARGET_DATE=$(date +%Y-%m-%d)
      YEAR=$(echo "$TARGET_DATE" | cut -d'-' -f1)
      MONTH=$(echo "$TARGET_DATE" | cut -d'-' -f2)
      DAY_NAME=$(date -d "$TARGET_DATE" +%A)
      
      DIARY_DIR="/home/node/.openclaw/wiki/agents/sebastian/Diary/$YEAR/$MONTH"
      DIARY_PATH="$DIARY_DIR/$TARGET_DATE - $DAY_NAME.md"
      
      CONTENT=$(jq -r '.json.response // .response // empty' "/home/node/.openclaw/workspace/data/diary/appended_diary.json")
      
      if [ -n "$CONTENT" ]; then
        # Re-apply frontmatter + appended content
        cat "/home/node/.openclaw/workspace/data/diary/existing_frontmatter.md" > "$DIARY_PATH"
        echo "" >> "$DIARY_PATH"
        echo "$CONTENT" >> "$DIARY_PATH"
      else
        echo "Error: Failed to parse merged content from LLM output."
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