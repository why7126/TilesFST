---
purpose: 部署文档
content: 部署组件、环境变量和运行方式
source: AI自动生成初稿，项目团队确认
update_method: 项目初始化后由人工确认；后续由AI辅助更新并经人工Review
note: 适用于瓷砖信息管理平台项目模板
---

# 部署说明


## 部署组件

- FastAPI 应用服务
- SQLite 数据库文件
- MinIO 对象存储
- Web 静态资源

## 环境变量

参考 `.env.example`。

## Docker Compose 部署方案

本项目默认支持 Docker Compose 本地开发与演示部署。

### 服务组成

| 服务 | 容器名 | 端口 | 说明 |
|---|---|---|---|
| backend | tile-info-platform-backend | 8000 | FastAPI 后端服务 |
| web | tile-info-platform-web | 3000 | React Web 展示端与管理端 |
| minio | tile-info-platform-minio | 9000 / 9001 | 对象存储与控制台 |

### 启动命令

```bash
./scripts/docker-up.sh
```

### 停止命令

```bash
./scripts/docker-down.sh
```

### 数据持久化

- SQLite 数据文件挂载到 `./data/sqlite/`。
- MinIO 数据映射到 `./data/minio/`，为本地 Docker 下对象存储持久化卷；桶内对象增长属预期行为。
- 业务媒体上传正式写入 MinIO `MINIO_BUCKET`，**不**写入 `data/uploads/`。
- `data/processed/`、`data/tmp/` 仍挂载供处理后产物与临时文件使用。

### Legacy uploads 清理

若曾在对象存储迁移（BUG-0006）前使用本地上传，宿主机 `data/uploads/` 可能残留无数据库引用的孤儿文件。清理方式：

```bash
python scripts/clean_legacy_uploads.py
python scripts/clean_legacy_uploads.py --apply
```

说明见 `data/README.md` 与 `docs/07-object-storage-strategy.md` §3。

### 默认管理员与密码恢复

Docker Compose 通过根目录 `.env` 向后端注入默认管理员相关变量：

```env
ADMIN_USERNAME=admin
ADMIN_INITIAL_PASSWORD=change-me-on-first-run
ADMIN_RESET_PASSWORD_ON_STARTUP=false
```

- 空数据库首次启动时，如果 `ADMIN_INITIAL_PASSWORD` 已配置，系统会创建 `ADMIN_USERNAME` 对应的 `admin` 角色账号，密码以 bcrypt 哈希写入 `users.password_hash`。
- `./data/sqlite/` 是持久化目录。数据库中已存在默认管理员时，普通服务重启不会自动覆盖该账号密码，也不会因为修改 `.env` 中的 `ADMIN_INITIAL_PASSWORD` 而静默重置密码。
- 若本地开发、演示或受控运维场景需要恢复默认管理员密码，可临时设置 `ADMIN_RESET_PASSWORD_ON_STARTUP=true` 并重启后端。恢复完成后应立即改回 `false`，避免后续重启再次覆盖管理员密码。
- 恢复流程不会在日志、接口响应或文档中输出明文密码；生产环境应使用安全的运维流程和密钥管理系统注入真实密码。

### 配置文件

| 文件 | 作用 |
|---|---|
| `docker-compose.yml` | 服务编排 |
| `src/backend/Dockerfile` | 后端镜像构建 |
| `src/backend/.env.docker` | 后端Docker环境变量 |
| `src/web/Dockerfile` | Web镜像构建 |
| `src/web/nginx.conf` | Web静态资源与API代理配置 |

### 注意事项

- 本地默认 MinIO 账号密码仅用于开发环境。
- 生产环境必须更换密钥，并使用安全的配置管理方式。
- SQLite 适合轻量级部署；如后续切换数据库，必须创建 OpenSpec Change。


## V4 环境变量与数据目录

初始化本地环境：

```bash
cp .env.example .env
./scripts/docker-up.sh
```

Docker Compose 会使用：

```text
.env.example
src/backend/.env.docker
data/sqlite/
data/minio/          # MinIO 持久化卷（正式业务媒体落盘）
data/uploads/        # 历史兼容目录；迁移后不应新增业务文件
data/processed/
data/tmp/
```

生产环境不得直接使用示例密钥，必须通过部署平台注入真实环境变量。

## Docker Compose 端口策略

默认开发端口：

```text
Backend: 8000
Web: 3000
MinIO API: 9000
MinIO Console: 9001
```

采用：

```text
容器内部端口固定
宿主机端口通过 .env 配置
```

示例：

```env
HOST_PORT_BACKEND=18080
HOST_PORT_WEB=13000
```

## MinIO 单桶策略

使用一个项目一个 Bucket：

```env
MINIO_BUCKET=tile-info-platform
```

并在桶内通过前缀区分：

```text
original/
thumbnails/
processed/
videos/
videos/covers/
videos/transcoded/
```
