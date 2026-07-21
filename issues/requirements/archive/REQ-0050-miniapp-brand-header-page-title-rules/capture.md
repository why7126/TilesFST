---
req_id: REQ-0050-miniapp-brand-header-page-title-rules
status: done
created_at: 2026-07-19 14:14:10
updated_at: 2026-07-19 20:51:26
recorded_by: product
source: 反馈
priority_hint: P1
parent_requirement: REQ-0048-miniapp-global-custom-navigation-bar
---

# 小程序 brand-header 页面标题规则

小程序 brand-header 需要按页面类型区分文案规则：首页展示两行品牌文案，其他页面只展示一行页面标题，并在非首页提供返回按钮。

# 原始描述

brand-header，除了首页外，其他页面都只有一行文字（首页有2行：菲尚特瓷砖馆+质感空间，由砖而生）

新规则是：
首页 brand-header：两行文案
菲尚特瓷砖馆
质感空间，由砖而生

其他页面 brand-header：只有一行页面标题文字
例如搜索、分类、详情、收藏、证书等页面显示各自标题，并带返回按钮。

全局共性：都需要避让顶部状态栏和微信右侧原生胶囊；非首页新增返回按钮；不自绘分享/关闭按钮。

# 待澄清

- [ ] 详情页标题是否固定显示“详情”，还是根据 SKU / 分类 / 证书名称动态展示。
- [ ] 非首页无页面栈时，返回按钮兜底行为是返回首页、返回上一业务入口，还是隐藏。

# 探索结论

（/req-explore 后人工确认写入）
