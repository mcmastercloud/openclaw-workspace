#!/bin/bash
# Diary Cover and Icon Patch Script
# Targets all pages in the Personal Journal database to match a specific icon and cover.

DB_ID="383b2203-a808-4eea-9012-8207b5578fa2"
NTN="/home/node/.npm-global/bin/ntn"

# Configuration based on requested reference page
COVER_URL="https://images.unsplash.com/photo-1462642109801-4ac2971a3a51?ixlib=rb-4.1.0&q=85&fm=jpg&crop=entropy&cs=srgb"
ICON_EMOJI="📖"

echo "Step 1: Fetching all diary page IDs..."
PAGES=$( $NTN api "v1/databases/$DB_ID/query" --method POST --notion-version 2022-06-28 | jq -r '.results[].id' )

if [ -z "$PAGES" ]; then
    echo "No pages found."
    exit 0
fi

echo "Step 2: Patching covers and icons via curl..."
for PAGE_ID in $PAGES; do
    echo "Updating $PAGE_ID..."
    curl -s "https://api.notion.com/v1/pages/$PAGE_ID" \
      -X PATCH \
      -H "Authorization: Bearer $NOTION_API_TOKEN" \
      -H "Notion-Version: 2022-06-28" \
      -H "Content-Type: application/json" \
      --data "{
        \"icon\": {
          \"type\": \"emoji\",
          \"emoji\": \"$ICON_EMOJI\"
        },
        \"cover\": {
          \"type\": \"external\",
          \"external\": {
            \"url\": \"$COVER_URL\"
          }
        }
      }" > /dev/null
    
    sleep 0.3
done

echo "Cover and Icon patch complete."
