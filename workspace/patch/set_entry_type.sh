#!/bin/bash
DB_ID="383b2203-a808-4eea-9012-8207b5578fa2"
NTN="/home/node/.npm-global/bin/ntn"

echo "Querying Notion database for entries..."

# Using the pattern that allows direct JSON patching via STDIN which usually works for ntn pages
PAGES=$($NTN api "v1/databases/$DB_ID/query" --method POST --notion-version 2022-06-28 | jq -r '.results[] | .id')

for PAGE_ID in $PAGES; do
  echo "Patching Page: $PAGE_ID"
  # Try the "pages update" command which supports STDIN properly
  echo '{"properties":{"Type":{"select":{"name":"Entry"}}}}' | $NTN pages update "$PAGE_ID" --notion-version 2022-06-28
done

echo "Patch complete."
