---
req_id: REQ-0053-miniapp-custom-navigation-best-practice
status: done
created_at: 2026-07-19 17:28:06
updated_at: 2026-07-19 21:05:25
recorded_by: product
source: 反馈
priority_hint: P1
parent_requirement: REQ-0048-miniapp-global-custom-navigation-bar
---

# 小程序自定义导航 best-practice 沉淀

为微信小程序自定义导航栏沉淀可复用 best-practice，明确状态栏安全区、微信右侧原生胶囊避让、返回按钮兜底、页面内容 offset 和截图验收矩阵，避免后续页面重复踩坑或仅依赖单页实现经验。

# 原始描述

为小程序自定义导航沉淀 best-practice，明确状态栏、胶囊、返回兜底、页面 offset 和截图验收矩阵

# 待澄清

- [ ] best-practice 最终沉淀位置是 `docs/knowledge-base/best-practices/`、小程序开发规范、OpenSpec tasks 模板，还是多处引用同一事实源。
- [ ] 状态栏与胶囊数据来源是否统一为 `wx.getWindowInfo()`、`wx.getMenuButtonBoundingClientRect()` 及降级默认值，并明确异常兜底策略。
- [ ] 返回按钮兜底行为是否统一为有页面栈时 `wx.navigateBack()`，无页面栈时回首页，或按页面声明业务 fallback route。
- [ ] 页面内容 offset 是否要求所有使用自定义导航的页面通过统一 CSS 变量、组件外层 class 或页面配置注入，避免内容被导航栏遮挡。
- [ ] 截图验收矩阵是否覆盖 DevTools、iPhone 刘海屏、iPhone 非刘海屏、Android 常见机型、横竖屏、首页/非首页/详情页/空状态等组合。
- [ ] 是否需要与 REQ-0052 的小程序 DevTools/真机验收 evidence 模板联动，复用设备、截图路径、结论和阻塞项字段。

# 探索结论

（/req-explore 后人工确认写入）
