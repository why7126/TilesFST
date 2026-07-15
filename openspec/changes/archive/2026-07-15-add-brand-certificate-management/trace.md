---
change_id: add-brand-certificate-management
type: add
status: applied
created_at: 2026-07-14 23:17:02
updated_at: 2026-07-15 09:35:08
source_requirement: REQ-0038-brand-certificate-management
source_path: issues/requirements/archive/REQ-0038-brand-certificate-management/
iteration: sprint-007
capabilities:
  - brand-certificate-management
related_specs:
  - brand-management
  - object-storage
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-list-page-consistency.md
  - docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md
  - docs/knowledge-base/best-practices/admin-media-upload-chain.md
---

# Change Trace

## 来源

- REQ：`REQ-0038-brand-certificate-management`
- 需求目录：`issues/requirements/archive/REQ-0038-brand-certificate-management/`
- 评审：`review.md` result `approved`

## Requirement Readiness Report

| 项 | 结果 |
|---|---|
| requirement.md | Ready |
| user-stories.md | Ready |
| business-flow.md | Ready |
| acceptance.md | Ready |
| trace.md | Ready |
| prototype/web | Ready |
| knowledge-base 横切 AC | Pass |

Readiness: Ready。

## Impact

```yaml
impact:
  backend: true
  web: true
  miniapp: false
  admin: true
  database: true
  storage: true
  api: true
capabilities:
  new:
    - brand-certificate-management
  modified: []
```

## Conflict Report

| 来源 | 冲突 | 处理 |
|---|---|---|
| HTML / PNG prototype | 保留早期品牌摘要栏 | 正式实现以 acceptance.md / requirement.md 为准，不展示品牌摘要栏 |
| HTML prototype | 包含裸 Hex 和压缩 CSS | 仅作视觉参考，正式代码使用 semantic token 和 shared UI |
| 原型视觉 | 弹窗、表格、上传成功态有参考价值 | 保留为视觉密度与交互态参考 |

## Implementation Evidence

| 层级 | 证据 |
|---|---|
| DB | `src/backend/app/db/schema.sql`、`schema.mysql.sql`、`migrations.py` 新增 `brand_certificates`、索引与 SQLite 升级路径 |
| API | `src/backend/app/api/v1/admin_brand_certificates.py` 新增列表、创建、详情、更新、show、hide、delete；`uploads.py` 新增 `/admin/uploads/brand-certificates` |
| Service | `brand_certificate_admin_service.py` 校验品牌存在、同品牌名称唯一、日期、文件元数据、有效状态、审计写入；`brand_admin_service.py` 增加品牌删除前证书约束 |
| Web | `BrandCertificateManagementPage.tsx` 新增一级页面、URL Query、筛选、分页、弹窗、上传状态机、预览、confirm；品牌列表页增加证书快捷入口 |
| UI 回归修复 | 列表页筛选条件调整为桌面端单行展示；弹窗上传“移除 / 重新上传”按钮水平对齐；字段级校验提示改为展示在对应字段或上传对象下方 |
| Docs / API Client | `docs/03-api-index.md`、`docs/04-database-design.md`、`docs/standards/error-codes.md`、`docs/standards/file-upload.md`、`rules/ui-design.md`；已运行 `./scripts/generate-openapi-client.sh` |
| Tests | `tests/integration/api/test_admin_brand_certificates.py`、`BrandCertificateManagementPage.test.tsx` 覆盖 API、上传、列表、弹窗、PDF 回显、confirm、日期字段级校验提示位置 |

## PNG / Prototype Checklist

- [x] 实现后记录 `/admin/brand-certificates` 与原型的并排验收结论：采用一级管理页，不实现 HTML/PNG 早期品牌摘要栏。
- [x] 确认页面无品牌摘要栏：正式页面只展示标题、指标、筛选、列表、分页与弹窗。
- [x] 确认弹窗 Computed width 为 760px：CSS 源 `.certificate-modal-card { width: 760px; }`，TSX 仅挂载 `certificate-modal-card`，未双挂 `modal-card`；Playwright 浏览器启动环境不可用，已以源码、CSS、Vitest DOM gate 替代记录。
- [x] 确认证书文件上传成功态、失败态和 PDF 文件卡片可用：Vitest 覆盖 PDF 上传成功回显，后端 pytest 覆盖非法类型错误。
- [x] 确认 Docker Web `:3000` 上传边界验收结果：小 PDF 经 `http://localhost:3000/api/v1/admin/uploads/brand-certificates` 返回 200；21MB PDF 返回 `400 / 50005`，非 Nginx 413。

## Knowledge-base Cross-cutting AC

| AC | 结果 | 证据 |
|---|---|---|
| AC-XCUT-001 | pass | `AdminListPage` 分页 DOM 使用 `.page-summary` + `.page-right`，Vitest 覆盖 |
| AC-XCUT-002 | pass | 指标卡复用 `MetricCard`，DOM 为 `.metric-label` / `.metric-value` / `.metric-desc` |
| AC-XCUT-003 | pass | 反馈复用 `AdminToast` fixed toast，无文档流 notice |
| AC-XCUT-004 | pass | 显示/隐藏/删除使用 React confirm dialog；未使用 `window.confirm` |
| AC-XCUT-005 | pass | 证书表单弹窗只挂 `certificate-modal-card`，未与 `modal-card` 双挂 |
| AC-XCUT-006 | warn-pass | CSS 宽度 760px；浏览器 computed 验收因本机 Playwright/Chrome 不可用未完成真实截图 |
| AC-XCUT-007 | pass | `.certificate-modal-card` flex column，`.certificate-modal-body` overflow auto，头尾固定 |
| AC-XCUT-008 | pass | 上传控件覆盖 `idle → uploading → done / failed` 状态机 |
| AC-XCUT-009 | pass | 上传成功后同弹窗即时展示图片/PDF 文件卡片 |
| AC-XCUT-010 | pass | Docker Web `:3000` 小文件 200，超限文件 `400 / 50005` |
| AC-XCUT-011 | pass | 字段级校验提示展示在对应字段、字段组或上传对象下方；`rules/ui-design.md` 已补充规范，Vitest 覆盖日期校验提示位置 |

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-14 23:17:02 | /req-opsx | 由 REQ-0038 创建 OpenSpec Change 初稿。 |
| 2026-07-14 23:31:34 | /sprint-propose sprint-007 | 纳入 sprint-007 正式范围。 |
| 2026-07-15 09:13:11 | /opsx-apply | 完成品牌证书 DB/API/上传/Web/测试/文档实现与 Docker Web 上传边界验收。 |
| 2026-07-15 09:35:08 | /opsx-archive precheck | 归档前补充列表筛选单行、上传按钮对齐、字段级校验提示位置与 UI 规范更新证据。 |
