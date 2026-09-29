---
requirement_id: REQ-0132-workbuddy-custom-connector
title: 腾讯 WorkBuddy 自定义连接器支持
terminal: multi
version: v1
status: in_sprint
owner: product
source: capture.md
priority: P1
parent_requirement:
created_at: 2026-09-04 16:50:11
updated_at: 2026-09-04 18:17:47
related_change: add-workbuddy-custom-connector
---

# REQ-0132 腾讯 WorkBuddy 自定义连接器支持

## 1. 需求背景

ProjectTilesFST 已具备瓷砖 SKU、品牌、类目、规格、媒体上传、管理端权限、公开查询、小程序查询、请求日志和任务链路观测等业务基础。企业内部人员在销售支持、选品咨询、商品资料维护和目录整理时，仍需要在管理端、资料表、聊天工具和人工问答之间切换，重复查询和整理成本较高。

腾讯 WorkBuddy 支持通过自定义连接器把外部服务能力接入 AI 工作流。将 ProjectTilesFST 封装为 WorkBuddy 自定义连接器后，企业人员可以用自然语言查询 SKU、获取商品详情、整理品牌/类目目录摘要，并在受控权限下发起管理端写操作。

本需求用于定义 ProjectTilesFST 的 WorkBuddy 连接器能力边界。交付采取分阶段策略：第一阶段用本地 stdio MCP + Skill 做只读 PoC，验证查询工具、目录摘要和 AI 使用价值；第二阶段升级为 HTTPS 远程 MCP 服务，补齐企业级鉴权、审计、限流、部署和管理端真实写操作。

## 2. 目标用户

| 用户 | 诉求 |
|---|---|
| 企业内部销售 / 导购 | 能用自然语言快速查询 SKU、规格、品牌、类目和商品详情，用于客户咨询和选品沟通。 |
| 商品运营人员 | 能让 WorkBuddy 辅助整理目录摘要、发现商品资料缺口，并生成待提交的维护草稿。 |
| 管理员 | 能控制连接器可访问的数据范围、可执行工具和写操作权限，并审计连接器操作。 |
| 研发 / 运维人员 | 能通过 MCP 工具日志、API 请求日志和 Task Trace 排查连接器调用失败、超时和越权问题。 |
| AI Agent / WorkBuddy | 能通过稳定、清晰、最小权限的 MCP 工具调用 ProjectTilesFST，而不是直接访问数据库或未收敛 API。 |

## 3. 范围

### 3.1 本期包含

- 建设 ProjectTilesFST 的 WorkBuddy 自定义连接器能力定义，采用 MCP + Skill。
- 第一阶段支持本地 stdio MCP PoC，连接本地或测试环境 FastAPI。
- 第一阶段支持只读工具：SKU 搜索、商品详情查询、品牌查询、类目查询和目录摘要。
- 第一阶段支持管理端写操作的 dry-run / 草稿预览，不真实提交业务数据。
- 第二阶段支持 HTTPS 远程 MCP 服务，供企业 WorkBuddy Agent 或多人场景使用。
- 第二阶段支持企业级鉴权、凭据注入、工具级权限、调用审计、限流、超时和错误摘要。
- 第二阶段支持管理端真实写操作，首批范围包括 SKU 创建/编辑、SKU 上下架、品牌/类目维护和媒体上传。
- 连接器调用必须通过 ProjectTilesFST 后端 API、服务层和对象存储适配层，不直接访问 SQLite/MySQL/MinIO。
- 连接器必须纳入请求日志、直接 API 调用追踪和任务类操作 Task Trace。
- 后续 OpenSpec Change 中应同步 API、部署、环境变量、测试、文档和连接器 Skill 使用说明。

### 3.2 本期不包含

- 不让 WorkBuddy 直接访问数据库、对象存储底层凭据或运行时文件。
- 不在第一阶段执行真实写操作、真实删除、真实媒体上传或生产数据修改。
- 不在第一阶段建设公网 HTTPS 服务、OAuth 授权流或企业级网关。
- 不自动审批、自动发布或自动删除 SKU、品牌、类目和媒体资源。
- 不绕过现有管理端 `admin/employee` 权限边界。
- 不保存完整请求体、完整响应体、Authorization、Cookie、Token、真实密钥、真实客户数据或对象存储完整敏感 key。
- 不建设独立 BI 看板、复杂工作流审批平台或跨企业多租户商业化市场能力。

## 4. 功能要求

### FR-001 连接器形态与能力边界

系统 MUST 支持以 MCP + Skill 方式将 ProjectTilesFST 暴露为腾讯 WorkBuddy 自定义连接器。

连接器 SHOULD 至少包含：

| 组件 | 说明 |
|---|---|
| MCP Server | 向 WorkBuddy 暴露稳定工具，并调用 ProjectTilesFST FastAPI。 |
| Skill | 说明工具用途、参数、错误处理、权限边界和确认规则。 |
| 连接器元信息 | 连接器名称、描述、图标、示例指令和版本要求。 |
| 配置文件 | 本地 stdio 或远程 HTTPS MCP 连接配置。 |

连接器工具 MUST 采用业务语义命名，不得把后端原始 API 全量暴露为通用请求代理。

### FR-002 第一阶段本地 stdio 只读 PoC

第一阶段 MUST 支持本地 stdio MCP Server，用于开发、内部验证和小范围演示。

本地 PoC MUST 支持以下只读能力：

- 按关键词、品牌、类目、规格、状态等条件搜索 SKU。
- 查询单个 SKU 的商品详情、规格、媒体摘要和公开展示信息。
- 查询品牌列表和品牌摘要。
- 查询类目树和类目摘要。
- 基于查询结果生成目录摘要、销售问答辅助材料或资料缺口提示。

第一阶段 SHOULD 支持写操作 dry-run 工具，仅返回拟提交变更摘要、字段差异和风险提示，不调用真实写入 API。

### FR-003 第二阶段 HTTPS 远程 MCP 服务

第二阶段 MUST 支持 HTTPS 远程 MCP 服务，供 WorkBuddy 企业 Agent 或多人使用。

远程 MCP 服务 MUST 满足：

- 通过 HTTPS 暴露 SSE 或 streamable HTTP 连接方式。
- 单次工具调用设置合理超时，失败时返回可读错误。
- 支持服务端环境变量或网关注入凭据，不在仓库记录真实凭据。
- 支持健康检查、部署配置、日志和基础监控。
- 可通过 Docker Compose 或生产等价方式部署。

### FR-004 只读工具

连接器 MUST 提供稳定的只读 MCP 工具。

首批只读工具 SHOULD 包含：

| 工具 | 输入 | 输出 |
|---|---|---|
| `search_tile_skus` | 关键词、品牌、类目、规格、分页、排序 | SKU 列表、命中总数、核心字段、媒体摘要 |
| `get_tile_sku_detail` | SKU ID 或业务标识 | 商品详情、规格、品牌、类目、图片/视频摘要 |
| `list_tile_brands` | 状态、关键词、分页 | 品牌列表、状态、摘要 |
| `list_tile_categories` | 层级、状态、父级 | 类目树或列表 |
| `summarize_catalog` | 查询条件、摘要目标 | 目录摘要、推荐话术、资料缺口 |

只读工具 MUST 遵守公开展示和管理端权限边界：公开查询只返回可公开数据，管理端查询必须鉴权。

### FR-005 管理端写操作 dry-run

第一阶段 SHOULD 提供管理端写操作 dry-run / 草稿预览能力。

dry-run 工具 SHOULD 覆盖：

- SKU 创建草稿。
- SKU 编辑字段差异预览。
- SKU 上下架影响预览。
- 品牌创建/编辑草稿。
- 类目创建/编辑草稿。
- 媒体上传参数和安全校验预览。

dry-run MUST 不写数据库、不上传对象存储、不改变上下架状态、不删除资源。返回结果 MUST 包含拟变更字段、缺失必填项、权限要求、风险提示和下一步人工确认方式。

### FR-006 管理端真实写操作

第二阶段 MAY 开放管理端真实写操作，首批范围为 SKU 创建/编辑、SKU 上下架、品牌/类目维护和媒体上传。

真实写操作 MUST 满足：

- 调用前具备管理员或员工身份鉴权，且工具级 scope 允许该操作。
- 高风险操作前要求 WorkBuddy 明确展示目标对象、变更摘要和确认动作。
- 请求必须携带幂等键或等价去重机制，避免重复创建或重复上传。
- 删除类操作不进入 MVP；如后续开放，必须独立评审和强确认。
- 媒体上传必须走后端上传接口和 MinIO 适配层，保留文件大小、MIME Type、扩展名和对象 Key 安全校验。
- 写入结果必须返回业务对象 ID、结果状态、错误码和审计追踪入口。

### FR-007 鉴权与权限

连接器 MUST 建立独立的鉴权和权限边界。

鉴权方案 SHOULD 分阶段演进：

| 阶段 | 建议方案 |
|---|---|
| 第一阶段 | 本地测试环境配置临时 API Token 或测试 Bearer Token，仅限开发/演示数据。 |
| 第二阶段 | 独立连接器凭据、工具级 scope、可轮换 token 或 OAuth / gateway 授权。 |

连接器凭据 MUST 不写入 Git，不出现在 `.env.example` 以外的真实值，不进入日志和 AI 输出。后端 MUST 不信任 WorkBuddy 传入的用户身份字段作为权限依据。

### FR-008 审计、请求日志与 Task Trace

连接器调用 MUST 按直接 API 调用入口纳入 ProjectTilesFST 观测模型。

观测要求：

- 不伪造 `usage_events`。
- API 请求必须写入 `request_logs`，并能识别 `client_type=workbuddy_connector` 或等价来源。
- MCP 工具调用 SHOULD 生成 `client_request_id` 或等价调用 ID，用于 WorkBuddy 侧与后端日志对齐。
- 写操作、上传、批量或长耗时工具 SHOULD 写入 Task Trace 和流程节点。
- 日志和 Trace 只保存脱敏摘要，不保存完整 prompt、完整 payload、Authorization、Cookie、Token、真实密钥或本机路径。

### FR-009 API、OpenAPI 与 Orval

若本需求新增或修改 HTTP API、请求头、响应字段、错误码或 Schema，系统 MUST 同步 OpenAPI、Orval、API 文档和集成测试。

连接器工具对后端 API 的调用 SHOULD 优先复用现有业务 API；当现有 API 不适合 AI 工具调用时，MAY 新增连接器专用只读聚合接口或 dry-run 接口，但必须保持 `/api/v1` 前缀、统一响应 envelope 和 Pydantic 校验。

### FR-010 部署与环境变量

第二阶段远程 MCP 服务 MUST 明确部署形态和环境变量边界。

部署要求 SHOULD 覆盖：

- MCP Server 服务启动方式。
- 连接 ProjectTilesFST API 的 base URL。
- 连接器凭据、超时、限流和日志级别。
- 本地 stdio 与远程 HTTPS 配置示例。
- Docker Compose 或生产部署矩阵的服务、端口、环境变量和健康检查。

新增环境变量 MUST 同步 `.env.example` 或部署 env 示例，并使用占位值和安全注释。

## 5. UI 约束

第一阶段不要求新增 Web 管理端 UI。

第二阶段若需要在管理端配置连接器凭据、工具权限、审计查询或启停开关，则 SHOULD 复用现有管理端 Design System、semantic token 和列表/表单组件，不单独建设营销式页面。

WorkBuddy Skill 和连接器说明中的用户可见文案 MUST 中文优先，并明确写操作确认规则、权限边界和错误恢复方式。

## 6. 关联需求

| 关联项 | 关系 |
|---|---|
| REQ-0006-tile-sku-management | SKU 创建、编辑、上下架能力来源。 |
| REQ-0005-brand-management | 品牌维护能力来源。 |
| REQ-0005-tile-category-management | 类目维护能力来源。 |
| REQ-0012-object-storage-key-layout | 媒体对象存储安全边界来源。 |
| REQ-0124-log-audit-behavior-trace-model | 请求日志、直接 API 调用和 Task Trace 观测模型来源。 |
| REQ-0126-product-data-collection-observability-standard | 产品数据采集与链路观测门禁来源。 |

## 7. 状态块

```yaml
requirement_status:
  status: in_sprint
  readiness: Partially Ready
  lifecycle_stage: review
  next_step: /opsx-apply REQ-0132-workbuddy-custom-connector
scope_decisions:
  first_stage:
    transport: stdio
    write_mode: dry-run
    real_write_enabled: false
  second_stage:
    transport: https
    real_write_enabled: true
    write_tools:
      - sku_create
      - sku_update
      - sku_publish_toggle
      - brand_manage
      - category_manage
      - media_upload
product_data_collection_observability:
  applicable: true
  affected_layers:
    - backend_api
    - request_logs
    - task_traces
    - task_trace_spans
    - admin_web_indirect
    - object_storage_indirect
    - deployment
  reason: 连接器将作为直接 API 调用方访问 ProjectTilesFST，并在第二阶段执行管理端写操作、媒体上传和远程 MCP 服务部署，涉及请求来源识别、链路字段、工具调用审计、任务链路、错误摘要、环境变量和凭据安全。
  usage_events: 直接 API 调用不伪造 usage_events；如后续管理端新增连接器配置 UI，则对应页面访问和表单提交按 Web 管理端行为事件规则采集。
  request_logs: 所有后端 API 调用默认写入 request_logs，并应能识别 workbuddy_connector 来源、client_request_id、资源类型、结果和错误摘要。
  task_trace: 写操作、媒体上传、批量或长耗时工具应接入 task_traces 和 task_trace_spans。
  validation: 后续 /opsx-apply 与 OpenSpec Change 需补充直接 API 调用、鉴权越权、dry-run 不写入、真实写操作审计、上传链路、OpenAPI/Orval、Docker/HTTPS 部署和脱敏日志验证。
```
openspec_changes:
  - change_id: add-workbuddy-custom-connector
    type: add
    status: applied
