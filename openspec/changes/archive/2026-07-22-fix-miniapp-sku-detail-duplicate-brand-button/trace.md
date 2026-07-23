---
change_id: fix-miniapp-sku-detail-duplicate-brand-button
status: proposed
created_at: 2026-07-21 08:35:43
updated_at: 2026-07-21 22:54:39
source: bug
source_bug: BUG-0070-miniapp-sku-detail-duplicate-brand-button
related_requirement: REQ-0044-miniapp-sku-detail-page
iteration: sprint-010
capabilities:
  - miniapp-sku-detail-page
---

# Trace - fix-miniapp-sku-detail-duplicate-brand-button

## 来源

| 类型 | ID | 说明 |
|---|---|---|
| BUG | `BUG-0070-miniapp-sku-detail-duplicate-brand-button` | 小程序商品详情页底部品牌按钮与内容区查看品牌主页重复 |
| REQ | `REQ-0044-miniapp-sku-detail-page` | 微信小程序 SKU 商品详情页 |
| Capability | `miniapp-sku-detail-page` | SKU 详情页品牌入口与底部操作栏规范 |

## Bug Analysis Report

| 项 | 内容 |
|---|---|
| 现象 | SKU 商品详情页内容区已有“查看品牌主页”入口，底部操作区仍显示品牌按钮 |
| 复现 | 进入任意 SKU 商品详情页，查看内容区品牌入口与底部固定操作栏 |
| 影响 | 品牌主页入口重复、底部操作区冗余、用户可能误以为两个入口职责不同 |
| 根因分类 | design / ux |
| 严重等级 | medium |
| Hotfix | 不需要 |

## 状态记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-21 22:54:39 | /opsx-apply | 删除小程序 SKU 详情页底部重复品牌按钮，保留内容区品牌卡入口；相关静态回归通过 |
| 2026-07-21 09:15:27 | /sprint-propose | 纳入 sprint-010 正式范围 |
| 2026-07-21 08:35:43 | /bug-opsx | 创建修复 Change，状态 proposed |

## 实现与验收证据

| 项 | 证据 |
|---|---|
| 底部品牌按钮 | `src/miniapp/pages/tile-detail/index.wxml` 已移除底部 `openBrand` 按钮；`index.ts` / `index.js` 已移除仅服务于底部按钮的跳转、埋点与导航锁状态 |
| 内容区品牌入口 | `src/miniapp/pages/tile-detail/index.wxml` 保留 `<brand-card>`，并继续传入 `hint="查看品牌主页"`、`source-module="sku-detail-brand"` 与 `sku-id` |
| 底部布局 | `src/miniapp/pages/tile-detail/index.wxss` 将底部操作栏调整为收藏 + 分享两列，无第三列空白占位 |
| 静态回归 | `uv run pytest tests/test_miniapp_static.py::test_miniapp_home_detail_search_smoke_contracts tests/test_miniapp_static.py::test_miniapp_global_custom_navigation_covers_subpages_and_back_fallback tests/test_miniapp_static.py::test_miniapp_sku_detail_page_covers_media_favorite_share_and_empty_states tests/test_miniapp_static.py::test_miniapp_brand_card_component_contract_and_states` 通过 |
| API / DB / Orval | 本次仅移除小程序前端重复按钮，不修改 API 契约或数据库结构，不需要 OpenAPI / Orval |
| 知识库 | 本缺陷为单页面重复入口收敛，无跨模块复用事故模式，本次不新增 `docs/knowledge-base/incidents/` |
