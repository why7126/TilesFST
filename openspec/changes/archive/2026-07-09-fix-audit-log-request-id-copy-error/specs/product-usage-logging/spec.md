## MODIFIED Requirements

### Requirement: 管理端日志审计页面

系统 SHALL 提供 Web 管理端日志审计页面，并对齐产品 v2 Golden Reference。

#### Scenario: 管理员打开日志审计页

- **WHEN** 已认证 admin 打开 `/admin/logs`
- **THEN** 系统 SHALL 在既有 Admin Shell 内渲染日志审计页面
- **AND** SYSTEM sidebar SHALL 展示并激活 `日志审计`。

#### Scenario: 指标与筛选可见

- **WHEN** admin 查看日志审计页
- **THEN** 页面 SHALL 展示 TODAY LOGS、API ERRORS、SLOW REQUESTS 和 SENSITIVE OPS 指标卡
- **AND** 页面 SHALL 展示日志类型、时间范围、操作者、状态或结果、资源或 ID、路径或 request id 筛选。
- **AND** 状态或结果筛选 SHALL 使用下拉选择交互，支持成功、失败和常见 HTTP 状态码精确筛选，且 SHALL 至少包含 `422 参数校验错误`。

#### Scenario: 日志表格支持排障

- **WHEN** admin 查看日志行
- **THEN** 表格 SHALL 展示时间、类型、事件或摘要、操作者、客户端、状态或结果、耗时、request id、复制操作和详情操作。
- **AND** 类型与状态或结果 SHALL 通过不同颜色或等价视觉样式区分不同值，便于管理员快速扫描异常日志。

#### Scenario: request_id 可复制且不造成布局位移

- **WHEN** admin 复制带有 request id 的日志记录
- **THEN** 系统 SHALL 优先将完整 request id 写入系统剪贴板
- **AND** 系统 SHALL 使用 fixed toast 或等价不造成布局位移的反馈展示成功、失败或兜底结果
- **AND** 当 Clipboard API 不存在、浏览器拒绝写入或写入失败时，系统 SHALL 不抛出未捕获错误
- **AND** 系统 SHALL 提供手动复制指引、可选中文本或等价兜底，使 admin 仍可获取完整 request id
- **AND** 系统 SHALL 仅在剪贴板写入成功时记录 `copy_request_id` 成功行为事件。

#### Scenario: employee 不可打开页面

- **WHEN** 已认证 employee 打开 `/admin/logs`
- **THEN** 系统 SHALL 按既有管理端授权模式展示 forbidden 状态或重定向
- **AND** 不暴露日志数据。

#### Scenario: 日志能力测试覆盖

- **WHEN** 实现完成
- **THEN** 后端测试 SHALL 覆盖日志记录、校验、脱敏、权限、筛选和 not-found 行为
- **AND** 前端测试 SHALL 覆盖列表渲染、筛选、request_id 复制成功、Clipboard API 不可用兜底、复制写入失败兜底、详情抽屉、forbidden 状态和分页结构。
