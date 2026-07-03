#!/bin/bash
# Inoreader API Handler with BWS-backed OAuth2

set -e

# Ensure custom tools and local binaries are in path
export PATH="/opt/custom-tools:/home/node/.local/bin:$PATH"
export BWS_ACCESS_TOKEN=$(</home/node/.config/bws/.token)

# Refresh tokens if close to expiration
ensure_authenticated() {

    local expires_at=$(bws-direct "3c678008-018f-4e2a-a0c8-b451013785fd" $BWS_ACCESS_TOKEN)
    local buffer=300 # 5 minutes

    if [ $(date +%s) -ge $((expires_at - buffer)) ]; then
        echo "Refreshing token"
        token_refresh
    fi
}

token_refresh() {
    echo "d"
    local id=$(bws-direct "67546151-c920-4bfa-ab25-b44b014df788" $BWS_ACCESS_TOKEN)
    local secret=$(bws-direct "32d4b5cb-c7b8-4113-b56c-b44b014e178e" $BWS_ACCESS_TOKEN)
    local refresh_token=$(bws-direct "ab61ca81-b4c7-48db-a608-b451013512ae" $BWS_ACCESS_TOKEN)

    local response=$(curl -s -X POST https://www.inoreader.com/oauth2/token \
        -d "client_id=$id&client_secret=$secret&grant_type=refresh_token&refresh_token=$refresh_token")

   # Store new tokens back to BWS

    bws-direct-put "cd034d95-a2d2-4ccf-a1a7-b44b014e38bc" "$(echo $response | jq -r '.access_token')" $BWS_ACCESS_TOKEN
    bws-direct-put "ab61ca81-b4c7-48db-a608-b451013512ae" "$(echo $response | jq -r '.refresh_token')" $BWS_ACCESS_TOKEN
    local expires_in=$(echo $response | jq -r '.expires_in')
    bws-direct-put "3c678008-018f-4e2a-a0c8-b451013785fd" "$(( $(date +%s) + expires_in ))" $BWS_ACCESS_TOKEN
}

# API request helper
inoreader_api_request() {
    ensure_authenticated
    local token=$(bws-direct "cd034d95-a2d2-4ccf-a1a7-b44b014e38bc" $BWS_ACCESS_TOKEN)
    local app_id=$(bws-direct "67546151-c920-4bfa-ab25-b44b014df788" $BWS_ACCESS_TOKEN)
    local app_key=$(bws-direct "32d4b5cb-c7b8-4113-b56c-b44b014e178e" $BWS_ACCESS_TOKEN)
    curl -s \
         -H "Authorization: Bearer $token" \
         -H "AppId: $app_id" \
         -H "AppKey: $app_key" \
         "https://www.inoreader.com/reader/api/0/$1"
}

# Run request based on argument
if [ $# -eq 0 ]; then
    echo "Usage: $0 <endpoint>"
    exit 1
fi

inoreader_api_request "$1"
