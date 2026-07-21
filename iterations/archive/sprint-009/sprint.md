---
note: workflow-sync — workflow-sync 自动同步 — 18/18 Change archived；0 applied；Sprint `completed`
sprint_id: sprint-009
status: completed
lifecycle_stage: archive
created_at: 2026-07-19 12:50:12
updated_at: 2026-07-20 23:33:49
---

# sprint-009 迭代规划

## 1. Sprint 目标

本 Sprint 聚焦微信小程序商品浏览、品牌展示组件化、品牌列表页、证书列表页、添加到我的小程序引导语、管理后台 Banner 投放范围配置优化、分类入口、搜索体验修复、首页推荐入口路由修复、SKU 详情页视频播放修复、商品列表页双列卡片展示策略收敛、用户侧收藏列表页、顶部导航文案规则收束、自定义导航 best-practice、设备验收 evidence 治理、Sprint 008 首页设备验收残留闭环与管理端品牌证书组件化沉淀，将 `REQ-0049-miniapp-product-card-component`、`REQ-0050-miniapp-brand-header-page-title-rules`、`REQ-0051-category-list-product-list-entry-by-level`、`REQ-0052-miniapp-device-evidence-template`、`REQ-0053-miniapp-custom-navigation-best-practice`、`REQ-0054-brand-card-common-component`、`REQ-0055-brand-certificate-common-component`、`REQ-0056-product-list-card-only-layout`、`REQ-0057-certificate-list-page`、`REQ-0059-favorite-list-page`、`REQ-0060-brand-list-page`、`REQ-0061-miniapp-share-add-guide`、`REQ-0062-admin-banner-placement-scope`、`BUG-0066-search-component-prototype-deviation`、`BUG-0067-home-recommendation-list-entry-routing`、`BUG-0068-miniapp-home-device-acceptance-followup` 与 `BUG-0069-miniapp-sku-detail-carousel-video-not-playable` 纳入正式迭代范围。各项均需先创建对应 OpenSpec Change 后再进入实现。

正式目标：

- `REQ-0049-miniapp-product-card-component`：沉淀微信小程序商品卡片组件，统一商品核心信息展示、图片占位、点击跳转、卡片级异常处理和列表场景复用。
- `REQ-0050-miniapp-brand-header-page-title-rules`：收束小程序 `brand-header` 页面标题规则，首页展示两行品牌文案，非首页仅展示一行页面标题并保留返回、状态栏和微信原生胶囊避让。
- `REQ-0051-category-list-product-list-entry-by-level`：补齐分类列表页一级分类聚合商品列表入口与二级分类精确商品列表入口，明确 `categoryLevel` 参数、聚合查询语义、空状态和埋点上下文。
- `REQ-0052-miniapp-device-evidence-template`：建立小程序 DevTools/真机验收 evidence 模板，区分自动化、DevTools、真机与 follow-up 证据，避免设备验收散落在 tasks、acceptance、trace 和 Sprint 验收报告中。
- `REQ-0053-miniapp-custom-navigation-best-practice`：沉淀小程序自定义导航 best-practice，明确状态栏、微信原生胶囊、返回兜底、页面 offset 和截图验收矩阵，供后续小程序页面与 Change 复用。
- `REQ-0054-brand-card-common-component`：沉淀微信小程序品牌卡片组件，统一品牌 Logo、品牌名称、入口提示、Logo fallback、点击跳转、卡片级异常和 SKU 详情页内联结构替换。
- `REQ-0055-brand-certificate-common-component`：沉淀管理端品牌证书通用组件，统一证书缩略图、信息单元、有效期/状态 Badge、预览入口和文件卡片，并复用 admin-list、admin-modal、media-upload 横切验收 gate。
- `REQ-0056-product-list-card-only-layout`：收敛微信小程序商品列表页展示策略，移除搜索、筛选和排序控件，采用与首页热销推荐一致的一行 2 个双列商品卡片展示。
- `REQ-0057-certificate-list-page`：新增微信小程序证书列表页，将证书 Tab 从占位页升级为公开证书聚合列表，覆盖公开证书 API、证书卡片、搜索筛选、分页加载、图片/PDF 预览、安全过滤、埋点和小程序导航 evidence。
- `REQ-0059-favorite-list-page`：新增用户侧收藏列表页，集中展示已收藏对象，支持详情跳转、取消收藏、空/错/未登录状态、收藏状态一致性和基础埋点。
- `REQ-0060-brand-list-page`：新增微信小程序品牌列表页，提供与首页轮播一致的品牌轮播、一行 2 个品牌卡片列表、品牌详情/商品列表跳转、公开品牌过滤、埋点和小程序导航设备 evidence。
- `REQ-0061-miniapp-share-add-guide`：新增微信小程序“添加到我的小程序”轻量引导语，覆盖右上角原生入口提示、胶囊避让、手工关闭、本地关闭状态和 DevTools/真机 evidence。
- `REQ-0062-admin-banner-placement-scope`：优化管理后台 Banner 投放范围配置，将展示端收敛为小程序，展示位置收敛为首页轮播与品牌列表页轮播，并删除旧 Web/专题/历史位置 Banner 业务数据。
- `BUG-0066-search-component-prototype-deviation`：修复微信小程序搜索组件与 REQ-0046 原型差异，补齐搜索首页、联想、结果、筛选和无结果 5 个状态的原型对齐验收。
- `BUG-0067-home-recommendation-list-entry-routing`：修复首页新品榜、热销榜和推荐模块「查看更多」入口误跳搜索页的问题，确保进入对应商品列表页并补静态回归断言。
- `BUG-0068-miniapp-home-device-acceptance-followup`：闭环 Sprint 008 小程序首页 DevTools / 真机验收残留，补齐首页真实预览、320-430 pt、胶囊避让和内容不遮挡 evidence。
- `BUG-0069-miniapp-sku-detail-carousel-video-not-playable`：修复 SKU 商品详情页轮播图视频 URL 生成字段错误，确保视频项使用安全媒体 URL 显示和播放，并保留图片轮播兼容性。

## 2. Scope

| 类型 | 编号 | 标题 | 状态 | 估算 | 说明 |
|---|---|---|---|---:|---|
| REQ | REQ-0049-miniapp-product-card-component | 微信小程序商品卡片组件 | done | 1.0 人天 | archived `update-miniapp-product-card-component`（2026-07-19 18:09:44） |
| REQ | REQ-0050-miniapp-brand-header-page-title-rules | 小程序 brand-header 页面标题规则 | done | 1.0 人天 | archived `update-miniapp-brand-header-title-rules`（2026-07-19 20:47:02） |
| REQ | REQ-0051-category-list-product-list-entry-by-level | 分类列表页支持一二级分类商品列表入口 | done | 3.0 人天 | archived `update-miniapp-category-product-list-entry`（2026-07-19 18:14:48） |
| REQ | REQ-0052-miniapp-device-evidence-template | 小程序 DevTools/真机验收 evidence 模板 | done | 1.0 人天 | archived `add-miniapp-device-evidence-template`（2026-07-19 18:11:18） |
| REQ | REQ-0053-miniapp-custom-navigation-best-practice | 小程序自定义导航 best-practice 沉淀 | done | 1.0 人天 | archived `add-miniapp-custom-navigation-best-practice`（2026-07-19 20:59:58） |
| REQ | REQ-0054-brand-card-common-component | 微信小程序品牌卡片组件 | done | 1.0 人天 | archived `add-miniapp-brand-card-component`（2026-07-19 21:11:26） |
| REQ | REQ-0055-brand-certificate-common-component | 生成品牌证书通用组件 | done | 3.0 人天 | archived `update-brand-certificate-common-component`（2026-07-19 18:14:29） |
| REQ | REQ-0056-product-list-card-only-layout | 微信小程序商品列表页改为双列商品卡片展示 | done | 1.0 人天 | archived `update-miniapp-product-list-card-only-layout`（2026-07-20 14:56:25） |
| REQ | REQ-0057-certificate-list-page | 新增证书列表页 | done | 3.0 人天 | archived `add-miniapp-certificate-list-page`（2026-07-20 10:22:00） |
| REQ | REQ-0058-brand-detail-home-page | 微信小程序新增品牌主页/详情页 | done | 5.0 人天 | archived `add-miniapp-brand-detail-home-page`（2026-07-20 08:12:39） |
| REQ | REQ-0059-favorite-list-page | 新增收藏列表页 | done | 3.0 人天 | archived `add-favorite-list-page`（2026-07-20 18:06:16） |
| REQ | REQ-0060-brand-list-page | 新增品牌列表页 | done | 3.0 人天 | archived `add-brand-list-page`（2026-07-20 23:23:22） |
| REQ | REQ-0061-miniapp-share-add-guide | 小程序添加到我的小程序引导语 | done | 1.0 人天 | archived `add-miniapp-share-add-guide`（2026-07-20 23:23:22） |
| REQ | REQ-0062-admin-banner-placement-scope | 管理后台 Banner 投放范围配置优化 | done | 3.0 人天 | archived `update-admin-banner-placement-scope`（2026-07-20 22:51:30） |
| BUG | BUG-0066-search-component-prototype-deviation | 搜索组件整体交互与原型差异较大 | done | 3.0 人天 | archived `fix-miniapp-search-prototype-alignment`（2026-07-19 18:14:29） |
| BUG | BUG-0067-home-recommendation-list-entry-routing | 首页推荐模块查看更多和榜单入口误跳搜索页 | done | 1.0 人天 | archived `fix-miniapp-home-recommendation-routing`（2026-07-19 18:26:06） |
| BUG | BUG-0068-miniapp-home-device-acceptance-followup | Sprint 008 小程序首页 DevTools 与真机验收残留未闭环 | done | 1.0 人天 | archived `fix-miniapp-home-device-acceptance`（2026-07-19 21:13:20） |
| BUG | BUG-0069-miniapp-sku-detail-carousel-video-not-playable | SKU 商品详情页轮播图视频不能显示和播放 | done | 1.0 人天 | archived `fix-miniapp-sku-detail-video-url`（2026-07-20 08:57:35） |

BUG：`BUG-0066`、`BUG-0067`、`BUG-0068`、`BUG-0069` 已纳入正式范围，优先级高于新增体验能力；当前完成度与验收风险以 Scope 表状态、关联 Change 和 acceptance-report 为准。

Change：已回填 18 个范围项关联 Change；18 archived，0 applied，0 in_progress，0 proposed。所有已纳入范围项均已关联 Change；执行开发与归档时以 Scope 表逐项状态为准。

## 3. 工作量与容量

| 项 | 值 |
|---|---:|
| 开发人数 | 2 |
| 测试人数 | 1 |
| Sprint 容量 | 30 人天 |
| 已纳入估算 | 36.0 人天 |
| 容量占用 | 120.00% |
| fix 缓冲 | -6.0 人天 |
| fix 缓冲比例 | -20.00% |

容量门禁：Pass with high risk。`REQ-0062` 按 M 级估算 3.0 人天；基于 `sprint.yaml` 当前正式范围，纳入后总占用为 36.0/30.0 人天，等于 120% 硬阻断阈值但未超过，已处于边界。fix 缓冲为 -6.0 人天 / -20.00%，低于 SHOULD >= 30% 建议；后续必须冻结新增范围，并优先移出低优先级项、拆分 Sprint 或以替换范围方式调整。

## 4. 里程碑

| 里程碑 | 目标日期 | 说明 |
|---|---|---|
| Sprint 规划完成 | 2026-07-19 12:50:12 | 纳入 `REQ-0049` |
| 范围更新 | 2026-07-19 13:28:32 | 纳入 `BUG-0066` 搜索组件原型偏差修复 |
| 范围更新 | 2026-07-19 14:37:36 | 纳入 `REQ-0050` brand-header 页面标题规则 |
| 范围更新 | 2026-07-19 15:12:56 | 纳入 `REQ-0051` 分类列表页一二级分类商品列表入口 |
| 范围更新 | 2026-07-19 15:52:45 | 纳入 `BUG-0067` 首页推荐入口路由修复 |
| 范围更新 | 2026-07-19 17:18:31 | 纳入 `REQ-0052` 小程序 DevTools/真机验收 evidence 模板 |
| 范围更新 | 2026-07-19 17:45:33 | 纳入 `BUG-0068` Sprint 008 小程序首页 DevTools / 真机验收残留闭环 |
| 范围更新 | 2026-07-19 17:53:58 | 纳入 `REQ-0054` 微信小程序品牌卡片组件 |
| 范围更新 | 2026-07-19 17:56:00 | 纳入 `REQ-0055` 品牌证书通用组件 |
| 范围更新 | 2026-07-19 19:22:27 | 纳入 `REQ-0053` 小程序自定义导航 best-practice 沉淀 |
| 范围更新 | 2026-07-19 22:09:29 | 纳入 `REQ-0056` 商品列表页双列商品卡片展示 |
| 范围更新 | 2026-07-20 00:10:56 | 纳入 `REQ-0059` 用户侧收藏列表页 |
| 范围更新 | 2026-07-20 08:12:49 | 纳入 `REQ-0060` 微信小程序品牌列表页 |
| 范围更新 | 2026-07-20 08:25:00 | 纳入 `REQ-0057` 微信小程序证书列表页 |
| 范围更新 | 2026-07-20 08:34:38 | 纳入 `REQ-0061` 小程序添加到我的小程序引导语 |
| 范围更新 | 2026-07-20 08:57:35 | 纳入 `BUG-0069` SKU 商品详情页轮播图视频播放修复 |
| 范围更新 | 2026-07-20 19:11:31 | 纳入 `REQ-0062` 管理后台 Banner 投放范围配置优化 |
| OpenSpec Change 创建 | 2026-07-31 18:00:00 | `REQ-0049` 已创建 `update-miniapp-product-card-component`；`REQ-0055` 已创建 `update-brand-certificate-common-component`；继续运行其余 REQ/BUG 的 `/req-opsx` 或 `/bug-opsx` |
| 实现与自测 | 2026-08-08 18:00:00 | 完成商品卡片组件、brand-header 标题规则、分类入口聚合查询、设备 evidence 模板、品牌卡片组件、品牌证书通用组件、搜索组件原型偏差修复、首页推荐入口路由修复、首页设备验收残留闭环、联调和基础测试 |
| 验收收口 | 2026-08-14 18:00:00 | 完成 acceptance 对照、原型对齐证据与 Sprint 收口 |

## 5. 风险

| 风险 | 影响 | 应对 |
|---|---|---|
| 商品卡片 Change 待实现 | `REQ-0049` 已创建 `update-miniapp-product-card-component`，尚未进入 `/opsx-apply` | 后续按 Sprint 门禁运行 `/opsx-apply update-miniapp-product-card-component` 或 `/sprint-apply sprint-009` |
| brand-header 标题规则 Change 尚未创建 | `REQ-0050` 虽已纳入 Sprint，但无法进入 `/opsx-apply` | 先运行 `/req-opsx REQ-0050-miniapp-brand-header-page-title-rules`，并回填 `changes[]` |
| 分类入口 Change 尚未创建 | `REQ-0051` 虽已纳入 Sprint，但无法进入 `/opsx-apply` | 先运行 `/req-opsx REQ-0051-category-list-product-list-entry-by-level`，并回填 `changes[]` |
| 首页推荐入口修复 Change 尚未创建 | BUG-0067 虽已纳入 Sprint，但无法进入 `/opsx-apply` | 先运行 `/bug-opsx BUG-0067-home-recommendation-list-entry-routing`，并回填 `changes[]` |
| 设备 evidence 模板 Change 尚未创建 | REQ-0052 虽已纳入 Sprint，但无法进入 `/opsx-apply` | 先运行 `/req-opsx REQ-0052-miniapp-device-evidence-template`，并回填 `changes[]` |
| 自定义导航 best-practice 待实现 | REQ-0053 已创建 `add-miniapp-custom-navigation-best-practice`，尚未进入 `/opsx-apply` | 后续按 Sprint 门禁运行 `/opsx-apply add-miniapp-custom-navigation-best-practice` 或 `/sprint-apply sprint-009` |
| 品牌卡片组件设备截图证据待补齐 | `add-miniapp-brand-card-component` 已完成代码实现与静态校验，尚缺微信开发者工具或真机 320/375/430 pt 截图证据 | 补齐 REQ-0054 AC-018 / AC-020 至 AC-022 对应 evidence 后再进入归档验收 |
| 首页设备验收残留 Change 尚未创建 | BUG-0068 虽已纳入 Sprint，但无法进入 `/opsx-apply` | 先运行 `/bug-opsx BUG-0068-miniapp-home-device-acceptance-followup`，并回填 `changes[]` |
| 商品卡片与父级列表边界混淆 | 可能把筛选、分页、列表容器重新纳入本 REQ | 以 `REQ-0049` acceptance 和 review 条件通过项为边界，只实现单个商品卡片 |
| 搜索修复范围扩散 | 可能把后台搜索配置、热门词管理或自然语言搜索并入本 BUG | 以 `BUG-0066` acceptance 非目标为边界，仅修复小程序搜索原型偏差 |
| 导航规则范围扩散 | 可能把全局导航重设计、底部 TabBar 或后台文案配置并入 REQ-0050 | 以 REQ-0050 acceptance 为边界，只收束首页两行和非首页单行标题规则 |
| 一级分类聚合语义被误实现 | 可能只查询直接挂载在一级分类下的商品，漏掉下属二级分类商品 | REQ-0051 design.md 必须明确 `categoryLevel=primary` 子分类展开与聚合查询策略 |
| 小程序已有原型文件多版本并存 | 视觉验收基准可能不一致 | 以后续 Change design 明确 prototype 优先级，并引用 `prototype/miniapp/` 现有文件 |
| REQ-0056 Change 待实现 | REQ-0056 已创建 `update-miniapp-product-list-card-only-layout`，尚未进入 `/opsx-apply` | 后续按 Sprint 门禁运行 `/opsx-apply update-miniapp-product-list-card-only-layout` 或 `/sprint-apply sprint-009` |
| 商品列表页与搜索页边界混淆 | 可能误删搜索页能力或把筛选能力重新放回商品列表页 | REQ-0056 design 必须明确仅商品列表页不展示搜索/筛选/排序控件，搜索页自身能力不受影响 |
| 收藏列表端范围待确认 | REQ-0059 当前为用户侧 multi，可能同时涉及微信小程序和店主 Web 展示端 | 实现前先确认首期端范围；若两端都做，需要拆分端侧任务和响应式验收 |
| 收藏列表 API/DB 复杂度可能扩大 | 收藏状态、取消收藏、详情页同步可能需要新增接口和数据表 | 先评估既有收藏能力；如新增 API/DB，必须同步 OpenAPI、Orval、数据库文档和测试 |
| 添加引导语纳入后 Sprint 仍超过名义容量 | 当前总估算 33.0/30.0 人天，fix 缓冲 -3.0 人天 / -10.00%，低于 SHOULD >= 30% | 冻结新增范围；优先移出低优先级项、拆分 Sprint 或以替换范围方式调整 |
| 品牌页轮播数据来源待确认 | REQ-0060 可复用 Banner 管理，也可能需要品牌页专属轮播位 | 实现前在 `add-brand-list-page` design/tasks 中确认数据来源；避免新增重复 Banner/品牌数据源 |
| 品牌详情页依赖未完全闭环 | 品牌卡片点击优先进入 REQ-0058 品牌详情页/主页，若未交付可能无目标页 | 实现阶段按 Change design 降级到品牌商品列表或轻提示，并记录验收证据 |
| 添加引导语可能遮挡原生胶囊或首页首屏 | REQ-0061 涉及右上角入口提示、状态栏和胶囊 reserve | 实现必须复用小程序自定义导航 best-practice，记录 320/375/430 pt DevTools evidence；真机不可用标记 blocked/follow_up |
| SKU 详情页视频 URL 字段语义回归 | BUG-0069 涉及后端 SKU 详情接口视频媒体 URL 与小程序轮播视频节点 | 实现必须使用 `tile_videos.object_key` 生成受控媒体 URL，补真实字段语义回归测试，并确认图片轮播不回归 |
| Banner 投放范围收敛影响旧数据 | REQ-0062 要删除旧 Web/专题/历史位置 Banner 业务数据，并影响首页与品牌列表页轮播数据来源 | 实现前确认迁移/删除脚本或启动清理策略，覆盖 SQLite/MySQL 测试；仅删除业务记录，不物理删除 MinIO 对象 |
| Sprint 容量到达 120% 边界 | 纳入 REQ-0062 后总估算 36.0/30.0 人天，fix 缓冲 -6.0 人天 | 冻结新增范围；后续仅允许替换、拆分或移出低优先级项，不再净新增范围 |

## 6. 知识库承接

| 来源 | 承接项 | 本 Sprint 处理 |
|---|---|---|
| `docs/knowledge-base/retrospectives/sprint-007-retrospective.md` | Workflow Sync 与 AI usage hook 成功路径保持 compact summary | 本 Sprint 命令输出只报告摘要、计数、warning 和 recommended action |
| `docs/knowledge-base/retrospectives/sprint-007-retrospective.md` | XL 业务能力前置拆层验收 | 本 Sprint 当前 11.0 人天；后续若 Change 扩大到 API/DB/上传/Web，必须重新估算并拆层 |
| `docs/knowledge-base/retrospectives/sprint-007-retrospective.md` | 归档路径残留检查 | Sprint 收尾阶段关注 `iterations/change/<sprint>` 旧路径残留 |
| `docs/knowledge-base/retrospectives/sprint-008-retrospective.md` | 小程序运行事实源漂移预防 | BUG-0067 修复必须同步 `.ts` 与实际加载 `.js`，并补静态测试防止首页入口再次误跳搜索页 |
| `docs/knowledge-base/retrospectives/sprint-008-retrospective.md` | 页面组件边界重叠预防 | BUG-0067 仅修首页推荐入口路由，不扩大到商品列表页 UI、后端 section 语义或推荐算法 |
| `docs/knowledge-base/retrospectives/sprint-008-retrospective.md` | 小程序设备验收建立独立 Gate | REQ-0052 必须沉淀 DevTools/真机 evidence 模板，区分自动化覆盖、设备验收和人工 follow-up |
| `docs/knowledge-base/retrospectives/sprint-008-retrospective.md` | 固定导航遮挡风险预防 | REQ-0053 必须沉淀自定义导航 best-practice，统一状态栏、胶囊、返回兜底、页面 offset 和截图验收矩阵 |
| `docs/knowledge-base/retrospectives/sprint-008-retrospective.md` | 强制关闭必须生成 follow-up Issue | BUG-0068 承接 Sprint 008 首页 DevTools/真机、320-430 pt、胶囊避让和内容不遮挡残留 |
| `docs/knowledge-base/retrospectives/sprint-008-retrospective.md` | 小程序组件边界重叠预防 | REQ-0054 只做单品牌卡片展示与跳转，不承接品牌主页、品牌商品列表容器、API/DB 或上传链路 |
| `docs/knowledge-base/retrospectives/sprint-008-retrospective.md` | 分类、搜索、商品列表组件边界清晰 | REQ-0056 必须明确商品列表页仅承接浏览、入口上下文、双列卡片和分页状态，搜索/筛选保留在搜索页边界内 |
| `docs/knowledge-base/retrospectives/sprint-008-retrospective.md` | 小程序页面设备验收与导航遮挡风险 | REQ-0059 若覆盖小程序，必须按自定义导航 best-practice 补充状态栏、胶囊 reserve、页面 offset 和 320/375/430 pt evidence |
| `docs/knowledge-base/retrospectives/sprint-008-retrospective.md` | 小程序页面设备验收与导航遮挡风险 | REQ-0060 品牌列表页必须覆盖品牌轮播、双列品牌卡片、TabBar、状态栏、胶囊 reserve 和 320/375/430 pt evidence |
| `docs/knowledge-base/best-practices/miniapp-custom-navigation.md` | 小程序自定义导航、页面 offset、返回兜底和截图矩阵 | REQ-0060 实现必须按品牌列表页页面形态确认导航策略，DevTools 通过不得写作真机通过 |
| `docs/knowledge-base/retrospectives/sprint-008-retrospective.md` | 小程序页面设备验收与导航遮挡风险 | REQ-0061 引导语必须覆盖状态栏、胶囊 reserve、页面 offset、关闭行为和 320/375/430 pt evidence |
| `docs/knowledge-base/best-practices/miniapp-custom-navigation.md` | 小程序自定义导航、页面 offset、返回兜底和截图矩阵 | REQ-0061 实现必须按添加引导语页面形态确认胶囊避让和 DevTools/真机 evidence，DevTools 通过不得写作真机通过 |
| `docs/07-object-storage-strategy.md` | 媒体对象使用 object_key 生成受控访问 URL | BUG-0069 实现必须修正 SKU 详情页视频 URL 来源，避免把原始文件名当作可访问 URL |
| `docs/knowledge-base/best-practices/admin-list-page-consistency.md` | 管理端列表页分页、fixed toast 与 confirm 一致性 | REQ-0055 必须保持品牌证书页分页 DOM、指标卡 DOM、fixed toast 和 DS confirm 不回归 |
| `docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md` | 管理端弹窗专属类与 computed width 防回归 | REQ-0055 的证书文件卡片接入不得破坏新增/编辑证书弹窗宽度和矮视口滚动 |
| `docs/knowledge-base/best-practices/admin-media-upload-chain.md` | 管理端媒体上传状态机和 Docker 边界验收 | REQ-0055 文件卡片必须覆盖 idle/uploading/done/failed，并保留同会话即时回显与 Docker `:3000` 边界验收 |
| `docs/knowledge-base/best-practices/admin-list-page-consistency.md` | 管理端列表页分页、筛选、fixed toast 与 confirm 一致性 | REQ-0062 必须保持 Banner 列表分页、筛选、上下线/删除确认和提示不回归 |
| `docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md` | 管理端弹窗专属类与 computed width 防回归 | REQ-0062 的 Banner 新增/编辑弹窗不得破坏宽度、矮视口滚动和表单项布局 |
| `docs/knowledge-base/best-practices/admin-media-upload-chain.md` | 管理端媒体上传状态机和 Docker 边界验收 | REQ-0062 Banner 图片上传必须覆盖 idle/uploading/done/failed、同会话即时回显与 Docker `:3000` 边界验收 |

## 7. 横切预防清单

| 标签 | 适用性 | 验收 gate |
|---|---|---|
| admin-list | applicable | REQ-0055 与 REQ-0062 实现必须对照 AC-XCUT-001 至 AC-XCUT-004，确保管理端列表分页 DOM、指标卡/筛选 DOM、fixed toast 和 DS confirm 不回归 |
| admin-form | N/A | 不涉及管理端表单页 |
| admin-modal | applicable | REQ-0055 与 REQ-0062 实现必须对照 AC-XCUT-005 至 AC-XCUT-007，确保新增/编辑弹窗 class、computed width 和矮视口滚动不回归 |
| media-upload | applicable | REQ-0055 与 REQ-0062 实现必须对照 AC-XCUT-008 至 AC-XCUT-010，确保文件/图片上传状态机、同会话回显和 Docker `:3000` 边界验收覆盖 |
| miniapp-prototype-alignment | applicable | BUG-0066 修复必须逐项对照 REQ-0046 的 5 个 HTML/PNG 原型与 AC-BUG-001 至 AC-BUG-014 |
| miniapp-navigation-title | applicable | REQ-0050 实现必须逐页对照首页双行、非首页单行、返回按钮、状态栏和微信原生胶囊避让 AC |
| miniapp-category-product-entry | applicable | REQ-0051 实现必须对照一级分类聚合、二级分类精确、`categoryLevel` 参数、空状态、防重复点击和埋点 AC |
| miniapp-home-recommendation-routing | applicable | BUG-0067 修复必须对照 AC-BUG-001 至 AC-BUG-008，确保新品/热销入口进入商品列表页且搜索场景不回归 |
| miniapp-device-evidence | applicable | REQ-0052 实现必须对照 AC-STRUCT、AC-STATE、AC-DEVTOOLS、AC-DEVICE、AC-BOUNDARY 与 AC-SAFE，确保无设备 evidence 时不得声称真机通过 |
| miniapp-custom-navigation-best-practice | applicable | REQ-0053 实现必须对照 AC-STRUCT、AC-SAFEAREA、AC-CAPSULE、AC-BACK、AC-OFFSET、AC-CHECK 与 AC-MATRIX，确保自定义导航规则和截图矩阵可复用 |
| miniapp-brand-card | applicable | REQ-0054 实现必须对照 AC-001 至 AC-022，覆盖 SKU 详情页替换、Logo fallback、长品牌名、入口不可用、320/375/430 pt 截图和 `.ts` / `.js` 运行入口一致性 |
| miniapp-home-device-acceptance | applicable | BUG-0068 闭环必须对照 AC-001 至 AC-008，补齐首页真实预览、320-430 pt、胶囊避让和内容不遮挡 evidence |
| miniapp-product-list-card-layout | applicable | REQ-0056 实现必须对照 AC-001 至 AC-017 与 AC-UI-001 至 AC-UI-012，确保商品列表页无搜索/筛选/排序控件、双列卡片不溢出且不影响搜索页能力 |
| miniapp-favorite-list-page | applicable | REQ-0059 实现必须对照收藏列表 AC-001 至 AC-022 与 AC-UI-001 至 AC-UI-009，确认收藏项详情跳转、取消收藏、空/错/未登录状态、状态同步和小程序导航 evidence |
| miniapp-brand-list-page | applicable | REQ-0060 实现必须对照品牌列表 AC-001 至 AC-DOC-004，确认品牌入口、品牌轮播、双列品牌卡片、公开品牌过滤、埋点和小程序导航 evidence |
| miniapp-share-add-guide | applicable | REQ-0061 实现必须对照添加引导语 AC，确认右上角原生入口提示、胶囊避让、手工关闭、当前会话不重复展示和 320/375/430 pt evidence |
| miniapp-sku-detail-video-url | applicable | BUG-0069 修复必须对照视频展示、视频播放、图片兼容和小程序 evidence AC，确认后端返回视频 URL 使用 `object_key` 生成 |

## 8. 依赖 ASCII 树

```text
sprint-009
├── REQ-0049 微信小程序商品卡片组件
│   ├── parent: REQ-0047 商品列表页通用组件并应用
│   ├── depends-on: REQ-0044 微信小程序 SKU 详情页
│   ├── related: REQ-0045 分类列表页
│   ├── related: REQ-0046 搜索通用组件并应用
│   └── next: /opsx-apply update-miniapp-product-card-component 或 /sprint-apply sprint-009
├── REQ-0050 小程序 brand-header 页面标题规则
│   ├── parent: REQ-0048 小程序全局自定义导航栏
│   ├── upstream: REQ-0042 微信小程序首页品牌自定义导航栏
│   ├── covered-page: search / category / product-list / tile-detail / favorites / certificates / store-info
│   └── next: /req-opsx REQ-0050-miniapp-brand-header-page-title-rules
├── REQ-0051 分类列表页支持一二级分类商品列表入口
│   ├── parent: REQ-0045 分类列表页
│   ├── related: REQ-0047 商品列表页通用组件并应用
│   ├── primary-entry: 一级分类下所有启用二级分类商品聚合列表
│   ├── secondary-entry: 二级分类精确商品列表
│   └── next: /req-opsx REQ-0051-category-list-product-list-entry-by-level
├── REQ-0052 小程序 DevTools/真机验收 evidence 模板
│   ├── related: REQ-0039 XL 管理端页面分层验收模板
│   ├── knowledge-base: sprint-008 小程序设备验收残留
│   ├── output: docs/standards/miniapp-device-evidence-template.md
│   └── next: /req-opsx REQ-0052-miniapp-device-evidence-template
├── REQ-0053 小程序自定义导航 best-practice
│   ├── parent: REQ-0048 小程序全局自定义导航栏
│   ├── related: REQ-0052 小程序 DevTools/真机验收 evidence 模板
│   ├── knowledge-base: sprint-008 固定导航遮挡风险与设备验收残留
│   ├── output: docs/knowledge-base/best-practices/miniapp-custom-navigation.md
│   └── next: /opsx-apply add-miniapp-custom-navigation-best-practice 或 /sprint-apply sprint-009
├── REQ-0054 微信小程序品牌卡片组件
│   ├── parent: REQ-0005 品牌管理
│   ├── first-apply: REQ-0044 微信小程序 SKU 详情页
│   ├── related: REQ-0049 微信小程序商品卡片组件
│   ├── boundary: 单品牌卡片展示 / Logo fallback / 跳转 / 埋点
│   └── next: 补齐 320/375/430 pt DevTools 或真机截图 evidence 后归档
├── REQ-0055 品牌证书通用组件
│   ├── parent: REQ-0038 管理后台 - 瓷砖品牌证书管理
│   ├── related: REQ-0005 品牌管理
│   ├── knowledge-base: admin-list / admin-modal / media-upload
│   ├── scope: CertificateThumb / Summary / ValidityBadge / VisibilityBadge / PreviewAction / FileCard
│   └── next: /opsx-apply update-brand-certificate-common-component
├── REQ-0056 商品列表页双列商品卡片展示
│   ├── parent: REQ-0047 商品列表页通用组件并应用
│   ├── related: REQ-0051 分类列表页支持一二级分类商品列表入口
│   ├── related: REQ-0041 微信小程序首页
│   ├── boundary: 商品列表页无搜索/筛选/排序控件，搜索页能力不受影响
│   └── next: /opsx-apply update-miniapp-product-list-card-only-layout 或 /sprint-apply sprint-009
├── REQ-0059 用户侧收藏列表页
│   ├── related: REQ-0047 商品列表页通用组件并应用
│   ├── related: REQ-0044 微信小程序 SKU 详情页
│   ├── related: REQ-0045 分类列表页
│   ├── change: add-favorite-list-page
│   ├── boundary: 收藏列表 / 详情跳转 / 取消收藏 / 空错未登录状态 / 状态一致性
│   └── next: /opsx-apply add-favorite-list-page 或 /sprint-apply sprint-009
├── REQ-0060 微信小程序品牌列表页
│   ├── parent: REQ-0005 品牌管理
│   ├── related: REQ-0041 微信小程序首页
│   ├── related: REQ-0054 微信小程序品牌卡片组件
│   ├── related: REQ-0058 品牌详情页/主页
│   ├── change: add-brand-list-page
│   ├── boundary: 品牌入口 / 品牌轮播 / 双列品牌卡片 / 公开品牌过滤 / 小程序导航 evidence
│   └── next: /opsx-apply add-brand-list-page 或 /sprint-apply sprint-009
├── REQ-0061 小程序添加到我的小程序引导语
│   ├── related: REQ-0041 微信小程序首页
│   ├── related: REQ-0048 小程序全局自定义导航栏
│   ├── related: REQ-0053 小程序自定义导航 best-practice
│   ├── change: add-miniapp-share-add-guide
│   ├── boundary: 右上角入口提示 / 胶囊避让 / 手工关闭 / 本地状态 / 设备 evidence
│   └── next: /opsx-apply add-miniapp-share-add-guide 或 /sprint-apply sprint-009
├── REQ-0062 管理后台 Banner 投放范围配置优化
│   ├── parent: REQ-0016 Banner 管理
│   ├── related: REQ-0060 微信小程序品牌列表页
│   ├── change: update-admin-banner-placement-scope
│   ├── boundary: 小程序 / 首页轮播 / 品牌列表页轮播 / 旧数据删除 / API DB Orval
│   └── next: /opsx-apply update-admin-banner-placement-scope 或 /sprint-apply sprint-009
├── BUG-0066 搜索组件整体交互与原型差异较大
│   ├── related_requirement: REQ-0046 搜索通用组件并应用
│   ├── source_change: add-miniapp-search-component
│   └── archived_change: fix-miniapp-search-prototype-alignment
├── BUG-0067 首页推荐模块查看更多和榜单入口误跳搜索页
│   ├── related_requirement: REQ-0047 商品列表页通用组件并应用
│   ├── source_change: add-miniapp-product-list-component
│   ├── affected-entry: 新品榜 / 热销榜 / 新品推荐查看更多 / 热销推荐查看更多
│   └── next: /bug-opsx BUG-0067-home-recommendation-list-entry-routing
├── BUG-0068 Sprint 008 小程序首页 DevTools 与真机验收残留未闭环
│   ├── related_requirement: REQ-0041 微信小程序首页
│   ├── related_bug: BUG-0065 微信小程序首页预览偏差
│   ├── acceptance-gap: 首页真实预览 / 320-430 pt / 胶囊避让 / 内容不遮挡
│   └── next: /bug-opsx BUG-0068-miniapp-home-device-acceptance-followup
└── BUG-0069 SKU 商品详情页轮播图视频不能显示和播放
    ├── related_requirement: REQ-0044 微信小程序 SKU 详情页
    ├── change: fix-miniapp-sku-detail-video-url
    ├── boundary: 视频 URL 生成 / 轮播视频节点 / 图片兼容 / 小程序 evidence
    └── next: /opsx-apply fix-miniapp-sku-detail-video-url
```

## 9. 发布计划

本 Sprint 当前为小程序商品浏览体验增强、品牌展示组件化、品牌列表页、证书列表页、添加到我的小程序引导语、管理后台 Banner 投放范围配置优化、分类入口补齐、商品列表页双列卡片展示策略收敛、SKU 详情页视频播放修复、用户侧收藏列表页、顶部导航规则收束、自定义导航 best-practice、设备验收治理、搜索体验修复、首页推荐入口路由修复、首页设备验收残留闭环与管理端品牌证书组件化沉淀。若 `REQ-0049`、`REQ-0050`、`REQ-0051`、`REQ-0052`、`REQ-0053`、`REQ-0054`、`REQ-0055`、`REQ-0056`、`REQ-0057`、`REQ-0059`、`REQ-0060`、`REQ-0061`、`REQ-0062`、`BUG-0066`、`BUG-0067`、`BUG-0068` 与 `BUG-0069` 完成实现与验收，可在后续版本公告中归入“微信小程序商品浏览、品牌展示、品牌列表、证书列表、添加到我的小程序引导语、管理后台 Banner 投放范围收敛、分类导航、商品列表双列卡片、SKU 详情页视频播放修复、用户收藏列表、自定义导航 best-practice、设备验收证据治理、首页推荐入口、搜索体验优化与管理端品牌证书组件复用”。

## 10. 关联文档

| 类型 | 路径 |
|---|---|
| REQ trace | `issues/requirements/archive/REQ-0049-miniapp-product-card-component/trace.md` |
| REQ requirement | `issues/requirements/archive/REQ-0049-miniapp-product-card-component/requirement.md` |
| REQ acceptance | `issues/requirements/archive/REQ-0049-miniapp-product-card-component/acceptance.md` |
| 原型 | `issues/requirements/archive/REQ-0049-miniapp-product-card-component/prototype/miniapp/` |
| REQ trace | `issues/requirements/archive/REQ-0050-miniapp-brand-header-page-title-rules/trace.md` |
| REQ requirement | `issues/requirements/archive/REQ-0050-miniapp-brand-header-page-title-rules/requirement.md` |
| REQ acceptance | `issues/requirements/archive/REQ-0050-miniapp-brand-header-page-title-rules/acceptance.md` |
| 原型 | `issues/requirements/archive/REQ-0050-miniapp-brand-header-page-title-rules/prototype/miniapp/` |
| REQ trace | `issues/requirements/archive/REQ-0051-category-list-product-list-entry-by-level/trace.md` |
| REQ requirement | `issues/requirements/archive/REQ-0051-category-list-product-list-entry-by-level/requirement.md` |
| REQ acceptance | `issues/requirements/archive/REQ-0051-category-list-product-list-entry-by-level/acceptance.md` |
| 原型 | `issues/requirements/archive/REQ-0051-category-list-product-list-entry-by-level/prototype/miniapp/` |
| BUG trace | `issues/bugs/archive/BUG-0066-search-component-prototype-deviation/trace.md` |
| BUG bug.md | `issues/bugs/archive/BUG-0066-search-component-prototype-deviation/bug.md` |
| BUG acceptance | `issues/bugs/archive/BUG-0066-search-component-prototype-deviation/acceptance.md` |
| BUG source prototype | `issues/requirements/archive/REQ-0046-search-component-application/prototype/` |
| BUG trace | `issues/bugs/archive/BUG-0067-home-recommendation-list-entry-routing/trace.md` |
| BUG bug.md | `issues/bugs/archive/BUG-0067-home-recommendation-list-entry-routing/bug.md` |
| BUG acceptance | `issues/bugs/archive/BUG-0067-home-recommendation-list-entry-routing/acceptance.md` |
| BUG trace | `issues/bugs/archive/BUG-0068-miniapp-home-device-acceptance-followup/trace.md` |
| BUG bug.md | `issues/bugs/archive/BUG-0068-miniapp-home-device-acceptance-followup/bug.md` |
| BUG acceptance | `issues/bugs/archive/BUG-0068-miniapp-home-device-acceptance-followup/acceptance.md` |
| BUG trace | `issues/bugs/archive/BUG-0069-miniapp-sku-detail-carousel-video-not-playable/trace.md` |
| BUG bug.md | `issues/bugs/archive/BUG-0069-miniapp-sku-detail-carousel-video-not-playable/bug.md` |
| BUG acceptance | `issues/bugs/archive/BUG-0069-miniapp-sku-detail-carousel-video-not-playable/acceptance.md` |
| REQ trace | `issues/requirements/archive/REQ-0052-miniapp-device-evidence-template/trace.md` |
| REQ requirement | `issues/requirements/archive/REQ-0052-miniapp-device-evidence-template/requirement.md` |
| REQ acceptance | `issues/requirements/archive/REQ-0052-miniapp-device-evidence-template/acceptance.md` |
| REQ trace | `issues/requirements/archive/REQ-0053-miniapp-custom-navigation-best-practice/trace.md` |
| REQ requirement | `issues/requirements/archive/REQ-0053-miniapp-custom-navigation-best-practice/requirement.md` |
| REQ acceptance | `issues/requirements/archive/REQ-0053-miniapp-custom-navigation-best-practice/acceptance.md` |
| 原型 | `issues/requirements/archive/REQ-0053-miniapp-custom-navigation-best-practice/prototype/miniapp/` |
| REQ trace | `issues/requirements/archive/REQ-0054-brand-card-common-component/trace.md` |
| REQ requirement | `issues/requirements/archive/REQ-0054-brand-card-common-component/requirement.md` |
| REQ acceptance | `issues/requirements/archive/REQ-0054-brand-card-common-component/acceptance.md` |
| 原型 | `issues/requirements/archive/REQ-0054-brand-card-common-component/prototype/miniapp/` |
| REQ trace | `issues/requirements/archive/REQ-0055-brand-certificate-common-component/trace.md` |
| REQ requirement | `issues/requirements/archive/REQ-0055-brand-certificate-common-component/requirement.md` |
| REQ acceptance | `issues/requirements/archive/REQ-0055-brand-certificate-common-component/acceptance.md` |
| 原型 | `issues/requirements/archive/REQ-0055-brand-certificate-common-component/prototype/web/` |
| REQ trace | `issues/requirements/archive/REQ-0056-product-list-card-only-layout/trace.md` |
| REQ requirement | `issues/requirements/archive/REQ-0056-product-list-card-only-layout/requirement.md` |
| REQ acceptance | `issues/requirements/archive/REQ-0056-product-list-card-only-layout/acceptance.md` |
| 原型 | `issues/requirements/archive/REQ-0056-product-list-card-only-layout/prototype/miniapp/` |
| REQ trace | `issues/requirements/archive/REQ-0059-favorite-list-page/trace.md` |
| REQ requirement | `issues/requirements/archive/REQ-0059-favorite-list-page/requirement.md` |
| REQ acceptance | `issues/requirements/archive/REQ-0059-favorite-list-page/acceptance.md` |
| 原型 | `issues/requirements/archive/REQ-0059-favorite-list-page/prototype/web/` |
| REQ trace | `issues/requirements/archive/REQ-0060-brand-list-page/trace.md` |
| REQ requirement | `issues/requirements/archive/REQ-0060-brand-list-page/requirement.md` |
| REQ acceptance | `issues/requirements/archive/REQ-0060-brand-list-page/acceptance.md` |
| 原型 | `issues/requirements/archive/REQ-0060-brand-list-page/prototype/miniapp/` |
| REQ trace | `issues/requirements/archive/REQ-0061-miniapp-share-add-guide/trace.md` |
| REQ requirement | `issues/requirements/archive/REQ-0061-miniapp-share-add-guide/requirement.md` |
| REQ acceptance | `issues/requirements/archive/REQ-0061-miniapp-share-add-guide/acceptance.md` |
| 原型 | `issues/requirements/archive/REQ-0061-miniapp-share-add-guide/prototype/miniapp/` |
| REQ trace | `issues/requirements/archive/REQ-0062-admin-banner-placement-scope/trace.md` |
| REQ requirement | `issues/requirements/archive/REQ-0062-admin-banner-placement-scope/requirement.md` |
| REQ acceptance | `issues/requirements/archive/REQ-0062-admin-banner-placement-scope/acceptance.md` |
| 原型 | `issues/requirements/archive/REQ-0062-admin-banner-placement-scope/prototype/web/` |
| Change | `openspec/changes/archive/2026-07-20-add-miniapp-share-add-guide/` |
| Change | `openspec/changes/archive/2026-07-20-fix-miniapp-sku-detail-video-url/` |
| Change | `openspec/changes/archive/2026-07-20-update-admin-banner-placement-scope/` |
| 复盘 | `docs/knowledge-base/retrospectives/sprint-009-retrospective.md` |

## 11. 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-20 23:33:49 | /sprint-exps | 生成 sprint-009 迭代复盘并回链知识库 |
| 2026-07-20 23:23:22 | /sprint-archive | 归档关闭 sprint-009：18/18 Change 已归档，351/351 tasks 完成，目录 change → archive |
| 2026-07-20 19:11:31 | /sprint-propose | 纳入 REQ-0062，容量估算更新为 36.0/30.0 人天 |
| 2026-07-20 08:57:35 | /sprint-propose | 纳入 BUG-0069，容量估算更新为 33.0/30.0 人天 |
| 2026-07-20 08:34:38 | /sprint-propose | 纳入 REQ-0061，容量估算更新为 32.0/30.0 人天 |
| 2026-07-20 08:25:00 | /sprint-propose | 纳入 REQ-0057，容量估算更新为 31.0/30.0 人天 |
| 2026-07-20 08:12:49 | /sprint-propose | 纳入 REQ-0060，容量估算更新为 31.0/30.0 人天 |
| 2026-07-20 00:10:56 | /sprint-propose | 纳入 REQ-0059，容量估算更新为 20.0/30.0 人天 |
| 2026-07-19 22:09:29 | /sprint-propose | 纳入 REQ-0056，容量估算更新为 17.0/30.0 人天 |
| 2026-07-19 19:22:27 | /sprint-propose | 纳入 REQ-0053，容量估算更新为 16.0/30.0 人天 |
| 2026-07-19 17:56:00 | /sprint-propose | 纳入 REQ-0055，容量估算更新为 15.0/30.0 人天 |
| 2026-07-19 17:53:58 | /sprint-propose | 纳入 REQ-0054，容量估算更新为 12.0/30.0 人天 |
| 2026-07-19 17:45:33 | /sprint-propose | 纳入 BUG-0068，容量估算更新为 11.0/30.0 人天 |
| 2026-07-19 17:18:31 | /sprint-propose | 纳入 REQ-0052，容量估算更新为 10.0/30.0 人天 |
| 2026-07-19 15:52:45 | /sprint-propose | 纳入 BUG-0067，容量估算更新为 9.0/30.0 人天 |
| 2026-07-19 15:12:56 | /sprint-propose | 纳入 REQ-0051，容量估算更新为 8.0/30.0 人天 |
| 2026-07-19 14:37:36 | /sprint-propose | 纳入 REQ-0050，容量估算更新为 5.0/30.0 人天 |
| 2026-07-19 13:28:32 | /sprint-propose | 纳入 BUG-0066，容量估算更新为 4.0/30.0 人天 |
| 2026-07-19 12:50:12 | /sprint-propose | 创建 sprint-009，纳入 REQ-0049 |
