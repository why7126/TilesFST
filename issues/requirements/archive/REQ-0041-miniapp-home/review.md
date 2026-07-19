---
review_id: REV-REQ-0041-001
requirement_id: REQ-0041-miniapp-home
date: 2026-07-16 09:40:45
participants:
  - product
result: approved
created_at: 2026-07-16 09:40:45
updated_at: 2026-07-16 09:40:45
---

# REQ-0041 微信小程序首页评审

## 评审结论

评审通过。REQ-0041 的范围已经明确收敛为原生微信小程序首页及首期必要闭环，包含首页、门店信息页、搜索页、商品详情页、分享、咨询和热销行为统计；同时明确排除收藏、预约表单、到店询价规则、快捷入口后台配置、服务入口后台配置、复杂用户画像和收藏驱动热销算法。

本需求具备进入 `/req-opsx` 的条件。后续 OpenSpec Change 应重点细化小程序页面、聚合接口、行为统计、门店咨询来源、数据库/接口/Orval 同步和测试验收。

## 评审清单

- [x] 范围清晰，In Scope / Out of Scope 明确。
- [x] 验收标准可测试，覆盖功能、范围控制、UI、状态降级、API/数据/安全、测试验证。
- [x] 优先级为 P1，符合小程序首页首期闭环价值。
- [x] UI 类需求已有 `prototype/miniapp/prototype.html`、`prototype/miniapp/prototype.png` 和原型上下文。
- [x] 与 `REQ-0021-sku-web-miniapp-preview` 的关系已说明：同属小程序展示视图相关，但不是父子 refinement。
- [x] 管理端 knowledge-base 横切标签 N/A 已说明，且已参考 sprint-007 分层验收经验。

## 条件通过项

- [ ] 实现阶段若新增或调整 `GET /api/miniapp/home`、分享/咨询事件、热销统计接口，MUST 同步 OpenAPI、Orval、API 文档和测试。
- [ ] 若行为统计需要新增表、字段或聚合模型，MUST 同步数据库文档、迁移和测试。
- [ ] 小程序端 MUST 仅访问后端授权接口和后端返回的安全图片 URL，不得直连未授权对象存储。
- [ ] 收藏、预约表单、到店询价规则、快捷入口后台配置、服务入口后台配置不得混入本 Change。
- [ ] 后续 `/req-opsx` 的 design / tasks MUST 引用本需求的原型、acceptance 和 trace 中的范围控制。

## 后续动作

1. `/req-opsx REQ-0041`
2. 通过 Sprint 规划后再进入实现阶段。
