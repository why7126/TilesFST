---
created_at: 2026-07-19 18:27:18
updated_at: 2026-07-19 22:17:30
---

# 微信小程序商品卡片组件实现证据

## 覆盖范围

| 入口 | 证据 | 结论 |
|---|---|---|
| 分类 / 商品列表 | `pages/product-list/index.wxml` 使用 `<product-card>`，传入 `categoryId`、`brandId`、`keyword`、`listContext`、`index`、`requestId` | pass |
| 搜索结果 | `pages/search/index.wxml` 的最近浏览、最佳匹配、SKU 结果列表均使用 `<product-card>`，并通过 `bindcardtap` 保留最近浏览 | pass |
| 首页推荐 | `pages/index/index.wxml` 的新品、热销、全部产品均使用 `<product-card>`，移除卡片内收藏视觉占位 | pass |
| SKU 详情入口 | `pages/tile-detail/index.ts/js` 白名单读取 `sourcePage`、`sourceModule`、`categoryId`、`brandId`、`keyword`、`listContext`、`index`、`requestId` | pass |

## 组件状态

| 状态 | 证据 | 结论 |
|---|---|---|
| 字段缺失 | `components/product-card/index.ts/js` 统一兜底 `未命名商品`、`品牌待确认`、`规格待补充`、`暂无`，并兼容清洗旧接口或缓存中的无价文案 | pass |
| 图片失败 | `components/product-card/index.wxml` 绑定 `onImageError`，失败展示 `暂无图片`；`index.ts/js` 记录 `product_card_image_failed` | pass |
| 不可查看 | 缺少 `skuId`、`available=false`、`is_public=false` 或 `status=offline` 时阻止跳转并提示 `商品暂不可查看` | pass |
| 防重复点击 | `NAV_LOCK_MS = 800`，跳转期间忽略重复点击 | pass |
| 埋点 | 曝光、点击、图片失败、不可用点击分别记录 `product_card_exposure`、`product_card_click`、`product_card_image_failed`、`product_card_unavailable_click` | pass |
| v1 操作边界 | 卡片内未提供收藏、分享、询价、购物车、联系客服或在线下单快捷按钮 | pass |

## 校验

| 命令 | 结果 |
|---|---|
| `uv run pytest tests/test_miniapp_static.py` | 20 passed |
| `uv run pytest tests/test_miniapp_static.py tests/test_miniapp_home.py::test_miniapp_home_returns_public_data_and_hides_internal_fields` | 21 passed |

## 设备验收说明

已基于用户提供的小程序首页验收截图和反馈完成修正：商品卡片信息顺序精简为 SKU 名称、品牌、规格、参考价格；价格空值、0 值、旧无价文案均显示为 `暂无`；首页全部产品改为与热销推荐一致的双列完整卡片布局，并保留持续下拉加载。分类列表、搜索结果和首页推荐三处复用入口均由静态测试覆盖。
