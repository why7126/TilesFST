---
review_id: REV-REQ-0078-001
requirement_id: REQ-0078-certificate-multiple-images-main-image
date: 2026-07-28
reviewed_at: 2026-07-28 22:38:51
participants:
  - product
result: approved
created_at: 2026-07-28 22:38:51
updated_at: 2026-07-28 22:38:51
---

# REQ-0078 需求评审

## 评审结论

通过。`REQ-0078` 定位为 `REQ-0038-brand-certificate-management` 的 refinement，范围聚焦于管理端品牌证书多张图片上传、主图设置、删除兜底、列表主图缩略图与上传安全回归，不直接扩大到店主 Web 或微信小程序证书详情多图展示。

需求文档已补齐 `requirement.md`、`user-stories.md`、`business-flow.md`、`acceptance.md`、`trace.md` 与 `prototype/web`，并将 `admin-list`、`admin-modal`、`media-upload` 三类 knowledge-base 横切验收转化为 AC-XCUT。验收标准可测试，后续允许进入 `/req-opsx` 和 Sprint 规划。

## 评审检查清单

- [x] 范围清晰，Out of Scope 明确。
- [x] 验收标准可测试，覆盖功能、UI、数据/API、测试和横切 AC。
- [x] 优先级 P1 合理，父需求 `REQ-0038-brand-certificate-management` 已完成。
- [x] UI 类原型与实现策略已决，`prototype/web/certificate-multiple-images-main-image.html` 可作为布局和状态验收参考。
- [x] 与现有 REQ 不重复；本需求明确为证书管理多图与主图规则增强，未重做证书管理页或公开证书列表页。

## 条件通过项

- [ ] `/req-opsx` 设计阶段必须确认 PDF/文档类证书与多张图片的互斥或并存策略。
- [ ] `/req-opsx` 设计阶段必须确认单证书图片数量上限；当前 PRD 默认 9 张，前后端校验需保持一致。
- [ ] 若新增证书图片关联表或 API contract 变化，必须同步 SQLite/MySQL 文档、Pydantic Schema、OpenAPI、Orval、API 文档和测试。
- [ ] 实现阶段必须保持上传走后端鉴权与对象存储适配层，不得前端直连未授权对象存储。
- [ ] 纳入 Sprint 前需确保 sprint 级横切预防清单覆盖 `admin-list`、`admin-modal`、`media-upload`。

## 后续动作

1. `/req-opsx REQ-0078-certificate-multiple-images-main-image`
2. `/sprint-propose` 纳入迭代正式范围
