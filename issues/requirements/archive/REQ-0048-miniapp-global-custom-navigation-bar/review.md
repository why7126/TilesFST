---
review_id: REV-REQ-0048-001
requirement_id: REQ-0048-miniapp-global-custom-navigation-bar
date: 2026-07-19
participants: []
result: approved
created_at: 2026-07-19 11:16:21
updated_at: 2026-07-19 11:16:21
---

# REQ-0048 小程序全局自定义导航栏评审

## 评审结论

评审通过。REQ-0048 已明确小程序首页与非首页自定义导航栏的行为边界：首页保留当前品牌 `brand-header`，非首页复用同一导航模块并新增左侧返回按钮；右侧继续避让微信原生分享 / 关闭胶囊；页面内容需避让 fixed header。

该需求与 `REQ-0042-custom-navigation-bar` 关系清晰，为首页品牌自定义导航栏的全局化延展，不是重复需求。PRD、用户故事、业务流程、验收标准和 miniapp 原型策略已补齐，可进入 `/req-opsx`。

## 评审检查清单

- [x] 范围清晰，Out of Scope 明确。
- [x] 验收标准可测试。
- [x] 优先级与依赖合理。
- [x] UI 类：原型或实现策略已决。
- [x] 无与现有 REQ 重复未说明。

## 条件通过项

- [ ] 后续 `/req-opsx` 的 design.md 需引用 `trace.md` 中的 `knowledge_base_refs`。
- [ ] 后续实现前需确认非首页无页面栈时的返回兜底策略，建议返回首页。
- [ ] 后续验收需在微信开发者工具或真机中验证胶囊避让、状态栏避让和 fixed header 内容不遮挡。

## 后续动作

1. `/req-opsx REQ-0048-miniapp-global-custom-navigation-bar`
2. 通过后纳入 Sprint，再执行开发实现。
