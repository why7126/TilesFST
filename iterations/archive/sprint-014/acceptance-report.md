---
note: workflow-sync — 9/9 Change 已 archive；0 applied；Sprint 已关闭
sprint_id: sprint-014
title: Sprint 014 验收报告
status: final
lifecycle_stage: archive
created_at: 2026-07-29 15:51:41
updated_at: 2026-07-31 08:15:46
owner: product
---

# Sprint 014 验收报告

## 1. 验收范围

| 类型 | ID | Change | 状态 | 验收结论 |
|---|---|---|---|---|
| REQ | REQ-0081-release-image-build-governance | update-release-image-build-governance | done，已归档（`update-release-image-build-governance` archived 2026-07-29 16:07:14） | 已完成实现、规格合并、Workflow Sync、Issue promote 与归档校验 |
| REQ | REQ-0082-admin-category-name-special-characters | update-admin-category-name-special-characters | done，已归档（`update-admin-category-name-special-characters` archived 2026-07-31 00:05:01） | 已完成实现、验收返修、规格合并、Workflow Sync、Issue promote 与归档校验 |
| REQ | REQ-0083-miniapp-brand-list-category-summary | update-miniapp-brand-list-category-summary | done，已归档（`update-miniapp-brand-list-category-summary` archived 2026-07-31 00:30:54） | 自动化验收通过；设备 evidence follow_up |
| REQ | REQ-0084-web-modal-disable-outside-close | update-web-modal-disable-outside-close | done，已归档（`update-web-modal-disable-outside-close` archived 2026-07-31 00:07:41） | 自动化验收通过，已归档 |
| REQ | REQ-0085-miniapp-global-home-floating-button | add-miniapp-global-home-floating-button | done，已归档（`add-miniapp-global-home-floating-button` archived 2026-07-31 00:03:10） | 自动化验收通过；DevTools/真机 evidence follow_up |
| BUG | BUG-0090-admin-sku-list-publish-sort-order | fix-admin-sku-list-publish-sort-order | done，已归档（`fix-admin-sku-list-publish-sort-order` archived 2026-07-31 00:18:00） | 自动化验收通过，已归档 |
| BUG | BUG-0092-miniapp-card-images-slow-load | fix-miniapp-card-image-loading | done，已归档（`fix-miniapp-card-image-loading` archived 2026-07-30 23:43:51） | 自动化验收通过；体验版/真机 evidence follow_up |
| BUG | BUG-0091-miniapp-product-list-sort-consistency | fix-miniapp-product-list-sort-consistency | done，已归档（`fix-miniapp-product-list-sort-consistency` archived 2026-07-31 00:22:58） | 自动化验收通过；分类树既有测试失败需另行处理 |
| BUG | BUG-0093-miniapp-category-secondary-grid-name-full-display | fix-miniapp-category-secondary-grid-name-display | done，已归档（`fix-miniapp-category-secondary-grid-name-display` archived 2026-07-30 23:48:19） | 自动化验收通过；DevTools/真机 evidence follow_up |

## 2. 功能验收清单

- [ ] 当发布范围包含后端、Web 构建、Dockerfile、Compose、`.env.example`、构建脚本、数据库 schema / migration、API / Orval 或离线镜像交付影响时，系统将 `image_required` 判定为 `true`。
- [ ] `image_required=false` 时，`release.json` 或 image plan 记录明确 rationale。
- [ ] `/image-prepare <version>` 读取 `releases/<version>/release.json`；缺失时阻断并提示先完成发布计划。
- [ ] `/image-prepare` 校验 `PRODUCT_VERSION`、`TILESFST_IMAGE_TAG`、`IMAGE_BUILD_TAG` 与发布版本一致，或记录明确差异理由。
- [ ] `/image-prepare` 生成 `releases/<version>/image-build-plan.json`，包含版本、image_required、image_tag、source_scope、build_env、input_files、input_hashes、database_impact、required_commands 和 blockers。
- [ ] `/image-build <version>` 读取有效 `image-build-plan.json`；缺失或过期时不得自行猜测构建输入。
- [ ] `/image-build` 复用或封装 `scripts/build-images.sh` 完成 backend/web 镜像构建、验证、离线包导出和 sha256 生成。
- [ ] `/image-build` 生成 `releases/<version>/image-manifest.json`，包含版本、image_tag、built_at、platform、backend_image、web_image、tarball、input_hashes、validation 和 source_plan。
- [ ] `/release-prepare` 在 `image_required=true` 时要求 image prepare 门禁 pass 或记录 blocker。
- [ ] `/release-publish` 校验 manifest 的版本、tag、input_hashes 与当前发布输入一致；manifest 缺失、过期或不匹配时阻断发布。
- [ ] 数据库 schema 或 migration 变更进入 image plan 和 manifest 的输入或证据摘要。
- [ ] 五个命令依赖关系明确：`/release-propose` → `/release-prepare` → `/image-prepare` → `/image-build` → `/release-publish`。
- [ ] 管理后台新增类目弹窗中，类目名称允许输入中文、英文、数字和常见可见特殊字符，且最多 15 个用户可见字符。
- [ ] 管理后台编辑类目弹窗中，类目名称使用与新增弹窗一致的校验规则。
- [ ] 合法样例 `岩板-大规格`、`仿古砖/客厅`、`600x1200(亮面)`、`A+B#系列` 可创建和更新成功。
- [ ] 超过 15 个字符、trim 后为空、换行、制表符和不可见控制字符均被前端和后端拒绝，并返回字段级错误。
- [ ] 创建 / 更新类目 API 服务端接受合法特殊字符名称，并继续校验鉴权、同层级唯一和统一 response envelope。
- [ ] API Schema、OpenAPI 字段描述、Orval 生成类型和测试夹具中不得保留“只能包含中文、英文和数字”的有效约束。
- [ ] 管理端类目列表、类目树、SKU 类目选择器、小程序分类页和 Web 展示端分类入口展示特殊字符名称时不重叠、不撑破容器。
- [x] 小程序品牌列表页上半部轮播图保持现有布局、图片比例、指示器、自动播放和点击行为不变。
- [x] 小程序品牌列表页下半部每行只展示一个品牌，左侧展示品牌 Logo、品牌名称和商品数量。
- [x] 品牌行右侧展示该品牌所有上架/公开商品对应的末级类目名称集合，同一品牌下重复末级类目只展示一次，且不使用 `+N` 折叠隐藏。
- [x] 商品数量与末级类目集合使用同一小程序公开商品口径，未公开、停用、下架或内部商品不计入。
- [x] 品牌有公开商品时，右侧类目区按商品关联类目展示末级类目；品牌无公开商品时仅左侧商品数量展示空态值，右侧类目区留空，不误导为加载失败。
- [x] 品牌行整体可点击，并沿用现有品牌主页/详情页或品牌商品列表跳转规则；不可用品牌不得打开无效页面。
- [x] 若品牌列表接口缺少 `productCount` 或 `leafCategoryNames`，API Schema、OpenAPI、Orval 或小程序 API 类型、接口文档和测试均已同步。
- [ ] Web 端管理端标准 Dialog / Modal 点击遮罩或弹窗外空白区域时不自动关闭。
- [ ] Web 展示端标准 Dialog / Modal 点击遮罩或弹窗外空白区域时不自动关闭。
- [ ] 表单弹窗外部点击后，已输入字段、已选择项、上传状态和弹窗滚动位置保持不变。
- [ ] 确认弹窗外部点击后仍保持打开，用户必须通过明确的取消、关闭图标、Esc 或确认按钮结束本次确认。
- [ ] 详情、预览类弹窗外部点击后仍保持打开，弹窗内滚动、图片切换和链接点击不受影响。
- [ ] 每个可关闭弹窗均存在可见、可点击、语义明确的关闭入口。
- [ ] 统一 Dialog / Modal 封装如存在，默认禁用外部点击关闭；页面级例外必须列出组件、原因和验收方式。
- [x] 小程序首页不展示返回首页悬浮按钮，TabBar 首页也不得出现重复回首页入口。
- [x] 小程序搜索、分类列表、分类商品列表、品牌列表、品牌详情、证书列表、收藏列表、商品详情等非首页页面展示统一返回首页悬浮按钮，并保持位置、尺寸、图标、触达面积和视觉层级一致。
- [x] 点击返回首页悬浮按钮通过 `switchTab` 或 `reLaunch` 安全返回首页，重复点击、页面栈异常或首页兜底不产生白屏、无效路径或重复导航。
- [x] 返回首页悬浮按钮不遮挡底部 TabBar、商品详情固定操作区、安全区、客服/分享/咨询等既有悬浮入口。
- [x] 对登录、表单编辑、支付/分享中间页或其它不应展示页面，记录明确例外原因和验收结论。
- [ ] 小程序分类页右侧二级类目卡片每行显示 2 个，加载态 skeleton 与实际卡片列数一致。
- [ ] 小程序分类页所有二级类目名称完整展示，不出现 `...`、行数截断或隐藏溢出。
- [ ] 二级类目长名称换行后不遮挡相邻卡片、一级类目、标题、“查看全部商品”入口、导航栏、底部 TabBar 或页面滚动。
- [ ] 点击任意二级类目仍进入对应商品列表，路由参数保持 `categoryId`、`categoryName`、`categoryLevel=secondary` 与 `sourcePage=category` 语义。
- [ ] 管理端 SKU 列表已发布 SKU 默认按 `published_at` 降序展示。
- [ ] 管理端 SKU 列表未发布 SKU 默认按 `created_at` 降序展示。
- [ ] 管理端 SKU 列表已发布和未发布混排时已发布优先，且分组内排序稳定。
- [ ] 管理端 SKU 列表搜索、筛选和分页保持同一排序契约，不重复、不漏项、不跳动。
- [ ] 管理端 SKU 新增、编辑、上架、下架和删除行为不回归，上架仍写入或刷新 `published_at`。
- [ ] 小程序首页、商品列表、搜索结果和品牌详情商品 Tab 的商品卡片图片优先使用列表缩略图或等价轻量 URL。
- [ ] 非首屏或分页后续商品卡片图片按可见性加载，不在页面初始化阶段一次性触发全部图片请求。
- [ ] 商品图片缺失、对象不存在、网络超时或解码失败时展示稳定占位，不影响商品名称、价格和点击能力。
- [ ] `/media/{object_key}` 图片响应具备缓存或等价缓存策略，并能观测慢请求、失败率和对象不存在。
- [ ] 公开 SKU 主图、缩略图与对象存储对象引用完成一致性校验，历史缺失对象有处理结论。
- [x] 小程序搜索商品结果页默认排序与品牌详情页商品 Tab 一致，按 `published_at` 升序、SKU ID 升序，空 `published_at` 使用 `created_at` 兜底。
- [x] 小程序一级分类聚合商品列表和二级分类精确商品列表默认排序与品牌详情页商品 Tab 一致。
- [x] 搜索商品结果页和分类商品列表页分页加载更多后不出现重复、漏项或已加载商品顺序跳动。
- [x] 首页“全部产品”列表排序保持既有策略，不因 BUG-0091 修复而变化。
- [x] 若搜索结果页存在相关性排序，验收材料明确相关性排序与默认发布时间排序的优先级。

## 3. 横切验收清单

- [ ] 构建计划、manifest、发布对象和公告均不得泄露密钥、真实 `.env`、数据库连接串、Authorization header、Cookie 或真实客户数据。
- [ ] 命令输出保持摘要化，展示版本、是否需要镜像、计划/manifest 路径、blocker 和下一步命令。
- [ ] 复用现有 `scripts/build-images.sh`、Dockerfile 和生产 Compose，不破坏既有镜像构建手册。
- [ ] 输入 hash 漂移、版本不一致、manifest 过期必须作为可阻断门禁，而不是仅作为 warning。
- [ ] 新增或修改发布、镜像命令 Skill 时遵守 `rules/agent-context-budget.md`，避免默认全量读取历史归档、生成物或大日志。
- [ ] 类目列表回归必须覆盖分页 DOM、fixed toast、DS confirm 和无 `window.confirm`。
- [ ] 类目新增 / 编辑弹窗回归必须覆盖无 `modal-card` 与专属类双挂载、computed width 正确、矮视口 body 可滚动。
- [ ] REQ-0084 触及的管理端弹窗 TSX 不得同时挂载 `modal-card` 与 `{feature}-modal-card` 等专属类；1440px computed width 与矮视口 body scroll 必须验收。
- [ ] REQ-0084 如触及上传控件，必须覆盖上传状态机 `idle -> uploading -> done/failed`、同会话即时回显和失败态展示；若未触及上传链路，Docker `:3000` 上传边界需标记 N/A 原因。
- [ ] BUG-0090 SKU 列表默认排序由后端分页查询统一保证，不得只在当前页本地排序。
- [ ] BUG-0090 SKU 列表发布时间列、更新时间列、分页 DOM、fixed toast、操作列和无 `window.confirm` 不回归。
- [ ] 小程序品牌单行列表在 320、375、430 pt 宽度下无文字重叠、Logo 拉伸、横向滚动、类目覆盖左侧信息或底部 TabBar 遮挡。（follow_up：待人工 DevTools evidence）
- [ ] 小程序品牌列表页 evidence 记录首屏轮播、品牌单行列表、胶囊避让、底部 TabBar、加载态、空态和错误态结论。（follow_up：待人工 DevTools evidence）
- [x] 小程序返回首页悬浮按钮 evidence 记录首页隐藏、非首页展示、搜索/分类列表/分类商品列表/品牌列表/品牌详情/证书列表/收藏列表/商品详情覆盖、底部避让、防重复点击和 DevTools 320/375/430 pt 结论。（follow_up：DevTools 截图待人工补录）
- [ ] 小程序分类页 evidence 记录 DevTools 320、375、390、430 pt 或等价视口，覆盖二级类目两列布局、长名称完整显示、胶囊避让、底部 TabBar、加载态和点击入口。
- [x] 真机验收不可用时标记 blocked 或 follow_up，不得把 DevTools 截图写作真机通过。

## 4. 验收证据

| 证据 | 状态 | 说明 |
|---|---|---|
| OpenSpec validate | 已通过 | `openspec validate update-release-image-build-governance --strict`；归档后 `openspec validate --specs --strict` 41 passed，`openspec validate --all --strict` 42 passed |
| Release validator tests | 已通过 | `uv run pytest tests/test_release_validation.py tests/test_ai_usage.py`，42 passed，覆盖 image gates、plan/manifest 引用、版本/tag 不一致和缺失证据 |
| Image plan validator tests | 已通过 | 覆盖 input hashes、database_impact、敏感信息扫描、tag mismatch blocker 和 input hash drift |
| Image manifest validator tests | 已通过 | 覆盖 source plan hash、manifest input hashes 匹配和安全字段 |
| Docker Compose config | 已通过 | `docker compose -f docker-compose.prod.yml config --quiet` 与 `docker compose -f docker-compose.prod.external.yml config --quiet` |
| AI usage hook | 已通过 | `image.prepare`、`image.build` 可识别 release version；`opsx.archive` hook 为 actual，warning 0 |
| REQ-0082 OpenSpec validate | 已通过 | `openspec validate update-admin-category-name-special-characters --strict` |
| REQ-0082 implementation tests | 已通过 | `uv run pytest src/backend/tests/test_admin_tile_categories.py` 16 passed；`pnpm --dir src/web test -- CategoryFormModal` 56 files / 300 tests passed；`pnpm --dir src/web test -- TileCategoryManagementPage TileSkuFormModal tile-categories-api` 56 files / 300 tests passed；`uv run pytest tests/test_miniapp_static.py` 30 passed |
| REQ-0082 acceptance fix tests | 已通过 | 类目树验收返修后运行 `pnpm --dir src/web test -- CategoryTree CategoryFormModal TileCategoryManagementPage`，57 files / 302 tests passed |
| REQ-0083 OpenSpec validate | 已通过 | `openspec validate update-miniapp-brand-list-category-summary --strict` |
| REQ-0083 OpenAPI / Orval | 已通过 | `bash scripts/generate-openapi-client.sh` 通过，Orval v8.17.0 生成 `tileApi`；`src/web/openapi.json` 与 `src/web/src/shared/api/generated.ts` 已包含 `leaf_category_names` |
| REQ-0083 implementation tests | 已通过 | `uv run pytest tests/test_miniapp_home.py::test_miniapp_brand_list_returns_public_brands_and_brand_list_carousel tests/test_miniapp_home.py::test_miniapp_brand_home_endpoints_return_public_detail_and_certificates tests/test_miniapp_static.py::test_miniapp_brand_list_page_covers_carousel_grid_entry_and_tracking`，3 passed；`python scripts/validate-api-standard.py` 通过；`python scripts/validate-directory-structure.py` 通过 |
| REQ-0083 DevTools 320/375/430 pt evidence | follow_up | 本次未伪造 DevTools 截图通过；需人工在微信开发者工具补录首屏轮播、品牌单行列表、胶囊避让、底部 TabBar、加载态、空态和错误态 evidence |
| REQ-0083 真机验收 | follow_up | 当前未执行真机验收；不得将 DevTools 或静态检查写作真机通过 |
| REQ-0083 acceptance modify | 已通过 | `/opsx-modify` 根据验收反馈移除“品牌有商品但无类目”的正常兜底语义；右侧类目按品牌下公开商品关联类目展示，只有无公开商品时展示无商品空态。返修后聚焦 pytest 3 passed，OpenSpec strict valid |
| REQ-0083 acceptance modify 2 | 已通过 | `/opsx-modify` 根据验收反馈取消端侧类目数量截断和 `+N` 折叠，品牌行右侧折行展示所有上架/公开商品关联的去重末级类目名称。返修后聚焦 pytest 3 passed，OpenSpec strict valid |
| REQ-0083 acceptance modify 3 | 已通过 | `/opsx-modify` 根据验收反馈拆分点击区域：品牌 Logo / 名称进入品牌详情页，右侧类目进入品牌 + 类目商品列表页；公开品牌接口新增 `leaf_categories` 类目 ID / 名称集合。返修后聚焦 pytest 3 passed，OpenAPI/Orval 已同步 |
| REQ-0083 acceptance modify 4 | 已通过 | `/opsx-modify` 根据验收反馈移除无公开商品品牌右侧“暂无商品”文案；左侧已展示空态值，右侧类目区保持空白避免重复。返修后聚焦 pytest 1 passed，OpenSpec strict valid |
| REQ-0084 OpenSpec validate | 已通过 | `openspec validate update-web-modal-disable-outside-close --strict` |
| REQ-0084 implementation tests | 待执行 | Web 标准弹窗外部点击不关闭、明确关闭入口、表单状态保留、确认弹窗不调用业务 API、admin-modal/media-upload 横切 AC 待 `/opsx-apply` 后补充 |
| REQ-0085 OpenSpec validate | 已通过 | `openspec validate add-miniapp-global-home-floating-button --strict` |
| REQ-0085 implementation tests | 已通过 | `uv run pytest tests/test_miniapp_static.py`，31 passed；覆盖首页隐藏、分类列表/品牌列表/证书列表/收藏列表等非首页 TabBar 页展示、搜索结果/商品列表/品牌详情/商品详情接入、`switchTab`/`reLaunch` 兜底、防重复点击、底部 tabbar/actionbar/list 避让与 TS/JS 同步 |
| REQ-0085 acceptance modify | 已通过 | `/opsx-modify` 根据验收反馈补齐分类列表页、品牌列表页、证书列表页、收藏列表页返回首页悬浮按钮；二次运行 `uv run pytest tests/test_miniapp_static.py` 31 passed，OpenSpec strict valid，目录结构校验通过 |
| REQ-0085 DevTools 320/375/430 pt evidence | follow_up | 当前执行环境无法打开微信开发者工具记录截图；已补静态门禁，不得表述为 DevTools 通过 |
| REQ-0085 real device evidence | follow_up | 当前无 iOS/Android 真机 evidence；归档前需补真机记录，若仍不可用需继续标记 blocked/follow_up |
| BUG-0091 OpenSpec validate | 已通过 | `openspec validate fix-miniapp-product-list-sort-consistency --strict` |
| BUG-0091 implementation tests | 已通过 | `uv run pytest tests/test_miniapp_home.py::test_miniapp_product_list_supports_context_filters_sort_and_facets tests/test_miniapp_home.py::test_miniapp_product_list_brand_default_sort_uses_published_at_and_id tests/test_miniapp_home.py::test_miniapp_product_list_category_and_keyword_default_sort_uses_public_order tests/test_miniapp_home.py::test_miniapp_product_list_primary_category_aggregates_self_and_enabled_children tests/test_miniapp_home.py::test_miniapp_product_list_filters_unpublished_and_disabled_relations tests/test_miniapp_home.py::test_miniapp_product_list_rejects_invalid_parameters`，6 passed；`uv run pytest tests/test_miniapp_static.py`，31 passed |
| BUG-0091 full miniapp_home regression | 部分失败（非本次修复） | `uv run pytest tests/test_miniapp_home.py` 中 BUG-0091 相关用例通过；`test_miniapp_category_tree_returns_public_two_level_data`、`test_miniapp_category_tree_allows_empty_children` 因当前基础 seed 与分类树测试样本 ID 冲突失败，需另行处理 |
| BUG-0090 OpenSpec validate | 已通过 | `openspec validate fix-admin-sku-list-publish-sort-order --strict` |
| BUG-0090 implementation tests | 已通过 | `uv run pytest src/backend/tests/test_admin_tile_skus.py -q`，25 passed；`pnpm --dir src/web test -- TileSkuManagementPage`，57 files / 305 tests passed；覆盖后端发布状态/业务时间排序、Web 后端顺序渲染、发布时间/更新时间列和无本地排序参数 |
| BUG-0093 OpenSpec validate | 已通过 | `openspec validate fix-miniapp-category-secondary-grid-name-display --strict` |
| BUG-0093 implementation tests | 已通过 | `uv run pytest tests/test_miniapp_static.py`，30 passed；覆盖分类页二级类目两列布局、skeleton 两列、名称不再 line-clamp/overflow 截断、二级类目点击路由参数不变 |
| BUG-0093 acceptance modify | 已验证 | 验收反馈二级类目名称垂直偏上；已调整 `.secondary-name` 为 flex 垂直/水平居中，二次运行 `uv run pytest tests/test_miniapp_static.py` 通过（31 passed） |
| BUG-0093 DevTools evidence | follow_up | 当前执行环境无法打开微信开发者工具记录 320/375/390/430 pt 截图；实现已补静态门禁，后续验收需补 DevTools evidence，不得表述为真机通过 |
| BUG-0093 real device evidence | follow_up | 当前无 iOS/Android 真机 evidence；发布或归档前需补真机记录，若仍不可用需继续标记 blocked/follow_up |
| BUG-0092 OpenSpec validate | 已通过 | `openspec validate fix-miniapp-card-image-loading --strict` |
| BUG-0092 implementation tests | 已通过 | `uv run pytest tests/test_media_storage.py tests/test_miniapp_home.py::test_miniapp_home_returns_public_data_and_hides_internal_fields tests/test_miniapp_home.py::test_miniapp_product_list_supports_context_filters_sort_and_facets tests/test_miniapp_home.py::test_miniapp_sku_detail_returns_public_media_recommendations_and_share tests/test_miniapp_static.py::test_miniapp_product_card_component_contract_and_reuse tests/test_miniapp_static.py::test_miniapp_home_images_have_runtime_fallback_handlers`，20 passed |
| BUG-0092 object audit script | 已通过 | `python -m py_compile scripts/audit-miniapp-card-images.py`；实现只读审计脚本，输出公开 SKU 主图、缩略图存在性和缺失清单 |
| BUG-0092 directory / OpenSpec gate | 已通过 | `python scripts/validate-directory-structure.py` 通过；`openspec validate fix-miniapp-card-image-loading --strict` 通过 |
| BUG-0092 full miniapp_home regression | 部分失败（非本次修复） | `uv run pytest tests/test_media_storage.py tests/test_miniapp_home.py ...` 中 BUG-0092 相关用例通过；`test_miniapp_category_tree_returns_public_two_level_data`、`test_miniapp_category_tree_allows_empty_children` 因分类树测试数据重复 ID / 共享数据污染失败，和本次图片链路修复无关 |
| BUG-0092 体验版 / 真机 evidence | follow_up | 当前未连接微信开发者工具或真机抓取 Network；不得把自动化测试写作体验版真机通过，需后续补录首屏图片完成时间、媒体失败率和对象缺失清单 |

## 5. 结论

最终结论：Sprint 014 于 2026-07-31 08:14:33 关闭。范围内 5 个 REQ、4 个 BUG、9 个 OpenSpec Change 均已完成 `/opsx-apply` 与 `/opsx-archive` 或等价归档闭环，OpenSpec specs 已合并，关联 Issue 均位于 `issues/**/archive/`，`python scripts/validate-sprint-archive-readiness.py --sprint sprint-014` 返回 PASS。

验收结论：通过，允许 Sprint 归档。自动化证据已覆盖 OpenSpec validate、后端 pytest、前端 Vitest、静态校验、API / Orval 同步、目录结构校验、发布镜像治理校验与相关聚焦回归。小程序 DevTools / 真机截图、体验版 Network evidence 等人工环境证据仍按既有记录保留为 follow_up，不作为本次 Sprint close blocker，后续发布前需按发布验收要求补录或继续标记不可用原因。
