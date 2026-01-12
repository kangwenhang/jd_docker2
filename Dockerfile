FROM mcr.microsoft.com/mssql-tools:latest

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      cron tzdata ca-certificates bash \
      curl jq \
      msmtp msmtp-mta bsd-mailx \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 运行脚本
COPY entrypoint.sh /app/entrypoint.sh
COPY backup.sh /app/backup.sh
COPY notify.sh /app/notify.sh
COPY healthcheck.sh /app/healthcheck.sh

# 模板统一放到 templates 目录
COPY templates /app/templates

RUN chmod +x \
    /app/entrypoint.sh \
    /app/backup.sh \
    /app/notify.sh \
    /app/healthcheck.sh

HEALTHCHECK --interval=5m --timeout=10s --retries=3 CMD ["/app/healthcheck.sh"]

CMD ["/app/entrypoint.sh"]
