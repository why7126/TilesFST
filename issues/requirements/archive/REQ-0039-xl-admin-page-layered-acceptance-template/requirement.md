---
requirement_id: REQ-0039-xl-admin-page-layered-acceptance-template
title: XL 管理端页面分层验收模板
terminal: web-admin
version: v1
status: done
owner: product
source: capture.md
priority: P1
parent_requirement:
created_at: 2026-07-16 09:01:50
updated_at: 2026-07-16 09:37:04
---

# REQ-0039 XL 管理端页面分层验收模板

## 1. 需求背景

管理端已经积累了品牌、Banner、SKU、用户、系统设置、接口文档、品牌证书等多个复杂页面。复杂页面往往同时触及数据库、API、上传、OpenAPI/Orval、Web 交互、Docker/Nginx 和横切 UI 约束。若每个页面在 PRD、OpenSpec、实现和验收阶段临时组织检查项，容易出现以下问题：

- API 字段或错误码变化后遗漏 OpenAPI、Orval、接口文档或前端类型同步。
- 上传链路只在后端或前端单侧验证，遗漏 MinIO 前缀、鉴权、失败态、Nginx body size 或 Docker Web 入口。
- 管理端页面只验收主流程，遗漏列表、表单、弹窗、确认操作、toast、分页、权限边界和移动/窄屏回归。
- UI 横切约束分散在历史 REQ、知识库和规则文档中，后续页面难以复用。
- Docker Compose、SQLite/MySQL、测试命令、N/A 判定和验收证据在不同 Change 中口径不一致。

本需求用于沉淀一套面向 XL 管理端页面的分层验收模板。这里的 “XL 管理端页面” 指业务链路较长、字段较多、可能跨 DB/API/上传/Web/Docker 多层的复杂管理端页面，而非某个具体页面名称。

## 2. 目标用户

| 用户 | 诉求 |
|---|---|
| 产品 / 需求负责人 | 在生成 PRD 和验收标准时有统一模板，避免复杂页面遗漏关键验收层。 |
| 后端开发 | 明确 DB、API、上传、错误码、鉴权和测试的必检项及 N/A 条件。 |
| 前端开发 | 明确 Orval、Web 页面状态、管理端组件复用和横切 UI gate 的验收口径。 |
| 测试 / 验收人员 | 按层检查交付结果，并能记录命令、截图、接口响应和 Docker 验证证据。 |
| AI / Codex Agent | 在后续 `/req-complete`、`/req-opsx`、`/opsx-apply` 中复用模板，减少重复探索和遗漏。 |

## 3. 需求目标

- 建立一套可复制的 XL 管理端页面分层验收模板。
- 模板 MUST 覆盖 DB、API、上传、Orval、Web、Docker 和横切 UI gate。
- 模板 MUST 支持 “适用 / 不适用 N/A” 判定，避免为了满足模板而引入无关工作。
- 模板 SHOULD 沉淀到长期治理文档或模板位置，优先考虑 `docs/standards/`；若后续需要命令族自动引用，再通过 OpenSpec Change 更新对应技能或模板。
- 后续复杂管理端页面需求 SHOULD 能在 `acceptance.md`、OpenSpec `acceptance.md`、Change `tasks.md` 或验收报告中引用该模板。

## 4. 范围

### 4.1 本期包含

| 范围 | 说明 |
|---|---|
| 模板结构 | 定义页面分层验收模板的章节、字段、层级和证据记录方式。 |
| DB gate | 覆盖表结构、迁移、SQLite/MySQL 兼容、Pydantic Schema、种子/测试数据和数据库文档同步判定。 |
| API gate | 覆盖请求/响应、统一 envelope、错误码、鉴权、OpenAPI、接口文档和后端测试判定。 |
| 上传 gate | 覆盖后端授权上传、MIME/大小限制、MinIO 单桶前缀、对象 key、失败态、媒体回显和 Nginx/Docker 边界。 |
| Orval gate | 覆盖是否改变 API contract、何时导出 OpenAPI、何时运行 Orval、禁止手写生成类型。 |
| Web gate | 覆盖管理端页面列表、筛选、表格、分页、表单、弹窗、抽屉、权限、loading/empty/error 状态和前端测试。 |
| Docker gate | 覆盖 Docker Compose、本地 `localhost:3000`、Web Nginx、后端环境变量、MinIO 和上传边界验证。 |
| 横切 UI gate | 覆盖 semantic token、Design System 组件、DS modal、fixed toast、无裸 Hex、无 layout shift、移动/窄屏关键视口。 |
| N/A 判定 | 为每层 gate 定义何时必须执行、何时可标记 N/A，以及 N/A 需要说明的理由。 |

### 4.2 本期不包含

| 不包含 | 说明 |
|---|---|
| 实现具体业务页面 | 本需求不新增或改造品牌、SKU、Banner、证书、用户、系统设置等具体页面。 |
| 修改 DB/API/上传链路 | 本需求只定义验收模板，不直接新增表、接口、上传入口、错误码或 MinIO 前缀。 |
| 运行 OpenAPI/Orval | 只有后续具体页面 Change 改变 API contract 时才执行。 |
| 修改 Web 源码 | 本需求不修改 `src/web/` 页面、组件、样式或生成代码。 |
| 修改 Docker Compose | 本需求不修改 Dockerfile、compose、Nginx 或环境变量。 |
| 自动改造技能命令 | 若需要让 `/req-complete` 自动套用模板，应作为后续实现任务明确纳入 Change。 |

## 5. 功能要求

### FR-001 模板基础结构

模板 MUST 以复杂管理端页面为对象，至少包含：

- 页面/Change 基本信息；
- 适用层级矩阵；
- DB gate；
- API gate；
- 上传 gate；
- Orval gate；
- Web gate；
- Docker gate；
- 横切 UI gate；
- 验收证据与 N/A 说明；
- 风险与剩余项记录。

模板 MUST 明确每层 gate 的状态字段，例如：

```yaml
gate_status: required | not_applicable | passed | failed | blocked
evidence: ""
na_reason: ""
owner: ""
```

### FR-002 DB gate

DB gate MUST 支持检查：

- 是否新增或修改 SQLite/MySQL 表结构、索引、唯一约束、默认值或迁移脚本。
- 是否同步 Pydantic Schema、Repository、Service 和数据库文档。
- 是否补充本地 SQLite 与生产 MySQL 差异说明。
- 是否需要种子数据、fixture 或数据迁移回滚策略。
- 是否补充 Repository/Service 单元测试或集成测试。

若页面不涉及数据模型变化，DB gate MAY 标记 N/A，但 MUST 写明“不新增表结构/字段/迁移，仅复用既有模型”等理由。

### FR-003 API gate

API gate MUST 支持检查：

- 新增或修改的接口路径、方法、权限、请求参数、响应结构和错误码。
- 是否使用统一响应 envelope 和项目错误码规范。
- 是否保留管理端鉴权与权限边界，不绕过 `requireAdmin` 或等价守卫。
- FastAPI 路由是否设置 `response_model`、`summary`、`description`、`tags`。
- 是否同步 `docs/03-api-index.md`、`docs/standards/api-governance.md` 或错误码文档。
- 是否补充 API 集成测试和失败场景测试。

若无 API contract 变化，API gate MUST 明确记录无需改 API，且不得因此运行无关 Orval。

### FR-004 上传 gate

上传 gate MUST 支持检查：

- 前端是否通过后端授权 `multipart/form-data` 上传，禁止直连未授权 MinIO。
- 后端是否校验文件大小、MIME type、扩展名和业务归属。
- 对象 key 是否使用项目约定的单桶前缀策略，不信任用户原始文件名。
- 上传成功响应是否满足页面所需回显字段，例如 `object_key`、`url`、证书文件元数据等。
- 上传失败是否映射明确错误码和 UI 错误态，不暴露内部路径或 MinIO 凭据。
- Web 上传控件是否覆盖 `idle -> uploading -> done / failed` 状态机。
- 修改上传大小或 Nginx 配置时，是否补充 Docker Web `localhost:3000` 上传边界验证。

若页面不含上传控件，上传 gate MAY 标记 N/A；若页面含上传控件但复用既有上传 API，MUST 至少验收前端状态、回显和失败态。

### FR-005 Orval gate

Orval gate MUST 支持检查：

- 是否新增或修改 API contract。
- 若有 contract 变化，MUST 导出 OpenAPI 并运行 `./scripts/generate-openapi-client.sh` 或项目等价命令。
- 前端是否使用 Orval 生成类型和客户端，禁止手写重复接口类型。
- 是否复核 `src/web/src/generated/` 或共享 API 生成物只由生成命令更新。
- 若无 contract 变化，MUST 在验收证据中说明 “Orval N/A” 的理由。

### FR-006 Web gate

Web gate MUST 支持检查管理端页面的主要交互：

- 页面路由、权限、导航入口和无权限行为。
- 列表页筛选、表格、分页、排序、空状态、加载状态和错误状态。
- 新增/编辑/详情/删除/启停/上下架/重置等表单与确认操作。
- 弹窗、抽屉、大表单和底部操作区在桌面与关键窄屏视口下可访问。
- API 成功、业务失败、校验失败、网络失败等反馈展示方式。
- 前端测试、浏览器 smoke 或 Playwright 截图证据。

Web gate SHOULD 要求复杂页面至少覆盖 `1440x1024` 桌面视口和一个移动/窄屏视口；是否扩大到 `375x812`、`390x844`、`768x1024` 由页面复杂度和变更风险决定。

### FR-007 Docker gate

Docker gate MUST 支持检查：

- 是否影响 `docker-compose.yml`、`docker-compose.prod*.yml`、Dockerfile、Nginx 或环境变量。
- 是否需要通过 Docker Compose 验证 Web、Backend、MinIO、数据库之间的实际联通。
- 上传、代理、Swagger、媒体读取等仅在容器环境暴露的问题是否有验证项。
- 若修改 Web Nginx 或上传大小限制，MUST 重建 Web 镜像并记录验证结果。

若 Change 只改文档或纯前端静态 UI 且不影响代理/上传/容器配置，Docker gate MAY 标记 N/A，并记录原因。

### FR-008 横切 UI gate

横切 UI gate MUST 支持检查：

- UI 使用 Design System semantic token，TSX/CSS 不新增裸 Hex 或任意设计色 `rgba(...)`。
- 管理端工作型页面保持克制密度，不引入营销式 hero 或无关说明文案。
- 状态/危险操作使用 DS confirm modal，不使用原生 `window.confirm` / `window.alert`。
- 成功/失败反馈使用 fixed toast 或等价固定反馈区域，不用文档流 notice 推挤布局。
- 列表页分页、指标卡、表单保存 CTA、宽弹窗、上传控件等横切模式遵循既有最佳实践。
- 页面在关键视口下无明显控件重叠、不可控横向溢出、底部按钮不可达或弹窗不可关闭。

模板 SHOULD 允许引用知识库最佳实践或历史 REQ 的 `AC-XCUT-*`，但不得把历史页面的具体业务 AC 原样套到无关页面。

### FR-009 验收证据与 N/A 记录

模板 MUST 要求每层 gate 记录验收证据：

- 相关文件或文档路径；
- 执行命令及结果摘要；
- 截图、接口响应、测试报告或 Docker 验证摘要；
- N/A 理由；
- 剩余风险和后续拆分项。

验收证据 SHOULD 保持摘要化，不复制大段测试日志、完整 OpenAPI/Orval 生成物或敏感环境变量。

## 6. UI / UE 约束

本需求不直接交付可见管理端页面，但模板本身 MUST 体现 Web 管理端 UI/UE 约束：

- 管理端页面优先复用 Design System、`shared/ui`、`shared/business` 与既有页面模板。
- 复杂页面验收应关注可扫描性、工作效率和布局稳定性，而非营销化视觉表达。
- UI gate 应强制 semantic token、DS modal、fixed toast、响应式稳定性和上传控件状态机。
- 若后续生成模板文档，Markdown 应使用表格和短检查项，便于复制到 `acceptance.md` 或验收报告。

## 7. 依赖与实施顺序

| 依赖 | 说明 |
|---|---|
| `rules/requirement-management.md` | REQ 文档生命周期和评审门禁。 |
| `rules/api.md` / `docs/standards/api-governance.md` | API、OpenAPI、Orval 和错误码治理。 |
| `rules/database.md` / `docs/04-database-design.md` | DB 结构、SQLite/MySQL 与文档同步约束。 |
| `rules/security.md` / `docs/standards/file-upload.md` | 上传、MinIO、安全和 Nginx body 限制。 |
| `rules/ui-design.md` / `src/web/README.md` | Web 管理端 Design System 和 semantic token 约束。 |
| `docs/standards/testing-governance.md` | 测试目录、测试层级和运行命令。 |
| REQ-0027 | 横切 AC、移动/窄屏验收和管理端 UI gate 的参考来源。 |

建议实施顺序：

1. 确认模板最终沉淀位置，优先 `docs/standards/`。
2. 设计模板的层级矩阵、gate 字段和 N/A 判定。
3. 提炼 DB/API/上传/Orval/Web/Docker/UI gate 的检查项。
4. 在后续 `/req-complete` 中生成 user stories、business flow 和 acceptance。
5. 评审通过后通过 OpenSpec Change 实现模板文档或命令族引用能力。

**建议 OpenSpec change 命名**：`add-xl-admin-page-acceptance-template`。

## 8. 关联需求

| 需求 / 模块 | 关系 |
|---|---|
| REQ-0000-build-design-system | 横切 UI gate、semantic token 和 DS 组件复用约束来源。 |
| REQ-0027-mobile-page-adaptation | 管理端移动/窄屏验收和 `AC-XCUT-*` 写法参考。 |
| REQ-0031-api-validation-envelope-governance | API envelope、校验错误和管理端表单错误映射参考。 |
| REQ-0028-admin-list-page-contract | 管理端列表页模板、分页和基础组件契约参考。 |
| 上传 / MinIO 标准 | 上传 gate 的安全、对象 key、失败态和 Docker Nginx 边界来源。 |

## 9. 状态

```yaml
requirement_id: REQ-0039-xl-admin-page-layered-acceptance-template
priority: P1
status: done
iteration: null
owner: product
parent_requirement: null
openspec_change: null  # 建议 add-xl-admin-page-acceptance-template
target_clients:
  web_admin: 本期模板服务对象
  web_catalog: 不涉及
  wechat_miniapp: 不涉及
api_change: false
database_change: false
upload_change: false
orval_required: false
docker_compose_required: false
```
