---
requirement_id: REQ-0024-product-usage-logging
title: 产品使用行为埋点与接口请求日志详情
terminal: multi
version: v2
status: in_sprint
owner: product
source: capture.md
priority: P1
parent_requirement:
created_at: 2026-07-02 11:51:22
updated_at: 2026-07-03 09:33:56
product_prototype_version: REQ-0024-log-audit-page-v2
---

# REQ-0024 产品使用行为埋点与接口请求日志详情

## 1. 需求背景

当前平台已经具备基础审计能力：`audit_logs` 表与 `AuditLogRepository` 已用于系统设置等管理端操作留痕，系统设置中也存在审计配置项（如保留天数、敏感字段脱敏）。但现有能力仍偏向单点业务审计，尚未形成统一的产品使用行为采集、接口请求日志记录、日志详情查询与安全治理闭环。

瓷砖信息管理平台后续会同时服务企业内部员工、店主 Web 展示端与微信小程序。为了分析功能使用情况、定位接口异常、追踪关键操作路径，并支持平台安全审计，需要新增一套 MVP 级别的“产品使用日志与埋点”能力。

本需求定位为平台治理能力，优先交付管理端与后端 API 的日志闭环；店主 Web 展示端与微信小程序埋点纳入设计范围，但是否本期实现由后续 `/req-complete` 与 Sprint 评审确认。

## 2. 目标用户

| 用户 | 诉求 |
|---|---|
| 系统管理员 | 查看关键操作、接口请求、错误详情与行为轨迹，支撑排障和审计 |
| 企业内部运营人员 | 在授权范围内理解数据维护、上传、上下架等操作是否成功 |
| 开发 / 运维人员 | 通过 request_id、耗时、状态码、错误摘要快速定位接口问题 |
| 产品负责人 | 了解页面访问、搜索筛选、按钮点击等核心功能使用情况 |

## 3. 范围

### 3.1 本期包含

- 后端 API 请求日志采集：记录请求方法、路径、状态码、耗时、request_id、操作者、客户端来源等摘要字段。
- 产品使用行为事件采集：覆盖页面访问、搜索筛选、按钮点击、表单提交、媒体上传、登录退出、发布/下架等关键行为。
- 埋点事件字典：人为定义事件名、触发时机、必填属性、可选属性与禁止属性，后续由代码枚举和后端校验固化。
- 日志详情存储：以 metadata JSON 或等价结构保存脱敏后的请求摘要、响应摘要、错误信息与上下文。
- 管理端日志查询入口：提供筛选、分页、列表与详情查看能力，仅系统管理员可访问。
- 统一安全策略：敏感字段脱敏、请求/响应体截断、日志保留周期、访问权限边界。
- 数据治理：明确 SQLite demo 与生产 MySQL 下的索引、分页、清理与归档策略。
- API 与 OpenAPI 约束：新增/变更接口时同步 `docs/03-api-index.md`、OpenAPI、Orval 与集成测试。

### 3.2 本期不包含

- 用户画像、漏斗分析、转化分析、实时大屏等复杂 BI 能力。
- 第三方埋点平台接入。
- 默认保存完整请求体或完整响应体。
- 日志批量导出、下载文件、水印报表。
- 分库分表、外部日志系统、消息队列异步采集。
- 运维级日志（容器 stdout、Nginx access log、数据库慢查询日志）的统一接入。

## 4. 信息架构

```text
admin-shell
└── SYSTEM
    ├── 系统设置
    ├── 接口文档
    └── 日志审计（建议新增）
        ├── 指标摘要
        │   ├── Today Logs
        │   ├── API Errors
        │   ├── Slow Requests
        │   └── Sensitive Ops
        ├── 筛选区
        │   ├── 日志类型：请求日志 / 行为事件 / 审计操作
        │   ├── 时间范围
        │   ├── 操作者
        │   ├── 状态码 / 结果
        │   ├── 资源 / ID
        │   └── 路径 / request_id
        ├── 日志列表
        └── 日志详情抽屉
```

建议管理端路由为 `/admin/logs` 或 `/admin/audit-logs`，页面面包屑展示为 `SYSTEM / LOG AUDIT`，导航入口位于 SYSTEM 分组。该页面与 `REQ-0017-system-settings` 的审计配置保持语义区分：系统设置中的“审计配置”用于配置策略；日志审计页用于查询、定位和查看日志详情。

产品 v2 原型确认管理端首屏包含：

- 左侧管理端 Shell 与 SYSTEM / 日志审计高亮。
- 顶部标题“日志审计”、说明文案与页面操作区。
- 四个指标卡：`TODAY LOGS`、`API ERRORS`、`SLOW REQUESTS`、`SENSITIVE OPS`。
- 筛选区：日志类型、时间范围、操作者、状态 / 结果、资源 / ID、路径 / request_id，支持查询与重置。
- 日志表格：时间、类型、事件 / 摘要、操作者、客户端、状态、耗时、request_id、复制、详情。
- 右侧详情抽屉：`LOG DETAIL`，可关闭，展示基础信息、请求信息、操作者 / 客户端、操作上下文、埋点属性、metadata JSON。

## 5. 数据模型要求

### 5.1 日志模型策略

实现阶段可在以下两种方案中择一，并在 OpenSpec design 中说明取舍：

| 方案 | 说明 | 适用情况 |
|---|---|---|
| 扩展 `audit_logs` | 在现有统一审计表基础上增加日志类型、请求字段、结果字段与索引 | 希望统一查询入口，控制实现复杂度 |
| 新增 `request_logs` / `usage_events` | 请求日志、行为事件与审计操作分表存储 | 后续数据量较大，便于独立清理与索引优化 |

无论采用哪种方案，MUST 保证日志查询使用 Repository 或统一数据访问层，SQL MUST 参数化。

### 5.2 建议字段

| 字段 | 说明 |
|---|---|
| `id` | 日志唯一 ID |
| `log_type` | `request`、`usage_event`、`audit` |
| `request_id` | 单次请求追踪 ID；同一请求产生的行为/错误可关联 |
| `actor_user_id` | 登录用户 ID；匿名访问可为空 |
| `actor_role` | `admin`、`employee`、`anonymous` 等 |
| `client_type` | `web_admin`、`web_catalog`、`miniapp`、`backend` |
| `event_name` | 行为事件名或业务动作 |
| `method` | HTTP 方法；非请求事件可为空 |
| `path` | 请求路径或页面路径 |
| `status_code` | HTTP 状态码 |
| `duration_ms` | 请求耗时 |
| `ip_address` | 客户端 IP，展示时可脱敏 |
| `user_agent` | User-Agent，需限制长度 |
| `summary` | 人类可读摘要 |
| `metadata` | JSON 字符串，保存脱敏后的上下文 |
| `created_at` | 创建时间 |

### 5.3 索引与保留周期

- MUST 为常用筛选建立索引：`created_at`、`log_type`、`actor_user_id`、`request_id`、`status_code`、`path` 或等价组合索引。
- MUST 支持按时间倒序分页查询，避免一次性加载大量日志。
- MUST 与系统设置中的 `audit.retention_days` 或新增日志保留策略对齐。
- 生产 MySQL 实现 MUST 同步 schema，并避免 SQLite-only DDL。

## 6. API 要求

### 6.1 建议接口

| 方法 | 路径 | 权限 | 说明 |
|---|---|---|---|
| GET | `/api/v1/admin/logs` | `require_system_admin` | 分页查询日志列表 |
| GET | `/api/v1/admin/logs/{id}` | `require_system_admin` | 查询单条日志详情 |
| POST | `/api/v1/usage-events` | 登录态或匿名受控 | 上报产品行为事件；是否公开给店主端/小程序待确认 |

接口实现 MUST 使用统一 `ApiResponse` 响应结构。列表接口 MUST 返回分页结构：`items`、`total`、`page`、`page_size`。

### 6.2 查询参数

| 参数 | 说明 |
|---|---|
| `page` / `page_size` | 分页参数，需限制最大值 |
| `log_type` | 日志类型 |
| `keyword` | 匹配摘要、路径、事件名或 request_id |
| `actor_user_id` | 操作者筛选 |
| `client_type` | 客户端类型 |
| `status_code` | 状态码筛选 |
| `start_time` / `end_time` | 时间范围 |

### 6.3 错误码

- 无权限访问日志查询接口 MUST 返回现有认证/授权错误码。
- 参数非法 MUST 使用参数校验错误码，并在 `docs/standards/error-codes.md` 同步登记。
- 日志不存在可复用 404 类错误码，或新增日志领域错误码；新增时 MUST 同步 `error_codes.py` 与错误码文档。

## 7. 埋点事件字典要求

### 7.1 设计原则

埋点事件和属性 MUST 由产品、研发、测试在需求阶段人为定义，形成事件字典；系统自动补充通用上下文。不得完全依赖自动采集 DOM 点击、接口调用或页面路径作为埋点事实源。

```text
人为定义
├── event_name：发生了什么
├── event_category：所属业务域
├── trigger：触发时机
├── required_properties：必填业务属性
├── optional_properties：可选业务属性
└── forbidden_properties：禁止采集字段

系统自动补充
├── user_id / role
├── client_type
├── page_path
├── request_id
├── session_id
├── timestamp
└── user_agent / ip 摘要
```

事件字典在 `/req-complete` 阶段 SHOULD 生成到需求包内，例如 `tracking-events.md`；实现阶段 MUST 将稳定事件名与属性规则同步为代码侧枚举、Schema 或等价校验逻辑。

### 7.2 MVP 事件清单

| event_name | 触发时机 | 必填属性 | 禁止属性 |
|---|---|---|---|
| `page_view` | 页面加载完成 | `page_path`, `module` | `token`, `password` |
| `search_submit` | 用户提交搜索 | `module`, `keyword` | `token`, `password` |
| `filter_change` | 筛选条件变化 | `module`, `filter_name`, `filter_value` | `token`, `password` |
| `detail_view` | 用户打开详情抽屉或详情页 | `module`, `entity_type`, `entity_id` | `token`, `password` |
| `copy_request_id` | 用户复制 request_id | `module`, `entity_type`, `entity_id`, `request_id` | `token`, `password`, `authorization`, `cookie` |
| `entity_create` | 新建业务对象成功 | `entity_type`, `entity_id` | `raw_payload`, `password` |
| `entity_update` | 编辑保存成功 | `entity_type`, `entity_id`, `changed_fields` | `before_value`, `password` |
| `entity_delete` | 删除业务对象成功 | `entity_type`, `entity_id` | `raw_payload`, `token` |
| `status_change` | 启停、上下架、冻结等状态变化 | `entity_type`, `entity_id`, `from_status`, `to_status` | `raw_payload`, `token` |
| `media_upload` | 媒体上传完成 | `media_type`, `business_type`, `file_size`, `result` | `raw_filename`, `token` |
| `login_success` | 登录成功 | `user_id`, `role` | `password`, `token` |
| `login_failed` | 登录失败 | `username_masked`, `reason` | `password`, `token` |
| `api_error` | 接口异常 | `request_id`, `path`, `status_code`, `error_code` | `authorization`, `cookie` |

### 7.3 校验与演进

- 前端和后端 MUST 只能上报事件字典中已定义的 `event_name`。
- 后端 MUST 校验必填属性、字段类型、字段长度与禁止字段。
- 后端 MUST 自动补充身份、角色、客户端、request_id、时间戳等通用上下文，不信任前端传入的身份信息。
- 敏感字段 MUST 在后端统一过滤；前端脱敏只能作为体验优化，不可作为安全边界。
- 新增事件或调整属性 MUST 先更新事件字典，再同步代码枚举、Schema、测试与 OpenSpec。
- 埋点上报失败 MUST 不阻断主业务流程，但 SHOULD 记录可观测错误摘要。

## 8. 功能要求

### FR-001 请求日志自动采集

- 后端 MUST 在统一中间件或等价入口中为 API 请求生成 `request_id`。
- MUST 记录请求方法、路径、状态码、耗时、操作者、客户端来源与创建时间。
- MUST 支持记录异常请求的错误码、错误消息摘要与 request_id。
- MUST NOT 记录健康检查、静态资源、Swagger 文档、媒体直出等噪声路由，除非后续配置明确开启。

### FR-002 行为事件采集

- MUST 定义事件命名规范，例如 `page_view`、`search_submit`、`filter_change`、`button_click`、`form_submit`、`media_upload`、`sku_publish`、`login_success`。
- MUST 基于事件字典实现行为事件采集；不得在业务代码中随意拼接未登记的 `event_name`。
- MUST 将事件字典中的必填属性同步为前端调用约束与后端 Pydantic Schema 或等价校验。
- 管理端 MUST 至少覆盖：登录、退出、页面访问、搜索筛选、创建/编辑/删除、启停/上下架、媒体上传、系统设置变更。
- 店主 Web 展示端与微信小程序事件覆盖范围待确认；若纳入本期，MUST 支持匿名会话标识且不得采集敏感个人信息。
- 行为事件上报失败 MUST 不阻断用户主流程。

### FR-003 日志详情与脱敏

- 日志详情 MUST 展示基础字段、操作者、请求摘要、行为上下文、错误摘要与 metadata。
- 详情抽屉 MUST 按产品 v2 原型分组展示：基础信息、请求信息、操作者 / 客户端、操作上下文、埋点属性、metadata JSON。
- 基础信息 MUST 包含日志 ID、日志类型、状态 / 结果、request_id、发生时间。
- 请求信息 MUST 包含 Method、Path、Status Code、Duration、Error Code；慢请求 SHOULD 在耗时旁标注。
- 操作者 / 客户端 MUST 包含操作者、User ID、客户端、IP 摘要、User Agent 摘要。
- 操作上下文 MUST 包含业务动作、操作摘要、失败原因或结果摘要。
- 埋点属性 MUST 包含 event_name、module、entity_type、entity_id、changed_fields 等事件字典字段。
- 默认 MUST NOT 保存完整密码、Token、Authorization Header、Cookie、真实密钥、MinIO AccessKey/SecretKey、数据库 DSN。
- 请求体、响应体如确需保存，MUST 采用字段白名单、敏感字段黑名单、长度截断与显式配置开关。
- metadata JSON 必须可解析；解析失败时列表页仍可展示基础字段。

### FR-004 管理端日志查询

- MUST 提供日志列表页，支持筛选、分页、排序与详情查看。
- 列表页指标摘要 MUST 展示今日日志总量、API 错误、慢请求、敏感操作数量。
- 筛选区 MUST 支持日志类型、时间范围、操作者、状态 / 结果、资源 / ID、路径 / request_id。
- 表格 MUST 展示时间、类型、事件 / 摘要、操作者、客户端、状态、耗时、request_id、复制与详情操作。
- MUST 提供按 request_id 查询或复制 request_id 的能力，便于排障。
- MUST 仅允许系统管理员访问；运营员工直链访问 MUST 返回 403 或管理端无权限页。
- UI MUST 复用管理端列表页模式，优先使用 `AdminListPage`、shadcn 基础组件和既有管理端样式，不新增营销式页面。

### FR-005 审计配置联动

- MUST 与系统设置中的审计配置保持一致，包括保留天数、是否允许导出、是否强制敏感操作审计、是否脱敏敏感字段。
- 若现有配置不足以表达请求日志和行为埋点策略，MUST 在 OpenSpec 阶段说明新增配置项，并同步 `.env.example` 或系统设置文档。

### FR-006 数据清理与性能

- MUST 明确日志保留周期和清理策略；本期可先提供手动脚本或后续任务规划，但 PRD/acceptance MUST 标注。
- 日志查询 MUST 使用分页与索引，禁止无条件全表扫描后在内存中过滤。
- SQLite 本地/demo 环境与 MySQL 生产环境都 MUST 可运行。

## 9. UI / UE 约束

- 管理端页面 MUST 继承当前暗色旗舰风 Design System，使用 semantic token 和既有组件。
- 列表页布局 SHOULD 参考用户管理、SKU 管理、接口文档页面的筛选 + 表格 + 分页模式。
- 详情 MUST 使用右侧抽屉承载；内容区按“基础信息 / 请求信息 / 操作者与客户端 / 操作上下文 / 埋点属性 / metadata JSON”分组。
- 页面文案 MUST 避免暴露敏感字段原值；被脱敏字段以 `******`、`已脱敏` 或等价文案展示。
- prototype MUST 包含管理端日志列表页、详情抽屉、对应 context，并以产品 v2 截图作为 UI Golden Reference。

## 10. 安全与合规要求

- MUST 区分管理端、店主展示端、小程序和后端任务的权限边界。
- MUST 遵守最小采集原则：只采集排障、审计和产品分析所需字段。
- MUST 对敏感字段进行脱敏或不采集。
- MUST 禁止提交真实日志文件、真实客户数据、运行时数据库文件。
- 日志访问 MUST 有鉴权；日志详情属于敏感信息，不得对普通店主或匿名用户开放。

## 11. 关联需求与现有能力

| 需求 / 能力 | 关系 |
|---|---|
| REQ-0017-system-settings | 已有审计配置与最近系统设置审计，本需求应复用或扩展其审计策略 |
| audit_logs | 已有统一审计表，本需求需评估扩展或分表 |
| REQ-0014-profile-page | 已有个人资料/登录活动思路，需避免重复日志模型 |
| REQ-0022-admin-api-docs-menu | 接口文档可帮助确认新增日志 API 与 OpenAPI/Orval 生成关系 |

## 12. 状态

```yaml
requirement_id: REQ-0024-product-usage-logging
priority: P1
status: in_sprint
owner: 产品负责人
iteration: sprint-004
openspec_change: add-product-usage-logging
readiness: Ready
next: /req-opsx REQ-0024-product-usage-logging
```
