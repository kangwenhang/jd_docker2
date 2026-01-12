#!/usr/bin/env bash
set -euo pipefail

: "${MSSQL_HOST:?}"
: "${MSSQL_USER:?}"
: "${MSSQL_PASSWORD:?}"
: "${BACKUP_DIR:=/backup}"
: "${RETENTION_DAYS:=30}"
: "${USE_COMPRESSION:=auto}"      # 0/1/auto
: "${NOTIFY_ENABLED:=0}"

mkdir -p "${BACKUP_DIR}"

sqlcmd_bin="/opt/mssql-tools/bin/sqlcmd"

# 库列表：优先 MSSQL_DBS（逗号分隔），否则 MSSQL_DB
dbs=""
if [ -n "${MSSQL_DBS:-}" ]; then
  dbs="${MSSQL_DBS}"
elif [ -n "${MSSQL_DB:-}" ]; then
  dbs="${MSSQL_DB}"
else
  echo "[ERROR] Please set MSSQL_DB or MSSQL_DBS in config."
  exit 1
fi
dbs="${dbs//,/ }"

ts="$(date +%F_%H%M%S)"

run_backup_one() {
  local db="$1"
  local file="${BACKUP_DIR}/${db}_${ts}.bak"

  echo "[INFO] Backup start: DB=${db} -> ${file}"

  local opts="WITH INIT"
  local try_compress=0
  case "${USE_COMPRESSION}" in
    1) try_compress=1 ;;
    0) try_compress=0 ;;
    auto) try_compress=1 ;;
    *) echo "[ERROR] USE_COMPRESSION must be 0/1/auto"; return 2 ;;
  esac

  if [ "${try_compress}" = "1" ]; then
    # 尝试压缩
    set +e
    "${sqlcmd_bin}" -S "${MSSQL_HOST}" -U "${MSSQL_USER}" -P "${MSSQL_PASSWORD}" -b \
      -Q "BACKUP DATABASE [${db}] TO DISK = N'${file}' ${opts}, COMPRESSION;" \
      2>"/tmp/backup_${db}.err"
    rc=$?
    set -e

    if [ $rc -eq 0 ]; then
      echo "[INFO] Backup done (COMPRESSION)."
      return 0
    fi

    # auto：压缩失败回退
    if [ "${USE_COMPRESSION}" = "auto" ]; then
      echo "[WARN] Backup with COMPRESSION failed for DB=${db}. Fallback to no compression."
      echo "[WARN] Error:"
      sed -n '1,160p' "/tmp/backup_${db}.err" || true

      "${sqlcmd_bin}" -S "${MSSQL_HOST}" -U "${MSSQL_USER}" -P "${MSSQL_PASSWORD}" -b \
        -Q "BACKUP DATABASE [${db}] TO DISK = N'${file}' ${opts};"
      echo "[INFO] Backup done (no compression)."
      return 0
    fi

    # 强制压缩模式：直接失败
    echo "[ERROR] Backup failed (COMPRESSION required)."
    sed -n '1,160p' "/tmp/backup_${db}.err" || true
    return 1
  fi

  # 不压缩
  "${sqlcmd_bin}" -S "${MSSQL_HOST}" -U "${MSSQL_USER}" -P "${MSSQL_PASSWORD}" -b \
    -Q "BACKUP DATABASE [${db}] TO DISK = N'${file}' ${opts};"
  echo "[INFO] Backup done (no compression)."
}

fail_count=0
success_count=0

for db in ${dbs}; do
  if run_backup_one "${db}"; then
    success_count=$((success_count+1))
  else
    fail_count=$((fail_count+1))
  fi
done

# 清理旧备份（按 db 前缀匹配）
for db in ${dbs}; do
  find "${BACKUP_DIR}" -type f -name "${db}_*.bak" -mtime +"${RETENTION_DAYS}" -print -delete || true
done
echo "[INFO] Cleanup done (keep ${RETENTION_DAYS} days)."

# 写入最近一次成功备份时间（健康检查用）
if [ "${success_count}" -gt 0 ]; then
  date +%s > "${BACKUP_DIR}/.last_success_epoch" || true
fi

# 通知（可选）
if [ "${NOTIFY_ENABLED}" = "1" ]; then
  if [ "${fail_count}" -eq 0 ]; then
    /app/notify.sh "✅ MSSQL backup success: ${success_count} DB(s) @ ${ts} (host=${MSSQL_HOST})"
  else
    /app/notify.sh "❌ MSSQL backup partial/failed: success=${success_count}, failed=${fail_count} @ ${ts} (host=${MSSQL_HOST})"
    exit 1
  fi
fi

# 没开通知但有失败，也返回非0
if [ "${fail_count}" -ne 0 ]; then
  exit 1
fi
