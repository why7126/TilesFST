---
req_id: REQ-0018-production-mysql-deployment
status: captured
created_at: 2026-06-28 20:15:00
updated_at: 2026-06-28 20:15:00
recorded_by: product
source: 反馈
priority_hint: P0
parent_requirement:
---

# 一句话

为生产环境部署提供 MySQL 数据库支持，使后端可在生产环境稳定运行（当前本地/Docker 开发环境使用 SQLite）。

# 原始描述

需要部署生产环境了，但生产环境需要使用 MySQL 数据库。

# 背景与关联

- 项目现状：后端 FastAPI + SQLite（本地开发与 Docker Compose 演示）；MinIO 对象存储；见 `docker-compose.yml`、`rules/database.md`、`docs/02-deployment.md`。
- 预期影响面：数据库连接层、迁移脚本、环境变量、生产部署文档、可能新增 `docker-compose.prod.yml` 或等价编排。
- 本地/演示环境是否继续保留 SQLite 作为默认，待 `/req-explore` 澄清。

# 待澄清

- [ ] 生产部署目标形态（单机 Docker Compose / 云托管 / K8s / 其他）
- [ ] MySQL 版本与字符集/collation 要求
- [ ] 本地开发与 Docker 演示是否仍默认 SQLite，生产通过 env 切换 MySQL
- [ ] 是否需要 SQLite → MySQL 数据迁移工具或仅 schema 初始化 + 种子数据
- [ ] 生产环境 MinIO 与现有单桶策略如何部署（是否纳入本 REQ 或独立）
- [ ] 高可用、备份、连接池、只读副本等是否为 MVP 范围
- [ ] 生产密钥、`.env.example` 与 `rules/environment.md` 对齐项

# 探索结论

（/req-explore 后人工确认写入）
