---
requirement_id: REQ-0123-upload-stage-trace-spans
title: 上传链路阶段级耗时写入 trace spans - 原型策略
status: pending_review
owner: product
source: requirement.md
created_at: 2026-08-25 18:43:20
updated_at: 2026-08-25 18:43:20
---

# 原型策略

## 1. UI 判定

本需求命中 `media-upload` 横切标签，但当前 PRD 默认不新增可见 UI，核心交付是后端上传链路的 task trace spans。管理端头像上传与通用图片上传的既有界面不应因本需求产生视觉或交互退化。

## 2. 本期原型策略

- 不生成独立 HTML 原型。
- 不生成 PNG Golden Reference。
- 后续 OpenSpec 若决定在管理端展示阶段耗时，再补充 UI Contract 与原型，展示形态应为紧凑阶段列表或折叠明细。
- 若无 UI 展示，验收应以 task trace spans、自动化测试和上传回归证据为主。

## 3. 后续 UI 约束

若后续需要管理端展示上传阶段耗时：

- 使用紧凑列表或表格，列出阶段、耗时、状态和脱敏错误摘要。
- 不展示完整对象 key、内部路径、异常堆栈、密钥或基础设施敏感配置。
- 使用 Design System semantic token，不使用裸 Hex。
- 上传状态机仍需满足 `idle -> uploading -> done/failed`。
- 成功反馈或错误反馈不得造成布局跳动。

