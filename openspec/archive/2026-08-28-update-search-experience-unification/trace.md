---
change_id: update-search-experience-unification
source_requirement: REQ-0128-search-experience-unification
source_sprint: sprint-026
status: applied
created_at: 2026-08-27 00:19:59
updated_at: 2026-08-28 15:10:59
---

# Change 追踪

## 来源

| 项 | 值 |
|---|---|
| REQ | `REQ-0128-search-experience-unification` |
| Sprint | `sprint-026` |
| Change 类型 | `update` |
| Capability | `miniapp-search`、`miniapp-home`、`miniapp-category-list-page`、`miniapp-brand-list-page`、`miniapp-certificate-list-page`、`miniapp-product-list-page`、`favorite-list-page`、`xl-admin-page-acceptance-template`、`product-usage-logging` |

## Requirement Readiness Report

| 项 | 结论 |
|---|---|
| 状态 | ready |
| 评审门禁 | 通过，REQ 状态为 `in_sprint` |
| Sprint 门禁 | 通过，REQ 已纳入 `sprint-026` |
| 文档完整性 | requirement、user-stories、business-flow、acceptance、trace、review、prototype context 均存在 |

## 产品数据采集与链路观测声明

```yaml
product_data_collection_observability:
  status: applicable
  affected_layers:
    - usage_events
    - request_logs
    - web_request_wrapper
    - miniapp_request_wrapper
    - api
  reason: 搜索入口、搜索提交、联想、结果曝光、无结果和列表筛选均属于可命名业务行为，且会触发小程序或管理端查询 API。
  validation: proposed 阶段已在 proposal/design/tasks/acceptance 写入观测声明；apply 阶段需验证事件名、关键词脱敏、链路 ID 透传、request logs 摘要、OpenAPI/Orval/DB 影响和 Task Trace N/A。
```

## UI Contract 摘要

| 项 | 结论 |
|---|---|
| 原型事实源 | 只有 context，无 HTML/PNG；按 context > acceptance > ui-design > spec 处理 |
| 小程序 | 首页和商品列表提供完整搜索页路径；品牌、证书、收藏提供当前页输入过滤；全部分类页不展示搜索入口 |
| 管理端 | 主要列表统一搜索、筛选、重置、真实分页和空态 |
| 视觉约束 | Web 管理端使用 semantic token；小程序沿用暗色旗舰风；不得新增裸 Hex |
| 证据要求 | apply 阶段提供小程序 320/375/430 pt 或等价证据；管理端提供代表列表截图或测试证据 |

## 验证记录

| 命令 | 结果 |
|---|---|
| `openspec status --change update-search-experience-unification --json` | 通过，proposal/design/specs/tasks 均已创建，`isComplete: true` |
| `python scripts/validate-openspec-language.py` | 通过 |
| `openspec validate update-search-experience-unification --strict` | 通过 |
| `python scripts/validate-product-data-observability-gates.py --change update-search-experience-unification` | 通过 |
| `python scripts/sync-workflow-status.py --event req.opsx --req REQ-0128-search-experience-unification --change update-search-experience-unification --sprint auto` | 通过，Sprint `sprint-026`，Updated 4，Errors 0 |
| `python scripts/sync-workflow-status.py --event opsx.apply --change update-search-experience-unification --sprint auto --dry-run` | 通过，dry-run 可解析到 Sprint `sprint-026` |
| `uv run pytest tests/test_miniapp_static.py` | 通过，38 passed；覆盖搜索入口组件化、页面复用、跳转参数、运行入口同步和小程序观测链路静态契约 |
| `./node_modules/.bin/vitest run src/pages/admin/LogAuditPage.test.tsx` | 通过，1 file / 17 tests；覆盖日志列表关键词搜索、筛选、重置、分页回到第一页和 usage event |

## Apply 实施摘要

| 范围 | 结论 |
|---|---|
| 小程序搜索入口 | `search-entry` 增加 `mode="entry"` 入口模式，首页、品牌、证书、商品列表、收藏统一复用组件；全部分类页不展示搜索入口 |
| 小程序搜索承接 | 新增 `utils/search-navigation`，统一传递 `sourcePage`、`scope`、`keyword`、分类/品牌/section/requestId 上下文 |
| 小程序列表搜索 | 商品列表复用后端 keyword 查询；品牌列表和证书列表复用后端 `keyword` 当前页过滤；收藏列表采用本地收藏范围过滤，不提供显著全局搜索调整入口 |
| 管理端列表搜索 | 日志审计列表补齐 keyword 输入，复用既有筛选、重置、分页和权限 API |
| API / Orval | 已为 `/api/v1/miniapp/brands` 和 `/api/v1/miniapp/certificates` 新增 `keyword` 查询参数并同步 OpenAPI / Orval；收藏列表为本地过滤，API N/A |
| DB | 未新增索引、表字段或迁移；DB 文档 N/A |
| Task Trace | 普通搜索与列表筛选无长耗时异步任务，Task Trace N/A |
| 视觉证据 | 本次以小程序 WXML/WXSS 静态契约和 Web DOM 测试作为等价证据；上线前仍建议在微信开发者工具或真机补拍 320/375/430 pt 截图 |

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-27 00:19:59 | `/req-opsx` | 创建 OpenSpec Change，并建立 proposal、design、spec delta、tasks、trace、acceptance 与 test-plan。 |
| 2026-08-27 00:52:25 | `/opsx-apply REQ-0128` | 完成搜索入口组件化复用、小程序主要列表搜索路径、管理端日志列表 keyword 搜索、行为链路透传与测试更新。 |
| 2026-08-27 10:16:13 | `/opsx-modify REQ-0128` | 二次返修综合 Tab 加载更多分区合并、SKU-only 轻量翻页响应，并收敛搜索 SKU 热度计算中的 `usage_events.metadata LIKE` 慢查询风险。 |
| 2026-08-27 09:46:27 | `/opsx-modify REQ-0128` | 根据验收截图返修搜索结果页品牌/证书卡片展示、去除“公开 SKU”文案、下滑自动加载更多，并补齐品牌 logo 与证书类型/图片搜索响应字段。 |
| 2026-08-28 08:44:12 | `/opsx-modify REQ-0128` | 三次返修搜索结果页自动加载 loading 分层，保留已展示结果并移除黄色“加载更多”主按钮。 |
| 2026-08-28 08:55:27 | `/opsx-modify REQ-0128` | 四次返修综合 Tab 内容流顺序为最佳匹配、品牌、证书、SKU；顶部 Tab 顺序保持综合、品牌、SKU、证书。 |
| 2026-08-28 09:05:39 | `/opsx-modify REQ-0128` | 分类列表页范围澄清返修：底部 Tab「全部分类」页不展示搜索入口，保留分类双栏浏览与进入商品列表路径。 |
| 2026-08-28 09:32:55 | `/opsx-modify REQ-0128` | 品牌列表页范围澄清返修：品牌列表页搜索改为当前页输入过滤，后端品牌列表 API 新增 `keyword`，搜索态隐藏 Banner，清空后恢复完整品牌列表和 Banner。 |
| 2026-08-28 09:48:04 | `/opsx-modify REQ-0128` | 品牌列表页搜索埋点返修：`list_search_submit` / `list_search_reset` 等待品牌列表请求成功后上报，并补齐 usage event 必填属性。 |
| 2026-08-28 10:13:06 | `/opsx-modify REQ-0128` | 证书列表页与收藏列表页搜索范围返修：证书列表页改为当前页输入过滤并新增 `/api/v1/miniapp/certificates?keyword=...`；收藏列表页移除全局搜索调整入口；两页搜索提交/清空埋点补齐必填字段。 |
| 2026-08-28 12:15:30 | `/opsx-modify REQ-0128` | 首页搜索入口搜索耗时返修：截图确认 `/api/v1/miniapp/search` 首屏 TTFB 约 3.80s；关键词进入搜索页跳过 `/search/home`；搜索首屏推荐词改为轻量默认词，避免触发 `get_search_home()` 与 `hot_score metadata LIKE` 分支。 |
| 2026-08-28 13:02:11 | `/opsx-modify REQ-0128` | 搜索结果页性能继续返修：截图确认 `/api/v1/miniapp/search` 首屏 TTFB 约 2.55s 仍偏慢；综合 Tab 移除未展示的 facets、类目 named、规格 named 查询，单独 Tab 只执行本 Tab 必要查询。 |

## 验收返修：截图逐项视觉对照

| 截图编号 | 页面 / 状态 | 期望表现 | 实际表现 | 偏差项 | 检查方式 | 处置结论 | 证据入口 |
|---|---|---|---|---|---|---|---|
| Image #1 | 小程序搜索结果页，关键词“携诚陶瓷”，综合 Tab | 品牌最佳匹配展示品牌图片、品牌名称、`x 个 SKU`；不重复展示“最佳匹配 / 品牌名称” | 品牌图片为文字占位；右侧出现“最佳匹配”和品牌名重复；SKU 数量含“公开” | 品牌卡片缺图、重复文案、内部可见性文案外露 | 附件截图人工对照 + `src/miniapp/pages/search/index.wxml` 代码定位 | 已返修 | `tests/test_miniapp_static.py::test_miniapp_search_matches_req0046_prototype_structure` |
| Image #1 | 小程序搜索结果页，品牌分区 | 品牌卡片展示品牌图片或稳定占位、品牌名称、`x 个 SKU` | 品牌图片为文字占位；右侧展示“品牌 / 信息待补充 / 相关信息 52” | 品牌实体字段未专用渲染 | 附件截图人工对照 + WXML/TS 归一化字段检查 | 已返修 | `tests/test_miniapp_home.py::test_miniapp_search_best_match_supports_exact_brand_match` |
| Image #1 | 小程序搜索结果页，证书分区 | 证书卡片展示证书图片或稳定占位、证书名称、品牌、证书类型 | 当前通用卡片未使用证书图片字段，也未稳定展示证书类型 | 证书实体字段未专用渲染，搜索响应缺类型补全 | WXML/后端搜索响应字段检查 | 已返修 | `tests/test_miniapp_home.py::test_miniapp_full_search_returns_tabs_facets_certificates_and_public_filter` |
| Image #1 | 小程序搜索结果页底部加载 | 用户持续下滑时自动加载下一页直到结束 | 当前只展示手动“加载更多”按钮 | 加载触发方式不符合用户预期 | `src/miniapp/pages/search/index.ts` / `.js` 代码定位 | 已返修，保留按钮兜底 | `tests/test_miniapp_static.py::test_miniapp_search_matches_req0046_prototype_structure` |
| 本次 Image #1 | 小程序搜索结果页，综合 Tab 下滑加载 | 加载更多在原列表基础上向下拓展，品牌 / 证书首屏固定，SKU 持续追加 | 用户反馈当前理解偏差，综合 Tab 多类型结果需要按分区合并；Network 中 `/api/v1/miniapp/search?...tab=all&page=1&page_size=20` 耗时约 3.76s | `displaySections` 翻页覆盖、综合搜索接口首屏和翻页查询路径偏重 | 用户截图 + `src/miniapp/pages/search/index.ts` + `src/backend/app/services/miniapp_home_service.py` + `src/backend/app/repositories/miniapp_home_repository.py` 代码定位 | 已二次返修 | `tests/test_miniapp_static.py::test_miniapp_search_matches_req0046_prototype_structure`; `tests/test_miniapp_home.py::test_miniapp_search_load_more_returns_sku_only_payload` |
| 2026-08-28 Image #1 | 小程序搜索结果页，自动加载下一页 | 自动加载下一页时结果列表保持可见，底部仅显示轻量加载状态，不能出现黄色“加载更多”主按钮 | 页面只剩 Tab 和整页“加载中...”；用户反馈仍能看到黄色按钮 | 首屏加载和翻页加载共用 `loading`，整页 loading 条件覆盖结果区；手动按钮仍按 `hasMore && !loading` 渲染 | 附件截图 + `src/miniapp/pages/search/index.wxml` / `.ts` / `.wxss` 代码定位 | 已三次返修 | `tests/test_miniapp_static.py::test_miniapp_search_matches_req0046_prototype_structure` |
| 2026-08-28 探索结论 | 小程序搜索结果页，综合 Tab 内容流 | 综合 Tab 内容流应按最佳匹配、品牌、证书、SKU 展示；顶部 Tab 顺序保持综合、品牌、SKU、证书 | 当前实现和 spec 仍按品牌、SKU、证书展示分区 | 证书会被 SKU 长列表压下去，信任背书信息露出偏晚 | `src/miniapp/pages/search/index.ts` / `.js` 分区排序定位 + `miniapp-search` spec 对照 | 已四次返修 | `tests/test_miniapp_static.py::test_miniapp_search_matches_req0046_prototype_structure` |
| 2026-08-28 探索结论 | 小程序底部 Tab「全部分类」页 | 全部分类页不展示搜索入口，保持分类双栏浏览；进入商品列表后再承接列表上下文搜索 | 当前实现已在分类页顶部加入 `search-entry` 并注册组件及 `openSearch` 跳转 | 产品边界澄清后，分类频道不应承担搜索入口角色 | `src/miniapp/pages/category/index.wxml` / `.ts` / `.json` / `.wxss` 定位 + REQ/Change 口径对照 | 已五次返修 | `tests/test_miniapp_static.py::test_miniapp_search_entry_unification_contracts`; `tests/test_miniapp_static.py::test_miniapp_category_page_covers_tree_cache_navigation_and_states` |
| 2026-08-28 探索结论 | 小程序品牌列表页 | 品牌列表页仅在当前页按品牌名称、品牌简称和品牌英文名过滤，结果保持品牌列表卡片布局；搜索态隐藏 Banner；清空后恢复完整列表和 Banner | 当前实现仍把品牌列表搜索作为进入完整搜索页的入口，后端品牌列表 API 不支持 `keyword` | 产品边界澄清后，品牌列表页本质是当前列表过滤，不是全局搜索结果承接页 | `src/miniapp/pages/brand-list/index.wxml` / `.ts` / `.js` + `src/backend/app/api/v1/miniapp.py` + `docs/03-api-index.md` 定位 | 已六次返修 | `tests/test_miniapp_static.py::test_miniapp_search_entry_unification_contracts`; `tests/test_miniapp_static.py::test_miniapp_brand_list_page_covers_carousel_grid_entry_and_tracking`; `tests/test_miniapp_home.py::test_miniapp_brand_list_returns_public_brands_and_brand_list_carousel` |
| 2026-08-28 Image #1 | 小程序品牌列表页，搜索提交埋点 | `POST /api/v1/usage-events` 应接受品牌列表搜索提交和清空事件，事件属性包含 `resultCount`、`requestId`、`page_path`、`sourcePage`、`scope` 和 `client_type` | 用户截图显示 `usage-events` POST 返回 400 Bad Request | 品牌页提前上报 `list_search_submit/reset`，请求成功前尚无 `resultCount`，导致后端事件字典必填字段缺失 | 附件截图 + `src/miniapp/pages/brand-list/index.ts` / `.js` + `src/backend/app/services/log_service.py` 事件字典定位 | 已七次返修 | `tests/test_miniapp_static.py::test_miniapp_brand_list_page_covers_carousel_grid_entry_and_tracking`; `tests/test_miniapp_home.py::test_miniapp_brand_list_usage_events_validate_dictionary_and_forbidden_properties` |
| 2026-08-28 探索结论 | 小程序证书列表页与收藏列表页 | 证书列表页应类似品牌列表页在当前页过滤，支持证书名称、品牌名称和证书类型；收藏列表页应收敛为当前收藏范围搜索 | 证书页仍为入口模式跳完整搜索页；收藏页虽已本地过滤，但空态和 cancel 仍保留全局搜索调整入口 | 产品边界澄清后，两页不应承担完整搜索结果页承接角色 | `src/miniapp/pages/certificates/index.*`、`src/miniapp/pages/favorites/index.*`、`src/backend/app/api/v1/miniapp.py`、`docs/03-api-index.md` 定位 | 已八次返修 | `tests/test_miniapp_static.py::test_miniapp_search_entry_unification_contracts`; `tests/test_miniapp_static.py::test_miniapp_certificate_list_page_replaces_placeholder_with_public_list`; `tests/test_miniapp_static.py::test_miniapp_favorite_list_page_uses_local_storage_and_states`; `tests/test_miniapp_home.py::test_miniapp_certificate_list_filters_public_data_and_supports_facets` |
| 2026-08-28 Image #1 / Image #2 | 首页带关键词进入搜索结果页，综合 Tab 首屏 | 首屏搜索请求应尽快返回，端侧不做无必要搜索首页请求；后端搜索首屏不为推荐词同步拉取搜索首页热门数据 | 用户截图显示 `/api/v1/miniapp/search` 状态 200，但总耗时约 3.81s，其中 TTFB 约 3.80s | 慢点集中在服务端首屏响应等待；搜索首屏仍会同步调用 `get_search_home()` 间接触发热门商品与 `hot_score metadata LIKE` 风险分支 | 附件截图 + `src/miniapp/pages/search/index.ts` + `src/backend/app/services/miniapp_home_service.py` + `src/backend/app/repositories/miniapp_home_repository.py` 代码定位 | 已九次返修 | `tests/test_miniapp_static.py::test_miniapp_search_matches_req0046_prototype_structure`; `tests/test_miniapp_home.py::test_miniapp_search_first_page_skips_search_home_hot_score_branch` |
| 2026-08-28 Image #1 | 搜索结果页，综合 Tab 首屏复测 | 搜索首屏应继续收敛 TTFB；未展示的数据不应继续参与首屏查询 | 用户截图显示 `/api/v1/miniapp/search` TTFB 约 2.55s，较 3.80s 改善但仍偏慢 | 首屏仍串行执行 SKU、品牌/类目/规格 named、证书和 facets；其中 facets 与类目/规格 named 当前 UI 不展示 | 附件截图 + `src/backend/app/services/miniapp_home_service.py` + `src/backend/app/repositories/miniapp_home_repository.py` 代码定位 | 已十次返修 | `tests/test_miniapp_home.py::test_miniapp_search_first_page_skips_search_home_hot_score_branch`; `tests/test_miniapp_home.py::test_miniapp_search_single_tabs_only_run_required_queries` |

## 验收返修：根因证据

```yaml
root_cause_status: confirmed
evidence:
  - type: screenshot
    source: Image #1
    finding: 品牌结果缺图、右侧重复展示最佳匹配和品牌名、SKU 数量含“公开”文案。
  - type: code
    source: src/miniapp/pages/search/index.wxml
    finding: 非 SKU bestMatch 和品牌/证书分区共用通用 section-result-product-card，固定渲染 image placeholder、card label、subtitle/count 和相关信息行。
  - type: code
    source: src/backend/app/repositories/miniapp_home_repository.py
    finding: 品牌 named result 原先未查询 logo_object_key，证书搜索结果原先未返回 type/file_mime_type 等展示字段。
  - type: test
    source: tests/test_miniapp_static.py; tests/test_miniapp_home.py
    finding: 已新增品牌/证书专用卡片、自动触底加载、品牌 logo、证书图片与类型字段断言。
conclusion: 根因是搜索结果页把品牌/证书复用为通用非 SKU 卡片模板，同时搜索响应字段未补齐实体图片和证书类型，导致视觉缺图、文案重复和字段语义不准确。
```

## 验收返修：二次根因证据

```yaml
load_more_root_cause_status: confirmed
performance_root_cause_status: probable
evidence:
  - type: screenshot
    source: 本次 Image #1
    finding: `/api/v1/miniapp/search?keyword=携诚陶瓷&tab=all&page=1&page_size=20` XHR 耗时约 3.76s，图片请求多在搜索响应后约百毫秒完成。
  - type: code
    source: src/miniapp/pages/search/index.ts
    finding: 翻页时顶层 `items` 追加，但实际渲染用 `displaySections` / `activeDisplaySection`，旧实现每次按新响应重算分区，导致综合 Tab 后续页可覆盖首屏分区。
  - type: code
    source: src/backend/app/services/miniapp_home_service.py
    finding: 旧 `tab=all` 搜索每页都会查询 SKU、品牌/类目/规格、证书、facets、推荐词和 best_match 所需数据，翻页重复计算首屏摘要。
  - type: code
    source: src/backend/app/repositories/miniapp_home_repository.py
    finding: 旧搜索 SKU 排序包含逐商品 `usage_events.metadata LIKE` 热度分计算，属于不可索引的慢查询风险；缺少逐 SQL 耗时日志，因此性能根因保持 probable。
  - type: test
    source: tests/test_miniapp_static.py; tests/test_miniapp_home.py::test_miniapp_search_load_more_returns_sku_only_payload
    finding: 已覆盖分区合并追加、后续页 SKU-only 响应、空 facets、无 best_match 和无推荐词。
conclusion: 加载覆盖根因为前端分区状态覆盖，已 confirmed；接口慢主要指向首屏/翻页重复查询和 metadata LIKE 热度计算，当前为 probable，已先通过轻量翻页和取消搜索热度计算收敛。
manual_follow_up_evidence:
  - 在微信开发者工具或本地 API 中复测同一关键词，记录 page=1 与 page=2 的接口耗时。
  - 若 page=1 仍高于目标阈值，补充后端 SQL 分段计时或 EXPLAIN，再决定是否新增索引或预聚合表。
```

## 验收返修：三次根因证据

```yaml
root_cause_status: confirmed
evidence:
  - type: screenshot
    source: 2026-08-28 Image #1
    finding: 自动加载下一页时页面仅剩 Tab 和整页“加载中...”空白态，且用户反馈仍能看到黄色加载按钮。
  - type: code
    source: src/miniapp/pages/search/index.wxml
    finding: 结果区顶部 loading 使用 `wx:if="{{loading}}"`，翻页时会遮蔽已展示的 displaySections；手动按钮仍使用 `more-btn` 渲染。
  - type: code
    source: src/miniapp/pages/search/index.ts
    finding: `loadResults(reset)` 无论首屏还是翻页均设置 `loading: true`，`onReachBottom` 也未区分 loadingMore 状态。
  - type: code
    source: src/miniapp/pages/search/index.wxss
    finding: `.more-btn` 仍继承黄色主按钮样式，自动加载模式下会暴露手动主按钮。
  - type: test
    source: tests/test_miniapp_static.py
    finding: 已新增 loadingMore、非首屏不覆盖结果、移除 more-btn 和底部轻量加载状态断言。
conclusion: 根因是搜索页把首屏加载和翻页加载绑定到同一个 `loading` 状态，并保留了手动“加载更多”主按钮渲染；已拆分 `loadingMore`，首屏 loading 仅在无结果时展示，翻页仅显示底部轻量状态。
```

## 验收返修：五次范围澄清证据

```yaml
root_cause_status: confirmed
evidence:
  - type: product_feedback
    source: /explore 分类列表页就是底部Tab的全部分类页，这个页面不需要搜索功能
    finding: 用户明确澄清底部 Tab「全部分类」页不需要搜索功能。
  - type: code
    source: src/miniapp/pages/category/index.wxml
    finding: 返修前分类页顶部存在 `search-entry`，与最新产品边界冲突。
  - type: code
    source: src/miniapp/pages/category/index.ts
    finding: 返修前分类页存在 `openSearch` 和 `navigateToSearch` 跳转逻辑，属于应移除的搜索入口路径。
  - type: spec
    source: openspec/archive/2026-08-28-update-search-experience-unification/specs/miniapp-category-list-page/spec.md
    finding: 已将分类页规格调整为不展示全局搜索入口、搜索框或等价搜索路径。
  - type: test
    source: tests/test_miniapp_static.py
    finding: 已补充分类页不注册 `search-entry`、不渲染 `<search-entry>`、不存在 `openSearch` / `navigateToSearch` 的反向断言。
conclusion: 根因是原 REQ-0128 将“全部分类页”误纳入搜索入口铺设范围；产品边界澄清后，分类页应保持结构化分类浏览，搜索能力由首页、品牌/证书/商品/收藏页面和商品列表上下文承接。
```

## 验收返修：六次范围澄清证据

```yaml
root_cause_status: confirmed
evidence:
  - type: product_feedback
    source: /explore 品牌列表页，仅支持搜索品牌名称，搜索结果页整体布局还是按照品牌列表页的布局，删除Banner轮播图
    finding: 用户明确澄清品牌列表页搜索本质是在当前品牌列表中过滤，不进入完整搜索结果页；搜索态需要隐藏 Banner。
  - type: code
    source: src/miniapp/pages/brand-list/index.wxml
    finding: 返修前品牌列表页使用入口模式跳转完整搜索页；已改为 `search-entry` 输入模式并绑定 input、submit、clear。
  - type: code
    source: src/backend/app/api/v1/miniapp.py
    finding: 返修前 `/api/v1/miniapp/brands` 不接受 `keyword`；已新增最长 80 字符的可选查询参数。
  - type: code
    source: src/backend/app/repositories/miniapp_home_repository.py
    finding: 已在品牌列表查询内对 `brands.name`、`brands.short_name`、`brands.english_name` 做启用品牌范围内匹配，不扩展到 SKU、证书、类目或后台备注。
  - type: docs
    source: docs/03-api-index.md; src/web/openapi.json; src/web/src/shared/api/generated.ts
    finding: 已同步 API 文档、OpenAPI 和 Orval 生成客户端中的 `keyword` 参数。
  - type: test
    source: tests/test_miniapp_static.py; tests/test_miniapp_home.py
    finding: 已覆盖品牌页输入模式、不跳完整搜索结果页、搜索态隐藏 Banner、清空恢复路径和后端 keyword 过滤。
conclusion: 根因是原实现把品牌列表页纳入“进入完整搜索页”的统一入口口径；最新产品边界要求品牌列表搜索保持在品牌列表页内，只过滤品牌字段并保留品牌卡片布局。
```

## 验收返修：七次根因证据

```yaml
root_cause_status: confirmed
evidence:
  - type: screenshot
    source: 2026-08-28 Image #1
    finding: 小程序品牌列表页搜索后 `POST /api/v1/usage-events` 返回 400 Bad Request。
  - type: code
    source: src/backend/app/services/log_service.py
    finding: `list_search_submit` 和 `list_search_reset` 的事件字典要求 `page_path`、`sourcePage`、`scope`、`resultCount`、`requestId`、`client_type`。
  - type: code
    source: src/miniapp/pages/brand-list/index.ts
    finding: 返修前 `onSearchSubmit` / `clearSearch` 在发起品牌列表请求前上报事件，缺少请求完成后才能得到的 `resultCount`。
  - type: code
    source: src/miniapp/services/api.ts
    finding: `track()` 会自动补充 `page_path`、`client_type` 和行为链路字段，但不会补充业务结果数。
  - type: test
    source: tests/test_miniapp_static.py; tests/test_miniapp_home.py
    finding: 已覆盖搜索埋点改为品牌列表请求成功后上报，且 `list_search_submit` / `list_search_reset` 满足后端 usage event 字典必填字段。
conclusion: 根因是端侧将品牌列表搜索提交/清空埋点放在请求成功之前，无法携带后端强制要求的 `resultCount`；已改为请求成功后带真实结果数上报。
```

## 验收返修：八次范围澄清证据

```yaml
root_cause_status: confirmed
evidence:
  - type: product_feedback
    source: /explore 证书列表页、收藏列表页的搜索功能也类似品牌列表页一样处理
    finding: 用户明确澄清证书列表页与收藏列表页都应按当前页或当前收藏范围过滤，不作为完整搜索结果页入口。
  - type: code
    source: src/miniapp/pages/certificates/index.wxml
    finding: 返修前证书页使用 `mode=entry` 和 `bind:tapentry=openSearch` 跳完整搜索页；已改为输入模式并绑定 input、submit、clear。
  - type: code
    source: src/backend/app/api/v1/miniapp.py
    finding: 返修前 `/api/v1/miniapp/certificates` 不接受 `keyword`；已新增最长 80 字符可选查询参数。
  - type: code
    source: src/backend/app/repositories/miniapp_home_repository.py
    finding: 已在公开证书查询内匹配证书名称、品牌名称、证书类型枚举和中文类型标签，并继续过滤隐藏、软删除和停用品牌证书。
  - type: code
    source: src/miniapp/pages/favorites/index.wxml
    finding: 返修前收藏页仍保留 `openGlobalSearch` cancel 和“去全局搜索调整”主按钮；已移除并保留收藏范围过滤与清空关键词。
  - type: test
    source: tests/test_miniapp_static.py; tests/test_miniapp_home.py
    finding: 已覆盖两页不跳完整搜索结果页、卡片布局保持、证书 keyword 过滤和 `list_search_submit/reset` usage event 字典验收。
conclusion: 根因是原实现将证书和收藏纳入“完整搜索页入口”的统一铺设口径；最新产品边界要求二者像品牌列表一样在本页或当前收藏范围内过滤。
```

## 验收返修：九次性能根因证据

```yaml
root_cause_status: confirmed
evidence:
  - type: screenshot
    source: 2026-08-28 Image #1 / Image #2
    finding: `/api/v1/miniapp/search` 状态 200，但本次请求总耗时约 3.81s，其中 Waiting/TTFB 约 3.80s，Content Download 约 1.54ms。
  - type: code
    source: src/miniapp/pages/search/index.ts
    finding: 返修前 `onLoad` 无论是否携带初始关键词均调用 `loadSearchHome()`，首页搜索入口带关键词进入时会额外请求 `/api/v1/miniapp/search/home`。
  - type: code
    source: src/backend/app/services/miniapp_home_service.py
    finding: 返修前 `search_all()` 首屏返回 `recommended_keywords=self.get_search_home().hot_keywords[:6]`，导致完整搜索响应同步进入搜索首页聚合。
  - type: code
    source: src/backend/app/services/miniapp_home_service.py; src/backend/app/repositories/miniapp_home_repository.py
    finding: `get_search_home()` 会调用 `list_products(... hot_first=True)`，该路径使用 `_hot_score_sql()`，存在逐商品 `usage_events.metadata LIKE` 扫描风险。
  - type: test
    source: tests/test_miniapp_static.py; tests/test_miniapp_home.py::test_miniapp_search_first_page_skips_search_home_hot_score_branch
    finding: 已覆盖关键词进入搜索页时不额外加载搜索首页，清空关键词再加载搜索首页；后端搜索首屏在 `_hot_score_sql()` 抛错时仍可返回。
conclusion: 根因是完整搜索首屏仍同步取搜索首页推荐词，间接触发热门商品与 `hot_score metadata LIKE` 慢查询风险；同时端侧关键词入口额外拉取搜索首页数据。已改为搜索首屏轻量默认推荐词，并仅在无关键词或清空关键词进入搜索首页时加载 `/search/home`。
```

## 验收返修：十次性能根因证据

```yaml
root_cause_status: probable
evidence:
  - type: screenshot
    source: 2026-08-28 Image #1
    finding: `/api/v1/miniapp/search` 本次请求 TTFB 约 2.55s，较前次约 3.80s 已改善，但仍主要耗时在服务端等待。
  - type: code
    source: src/backend/app/services/miniapp_home_service.py
    finding: 返修前搜索首屏仍串行执行 SKU、品牌/类目/规格 named、证书、facets 和 best_match 组装。
  - type: code
    source: src/backend/app/repositories/miniapp_home_repository.py
    finding: `list_search_named_results()` 中类目和规格 named、`list_search_facets()` 中品牌/类目/规格 facets 均包含 `LIKE`、`COUNT` 或 `GROUP BY` 查询，但当前搜索结果 UI 不展示这些数据。
  - type: test
    source: tests/test_miniapp_home.py::test_miniapp_search_first_page_skips_search_home_hot_score_branch; tests/test_miniapp_home.py::test_miniapp_search_single_tabs_only_run_required_queries
    finding: 已覆盖完整搜索首屏不触发 facets 聚合和类目/规格 named 查询，且品牌/证书/SKU 单独 Tab 只执行本 Tab 必要查询。
conclusion: 截图与代码共同指向首屏仍存在未展示数据的多组聚合查询，但缺少逐 SQL timing，具体最慢 SQL 保持 probable；已按当前 UI 展示边界继续收敛查询集合。
manual_follow_up_evidence:
  - 重启后端后用同一关键词复测 `/api/v1/miniapp/search` 首屏 TTFB。
  - 若仍高于目标阈值，下一步补后端 SQL 分段计时或 EXPLAIN，再决定是否新增索引、预聚合或搜索专用表。
```

## 验收返修：十一次性能根因证据

```yaml
root_cause_status: probable
evidence:
  - type: screenshot
    source: 2026-08-28 Image #1
    finding: `/api/v1/miniapp/search` 本次请求 TTFB 约 2.43s，移除 facets、类目 named 和规格 named 后改善不明显，主要等待仍发生在服务端搜索响应。
  - type: product_feedback
    source: /opsx-modify REQ-0128 搜索结果页性能继续返修
    finding: 用户明确要求针对品牌关键词增加搜索快路径，先识别品牌精确或高置信命中，再让 SKU 查询使用 `brand_id` 过滤。
  - type: code
    source: src/backend/app/repositories/miniapp_home_repository.py
    finding: 已新增品牌精确命中查询，支持品牌名称、品牌简称和品牌英文名；`_search_product_filters()` 在传入 `search_brand_id` 时改为 `t.brand_id = :search_brand_id`，不拼接 SKU 多字段 `OR LIKE` 条件。
  - type: code
    source: src/backend/app/services/miniapp_home_service.py
    finding: `search_all()` 在品牌、SKU 或综合 Tab 下先识别品牌快路径；命中后 SKU 列表和 count 共用 `brand_id` 过滤，并复用该品牌命中构造品牌分区与 best_match。
  - type: test
    source: tests/test_miniapp_home.py::test_miniapp_search_product_filters_brand_fast_path_skips_keyword_like; tests/test_miniapp_home.py::test_miniapp_search_exact_brand_uses_brand_id_fast_path
    finding: 已通过测试钩子验证品牌词搜索会向 SKU 查询传入 `search_brand_id`，且生成的 SKU filter 不包含 `t.name LIKE :keyword`、`b.name LIKE :keyword` 等全字段主路径条件。
conclusion: 现场耗时仍需重启后端后复测确认；当前证据支持剩余慢点大概率来自品牌词仍使用通用 SKU 多字段 `OR LIKE` 列表和 count 查询。已针对该场景切到品牌 ID 快路径，避免品牌词场景继续扫描 SKU 多字段。
manual_follow_up_evidence:
  - 重启后端后用同一关键词复测 `/api/v1/miniapp/search?keyword=携诚陶瓷&tab=all&page=1&page_size=20` 首屏 TTFB。
  - 若品牌快路径后 TTFB 仍明显偏高，补真实 SQL 分段 timing 或 EXPLAIN，分别定位 SKU list、SKU count、品牌精确命中和证书查询耗时。
```

## 验收返修：十二次性能定位证据

```yaml
root_cause_status: unknown
evidence:
  - type: screenshot
    source: 2026-08-28 Image #1
    finding: `/api/v1/miniapp/search` 最新复测总耗时约 2.51s，Waiting/TTFB 约 2.50s；DevTools 的 Server Timing 区域仍无服务端分段数据。
  - type: code
    source: src/backend/app/api/v1/miniapp.py
    finding: 已为完整搜索接口增加 `Server-Timing` 响应头，承载服务端搜索阶段耗时。
  - type: code
    source: src/backend/app/services/miniapp_home_service.py
    finding: 已在搜索服务中记录 `search_brand_match`、`search_brand_named`、`search_certificates` 和 `search_build` 等阶段耗时。
  - type: code
    source: src/backend/app/repositories/miniapp_home_repository.py
    finding: 已在 SKU 搜索仓储中拆分记录 `search_sku_list` 和 `search_sku_count`，用于区分列表查询和总数查询耗时。
  - type: test
    source: tests/test_miniapp_home.py::test_miniapp_search_exact_brand_uses_brand_id_fast_path
    finding: 已覆盖响应头包含 `search_brand_match`、`search_sku_list`、`search_sku_count` 和 `search_certificates` 阶段。
conclusion: 最新截图只能确认服务端整体 TTFB 仍慢，无法确认具体 SQL 或阶段；本轮改为补充分段耗时观测信号，下一次复测应以 `Server-Timing` 阶段耗时作为确定根因依据。
manual_follow_up_evidence:
  - 重启后端后在微信开发者工具选中 `/api/v1/miniapp/search`，查看 Timing 面板底部 Server Timing 阶段。
  - 若 `search_sku_count` 或 `search_sku_list` 占主要耗时，再针对对应 SQL 做 EXPLAIN 和索引方案；若 `search_certificates` 占主要耗时，则收敛证书搜索字段或增加证书查询索引。
```

## 验收返修：十三次性能根因证据

```yaml
root_cause_status: confirmed
evidence:
  - type: screenshot
    source: 2026-08-28 Image #1
    finding: `Server-Timing` 显示 `search_brand_match=2ms`、`search_certificates=4ms`、`search_sku_count=9ms`、`search_sku_list=8ms`，但 `search_build=2.77s`，慢段集中在服务端响应构建而非 SQL 查询。
  - type: code
    source: src/backend/app/services/miniapp_home_service.py
    finding: 返修前搜索结果 SKU 卡片通过 `_to_product_card()` 调用 `_image_variant_urls()`；该路径对每张图同步执行 thumbnail 和 display 对象存在性探测。
  - type: code
    source: src/backend/app/services/miniapp_home_service.py
    finding: `_media_object_exists()` 使用对象存储客户端 `get_object_info()`，在搜索列表十几张图片场景下会放大为多次同步存储探测。
  - type: code
    source: src/backend/app/services/miniapp_home_service.py
    finding: 已为搜索结果 SKU 卡片传入 `verify_media_exists=False`，直接返回约定缩略图和展示图 URL，并新增 `search_product_cards` 阶段耗时。
  - type: test
    source: tests/test_miniapp_home.py::test_miniapp_search_exact_brand_uses_brand_id_fast_path
    finding: 已 monkeypatch `_media_object_exists()` 抛错并验证搜索仍返回成功，证明搜索卡片构建不再逐卡片探测对象存储。
conclusion: 根因已确认为搜索响应构建阶段逐卡片同步探测媒体对象存在性，而不是 SKU list、SKU count、品牌或证书 SQL 查询。已改为列表卡片直接使用约定派生图 URL，由小程序图片 fallback 兜底缺失素材。
manual_follow_up_evidence:
  - 重启后端后复测同一关键词，确认 `search_product_cards` 与 `search_build` 显著下降。
  - 若 `search_build` 仍偏高，继续用新增分段定位非媒体转换开销。
```

## 验收返修：十四次同类风险证据

```yaml
root_cause_status: confirmed
evidence:
  - type: code
    source: src/backend/app/services/miniapp_home_service.py
    finding: 首页新品/热销、商品列表、搜索首页最近浏览/热门商品和 SKU 详情推荐均复用 `_to_product_card()` 构建列表型 SKU 卡片，存在与搜索结果页同源的逐卡片媒体探测风险。
  - type: code
    source: src/backend/app/services/miniapp_home_service.py
    finding: 已新增 `_to_list_product_card()` 作为列表型 SKU 卡片轻量路径，并将首页、商品列表、搜索首页和详情推荐迁移到该路径。
  - type: boundary
    source: src/backend/app/services/miniapp_home_service.py
    finding: SKU 详情主卡片、详情媒体列表、Banner、证书详情和品牌 Hero 继续使用 `_image_variant_urls()` 默认存在性探测，避免破坏详情页媒体质量兜底。
  - type: test
    source: tests/test_miniapp_home.py::test_miniapp_list_product_cards_skip_media_existence_probe; tests/test_miniapp_home.py::test_miniapp_home_and_detail_recommendation_cards_use_lightweight_media_path
    finding: 已覆盖商品列表和搜索首页在 `_media_object_exists()` 抛错时仍可成功返回；首页商品卡片和 SKU 详情推荐存在轻量 `verify_exists=False` 调用，同时详情主媒体仍存在 `verify_exists=True` 调用。
conclusion: 同源慢因不只影响完整搜索页，也会影响其它列表型 SKU 卡片；已通过统一轻量 helper 收敛列表路径，并保留详情型媒体探测边界。
```

## 验收返修：验证记录

| 命令 | 结果 |
|---|---|
| `uv run pytest tests/test_miniapp_static.py::test_miniapp_search_entry_unification_contracts tests/test_miniapp_static.py::test_miniapp_certificate_list_page_replaces_placeholder_with_public_list tests/test_miniapp_static.py::test_miniapp_favorite_list_page_uses_local_storage_and_states tests/test_miniapp_home.py::test_miniapp_certificate_list_filters_public_data_and_supports_facets tests/test_miniapp_home.py::test_miniapp_certificate_detail_load_failed_usage_event_is_accepted tests/test_miniapp_home.py::test_miniapp_contract_drift_usage_events_are_registered_and_persisted` | 通过，6 passed；覆盖八次返修的证书列表页当前页输入过滤、证书 API keyword、收藏页移除全局搜索调整入口和两页列表搜索埋点必填字段 |
| `bash scripts/generate-openapi-client.sh` | 通过；已同步 `/api/v1/miniapp/certificates` 的 `keyword` 查询参数到 `src/web/openapi.json` 与 `src/web/src/shared/api/generated.ts` |
| `uv run pytest tests/test_miniapp_static.py::test_miniapp_search_matches_req0046_prototype_structure tests/test_miniapp_home.py::test_miniapp_search_first_page_skips_search_home_hot_score_branch tests/test_miniapp_home.py::test_miniapp_search_load_more_returns_sku_only_payload` | 通过，3 passed；覆盖九次返修的关键词进入搜索页跳过 `/search/home`、搜索首屏不触发 `hot_score metadata LIKE` 分支和综合 Tab SKU-only 翻页回归 |
| `uv run pytest tests/test_miniapp_static.py tests/test_miniapp_home.py` | 通过，84 passed；覆盖小程序搜索页、首页入口、列表搜索、完整搜索首屏性能分支和相关后端接口整体回归 |
| `uv run pytest tests/test_miniapp_home.py::test_miniapp_full_search_returns_tabs_facets_certificates_and_public_filter tests/test_miniapp_home.py::test_miniapp_search_first_page_skips_search_home_hot_score_branch tests/test_miniapp_home.py::test_miniapp_search_single_tabs_only_run_required_queries tests/test_miniapp_home.py::test_miniapp_search_load_more_returns_sku_only_payload` | 通过，4 passed；覆盖十次返修的综合 Tab 空 facets、跳过类目/规格 named、跳过 facets 聚合和单独 Tab 最小查询集合 |
| `uv run pytest tests/test_miniapp_home.py::test_miniapp_search_product_filters_brand_fast_path_skips_keyword_like tests/test_miniapp_home.py::test_miniapp_search_exact_brand_uses_brand_id_fast_path tests/test_miniapp_home.py::test_miniapp_search_first_page_skips_search_home_hot_score_branch tests/test_miniapp_home.py::test_miniapp_search_single_tabs_only_run_required_queries` | 通过，4 passed；覆盖十一返修的品牌词 SKU `brand_id` 快路径、全字段 SKU `OR LIKE` 主路径回避、搜索首屏不触发搜索首页和单独 Tab 最小查询集合 |
| `uv run pytest tests/test_miniapp_home.py::test_miniapp_search_exact_brand_uses_brand_id_fast_path tests/test_miniapp_home.py::test_miniapp_search_product_filters_brand_fast_path_skips_keyword_like` | 通过，2 passed；覆盖十二/十三返修的搜索接口 `Server-Timing` 分段耗时响应头、品牌词 SKU `brand_id` 快路径和搜索卡片构建不探测对象存储 |
| `uv run pytest tests/test_miniapp_home.py::test_miniapp_list_product_cards_skip_media_existence_probe tests/test_miniapp_home.py::test_miniapp_home_and_detail_recommendation_cards_use_lightweight_media_path tests/test_miniapp_home.py::test_miniapp_search_exact_brand_uses_brand_id_fast_path` | 通过，3 passed；覆盖十四返修的商品列表、搜索首页、首页商品卡片和 SKU 详情推荐等列表型 SKU 卡片不触发对象存储存在性探测，同时保留详情主媒体探测路径 |
| `uv run pytest tests/test_miniapp_static.py tests/test_miniapp_home.py` | 通过，87 passed；覆盖小程序搜索页、首页入口、品牌/证书/收藏列表搜索、搜索首屏性能分支、品牌词 SKU `brand_id` 快路径和相关后端接口回归 |
| `uv run pytest tests/test_miniapp_static.py tests/test_miniapp_home.py` | 通过，87 passed；确认搜索接口 `Server-Timing` 响应头不破坏既有小程序搜索 JSON 契约 |
| `uv run pytest tests/test_miniapp_static.py tests/test_miniapp_home.py` | 通过，87 passed；确认搜索结果 SKU 卡片跳过同步对象存储探测后，小程序搜索、首页、详情、品牌和证书相关接口不回归 |
| `uv run pytest tests/test_miniapp_static.py tests/test_miniapp_home.py` | 通过，89 passed；覆盖小程序静态契约、首页商品卡片、商品列表、搜索首页、搜索结果和 SKU 详情推荐等列表型 SKU 卡片轻量媒体路径完整回归 |
| `git diff --check -- <返修相关源码与文档>` | 通过 |
| `openspec validate update-search-experience-unification --strict` | 通过 |
| `python scripts/validate-product-data-observability-gates.py --change update-search-experience-unification` | 通过 |
| `python scripts/validate-openspec-language.py` | 通过 |
| `python scripts/validate-root-cause-evidence.py --change update-search-experience-unification` | 通过，blockers=0，warnings=0 |
| `uv run pytest tests/test_miniapp_static.py tests/test_miniapp_home.py` | 通过，82 passed |
| `uv run pytest src/backend/tests/test_product_usage_logging.py tests/test_miniapp_home.py::test_miniapp_search_usage_events_validate_dictionary_and_forbidden_properties tests/test_miniapp_home.py::test_miniapp_track_literal_events_are_registered_in_backend_dictionary` | 通过，27 passed |
| `./node_modules/.bin/vitest run src/pages/admin/LogAuditPage.test.tsx` | 通过，1 file / 17 tests |
| `git diff --check -- <返修相关源码与文档>` | 通过 |
| `openspec validate update-search-experience-unification --strict` | 通过 |
| `python scripts/validate-product-data-observability-gates.py --change update-search-experience-unification` | 通过 |
| `python scripts/validate-openspec-language.py` | 通过 |
| `uv run pytest tests/test_miniapp_static.py tests/test_miniapp_home.py::test_miniapp_full_search_returns_tabs_facets_certificates_and_public_filter tests/test_miniapp_home.py::test_miniapp_search_best_match_supports_exact_brand_match tests/test_miniapp_home.py::test_miniapp_search_load_more_returns_sku_only_payload tests/test_miniapp_home.py::test_miniapp_search_best_match_prefers_sku_then_certificate_match` | 通过，42 passed；覆盖二次返修的分区合并、SKU-only 翻页响应和品牌/证书搜索卡片回归 |
| `uv run pytest tests/test_miniapp_static.py tests/test_miniapp_home.py` | 通过，83 passed；覆盖小程序搜索页、列表页、搜索接口和相关行为事件回归 |
| `python scripts/validate-root-cause-evidence.py --change update-search-experience-unification` | 通过，blockers=0，warnings=0 |
| `python scripts/sync-workflow-status.py --event opsx.modify --change update-search-experience-unification --sprint auto` | 通过，Sprint `sprint-026`，Updated 1，Errors 0 |
| `python scripts/extract-ai-usage.py --post-command-hook --workflow-event opsx.modify --change update-search-experience-unification --sprint sprint-026 --json` | 通过，`usage_mode=actual`，`command_run_count=1`，Sprint snapshot refreshed，warnings=0 |
| `uv run pytest tests/test_miniapp_static.py::test_miniapp_brand_list_page_covers_carousel_grid_entry_and_tracking tests/test_miniapp_home.py::test_miniapp_brand_list_usage_events_validate_dictionary_and_forbidden_properties` | 通过，2 passed；覆盖七次返修的品牌列表搜索埋点成功后上报、`resultCount` / `requestId` 补齐和 usage event 字典验收 |
| `uv run pytest tests/test_miniapp_static.py tests/test_miniapp_home.py` | 通过，83 passed；覆盖三次返修的自动加载不整页覆盖、底部 `loadingMore` 状态、移除黄色“加载更多”按钮、SKU-only 翻页响应和小程序搜索相关回归 |
| `uv run pytest tests/test_miniapp_static.py tests/test_miniapp_home.py::test_miniapp_search_load_more_returns_sku_only_payload` | 通过，39 passed；覆盖四次返修的综合 Tab 内容流顺序、顶部 Tab 顺序不变、后续页 SKU-only 追加和小程序静态契约回归 |
| `uv run pytest tests/test_miniapp_static.py` | 通过，38 passed；覆盖五次返修的全部分类页不展示 `search-entry`、不注册搜索组件、不保留 `openSearch` / `navigateToSearch`，并确认分类双栏与进入商品列表路径回归 |
| `uv run pytest tests/test_miniapp_static.py::test_miniapp_search_entry_unification_contracts tests/test_miniapp_static.py::test_miniapp_brand_list_page_covers_carousel_grid_entry_and_tracking tests/test_miniapp_home.py::test_miniapp_brand_list_returns_public_brands_and_brand_list_carousel` | 通过，3 passed；覆盖六次返修的品牌列表页输入模式搜索、不跳完整搜索结果页、搜索态隐藏 Banner、清空恢复路径和后端 `keyword` 品牌字段过滤 |
| `bash scripts/generate-openapi-client.sh` | 通过；已同步 `/api/v1/miniapp/brands` 的 `keyword` 查询参数到 `src/web/openapi.json` 与 `src/web/src/shared/api/generated.ts` |
| `git diff --check` | 通过 |
| `openspec validate update-search-experience-unification --strict` | 通过 |
| `python scripts/validate-product-data-observability-gates.py --change update-search-experience-unification` | 通过 |
| `python scripts/validate-openspec-language.py` | 通过 |
| `python scripts/validate-root-cause-evidence.py --change update-search-experience-unification` | 通过，blockers=0，warnings=0 |
| `python scripts/sync-workflow-status.py --event opsx.modify --change update-search-experience-unification --sprint auto` | 通过，Sprint `sprint-026`，Updated 1，Errors 0 |
| `python scripts/extract-ai-usage.py --post-command-hook --workflow-event opsx.modify --change update-search-experience-unification --sprint sprint-026 --json` | 通过，`usage_mode=actual`，`command_run_count=1`，Sprint snapshot refreshed，warnings=0 |
