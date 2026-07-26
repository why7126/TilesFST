## 1. Snapshot 契约与采集

- [x] 1.1 定义 Request Snapshot Pydantic Schema、字段枚举、空值语义和脱敏状态表达。
- [x] 1.2 实现 Snapshot builder，采集 method、path、route_template、request_id、client_type、actor、environment、started_at、finished_at 和 duration。
- [x] 1.3 实现 route template 获取与 `unknown` / `unmatched` 等降级策略。
- [x] 1.4 实现 query 白名单、body schema 摘要、敏感字段黑名单、长度截断和脱敏规则。
- [x] 1.5 实现业务资源标识提取，覆盖 path、query、body 和业务上下文来源。

## 2. 存储与 API

- [x] 2.1 扩展 request logs 存储结构或 metadata schema，明确 SQLite demo 与 MySQL production 兼容方案。
- [x] 2.2 更新 SQLite schema、MySQL schema 和 migration，避免 SQLite-only DDL 泄漏到生产。（本实现采用 metadata JSON，无 DDL 变更；已通过 schema drift 测试。）
- [x] 2.3 扩展日志服务和仓储，保存 Snapshot 且日志采集失败不阻断主业务响应。
- [x] 2.4 扩展 `GET /api/v1/admin/logs/{id}` 响应，返回结构化 Request Snapshot。
- [x] 2.5 保持日志列表分页、筛选、request_id、task_trace_id 和权限边界不回退。

## 3. Web 管理端

- [x] 3.1 扩展 Orval 生成类型后，更新日志详情抽屉数据映射。
- [x] 3.2 在日志详情抽屉中分组展示请求信息、输入摘要、业务资源、响应结果、操作者 / 客户端、环境与时间。
- [x] 3.3 增加 JSON 辅助视图、敏感字段脱敏状态、缺失字段空态和 metadata 解析失败兜底。
- [x] 3.4 验证移动端日志详情抽屉仍可滚动、可关闭且不丢失列表上下文。

## 4. 文档与生成物

- [x] 4.1 更新 OpenAPI 并运行 Orval，确保 generated files 只由生成命令更新。
- [x] 4.2 更新 `docs/03-api-index.md`，说明日志详情 Snapshot response schema。
- [x] 4.3 更新 `docs/04-database-design.md`，说明 Snapshot 存储方式、索引或不索引字段理由。
- [x] 4.4 如新增或复用错误码，更新 `docs/standards/error-codes.md` 与后端错误码定义。（未新增错误码，沿用 `30070` not found / 既有 forbidden。）

## 5. 测试与验证

- [x] 5.1 后端测试覆盖 route template 获取与降级、query 白名单、body schema 摘要、敏感字段不落库和错误请求上下文。
- [x] 5.2 后端测试覆盖 SQLite/MySQL schema 兼容、日志采集失败不阻断主业务响应和管理员权限边界。
- [x] 5.3 前端测试覆盖 Snapshot 分组展示、JSON 辅助视图、空态、metadata 解析失败、详情抽屉滚动关闭和 forbidden 状态。
- [x] 5.4 运行相关 pytest、Vitest 和 OpenSpec 校验，并记录验证结果。
