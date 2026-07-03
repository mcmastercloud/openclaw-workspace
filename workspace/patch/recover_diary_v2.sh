#!/bin/bash
DB_ID="383b2203-a808-4eea-9012-8207b5578fa2"
NTN="/home/node/.npm-global/bin/ntn"
WORKSPACE="/home/node/.openclaw/workspace/diary"

echo "Starting robust recovery..."

find "$WORKSPACE" -name "*.md" | while read -r DIARY_PATH; do
    FILENAME=$(basename "$DIARY_PATH")
    
    # Check if filename is YYYY-MM-DD
    if [[ "$FILENAME" =~ ^([0-9]{4}-[0-9]{2}-[0-9]{2}) ]]; then
        DATE="${BASH_REMATCH[1]}"
    # Check if path is YYYY/MM/DD.md
    elif [[ "$DIARY_PATH" =~ ([0-9]{4})/([0-9]{2})/([0-9]{2})\.md$ ]]; then
        DATE="${BASH_REMATCH[1]}-${BASH_REMATCH[2]}-${BASH_REMATCH[3]}"
    else
        echo "Skipping non-dated file: $DIARY_PATH"
        continue
    fi

    echo "Processing $DATE ($DIARY_PATH)..."
    
    SEARCH_JSON="{\"filter\":{\"property\":\"Date\",\"date\":{\"equals\":\"$DATE\"}}}"
    PAGE_ID=$($NTN api "v1/databases/$DB_ID/query" --method POST --notion-version 2022-06-28 -- "$SEARCH_JSON" | jq -r '.results[0].id // empty')
    
    if [ -n "$PAGE_ID" ] && [ "$PAGE_ID" != "null" ]; then
        # 1. Restore Content
        $NTN pages update "$PAGE_ID" --notion-version 2022-06-28 < "$DIARY_PATH" > /dev/null
        # 2. Fix Properties
        PROP_JSON='{"properties":{"Type":{"select":{"name":"Entry"}}}}'
        $NTN api "v1/pages/$PAGE_ID" --method PATCH --notion-version 2022-06-28 -- "$PROP_JSON" > /dev/null
        echo "✅ Restored $DATE"
    else
        echo "❌ Page not found for $DATE"
    fi
done

echo "Recovery complete."
