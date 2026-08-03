## Context

`REQ-0085-miniapp-global-home-floating-button` 已完成评审并处于 `approved`。现有正式能力 `miniapp-global-custom-navigation-bar` 已定义小程序首页/非首页自定义导航、返回兜底、状态栏与胶囊避让、fixed header offset 和小程序导航 best-practice。本 Change 在该能力上新增一个非首页“返回首页”辅助入口：它不是顶部返回按钮的替代，而是让用户从深层页面快速回到首页的独立悬浮按钮。

当前约束：

- 首页不展示该悬浮按钮。
- 默认覆盖搜索结果页、分类列表页、分类商品列表页、品牌列表页、品牌详情页、证书列表页、收藏列表页、商品详情页等首页以外业务页面。
- 登录页、授权页、错误页、全屏视频页、图片预览页等特殊页面必须在实现前明确展示或豁免理由。
- 不新增后台配置、后端 API、数据库字段、Web 展示端能力或埋点报表。
- 小程序导航与设备验收继续引用 `docs/knowledge-base/best-practices/miniapp-custom-navigation.md`。

## Goals / Non-Goals

**Goals:**

- 提供统一返回首页悬浮按钮组件或等价统一接入策略。
- 首页隐藏，主要非首页业务页面展示；分类、品牌、证书、收藏等非首页 TabBar 页面也展示，并上移避让自定义 TabBar。
- 点击后稳定进入首页，避免重复跳转、空白页和页面栈异常。
- 按页面形态避让底部 TabBar、固定操作栏、安全区、客服/分享/咨询类悬浮入口和页面核心内容。
- 明确 DevTools 320/375/430 pt 与真机 evidence 记录要求。

**Non-Goals:**

- 不改造首页内容、首页布局或底部 TabBar。
- 不调整顶部自定义导航栏标题、返回按钮和胶囊规则。
- 不新增登录/授权、全屏视频、图片预览等特殊页面体验改造。
- 不新增 API、数据库字段、管理端配置、Web 展示端能力、埋点统计或运营报表。
- 不修改 MinIO、媒体上传或对象存储策略。

## Decisions

### D1. 作为既有 `miniapp-global-custom-navigation-bar` 能力的增量

本需求属于小程序跨页面导航辅助能力，直接依赖现有自定义导航的状态栏、安全区、页面栈和 evidence 规则。因此 delta spec 修改 `miniapp-global-custom-navigation-bar`，并在其中新增“非首页返回首页悬浮按钮”要求。

备选方案：新增独立 capability `miniapp-global-home-floating-button`。该方案会把导航安全区、返回兜底、胶囊避让和截图 evidence 分散到两个能力中，归档后更容易遗漏复用约束，因此不采用。

### D2. 统一组件或统一配置接入

实现阶段应优先建立统一组件、behavior/mixin 或等价配置式接入策略，集中管理展示判定、点击回首页、防重复点击和位置偏移。各页面只声明“是否展示、是否上移、是否豁免”的最小差异。

备选方案：每个页面手写悬浮按钮。该方案短期快，但容易造成按钮样式、路由、防抖和安全区偏移不一致，因此不采用。

### D3. 首页路径策略由 TabBar 配置决定

设计默认先确认首页是否为 TabBar 页面：

- 若首页为 TabBar 页面，返回首页操作优先使用 `wx.switchTab` 或项目确认等价策略。
- 若首页非 TabBar 页面，或产品要求清理深层页面栈，使用 `wx.reLaunch` 或项目确认等价策略。
- 导航 API fail 时保留当前页面，并给出短提示或静默恢复，不清空页面内容。

这样可以避免 `navigateTo` 重复堆叠首页，也避免错误地使用 `navigateBack` 作为“返回首页”语义。

### D4. 展示覆盖采用白名单 + 例外清单

首期默认覆盖搜索结果页、分类列表页、分类商品列表页、品牌列表页、品牌详情页、证书列表页、收藏列表页、商品详情页。实现前必须列出实际页面路径与例外页面：

- 首页及首页 Tab：隐藏。
- 搜索结果页、分类列表页、分类商品列表页、品牌列表页、品牌详情页、证书列表页、收藏列表页、商品详情页：展示。
- 非首页 TabBar 页面：展示并使用 TabBar 偏移，避免遮挡当前 TabBar 入口。
- 登录、授权、错误、全屏视频、图片预览、原生预览等特殊流程：展示或豁免必须有理由。

当页面存在底部固定操作区时，按钮上移；当页面存在客服、分享或咨询类悬浮入口时，必须明确避让、合并或隐藏策略。

### D5. 原型与验收冲突解决

本 REQ 存在 `prototype/miniapp/`，不存在 `prototype/web/`，因此 Web UI Explore Gate 不适用。

优先级：

```text
prototype/miniapp/home-floating-button.html > prototype/miniapp/context.md > acceptance.md > docs/knowledge-base/best-practices/miniapp-custom-navigation.md > rules/ui-design.md > openspec/specs
```

Conflict Resolution：

- 现有 `miniapp-global-custom-navigation-bar` 已要求无页面栈时可兜底回首页；本 Change 不修改顶部返回按钮语义，而是新增独立悬浮按钮。
- 首页既有导航和 TabBar 规则不冲突；本 Change 明确首页隐藏悬浮按钮。
- SKU 详情页已有底部固定操作栏要求；本 Change 要求悬浮按钮上移避让，不覆盖收藏/分享等底部操作。

## Risks / Trade-offs

- [Risk] 页面逐个接入导致样式和路由分叉 → Mitigation: 使用统一组件或统一配置接入，并在任务中要求检查页面清单。
- [Risk] 悬浮按钮遮挡底部操作区或安全区 → Mitigation: 对商品详情等存在固定操作栏页面单独配置上移偏移，并做 320/375/430 pt evidence。
- [Risk] 首页导航 API 选择错误导致重复堆叠首页或跳转失败 → Mitigation: 先确认首页是否为 TabBar 页面，并用 `switchTab` / `reLaunch` 分支处理。
- [Risk] 特殊页面展示按钮破坏沉浸式体验 → Mitigation: 登录、授权、错误、全屏视频、图片预览等页面必须有展示或豁免理由。
- [Risk] 真机 evidence 不可用 → Mitigation: DevTools 与真机结论分层；真机不可用时标记 blocked 或 follow_up，不写作真机通过。

## Migration Plan

1. 确认小程序首页路径、TabBar 配置、主要非首页页面路径和特殊页面清单。
2. 增加统一返回首页悬浮按钮组件或等价统一接入策略。
3. 接入默认覆盖页面，并为底部固定操作区或已有悬浮入口配置偏移/豁免。
4. 补充小程序静态/页面测试或等价校验。
5. 记录 DevTools 320/375/430 pt evidence；真机不可用时标记 blocked 或 follow_up。

回滚策略：保留页面原有顶部返回、TabBar 和页面跳转能力；如悬浮按钮出现严重遮挡或跳转问题，可临时关闭统一组件展示配置，并保留本 Change 的测试证据与问题记录。

## Open Questions

- 首页当前是否为 TabBar 页面，最终导航 API 使用 `wx.switchTab` 还是 `wx.reLaunch`。
- 实际项目中品牌详情页、搜索结果页、分类商品列表页、商品详情页的页面路径清单。
- 是否存在客服、咨询或分享类悬浮入口需要与返回首页按钮避让或合并。
