---
requirement_id: REQ-0048-miniapp-global-custom-navigation-bar
title: 小程序全局自定义导航栏
terminal: miniapp
version: v1
status: done
owner: product
source: capture.md
priority: P1
parent_requirement: REQ-0042-custom-navigation-bar
created_at: 2026-07-19 11:06:32
updated_at: 2026-07-19 12:27:05
---

# REQ-0048 小程序全局自定义导航栏

## 1. 需求背景

`REQ-0042-custom-navigation-bar` 已将微信小程序首页搜索框上方的 `brand-header` 定义为首页品牌自定义导航栏，并明确右侧需要避让微信原生分享 / 关闭胶囊区域。本需求在该基础上，将自定义导航栏能力扩展到小程序非首页页面，形成统一的顶部导航模块。

首页继续保留当前品牌 `brand-header` 表达，不引入返回按钮；非首页使用同一导航模块，并在左侧新增返回按钮，便于用户从搜索、详情、分类、列表、收藏、证书和门店信息等页面返回上一层。导航栏右侧继续避让微信原生胶囊，页面内容必须避让 fixed header，避免首屏内容被遮挡。

## 2. 目标用户

| 用户 | 诉求 |
|---|---|
| 装修业主 | 在搜索、分类、商品详情等页面能稳定返回上一页，并继续使用微信原生分享能力。 |
| 设计师 | 展示商品详情或证书时，顶部品牌与返回行为一致，不干扰内容浏览。 |
| 门店销售 | 在客户演示小程序时，跨页面导航体验一致，返回与分享路径清晰。 |
| 开发 / 测试人员 | 有统一的导航模块边界、页面覆盖范围和避让验收标准，减少每页重复实现。 |

## 3. 需求目标

- 建立小程序全局自定义导航栏规则，覆盖首页与主要非首页页面。
- 首页保留当前品牌 `brand-header`，不新增左侧返回按钮。
- 非首页复用同一导航模块，左侧显示返回按钮。
- 导航栏右侧必须避让微信原生分享 / 关闭胶囊，不手绘模拟系统胶囊。
- 页面内容必须根据导航栏高度和状态栏安全区下移，避免被 fixed header 遮挡。
- 返回行为、分享行为、状态栏避让和内容避让必须可验收。

## 4. 范围

### 4.1 本期包含

| 范围 | 说明 |
|---|---|
| 首页导航 | 首页继续保留当前品牌 `brand-header`，作为品牌型自定义导航栏。 |
| 非首页导航 | 非首页使用同一导航模块，在左侧新增返回按钮。 |
| 返回按钮 | 覆盖 search、tile-detail、category、product-list、favorites、certificates、store-info 等页面。 |
| 原生胶囊避让 | 导航栏右侧为微信原生分享 / 关闭胶囊保留安全区域。 |
| 状态栏避让 | 导航栏必须适配不同机型状态栏高度、安全区和胶囊位置。 |
| 内容避让 | 页面主体内容不得被 fixed header 遮挡，滚动起点与骨架屏同样需要避让。 |
| 分享能力 | 保留微信小程序原生分享行为，不因自定义导航栏丢失分享入口或分享配置。 |

### 4.2 本期不包含

| 不包含 | 说明 |
|---|---|
| 新增业务页面 | 本需求只规范已有和已规划页面的导航栏，不新增业务页面。 |
| 后台配置导航 | 不提供导航栏 Logo、标题、颜色、按钮策略的后台配置。 |
| 手绘系统胶囊 | 不在页面内模拟微信分享 / 关闭按钮或胶囊控件。 |
| 改造底部 TabBar | 不调整现有 TabBar 范围、文案、图标和路由。 |
| 新增 API / DB | 默认不新增接口、表或字段。 |
| 完整视觉重设计 | 不重新设计小程序整体视觉，仅在现有品牌导航基础上做全局化。 |

## 5. 功能要求

### FR-001 全局导航模块

- 小程序 MUST 抽象或复用统一的自定义导航模块，承接首页和非首页的顶部导航展示。
- 首页 MUST 保留当前品牌 `brand-header` 的品牌表达，包括品牌 Logo、门店名称和品牌副文案或等价元素。
- 非首页 MUST 使用同一导航模块的非首页形态，左侧显示返回按钮，中间 / 左中区域展示品牌或页面标题信息。
- 导航模块 MUST 支持按页面类型区分首页形态与非首页形态，不得在首页误显示返回按钮。

### FR-002 非首页返回按钮

- search、tile-detail、category、product-list、favorites、certificates、store-info 等非首页页面 MUST 在导航栏左侧显示返回按钮。
- 返回按钮点击后 SHOULD 优先执行小程序页面栈返回上一页。
- 当页面栈无上一页时，返回按钮 MUST 有明确兜底策略，建议返回首页。
- 返回按钮的点击热区 MUST 不小于 44x44 pt，不得与品牌 Logo、标题或页面内容重叠。
- 返回按钮 loading、空状态、错误状态下仍应保持可用，除非当前页面正在执行不可中断的关键操作。

### FR-003 微信原生胶囊避让

- 导航栏右侧 MUST 根据微信小程序胶囊按钮位置预留不可占用区域。
- 品牌内容、页面标题、返回按钮、搜索入口或其他自定义元素 MUST NOT 进入微信原生分享 / 关闭胶囊区域。
- 页面 MUST 使用微信小程序可获取的状态栏、菜单按钮或安全区信息进行布局计算，避免硬编码单一机型高度。
- 不得在 WXML / WXSS 中手绘模拟分享按钮、关闭按钮或胶囊控件。

### FR-004 分享行为

- 自定义导航栏改造后，页面仍 MUST 保留微信小程序原生分享能力。
- 支持分享的页面 SHOULD 继续通过页面级分享配置输出正确标题、路径和封面。
- tile-detail 页面分享 MUST 继续指向当前 SKU 详情，并保留必要的 SKU 参数。
- 非分享页面不得因为导航栏右侧避让而出现不可点击的伪分享按钮。

### FR-005 fixed header 内容避让

- 当导航栏使用 fixed / sticky 顶部定位时，页面主体 MUST 通过统一 spacing、padding 或占位层避让导航栏高度。
- 首屏内容、搜索框、媒体区、分类列表、商品卡片、收藏列表、证书列表和门店信息内容 MUST NOT 被导航栏遮挡。
- 加载态、空状态、错误态、骨架屏和下拉刷新区域 MUST 同样遵守内容避让。
- 不同页面不得各自硬编码互相冲突的顶部 padding；实现阶段 SHOULD 使用统一变量或工具函数承接导航栏高度。

### FR-006 页面覆盖范围

- 本期至少覆盖以下页面：search、tile-detail、category、product-list、favorites、certificates、store-info。
- 若实现阶段发现已有其他非首页页面使用同类顶部导航，也 SHOULD 纳入统一模块，避免新增重复 header。
- 后续新增非首页页面 SHOULD 默认接入该导航模块，除非 OpenSpec 或 PRD 明确豁免。

### FR-007 状态稳定

- 首次进入页面、从分享卡片进入、从首页跳转、从详情推荐跳转和返回上一页时，导航栏高度与内容起点 MUST 稳定。
- 网络失败、数据为空、SKU 下架或页面参数错误时，导航栏仍 MUST 展示并提供返回能力。
- 屏幕宽度 320 到 430 pt 范围内，返回按钮、品牌内容 / 页面标题和右侧胶囊避让区不得重叠。

## 6. UI / UE 约束

- UI MUST 延续 `REQ-0042` 与 `REQ-0043` 的深色品牌导航视觉，不引入与当前首页冲突的新主题。
- 首页导航应保持当前 `brand-header` 的品牌识别强度，非首页导航应更轻量，以返回和页面识别为主。
- 返回按钮 SHOULD 使用清晰的左箭头图标，可搭配无障碍文本或隐藏语义标签。
- 非首页标题若展示动态内容，MUST 控制单行截断，不能挤压右侧胶囊避让区。
- 导航栏层级必须高于页面内容，但不得遮挡微信原生胶囊。
- 内容区顶部间距应由导航栏实际高度推导，不应靠视觉猜测微调。
- 不同机型、不同状态栏高度和横向窄屏下，导航栏不应产生横向滚动。

## 7. 关联需求

| 关联项 | 关系 |
|---|---|
| `REQ-0042-custom-navigation-bar` | 父需求；首页品牌自定义导航栏基础。 |
| `REQ-0043-miniapp-home-style-optimization` | 视觉基准；全局导航需延续小程序深色品牌风格。 |
| `REQ-0044-miniapp-sku-detail-page` | 重点覆盖页面；商品详情需要返回和分享行为稳定。 |
| `REQ-0046-search-component-application` | 覆盖 search 页面；搜索页需要接入非首页导航。 |
| `REQ-0047-product-list-common-component-application` | 覆盖 product-list 页面；商品列表页需要接入非首页导航。 |

## 8. 技术与实现影响预判

| 领域 | 影响预判 |
|---|---|
| 小程序 | 预计影响 `src/miniapp` 的全局配置、导航组件、首页与多个非首页页面 WXML/WXSS/TS。 |
| API | 默认不新增 API；分享路径继续使用现有页面参数。 |
| 数据库 | 默认不新增表或字段。 |
| Web 管理端 | 不涉及。 |
| Web 展示端 | 不涉及。 |
| Orval | 默认不需要；若后续新增接口 contract，则实现阶段再同步。 |
| Docker Compose | 不涉及。 |
| 测试 | 后续 `req-complete` / OpenSpec 阶段需补充返回、分享、状态栏避让和内容不遮挡验收。 |

## 9. 状态块

```yaml
requirement_id: REQ-0048-miniapp-global-custom-navigation-bar
status: done
priority: P1
terminal: miniapp
parent_requirement: REQ-0042-custom-navigation-bar
readiness: Ready
next_step: /opsx-apply add-miniapp-global-custom-navigation-bar
decision:
  split_rationale: 同一功能域的一个交付单元，围绕小程序全局自定义导航栏展开。
  home_behavior: keep current brand-header, no back button
  non_home_behavior: reuse same navigation module with left back button
  native_capsule: reserve right safe area for WeChat native share and close capsule
  covered_pages:
    - search
    - tile-detail
    - category
    - product-list
    - favorites
    - certificates
    - store-info
  acceptance_focus:
    - back behavior
    - share behavior
    - status bar safe-area avoidance
    - content not covered by fixed header
```
