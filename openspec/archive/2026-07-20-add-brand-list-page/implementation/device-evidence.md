---
change_id: add-brand-list-page
source_requirement: REQ-0060-brand-list-page
status: archived
created_at: 2026-07-20 23:23:22
updated_at: 2026-07-20 23:23:22
---

# 品牌列表页实现与设备 Evidence

## 实现摘要

- 小程序已注册 `pages/brand-list/index`，TabBar 第 3 项为“品牌”，首页快捷入口进入品牌列表页。
- 品牌列表页使用 `GET /api/v1/miniapp/brands?page=...&pageSize=...`；OpenAPI、API 文档与后端测试已覆盖公开品牌列表、安全字段过滤、品牌列表页轮播和分页回归。
- 页面使用自定义导航 `custom-navigation`，主体保留底部 `env(safe-area-inset-bottom)` 与 TabBar padding。
- 品牌轮播固定高度 `300rpx`，双列品牌网格使用 `repeat(2, minmax(0, 1fr))`，品牌卡片 grid 态固定 `min-height: 244rpx`，品牌名与辅助文案均限制两行，避免 320/375/430 pt 宽度下横向滚动或文字溢出。
- 加载、空态、错误态和加载更多错误态均在 `pages/brand-list/index.wxml` 中有独立分支。

## 静态测试 Evidence

```yaml
target: add-brand-list-page
page_path: pages/brand-list/index
source: static_test
status: passed
artifact_ref:
  - tests/test_miniapp_static.py::test_miniapp_brand_list_page_covers_carousel_grid_entry_and_tracking
  - tests/test_miniapp_global_custom_navigation_covers_subpages_and_back_fallback
  - tests/test_miniapp_home_detail_search_smoke_contracts
conclusion:
  route_and_tabbar_entry: pass
  custom_navigation: pass
  carousel_framing_contract: pass
  two_column_grid_contract: pass
  tabbar_bottom_padding: pass
  loading_empty_error_states: pass
  analytics_privacy_fields: pass
remaining_risk: 当前执行环境未提供微信开发者工具预览能力；本记录为仓库可复核静态 evidence，不表述为 DevTools 截图或真机通过。
```

## 视口 Evidence

```yaml
target: add-brand-list-page
page_path: pages/brand-list/index
viewport: 320pt
source: static_layout_review
status: recorded_static_pass
artifact_ref: tests/test_miniapp_static.py::test_miniapp_brand_list_page_covers_carousel_grid_entry_and_tracking
conclusion:
  carousel_framing: pass
  two_column_cards: pass
  tabbar_overlap: pass
  loading_state: pass
  empty_state: pass
  error_state: pass
remaining_risk: 未运行微信开发者工具截图；如需视觉截图，后续人工用 DevTools 补录。
```

```yaml
target: add-brand-list-page
page_path: pages/brand-list/index
viewport: 375pt
source: static_layout_review
status: recorded_static_pass
artifact_ref: tests/test_miniapp_static.py::test_miniapp_brand_list_page_covers_carousel_grid_entry_and_tracking
conclusion:
  carousel_framing: pass
  two_column_cards: pass
  tabbar_overlap: pass
  loading_state: pass
  empty_state: pass
  error_state: pass
remaining_risk: 未运行微信开发者工具截图；如需视觉截图，后续人工用 DevTools 补录。
```

```yaml
target: add-brand-list-page
page_path: pages/brand-list/index
viewport: 430pt
source: static_layout_review
status: recorded_static_pass
artifact_ref: tests/test_miniapp_static.py::test_miniapp_brand_list_page_covers_carousel_grid_entry_and_tracking
conclusion:
  carousel_framing: pass
  two_column_cards: pass
  tabbar_overlap: pass
  loading_state: pass
  empty_state: pass
  error_state: pass
remaining_risk: 未运行微信开发者工具截图；如需视觉截图，后续人工用 DevTools 补录。
```

## 真机 Evidence

```yaml
target: add-brand-list-page
page_path: pages/brand-list/index
source: real_device
status: follow_up
artifact_ref: manual-summary
conclusion:
  status_bar: follow_up
  capsule_reserve: follow_up
  tabbar_overlap: follow_up
remaining_risk: 当前记录未包含设备型号、系统类型、微信版本或截图；不得写作真机通过。
```

## API / DB / Orval

```yaml
api: updated
database: not_applicable
orval: updated_or_existing_generated_client
api_docs: updated
backend_tests: passed_targeted
evidence:
  - src/web/openapi.json includes GET /api/v1/miniapp/brands
  - docs/03-api-index.md documents GET /api/v1/miniapp/brands
  - tests/test_miniapp_home.py covers brand list response, safe media URL and field filtering
```
