#!/usr/bin/env bash
set -euo pipefail

HEALTH_MAX_AGE_HOURS="${HEALTH_MAX_AGE_HOURS:-30}"
BACKUP_DIR="${BACKUP_DIR:-/backup}"
marker="${BACKUP_DIR}/.last_success_epoch"

if [ ! -f "${marker}" ]; then
  echo "No last success marker: ${marker}"
  exit 1
fi

last_epoch="$(cat "${marker}" 2>/dev/null || echo 0)"
now_epoch="$(date +%s)"
max_age_sec="$((HEALTH_MAX_AGE_HOURS * 3600))"
age="$((now_epoch - last_epoch))"

if [ "${age}" -le "${max_age_sec}" ]; then
  echo "OK: last success ${age}s ago"
  exit 0
fi

echo "STALE: last success ${age}s ago (max ${max_age_sec}s)"
exit 1
