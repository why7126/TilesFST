---
requirement_id: REQ-0090-media-five-point-acceptance-template
status: pending_review
created_at: 2026-08-01 09:50:59
updated_at: 2026-08-01 09:50:59
---

# Prototype Context

本需求不新增 Web 管理端、店主端或小程序页面，因此不需要 HTML/PNG 交互原型。

后续若 `/req-opsx` 决定将媒体五联验收模板做成可视化工具或管理端检查页，原型应遵守以下策略：

- 采用紧凑表格或检查清单展示五联维度，不做营销式页面。
- 每个媒体样例固定展示 key、object、URL、thumbnail benefit、miniapp render 五列状态。
- 状态使用 `pass`、`fail`、`n/a`、`blocked`，并提供证据或失败原因字段。
- 上传相关控件必须遵守 `docs/knowledge-base/best-practices/admin-media-upload-chain.md` 的状态机与即时回显要求。
- Web UI 必须使用 Design System semantic token，不得直接写裸 Hex。
