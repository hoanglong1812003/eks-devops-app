#!/bin/bash

# Health check script for FCAJ Chatbot
# Usage: ./health-check.sh [url]

URL=${1:-"http://localhost:8501"}

echo "🏥 Checking health of FCAJ Chatbot at $URL..."

# Check if service is responding
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" $URL/_stcore/health)

if [ $HTTP_CODE -eq 200 ]; then
    echo "✅ Service is healthy (HTTP $HTTP_CODE)"
    exit 0
else
    echo "❌ Service is unhealthy (HTTP $HTTP_CODE)"
    exit 1
fi
