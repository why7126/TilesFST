---
bug_id: BUG-0148-miniapp-product-list-card-image-fit
root_cause_status: confirmed
created_at: 2026-09-04 17:44:16
updated_at: 2026-09-04 17:44:16
evidence_source: user_screenshot_and_code_review
---

# 根因分析

## 根因状态

`confirmed`

## 直接原因

微信小程序 `components/product-card/` 中商品图片使用填充裁切模式渲染，`grid` 商品卡片图片框又采用偏矮的固定比例，导致列表卡片中商品图片为了铺满容器被裁切，无法优先完整显示整张图片。

## 根本原因

历史 `REQ-0049-miniapp-product-card-component` 与 `REQ-0056-product-list-card-only-layout` 将商品卡片目标收敛为固定比例、双列稳定、防布局跳动和首页热销推荐式密度，但未把“列表卡片完整显示整张商品图”作为明确验收项。实现侧因此选择了更偏视觉铺满的 `aspectFill` 和 `aspect-ratio: 1 / 0.86`，与本次用户提出的完整露图优先目标不一致。

## 触发条件

- 页面或模块复用 `components/product-card/`。
- 调用方传入 `density="grid"`。
- 商品图片尺寸、主体位置或背景构图不适合被当前扁比例容器裁切。

## 分类

- 类型：UI / design contract
- 端：miniapp
- 层级：组件展示与小程序页面复用
- 数据影响：无
- API 影响：无

## 证据链

| 证据 | 类型 | 入口 | 说明 |
|---|---|---|---|
| 用户参考截图 | 截图 | `issues/bugs/archive/BUG-0148-miniapp-product-list-card-image-fit/screenshots/reference-product-card-image-fit.png` | 参考图展示目标效果：双列卡片应完整露出方砖主体。 |
| 商品卡片图片模式 | 代码定位 | `src/miniapp/components/product-card/index.wxml` | 商品图片使用填充裁切模式，能够解释无法完整显示整图。 |
| `grid` 图片框比例 | 代码定位 | `src/miniapp/components/product-card/index.wxss` | `grid` / `compact` 图片框当前为偏扁固定比例，能够解释卡片高度偏低。 |
| 商品列表复用方式 | 代码定位 | `src/miniapp/pages/product-list/index.wxml` | 商品列表页通过 `density="grid"` 复用同一商品卡片。 |
| 品牌详情复用方式 | 代码定位 | `src/miniapp/pages/brand-detail/index.wxml` | 品牌详情商品 Tab 也通过 `density="grid"` 复用同一商品卡片。 |
| 现有测试契约 | 测试定位 | `tests/test_miniapp_static.py` | 静态测试断言当前图片比例，说明后续修复需同步调整测试契约。 |

## 验证方式

修复前验证：

1. 打开小程序商品列表页或品牌详情商品 Tab。
2. 查看 `density="grid"` 商品卡片。
3. 对照参考截图，确认当前图片存在裁切或完整方砖主体无法露出，且卡片高度偏低。

修复后验证：

1. `grid` 商品卡片图片完整显示整张图，主体不被裁切。
2. 图片区域高度或比例更接近参考图，不出现明显拉伸、破图或突兀留白。
3. 商品列表页、品牌详情商品 Tab、首页全部产品 `grid` 场景均通过 320 / 375 / 430 pt 视口检查。
4. 静态测试更新为新的 `grid` 图片比例与展示模式契约。

## 人工补证

当前根因已由截图和代码定位确认。后续实现阶段仍建议补充小程序 DevTools 或真机截图作为视觉验收证据，重点覆盖商品列表页、品牌详情商品 Tab 和首页全部产品 `grid` 场景。
