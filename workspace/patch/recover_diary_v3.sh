#!/bin/bash
DB_ID="383b2203-a808-4eea-9012-8207b5578fa2"
NTN="/home/node/.npm-global/bin/ntn"
WORKSPACE="/home/node/.openclaw/workspace/diary"

echo "Starting robust recovery v3..."

find "$WORKSPACE" -name "*.md" | while read -r DIARY_PATH; do
    FILENAME=$(basename "$DIARY_PATH")
    
    if [[ "$FILENAME" =~ ^([0-9]{4}-[0-9]{2}-[0-9]{2}) ]]; then
        DATE="${BASH_REMATCH[1]}"
    elif [[ "$DIARY_PATH" =~ ([0-9]{4})/([0-9]{2})/([0-9]{2})\.md$ ]]; then
        DATE="${BASH_REMATCH[1]}-${BASH_REMATCH[2]}-${BASH_REMATCH[3]}"
    else
        echo "Skipping non-dated file: $DIARY_PATH"
        continue
    fi

    echo "Querying Notion for $DATE..."
    
    # Use jq to build the JSON string and pass via heredoc to prevent shell escaping issues
    PAGE_ID=$(jq -n --arg date "$DATE" '{"filter":{"property":"Date","date":{"equals":$date}}}' | $NTN api "v1/databases/$DB_ID/query" --method POST --notion-version 2022-06-28 -- - | jq -r '.results[0].id // empty')
    
    if [ -n "$PAGE_ID" ] && [ "$PAGE_ID" != "null" ]; then
        echo "✅ Found $PAGE_ID. Restoring..."
        $NTN pages update "$PAGE_ID" --notion-version 2022-06-28 < "$DIARY_PATH" > /dev/null
        
        # Set Type property
        jq -n '{"properties":{"Type":{"select":{"name":"Entry"}}}}' | $NTN api "v1/pages/$PAGE_ID" --method PATCH --notion-version 2022-06-28 -- - > /dev/null
    else
        echo "❌ Page not found for $DATE"
    fi
    # Sleep slightly to stay within rate limits for bulk updates
    sleep 0.5
done

echo "Recovery complete."
