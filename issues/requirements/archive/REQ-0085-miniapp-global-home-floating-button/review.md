---
review_id: REV-REQ-0085-001
requirement_id: REQ-0085-miniapp-global-home-floating-button
date: 2026-07-30
participants:
  - product
result: approved
created_at: 2026-07-30 23:12:47
updated_at: 2026-07-30 23:12:47
---

# 需求评审

## 评审结论

REQ-0085 小程序非首页页面新增返回首页全局悬浮按钮评审通过。

该需求范围清晰：仅针对微信小程序非首页主要业务页面新增统一返回首页悬浮按钮，首页不展示；不包含首页改造、底部 TabBar 改造、Web 展示端、管理端配置、登录授权链路、埋点分析或全屏媒体体验改造。验收标准覆盖功能、UI、安全区、页面栈、异常状态、设备 evidence 与小程序导航 best-practice，具备进入 OpenSpec Change 的条件。

## 评审检查清单

- [x] 范围清晰，Out of Scope 明确。
- [x] 验收标准可测试，覆盖首页隐藏、非首页展示、点击返回、遮挡规避、异常兜底和设备 evidence。
- [x] 优先级 P1 合理，符合小程序深层浏览快速回首页的体验价值。
- [x] UI 类需求已提供 `prototype/miniapp/` 原型策略和静态 HTML。
- [x] 未发现与现有 REQ 重复；与品牌、类目、商品详情相关需求关系已说明。

## 条件通过项

- [ ] `/req-opsx` 阶段 MUST 明确首页是否为 TabBar 页面，并据此选择 `wx.switchTab`、`wx.reLaunch` 或项目确认的等价导航策略。
- [ ] `/req-opsx` 阶段 MUST 输出页面覆盖清单和例外清单，至少覆盖首页、搜索结果页、分类商品列表页、品牌详情页、商品详情页、登录/授权页、错误页、全屏视频页和图片预览页。
- [ ] 实现阶段 MUST 遵守 `docs/knowledge-base/best-practices/miniapp-custom-navigation.md`，补充 DevTools 320/375/430 pt evidence；真机不可用时不得写作真机通过。

## 后续动作

1. `/req-opsx REQ-0085-miniapp-global-home-floating-button`
2. 纳入 Sprint 后再执行 `/opsx-apply`
