## Context

REQ-0038 已通过评审，需求包位于 `issues/requirements/archive/REQ-0038-brand-certificate-management/`。它要求新增独立一级管理端页面 `/admin/brand-certificates`，并通过必填 `brand_id` 建立品牌与证书的一对多关系。现有 `brand-management` spec 已覆盖品牌主数据、品牌 Logo 上传和品牌条件删除；`object-storage` spec 已覆盖 MinIO 单桶、MIME/大小校验、受控读取与对象 Key 前缀策略。

本 Change 只提出 OpenSpec 工件，不实现源码。后续实现必须先纳入 Sprint，然后通过 `/opsx-apply` 或 `/sprint-apply` 执行。

关联需求与知识库：

- `issues/requirements/archive/REQ-0038-brand-certificate-management/requirement.md`
- `issues/requirements/archive/REQ-0038-brand-certificate-management/acceptance.md`
- `issues/requirements/archive/REQ-0038-brand-certificate-management/prototype/web/prototype-context.md`
- `docs/knowledge-base/best-practices/admin-list-page-consistency.md`
- `docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md`
- `docs/knowledge-base/best-practices/admin-media-upload-chain.md`

## Goals / Non-Goals

**Goals:**

- 新增品牌证书数据模型、API、权限、审计和服务端有效状态计算。
- 新增管理端证书列表页、筛选、分页、指标、弹窗 CRUD、预览、显示/隐藏和删除。
- 证书文件走后端授权上传与 MinIO 单桶策略，支持图片和 PDF。
- 同步 OpenAPI、Orval、docs、DB 文档和自动化测试。
- 把 REQ-0038 的 knowledge-base 横切 AC 纳入实现验收。

**Non-Goals:**

- 不实现店主端品牌详情证书展示页面。
- 不实现 OCR、证书审批流、电子签章、真伪校验、批量操作、导出、多语言证书名或 SKU 证书绑定。
- 不创建额外对象存储 Bucket。
- 不在 propose 阶段修改 `src/` 或测试代码。

## Decisions

### D1. UI 策略采用 tailwind-ds，而不是完整 CSS Port

管理端证书页应优先复用 `AdminListPage`、共享分页、Badge、Confirm、Toast、Upload 等 DS / shared 组件，并使用 semantic token。原型 HTML/PNG 只作为视觉密度、表格、弹窗和上传态参考，不直接 port 裸 Hex、压缩 CSS 或旧品牌摘要栏结构。

备选方案：完整 CSS Port 原型 HTML。该方案会带入裸色值、早期品牌摘要栏和压缩 CSS，容易绕过 `rules/ui-design.md` 的 semantic token 与组件复用要求，因此不采用。

### D2. 证书作为独立主数据表，不嵌入 brands JSON 字段

新增 `brand_certificates` 表或等价 schema，以 `brand_id` 外键关联品牌。字段覆盖证书名称、类型、编号、发证机构、文件元数据、有效期、展示状态、排序、备注、软删除和审计时间。

备选方案：在 `brands` 表中增加 JSON 附件字段。该方案难以支持跨品牌筛选、到期统计、排序、软删除、唯一性和分页治理，因此不采用。

### D3. 有效状态由服务端计算，前端只展示

服务端根据 `is_permanent`、`effective_date`、`expiry_date` 和当前日期返回 `validity_status`。前端不得作为唯一计算源，只负责展示、筛选参数和空/错/加载态。

备选方案：前端根据日期自行计算。该方案会造成时区、筛选和 API 结果不一致，且不利于后续店主端复用，因此不采用。

### D4. 文件上传复用对象存储适配层与后端授权链路

证书文件支持 JPG、PNG、WebP、PDF，单文件最大 20MB；上传必须经后端鉴权、MIME/大小校验、对象 Key 生成和 MinIO 写入。业务保存前必须得到 `file_url`、`file_key`、文件名、MIME 和大小。

备选方案：前端直传未授权对象存储或写入本地 `UPLOAD_DIR`。该方案违反安全与对象存储规则，因此不采用。

### D5. 品牌删除前增加证书约束

若品牌存在未删除证书，删除品牌时必须阻止或要求先迁移/删除证书。品牌停用不自动删除证书；店主端未来展示时不展示停用品牌及其证书。

备选方案：删除品牌时级联软删除证书。该方案容易造成证书审计与文件引用丢失，不符合可追溯目标，因此不采用。

## Conflict Resolution

REQ-0038 的 `prototype/web/brand-certificate-management.html` 与 PNG 保留了早期品牌摘要栏；`acceptance.md` 和 `prototype-context.md` 已明确品牌证书是一级页，不展示品牌摘要栏或品牌详情面包屑。实现优先级按 `acceptance.md > requirement.md > prototype-context.md > HTML > PNG > rules/ui-design.md` 执行。

冲突处理：

- 页面结构以 `acceptance.md` AC-001、AC-003、AC-004、AC-010、AC-029 为准。
- HTML/PNG 仅参考暗色工业风、密度、表格、弹窗、上传成功态和响应式节奏。
- 正式代码不得复制 HTML 原型中的裸 Hex 或压缩 CSS。
- 若实现时发现 HTML/PNG 与 AC 冲突，必须在 Change `trace.md` 的 PNG/Prototype checklist 记录采用 AC 的原因。

## Risks / Trade-offs

- API/DB/Web/Upload 同时变化，改动面较大 -> 按任务分层实现，先 DB/API，再 Orval，再 Web。
- PDF 上传与预览可能与现有图片上传组件不同 -> 上传组件需要支持文件卡片态和 MIME 分支，PDF 预览失败需有 fallback。
- Nginx 413 可能早于后端业务校验 -> Docker Web `:3000` 必须执行边界文件验收。
- 同品牌名称唯一性与软删除组合在 SQLite/MySQL 表达不同 -> migration 与 repository 测试必须覆盖软删除后同名可重建或明确拒绝策略。
- 权限点若当前系统尚未细粒度实现 -> 首版至少保留权限声明、UI 隐藏/只读策略和后端鉴权扩展点。

## Migration Plan

1. 新增数据库 schema / migration，创建 `brand_certificates` 表并补充 DB 文档。
2. 新增后端 schemas、repository、service、router、权限点、错误码和审计记录。
3. 更新 OpenAPI 并生成 Orval 客户端。
4. 新增 Web 管理端页面、导航入口、品牌列表快捷入口、弹窗和上传/预览交互。
5. 补充后端集成测试、前端组件/页面测试、上传链路测试和 OpenSpec 校验。
6. 通过 Docker Compose 验证 Web `:3000` 上传边界和媒体回显。

Rollback：若发布后需要回滚 Web 入口，应隐藏导航与品牌快捷入口；后端保留表结构和 API 不做破坏性删除，后续通过数据迁移或版本脚本处理。

## Open Questions

- 证书文件对象 Key 是否需要专用语义前缀（如 `files/default/brand-certificates/`），还是复用现有 `original/` 前缀并以资源类型区分？
- 当前权限系统是否已有细粒度 permission registry；若没有，首版权限点如何映射到 `admin` / `employee`？
- 品牌存在证书时删除品牌是强制阻止，还是允许迁移证书后删除？本 Change 默认要求阻止或先迁移/删除。
