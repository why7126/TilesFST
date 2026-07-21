## Context

本 Change 来源于 `REQ-0050-miniapp-brand-header-page-title-rules`，状态为 `in_sprint`，已纳入 `sprint-009`。它是 `REQ-0048-miniapp-global-custom-navigation-bar` 的规则细化，目标不是重做导航组件，而是把 `brand-header` 在首页和非首页的标题契约固定下来。

当前正式 spec `miniapp-global-custom-navigation-bar` 已要求首页保留品牌导航形态、非首页展示返回导航形态、避让微信原生胶囊与状态栏、页面内容避让 fixed header。本 Change 在此基础上进一步明确：

- 首页品牌文案固定为两行：`菲尚特瓷砖馆`、`质感空间，由砖而生`。
- 非首页只能渲染一行页面标题，不允许任何第二行辅助文案。
- 商品详情页顶部标题固定为 `商品详情`，SKU 编号、商品名称和品牌信息留在内容区。

## Readiness Report

**结果：ready。**

- `requirement.md`、`user-stories.md`、`business-flow.md`、`acceptance.md`、`trace.md` 齐全。
- `trace.md` status 为 `in_sprint`，review 已通过，`iteration: sprint-009`。
- 存在 `prototype/miniapp/brand-header-title-rules.html` 与 `prototype/miniapp/context.md`，可作为小程序视觉和交互参考。
- 本需求不命中管理端 `admin-list`、`admin-form`、`admin-modal`、`media-upload` 横切 AC。

## Impact Analysis

```yaml
impact:
  backend: false
  web: false
  miniapp: true
  admin: false
  database: false
  storage: false
  api: false
capabilities:
  new: []
  modified:
    - miniapp-global-custom-navigation-bar
change_type: update
```

## Goals / Non-Goals

**Goals:**

- 统一首页与非首页 `brand-header` 文案规则。
- 保持非首页返回按钮、无页面栈兜底回首页和加载 / 空 / 错状态可用。
- 保持微信顶部状态栏与右侧原生胶囊避让，不自绘系统按钮。
- 保持页面主体、状态页和骨架屏不被 fixed header 遮挡。
- 给后续 `/opsx-apply` 提供可逐项实现和验证的 tasks。

**Non-Goals:**

- 不新增业务页面。
- 不新增后台标题配置、品牌文案配置或动态详情标题配置。
- 不调整底部 TabBar 文案、图标、路由或自定义底栏组件。
- 不新增 API、数据库表或字段。
- 不改 Web 展示端、管理端或 Orval 生成物。

## Conflict Resolution

原型与验收的优先级按本需求上下文执行：

```text
acceptance.md
  > prototype/miniapp/brand-header-title-rules.html
  > prototype/miniapp/context.md
  > rules/ui-design.md
  > openspec/specs
```

冲突处理：

- 正式 spec 原本允许非首页展示“页面标题、品牌短标题或等价页面识别信息”，本 Change 收窄为非首页只展示一行页面标题。
- 正式 spec 原本要求首页品牌 Logo、门店名称和品牌副文案稳定展示；本 Change 固定首页文案为 `菲尚特瓷砖馆` 与 `质感空间，由砖而生`，不得被接口描述或页面上下文覆盖。
- HTML 原型只展示首页、搜索页、商品详情页三个代表状态；acceptance 覆盖 search、category、product-list、tile-detail、favorites、certificates、store-info，后续实现以 acceptance 覆盖范围为准。
- 原型用虚线区域标注“原生胶囊避让区”；实现不得按原型自绘微信分享 / 关闭按钮或自定义胶囊。
- 320/375/430 pt 宽度无重叠、内容不遮挡是实现验收 gate；无法自动化验证时必须留 DevTools 或真机 evidence。

## Decisions

### D1. 采用导航组件契约收敛，而不是逐页复制样式

后续实现应优先在 `custom-navigation` 或等价组件内定义首页 / 非首页形态，页面只传入页面类型、标题或必要上下文。这样可以避免各页通过复制 WXML / WXSS 产生不同的标题行高、胶囊避让和 header offset。

### D2. 非首页标题单行化

非首页标题区域只允许单行文本。长标题使用单行截断，不允许换行、不允许横向滚动，也不允许为隐藏第二行保留明显空白。商品详情页标题固定为 `商品详情`，SKU 信息进入详情内容区。

### D3. 保留微信原生能力边界

导航栏右侧只负责预留微信原生菜单按钮 / 胶囊安全空间。页面不得在 WXML / WXSS 中新增模拟分享、关闭或胶囊控件；分享继续由小程序原生能力或页面级分享配置承接。

### D4. 统一 header offset

fixed header 的实际高度应由统一变量、工具函数、组件事件或 layout class 传递给页面主体和状态页。覆盖页面不得散落互相冲突的顶部 padding 硬编码。

## Risks / Trade-offs

- 非首页历史调用仍传 `subtitle` → 组件层忽略或移除非首页 subtitle，并补静态检查 / 页面断言。
- 商品详情页顶部不显示 SKU 编号可能降低即时识别 → SKU 编号、商品名和品牌信息保留在内容区，分享标题和路径不受影响。
- 微信菜单按钮信息获取失败 → 使用安全 fallback 尺寸，仍预留右侧不可占用区域。
- 设备证据无法完全自动化 → 至少记录 320、375、430 pt 宽度下的 DevTools 或真机截图 / 说明，后续可复用 REQ-0052 evidence 模板。

## Migration Plan

1. 更新导航组件契约，区分首页双行品牌形态和非首页单行标题形态。
2. 更新 index、search、tile-detail、category、product-list、favorites、certificates、store-info 标题参数或调用方式。
3. 统一内容 offset，覆盖正常、加载、空态、错误态和骨架屏。
4. 补充小程序静态测试或等价验证。
5. 用微信开发者工具或真机记录 320、375、430 pt evidence。

回滚策略：若实现出现布局风险，可回滚页面调用和组件变更到父需求 REQ-0048 的全局导航形态，但不得保留自绘胶囊或遮挡微信原生区域的实现。
