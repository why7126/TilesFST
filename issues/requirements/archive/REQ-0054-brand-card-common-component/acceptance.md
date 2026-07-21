---
requirement_id: REQ-0054-brand-card-common-component
title: 微信小程序品牌卡片组件验收清单
status: done
created_at: 2026-07-19 17:45:31
updated_at: 2026-07-19 21:10:48
owner: product
source: requirement.md
---

# 微信小程序品牌卡片组件验收清单

## 功能 AC

- [ ] AC-001 品牌卡片作为微信小程序可复用组件沉淀，SKU 详情页不再保留重复的内联品牌卡片结构。
- [ ] AC-002 组件接收单个品牌展示对象，不在组件内部直接请求品牌列表、SKU 列表或品牌详情接口。
- [ ] AC-003 卡片展示品牌 Logo、品牌名称和入口提示；副文案缺失时按统一策略隐藏或展示兜底，不出现空字符串、`null`、`undefined`。
- [ ] AC-004 品牌名称长文本在 320px 小屏宽度下不撑破卡片，最多按设计策略截断或换行。
- [ ] AC-005 Logo 区域使用稳定尺寸容器，图片加载前后卡片高度不跳动。
- [ ] AC-006 Logo 缺失或加载失败时展示品牌首字、默认图片或统一深色占位，不出现破图。
- [ ] AC-007 图片异常时卡片仍保持品牌名称和入口提示可读，且不影响 SKU 详情页其他模块。
- [ ] AC-008 整个品牌卡片可点击，触控区域不小于 44px，并提供小程序触控反馈。
- [ ] AC-009 当存在 `brand_entry_path` 时，点击卡片优先跳转到该入口。
- [ ] AC-010 当 `brand_entry_path` 缺失但品牌名称可用时，点击卡片 fallback 到品牌关键词搜索页，且品牌名称经过 URL 编码。
- [ ] AC-011 当品牌数据缺失、品牌名称不可用或入口不可用时，卡片阻止无效跳转，并提示“品牌内容暂不可查看”或等价文案。
- [ ] AC-012 连续快速点击品牌卡片不会重复打开多个页面或重复触发多次跳转。
- [ ] AC-013 品牌卡片点击埋点包含 `brandId`、`brandName`、`sourcePage`、`sourceModule`、`skuId` 等可用上下文。
- [ ] AC-014 Logo 加载失败时记录 `brand_card_image_failed` 或等价异常事件。
- [ ] AC-015 不可用状态被点击时记录 `brand_card_unavailable_click` 或等价事件。
- [ ] AC-016 组件参数预留后续品牌商品列表、同品牌推荐、首页品牌推荐的来源上下文，但首版不实现这些页面容器。
- [ ] AC-017 首版不新增品牌 API、数据库字段、Logo 上传链路、MinIO 策略或管理端品牌维护操作。
- [ ] AC-018 微信开发者工具或真机截图覆盖 320/375/430 pt 宽度，卡片 Logo、文字、入口提示不重叠、不遮挡、不溢出。
- [ ] AC-019 新增小程序组件后同步运行入口策略，确保微信开发者工具实际加载的 `.js` 与源 `.ts` 逻辑一致或存在项目认可的构建同步说明。

## Prototype AC

- [ ] AC-020 `prototype/miniapp/brand-card-component.html` 提供品牌卡片正常态、Logo 缺失态、长品牌名态和不可用态的静态预览。
- [ ] AC-021 `prototype/miniapp/brand-card-component-context.md` 说明字段、状态、跳转和移动端验收策略。
- [ ] AC-022 PNG Golden Reference 可在后续 `/req-complete` refinement 或 OpenSpec 设计阶段补齐；缺 PNG 不阻塞本需求进入评审。

## 横切 AC（knowledge-base）

本 REQ 不命中 `admin-list`、`admin-form`、`admin-modal`、`media-upload` 标签；品牌 Logo 仅展示与 fallback，不涉及上传链路。因此无 AC-XCUT 写入，Knowledge-base gate 为 N/A。

