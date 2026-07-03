#!/bin/bash
# 2. Exchange Code for Tokens
if [ -z "$1" ]; then
    echo "Usage: ./exchange_code.sh <authorization_code>"
    exit 1
fi

ID=$(bws-direct "67546151-c920-4bfa-ab25-b44b014df788")
SECRET=$(bws-direct "32d4b5cb-c7b8-4113-b56c-b44b014e178e")
REDIRECT_URI="http://localhost:8080/callback"
CODE=$1

response=$(curl -s -X POST https://www.inoreader.com/oauth2/token \
    -d "client_id=$ID&client_secret=$SECRET&grant_type=authorization_code&code=$CODE&redirect_uri=$REDIRECT_URI")

# Parse JSON
ACCESS_TOKEN=$(echo $response | jq -r '.access_token')
REFRESH_TOKEN=$(echo $response | jq -r '.refresh_token')
EXPIRES_IN=$(echo $response | jq -r '.expires_in')

# Save to BWS
bws-direct-put "cd034d95-a2d2-4ccf-a1a7-b44b014e38bc" --value "$ACCESS_TOKEN"
bws-direct-put "ab61ca81-b4c7-48db-a608-b451013512ae" --value "$REFRESH_TOKEN"
bws-direct-put "3c678008-018f-4e2a-a0c8-b451013785fd" --value $(( $(date +%s) + EXPIRES_IN ))

echo "Tokens exchanged and saved to BWS successfully."
