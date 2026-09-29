---
created_at: 2026-09-04 17:55:26
updated_at: 2026-09-11 09:12:44
---

## ADDED Requirements

### Requirement: 连接器校验与写入去重

工具执行前 SHALL 使用 Pydantic 校验发布的输入类型、必填项与枚举，写工具 SHALL 校验基础业务 payload。预览 SHALL 使用同一基础模型提示缺失或无效字段，后端 SHALL 保留完整业务校验权威。错误输出 SHALL 使用固定安全摘要，不透传底层异常、完整 payload 或凭据。

#### Scenario: 非法写入参数不触发后端

- **WHEN** 请求缺必填参数、confirmed 类型错误、幂等键长度非法或基础业务字段无效
- **THEN** 工具 SHALL 返回 invalid_arguments 或 invalid_payload
- **AND** SHALL 不发起写入请求。

#### Scenario: 同一操作并发或重启后重试

- **WHEN** 同一后端与用户对同一幂等键重复调用，且使用相同持久化账本
- **THEN** SHALL 最多执行一次后端写入请求
- **AND** 异参数 SHALL 返回 idempotency_conflict，已完成操作 SHALL 返回 duplicate_operation 和 operation_ref
- **AND** 超时、崩溃或结果未知 SHALL 保留预约，返回 operation_uncertain 并要求先核对业务结果，不自动换键重试。

#### Scenario: 媒体输入防护

- **WHEN** 上传工具收到无扩展名、扩展名与 MIME 不符、含路径的文件名、空内容或非法 Base64
- **THEN** 连接器 SHALL 返回 `invalid_media`
- **AND** SHALL NOT 调用后端或预约幂等键
- **AND** 预览 SHALL 提示可根据元数据识别的文件名与空文件风险。

### Requirement: 远程凭据绑定真实用户

远程入口 SHALL 使用服务端受控凭据映射和后端 auth/me 验证调用者身份，缺失配置 SHALL 拒绝访问。工具权限 SHALL 受映射 scope、服务端上限和后端角色共同限制，不新增业务数据所有者隔离规则。

#### Scenario: 用户隔离与权限撤销

- **WHEN** 不同连接器凭据发起请求
- **THEN** SHALL 使用各自的后端凭据验证并查询，不复用共享后端 Token
- **AND** 删除映射、后端身份过期或角色不符合要求 SHALL 阻止后续调用。

#### Scenario: 工具审计脱敏

- **WHEN** 工具调用成功或失败
- **THEN** SHALL 记录工具名、身份摘要、结果、耗时和可用的请求编号/操作引用
- **AND** SHALL 不记录完整参数、响应或凭据。

### Requirement: WorkBuddy 自定义连接器能力边界

系统 SHALL 支持以 MCP + Skill 方式将 ProjectTilesFST 暴露为腾讯 WorkBuddy 自定义连接器。连接器 SHALL 包含 MCP Server、外部 Skill、连接器元信息和连接配置。MCP 工具 SHALL 使用业务语义命名，SHALL NOT 将后端原始 API 暴露为通用 HTTP 代理，SHALL NOT 允许 WorkBuddy 直接访问 SQLite/MySQL、MinIO 底层凭据、运行时文件或任意本机路径。

#### Scenario: 连接器交付包与运行时代码分离

- **WHEN** 系统交付 WorkBuddy 自定义连接器
- **THEN** MCP 运行时代码 SHALL 位于 `src/mcp/workbuddy/`
- **AND** WorkBuddy manifest、`mcp.json`、外部 Skill、图标和打包说明 SHALL 位于 `connectors/workbuddy/`
- **AND** 外部 WorkBuddy Skill SHALL NOT 放入 `.agents/skills/`。

#### Scenario: 禁止通用代理工具

- **WHEN** WorkBuddy 调用 ProjectTilesFST MCP 工具
- **THEN** 工具 SHALL 只暴露明确业务能力
- **AND** 工具 SHALL NOT 接受任意 URL、SQL、文件路径、对象存储 key 或后端路由作为自由输入。

### Requirement: 本地 stdio MCP 只读 PoC

系统 SHALL 在第一阶段支持本地 stdio MCP Server，用于开发、内部验证和小范围演示。该 Server SHALL 连接本地或测试环境 ProjectTilesFST FastAPI，并提供只读工具与管理端写操作 dry-run 工具。第一阶段 SHALL NOT 执行真实管理端写操作、真实媒体上传或生产数据修改。

#### Scenario: 本地 stdio 连接配置

- **GIVEN** 开发或演示人员已配置本地或测试环境 FastAPI base URL
- **WHEN** WorkBuddy 通过本地 stdio 启动 ProjectTilesFST MCP Server
- **THEN** MCP Server SHALL 加载工具列表、参数 schema 和示例指令
- **AND** 凭据 SHALL 通过本地环境变量或受控测试配置注入
- **AND** 仓库 SHALL NOT 保存真实 Token、Cookie、Authorization header 或生产凭据。

#### Scenario: 第一阶段拒绝真实写入

- **WHEN** WorkBuddy 在第一阶段请求创建、编辑、上下架、品牌/类目维护或媒体上传
- **THEN** MCP Server SHALL 只返回 dry-run 草稿或风险提示
- **AND** 系统 SHALL NOT 写数据库
- **AND** 系统 SHALL NOT 上传对象存储
- **AND** 系统 SHALL NOT 改变 SKU、品牌、类目或媒体资源状态。

### Requirement: WorkBuddy 只读 MCP 工具

系统 SHALL 提供稳定的只读 MCP 工具，首批 SHALL 覆盖 SKU 搜索、商品详情、品牌查询、类目查询和目录摘要。只读查询 SHALL 遵守公开展示和管理端权限边界：公开查询只返回可公开数据，管理端查询必须鉴权。

#### Scenario: 搜索 SKU

- **WHEN** WorkBuddy 调用 `search_tile_skus` 并提交关键词、品牌、类目、规格、状态、分页或排序条件
- **THEN** 工具 SHALL 返回 SKU 列表、命中总数、核心字段、品牌、类目、状态和媒体摘要
- **AND** 响应 SHALL 不包含未授权管理字段、对象存储 raw URL 或敏感内部路径。

#### Scenario: 原生工具结果格式

- **WHEN** 原生 MCP 客户端调用工具
- **THEN** tools/call 结果 SHALL 使用 type=text 的 content 内容块，text 为 JSON 序列化业务结果
- **AND** 业务 ok=false 时 SHALL 返回 isError=true。

#### Scenario: SKU 分页合法档位

- **WHEN** WorkBuddy 获取搜索工具 schema 或调用 `search_tile_skus`
- **THEN** page_size schema SHALL 声明 10/20/50/100 枚举且默认 20
- **AND** 运行时 SHALL 将非标准整数向上归一到合法档位并封顶 100，5 转为 10
- **AND** 工具 SHALL 保持页码和筛选条件，返回后端实际分页信息。

#### Scenario: 摘要样本与后端分页分离

- **WHEN** WorkBuddy 调用 `summarize_catalog`，sample_size 为 5
- **THEN** 工具 SHALL 使用 page_size=10 查询 SKU，按原序最多返回 5 条代表 SKU
- **AND** sample_count SHALL 等于实际返回样本数量，后端目录汇总 SHALL 保持不变。

#### Scenario: 查询 SKU 详情

- **WHEN** WorkBuddy 调用 `get_tile_sku_detail` 并提交 SKU ID 或业务标识
- **THEN** 工具 SHALL 返回商品详情、规格、品牌、类目、上下架状态、图片/视频摘要和可公开展示信息
- **AND** 媒体 URL 或预览信息 SHALL 来自后端 API 或受控媒体读取接口。

#### Scenario: 查询品牌与类目

- **WHEN** WorkBuddy 调用 `list_tile_brands` 或 `list_tile_categories`
- **THEN** 工具 SHALL 支持状态、关键词、分页、层级或父级筛选
- **AND** 响应 SHALL 返回品牌或类目的业务摘要、状态和层级信息
- **AND** 响应 SHALL 遵守后端权限和字段白名单。

#### Scenario: 生成目录摘要

- **WHEN** WorkBuddy 调用 `summarize_catalog` 并提交查询条件和摘要目标
- **THEN** 工具 SHALL 返回覆盖范围、代表 SKU、目录摘要、销售辅助话术和资料缺口提示
- **AND** 摘要 SHALL 标明可人工复核的数据来源
- **AND** 系统 SHALL NOT 保存完整 prompt、完整请求体、真实密钥或真实客户敏感数据。

### Requirement: 管理端写操作 dry-run

系统 SHALL 在第一阶段提供管理端写操作 dry-run 或草稿预览能力。dry-run 工具 SHALL 覆盖 SKU 创建草稿、SKU 编辑字段差异预览、SKU 上下架影响预览、品牌创建/编辑草稿、类目创建/编辑草稿和媒体上传参数安全校验预览。

#### Scenario: dry-run 返回拟变更摘要

- **WHEN** WorkBuddy 调用任一 `preview_*` dry-run 工具
- **THEN** 工具 SHALL 返回拟变更字段、字段差异、缺失必填项、权限要求、风险提示和下一步人工确认方式
- **AND** 响应 SHALL 明确该调用未执行真实写入。

#### Scenario: dry-run 不产生副作用

- **WHEN** dry-run 请求包含有效或无效业务 payload
- **THEN** 系统 SHALL NOT 新增、更新或删除数据库记录
- **AND** 系统 SHALL NOT 上传、移动或删除对象存储对象
- **AND** 系统 SHALL NOT 改变 SKU 上下架状态。

### Requirement: HTTPS 远程 MCP 服务

系统 SHALL 在第二阶段支持 HTTPS 远程 MCP 服务，供 WorkBuddy 企业 Agent 或多人场景使用。远程服务 SHALL 支持无状态 Streamable HTTP JSON、健康检查、超时、限流、日志配置和环境变量注入。

#### Scenario: 无状态 JSON 传输协商

- **WHEN** 原生客户端初始化远程 MCP 并发送后续请求
- **THEN** 系统 SHALL 协商受支持的 2024-11-05、2025-03-26 或 2025-06-18，未知初始化版本返回 2025-06-18
- **AND** 后续 MCP-Protocol-Version 缺失按 2025-03-26，非法版本返回 400
- **AND** 系统 SHALL 校验 JSON Content-Type 和同时接受 JSON/event-stream 的 Accept，分别以 415/406 拒绝不兼容请求
- **AND** 合法通知及客户端响应 SHALL 返回无正文 202，缺 id 的消息 SHALL NOT 执行写工具
- **AND** 系统 SHALL 提供无状态 JSON 响应，不创建 session，GET/DELETE 返回 405，默认超出 8 MiB 的完整 JSON 请求返回 413
- **AND** 非法 JSON、非法 envelope、未知方法、非法参数及内部错误 SHALL 返回固定脱敏 JSON-RPC 错误

#### Scenario: 单实例部署准备与证据边界

- **WHEN** 交付远程部署准备包
- **THEN** 系统 SHALL 提供非 root 镜像、只读根文件系统、只读凭据目录、私有 loopback 端口、持久化幂等卷和默认关闭的写工具
- **AND** health SHALL 仅表示进程存活，不表示用户凭据或后端连通性已通过
- **AND** 本地 SDK 互操作和容器 smoke SHALL NOT 代替真实 HTTPS 网关与 WorkBuddy 原生远程验收

#### Scenario: 远程 MCP 健康检查

- **WHEN** 运维或 WorkBuddy 平台检查远程 MCP 服务健康状态
- **THEN** 服务 SHALL 返回可读健康状态
- **AND** 健康检查 SHALL NOT 暴露真实凭据、内部连接串、对象存储 endpoint 密钥或敏感环境变量。

#### Scenario: 远程工具调用失败

- **WHEN** 远程 MCP 工具调用因超时、鉴权失败、scope 不足、后端不可用或参数非法失败
- **THEN** 工具 SHALL 返回可读错误摘要、稳定错误码或等价错误分类
- **AND** 日志 SHALL 只保存脱敏摘要
- **AND** 响应 SHALL NOT 包含 Authorization、Cookie、Token、真实密钥、完整 payload 或本机绝对路径。

### Requirement: 管理端真实写操作

系统 MAY 在第二阶段开放管理端真实写操作，首批范围 SHALL 限定为 SKU 创建/编辑、SKU 上下架、品牌/类目维护和媒体上传。真实写操作 SHALL 通过 ProjectTilesFST 后端 API、服务层和对象存储适配层执行，SHALL 校验身份、工具级 scope、Pydantic schema 和幂等键。删除操作 SHALL NOT 进入 MVP。

#### Scenario: 真实写操作鉴权和确认

- **WHEN** WorkBuddy 请求执行真实写操作
- **THEN** 系统 SHALL 校验管理员或员工身份
- **AND** 系统 SHALL 校验工具级 scope 允许该操作
- **AND** WorkBuddy Skill SHALL 要求展示目标对象、变更摘要、影响范围和确认动作
- **AND** 请求 SHALL 携带幂等键或等价去重机制。

#### Scenario: 下架目标与后端一致

- **WHEN** 用户确认以 `DISABLED` 为目标执行 SKU 下架
- **THEN** 工具 SHALL 调用后端 unpublish 并返回实际状态
- **AND** 旧参数 `DRAFT` SHALL 仅作为下架兼容别名，预览显示 `DISABLED`，SHALL NOT 宣称转为草稿。

#### Scenario: 真实写操作返回审计入口

- **WHEN** 真实写操作成功或失败
- **THEN** 响应 SHALL 返回业务对象 ID、结果状态、错误码或等价错误分类
- **AND** 响应 SHOULD 返回 request id、task trace id 或等价审计追踪入口
- **AND** 错误摘要 SHALL 脱敏并截断。

#### Scenario: 媒体上传经后端适配层

- **WHEN** WorkBuddy 执行真实媒体上传
- **THEN** 工具 SHALL 调用 ProjectTilesFST 后端上传 API
- **AND** 后端 SHALL 校验 MIME、大小、扩展名、用途和目标业务对象
- **AND** 媒体 SHALL 经 MinIO/S3 兼容对象存储适配层写入
- **AND** 工具 SHALL NOT 持有对象存储写入凭据或自行拼接 raw URL。

### Requirement: 连接器鉴权与工具级权限

系统 SHALL 为 WorkBuddy 连接器建立独立鉴权和权限边界。第一阶段 MAY 使用本地测试 Token 或测试 Bearer Token；第二阶段 SHALL 支持可轮换连接器凭据、工具级 scope 或企业网关注入凭据。后端 SHALL NOT 信任 WorkBuddy 传入的用户身份字段作为认证或授权依据。

#### Scenario: 凭据缺失或 scope 不足

- **WHEN** WorkBuddy 调用需要鉴权或 scope 的工具但凭据缺失、过期或权限不足
- **THEN** 系统 SHALL 拒绝调用
- **AND** 响应 SHALL 返回明确错误码或错误分类
- **AND** 日志和响应 SHALL NOT 暴露真实凭据内容。

#### Scenario: 不信任客户端身份字段

- **WHEN** 工具请求携带 WorkBuddy 用户名、昵称、邮箱或自声明角色
- **THEN** 后端 SHALL NOT 将这些字段作为认证、授权或租户隔离依据
- **AND** 后端 SHALL 仅使用可信鉴权上下文和已校验 scope 判定权限。

### Requirement: 连接器请求日志与 Task Trace

系统 SHALL 将 WorkBuddy 连接器调用作为直接 API 调用入口纳入产品数据采集与链路观测模型。连接器 SHALL NOT 伪造 `usage_events`。所有后端 API 调用 SHALL 写入 `request_logs`，并能识别 `workbuddy_connector` 或等价来源。写操作、媒体上传、批量或长耗时工具 SHALL 写入 `task_traces` 和 `task_trace_spans`。

#### Scenario: 只读工具请求日志

- **WHEN** WorkBuddy 调用只读 MCP 工具并触发后端 API 请求
- **THEN** `request_logs` SHALL 记录服务端可信 `request_id`
- **AND** `request_logs` SHALL 记录 `client_type=workbuddy_connector` 或等价来源
- **AND** `request_logs` SHOULD 记录 `client_request_id`、资源类型、结果和脱敏错误摘要
- **AND** 系统 SHALL NOT 为该直接 API 调用伪造 `usage_events`。

#### Scenario: 写操作与上传接入 Task Trace

- **WHEN** WorkBuddy 执行真实写操作、媒体上传、批量或长耗时工具
- **THEN** 系统 SHALL 创建或关联 `task_traces`
- **AND** 关键流程节点 SHALL 记录到 `task_trace_spans`
- **AND** `task_traces.parent_request_id` SHALL 优先关联 `request_logs.request_id`。

#### Scenario: 观测数据脱敏

- **WHEN** 系统记录连接器请求日志、Task Trace、流程节点或审计摘要
- **THEN** 记录 SHALL NOT 保存完整 prompt、完整请求体、完整响应体、Authorization、Cookie、Token、真实密钥、对象存储完整敏感 key、本机绝对路径或真实客户敏感数据。

#### Scenario: 品牌与类目真实写入链路

- **WHEN** 已鉴权的 WorkBuddy 来源调用品牌或类目创建、编辑、启用、停用
- **THEN** 后端 SHALL 通过 TaskTraceService 记录成功或失败节点并关联服务端 request_id
- **AND** 观测失败 SHALL NOT 覆盖业务成功或业务错误
- **AND** SHALL NOT 为非连接器来源或只读请求额外创建该类连接器任务。

### Requirement: 连接器 API、OpenAPI、Orval 与测试同步

系统 SHALL 优先复用现有业务 API 支撑 WorkBuddy 工具。若新增或修改 HTTP API、请求头、响应字段、错误码或 Schema，变更 SHALL 同步 OpenAPI、Orval、`docs/03-api-index.md`、API 治理说明和集成测试。若新增数据库结构、索引、迁移或保留周期，变更 SHALL 同步 SQLite/MySQL schema、数据库设计文档和测试。

#### Scenario: 新增连接器专用 API

- **WHEN** 现有业务 API 不能安全或高效支撑 AI 工具调用
- **THEN** 系统 MAY 新增连接器专用只读聚合接口或 dry-run 接口
- **AND** 新接口 SHALL 使用 `/api/v1` 前缀
- **AND** 新接口 SHALL 使用统一 response envelope、Pydantic 校验和稳定错误码
- **AND** OpenAPI、Orval、API 文档和集成测试 SHALL 同步更新。

#### Scenario: 不需要 Orval 或 DB 变更

- **WHEN** 实现仅新增 MCP 运行时代码和连接器交付包，且未新增或修改 Web 可消费 HTTP API、数据库结构或迁移
- **THEN** 实现验收 SHALL 明确记录 Orval 或 DB 变更 N/A 原因
- **AND** N/A 说明 SHALL 可追溯到本 Change 的 design、tasks 或验收材料。

### Requirement: 连接器部署与环境变量

系统 SHALL 为 WorkBuddy 连接器提供本地 stdio 与远程 HTTPS 两种部署说明。新增环境变量 SHALL 同步 `.env.example` 或部署 env 示例，并使用占位值和安全注释。第二阶段远程 MCP 服务 SHALL 提供 Docker Compose 或生产等价部署、健康检查、超时、限流和日志级别配置。

#### Scenario: 本地 stdio 配置示例

- **WHEN** 开发或演示人员配置本地 WorkBuddy 连接器
- **THEN** `connectors/workbuddy/` SHALL 提供本地 stdio MCP 配置示例
- **AND** 示例 SHALL 只包含占位 base URL、测试凭据变量名和安全说明
- **AND** 示例 SHALL NOT 包含真实凭据、真实客户数据或本机私有绝对路径。

#### Scenario: 远程 HTTPS 部署配置

- **WHEN** 团队部署第二阶段远程 MCP 服务
- **THEN** 部署文档 SHALL 说明服务启动方式、ProjectTilesFST API base URL、连接器凭据、超时、限流、日志级别和健康检查
- **AND** Docker Compose 或生产等价配置 SHALL 使用可提交 env 示例
- **AND** 真实 `.env`、密钥、数据库连接串和对象存储凭据 SHALL 不进入 Git。
