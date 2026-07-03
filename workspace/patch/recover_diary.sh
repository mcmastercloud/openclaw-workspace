#!/bin/bash
DB_ID="383b2203-a808-4eea-9012-8207b5578fa2"
NTN="/home/node/.npm-global/bin/ntn"
WORKSPACE="/home/node/.openclaw/workspace/diary"

echo "Starting recovery of diary content from local files..."

# Find all diary files in the workspace
find "$WORKSPACE" -name "*.md" | while read -r DIARY_PATH; do
    # Extract filename: "2026-05-31 - Sunday.md"
    FILENAME=$(basename "$DIARY_PATH")
    # Extract date: "2026-05-31"
    DATE=$(echo "$FILENAME" | cut -d' ' -f1)
    
    echo "Recovering $FILENAME ($DATE)..."
    
    # Find the page ID for this date
    SEARCH_JSON="{\"filter\":{\"property\":\"Date\",\"date\":{\"equals\":\"$DATE\"}}}"
    PAGE_ID=$($NTN api "v1/databases/$DB_ID/query" --method POST --notion-version 2022-06-28 -- "$SEARCH_JSON" | jq -r '.results[0].id // empty')
    
    if [ -n "$PAGE_ID" ] && [ "$PAGE_ID" != "null" ]; then
        echo "Found page ID: $PAGE_ID. Restoring content..."
        # Restore content and set the Type property correctly this time
        $NTN pages update "$PAGE_ID" --notion-version 2022-06-28 < "$DIARY_PATH"
        
        # Now set the property correctly using the 'api' PATCH method instead of 'pages update' for content
        PROP_JSON='{"properties":{"Type":{"select":{"name":"Entry"}}}}'
        $NTN api "v1/pages/$PAGE_ID" --method PATCH --notion-version 2022-06-28 -- "$PROP_JSON" > /dev/null
        
        echo "Restored $DATE successfully."
    else
        echo "Could not find Notion page for $DATE. Skipping."
    fi
done

echo "Recovery complete."
