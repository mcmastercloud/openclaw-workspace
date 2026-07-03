#!/bin/bash
# 1. Generate Auth URL
CLIENT_ID=$(bws-direct "67546151-c920-4bfa-ab25-b44b014df788")
REDIRECT_URI="http://localhost:8080/callback" # Example
STATE=$(openssl rand -hex 16)

echo "Visit this URL in your browser:"
echo "https://www.inoreader.com/oauth2/auth?client_id=$CLIENT_ID&response_type=code&redirect_uri=$REDIRECT_URI&scope=read&state=$STATE"
echo
echo "After authorizing, you will be redirected to a URL starting with $REDIRECT_URI"
echo "Copy the 'code' parameter from that URL and run: ./exchange_code.sh <code_from_url>"
