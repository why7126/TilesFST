## 1. 配置实现

- [x] 1.1 移除 `Settings.sqlite_database_url`，将 `DATABASE_URL` 默认值设为本地 SQLite DSN。
- [x] 1.2 更新数据库 URL 解析逻辑，非生产也直接使用 `DATABASE_URL`。
- [x] 1.3 更新 `.env.example`，移除 `SQLITE_DATABASE_URL` 并补充单一入口说明。

## 2. 文档与规格

- [x] 2.1 更新 `docs/02-deployment.md` 的数据库环境变量说明。
- [x] 2.2 更新 `docs/04-database-design.md` 的数据库选择矩阵与路径说明。
- [x] 2.3 运行 OpenSpec 严格校验。

## 3. 测试与收尾

- [x] 3.1 更新数据库配置测试和 test fixtures。
- [x] 3.2 运行聚焦 pytest。
- [x] 3.3 运行 Workflow Sync 和 AI usage hook。
