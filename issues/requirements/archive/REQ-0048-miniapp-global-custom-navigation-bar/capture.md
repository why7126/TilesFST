---
req_id: REQ-0048-miniapp-global-custom-navigation-bar
status: done
created_at: 2026-07-19 11:02:04
updated_at: 2026-07-19 12:27:05
recorded_by: product
source: 反馈
priority_hint: P1
parent_requirement: REQ-0042-custom-navigation-bar
---

# 小程序全局自定义导航栏

微信小程序需要将自定义导航栏能力扩展为全局导航模块：首页保留当前品牌 brand-header，非首页复用同一导航模块并在左侧新增返回按钮，右侧继续避让微信原生分享/关闭胶囊。

# 原始描述

小程序全局自定义导航栏
首页：保留当前品牌 brand-header
非首页：同一导航模块，左侧新增返回按钮
右侧：继续避让微信原生分享/关闭胶囊
页面范围：search、tile-detail、category、product-list、favorites、certificates、store-info 等
验收：返回行为、分享行为、状态栏避让、内容不被 fixed header 遮挡

# 待澄清

- [ ] 非首页返回按钮在无页面栈时的兜底行为：返回首页、返回上一业务入口，还是隐藏返回按钮。
- [ ] 页面范围是否包含后续新增小程序页面，还是仅覆盖本次列举页面。
- [ ] 非首页标题展示规则：固定页面标题、动态 SKU/分类标题，还是仅展示品牌信息与返回按钮。

# 探索结论

（/req-explore 后人工确认写入）
