#!/bin/bash
# Test script to verify the API works after deployment

API_URL=${1:-"http://localhost:8000"}

echo "Testing Hardscapes API at: $API_URL"
echo "========================================"

# Test 1: Health check
echo -e "\n1. Health Check (GET /):"
curl -s "$API_URL/" | python -m json.tool || echo "Failed"

# Test 2: Get words for level 1
echo -e "\n\n2. Get words for level 1 (GET /words?level=1&limit=5):"
curl -s "$API_URL/words?level=1&limit=5" | python -m json.tool || echo "Failed"

# Test 3: Get stats
echo -e "\n\n3. Get database stats (GET /stats):"
curl -s "$API_URL/stats" | python -m json.tool || echo "Failed"

# Test 4: Custom parameters
echo -e "\n\n4. Get words with custom parameters (level=5, min_len=4, max_len=6):"
curl -s "$API_URL/words?level=5&min_len=4&max_len=6&limit=3" | python -m json.tool || echo "Failed"

echo -e "\n\n========================================"
echo "Testing complete!"
