---
bug_id: BUG-0126-miniapp-brand-media-slow-load
created_at: 2026-08-10 23:08:03
updated_at: 2026-08-10 23:08:03
severity: high
related_requirement:
related_bug: BUG-0110-miniapp-card-banner-thumbnail-usage
---

# 根因分析

## 直接原因

微信小程序品牌链路的图片展示虽然已经倾向使用 `.thumb` 缩略图 URL，但性能收益依赖以下条件同时成立：

1. `.thumb` 对象真实存在。
2. `.thumb` 对象体积和像素尺寸明显小于原图。
3. 端侧非首屏图片启用懒加载。
4. `/media/{object_key}` 在生产环境具备可复用缓存或 CDN 能力。

当前探索阶段发现这些条件尚未形成闭环，因此可能出现图片能显示但加载慢的情况。

## 根本原因

本缺陷属于媒体性能治理覆盖不足，具体表现为：

- 缩略图 URL 与真实轻量对象之间缺少强验收：后端可返回同目录 `.thumb` URL，但媒体读取链路在 `.thumb` 缺失时会自动回退同目录原图。该策略能避免破图，却会隐藏“缩略图未命中、实际下载原图”的性能退化。
- 缩略图体积目标未固化：系统配置 `media.thumbnail_max_size_kb` 默认可能为 `0`，表示生成缩略图时不强制目标体积上限；历史对象即使存在 `.thumb`，也可能仍然偏大。
- 品牌链路端侧加载策略未完整覆盖：商品卡片组件已支持 `lazy-load`，但品牌列表 Banner、品牌列表 Logo、品牌详情 Logo、品牌详情证书图片的小程序懒加载和首屏/非首屏分层仍需补齐。
- 生产媒体读取链路可能未充分缓存：`/media/{object_key}` 是后端受控读取对象存储的代理路径；若无 CDN 或反向代理缓存，多图页面首屏会反复穿透后端和对象存储。

## 触发条件

- 访问小程序品牌列表页时，页面同时加载品牌 Banner 与多条品牌 Logo。
- 从品牌列表页进入品牌分类商品列表页时，商品卡片图较多且缩略图缺失、过大或回退原图。
- 访问品牌详情页时，顶部品牌 Logo、商品卡片图或证书图片需要加载。
- 网络处于弱网、移动网络、跨地域对象存储访问或对象存储响应慢的环境。
- 历史品牌 Logo、Banner、SKU 主图或证书图片未完成缩略图回填、重生成或 CDN 缓存预热。

## 分类

- 类型：media-performance / miniapp-render / object-storage
- 层级：小程序端渲染 + 后端媒体代理 + 对象存储对象治理
- 回归关系：与 `BUG-0110-miniapp-card-banner-thumbnail-usage` 相关，属于小程序媒体缩略图治理在品牌链路实际性能验收上的延伸问题。

## 待验证项

- 抽样确认品牌 Logo、品牌列表 Banner、证书图片和品牌过滤商品卡片主图的 `.thumb` 对象是否存在。
- 对比原图与 `.thumb` 的字节数、像素尺寸和 MIME，确认缩略图收益。
- 通过后端 `media_read` 日志确认 `.thumb` 请求是否实际 resolved 到原图。
- 通过微信 DevTools、真机或体验版 Network 记录图片耗时、资源大小和页面可见等待。
- 确认生产网关、Nginx 或 CDN 是否缓存 `/media/` 图片响应。
