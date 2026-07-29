---
change_id: update-certificate-multiple-images-main-image
change_type: update
status: applied
created_at: 2026-07-28 22:48:48
updated_at: 2026-07-29 00:10:51
source_requirement: REQ-0078-certificate-multiple-images-main-image
source_requirement_path: issues/requirements/archive/REQ-0078-certificate-multiple-images-main-image/
iteration: sprint-013
capabilities:
  - brand-certificate-management
impact:
  backend: true
  web: true
  admin: true
  miniapp: true
  database: true
  storage: true
  api: true
---

# Change Trace

## 来源

| 来源 | 路径 |
|---|---|
| REQ | `issues/requirements/archive/REQ-0078-certificate-multiple-images-main-image/` |
| Requirement | `issues/requirements/archive/REQ-0078-certificate-multiple-images-main-image/requirement.md` |
| Acceptance | `issues/requirements/archive/REQ-0078-certificate-multiple-images-main-image/acceptance.md` |
| Prototype | `issues/requirements/archive/REQ-0078-certificate-multiple-images-main-image/prototype/web/certificate-multiple-images-main-image.html` |

## Requirement Readiness Report

| 项 | 结论 |
|---|---|
| REQ status | approved |
| Readiness | Ready |
| Knowledge-base gate | Pass |
| Cross-cutting tags | admin-list, admin-modal, media-upload |
| Change type | update |

## Conflict Resolution

| 冲突 | 处理 |
|---|---|
| prototype HTML 示例宽度 880px vs existing spec 弹窗宽度 760px | 最终实现保持 existing spec 的 760px；HTML 只作为多图状态和布局语义参考 |
| 多图与 PDF/文档并存策略未完全确定 | design.md 记录 Open Question；apply 前必须确认互斥或并存策略 |

## PNG Checklist

- [ ] 如需要 Golden Reference，基于 `prototype/web/certificate-multiple-images-main-image.html` 导出 PNG。
- [ ] PNG 导出后确认弹窗宽度冲突已在设计中消化，不以 HTML 880px 覆盖 existing spec。
- [ ] 1440x1024 列表分页、指标卡、fixed toast、弹窗滚动和上传状态均覆盖。

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-29 00:10:51 | docs-sync | 记录 apply 后 follow-up：小程序公开证书列表/品牌证书 Tab 返回主图 URL、证书卡片高度调整、tabbar 激活态修复；管理端证书列表移除预览按钮，证书图片上传提示改为 SKU help 样式。 |
| 2026-07-28 23:18:40 | /opsx-apply | Change apply 完成；后端、Web 管理端、DB/API/Orval、上传边界和核心测试已落地。 |
| 2026-07-28 22:59:15 | /sprint-propose | 纳入 `sprint-013` 正式范围，后续允许按 Sprint 编排进入 `/opsx-apply`。 |
| 2026-07-28 22:48:48 | /req-opsx | 从 `REQ-0078` 创建 OpenSpec Change，状态 proposed。 |
