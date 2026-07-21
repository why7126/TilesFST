---
review_id: REV-REQ-0061-001
requirement_id: REQ-0061-miniapp-share-add-guide
date: 2026-07-20
created_at: 2026-07-20 00:09:20
updated_at: 2026-07-20 00:09:20
participants:
  - product
result: approved
reviewed_by: product
---

# REQ-0061 小程序添加到我的小程序引导语评审

## 评审结论

评审通过。该需求围绕微信小程序右上角系统入口附近的“添加到我的小程序”引导语展开，范围清晰、验收标准可测试，且已明确不修改微信原生菜单、不手绘系统胶囊、不新增 Web / 管理端 / 后端配置能力。

本需求可进入 `/req-opsx` 阶段，后续 OpenSpec Change 需继续引用 `docs/knowledge-base/best-practices/miniapp-custom-navigation.md`，并在实现验收中覆盖状态栏、胶囊 reserve、页面 offset、DevTools / 真机 evidence。

## 评审检查清单

- [x] 范围清晰，Out of Scope 明确。
- [x] 验收标准可测试，覆盖展示、关闭、频率、胶囊避让、API / DB N/A 和测试 evidence。
- [x] 优先级 P1 合理，符合小程序留存与下次找回诉求。
- [x] UI 类需求已提供 `prototype/miniapp/context.md` 与 `prototype/miniapp/prototype.html`。
- [x] 与现有 `REQ-0041`、`REQ-0048`、`REQ-0053` 的关系已说明，不与既有需求重复。

## 条件通过项

- [x] 关闭后再次展示策略在需求中保留待确认项；评审接受“至少当前会话内不再展示”为后续实现默认底线。
- [x] 首期展示场景以首页进入为主；若 OpenSpec 阶段扩展为全局引导，必须补充非首页不遮挡验收。
- [x] 默认不新增 API / DB / Orval；若后续引入服务端配置或埋点，必须另行同步 API、数据库文档和测试。

## 后续动作

1. `/req-opsx REQ-0061-miniapp-share-add-guide`
2. `/sprint-propose` 纳入迭代后再实现。
3. 实现阶段按小程序自定义导航最佳实践补齐设备 evidence。
