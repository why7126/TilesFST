## MODIFIED Requirements

### Requirement: 管理端日志查询 API
系统 SHALL 提供仅管理员可用的日志列表与详情查询 API。

#### Scenario: 管理员查询日志列表
- **WHEN** 已认证 admin 调用 `GET /api/v1/admin/logs`
- **THEN** 系统 SHALL 返回统一响应，包含分页日志项、total、page、page_size 和指标摘要。

#### Scenario: 支持日志列表筛选
- **WHEN** admin 按日志类型、时间范围、操作者、client type、status code 或 result、resource id、path、keyword、request id 或 task trace id 筛选
- **THEN** 系统 SHALL 仅返回匹配日志，并按最新优先排序。

#### Scenario: 操作者筛选保持 actor_user_id 语义
- **WHEN** admin 通过日志审计页面选择某个操作者候选后查询日志
- **THEN** 日志列表 API SHALL 使用该用户的稳定 `actor_user_id` 作为过滤条件
- **AND** API SHALL NOT 将用户显示名称、昵称或账号字符串解释为 `actor_user_id`
- **AND** API SHALL 保持既有 `actor_user_id` 查询参数兼容。

#### Scenario: 管理员查询日志详情
- **WHEN** 已认证 admin 针对已存在日志调用 `GET /api/v1/admin/logs/{id}`
- **THEN** 系统 SHALL 返回基础信息、请求信息、操作者与客户端、操作上下文、事件属性和 metadata 等详情分组。

#### Scenario: 拒绝非管理员访问
- **WHEN** employee、店主端客户端、小程序用户或匿名用户调用管理端日志 API
- **THEN** 系统 SHALL 使用已文档化的 forbidden 响应拒绝访问。

#### Scenario: 日志不存在返回 not found
- **WHEN** admin 请求不存在的 log id
- **THEN** 系统 SHALL 返回已文档化的 404 类错误响应。

### Requirement: 管理端日志审计页面

系统 SHALL 提供 Web 管理端日志审计页面，并对齐产品 v2 Golden Reference。

#### Scenario: 管理员打开日志审计页

- **WHEN** 已认证 admin 打开 `/admin/logs`
- **THEN** 系统 SHALL 在既有 Admin Shell 内渲染日志审计页面
- **AND** SYSTEM sidebar SHALL 展示并激活 `日志审计`。

#### Scenario: 指标与筛选可见

- **WHEN** admin 查看日志审计页
- **THEN** 页面 SHALL 展示 TODAY LOGS、API ERRORS、SLOW REQUESTS 和 SENSITIVE OPS 指标卡
- **AND** 页面 SHALL 展示日志类型、时间范围、状态或结果、操作者、Task Trace ID、路径 / Request ID 筛选。
- **AND** 时间范围 SHALL 提供最近5分钟、最近10分钟、最近30分钟、最近1小时、最近3小时、最近6小时、最近12小时、最近1天、最近2天、最近3天和最近7天，不提供全部时间选项。
- **AND** 状态或结果筛选 SHALL 使用下拉选择交互，支持成功、失败和常见 HTTP 状态码精确筛选，且 SHALL 至少包含 `422 参数校验错误`。

#### Scenario: 操作者筛选使用可搜索单选下拉

- **WHEN** admin 使用 `/admin/logs` 的操作者筛选项
- **THEN** 页面 SHALL 提供单选可搜索下拉，而不是要求 admin 直接输入 User ID
- **AND** 下拉 SHALL 支持按用户名称和账号搜索操作者候选
- **AND** 候选项 SHALL 只展示两行：第一行账号 `username`，第二行用户名称 `display_name || username`
- **AND** 候选项 SHALL 使用账号行区分同名用户。

#### Scenario: 操作者筛选查询日志

- **WHEN** admin 在操作者下拉中选择一个用户候选
- **THEN** 页面 SHALL 使用该用户的 `id` 作为 `actor_user_id` 请求日志列表
- **AND** 页面 SHALL NOT 将用户名称或账号字符串作为 `actor_user_id` 传给日志列表 API
- **AND** 筛选变化 SHALL 将当前页重置为 1 并重新查询。

#### Scenario: 操作者筛选清空与重置

- **WHEN** admin 清空操作者筛选或点击页面重置
- **THEN** 页面 SHALL 清除 `actor_user_id` 过滤条件
- **AND** 日志列表 SHALL 按全部操作者和其他默认筛选条件重新查询。

#### Scenario: 操作者候选异常状态

- **WHEN** 操作者候选正在加载、无匹配结果或加载失败
- **THEN** 页面 SHALL 在下拉或等价控件区域展示清晰状态
- **AND** 候选加载失败 SHALL NOT 阻止 admin 使用日志类型、时间范围、状态、Task Trace ID、路径 / Request ID 等其他筛选
- **AND** 候选加载失败反馈 SHALL 与日志列表查询失败反馈可区分。

#### Scenario: 日志表格支持排障

- **WHEN** admin 查看日志行
- **THEN** 表格 SHALL 展示时间、类型、事件或摘要、操作者账号、客户端、状态或结果、耗时、Task Trace、request id 和详情操作。
- **AND** 操作者列 SHALL 使用 `actor_username` 单行展示，不展示用户名称。
- **AND** Task Trace 与 request id 列 SHALL 均以单行短 ID 加复制操作展示。
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
- **AND** 前端测试 SHALL 覆盖列表渲染、筛选、操作者候选搜索、操作者选择、清空、重置、候选无结果、候选加载失败、同名用户区分、request_id 复制成功、Clipboard API 不可用兜底、复制写入失败兜底、详情抽屉、forbidden 状态和分页结构。
