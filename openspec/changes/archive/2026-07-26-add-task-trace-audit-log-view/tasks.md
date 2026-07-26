## 1. 后端 Task Trace 模型与存储

- [x] 1.1 明确最终数据模型：扩展日志表、新增 `task_traces` / `task_trace_spans`，或组合方案，并在实现记录中说明取舍。
- [x] 1.2 实现 SQLite demo schema 与 MySQL production schema，包含 `task_trace_id`、`task_type`、`created_at` 或等价索引。
- [x] 1.3 新增或扩展 Repository / Service 层记录 task trace 与 task span，禁止路由层直接拼 SQL。
- [x] 1.4 实现 `task_trace_id` 生成 / 校验规则，确保不包含原始文件名、手机号、密钥、业务敏感信息或可枚举自增序列。
- [x] 1.5 实现 metadata 脱敏、截断和安全 JSON 序列化，确保不保存 Authorization、Cookie、AccessKey、SecretKey、数据库 DSN、`.env`、真实客户数据或内部绝对路径。

## 2. 日志审计 API 与契约

- [x] 2.1 扩展 `GET /api/v1/admin/logs` 查询能力，支持 `task_trace_id` 或路径 / request_id / task_trace_id 组合筛选。
- [x] 2.2 扩展日志列表响应，返回任务摘要字段，如 `task_trace_id`、`task_type`、`task_status`、`task_duration_ms`。
- [x] 2.3 扩展 `GET /api/v1/admin/logs/{id}` 详情响应，返回 `task_trace` 或 `task_spans` 时间线分组。
- [x] 2.4 保持无 `task_trace_id` 的普通日志兼容，不返回空时间线错误。
- [x] 2.5 确认系统管理员权限边界，employee / 匿名 / 小程序 / 店主端不得访问任务追踪日志。
- [x] 2.6 同步 OpenAPI、Orval、`docs/03-api-index.md`、`docs/04-database-design.md` 与错误码文档。

## 3. 上传首批场景

- [x] 3.1 图片上传记录并关联 `task_trace_id`，覆盖前端、后端、对象存储、数据库和响应节点。
- [x] 3.2 视频上传记录并关联 `task_trace_id`，覆盖 BUG-0085 的 99% 耗时拆解。
- [x] 3.3 文件 / 证书类上传记录并关联 `task_trace_id`，覆盖大小、MIME、对象 key 前缀和失败错误码。
- [x] 3.4 上传控件保持 `idle -> uploading -> done / failed` 状态机，成功同会话即时回显，失败在控件内展示错误。
- [x] 3.5 继续走后端鉴权和对象存储适配层，禁止前端直连未授权对象存储或写入 legacy `data/uploads/`。

## 4. 管理端日志审计 UI

- [x] 4.1 在日志审计列表筛选区加入 `task_trace_id` 查询能力，保持管理端列表页布局不溢出。
- [x] 4.2 日志列表展示任务类型、任务状态、任务耗时或慢节点摘要。
- [x] 4.3 日志详情抽屉新增 Task Trace 分组，展示任务摘要和节点时间线。
- [x] 4.4 支持复制 `task_trace_id` 和关联 `request_id`，复制成功/失败使用 fixed toast 或等价固定反馈，不造成布局位移。
- [x] 4.5 无 task trace 的普通日志保持既有详情展示。
- [x] 4.6 若 Sprint 实现前可导出 PNG，则补 `prototype/web/task-trace-log-detail.png`；若不导出，验收记录写明 N/A 理由。

## 5. 横切验收与测试

- [x] 5.1 后端 pytest 覆盖 task trace 记录、span 排序、日志列表筛选、日志详情时间线、权限、脱敏和 not-found。
- [x] 5.2 后端 pytest 覆盖上传成功、上传校验失败、对象存储失败或慢节点摘要，不泄露敏感字段。
- [x] 5.3 前端 Vitest 覆盖日志审计筛选、任务时间线渲染、复制兜底、无 task trace 日志兼容和分页 DOM。
- [x] 5.4 前端 Vitest 或组件测试覆盖上传状态机 `idle -> uploading -> done / failed`、同会话回显和控件内错误。
- [x] 5.5 OpenAPI / Orval 生成完成后检查生成类型，不手工修改 generated 文件。
- [x] 5.6 Docker Web 入口 `http://localhost:3000` 覆盖上传边界文件验收：小文件成功、超限文件统一错误码，且不得只验证后端 `:8000`。
- [x] 5.7 运行与变更相关的后端、前端、OpenSpec 和目录校验；测试失败时记录阻塞项和修复结论。

## 6. 文档与追溯

- [x] 6.1 同步 REQ-0069 trace、OpenSpec trace 和实现验证摘要。
- [x] 6.2 同步 `docs/03-api-index.md`、`docs/04-database-design.md`、`docs/standards/file-upload.md` 或相关长期文档。
- [x] 6.3 在 Sprint 验收或 Change trace 中引用 `admin-list`、`media-upload` knowledge-base 横切 AC。
- [x] 6.4 修复后评估是否需要将上传任务追踪经验沉淀到 `docs/knowledge-base/incidents/` 或 `best-practices/`；若不需要，记录 N/A 理由。
