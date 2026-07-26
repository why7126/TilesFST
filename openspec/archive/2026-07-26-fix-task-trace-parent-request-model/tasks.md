## 1. 数据模型与追踪上下文

- [x] 1.1 盘点现有 Task Trace / span 存储结构，确定 `parent_request_id` 使用独立字段或结构化 metadata，并在实现说明中记录取舍。
- [x] 1.2 如采用独立字段，新增 SQLite / MySQL 兼容 schema、索引和迁移，避免 SQLite-only DDL。
- [x] 1.3 更新 Task Trace repository / schema / service，使任务摘要可写入和查询 `parent_request_id`。
- [x] 1.4 更新 Task Trace 创建逻辑，从后端请求上下文写入 `parent_request_id`，不得信任前端传值。
- [x] 1.5 更新 task span 写入逻辑，使有请求上下文的 span 写入当前 `request_id`，内部节点保留安全兜底。

## 2. API 与上传链路

- [x] 2.1 更新任务型接口和上传接口，使 request logs、usage events、audit logs、Task Trace 和 spans 使用同一个 `task_trace_id` 串联。
- [x] 2.2 校验前端携带的 `task_trace_id` 格式、权限边界和任务归属；缺失或非法值不得破坏主请求日志落库。
- [x] 2.3 更新日志详情 API，支持从主请求 `request_id` 返回关联 Task Trace 摘要，并在 Task Trace 时间线中返回 span `request_id`。
- [x] 2.4 兼容历史缺失字段：无 `task_trace_id`、无 `parent_request_id` 或无 span `request_id` 时返回安全空值或隐藏关联入口。
- [x] 2.5 确认图片、视频、文件上传 span 至少覆盖后端接收、文件校验、对象存储写入、数据库落库和响应返回节点。

## 3. Web 管理端

- [x] 3.1 更新日志详情 Task Trace 分组，展示 `task_trace_id`、`parent_request_id`、任务状态、任务类型和耗时。
- [x] 3.2 更新 span 列表展示 `span_name`、状态、耗时、`request_id`、错误码和摘要。
- [x] 3.3 支持复制或定位 `parent_request_id`、`task_trace_id`、span `request_id`，反馈使用 fixed toast 或等价固定层且不造成布局位移。
- [x] 3.4 历史数据缺少字段时展示“未记录”或隐藏跳转入口，不展示误导性关联。
- [x] 3.5 保持上传控件 `idle → uploading → done / failed` 状态机、同会话即时回显和控件内错误展示。

## 4. OpenAPI、Orval 与文档

- [x] 4.1 同步 OpenAPI response models、summaries、descriptions 和 tags，暴露新增追踪字段。
- [x] 4.2 运行 Orval 生成 Web client types，禁止手写 generated 文件。
- [x] 4.3 更新 `docs/03-api-index.md`、`docs/04-database-design.md` 和适用错误码文档。
- [x] 4.4 若新增环境变量、上传限制或对象存储策略说明，同步 `.env.example` 和部署文档。

## 5. 测试与验证

- [x] 5.1 后端测试覆盖 `parent_request_id` 写入、span `request_id` 写入、一主请求多 Task Trace、缺失字段兜底和权限拒绝。
- [x] 5.2 后端测试覆盖非法 `task_trace_id` 不破坏主请求日志落库，并返回或记录明确错误摘要。
- [x] 5.3 前端测试覆盖日志详情 Task Trace 分组、复制反馈、缺失字段兜底和无布局位移反馈。
- [x] 5.4 上传链路测试覆盖图片、视频、文件至少一个代表场景的 `task_trace_id`、`parent_request_id` 与 span `request_id`。
- [x] 5.5 Docker Web `http://localhost:3000` 验证上传边界文件：小文件成功、超限文件返回统一错误码，不仅验证后端 `:8000`。
- [x] 5.6 运行相关 pytest、Vitest / Testing Library、OpenSpec 校验和 Workflow Sync 检查。
