## Context

REQ-0045 已将微信小程序分类列表页评审通过并纳入 `sprint-008`。当前小程序已有首页与 SKU 详情页能力，首页 TabBar 目标已经包含“分类”，但尚缺可承接该 Tab 的正式分类频道。后台已有 `tile-category-management` 主数据能力；本 Change 需要在不扩大管理端维护范围的前提下，为小程序提供公开、可缓存、可跳转的分类浏览体验。

## Goals / Non-Goals

### Goals

- 新增 `pages/category/index`，作为底部 TabBar「分类」频道。
- 展示一级分类左侧导航与二级分类右侧三列宫格。
- 仅展示启用分类，按后台排序值升序，排序相同时按创建时间升序。
- 支持公开分类树读取、版本号缓存、静默刷新、页面返回恢复。
- 支持二级分类跳转分类商品列表页。
- 分类列表页不展示店铺 Logo/Header 模块或搜索框。
- 覆盖骨架屏、空状态、网络失败、下架分类移除、埋点和移动端触控验收。

### Non-Goals

- 不新增管理端分类维护页、批量分类维护、分类封面上传 UI 或权限配置。
- 不在分类页展示店铺 Logo/Header 模块、搜索框、商品卡片、价格、收藏、筛选排序栏、热门分类模块或完整商品列表页。
- 不新增购物、询价、库存、订单或客户管理能力。
- 不在分类列表页读取或渲染二级分类图片资源。

## Decisions

### D1. 小程序 UI 策略

本 Change 采用小程序原生实现策略，复用 REQ-0045 的 `prototype/miniapp/` 作为首要设计依据，不走 Web `prototype/web` 的 CSS Port / DS Explore Gate。页面视觉应延续小程序首页的深色高端风格，并在 320-430 pt 宽度范围内验证左右双栏、底部 TabBar 和触控区域。

### D2. 分类树数据契约

优先复用现有 `tile_categories` 主数据，提供小程序公开读取契约：

```http
GET /api/miniapp/categories/tree?depth=2
```

响应只返回两级启用分类及公开字段：

```json
{
  "code": 0,
  "data": {
    "version": "20260718-01",
    "items": [
      {
        "id": "floor",
        "name": "地面砖",
        "sort": 10,
        "children": [
          {
            "id": "polished-marble",
            "name": "通体大理石",
            "coverUrl": "https://.../thumb.jpg",
            "sort": 10
          }
        ]
      }
    ]
  }
}
```

`coverUrl` 仅作为接口兼容字段，分类列表页不渲染该资源。若实现阶段发现已有公开接口可以等价满足该契约，可复用并在实现说明中记录映射关系；若新增或调整 API，必须同步 OpenAPI、Orval、`docs/03-api-index.md`、错误码/治理文档和集成测试。

### D3. 缓存与刷新

分类页进入时先读取本地缓存；无缓存展示骨架屏。请求成功后使用 `version` 判断是否需要无闪动更新。切换一级分类不重新请求接口。缓存建议 24 小时，进入页面时仍可静默刷新；刷新失败不得清空已展示缓存。

### D4. 跳转与页面恢复

二级分类卡片整块可点击，跳转：

```text
pages/product-list/index?categoryId={secondaryCategoryId}&categoryName={encodedName}
```

300ms 内重复点击只触发一次。跳转失败展示“页面打开失败，请重试”。从分类商品列表或 SKU 详情返回后，恢复当前一级分类、左侧滚动位置和右侧滚动位置；若当前分类已下架，回退到第一个可用一级分类。

### D5. 图片与存储边界

分类列表页不展示二级分类图片，不自动取第一款商品主图替代分类展示图，也不加载分类封面缩略图或原始大图。若后端为兼容旧契约返回 `coverUrl`，仍必须使用安全公开 URL，不暴露原始 object key；真实分类封面维护能力如需上线，应拆分后续 REQ/Change。

### D6. 埋点与隐私

分类页埋点包括 `category_page_view`、`primary_category_click`、`secondary_category_click`、`category_load_failed`。事件只允许必要分类 ID、索引、来源、错误码和是否有缓存，不得包含 Authorization header、Cookie、手机号、原始 payload 或其他敏感信息。

## Conflict Resolution

| 来源 | 结论 |
|---|---|
| `prototype/miniapp/prototype.html` | 首要 UI 依据，定义 390x844 高保真分类页、左侧 98px 导航、右侧三列宫格和底部 TabBar。 |
| `prototype/miniapp/prototype.png` | 视觉验收参考，需用于后续实现截图对比或人工验收。 |
| `prototype/miniapp/context.md` | 定义深色风格、组件树、一级/二级分类组件和负面约束。 |
| `prototype/miniapp/interaction.md` | 定义缓存、切换、跳转、防抖、返回恢复、滚动、异常态和无障碍。 |
| `acceptance.md` | 与原型一致；其中 API/Orval 同步为条件性要求，取决于是否新增/调整接口。 |
| `rules/ui-design.md` | Web token 规则对小程序不直接套用，但“工业石材 · 暗色旗舰风”和品牌金克制使用应保持一致。 |
| 既有 specs | `miniapp-home` 已定义 TabBar 目标和安全降级，`tile-category-management` 定义后台类目主数据；本 Change 新增小程序分类页公开展示能力，不修改管理端维护要求。 |

## Risks

- Sprint 008 fix 缓冲已降至 4.0 人天 / 13.33%，分类页实现必须控制范围。
- 分类商品列表页若尚未完整实现，分类页跳转必须安全降级或进入已有可用承接页，不得白屏。
- 若新增 API，必须同步 OpenAPI、Orval、docs 和测试，避免小程序端手写重复类型。

## Verification

- OpenSpec validate: `openspec validate add-miniapp-category-list-page --strict`
- 后端/API：分类树接口成功、启用过滤、排序、版本号、公开字段过滤、错误处理测试。
- 小程序：分类页静态/交互测试、TabBar 入口、双栏滚动、防抖、缓存恢复、异常态、埋点。
- 视觉：390x844、375x812、320-430 pt 范围截图或人工验收；确认不出现商品卡片、价格、热门分类或白底卡片。
