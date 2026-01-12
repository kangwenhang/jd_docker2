#!/usr/bin/env bash
set -euo pipefail

msg="${1:-}"
[ -z "$msg" ] && exit 0

# shellcheck disable=SC1090
[ -f /config/config.env ] && source /config/config.env

send_wecom() {
  if [ -n "${NOTIFY_WECOM_WEBHOOK:-}" ]; then
    curl -fsS -X POST "${NOTIFY_WECOM_WEBHOOK}" \
      -H 'Content-Type: application/json' \
      -d "{\"msgtype\":\"text\",\"text\":{\"content\":\"${msg}\"}}" >/dev/null || true
  fi
}

send_telegram() {
  if [ -n "${NOTIFY_TELEGRAM_BOT_TOKEN:-}" ] && [ -n "${NOTIFY_TELEGRAM_CHAT_ID:-}" ]; then
    curl -fsS -X POST "https://api.telegram.org/bot${NOTIFY_TELEGRAM_BOT_TOKEN}/sendMessage" \
      -d "chat_id=${NOTIFY_TELEGRAM_CHAT_ID}" \
      --data-urlencode "text=${msg}" >/dev/null || true
  fi
}

send_email() {
  if [ -n "${NOTIFY_EMAIL_TO:-}" ] && [ -n "${SMTP_HOST:-}" ]; then
    : "${NOTIFY_EMAIL_FROM:=mssql-backup@localhost}"
    : "${SMTP_PORT:=587}"
    : "${SMTP_TLS:=on}"

    cat > /etc/msmtprc <<EOF
defaults
auth           on
tls            ${SMTP_TLS}
tls_trust_file /etc/ssl/certs/ca-certificates.crt
logfile        /var/log/msmtp.log

account        default
host           ${SMTP_HOST}
port           ${SMTP_PORT}
user           ${SMTP_USER:-}
password       ${SMTP_PASSWORD:-}
from           ${NOTIFY_EMAIL_FROM}
EOF
    chmod 600 /etc/msmtprc

    printf "Subject: MSSQL Backup Notification\nFrom: %s\nTo: %s\n\n%s\n" \
      "${NOTIFY_EMAIL_FROM}" "${NOTIFY_EMAIL_TO}" "${msg}" \
      | /usr/sbin/sendmail -t >/dev/null || true
  fi
}

send_wecom
send_telegram
send_email
