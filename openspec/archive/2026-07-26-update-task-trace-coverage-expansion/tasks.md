## 1. Scope 与设计确认

- [x] 1.1 输出首批任务型接口候选清单，至少评估保存 SKU、批量操作、导入导出、媒体处理、异步任务和复杂查询六类场景。
- [x] 1.2 为每个候选接口标注任务类型、优先级、关键步骤、预期 span、是否异步、是否批量、是否涉及对象存储或外部依赖。
- [x] 1.3 标注未纳入首批的接口原因和后续排期建议。
- [x] 1.4 确认是否需要新增任务状态查询接口；如新增，补充 API、错误码、OpenAPI、Orval 和测试。

## 2. 后端 Task Trace 接入

- [x] 2.1 扩展或新增 Task Trace helper / service / repository，支持生成或确认可信 `task_trace_id`、绑定 request_id、开始 / 结束 / 失败 span。
- [x] 2.2 支持同步任务、异步任务和批量任务上下文传递；异步 worker 必须继承原始 `task_trace_id`。
- [x] 2.3 接入首批任务型接口 span，覆盖校验、业务处理、持久化、外部依赖、响应、失败、超时和部分成功摘要。
- [x] 2.4 span 写入失败必须降级记录，不得掩盖主业务错误。
- [x] 2.5 metadata 必须统一脱敏、截断、安全 JSON 化，不保存 Authorization、Cookie、密钥、DSN、`.env`、真实客户数据、内部绝对路径或完整敏感请求体。

## 3. API / DB / Docs 同步

- [x] 3.1 如新增或调整 Task Trace 存储字段，同步 SQLite schema、MySQL schema、迁移脚本、索引和 `docs/04-database-design.md`。
- [x] 3.2 如接口响应新增 `task_trace_id`、任务摘要、任务状态或时间线字段，同步 OpenAPI、Orval 和 Web API 类型。
- [x] 3.3 更新 `docs/03-api-index.md` 与适用错误码文档，说明新增字段、查询参数、响应结构和错误码。
- [x] 3.4 确保管理端日志 API 和首批任务型接口继续使用统一 `ApiResponse`。

## 4. Web 管理端

- [x] 4.1 在复杂任务成功、失败、处理中或部分成功反馈中展示或提供复制 `task_trace_id` 的入口。
- [x] 4.2 复制反馈使用 fixed toast 或等价固定层，不造成页面布局位移。
- [x] 4.3 无 `task_trace_id` 的任务保持原交互，不显示空追踪组件。
- [x] 4.4 失败反馈只展示安全错误码、脱敏摘要和追踪标识，不暴露内部路径、堆栈、原始请求体或敏感 metadata。
- [x] 4.5 若实际改动日志审计列表、上传控件或弹窗，补读对应 best-practices 并补充 AC-XCUT 或执行输出说明。

## 5. 测试与验证

- [x] 5.1 后端 pytest 覆盖 task_trace_id 生成 / 透传、span 写入、失败节点、部分成功、异步继承、权限和脱敏。
- [x] 5.2 Web Vitest / Testing Library 覆盖追踪标识展示、复制反馈、无 trace 兼容、失败反馈和日志审计入口。
- [x] 5.3 OpenAPI / Orval 生成校验通过，生成物不得手工修改。
- [x] 5.4 涉及生产 DB、对象存储、上传或异步任务边界时，在 apply 中段前置 smoke evidence stub；无对应边界时记录 N/A。
- [x] 5.5 运行相关测试并在 Change trace 或 apply 输出中记录验证摘要。

## 6. 门禁

- [x] 6.1 `openspec validate update-task-trace-coverage-expansion --strict` 通过。
- [x] 6.2 后续 `/opsx-apply` 前，REQ-0074 必须先纳入某个 Sprint 正式范围。
