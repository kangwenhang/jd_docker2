#!/usr/bin/env bash
set -euo pipefail

CONFIG_DIR="/config"
CONFIG_FILE="${CONFIG_FILE:-/config/config.env}"
CRON_FILE="${CRON_FILE:-/config/schedule.cron}"

TEMPLATE_DIR="/app/templates"
TEMPLATE_CONFIG="${TEMPLATE_DIR}/config.env.example"
TEMPLATE_CRON="${TEMPLATE_DIR}/schedule.cron.example"

mkdir -p "$CONFIG_DIR"

# 如果配置不存在 → 从 templates 复制模板并退出
if [ ! -f "$CONFIG_FILE" ]; then
  echo "=============================================="
  echo "[INFO] Config file not found."
  echo "[INFO] Creating config templates from ${TEMPLATE_DIR}"
  cp "$TEMPLATE_CONFIG" "$CONFIG_FILE"
  cp "$TEMPLATE_CRON" "$CRON_FILE"
  echo
  echo "[ACTION REQUIRED]"
  echo "Please edit the following files and restart container:"
  echo "  - $CONFIG_FILE"
  echo "  - $CRON_FILE"
  echo "=============================================="
  exit 1
fi

# shellcheck disable=SC1090
source "$CONFIG_FILE"

: "${MSSQL_HOST:?}"
: "${MSSQL_USER:?}"
: "${MSSQL_PASSWORD:?}"
: "${BACKUP_DIR:=/backup}"
: "${RETENTION_DAYS:=30}"
: "${TZ:=Asia/Shanghai}"

# cron 文件不存在也从模板生成
if [ ! -f "$CRON_FILE" ]; then
  echo "[INFO] Cron file not found, creating from template."
  cp "$TEMPLATE_CRON" "$CRON_FILE"
  echo "[ACTION REQUIRED] Please edit $CRON_FILE and restart container."
  exit 1
fi

echo "[INFO] Using config: $CONFIG_FILE"
echo "[INFO] Using cron:   $CRON_FILE"

# 写入 cron（执行前先加载配置）
cat > /etc/cron.d/mssql-backup <<EOF
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
TZ=${TZ}

$(sed -E "s#(/app/backup\.sh)#source ${CONFIG_FILE} \&\& \\1#g" "$CRON_FILE")
EOF

chmod 0644 /etc/cron.d/mssql-backup
crontab /etc/cron.d/mssql-backup

# 启动时跑一次（可选）
echo "[INFO] Running one backup immediately..."
/app/backup.sh || true

echo "[INFO] Starting cron..."
exec cron -f
