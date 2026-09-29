---
created_at: 2026-09-04 17:55:26
updated_at: 2026-09-11 09:12:44
---

## 上下文

REQ-0132 已纳入 `sprint-029`，状态为 `in_sprint`。本 Change 负责把 ProjectTilesFST 暴露为腾讯 WorkBuddy 自定义连接器，交付采用两阶段路线：

- 第一阶段：本地 stdio MCP PoC，面向开发、演示和内部验证，只读查询为主，管理端写操作仅 dry-run。
- 第二阶段：HTTPS 远程 MCP 服务，面向企业 WorkBuddy Agent 或多人场景，补齐鉴权、工具级权限、审计、限流、部署和受控真实写操作。

现有能力边界：

- SKU、品牌、类目能力由现有 `/api/v1/admin/*` 和公开查询能力承载。
- 媒体上传必须经后端授权上传接口和 MinIO 适配层。
- 请求日志和 Task Trace 已有通用规范，连接器属于直接 API 调用入口。
- 外部连接器目录边界已经明确：`src/mcp/<connector>/` 放运行时代码，`connectors/<connector>/` 放外部交付包。

## 目标

- 提供 WorkBuddy 可消费的 MCP 工具集合和中文 Skill 使用说明。
- 第一阶段交付本地 stdio PoC，覆盖 SKU 搜索、商品详情、品牌/类目查询、目录摘要和写操作 dry-run。
- 第二阶段设计 HTTPS 远程 MCP 服务边界，支持企业级鉴权、工具级 scope、审计、限流、错误摘要和真实写操作。
- 保证连接器只能通过后端 API、服务层和对象存储适配层访问 ProjectTilesFST，不直连数据库、MinIO 或运行时文件。
- 将连接器调用纳入 `request_logs`；高风险、上传、批量或长耗时工具纳入 `task_traces` 和 `task_trace_spans`。

## 非目标

- 第一阶段不开放真实写操作、真实删除、真实媒体上传或生产数据修改。
- 第一阶段不建设公网 HTTPS 服务、OAuth 授权流或企业级网关。
- 不建设独立 BI 看板、复杂审批平台或跨企业多租户市场能力。
- 不恢复 `.codex/`、`.cursor/`、`.claude/`、`.opencode/`、`.kiro/` 等外部工具入口目录。
- 不新增管理端 UI；若第二阶段需要配置页，应另在实现任务中复用既有 Design System。

## 设计决策

### 本地隔离验收返修

新增独立 Compose 验收环境与真实 stdio 协议驱动，专属 SQLite、MinIO 和幂等卷，不读取业务 env、不发布宿主机端口。媒体上限缩小为 1 MiB 验证边界，不能替代生产文件性能与视频播放验收。单机共享卷、四进程同键并发、容器重启分别留证，不据此宣称跨主机保证。

下架目标使用后端实际状态 `DISABLED`；保留 `DRAFT` 作为旧下架别名，预览显示实际目标 `DISABLED`，不表示转成草稿。媒体输入在连接器增加无路径文件名、MIME/扩展名一致、非空合法 Base64 校验，非法输入返回 `invalid_media`，在后端调用与幂等预约前拒绝；大小和业务用途由后端继续判定。

真实验收发现品牌/类目八种维护动作缺失 Task Trace。本轮仅为该两类路由的 WorkBuddy 来源请求追加鉴权后的观测依赖，复用 TaskTraceService 和独立观测 Session，记录接收、业务成功/失败及响应节点；记录固定摘要，不记录 payload，观测失败不覆盖业务结果。其余客户端和业务 HTTP 契约不变。

### 验收返修：校验、幂等与远程身份

工具 schema 通过 Pydantic 模型在执行前强校验；SKU 分页整数仍先归一化，其他字段不做隐式类型转换。写入基础 payload 校验与预览共用模型，完整业务字段由后端 Pydantic 与服务层作最终校验。预览只返回字段摘要、变更字段及缺失项，不返回完整 payload；错误字符串使用固定摘要，不透传底层异常。外部 Skill 中文说明参数、确认与不确定结果恢复。

幂等在连接器统一工具入口执行：验证身份后，以后端地址、可信用户 ID、幂等键定位持久化写入预约，以工具和规范化参数摘要检测冲突。只记录摘要和状态，不存业务请求或响应。原子目录创建确保同一共享卷上单个执行者，先 fsync 预约再调用 API；成功标记 completed，未知结果保持 pending/uncertain。重复调用返回稳定错误及 operation_ref 而不重放完整结果；业务结果通过查询恢复。跨主机不共享目录、直接调用后端或更换键不在该去重保证内，不能宣称后端具备全局幂等。持久化部署与保留规则见部署文档。

远程入口按用户隔离身份，连接器凭据摘要映射到后端凭据与 scope，调用时经 auth/me 验证 active admin/employee，不接受请求体身份或客户端自报 scope。scope 为映射与服务端上限交集，必须具备 catalog:read。未配置映射拒绝访问，旧共享 Bearer 迁移到映射文件；本地 stdio 配置不受影响。该设计不增加 OAuth、不改变后端数据可见性。HTTP Origin 请求拒绝，通知返回 202，后台调用移入线程池；真实 HTTPS 和远程 MCP 客户端兼容需部署验收。

### D1 目录与交付边界

运行时代码放入 `src/mcp/workbuddy/`，包含 MCP server 入口、tool registry、schema、后端 API client、鉴权/审计适配和测试。WorkBuddy 交付包放入 `connectors/workbuddy/`，包含 manifest、`mcp.json`、外部 Skill、图标占位和 README。

取舍：将 MCP 运行时代码放入 `src/mcp` 可以复用项目源码治理、测试和部署边界；将外部平台资产放入 `connectors` 可以避免 `.agents/skills/` 与 WorkBuddy Skill 混淆。

### D2 工具不是通用 HTTP 代理

MCP 工具使用业务语义命名，例如 `search_tile_skus`、`get_tile_sku_detail`、`list_tile_brands`、`list_tile_categories`、`summarize_catalog` 和 `preview_*` dry-run 工具。工具不得暴露任意 URL、SQL、文件路径或对象存储 key 读取能力。

取舍：业务语义工具会比通用代理多一些适配代码，但能稳定控制权限、参数 schema、错误摘要和 AI 可理解输出。

### D2.1 SKU 分页与摘要样本

MCP tools/call 结果采用标准文本内容块：content[].type=text，text 保存 JSON 序列化业务结果；业务 ok=false 时 isError=true。禁止使用自定义 type=json 内容块，确保原生客户端可解析。

`search_tile_skus.page_size` 的 schema 枚举为 10/20/50/100，默认 20。运行时兼容非标准整数，向上取最近合法档位，低于 10 使用 10，高于 100 使用 100；页码和筛选条件保持原值，返回后端实际分页信息。查询前 5 条时可取 10 条，由调用方展示前 5 条，不能将后端整页伪装为 5 条分页。

`summarize_catalog.sample_size` 仍为 1 至 50，默认 10；SKU 请求采用同一分页归一化，再按样本数截取代表 SKU，sample_count 反映实际样本数量，后端汇总数据不截取。

### D3 第一阶段写操作全部 dry-run

第一阶段写操作只返回拟变更字段、差异、缺失项、权限要求、风险提示和人工确认方式，不调用真实写入 API，不上传对象存储，不改变上下架状态。

取舍：dry-run 降低 AI 误操作风险，并让团队先验证 WorkBuddy 意图识别和草稿质量；真实写入保留到第二阶段，在鉴权审计完整后开放。

### D4 第二阶段真实写操作需要 scope、幂等和确认

真实写工具必须校验连接器凭据、后端用户身份、工具级 scope、Pydantic schema 和幂等键。高风险操作前，WorkBuddy Skill 必须要求展示目标对象、变更摘要、影响范围和确认动作。删除操作不进入 MVP。

取舍：确认和幂等会增加调用流程，但能显著降低重复创建、误上下架和上传错对象的风险。

### D5 连接器作为直接 API 调用入口接入观测

连接器不伪造 `usage_events`。所有后端 API 调用必须进入 `request_logs`，并能识别 `client_type=workbuddy_connector` 或等价来源、`client_request_id`、资源类型、结果和脱敏错误摘要。写操作、媒体上传、批量或长耗时工具必须接入 Task Trace。

取舍：直接 API 入口保持观测模型语义清晰；真正由 Web 管理端 UI 触发的连接器配置行为，才按 Web 管理端行为事件采集。

### D6 API 与部署同步

连接器优先复用现有业务 API。若需要新增连接器专用聚合查询或 dry-run API，必须保持 `/api/v1` 前缀、统一响应 envelope、错误码和 Pydantic 校验，并同步 OpenAPI、Orval、`docs/03-api-index.md`、API 治理说明和集成测试。第二阶段远程 MCP 服务必须补充 Docker Compose 或生产等价部署、健康检查、环境变量示例和超时/限流配置。

取舍：复用业务 API 可以减少后端面积；新增聚合接口只在现有 API 无法安全表达 AI 工具需求时使用。

## 产品数据采集与链路观测

```yaml
product_data_collection_observability:
  status: applicable
  affected_layers:
    - backend_api
    - request_logs
    - task_traces
    - task_trace_spans
    - admin_web_indirect
    - object_storage_indirect
    - deployment
  reason: 连接器将作为直接 API 调用方访问 ProjectTilesFST，并在第二阶段执行管理端写操作、媒体上传和远程 MCP 服务部署，涉及请求来源识别、工具调用审计、任务链路、错误摘要、环境变量和凭据安全。
  validation:
    - 直接 API 调用不得伪造 usage_events。
    - 所有后端 API 调用必须进入 request_logs，并保存 workbuddy_connector 来源、client_request_id、资源类型、结果和脱敏错误摘要。
    - dry-run 工具必须验证不写数据库、不上传对象存储、不改变业务状态。
    - 真实写操作、媒体上传、批量或长耗时工具必须验证 task_traces 与 task_trace_spans。
    - 日志、Trace、错误摘要和审计记录不得保存完整 prompt、完整 payload、Authorization、Cookie、Token、真实密钥、本机绝对路径或真实客户敏感数据。
```

若实现阶段新增或修改 API contract，必须同步 OpenAPI、Orval、API 文档和测试；若新增 DB 表、字段、索引、迁移或保留周期，必须同步 SQLite/MySQL schema、数据库设计文档和测试。

## 原型与 UI 冲突

本 REQ 目录下未提供 `prototype/`，第一阶段不新增 Web 管理端 UI，UI Explore Gate 不触发。

第二阶段若新增管理端连接器配置、权限或审计页面，必须复用 `AdminListPage`、`AdminEditPage`、shadcn 基础组件和 semantic token；不得新增营销式页面，不得新增裸 Hex。

## 风险与缓解

| 风险 | 缓解 |
|---|---|
| WorkBuddy 工具过宽导致越权或数据泄露 | 只提供业务语义工具，限制字段白名单，后端鉴权和工具级 scope 双重校验。 |
| dry-run 与真实写入语义不一致 | dry-run 输出必须明确拟提交 payload、字段差异和真实写入所需权限；真实写入复用相同 Pydantic schema 或等价校验。 |
| 连接器日志泄露 prompt、Token 或对象存储 key | 统一脱敏 helper，仅记录摘要、错误码、资源类型和截断后的安全字段。 |
| 远程 MCP 服务部署后超时或重复提交 | 工具级超时、限流、幂等键、健康检查和 Task Trace 节点一起落地。 |
| 媒体上传绕过后端适配层 | MCP 工具只能调用后端上传 API，不允许持有 MinIO 写入凭据或拼接 raw URL。 |

## 迁移与回滚

- 第一阶段新增本地 stdio 配置和连接器代码，不改变现有 Web、小程序和后端业务流程；回滚时移除 `src/mcp/workbuddy/` 与 `connectors/workbuddy/` 即可停止连接器入口。
- 第二阶段新增远程 MCP 服务和环境变量时，必须提供服务启停、健康检查和凭据轮换说明；回滚时禁用远程 MCP 服务、撤销连接器凭据并保留脱敏审计记录。
- 若新增 DB 结构，必须提供迁移和回滚策略；若只复用现有表与 request/task trace 表，应在实现验收中说明 DB 变更 N/A。

## 实现确认

- 远程 MCP 入口采用无状态 Streamable HTTP JSON，协商 2024-11-05、2025-03-26 和 2025-06-18；通知/客户端响应返回 202，不提供服务端 SSE 或 session。Pydantic 校验 JSON-RPC，工具错误保留文本内容块。官方 SDK 只作为互操作测试依赖，不替换既有 registry。
- 部署使用独立单实例 Compose，继承后端锁定依赖镜像、非 root/只读根目录、私有 loopback 端口、只读凭据目录和持久化卷。网关终止 TLS，默认写入关闭、完整 JSON 请求体限制 8 MiB；企业凭据、TLS、跨主机和保留恢复策略仍单独验收，不能以本地 SDK/容器通过替代。
- 第二阶段真实写操作 scope 已落地为 `tile_sku:write`、`tile_sku:publish`、`brand:write`、`category:write` 和 `media:upload`；凭据由环境变量或企业密钥系统注入。
- 真实媒体上传已通过后端 `/api/v1/admin/uploads/*` multipart API 适配，MCP 不直接访问 MinIO 或对象存储。
