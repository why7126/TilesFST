---
note: workflow-sync — 16/16 Change 已 archive；0 applied；待人工 sign-off
title: sprint-026 验收报告
acceptance_status: passed
created_at: 2026-08-25 15:21:18
updated_at: 2026-08-28 16:21:48
---

# sprint-026 验收报告

## 验收范围

| 类型 | 编号 | 标题 | 验收状态 | 说明 |
|---|---|---|---|---|
| BUG | BUG-0141-ai-usage-token-count-jsonl | AI usage extractor 未识别新版 token_count JSONL 导致 Sprint snapshot 缺失 | done，已归档（`fix-ai-usage-message-content-token-count` archived 2026-08-25 15:13:14） | Change 已归档，AI usage snapshot actual 恢复 |
| BUG | BUG-0140-admin-current-user-avatar-missing-object | 当前登录用户头像引用缺失媒体对象 | done，已归档（`fix-admin-current-user-avatar-object-consistency` archived 2026-08-25 15:44:17） | Change 已归档，媒体四联验收通过 |
| BUG | BUG-0139-admin-avatar-upload-nginx-redirect-cors | 管理后台头像上传被 Nginx 301 重定向丢端口导致 CORS 拦截 | done，已归档（`fix-admin-avatar-upload-nginx-redirect-cors` archived 2026-08-25 15:35:15） | 修复 Change 已归档 |
| REQ | REQ-0123-upload-stage-trace-spans | 上传链路阶段级耗时写入 trace spans | done，已归档（`add-upload-stage-trace-spans` archived 2026-08-25 19:16:00） | OpenSpec Change 已归档 |
| REQ | REQ-0124-log-audit-behavior-trace-model | 日志审计补齐行为链路与任务链路采集模型 | done，已归档（`add-log-audit-behavior-trace-model` archived 2026-08-27 23:10:25） | 后端、DB、Web、API 文档、Orval 与聚焦测试已完成 |
| REQ | REQ-0126-product-data-collection-observability-standard | 建立通用产品数据采集与链路观测规范 | done，已归档（`add-product-data-collection-observability-standard` archived 2026-08-26 19:36:50） | OpenSpec Change 已归档 |
| REQ | REQ-0127-product-data-collection-observability-hard-gate | 产品数据采集与链路观测规范硬门禁 | done，已归档（`add-product-data-collection-observability-hard-gate` archived 2026-08-27 23:14:21） | AGENTS、rules、req/opsx/sprint 技能与实现级门禁校验脚本已完成 |
| REQ | REQ-0129-miniapp-sku-detail-actionbar-compact-favorite | 小程序商品详情页底部收藏按钮与操作栏紧凑化 | done，已归档（`update-miniapp-sku-detail-actionbar-compact-favorite` archived 2026-08-28 14:27:38） | OpenSpec Change 已归档 |

## 验收门禁

- 新版 `payload.type=message`、`payload.role=user`、`payload.content` 文本片段列表可建立 command run。
- `payload.type=token_count` 且 token 用量位于 `payload.info.last_token_usage` 时，可归属到对应 command run。
- `sprint-025` snapshot 不再因 `required-metrics-empty` 失败。
- 脱敏与隐私边界通过：不持久化 prompt 原文、系统/开发者指令、工具输出正文、本机绝对路径、Authorization header、Cookie、`.env` 内容或密钥。
- BUG-0140 按媒体四联验收：头像 `object_key` 可追溯、对象存在、`/media/{object_key}` 可读、管理端头像 render/fallback 正常。
- BUG-0139 按 Docker Web 上传边界验收：`POST /api/v1/admin/uploads` 不再 301，端口不丢失，CORS 不再拦截，头像上传状态机与即时回显正常。
- REQ-0123 按上传 trace spans 验收：`file_read`、`original_put_object`、`thumbnail_generate`、`thumbnail_put_object`、`display_generate`、`display_put_object` 六阶段可追踪，日志不作为唯一事实源。
- REQ-0124 按链路采集模型验收：界面触发入口可从 `behavior_trace_id` 联动行为、请求、任务和流程节点；直接 API 调用在行为链路为空时仍可从 `request_id` 追踪任务链路；日志审计页按 `behavior_trace_id`、`request_id`、`task_trace_id` 查询并保持 admin-list 横切验收。
- REQ-0126 按通用采集与链路观测规范验收：覆盖小程序、店主端、App、Web 管理端和后端 API，明确业务行为事件、所有业务 API 请求日志、四层链路模型、直接 API 入口、标准数据结构、Task Trace 分级覆盖、默认保留周期、禁止采集字段和新产品接入 checklist。
- REQ-0127 按采集规范硬门禁验收：入口、规则、req/opsx/sprint 技能和实现级校验脚本均引用 `docs/standards/product-data-collection-observability.md`；触发范围内材料要求声明 `product_data_collection_observability`、affected layers、N/A 原因和 validation 摘要。
- REQ-0129 按小程序商品详情页操作栏紧凑化验收：收藏按钮无可见第二行“收藏 / 已收藏”文字，收藏状态仍可通过心形状态和 toast 反馈识别，底部操作栏高度压缩，返回首页悬浮按钮 actionbar offset 与安全区避让通过 320/375/430pt 视觉证据确认；实现 diff 确认不修改收藏 API、DB、请求封装或行为事件。
- REQ-0128 搜索结果页验收返修：品牌卡片展示品牌图片或稳定占位、品牌名称和 `x 个 SKU`；证书卡片展示证书图片或稳定占位、证书名称、品牌和证书类型；搜索结果页下滑自动加载更多，并继续保留手动加载兜底。
- REQ-0128 搜索结果页二次返修：综合 Tab 采用“品牌 / 证书首屏固定，SKU 无限追加”的 MVP；后续页按分区合并，不覆盖已展示结果；搜索接口后续页返回 SKU-only 轻量响应，并取消搜索 SKU 逐商品 `usage_events.metadata LIKE` 热度计算。
- REQ-0128 搜索结果页三次返修：自动加载下一页时不再切换为整页“加载中...”空白态，结果列表保持可见，仅在底部显示轻量加载或完成状态；移除黄色“加载更多”主按钮。
- REQ-0128 搜索结果页四次返修：综合 Tab 内容流顺序调整为最佳匹配、品牌、证书、SKU；顶部 Tab 顺序保持综合、品牌、SKU、证书，后续页仍只向 SKU 分区追加。
- REQ-0128 分类列表页范围澄清返修：底部 Tab「全部分类」页不展示搜索入口，保持一级 / 二级分类双栏浏览；用户进入商品列表后再承接列表上下文搜索。
- REQ-0128 品牌列表页范围澄清返修：品牌列表页搜索改为当前页品牌字段过滤，支持品牌名称、品牌简称和品牌英文名；搜索结果保持品牌列表卡片布局，搜索态隐藏 Banner，清空后恢复完整品牌列表和 Banner。
- REQ-0128 品牌列表页搜索埋点返修：`list_search_submit` / `list_search_reset` 等待品牌列表请求成功后上报，补齐结果数量和请求 ID，避免 `usage-events` 因必填字段缺失返回 400。
- REQ-0128 证书列表页与收藏列表页搜索范围返修：证书列表页改为当前页输入过滤并支持 `/api/v1/miniapp/certificates?keyword=...`；收藏列表页收敛为当前收藏范围搜索并移除显著全局搜索调整入口；两页搜索提交/清空埋点补齐 usage event 必填字段。
- REQ-0128 首页搜索入口搜索耗时返修：用户截图确认 `/api/v1/miniapp/search` 首屏 TTFB 约 3.80s；关键词进入搜索页时跳过无必要 `/search/home` 请求，搜索首屏推荐词改为轻量默认词，避免同步触发 `get_search_home()` 与 `hot_score metadata LIKE` 慢查询分支。
- REQ-0128 搜索结果页性能继续返修：用户复测截图显示 `/api/v1/miniapp/search` 首屏 TTFB 降至约 2.55s 但仍偏慢；综合 Tab 移除当前 UI 未展示的 facets、类目 named 和规格 named 查询，品牌/证书/SKU 单独 Tab 只执行本 Tab 必要查询。
- REQ-0128 搜索结果页性能品牌词返修：用户复测截图显示 `/api/v1/miniapp/search` TTFB 约 2.43s；品牌关键词精确命中时先识别品牌，SKU 列表和 count 使用 `brand_id` 过滤，避免继续走 SKU 多字段 `OR LIKE` 主路径。
- REQ-0128 搜索结果页性能定位返修：用户复测截图显示 `/api/v1/miniapp/search` TTFB 仍约 2.50s，DevTools 未展示服务端分段耗时；完整搜索接口新增 `Server-Timing` 响应头，拆分品牌识别、SKU list、SKU count、品牌 named、证书查询和总构建耗时。
- REQ-0128 搜索结果页卡片构建性能返修：`Server-Timing` 显示 SKU list、SKU count、品牌和证书查询均为毫秒级，`search_build` 约 2.77s；搜索结果 SKU 卡片改为直接使用约定缩略图 / 展示图 URL，不再逐卡片同步探测对象存储文件存在性，并新增 `search_product_cards` 分段。
- REQ-0128 列表型 SKU 卡片同类性能返修：将小程序首页新品/热销、商品列表、搜索首页最近浏览/热门商品和 SKU 详情推荐统一迁移到轻量列表卡片路径，不再逐卡片同步探测对象存储；详情主媒体、Banner、证书详情和品牌 Hero 保留存在性探测。

## REQ-0128 返修验证证据

- `uv run pytest tests/test_miniapp_static.py tests/test_miniapp_home.py`：82 passed，覆盖小程序搜索结果页品牌/证书专用卡片、去除“公开 SKU”文案、下滑自动加载更多、品牌 logo 搜索响应、证书图片与证书类型搜索响应、usage event 字典登记和敏感对象 key 不外泄。
- `uv run pytest tests/test_miniapp_static.py tests/test_miniapp_home.py::test_miniapp_full_search_returns_tabs_facets_certificates_and_public_filter tests/test_miniapp_home.py::test_miniapp_search_best_match_supports_exact_brand_match tests/test_miniapp_home.py::test_miniapp_search_load_more_returns_sku_only_payload tests/test_miniapp_home.py::test_miniapp_search_best_match_prefers_sku_then_certificate_match`：42 passed，覆盖综合 Tab 分区合并追加、后续页 SKU-only 轻量响应、空 facets、无最佳匹配/推荐词，以及品牌/证书搜索卡片回归。
- `uv run pytest tests/test_miniapp_static.py tests/test_miniapp_home.py`：83 passed，覆盖自动加载下一页不以整页 loading 覆盖结果、移除黄色“加载更多”按钮、底部 loadingMore 状态、SKU-only 翻页响应和小程序搜索相关回归。
- `uv run pytest tests/test_miniapp_static.py tests/test_miniapp_home.py::test_miniapp_search_load_more_returns_sku_only_payload`：39 passed，覆盖综合 Tab 内容流顺序、顶部 Tab 顺序不变、后续页 SKU-only 追加和小程序静态契约回归。
- `uv run pytest tests/test_miniapp_static.py`：38 passed，覆盖全部分类页不展示 `search-entry`、不注册搜索组件、不保留 `openSearch` / `navigateToSearch`，并确认分类双栏与进入商品列表路径回归。
- `uv run pytest tests/test_miniapp_static.py::test_miniapp_search_entry_unification_contracts tests/test_miniapp_static.py::test_miniapp_brand_list_page_covers_carousel_grid_entry_and_tracking tests/test_miniapp_home.py::test_miniapp_brand_list_returns_public_brands_and_brand_list_carousel`：3 passed，覆盖品牌列表页输入模式搜索、不跳完整搜索结果页、搜索态隐藏 Banner、后端 `/api/v1/miniapp/brands?keyword=...` 品牌字段过滤和清空恢复路径。
- `bash scripts/generate-openapi-client.sh`：通过，已同步 `/api/v1/miniapp/brands` 的 `keyword` 查询参数到 `src/web/openapi.json` 与 `src/web/src/shared/api/generated.ts`。
- `uv run pytest tests/test_miniapp_static.py::test_miniapp_brand_list_page_covers_carousel_grid_entry_and_tracking tests/test_miniapp_home.py::test_miniapp_brand_list_usage_events_validate_dictionary_and_forbidden_properties`：2 passed，覆盖品牌列表页搜索提交/清空埋点成功后上报、`resultCount` / `requestId` 补齐和 usage event 字典验收。
- `uv run pytest tests/test_miniapp_static.py::test_miniapp_search_entry_unification_contracts tests/test_miniapp_static.py::test_miniapp_certificate_list_page_replaces_placeholder_with_public_list tests/test_miniapp_static.py::test_miniapp_favorite_list_page_uses_local_storage_and_states tests/test_miniapp_home.py::test_miniapp_certificate_list_filters_public_data_and_supports_facets tests/test_miniapp_home.py::test_miniapp_certificate_detail_load_failed_usage_event_is_accepted tests/test_miniapp_home.py::test_miniapp_contract_drift_usage_events_are_registered_and_persisted`：6 passed，覆盖证书列表页当前页输入过滤、证书 API keyword、收藏页移除全局搜索调整入口和两页列表搜索埋点必填字段。
- `bash scripts/generate-openapi-client.sh`：通过，已同步 `/api/v1/miniapp/certificates` 的 `keyword` 查询参数到 `src/web/openapi.json` 与 `src/web/src/shared/api/generated.ts`。
- `uv run pytest tests/test_miniapp_static.py::test_miniapp_search_matches_req0046_prototype_structure tests/test_miniapp_home.py::test_miniapp_search_first_page_skips_search_home_hot_score_branch tests/test_miniapp_home.py::test_miniapp_search_load_more_returns_sku_only_payload`：3 passed，覆盖首页带关键词进入搜索页跳过搜索首页、搜索首屏不触发 `hot_score metadata LIKE` 分支和综合 Tab SKU-only 翻页回归。
- `uv run pytest tests/test_miniapp_static.py tests/test_miniapp_home.py`：84 passed，覆盖小程序搜索页、首页入口、品牌/证书/收藏列表搜索、完整搜索首屏性能分支和相关后端接口回归。
- `uv run pytest tests/test_miniapp_home.py::test_miniapp_full_search_returns_tabs_facets_certificates_and_public_filter tests/test_miniapp_home.py::test_miniapp_search_first_page_skips_search_home_hot_score_branch tests/test_miniapp_home.py::test_miniapp_search_single_tabs_only_run_required_queries tests/test_miniapp_home.py::test_miniapp_search_load_more_returns_sku_only_payload`：4 passed，覆盖综合 Tab 返回空 facets、跳过类目/规格 named、跳过 facets 聚合，以及品牌/证书/SKU 单独 Tab 最小查询集合。
- `uv run pytest tests/test_miniapp_home.py::test_miniapp_search_product_filters_brand_fast_path_skips_keyword_like tests/test_miniapp_home.py::test_miniapp_search_exact_brand_uses_brand_id_fast_path tests/test_miniapp_home.py::test_miniapp_search_first_page_skips_search_home_hot_score_branch tests/test_miniapp_home.py::test_miniapp_search_single_tabs_only_run_required_queries`：4 passed，覆盖品牌词搜索 SKU `brand_id` 快路径、全字段 SKU `OR LIKE` 主路径回避、搜索首屏不触发搜索首页和单独 Tab 最小查询集合。
- `uv run pytest tests/test_miniapp_home.py::test_miniapp_search_exact_brand_uses_brand_id_fast_path tests/test_miniapp_home.py::test_miniapp_search_product_filters_brand_fast_path_skips_keyword_like`：2 passed，覆盖搜索接口 `Server-Timing` 分段耗时响应头、品牌词 SKU `brand_id` 快路径和搜索卡片构建不探测对象存储。
- `uv run pytest tests/test_miniapp_home.py::test_miniapp_list_product_cards_skip_media_existence_probe tests/test_miniapp_home.py::test_miniapp_home_and_detail_recommendation_cards_use_lightweight_media_path tests/test_miniapp_home.py::test_miniapp_search_exact_brand_uses_brand_id_fast_path`：3 passed，覆盖商品列表、搜索首页、首页商品卡片和 SKU 详情推荐等列表型 SKU 卡片不触发对象存储存在性探测，同时保留详情主媒体探测路径。
- `uv run pytest tests/test_miniapp_static.py tests/test_miniapp_home.py`：87 passed，覆盖小程序搜索页、首页入口、品牌/证书/收藏列表搜索、搜索首屏性能分支、品牌词 SKU `brand_id` 快路径和相关后端接口回归。
- `uv run pytest tests/test_miniapp_static.py tests/test_miniapp_home.py`：87 passed，确认搜索结果 SKU 卡片跳过同步对象存储探测后，小程序搜索、首页、详情、品牌和证书相关接口不回归。
- `uv run pytest tests/test_miniapp_static.py tests/test_miniapp_home.py`：89 passed，覆盖小程序静态契约、首页商品卡片、商品列表、搜索首页、搜索结果和 SKU 详情推荐等列表型 SKU 卡片轻量媒体路径完整回归。
- `openspec validate update-search-experience-unification --strict`、`python scripts/validate-product-data-observability-gates.py --change update-search-experience-unification`、`python scripts/validate-openspec-language.py`、`python scripts/validate-root-cause-evidence.py --change update-search-experience-unification`：均通过，根因证据 blockers=0，warnings=0。
- `uv run pytest src/backend/tests/test_product_usage_logging.py tests/test_miniapp_home.py::test_miniapp_search_usage_events_validate_dictionary_and_forbidden_properties tests/test_miniapp_home.py::test_miniapp_track_literal_events_are_registered_in_backend_dictionary`：27 passed，覆盖 usage event 字典、请求日志、敏感字段拒绝和小程序搜索事件登记。
- `./node_modules/.bin/vitest run src/pages/admin/LogAuditPage.test.tsx`：17 passed，确认管理端日志审计回归未受影响。

## 验收结果

```yaml
acceptance_status: passed
accepted_at: 2026-08-28 16:15:59
accepted_by: workflow-sync
evidence: []
failed_items: []
notes: sprint-026 范围内 16/16 Change 已归档，关联 REQ/BUG 验收结果已回填；Sprint 关闭前进行 residual 与 stale scan 复核。
```

## REQ-0124 实现验证证据

- `uv run pytest src/backend/tests/test_product_usage_logging.py tests/test_mysql_schema_drift.py tests/test_mysql_migrations.py`：32 passed，覆盖行为链路字段、直接 API 空链路、任务 parent_request_id / spans、脱敏和 SQLite/MySQL 迁移。
- `corepack pnpm test -- LogAuditPage usage-tracking auth-api`：62 test files / 364 tests passed，覆盖前端透传、日志审计筛选、详情展示、复制 fixed toast 和 admin-list 结构。
- `bash scripts/generate-openapi-client.sh`：OpenAPI / Orval 已同步新增字段与查询参数。
