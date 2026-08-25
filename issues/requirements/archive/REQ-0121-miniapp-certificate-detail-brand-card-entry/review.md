---
review_id: REV-REQ-0121-001
requirement_id: REQ-0121-miniapp-certificate-detail-brand-card-entry
date: 2026-08-24
reviewed_at: 2026-08-24 15:42:12
participants: []
result: approved
created_at: 2026-08-24 15:42:12
updated_at: 2026-08-24 15:42:12
---

# 需求评审

## 评审结论

评审通过。

本需求范围清晰，聚焦小程序证书详情页所属品牌入口复用 `brand-card`、补齐 `brand_logo_thumbnail_url`、统一 `brand_card_click` 埋点与品牌 Logo 缩略图消费策略。Out of Scope 已排除证书详情页整体重构、管理端维护能力、数据库新增字段、图片派生能力和 Web 端组件建设，可进入 Sprint 规划。

## 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 范围清晰，Out of Scope 明确 | 通过 | 已限定为证书详情页品牌入口复用和字段/埋点契约。 |
| 验收标准可测试 | 通过 | AC 覆盖组件复用、字段、跳转、埋点、UI、数据安全和媒体四联证据。 |
| 优先级与依赖合理 | 通过 | P1；依赖 `REQ-0115` 图片多规格、`REQ-0054` brand-card 与证书详情页既有能力。 |
| UI 类原型或实现策略已决 | 通过 | 已提供 `prototype/miniapp/prototype-context.md`，采用局部复用策略，不新建完整 HTML 原型。 |
| 无与现有 REQ 重复未说明 | 通过 | 与 `REQ-0054`、`REQ-0080`、`REQ-0118` 的关系已说明，本需求是证书详情页落地与收敛。 |

## 条件通过项

- [ ] 后续 `/req-opsx` 设计阶段必须明确证书详情 `brand` 数据的字段来源：若涉及后端响应字段变更，需同步 Schema、OpenAPI/Orval 或小程序服务层类型及后端测试。
- [ ] 后续实现验收必须补齐小程序媒体四联证据，证明 `brand_logo_thumbnail_url` 被实际消费且未 fallback 到原图。
- [ ] 后续实现验收必须回归所有当前 `brand-card` 调用方，确认 `brand_card_click` 事件名统一且既有页面未回退。

## 后续建议

评审通过后推荐先执行 `/sprint-propose` 纳入迭代，再执行 `/req-opsx` 创建 OpenSpec Change。
