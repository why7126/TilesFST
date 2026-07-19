---
requirement_id: REQ-0050-miniapp-brand-header-page-title-rules
title: 小程序 brand-header 页面标题规则
terminal: miniapp
version: v1
status: in_sprint
owner: product
source: capture.md
priority: P1
parent_requirement: REQ-0048-miniapp-global-custom-navigation-bar
created_at: 2026-07-19 14:23:10
updated_at: 2026-07-19 14:40:17
---

# REQ-0050 小程序 brand-header 页面标题规则

## 1. 需求背景

`REQ-0048-miniapp-global-custom-navigation-bar` 已将小程序自定义导航栏扩展为全局导航模块：首页使用品牌型 `brand-header`，非首页使用带返回按钮的导航形态，并统一避让微信顶部状态栏和右侧原生胶囊。

本需求进一步收束 `brand-header` 的文案规则：只有首页保留两行品牌文案；搜索、分类、详情、收藏、证书等其他页面只展示一行页面标题。非首页继续保留返回按钮，右侧继续避让微信原生分享 / 关闭胶囊，不在页面内自绘分享或关闭按钮。

一句话：`brand-header` 首页负责品牌表达，非首页负责页面识别和返回。

## 2. 目标用户

| 用户 | 诉求 |
|---|---|
| 装修业主 | 在搜索、分类、详情等页面快速识别当前页面，并能稳定返回上一页。 |
| 设计师 | 展示商品详情、证书或分类时，顶部标题简洁，不被副文案挤占内容空间。 |
| 门店销售 | 演示小程序时，首页品牌露出明确，非首页导航更轻量、更清晰。 |
| 开发 / 测试人员 | 有明确的首页 / 非首页文案边界，减少各页面自行传入副标题导致的不一致。 |

## 3. 需求目标

- 首页 `brand-header` 固定展示两行文案：`菲尚特瓷砖馆` 与 `质感空间，由砖而生`。
- 非首页 `brand-header` 只展示一行页面标题文字，不展示副标题、副文案或品牌第二行。
- 非首页继续显示返回按钮，首页不显示返回按钮。
- 所有使用自定义导航栏的页面都必须避让顶部状态栏和微信右侧原生胶囊。
- 不自绘微信分享 / 关闭按钮，不用自定义胶囊替代原生能力。
- 页面内容必须继续避让 fixed header，不能被顶部导航遮挡。

## 4. 范围

### 4.1 本期包含

| 范围 | 说明 |
|---|---|
| 首页两行文案 | 首页 `brand-header` 展示 `菲尚特瓷砖馆` 和 `质感空间，由砖而生`。 |
| 非首页一行标题 | 搜索、分类、商品详情、商品列表、收藏、证书、门店信息等页面只展示页面标题。 |
| 返回按钮 | 非首页导航栏左侧保留返回按钮；首页不显示返回按钮。 |
| 胶囊避让 | 导航栏右侧继续为微信原生分享 / 关闭胶囊预留安全区域。 |
| 状态栏避让 | 导航栏继续根据状态栏高度、菜单按钮位置或安全区信息计算布局。 |
| 内容避让 | 页面主体、加载态、空态、错误态和骨架屏不得被顶部 fixed header 遮挡。 |

### 4.2 本期不包含

| 不包含 | 说明 |
|---|---|
| 新增业务页面 | 本需求只规范现有或已接入自定义导航的页面标题，不新增页面能力。 |
| 动态详情标题 | 商品详情页本期建议固定显示 `商品详情`，SKU 编号、商品名留在页面内容区。 |
| 后台配置文案 | 不提供品牌标题、副文案或页面标题的后台配置。 |
| 自绘系统按钮 | 不绘制分享按钮、关闭按钮或微信胶囊控件。 |
| 底部 TabBar 改造 | 不调整 TabBar 文案、图标、路由或自定义底栏组件。 |
| API / DB 变更 | 默认不新增接口、表或字段。 |
| 小程序整体视觉重设计 | 不重新设计页面主题，只收束顶部导航文案规则。 |

## 5. 功能要求

### FR-001 首页 brand-header 文案

- 首页 `brand-header` MUST 展示两行文案。
- 第一行 MUST 为 `菲尚特瓷砖馆`。
- 第二行 MUST 为 `质感空间，由砖而生`。
- 首页 MUST NOT 显示返回按钮。
- 首页右侧 MUST 继续避让微信原生分享 / 关闭胶囊。
- 首页不得因品牌文案调整导致搜索框、Banner 或首屏内容被 fixed header 遮挡。

### FR-002 非首页单行页面标题

- 非首页 `brand-header` MUST 只展示一行页面标题文字。
- 非首页 MUST NOT 展示 `subtitle`、品牌副文案、SKU 编号第二行或类似辅助文案。
- 页面标题 SHOULD 使用稳定中文短标题，例如：`搜索`、`全部分类`、`商品详情`、`全部商品`、`收藏`、`证书`、`门店信息`。
- 标题过长时 MUST 单行截断，不得换成第二行，不得挤压右侧胶囊避让区。
- 商品详情页本期 SHOULD 固定显示 `商品详情`；SKU 编号、商品名称和品牌信息保留在详情内容区展示。

### FR-003 非首页返回按钮

- 非首页导航栏左侧 MUST 显示返回按钮。
- 返回按钮点击后 SHOULD 优先返回上一页。
- 当页面栈无上一页时，返回按钮 MUST 兜底返回首页。
- 返回按钮点击热区 MUST 足够稳定，不得与页面标题、品牌文案或页面内容重叠。
- 加载态、空态、错误态下返回按钮仍应可用。

### FR-004 顶部安全区与原生胶囊避让

- 所有自定义导航页面 MUST 避让微信顶部状态栏。
- 导航栏右侧 MUST 根据微信原生菜单按钮 / 胶囊区域预留空间。
- 自定义标题、返回按钮、Logo 或其他元素 MUST NOT 进入微信原生胶囊区域。
- 页面 MUST NOT 自绘分享按钮、关闭按钮或胶囊形态。
- 分享能力仍由微信小程序原生能力或页面级分享配置承接。

### FR-005 页面内容避让

- 导航栏采用 fixed 顶部定位时，页面主体 MUST 通过统一 spacer、padding 或等价机制避让实际导航高度。
- 搜索框、分类列表、商品列表、详情媒体区、收藏占位、证书占位和门店信息内容 MUST NOT 被导航栏遮挡。
- 加载态、空态、错误态、骨架屏和返回后恢复状态 MUST 同样遵守内容避让。
- 不同页面不应各自硬编码互相冲突的顶部高度。

### FR-006 页面覆盖与后续扩展

- 本期至少覆盖已使用自定义导航的页面：index、search、tile-detail、category、product-list、favorites、certificates、store-info。
- `index` MUST 使用首页两行品牌文案规则。
- search、tile-detail、category、product-list、favorites、certificates、store-info MUST 使用非首页单行标题规则。
- 若 `find`、`profile` 或后续新增页面接入自定义导航，也 SHOULD 默认遵守非首页单行标题规则，除非后续需求明确豁免。

## 6. UI / UE 约束

- UI MUST 延续 `REQ-0042`、`REQ-0043`、`REQ-0048` 的小程序深色品牌导航风格。
- 首页两行文案需要体现品牌感；非首页标题需要更安静、简洁，以页面识别和返回为主。
- 非首页标题字号、行高和垂直居中应按单行标题设计，不为隐藏第二行预留不自然空白。
- 返回按钮应使用清晰左箭头或等价图标，不承担分享、关闭或首页入口含义。
- 320 到 430 pt 宽度范围内，返回按钮、标题和右侧胶囊避让区不得重叠。
- 标题不得出现横向滚动，不得因长文案导致页面级布局抖动。
- 不得使用自绘胶囊、伪分享按钮或伪关闭按钮填充右侧避让区域。

## 7. 关联需求

| 关联项 | 关系 |
|---|---|
| `REQ-0042-custom-navigation-bar` | 首页品牌自定义导航栏基础；明确不自绘原生分享 / 关闭按钮。 |
| `REQ-0048-miniapp-global-custom-navigation-bar` | 父需求；本需求细化其首页 / 非首页文案规则。 |
| `REQ-0044-miniapp-sku-detail-page` | 覆盖商品详情页；标题建议固定为 `商品详情`。 |
| `REQ-0046-search-component-application` | 覆盖搜索页；标题固定为 `搜索`。 |
| `REQ-0047-product-list-common-component-application` | 覆盖商品列表页；标题按列表上下文展示一行。 |

## 8. 技术与实现影响预判

| 领域 | 影响预判 |
|---|---|
| 小程序 | 预计影响 `src/miniapp/components/custom-navigation/` 与已接入该组件的页面 WXML / TS / WXSS。 |
| API | 默认不新增 API。 |
| 数据库 | 默认不新增表或字段。 |
| Web 管理端 | 不涉及。 |
| Web 展示端 | 不涉及。 |
| Orval | 不需要。 |
| Docker Compose | 不涉及。 |
| 测试 | 后续需补充首页两行、非首页单行、返回兜底、胶囊避让和内容不遮挡验收。 |

## 9. 状态块

```yaml
requirement_id: REQ-0050-miniapp-brand-header-page-title-rules
status: in_sprint
priority: P1
terminal: miniapp
parent_requirement: REQ-0048-miniapp-global-custom-navigation-bar
readiness: Ready
next_step: /req-opsx REQ-0050-miniapp-brand-header-page-title-rules
decision:
  split_rationale: 同一功能域的规则细化，作为 REQ-0048 的子需求处理。
  home_brand_header:
    lines:
      - 菲尚特瓷砖馆
      - 质感空间，由砖而生
    back_button: false
  subpage_brand_header:
    line_count: 1
    content: page_title
    back_button: true
    subtitle: forbidden
  detail_title_policy: 商品详情页本期固定显示“商品详情”，动态 SKU 信息留在内容区。
  no_page_stack_back_fallback: 返回首页
  native_capsule: 避让微信右侧原生胶囊，不自绘分享 / 关闭按钮。
  covered_pages:
    - index
    - search
    - tile-detail
    - category
    - product-list
    - favorites
    - certificates
    - store-info
  pending_scope_confirmation:
    - find 页面是否接入 custom-navigation
    - profile 页面是否接入 custom-navigation
```
