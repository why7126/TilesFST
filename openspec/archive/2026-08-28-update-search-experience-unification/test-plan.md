---
change_id: update-search-experience-unification
source_requirement: REQ-0128-search-experience-unification
source_sprint: sprint-026
created_at: 2026-08-27 00:19:59
updated_at: 2026-08-28 15:10:59
---

# 测试计划

## OpenSpec 与治理校验

- `python scripts/validate-openspec-language.py`
- `openspec validate update-search-experience-unification --strict`
- `python scripts/validate-product-data-observability-gates.py --change update-search-experience-unification`
- `python scripts/sync-workflow-status.py --event req.opsx --req REQ-0128-search-experience-unification --change update-search-experience-unification --sprint auto`
- `python scripts/sync-workflow-status.py --event opsx.apply --change update-search-experience-unification --sprint auto --dry-run`
- `python scripts/validate-sprint-scope.py sprint-026 --item REQ-0128-search-experience-unification --item update-search-experience-unification`

## 小程序测试

- 覆盖首页搜索入口点击进入 `/pages/search/index`，并携带 `sourcePage`、`scope` 和初始关键词。
- 覆盖品牌、证书、商品列表、收藏页面的搜索入口或搜索路径；覆盖全部分类页不展示搜索入口。
- 覆盖品牌列表页按品牌名称、品牌简称和品牌英文名在当前页过滤，搜索结果保持品牌卡片布局，搜索态隐藏 Banner，清空后恢复完整列表和 Banner。
- 覆盖证书列表页按证书名称、品牌名称、证书类型枚举或中文类型标签在当前页过滤，搜索结果保持证书卡片布局，清空后恢复完整证书列表。
- 覆盖收藏列表页只在当前收藏范围内搜索，搜索结果保持收藏卡片布局，空态不展示显著的全局搜索调整主按钮。
- 覆盖搜索页首页、联想、提交、结果、无结果、加载、错误和联想失败降级。
- 覆盖首页带关键词进入搜索页时不额外请求 `/api/v1/miniapp/search/home`，清空关键词回到搜索首页时再加载搜索首页数据。
- 覆盖搜索结果页品牌卡片展示品牌图片、品牌名称和 `x 个 SKU`，不出现“公开 SKU”文案。
- 覆盖搜索结果页证书卡片展示证书图片、证书名称、品牌和证书类型。
- 覆盖搜索结果页 `onReachBottom` 自动加载更多，并避免 loading 中重复加载。
- 覆盖综合 Tab 内容流顺序为最佳匹配、品牌、证书、SKU，且顶部 Tab 顺序保持综合、品牌、SKU、证书。
- 覆盖综合 Tab 后续页按分区合并：品牌 / 证书首屏固定，SKU 分区追加新结果，不用后续页覆盖已展示分区。
- 覆盖自动加载下一页时保留已展示结果，仅显示底部轻量加载状态，并移除黄色“加载更多”主按钮。
- 覆盖列表内搜索空态能说明当前范围，并能调整关键词或进入全局搜索。
- 覆盖 `.ts` 与 `.js` 运行入口一致。
- 覆盖 320、375、430 pt 或等价微信开发者工具视口下无遮挡。

## 管理端测试

- 覆盖品牌、类目、SKU、规格、Banner、证书、用户、日志中的代表性列表搜索输入、筛选变化、重置和分页回到第一页。
- 覆盖后端真实 total 展示、空态、错误态和权限边界。
- 覆盖 `page-summary`、`page-right`、fixed toast、DS confirm、nowrap、sticky 操作列等 admin-list 横切 gate。
- API contract 变化时运行后端测试、前端测试、OpenAPI 导出和 Orval 生成。

## 后端与观测测试

- 覆盖新增或调整查询参数的长度限制、枚举、分页、权限过滤和错误响应。
- 覆盖 `/api/v1/miniapp/certificates?keyword=...` 只匹配公开证书的证书名称、品牌名称、证书类型枚举或中文类型标签。
- 覆盖综合 Tab 与 SKU Tab 后续页的 SKU-only 轻量响应：跳过品牌、证书、facets、推荐词和最佳匹配。
- 覆盖搜索 SKU 查询不依赖逐商品 `usage_events.metadata LIKE` 热度计算。
- 覆盖 `/api/v1/miniapp/search` 首屏不通过 `get_search_home()` 生成推荐词，并避免触发 `hot_score metadata LIKE` 分支。
- 覆盖 `/api/v1/miniapp/search` 首屏不触发 facets 聚合、类目 named 和规格 named 查询；品牌/证书/SKU 单独 Tab 只触发本 Tab 必要查询。
- 覆盖 `/api/v1/miniapp/search` 品牌关键词精确命中时，SKU 查询使用 `brand_id` 快路径，并通过测试钩子确认不走全字段 SKU `OR LIKE` 主路径。
- 覆盖 `/api/v1/miniapp/search` 返回 `Server-Timing` 分段耗时响应头，且该头只包含阶段名和毫秒数。
- 覆盖小程序首页新品/热销、商品列表、搜索首页最近浏览/热门商品、完整搜索结果和 SKU 详情推荐等列表型 SKU 卡片构建不逐卡片调用对象存储存在性探测。
- 覆盖搜索相关 request logs 的 `behavior_trace_id`、`parent_behavior_event_id`、`client_request_id`、脱敏 query 摘要、结果数量和耗时字段。
- 覆盖 usage events 事件字典允许稳定搜索事件名，并拒绝未知事件和禁止属性。
- 覆盖关键词原文、Authorization、Cookie、Token、密码、完整 payload、本机路径和完整对象 key 不进入日志或事件属性。
- 普通搜索 Task Trace N/A；复杂查询若接入则补充 Task Trace 测试。

## 本次执行结果

| 命令 | 结果 |
|---|---|
| `uv run pytest tests/test_miniapp_static.py` | 通过，38 passed |
| `./node_modules/.bin/vitest run src/pages/admin/LogAuditPage.test.tsx` | 通过，1 file / 17 tests |
| `python scripts/validate-product-data-observability-gates.py --change update-search-experience-unification` | 通过 |
| `python scripts/validate-openspec-language.py` | 通过 |
| `openspec validate update-search-experience-unification --strict` | 通过 |
| `python scripts/sync-workflow-status.py --event opsx.apply --change update-search-experience-unification --sprint auto --dry-run` | 通过，Sprint `sprint-026`，Errors 0 |

## 验收返修执行结果

| 命令 | 结果 |
|---|---|
| `uv run pytest tests/test_miniapp_static.py tests/test_miniapp_home.py` | 通过，82 passed |
| `uv run pytest src/backend/tests/test_product_usage_logging.py tests/test_miniapp_home.py::test_miniapp_search_usage_events_validate_dictionary_and_forbidden_properties tests/test_miniapp_home.py::test_miniapp_track_literal_events_are_registered_in_backend_dictionary` | 通过，27 passed |
| `./node_modules/.bin/vitest run src/pages/admin/LogAuditPage.test.tsx` | 通过，1 file / 17 tests |
| `git diff --check -- <返修相关源码与文档>` | 通过 |
| `openspec validate update-search-experience-unification --strict` | 通过 |
| `python scripts/validate-product-data-observability-gates.py --change update-search-experience-unification` | 通过 |
| `python scripts/validate-openspec-language.py` | 通过 |
| `uv run pytest tests/test_miniapp_static.py tests/test_miniapp_home.py::test_miniapp_full_search_returns_tabs_facets_certificates_and_public_filter tests/test_miniapp_home.py::test_miniapp_search_best_match_supports_exact_brand_match tests/test_miniapp_home.py::test_miniapp_search_load_more_returns_sku_only_payload tests/test_miniapp_home.py::test_miniapp_search_best_match_prefers_sku_then_certificate_match` | 通过，42 passed |
| `uv run pytest tests/test_miniapp_static.py tests/test_miniapp_home.py` | 通过，83 passed |
| `python scripts/validate-root-cause-evidence.py --change update-search-experience-unification` | 通过，blockers=0，warnings=0 |
| `python scripts/sync-workflow-status.py --event opsx.modify --change update-search-experience-unification --sprint auto` | 通过，Sprint `sprint-026`，Updated 1，Errors 0 |
| `python scripts/extract-ai-usage.py --post-command-hook --workflow-event opsx.modify --change update-search-experience-unification --sprint sprint-026 --json` | 通过，`usage_mode=actual`，`command_run_count=1`，Sprint snapshot refreshed，warnings=0 |
| `uv run pytest tests/test_miniapp_static.py tests/test_miniapp_home.py` | 通过，83 passed，覆盖自动加载下一页不以整页 loading 覆盖结果、移除黄色“加载更多”按钮、底部 loadingMore 状态、SKU-only 翻页响应和小程序搜索相关回归。 |
| `uv run pytest tests/test_miniapp_static.py tests/test_miniapp_home.py::test_miniapp_search_load_more_returns_sku_only_payload` | 通过，39 passed，覆盖综合 Tab 内容流顺序、顶部 Tab 顺序不变、后续页 SKU-only 追加和小程序静态契约回归。 |
| `uv run pytest tests/test_miniapp_static.py` | 通过，38 passed，覆盖全部分类页不展示 `search-entry`、不注册搜索组件、不保留 `openSearch` / `navigateToSearch`，并确认分类双栏与进入商品列表路径回归。 |
| `uv run pytest tests/test_miniapp_static.py::test_miniapp_search_entry_unification_contracts tests/test_miniapp_static.py::test_miniapp_brand_list_page_covers_carousel_grid_entry_and_tracking tests/test_miniapp_home.py::test_miniapp_brand_list_returns_public_brands_and_brand_list_carousel` | 通过，3 passed，覆盖品牌列表页输入模式搜索、不跳完整搜索结果页、搜索态隐藏 Banner、`/api/v1/miniapp/brands?keyword=...` 按品牌字段过滤、OpenAPI/Orval 参数同步。 |
| `uv run pytest tests/test_miniapp_static.py::test_miniapp_brand_list_page_covers_carousel_grid_entry_and_tracking tests/test_miniapp_home.py::test_miniapp_brand_list_usage_events_validate_dictionary_and_forbidden_properties` | 通过，2 passed，覆盖品牌列表页搜索埋点在请求成功后上报 `resultCount` 和 `requestId`，并确认 `list_search_submit` / `list_search_reset` 满足 usage event 字典必填字段。 |
| `uv run pytest tests/test_miniapp_static.py::test_miniapp_search_entry_unification_contracts tests/test_miniapp_static.py::test_miniapp_certificate_list_page_replaces_placeholder_with_public_list tests/test_miniapp_static.py::test_miniapp_favorite_list_page_uses_local_storage_and_states tests/test_miniapp_home.py::test_miniapp_certificate_list_filters_public_data_and_supports_facets tests/test_miniapp_home.py::test_miniapp_certificate_detail_load_failed_usage_event_is_accepted tests/test_miniapp_home.py::test_miniapp_contract_drift_usage_events_are_registered_and_persisted` | 通过，6 passed，覆盖证书列表页输入模式当前页过滤、`/api/v1/miniapp/certificates?keyword=...`、收藏页移除全局搜索调整入口，以及两页 `list_search_submit/reset` 必填字段。 |
| `bash scripts/generate-openapi-client.sh` | 通过，已同步 `/api/v1/miniapp/certificates` 的 `keyword` 查询参数到 `src/web/openapi.json` 与 `src/web/src/shared/api/generated.ts`。 |
| `uv run pytest tests/test_miniapp_static.py::test_miniapp_search_matches_req0046_prototype_structure tests/test_miniapp_home.py::test_miniapp_search_first_page_skips_search_home_hot_score_branch tests/test_miniapp_home.py::test_miniapp_search_load_more_returns_sku_only_payload` | 通过，3 passed，覆盖首页带关键词进入搜索页跳过搜索首页、后端搜索首屏不触发 `hot_score metadata LIKE` 分支和综合 Tab SKU-only 翻页回归。 |
| `uv run pytest tests/test_miniapp_static.py tests/test_miniapp_home.py` | 通过，84 passed，覆盖小程序搜索页、首页入口、品牌/证书/收藏列表搜索、完整搜索首屏性能分支和相关后端接口回归。 |
| `uv run pytest tests/test_miniapp_home.py::test_miniapp_search_exact_brand_uses_brand_id_fast_path tests/test_miniapp_home.py::test_miniapp_search_product_filters_brand_fast_path_skips_keyword_like` | 通过，2 passed，覆盖品牌词搜索 SKU `brand_id` 快路径、全字段 SKU `OR LIKE` 主路径回避、`Server-Timing` 分段耗时响应头和搜索卡片构建不探测对象存储。 |
| `uv run pytest tests/test_miniapp_home.py::test_miniapp_search_product_filters_brand_fast_path_skips_keyword_like tests/test_miniapp_home.py::test_miniapp_search_exact_brand_uses_brand_id_fast_path tests/test_miniapp_home.py::test_miniapp_search_first_page_skips_search_home_hot_score_branch tests/test_miniapp_home.py::test_miniapp_search_single_tabs_only_run_required_queries` | 通过，4 passed，覆盖品牌词搜索 SKU `brand_id` 快路径、全字段 SKU `OR LIKE` 主路径回避、搜索首屏不触发搜索首页和单独 Tab 最小查询集合。 |
| `uv run pytest tests/test_miniapp_static.py tests/test_miniapp_home.py` | 通过，87 passed，覆盖小程序搜索页、首页入口、品牌/证书/收藏列表搜索、搜索首屏性能分支、品牌词 SKU `brand_id` 快路径和相关后端接口回归。 |
| `uv run pytest tests/test_miniapp_static.py tests/test_miniapp_home.py` | 通过，87 passed，覆盖搜索接口 `Server-Timing` 响应头不破坏既有小程序搜索 JSON 契约。 |
| `uv run pytest tests/test_miniapp_static.py tests/test_miniapp_home.py` | 通过，87 passed，覆盖搜索结果 SKU 卡片跳过同步对象存储探测后，小程序搜索、首页、详情、品牌和证书相关接口不回归。 |
| `uv run pytest tests/test_miniapp_home.py::test_miniapp_list_product_cards_skip_media_existence_probe tests/test_miniapp_home.py::test_miniapp_home_and_detail_recommendation_cards_use_lightweight_media_path tests/test_miniapp_home.py::test_miniapp_search_exact_brand_uses_brand_id_fast_path` | 通过，3 passed，覆盖商品列表、搜索首页、首页商品卡片和 SKU 详情推荐等列表型 SKU 卡片不触发对象存储存在性探测，同时保留详情主媒体存在性探测路径。 |
| `uv run pytest tests/test_miniapp_static.py tests/test_miniapp_home.py` | 通过，89 passed，覆盖小程序静态契约、首页商品卡片、商品列表、搜索首页、搜索结果和 SKU 详情推荐等列表型 SKU 卡片轻量媒体路径完整回归。 |
| `git diff --check -- <返修相关源码与文档>` | 通过 |
| `openspec validate update-search-experience-unification --strict` | 通过 |
| `python scripts/validate-product-data-observability-gates.py --change update-search-experience-unification` | 通过 |
| `python scripts/validate-openspec-language.py` | 通过 |
| `python scripts/validate-root-cause-evidence.py --change update-search-experience-unification` | 通过，blockers=0，warnings=0 |

## N/A 说明

- 后端查询参数：本次已新增 `/api/v1/miniapp/brands` 可选 `keyword` 参数，长度限制 80，仅匹配品牌名称、品牌简称和品牌英文名；搜索态响应 `banners=[]`。本次返修新增 `/api/v1/miniapp/certificates` 可选 `keyword` 参数，长度限制 80，仅匹配证书名称、品牌名称、证书类型枚举和中文类型标签。
- OpenAPI / Orval：已运行 `bash scripts/generate-openapi-client.sh` 同步 `src/web/openapi.json` 与 `src/web/src/shared/api/generated.ts`。
- 数据库：未新增检索字段、索引、表结构或迁移，N/A。
- Task Trace：本次为普通搜索与列表筛选交互，无长耗时异步任务，N/A。
