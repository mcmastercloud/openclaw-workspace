#!/bin/bash
# Diary Property Patch Script
# Target: Set Type=Entry for all pages in the Personal Journal database where it is missing.

DB_ID="383b2203-a808-4eea-9012-8207b5578fa2"
NTN="/home/node/.npm-global/bin/ntn"

echo "Step 1: Fetching all diary page IDs..."
# We use ntn to query but curl to patch safely
PAGES=$( $NTN api "v1/databases/$DB_ID/query" --method POST --notion-version 2022-06-28 | jq -r '.results[] | select(.properties.Type.select == null) | .id' )

if [ -z "$PAGES" ]; then
    echo "No pages found with missing Type property."
    exit 0
fi

echo "Step 2: Patching properties via curl..."
for PAGE_ID in $PAGES; do
    echo "Updating $PAGE_ID..."
    curl -s "https://api.notion.com/v1/pages/$PAGE_ID" \
      -X PATCH \
      -H "Authorization: Bearer $NOTION_API_TOKEN" \
      -H "Notion-Version: 2022-06-28" \
      -H "Content-Type: application/json" \
      --data '{
        "properties": {
          "Type": {
            "select": { "name": "Entry" }
          }
        }
      }' > /dev/null
    
    # Gentle rate limiting
    sleep 0.3
done

echo "Property patch complete."
