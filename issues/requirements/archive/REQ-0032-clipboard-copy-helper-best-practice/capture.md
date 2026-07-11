---
req_id: REQ-0032-clipboard-copy-helper-best-practice
status: archived
created_at: 2026-07-11 13:20:12
updated_at: 2026-07-11 20:10:50
recorded_by: product
source: 用户输入
priority_hint: P1
parent_requirement: REQ-0000-build-design-system
---

# Clipboard 复制交互沉淀共享 helper 或 best-practice

沉淀 Clipboard 复制交互的共享 helper 或最佳实践，统一前端复制能力在成功、失败、Clipboard API 不存在、手动复制兜底等场景下的处理方式。

# 原始描述

为 Clipboard 复制交互沉淀共享 helper 或 best-practice，覆盖成功、失败、API 不存在、手动复制。

# 待澄清

- [ ] 需要落为可复用代码 helper，还是先沉淀为 Design System / 前端工程最佳实践文档。
- [ ] 覆盖端范围：仅 Web 管理端，还是包含店主 Web 展示端与微信小程序的复制交互约束。
- [ ] 成功、失败、API 不存在、手动复制的用户提示文案与视觉反馈是否需要统一接入现有 toast / dialog 组件。
- [ ] 是否需要为浏览器权限限制、非安全上下文、移动端长按复制等场景提供明确验收标准。

# 探索结论

（/req-explore 后人工确认写入）
