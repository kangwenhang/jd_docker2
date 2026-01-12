#!/usr/bin/env bash
set -euo pipefail

###############################################################################
# 1. 自动加载配置文件（支持手动 / cron / docker exec 任意方式执行）
###############################################################################
CONFIG_FILE="/config/config.env"

if [ -f "$CONFIG_FILE" ]; then
  # 修复 Windows CRLF (\r) 问题
  sed -i 's/\r$//' "$CONFIG_FILE" || true
  # 自动导出变量
  set -a
  # shellcheck disable=SC1090
  source "$CONFIG_FILE"
  set +a
else
  echo "[ERROR] Config file not found: $CONFIG_FILE"
  exit 1
fi

###############################################################################
# 2. 变量校验（此时一定已经加载完成）
###############################################################################
: "${MSSQL_HOST:?}"
: "${MSSQL_USER:?}"
: "${MSSQL_PASSWORD:?}"

BACKUP_DIR="${BACKUP_DIR:-/backup}"
RETENTION_DAYS="${RETENTION_DAYS:-30}"
USE_COMPRESSION="${USE_COMPRESSION:-auto}"
NOTIFY_ENABLED="${NOTIFY_ENABLED:-0}"

mkdir -p "${BACKUP_DIR}"

sqlcmd_bin="/opt/mssql-tools/bin/sqlcmd"

###############################################################################
# 3. 解析数据库列表（单库 / 多库）
###############################################################################
dbs=""
if [ -n "${MSSQL_DBS:-}" ]; then
  dbs="${MSSQL_DBS}"
elif [ -n "${MSSQL_DB:-}" ]; then
  dbs="${MSSQL_DB}"
else
  echo "[ERROR] Please set MSSQL_DB or MSSQL_DBS in config."
  exit 1
fi

# 统一格式：逗号 → 空格
dbs="${dbs//,/ }"

ts="$(date +%F_%H%M%S)"

###############################################################################
# 4. 备份函数（支持 COMPRESSION auto 回退）
###############################################################################
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
    *)
      echo "[ERROR] USE_COMPRESSION must be 0/1/auto"
      return 2
      ;;
  esac

  if [ "$try_compress" -eq 1 ]; then
    set +e
    "${sqlcmd_bin}" \
      -S "${MSSQL_HOST}" \
      -U "${MSSQL_USER}" \
      -P "${MSSQL_PASSWORD}" \
      -b \
      -Q "BACKUP DATABASE [${db}] TO DISK = N'${file}' ${opts}, COMPRESSION;" \
      2>"/tmp/backup_${db}.err"
    rc=$?
    set -e

    if [ "$rc" -eq 0 ]; then
      echo "[INFO] Backup done (COMPRESSION)."
      return 0
    fi

    if [ "${USE_COMPRESSION}" = "auto" ]; then
      echo "[WARN] COMPRESSION failed for DB=${db}, fallback to no compression."
      sed -n '1,160p' "/tmp/backup_${db}.err" || true

      "${sqlcmd_bin}" \
        -S "${MSSQL_HOST}" \
        -U "${MSSQL_USER}" \
        -P "${MSSQL_PASSWORD}" \
        -b \
        -Q "BACKUP DATABASE [${db}] TO DISK = N'${file}' ${opts};"

      echo "[INFO] Backup done (no compression)."
      return 0
    fi

    echo "[ERROR] Backup failed (COMPRESSION required)."
    sed -n '1,160p' "/tmp/backup_${db}.err" || true
    return 1
  fi

  "${sqlcmd_bin}" \
    -S "${MSSQL_HOST}" \
    -U "${MSSQL_USER}" \
    -P "${MSSQL_PASSWORD}" \
    -b \
    -Q "BACKUP DATABASE [${db}] TO DISK = N'${file}' ${opts};"

  echo "[INFO] Backup done (no compression)."
}

###############################################################################
# 5. 执行备份
###############################################################################
fail_count=0
success_count=0

for db in ${dbs}; do
  if run_backup_one "${db}"; then
    success_count=$((success_count + 1))
  else
    fail_count=$((fail_count + 1))
  fi
done

###############################################################################
# 6. 清理旧备份
###############################################################################
for db in ${dbs}; do
  find "${BACKUP_DIR}" -type f -name "${db}_*.bak" -mtime +"${RETENTION_DAYS}" -print -delete || true
done

echo "[INFO] Cleanup done (keep ${RETENTION_DAYS} days)."

###############################################################################
# 7. 写入健康检查标记
###############################################################################
if [ "${success_count}" -gt 0 ]; then
  date +%s > "${BACKUP_DIR}/.last_success_epoch" || true
fi

###############################################################################
# 8. 通知（可选）
###############################################################################
if [ "${NOTIFY_ENABLED}" = "1" ]; then
  if [ "${fail_count}" -eq 0 ]; then
    /app/notify.sh "✅ MSSQL backup success: ${success_count} DB(s) @ ${ts} (host=${MSSQL_HOST})"
  else
    /app/notify.sh "❌ MSSQL backup partial/failed: success=${success_count}, failed=${fail_count} @ ${ts} (host=${MSSQL_HOST})"
    exit 1
  fi
fi

###############################################################################
# 9. 返回码
###############################################################################
if [ "${fail_count}" -ne 0 ]; then
  exit 1
fi

exit 0
