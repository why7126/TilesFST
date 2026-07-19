## Context

`REQ-0042-custom-navigation-bar` 已明确首页 `brand-header` 的品牌导航边界，并要求右侧避让微信原生分享 / 关闭胶囊。REQ-0048 将该能力推广到非首页：search、tile-detail、category、product-list、favorites、certificates、store-info 等页面都需要统一导航模块、左侧返回按钮和 fixed header 内容避让。

当前 Sprint 008 已纳入 REQ-0048，容量占用达到 120.00% 上限。本 Change 必须保持小程序单端、低改动面和复用优先，不扩展后台配置、API、数据库或新增业务页面。

## Goals / Non-Goals

**Goals:**

- 复用或抽象统一小程序自定义导航模块。
- 首页保留当前品牌 `brand-header`，不出现返回按钮。
- 非首页显示左侧返回按钮，优先 `navigateBack`，无页面栈时兜底返回首页。
- 所有覆盖页面避让微信原生分享 / 关闭胶囊和状态栏安全区。
- 统一页面内容顶部 offset，避免 fixed header 遮挡首屏内容、状态页和下拉刷新区。
- 保留支持分享页面的微信原生分享能力。

**Non-Goals:**

- 不新增业务页面。
- 不新增后台导航配置、颜色配置、Logo 配置或页面标题配置。
- 不手绘模拟微信系统分享按钮、关闭按钮或胶囊控件。
- 不调整底部 TabBar。
- 默认不新增 API、数据库字段、对象存储能力或 Orval 生成物。
- 不进行小程序整体视觉重设计。

## Decisions

### D1. 统一导航模块，按页面类型切换形态

实现阶段 SHOULD 抽象 `custom-navigation` 或等价组件/模块，以 `variant=home|subpage`、`title`、`subtitle`、`showBack` 等输入控制展示。首页使用品牌形态，非首页使用返回形态。

理由：减少每个页面重复实现 header 和顶部 padding，降低后续页面接入时的布局漂移风险。

替代方案：每页单独实现导航。该方案短期更快，但会导致胶囊避让、状态栏高度和内容 offset 难以统一，拒绝。

### D2. 运行时读取微信状态栏与胶囊信息

实现阶段 MUST 使用微信小程序可获得的系统信息和菜单按钮位置信息，计算状态栏高度、胶囊避让宽度和导航内容高度。不得只按单一机型硬编码高度。

理由：REQ-0048 的核心验收是状态栏避让、原生胶囊避让和 320-430 pt 宽度适配。

### D3. 返回策略优先页面栈，兜底首页

非首页返回按钮点击时 SHOULD 优先使用页面栈返回上一页；当页面栈为空或无上一页时 MUST 兜底返回首页。

理由：从分享卡片直达 tile-detail 时页面栈可能为空，返回按钮不能失效或报错。

### D4. 统一内容 offset

实现阶段 SHOULD 通过统一 CSS 变量、computed style 或公共 layout class 暴露导航总高度。页面主体、加载态、空态、错误态、骨架屏和下拉刷新区域都必须使用该 offset。

理由：REQ-0048 明确禁止内容被 fixed header 遮挡，也禁止各页面散落互相冲突的硬编码高度。

### D5. Conflict Resolution

本 REQ 只有 `prototype/miniapp`，没有 `prototype/web`；不触发 Web UI Explore Gate。原型优先级按本 Change 解释为：`prototype/miniapp/prototype.html` > `prototype/miniapp/context.md` > `acceptance.md` > `rules/ui-design.md` > 既有 `openspec/specs`。

冲突处理：

- 与 `REQ-0042` 的“首页不做全局导航壳”不冲突；REQ-0048 是后续全局化延展。
- 与 `miniapp-home` 中首页真实小程序导航环境要求兼容；本 Change 禁止手绘系统胶囊。
- 若原型中的虚线胶囊占位与真实微信胶囊位置不同，以微信运行时信息和真机/开发者工具验收为准。

## Risks / Trade-offs

- **容量已达 120% 上限** → 本 Change 只做 S 级 refinement，禁止扩展 API/DB、后台配置或新增业务页面。
- **不同页面已有顶部 padding 不一致** → 通过统一导航高度变量和页面接入清单收敛。
- **分享直达页面无返回栈** → 返回按钮必须提供首页兜底。
- **右侧胶囊机型差异** → 使用微信运行时信息，验收覆盖 320、375、430 pt 宽度。
- **原生胶囊被误手绘** → spec 和 tasks 明确禁止 WXML/WXSS 自绘系统分享、关闭或胶囊。

## Migration Plan

1. 创建或复用统一导航模块。
2. 首页接入首页形态，确认 brand-header 不回退、不新增返回按钮。
3. search、tile-detail、category、product-list、favorites、certificates、store-info 接入非首页形态。
4. 统一内容 offset，逐页验证首屏、加载态、空态和错误态。
5. 在微信开发者工具或真机验证返回、分享、胶囊避让和 320-430 pt 布局。

回滚策略：保留页面原有导航/顶部布局入口；若统一导航模块出现阻断，可逐页回退到原页面 header，但必须保留已验证页面的内容 offset 不遮挡。
