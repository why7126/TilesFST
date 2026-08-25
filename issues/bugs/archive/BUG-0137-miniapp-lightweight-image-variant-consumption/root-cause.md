---
bug_id: BUG-0137-miniapp-lightweight-image-variant-consumption
root_cause_status: confirmed
category: design
created_at: 2026-08-24 15:02:18
updated_at: 2026-08-25 08:07:55
---

# Root Cause

## 根因状态

`confirmed`

当前代码定位、微信小程序 DevTools Network/render 截图和 AppData 样本已经形成闭环：小程序 Banner 仍通过单一 `image_url` 渲染，品牌 Logo 普通展示代码仍存在 `brand_logo_url` 原图 fallback，商品详情分享图在 `thumbnail_url` 同时存在时仍下发 `.jpg` 原图 `share.image_url`。验收返修阶段又确认首页缺图 fallback 指向小程序包内不存在的 `/assets/tile-placeholder.png`，DevTools Network 显示该资源 307 后 500。因此根因保持 `confirmed`。

## 直接原因

小程序普通展示链路缺少统一的轻量图消费字段和端侧兜底约束：

- Banner 页面模板仍直接使用 `item.image_url` 渲染轮播图，schema 未暴露 `thumbnail_url` / `display_url` 等可区分轻量图的字段。
- 品牌列表、品牌详情和品牌卡片组件仍允许 `brand_logo_thumbnail_url || brand_logo_url` 或等价逻辑，普通展示可以退回品牌 Logo 原图。
- 商品详情分享图仍可能使用 `original_url`、`preview_url` 或 `url` 作为分享图片来源；用户补证样本已复现商品详情 `share.image_url` 为 `.jpg` 原图，而同一资源存在 `.thumb.webp`。
- 验收返修前，首页和多个列表入口把缺图 fallback 写为 `/assets/tile-placeholder.png`，但小程序包内不存在该文件；首页图片加载失败后会继续请求该无效本地静态资源。

## 根本原因

媒体多规格能力已经建立 `thumb` / `display` / `original` 的字段语义，但小程序端不同业务入口仍以历史兼容字段为消费契约。字段命名和 fallback 策略没有形成统一矩阵，导致“展示图”和“原图/预览图”的边界在 Banner、品牌 Logo、分享图三个入口里继续漂移。

## 触发条件

1. Banner、品牌 Logo 或分享图关联的媒体对象存在原图 URL 或旧 `url` 字段。
2. 轻量图字段缺失、未下发、对象不可读，或端侧模板未优先消费轻量图字段。
3. 用户打开小程序首页、品牌列表页、品牌详情页、商品详情页，或触发分享入口。
4. 端侧 fallback 逻辑选择 `image_url`、`brand_logo_url`、`preview_url`、`url` 或 `original_url`。
5. 普通展示或分享入口可能请求原图，造成冷加载大图、流量增加或验收证据缺口。

## 证据链

| 证据入口 | 类型 | 摘要 | 结论 |
|---|---|---|---|
| `src/backend/app/schemas/miniapp_home.py` | 代码定位 | `MiniappBannerItem` 仅定义 `image_url`，未定义 `thumbnail_url` / `display_url` | Banner schema 缺少轻量图字段契约 |
| `src/miniapp/pages/index/index.wxml` | 代码定位 | 首页 Banner 图片 `src` 绑定 `item.image_url` | 首页 Banner 普通展示无法区分轻量图与原图 |
| `src/miniapp/pages/brand-list/index.wxml` | 代码定位 | 品牌列表 Banner 使用 `item.image_url`；品牌 Logo 使用 `item.brand_logo_thumbnail_url || item.brand_logo_url` | 品牌入口仍有单字段 Banner 和原 Logo fallback |
| `src/miniapp/pages/brand-detail/index.wxml` | 代码定位 | 品牌详情 Logo 使用 `brand.brand_logo_thumbnail_url || brand.brand_logo_url` | 品牌详情普通展示仍可能退到原 Logo |
| `src/miniapp/components/brand-card/index.ts` | 代码定位 | `allowOriginalLogoFallback` 默认 `true`，`logoSrc` 使用 `brand_logo_thumbnail_url || originalLogo` | 复用品牌卡片默认允许原图 fallback |
| `src/backend/app/services/miniapp_home_service.py` | 代码定位 | 证书详情分享图从图片媒体 `entry.url` 派生；SKU 详情分享图使用 `media[0].preview_url or media[0].url` | 分享图字段优先级可能绕过轻量展示字段 |
| `src/miniapp/pages/tile-detail/index.ts` | 代码定位 | `skuShareImage()` fallback 包含 `product.cover_image`、`mainImage.preview_url`、`mainImage.url` | 小程序分享图端侧仍保留旧图字段 fallback |
| 用户补证截图：17:22 首页 Network | 小程序 DevTools Network | `/home` XHR 200，资源约 10.1 kB，耗时约 3.03 s；首页渲染可见 Banner 与商品卡片，图片请求为 `.webp` | 首页 Banner 运行入口已补 Network/render 证据；当前样本未复现原图请求，但仍只能消费 `image_url` |
| 用户补证截图：17:24 品牌列表 Network/render | 小程序 DevTools Network + render | `/brands?page=1&pageSize=20` XHR 200，资源约 8.1 kB，耗时约 1.22 s；品牌页渲染可见 Banner 和品牌矩阵，图片请求为 `.webp`，约 5.9-10.4 kB | 品牌 Logo 运行入口已补 Network/render 证据；当前样本未复现原图请求，但代码 fallback 风险仍存在 |
| 用户补证截图：17:25 品牌详情商品列表 render | 小程序 DevTools Network + render | 品牌详情页渲染可见品牌 Banner 与商品网格，`products?brandId=6&page=1...` XHR 200，资源约 8.5 kB，耗时约 1.21 s | 品牌详情/品牌商品入口已补 render 证据，仍需修复后补齐图片 URL 级别 Network 断言 |
| 用户补证截图：17:27 商品详情 AppData/render | 小程序 DevTools AppData + render | 商品详情 `share.image_url` 为脱敏商品主图 `.jpg` 原图；同一对象存在 `.thumb.webp` 的 `thumbnail_url`；页面渲染可见商品详情和分享按钮 | 商品详情分享图原图 fallback 已被运行时数据直接复现 |
| 用户补证截图：17:28 证书详情 AppData/render | 小程序 DevTools AppData + render | 证书详情 `share.image_url` 为 `images/default/brand-certificates/...display.webp`，同一对象存在 `.thumb.webp`；页面渲染可见证书详情 | 证书详情分享链路当前样本使用 display 图，可作为商品详情异常的对照样本 |
| 用户补证截图：2026-08-25 08:00 左右 首页 Network | 小程序 DevTools Network | `tile-placeholder.png` 先 307 Redirect，随后 500 `text/plain`；请求路径映射到 `__pageframe__/assets/tile-placeholder.png` | 首页 fallback 指向不存在的本地占位图，缺图/加载失败状态仍会产生无效请求 |
| `src/miniapp/assets/` | 文件清单 | 本地资源目录只有 `logos/` 与 `tabbar/`，不存在 `tile-placeholder.png` | 资源缺失与 Network 500 对应 |
| `issues/bugs/archive/BUG-0137-miniapp-lightweight-image-variant-consumption/bug.md` | 缺陷描述 | 正式 BUG 要求 Banner、品牌 Logo、分享图统一轻量图字段并禁止普通展示冷加载原图 | 修复与验收基线已明确 |

## 修复后补证步骤

1. 修复后使用脱敏测试数据准备首页 Banner、品牌列表 Banner、品牌 Logo、商品详情分享图、证书详情分享图各 1 条样本。
2. 在微信小程序 DevTools 禁用缓存后分别打开首页、品牌列表、品牌详情、商品详情和证书详情。
3. 记录 Network evidence：页面路径、媒体 URL 类型、请求域名、HTTP 状态、资源大小、耗时、是否命中缓存和 render 结果。
4. 确认普通展示只请求 `thumbnail_url` / `thumb_url` / `display_url`；缺轻量图时展示视图占位、品牌首字、已有稳定默认图或失败态，不得回退到原图，也不得请求不存在的本地占位图。
5. 分享图如平台要求高清图，必须明确记录为分享入口例外，并证明该例外不影响普通展示冷加载。
6. 将截图、录屏或人工摘要回填到 `acceptance.md` 的四联验收和验收结果回填区域。

## 验证方式

- 修复前：通过代码定位和小程序 Network evidence 证明 Banner、品牌 Logo、分享图至少一个入口存在原图或旧字段 fallback。
- 修复后：通过后端测试、静态测试和小程序 Network/render evidence 证明三类入口均消费轻量图字段；缺轻量图时展示占位或失败态，不请求原图。
