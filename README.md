# mssql-backup-docker

## 📦 项目简介 / Introduction

**mssql-backup-docker** 是一个基于 Docker 的轻量级备份工具，  
用于将 **远程 Microsoft SQL Server（如 Windows Server 2012 R2）**  
按计划自动备份到 **NAS（如飞牛 fnOS / 群晖 / 威联通）或任意目录**。

**mssql-backup-docker** is a lightweight Docker-based backup tool for  
scheduled backups of **remote Microsoft SQL Server** databases  
to a **NAS (fnOS / Synology / QNAP) or any directory**.

---

## ✨ 功能特性 / Features

- ⏱ 基于 cron 的定时备份  
  Cron-based scheduled backups
- 🧾 使用 `sqlcmd` 进行原生 SQL Server 备份  
  Native SQL Server backups via `sqlcmd`
- 📁 支持单库 / 多库备份  
  Single or multiple database backup support
- 🧩 首次启动自动生成配置模板  
  Auto-generate config templates on first run
- 🗑 备份保留策略（保留 N 天）  
  Retention cleanup (keep N days)
- 🗜 备份压缩策略：`0 / 1 / auto`  
  Compression strategy: `0 / 1 / auto`
- ❤️ 健康检查（基于最近一次成功备份时间）  
  Healthcheck based on last successful backup time
- 🔔 可选通知：企业微信 / Telegram / Email  
  Optional notifications: WeCom / Telegram / Email
- 🐳 多架构镜像（amd64 / arm64）  
  Multi-arch Docker image (amd64 / arm64)

---

## 🚀 快速开始（推荐：Docker Compose）  
## 🚀 Quick Start (Recommended: Docker Compose)

### 1️⃣ 创建工作目录  
### 1️⃣ Create working directory

```bash
mkdir mssql-backup && cd mssql-backup
