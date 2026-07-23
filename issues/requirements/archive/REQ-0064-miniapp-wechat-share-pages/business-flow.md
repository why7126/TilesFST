---
requirement_id: REQ-0064-miniapp-wechat-share-pages
title: 微信小程序多页面支持微信分享 - 业务流程
status: done
created_at: 2026-07-21 09:45:04
updated_at: 2026-07-22 08:26:47
---

# 业务流程

## 1. 总体分享流程

```text
用户进入目标页面
  |
  +-- 首页
  +-- 商品详情页
  +-- 商品列表页
  +-- 品牌详情页
        |
        v
页面准备分享上下文
  |
  +-- 标题：页面语义 / 商品名 / 列表标题 / 品牌名
  +-- 路径：页面路径 + 必要 query 参数
  +-- 图片：分享图 / 主图 / 品牌图 / 本地兜底图
  +-- 埋点：页面、渠道、业务 ID、来源
        |
        v
用户触发微信原生分享
  |
  +-- 分享给微信朋友：返回小程序卡片配置
  |
  +-- 分享到朋友圈：返回朋友圈配置
        |
        v
被分享用户点击入口
  |
  +-- 参数有效：进入对应页面并加载数据
  |
  +-- 参数无效 / 数据不可见 / 网络失败：展示错误或空状态
        |
        v
无页面栈直达时，返回按钮兜底到首页
```

## 2. 页面路径策略

| 页面 | 分享路径策略 | 直达兜底 |
|---|---|---|
| 首页 | `/pages/index/index?source=share` 或等价来源标识 | 首页加载失败时保留重试或默认内容兜底。 |
| 商品详情页 | `/pages/tile-detail/index?skuId=<id>&source=share` | `skuId` 无效时展示商品暂不可查看，并可返回首页。 |
| 商品列表页 | `/pages/product-list/index?<当前上下文>` | 参数缺失时降级为全部商品或对应可解析列表。 |
| 品牌详情页 | `/pages/brand-detail/index?brandId=<id>&source=share` | `brandId` 无效时提示返回品牌馆或首页。 |

## 3. 商品列表上下文保留

```text
商品列表上下文
  |
  +-- 搜索列表：keyword
  +-- 分类列表：categoryId + categoryLevel + categoryName
  +-- 品牌商品：brandId
  +-- 榜单入口：section=new | hot
  +-- 来源入口：sourcePage
```

规则：

- 分享路径 SHOULD 尽可能保留用户进入列表时的业务上下文。
- 参数值 MUST 经过安全编码，尤其是中文分类名和搜索词。
- 被分享用户打开列表后，页面标题、空状态、错误态和加载结果 MUST 与参数语义一致。
- 不可解析参数不得导致白屏；应降级到可浏览列表或明确错误态。

## 4. 分享埋点流程

```text
页面生成分享配置
  |
  +-- 记录分享触发事件
        |
        +-- 成功：继续返回微信分享对象
        |
        +-- 失败：吞掉错误，仅记录 console 或静默失败
  |
  v
微信平台处理分享
```

埋点字段建议：

| 字段 | 说明 |
|---|---|
| `page_path` | 当前分享页面路径。 |
| `share_channel` | `wechat_friend` 或 `wechat_timeline`。 |
| `sku_id` | 商品详情页适用。 |
| `brand_id` | 品牌详情页或品牌商品列表适用。 |
| `category_id` / `category_level` / `category_name` | 分类列表适用。 |
| `keyword` | 搜索列表适用。 |
| `section` | 新品榜 / 热销榜适用。 |

## 5. 与相关需求差异

| 关联需求 | 已有重点 | REQ-0064 差异 |
|---|---|---|
| `REQ-0041-miniapp-home` | 首页、分享、咨询、热销行为统计。 | 补齐首页朋友圈分享，并将首页纳入统一分享矩阵。 |
| `REQ-0044-miniapp-sku-detail-page` | SKU 详情页信息架构、收藏、分享。 | 补齐朋友圈分享和跨页面分享验收契约。 |
| `REQ-0047-product-list-common-component-application` | 商品列表组件与列表页展示。 | 补齐商品列表页分享能力和筛选上下文保留。 |
| `REQ-0048-miniapp-global-custom-navigation-bar` | 自定义导航、原生胶囊避让、返回兜底。 | 确认分享直达场景必须继续遵守导航与胶囊边界。 |
| `REQ-0058-brand-detail-home-page` | 品牌详情页/主页信息结构。 | 补齐品牌详情页朋友圈分享和 `brandId` 直达契约。 |

## 6. 后续 OpenSpec 关注点

- 若仅补齐页面级分享配置，默认不需要新增后端 API、数据库或 Orval。
- 若实现阶段决定新增后台分享图 / 分享文案配置，必须拆成额外范围或在 Change 中明确 API、DB、管理端影响。
- 小程序运行事实源需同时关注 `.ts` 与实际运行 `.js` 是否同步，避免 DevTools 加载旧逻辑。
- 设备 evidence 应前置到实现阶段，不等归档时再补。
