## ADDED Requirements

### Requirement: Task Trace 主请求关联模型
系统 SHALL 为 Task Trace 建立主请求、子请求与 span 的强关联模型，确保任务链路可以从主请求进入 Task Trace，也可以从 Task Trace span 回到对应请求日志。

#### Scenario: Task Trace 记录触发主请求
- **WHEN** API 请求触发一个 Task Trace
- **THEN** 系统 SHALL 记录触发该 Task Trace 的主请求 `request_id`
- **AND** 该字段语义 SHALL 为 `parent_request_id`
- **AND** `parent_request_id` SHALL 来自后端请求上下文，不得信任前端传入值。

#### Scenario: parent_request_id 存储可查询
- **WHEN** 系统持久化 Task Trace 任务摘要
- **THEN** 系统 SHALL 使用独立字段或等价结构化字段保存 `parent_request_id`
- **AND** OpenSpec design SHALL 说明采用独立字段还是 metadata 结构化字段
- **AND** 查询路径 SHALL 索引友好，不得以无界 metadata 模糊扫描作为主查询方式。

#### Scenario: 一个主请求触发多个 Task Trace
- **WHEN** 一个主请求触发多个 Task Trace
- **THEN** 系统 SHALL 保留一对多关联
- **AND** 管理端日志详情 SHALL 能区分多个任务摘要。

#### Scenario: span 写入当前 request_id
- **WHEN** task span 发生在某个 HTTP 请求生命周期中
- **THEN** span SHALL 写入当前请求的 `request_id`
- **AND** 同一 `task_trace_id` SHALL 能关联多个 request id。

#### Scenario: 内部 span 缺少请求上下文
- **WHEN** task span 是无直接 HTTP 请求上下文的后端内部节点
- **THEN** span SHALL 保留 `task_trace_id`、span 顺序、状态和耗时
- **AND** span MAY 继承 `parent_request_id` 或将 `request_id` 标为空
- **AND** API 和页面 SHALL 不展示误导性请求跳转。

#### Scenario: 任务型接口统一透传 task_trace_id
- **WHEN** 任务型接口创建、处理或上报任务节点
- **THEN** request logs、usage events、audit logs、Task Trace 和 task spans SHALL 使用同一个 `task_trace_id` 串联
- **AND** 后端 SHALL 校验前端携带的 `task_trace_id` 格式、权限边界和任务归属。

#### Scenario: 缺失或非法 task_trace_id 不破坏请求日志
- **WHEN** 任务型接口收到缺失或非法 `task_trace_id`
- **THEN** 主请求日志 SHALL 仍然落库
- **AND** 系统 SHALL 返回或记录明确的可观测错误摘要。

#### Scenario: 日志详情支持双向定位
- **WHEN** admin 查看带有 `request_id` 或 `task_trace_id` 的日志详情
- **THEN** 日志详情 SHALL 能从主请求 `request_id` 展示关联 Task Trace 摘要或入口
- **AND** Task Trace 时间线 SHALL 展示 span 关联的 `request_id`
- **AND** admin SHALL 能从 span 的 `request_id` 定位到对应请求日志详情。

#### Scenario: 历史缺失字段安全兜底
- **WHEN** 历史日志缺少 `task_trace_id`、Task Trace 缺少 `parent_request_id` 或 span 缺少 `request_id`
- **THEN** API 和页面 SHALL 安全兜底
- **AND** SHALL NOT 展示空状态错误或误导性关联。

#### Scenario: 上传首批验证主请求关联
- **WHEN** admin 上传图片、视频或文件
- **THEN** 上传主请求 SHALL 生成或绑定 `task_trace_id`
- **AND** Task Trace SHALL 记录上传主请求的 `request_id` 为 `parent_request_id`
- **AND** 上传相关 span SHALL 至少覆盖后端接收、文件校验、对象存储写入、数据库落库和响应返回节点
- **AND** 有请求上下文的上传 span SHALL 写入当前 API 请求的 `request_id`。

#### Scenario: 追踪字段不作为权限依据
- **WHEN** 系统使用 `request_id`、`parent_request_id` 或 `task_trace_id` 定位日志或任务
- **THEN** 这些字段 SHALL 仅用于追踪与定位
- **AND** SHALL NOT 作为权限判断依据
- **AND** 任务链路查询 SHALL 仅系统管理员可访问。

#### Scenario: 追踪数据保持安全脱敏
- **WHEN** 系统记录 Task Trace、span 或关联日志 metadata
- **THEN** 系统 SHALL NOT 存储 Authorization、Cookie、AccessKey、SecretKey、数据库 DSN、`.env` 内容、真实客户数据、内部绝对路径或完整敏感请求体。

#### Scenario: 契约与生成物同步
- **WHEN** 日志详情、任务追踪 API、上传响应或数据模型新增 `parent_request_id`、span `request_id` 或任务摘要字段
- **THEN** OpenAPI SHALL 暴露这些字段
- **AND** Orval SHALL 生成或更新对应 Web client types
- **AND** generated files SHALL NOT be hand-edited
- **AND** `docs/03-api-index.md`、`docs/04-database-design.md` 和适用错误码文档 SHALL 同步更新。

#### Scenario: media-upload 横切验收
- **WHEN** 实现涉及图片、视频或文件上传链路
- **THEN** 上传控件 SHALL 保持 `idle → uploading → done / failed` 状态机
- **AND** 上传成功后同会话 SHALL 即时回显媒体结果
- **AND** 上传失败 SHALL 在控件内展示错误，不能只依赖全局 toast
- **AND** Docker Web 入口 `http://localhost:3000` SHALL 覆盖小文件成功和超限文件统一错误码验收
- **AND** 上传链路 SHALL 继续走后端鉴权和对象存储适配层，不得前端直连未授权对象存储或写入 legacy `data/uploads/`。
