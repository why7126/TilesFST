---
purpose: 生产部署矩阵
content: prod-mysql-tencent-cos 前置条件、启动方式和安全边界
source: REQ-0093 standardize-deployment-environment-matrix
created_at: 2026-08-03 19:10:00
updated_at: 2026-08-25 11:18:08
---

# 生产部署矩阵

当前生产目标环境为 `prod-mysql-tencent-cos`：

- 数据库：外部 MySQL 8.0+。
- 对象存储：腾讯云 COS。
- Compose：`deploy/prod/compose.tencent-cos.yml`。
- env 示例：`deploy/prod/mysql-tencent-cos.env.example`。
- 文档站：默认启用 `docs-site` profile 并启动 `tilesfst-docs-site`，端口由 `HOST_PORT_MINTLIFY_DOCS` 控制。
- 维护任务：按需启用 `maintenance` profile 或显式 `run --rm tilesfst-maintenance`，用于受控媒体历史维护 dry-run / apply。
- 重启策略：业务服务与文档站使用 `restart: unless-stopped`；维护任务为一次性受控执行，不配置常驻自启。

说明：根目录 `docker-compose.yml` 只作为本地/demo 编排事实源；生产不继承它的 SQLite 挂载或本地 MinIO profile。当前推荐生产入口是 `deploy/prod/compose.tencent-cos.yml`，根目录 `docker-compose.prod.yml` 与 `docker-compose.prod.external.yml` 仅作为 VPS/离线交付兼容入口维护。

前置条件：

- 运维已创建 MySQL 数据库、账号和最小权限。
- 运维已创建 COS bucket、region、endpoint、访问密钥和权限策略。
- `OBJECT_STORAGE_AUTO_CREATE_BUCKET=false`，生产不由应用自动建桶。
- `APP_SECRET_KEY`、`ADMIN_INITIAL_PASSWORD`、`DATABASE_URL`、COS 密钥必须替换为真实安全值，且不得提交 Git。

配置与启动：

```bash
cp deploy/prod/mysql-tencent-cos.env.example deploy/prod/mysql-tencent-cos.env
# 编辑 deploy/prod/mysql-tencent-cos.env，替换所有生产占位值
./deploy/scripts/up.sh prod mysql-tencent-cos
```

停止：

```bash
./deploy/scripts/down.sh prod
```

生产 Compose 不启动本地 MinIO 或 `minio-init`，也不挂载 SQLite 数据目录；默认启动 `tilesfst-docs-site`，用于生产 `/docs` 承载、反代或发布验收预览。docs-site 使用 `deploy/docs-site/Dockerfile` 构建预装 Mintlify CLI 的本地可复用镜像；Mintlify 预览缓存不作为业务数据持久化，仅留在容器临时文件系统内，不挂载宿主机 `~/.mintlify*`。

## 生产媒体维护任务

`tilesfst-maintenance` 复用后端生产镜像和生产 env 注入，默认命令只执行只读对象 key 审计示例，不随业务服务默认启动。生产维护任务必须在生产服务器或受控堡垒环境执行，不得下载生产 `.env` 到开发机长期保存。

只读 dry-run 示例：

```bash
./deploy/scripts/media-maintenance.sh prod mysql-tencent-cos object-key-audit --limit 100
```

媒体漂移聚合 dry-run 示例：

```bash
./deploy/scripts/media-maintenance.sh prod mysql-tencent-cos media-drift-reconcile --limit 100
```

写操作必须先完成 MySQL 快照和对象存储 bucket/prefix 快照，并显式传入 `--apply --confirm-backup`。`media-drift-reconcile` 是生产推荐聚合入口；`bug-0116-media-drift` 仅作为历史兼容别名保留。部署脚本会阻断缺少 `--confirm-backup` 的 apply；维护 CLI 输出只包含统计、脱敏对象标识、错误码和失败原因摘要，不得输出真实密钥、数据库连接串、Authorization header、Cookie、生产 `.env` 原文、本机绝对路径或真实客户敏感数据。

变更生产 Compose 文档或 env 示例后，至少校验：

```bash
TILESFST_DEPLOY_ENV_FILE=mysql-tencent-cos.env.example docker compose --project-name tilesfst --env-file deploy/prod/mysql-tencent-cos.env.example --profile docs-site -f deploy/prod/compose.tencent-cos.yml config --quiet
```
