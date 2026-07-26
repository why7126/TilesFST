## MODIFIED Requirements

### Requirement: 本地 Docker Compose 演示部署不得回归

现有 `docker-compose.yml` 和 `./scripts/docker-up.sh` MUST 继续支持本地开发与演示部署，默认使用 SQLite + MinIO。生产 Compose 的新增 MUST NOT 迫使本地开发者安装 MySQL。

#### Scenario: 本地 docker-up 仍使用 SQLite

- **WHEN** 开发者按现有本地文档执行 `./scripts/docker-up.sh`
- **THEN** backend MUST 使用 SQLite 数据卷
- **AND** MinIO MUST 继续按单桶初始化
- **AND** 开发者 MUST NOT 需要本地 MySQL

#### Scenario: 生产入口 smoke 不返回 Nginx 502

- **WHEN** 团队修复生产运行时、外层 Nginx upstream、Docker Web Nginx 或 Backend 启动配置
- **THEN** `https://tilesfst.wjoyhappy.site/` MUST NOT 返回 Nginx 502
- **AND** `https://tilesfst.wjoyhappy.site/api/v1/health` MUST 返回 200 与健康响应
- **AND** 生产 smoke 记录 MUST 包含根路径、健康检查、实际小程序 SKU 接口和实际 `/media/{object_key}` 视频 URL 的响应状态
- **AND** 若生产验证不可执行，Change 验收 MUST 记录具体 N/A 原因和替代生产等价验证。

### Requirement: Web 层 Swagger 代理

The Web deployment layer SHALL proxy Swagger and OpenAPI documentation routes to the backend so Web-origin documentation links work in local development and Docker deployments. Future changes touching Swagger documentation routes, Web proxy configuration, or production deployment documentation MUST explicitly record the dev, Docker, and production-equivalent proxy strategy for `/docs`, `/redoc`, `/openapi.json`, and Swagger UI resource paths.

#### Scenario: Existing backend proxy routes remain intact

- **WHEN** the Swagger proxy configuration is added or production proxy configuration is repaired
- **THEN** `/api/`, `/media/`, and `/openapi.json` SHALL continue to proxy to backend as before
- **AND** existing upload size and media proxy behavior SHALL NOT regress
- **AND** production-equivalent smoke SHALL confirm `/api/v1/health` and `/media/{object_key}` are not handled by the Web SPA fallback.
