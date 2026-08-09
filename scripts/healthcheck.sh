#!/usr/bin/env bash
# ==============================================================================
# AuraMed AI - Automated Deployment Health Verification Script
# ==============================================================================

set -eo pipefail

HOST="${HEALTHCHECK_HOST:-http://localhost}"
PORT="${HEALTHCHECK_PORT:-8000}"
ENDPOINT="${HEALTHCHECK_ENDPOINT:-/health}"
MAX_RETRIES="${MAX_RETRIES:-10}"
RETRY_INTERVAL="${RETRY_INTERVAL:-3}"

if [[ "$1" == "--dry-run" ]]; then
    echo "[HEALTHCHECK] Executing dry-run deployment health verification..."
    echo "[HEALTHCHECK] Target Endpoint: ${HOST}:${PORT}${ENDPOINT}"
    echo "[HEALTHCHECK] ✅ Dry-run health verification PASSED (Simulation Successful)."
    exit 0
fi

echo "[HEALTHCHECK] Starting deployment health polling..."
echo "[HEALTHCHECK] Checking ${HOST}:${PORT}${ENDPOINT} (Max retries: ${MAX_RETRIES})"

count=0
until [ $count -ge $MAX_RETRIES ]
do
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "${HOST}:${PORT}${ENDPOINT}" || echo "000")
    if [ "$HTTP_CODE" -eq 200 ]; then
        echo "[HEALTHCHECK] ✅ Deployment HEALTHY! Received HTTP 200 OK from ${HOST}:${PORT}${ENDPOINT}"
        exit 0
    fi
    count=$((count+1))
    echo "[HEALTHCHECK] Retry $count/$MAX_RETRIES: Server responded with HTTP $HTTP_CODE. Waiting $RETRY_INTERVAL seconds..."
    sleep $RETRY_INTERVAL
done

echo "[HEALTHCHECK] ❌ Deployment FAILED! Server did not respond with HTTP 200 after $MAX_RETRIES retries."
exit 1
