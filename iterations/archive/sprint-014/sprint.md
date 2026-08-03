---
note: workflow-sync — workflow-sync 自动同步 — 9/9 Change archived；0 applied；Sprint `completed`
sprint_id: sprint-014
title: Sprint 014 发布治理、类目命名与品牌列表优化
status: completed
lifecycle_stage: archive
created_at: 2026-07-29 15:51:41
updated_at: 2026-07-31 08:14:33
owner: product
---

# Sprint 014 发布治理、类目命名与品牌列表优化

## 1. Sprint 目标

本 Sprint 在已完成 `REQ-0081-release-image-build-governance` 的基础上，继续纳入 `REQ-0082-admin-category-name-special-characters`、`REQ-0083-miniapp-brand-list-category-summary`、`REQ-0084-web-modal-disable-outside-close`、`REQ-0085-miniapp-global-home-floating-button`、`BUG-0090-admin-sku-list-publish-sort-order`、`BUG-0091-miniapp-product-list-sort-consistency`、`BUG-0092-miniapp-card-images-slow-load` 与 `BUG-0093-miniapp-category-secondary-grid-name-full-display`：一方面保持发布镜像准备与构建治理的归档成果，另一方面完成管理后台瓷砖类目名称规则调整、Web 标准弹窗防误关闭策略、小程序品牌列表页和全局返回首页导航体验，并修复管理端 SKU 列表排序、小程序商品排序、商品卡片图片加载和分类页二级类目长名称展示问题。

正式范围：

- `REQ-0081-release-image-build-governance`
- `REQ-0082-admin-category-name-special-characters`
- `REQ-0083-miniapp-brand-list-category-summary`
- `REQ-0084-web-modal-disable-outside-close`
- `REQ-0085-miniapp-global-home-floating-button`
- `BUG-0090-admin-sku-list-publish-sort-order`
- `BUG-0091-miniapp-product-list-sort-consistency`
- `BUG-0092-miniapp-card-images-slow-load`
- `BUG-0093-miniapp-category-secondary-grid-name-full-display`

### REQ-0081-release-image-build-governance 要点

- 新增 `/image-prepare <version>`，负责读取 `release.json`、校验版本/tag/Compose/Dockerfile/构建 env/schema/migration 等输入，并生成 `releases/<version>/image-build-plan.json`。
- 新增 `/image-build <version>`，负责基于有效 plan 复用或封装 `scripts/build-images.sh`，构建 backend/web 镜像、执行验证、导出离线包和生成 `image-manifest.json`。
- 发布流程必须判断 `image_required`，并在需要时要求 image prepare / image build 证据进入 `release.json` 门禁。
- 数据库 schema 或 migration 变更必须进入 image plan 与 manifest input hash，发布确认阶段需阻断 manifest 过期或输入漂移。
- Docker、buildx、网络或基础镜像源不可用时只能记录 blocker 或外部构建证据，不得伪造成功 manifest。

### REQ-0082-admin-category-name-special-characters 要点

- 管理后台类目新增 / 编辑弹窗的类目名称规则调整为最多 15 个用户可见字符，并允许中文、英文、数字和常见可见特殊字符。
- 后端创建 / 更新类目 API 必须接受合法特殊字符名称，并拒绝空名称、16 字符名称、换行、制表符和不可见控制字符。
- OpenAPI / Orval / API 文档 / 测试夹具不得保留“只能包含中文、英文和数字”的有效约束。
- 管理端类目列表、类目树、SKU 类目选择器、小程序分类页和 Web 展示端分类入口需回归特殊字符名称展示兼容性。
- 管理端左侧类目树默认仅显示一级类目，二级及以下默认收起；有子级类目前置 `+/-` 展开 / 收起控件，展开操作不得触发筛选。
- 实现阶段必须承接 admin-list 与 admin-modal 横切 AC：分页 DOM、fixed toast、DS confirm、无 `window.confirm`、弹窗 computed width 和矮视口滚动不回归。

### REQ-0083-miniapp-brand-list-category-summary 要点

- 小程序品牌列表页顶部轮播图保持既有视觉、数据来源、指示器、自动播放和点击行为不变。
- 下半部品牌列表从双列品牌卡片调整为每行一个品牌的信息行。
- 品牌行左侧展示品牌 Logo、品牌名称和该品牌公开商品数量；右侧展示该品牌公开商品对应的末级类目名称集合。
- 商品数量与末级类目集合必须使用同一小程序公开商品口径，过滤未公开、停用、下架或内部数据。
- 如现有品牌列表接口缺少 `productCount` 或 `leafCategoryNames`，实现阶段必须同步公开 API 契约、OpenAPI、Orval 或小程序 API 类型、接口文档与测试。
- 小程序验收必须覆盖 DevTools 320、375、430 pt evidence；真机不可用时标记 blocked 或 follow_up，不得写作真机通过。

### REQ-0084-web-modal-disable-outside-close 要点

- Web 管理端和 Web 展示端标准 Dialog / Modal 点击遮罩或弹窗外空白区域时必须保持打开。
- 表单弹窗、确认弹窗、详情/预览弹窗和含上传控件弹窗必须保留明确关闭入口，例如关闭图标、取消按钮、返回按钮或业务完成关闭。
- 现有品牌启停确认、SKU 弹窗滚动修复等旧规格中的“遮罩关闭弹窗”需按本 Change 更新为“遮罩不关闭，取消/关闭图标/Esc/确认等明确动作结束流程”。
- Popover、Dropdown、Tooltip、Select 下拉层、日期选择器等轻量浮层默认不纳入本需求。
- 实现阶段必须承接 admin-modal 与 media-upload 横切 AC：无 `modal-card` 双类挂载、computed width、矮视口 body scroll、上传状态机和同会话即时回显不回归。
- 本 Change 不修改后端 API、数据库、OpenAPI、Orval、小程序、MinIO、Nginx 或 Docker Compose。

### REQ-0085-miniapp-global-home-floating-button 要点

- 小程序首页不展示返回首页悬浮按钮，避免首页出现重复入口。
- 搜索结果页、分类列表页、分类商品列表页、品牌列表页、品牌详情页、证书列表页、收藏列表页、商品详情页等主要非首页业务页面展示统一返回首页悬浮按钮。
- 点击悬浮按钮后必须快速回到首页；首页为 TabBar 页面时优先使用 `wx.switchTab` 或项目确认等价策略，首页非 TabBar 或需重置页面栈时使用 `wx.reLaunch` 或等价策略。
- 悬浮按钮必须避让底部 TabBar、底部固定操作区、系统安全区、客服/分享/咨询类悬浮入口和页面核心内容。
- 登录页、授权页、错误页、全屏视频页、图片预览页等特殊页面必须在实现阶段明确展示或豁免理由。
- 小程序验收必须引用 `docs/knowledge-base/best-practices/miniapp-custom-navigation.md`，覆盖 DevTools 320/375/430 pt evidence；真机不可用时标记 blocked 或 follow_up，不得写作真机通过。

### BUG-0093-miniapp-category-secondary-grid-name-full-display 要点

- 小程序分类页右侧二级类目卡片从每行 3 个调整为每行 2 个。
- 二级类目加载态 skeleton 必须与实际卡片保持两列布局一致。
- 所有二级类目名称必须完整显示，不出现 `...`、行数截断或隐藏溢出。
- 长名称允许自然换行，但不得遮挡相邻卡片、一级类目列表、当前一级类目标题、“查看全部商品”入口、导航栏或底部 TabBar。
- 点击二级类目仍进入对应商品列表页，`categoryId`、`categoryName`、`categoryLevel=secondary` 和 `sourcePage=category` 语义不变。

### BUG-0092-miniapp-card-images-slow-load 要点

- 小程序首页、商品列表、搜索和品牌详情商品 Tab 的商品卡片图片加载性能与稳定性需要修复。
- 修复需关注公开 SKU 图片 URL、受控媒体读取缓存与观测、MinIO thumbnails 前缀和对象引用一致性。
- 若涉及 API、DB、Orval 或 docs，必须同步对应契约、文档和测试。

### BUG-0090-admin-sku-list-publish-sort-order 要点

- Web 管理端 SKU 列表默认排序不应继续按更新时间排序。
- 已发布 SKU 按 `published_at DESC`，未发布 SKU 按 `created_at DESC`，混排时已发布分组优先。
- 搜索、品牌筛选、类目筛选、状态筛选、素材完整度筛选和分页必须保持同一排序契约。
- 若仅调整默认排序 SQL 且不新增接口字段，预计不需要 Orval；若新增排序参数或响应字段，必须同步 OpenAPI、Orval、docs 和测试。

### BUG-0091-miniapp-product-list-sort-consistency 要点

- 小程序搜索商品结果页和分类商品列表页的商品排序需与品牌详情页商品 Tab 保持一致。
- 默认排序基准为 SKU 发布时间 `published_at` 升序、SKU ID 升序；`published_at` 为空时使用 `created_at` 兜底。
- 分页加载更多后必须保持整体排序稳定，不出现重复、漏项或顺序漂移。
- 首页“全部产品”列表不纳入本 BUG 修复范围，排序保持既有策略。
- 若搜索结果页存在相关性排序，必须在实现和验收材料中明确相关性与默认排序的优先级。

## 2. Scope

| 类型 | 编号 | 标题 | 状态 | 估算 | 说明 |
|---|---|---|---|---:|---|
| REQ | REQ-0081-release-image-build-governance | 发布镜像准备与构建治理 | done | 8.0 人天 | archived `update-release-image-build-governance`（2026-07-29 16:07:14） |
| REQ | REQ-0082-admin-category-name-special-characters | 管理后台瓷砖类目名称允许特殊字符 | done | 3.0 人天 | archived `update-admin-category-name-special-characters`（2026-07-31 00:05:01） |
| REQ | REQ-0083-miniapp-brand-list-category-summary | 小程序品牌列表页按品牌单行展示类目汇总 | done | 3.0 人天 | archived `update-miniapp-brand-list-category-summary`（2026-07-31 00:30:54） |
| REQ | REQ-0084-web-modal-disable-outside-close | Web 端所有弹窗禁用点击空白区域自动关闭 | done | 3.0 人天 | archived `update-web-modal-disable-outside-close`（2026-07-31 00:07:41） |
| REQ | REQ-0085-miniapp-global-home-floating-button | 小程序非首页页面新增返回首页全局悬浮按钮 | done | 3.0 人天 | archived `add-miniapp-global-home-floating-button`（2026-07-31 00:03:10） |
| BUG | BUG-0090-admin-sku-list-publish-sort-order | 管理端 SKU 列表默认排序未按发布状态使用业务时间 | done | 1.0 人天 | archived `fix-admin-sku-list-publish-sort-order`（2026-07-31 00:18:00） |
| BUG | BUG-0092-miniapp-card-images-slow-load | 小程序体验版商品卡片图片加载很慢 | done | 5.0 人天 | archived `fix-miniapp-card-image-loading`（2026-07-30 23:43:51） |
| BUG | BUG-0093-miniapp-category-secondary-grid-name-full-display | 小程序分类页二级类目卡片 3 列布局导致名称未完整显示 | done | 1.0 人天 | archived `fix-miniapp-category-secondary-grid-name-display`（2026-07-30 23:48:19） |
| BUG | BUG-0091-miniapp-product-list-sort-consistency | 小程序搜索商品结果页与分类商品列表页排序需与品牌详情页一致 | done | 1.0 人天 | archived `fix-miniapp-product-list-sort-consistency`（2026-07-31 00:22:58） |

<!-- workflow-sync:scope-requirements:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| REQ-0081 | 发布镜像准备与构建治理 | P1 | done | archived `update-release-image-build-governance`（2026-07-29 16:07:14） |
| REQ-0082 | 管理后台瓷砖类目名称允许特殊字符 | P1 | done | archived `update-admin-category-name-special-characters`（2026-07-31 00:05:01） |
| REQ-0083 | 小程序品牌列表页按品牌单行展示类目汇总 | P1 | done | archived `update-miniapp-brand-list-category-summary`（2026-07-31 00:30:54） |
| REQ-0084 | Web 端所有弹窗禁用点击空白区域自动关闭 | P1 | done | archived `update-web-modal-disable-outside-close`（2026-07-31 00:07:41） |
| REQ-0085 | 小程序非首页页面新增返回首页全局悬浮按钮 | P1 | done | archived `add-miniapp-global-home-floating-button`（2026-07-31 00:03:10） |
<!-- workflow-sync:scope-requirements:end -->

<!-- workflow-sync:scope-bugs:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| BUG-0090 | 管理端 SKU 列表默认排序未按发布状态使用业务时间 | medium | done | archived `fix-admin-sku-list-publish-sort-order`（2026-07-31 00:18:00） |
| BUG-0092 | 小程序体验版商品卡片图片加载很慢 | high | done | archived `fix-miniapp-card-image-loading`（2026-07-30 23:43:51） |
| BUG-0093 | 小程序分类页二级类目卡片 3 列布局导致名称未完整显示 | medium | done | archived `fix-miniapp-category-secondary-grid-name-display`（2026-07-30 23:48:19） |
| BUG-0091 | 小程序搜索商品结果页与分类商品列表页排序需与品牌详情页一致 | medium | done | archived `fix-miniapp-product-list-sort-consistency`（2026-07-31 00:22:58） |
<!-- workflow-sync:scope-bugs:end -->

<!-- workflow-sync:scope-changes:start -->
| Change ID | 关联需求 | 状态 | Sprint 目标 |
|---|---|---|---|
| `update-release-image-build-governance` | REQ-0081-release-image-build-governance | archived | archived `update-release-image-build-governance`（2026-07-29 16:07:14） |
| `update-admin-category-name-special-characters` | REQ-0082-admin-category-name-special-characters | archived | archived `update-admin-category-name-special-characters`（2026-07-31 00:05:01） |
| `update-miniapp-brand-list-category-summary` | REQ-0083-miniapp-brand-list-category-summary | archived | archived `update-miniapp-brand-list-category-summary`（2026-07-31 00:30:54） |
| `update-web-modal-disable-outside-close` | REQ-0084-web-modal-disable-outside-close | archived | archived `update-web-modal-disable-outside-close`（2026-07-31 00:07:41） |
| `fix-miniapp-card-image-loading` | BUG-0092-miniapp-card-images-slow-load | archived | archived `fix-miniapp-card-image-loading`（2026-07-30 23:43:51） |
| `fix-miniapp-category-secondary-grid-name-display` | BUG-0093-miniapp-category-secondary-grid-name-full-display | archived | archived `fix-miniapp-category-secondary-grid-name-display`（2026-07-30 23:48:19） |
| `add-miniapp-global-home-floating-button` | REQ-0085-miniapp-global-home-floating-button | archived | archived `add-miniapp-global-home-floating-button`（2026-07-31 00:03:10） |
| `fix-miniapp-product-list-sort-consistency` | BUG-0091-miniapp-product-list-sort-consistency | archived | archived `fix-miniapp-product-list-sort-consistency`（2026-07-31 00:22:58） |
| `fix-admin-sku-list-publish-sort-order` | BUG-0090-admin-sku-list-publish-sort-order | archived | archived `fix-admin-sku-list-publish-sort-order`（2026-07-31 00:18:00） |
<!-- workflow-sync:scope-changes:end -->

Change：已回填 9 个范围项关联 Change；2 archived，6 applied，0 in_progress，1 proposed。执行开发与归档时以 Scope 表逐项状态为准。

## 3. 工作量与容量

| 项 | 值 |
|---|---:|
| developers | 2 |
| testers | 1 |
| capacity_person_days | 30 |
| estimated_story_points | 28 |
| estimated_person_days | 28.0 |
| capacity_usage | 93.33% |
| fix_buffer_person_days | 2.0 |
| fix_buffer_ratio | 6.67% |

容量门禁：Pass。`project.yaml` 未提供显式 Sprint 容量，沿用 sprint-013 已确认容量基线 2 dev + 1 tester / 30 人天。本 Sprint 当前纳入 5 个 REQ、4 个 BUG 与 9 个 Change，估算 28.0 人天，占用 93.33%，低于 30 人天容量，满足容量硬门禁。当前 fix buffer 为 2.0 人天 / 6.67%，明显低于建议 30%，需冻结后续新增范围，优先完成已纳入项；若出现 P0 缺陷，需移出低优先级未实现项后重新规划。

## 4. 里程碑

| 阶段 | 目标日期 | 交付 |
|---|---|---|
| 规划确认 | 2026-07-29 15:51:41 | Sprint 四件套、REQ/Change trace 同步 |
| 追加范围确认 | 2026-07-30 22:55:04 | REQ-0082 与 `update-admin-category-name-special-characters` 纳入 Sprint 正式范围 |
| 品牌列表范围确认 | 2026-07-30 23:04:59 | REQ-0083 与 `update-miniapp-brand-list-category-summary` 纳入 Sprint 正式范围 |
| 分类页缺陷范围确认 | 2026-07-30 23:21:51 | BUG-0093 与 `fix-miniapp-category-secondary-grid-name-display` 纳入 Sprint 正式范围 |
| 返回首页悬浮按钮范围确认 | 2026-07-30 23:26:20 | REQ-0085 与 `add-miniapp-global-home-floating-button` 纳入 Sprint 正式范围 |
| Web 弹窗关闭策略范围确认 | 2026-07-30 23:33:30 | REQ-0084 与 `update-web-modal-disable-outside-close` 纳入 Sprint 正式范围 |
| SKU 列表排序缺陷范围确认 | 2026-07-30 23:36:11 | BUG-0090 与 `fix-admin-sku-list-publish-sort-order` 纳入 Sprint 正式范围 |
| 实现完成 | 2026-08-05 18:00:00 | 类目名称特殊字符规则、API / Orval、管理端、小程序/Web 展示回归、文档和测试完成 |
| 验收归档 | 2026-08-12 18:00:00 | Change archive、REQ archive、发布说明与验收报告闭环 |

## 5. 风险

| 风险 | 缓解 |
|---|---|
| `/image-prepare` 与 `/image-build` 边界混淆，导致准备阶段隐式执行真实构建 | 技能文档明确 prepare 只生成 plan 和 blocker，真实构建只由 build 或明确等价流程承载 |
| release gates 只记录 warning，未真正阻断 manifest 缺失或过期 | `scripts/validate-release.py` 增加强门禁，缺 plan/manifest、版本/tag 不一致、input hash 漂移均失败 |
| 数据库 schema / migration 变更没有进入镜像输入快照 | image plan 统一收集 SQLite schema、MySQL schema、migration、数据库文档和回滚说明 hash |
| 敏感信息被写入 plan、manifest、公告或 AI usage | 校验脚本扫描 `.env` 内容、连接串、Authorization header、Cookie、密钥和本机绝对路径 |
| `unify-image-version-env` 已完成但未归档，版本变量规则重复定义 | apply 阶段优先复用其统一 tag 决策，只在 release/image 门禁层补证据契约 |
| Docker 或网络不可用导致本地无法产出 manifest | 记录 blocker 与人工外部构建证据字段，要求来源、校验方式、sha256 和风险说明 |
| 类目名称特殊字符前后端校验口径不一致 | 后端 Schema/Service 作为事实源，OpenAPI 导出后 Orval 生成，前端表单和 pytest/Vitest 覆盖相同合法/非法样例 |
| 特殊字符或 15 字符名称导致列表、树、选择器、小程序分类入口布局异常 | 执行 admin-list/admin-modal 横切 AC，并用 `岩板-大规格`、`仿古砖/客厅`、`600x1200(亮面)`、`A+B#系列` 做多端展示回归 |
| 品牌列表公开接口缺少商品数量或末级类目集合 | apply 阶段先确认接口契约；缺字段时同步扩展公开 API、OpenAPI、Orval 或小程序 API 类型和测试 |
| 小程序品牌行右侧类目过多导致小屏拥挤 | 使用折行、限行省略或“等 N 类”策略，并按 320/375/430 pt 记录 evidence |
| 小程序分类页二级类目长名称回归再次漏验 | BUG-0093 apply 必须同时验证两列布局、skeleton 一致性、完整名称展示、长名称换行和二级类目点击路由 |
| 小程序返回首页悬浮按钮遮挡底部操作区或已有悬浮入口 | REQ-0085 apply 必须先梳理页面覆盖/例外清单，对商品详情底部操作区、TabBar、安全区、客服/分享/咨询入口配置避让或豁免 |
| 搜索/分类商品列表排序修复误改首页全部产品或搜索相关性 | BUG-0091 apply 必须把首页“全部产品”列为不变回归项，并在存在相关性排序时明确相关性与默认发布时间排序优先级 |
| 新增 REQ-0085 后 fix buffer 低于建议 30% | 本 Sprint 后续不得继续扩大小程序范围；优先完成 REQ-0085、BUG-0092、BUG-0093 后再评估新增项 |
| 新增 REQ-0084 后 fix buffer 降至 6.67% | 本 Sprint 后续冻结新增范围，优先完成已纳入 9 个 Change；若出现 P0 缺陷，需移出低优先级未实现项后重新规划 |
| Web 弹窗策略修改可能遗漏历史自定义弹窗 | apply 阶段先盘点管理端与展示端标准 Dialog / Modal，优先修改共享封装，再补齐 feature-local 自定义弹窗 |
| 旧测试仍断言遮罩关闭弹窗 | apply 阶段更新测试语义，覆盖外部点击保持打开、明确关闭入口可关闭、确认弹窗不调用业务 API |
| SKU 列表排序契约与历史 `updated_at` 默认规则冲突 | 以 `fix-admin-sku-list-publish-sort-order` delta spec 为准，后端统一排序，测试覆盖已发布、未发布、混排、空时间和分页稳定 |
| 小程序真机或 DevTools evidence 不完整 | 承接 sprint-013 复盘，DevTools 与真机状态分开记录；真机不可用时标记 blocked 或 follow_up |

## 6. 知识库承接

| 来源 | 承接动作 |
|---|---|
| `docs/knowledge-base/retrospectives/sprint-013-retrospective.md` | 控制 Scope 薄片化，本 Sprint 只纳入 REQ-0081 与对应 Change，不把发布版本计划、CI/CD、远程镜像推送扩大进来。 |
| `docs/knowledge-base/retrospectives/sprint-013-retrospective.md` | apply/archive 阶段优先补齐 Change trace、release-note 和 acceptance 同步，避免归档后靠 fallback 补证据。 |
| `docs/knowledge-base/retrospectives/sprint-013-retrospective.md` | 对命令治理类改动使用增量读取和脚本校验，避免重复读取完整历史归档与大生成物。 |
| `docs/knowledge-base/retrospectives/sprint-013-retrospective.md` | 管理端 UI 问题重复出现，REQ-0082 apply 前必须前置 admin-list/admin-modal 验收模板。 |
| `docs/knowledge-base/retrospectives/sprint-013-retrospective.md` | 小程序 evidence 作为独立发布边界管理，REQ-0083 必须尽早安排 DevTools 320/375/430 pt 视口验收，真机不可用时保留 blocked/follow_up。 |
| `docs/knowledge-base/retrospectives/sprint-013-retrospective.md` | 涉及排序的 BUG 必须写清事实字段、空值策略和不影响分支；BUG-0090 apply 必须区分 `published_at`、`created_at` 与 `updated_at`。 |
| `docs/knowledge-base/best-practices/admin-list-page-consistency.md` | 类目列表回归必须覆盖分页 DOM、fixed toast、DS confirm 和无 `window.confirm`。 |
| `docs/knowledge-base/best-practices/admin-list-page-consistency.md` | BUG-0090 管理端 SKU 列表回归必须覆盖分页 DOM、发布时间/更新时间列、fixed toast、无 `window.confirm` 和当前页不做本地跨页排序。 |
| `docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md` | 类目新增 / 编辑弹窗回归必须覆盖无双类挂载、computed width 和矮视口滚动。 |
| `docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md` | REQ-0084 Web 弹窗策略必须覆盖无 `modal-card` 双类挂载、computed width、矮视口滚动和明确关闭入口可达。 |
| `docs/knowledge-base/best-practices/admin-media-upload-chain.md` | REQ-0084 如触及含上传控件弹窗，必须覆盖上传状态机、同会话即时回显和失败态展示；若未触及上传链路，Docker `:3000` 上传边界可按 AC 标记 N/A。 |
| `docs/knowledge-base/best-practices/miniapp-custom-navigation.md` | 品牌列表页回归必须覆盖自定义导航 offset、胶囊避让、返回兜底、首屏轮播、品牌单行列表和底部 TabBar。 |
| `docs/knowledge-base/best-practices/miniapp-custom-navigation.md` | BUG-0093 分类页回归必须覆盖 TabBar 页面首屏内容、标题与胶囊避让、底部 TabBar 遮挡、DevTools 320/375/430 pt evidence 和真机 blocked/follow_up 边界。 |
| `docs/knowledge-base/best-practices/miniapp-custom-navigation.md` | REQ-0085 返回首页悬浮按钮必须覆盖首页隐藏、非首页展示、页面栈/首页兜底、安全区/TabBar/固定操作区避让、DevTools 320/375/430 pt evidence 和真机 blocked/follow_up 边界。 |
| `docs/knowledge-base/retrospectives/sprint-013-retrospective.md` | BUG-0091 承接品牌商品排序经验：涉及排序的 BUG 必须写清事实字段、空值策略、不影响的排序分支，并避免小程序端跨页重排。 |

## 7. 横切预防清单

- [ ] `/image-prepare` 必须拒绝缺失 `release.json` 的版本，不得猜测发布范围。
- [ ] `/image-build` 必须拒绝缺失或过期的 `image-build-plan.json`。
- [ ] `image-build-plan.json` 和 `image-manifest.json` 不得包含真实 `.env`、密钥、数据库连接串、Authorization header、Cookie、真实客户数据或本机绝对路径。
- [ ] `release.json` 在 `image_required=true` 时必须引用 image plan；需要交付镜像时必须引用有效 manifest 或受控外部构建证据。
- [ ] 数据库 schema、migration、Dockerfile、Compose、构建脚本、构建 env 示例、Nginx 配置和相关发布文档进入 input hash。
- [ ] manifest 生成后如输入 hash 漂移，`/release-publish` 必须阻断或要求重新构建。
- [ ] 命令成功输出保持 compact summary，只展示版本、是否需要镜像、证据路径、blocker 和下一步命令。
- [ ] AI usage hook 支持 `image.prepare` 与 `image.build` 归因到 release version，且不持久化 prompt、skill body、路径和敏感值。
- [ ] 类目列表如因 REQ-0082 调整展示或测试，分页 DOM 必须与用户管理基准一致，反馈使用 fixed toast。
- [ ] 类目启停、删除等状态变更若被触达修改，必须使用 DS confirm modal；不得新增 `window.confirm`。
- [ ] 类目新增 / 编辑弹窗不得同时挂载通用 `modal-card` 与业务专属类，1440px computed width 与矮视口滚动需验收。
- [ ] 特殊字符类目名称在管理端类目树、列表、选择器、小程序分类入口和 Web 展示入口不得重叠、遮挡或撑破容器。
- [ ] SKU 列表默认排序必须由后端分页查询统一保证，不得只在 Web 当前页本地排序。
- [ ] SKU 列表发布时间列、更新时间列、分页 DOM、fixed toast、操作列和无 `window.confirm` 在 BUG-0090 apply 后不回归。
- [ ] SKU 列表排序测试必须覆盖已发布 `published_at`、未发布 `created_at`、混排、空发布时间、同时间和分页稳定。
- [ ] 品牌列表页顶部轮播在 REQ-0083 apply 后保持视觉、数据来源、指示器、自动播放和点击行为不变。
- [ ] 品牌单行列表在 320、375、430 pt 宽度下无文字重叠、Logo 拉伸、横向滚动、类目覆盖左侧信息或底部 TabBar 遮挡。
- [ ] 品牌公开商品数量与末级类目集合使用同一公开商品口径，并过滤未公开、停用、下架或内部数据。
- [ ] 分类页二级类目卡片必须每行 2 个，加载态 skeleton 同步两列。
- [ ] 分类页二级类目名称完整展示，不得使用 `...`、line-clamp 或隐藏溢出省略名称。
- [ ] 分类页长名称换行后不得遮挡标题、“查看全部商品”、左侧一级类目、底部 TabBar 或点击热区。
- [ ] 返回首页悬浮按钮在首页隐藏，在搜索结果页、分类列表页、分类商品列表页、品牌列表页、品牌详情页、证书列表页、收藏列表页、商品详情页等非首页业务页面展示。
- [ ] 返回首页悬浮按钮点击后可安全进入首页，连续点击不会重复跳转或堆叠首页。
- [ ] 返回首页悬浮按钮不得遮挡底部 TabBar、商品详情底部操作区、客服/分享/咨询类悬浮入口、安全区或页面核心内容。
- [ ] 登录页、授权页、错误页、全屏视频页、图片预览页等特殊页面必须记录展示或豁免理由。
- [ ] 搜索商品结果页和分类商品列表页默认排序必须与品牌详情页商品 Tab 一致，按 `published_at` 升序、SKU ID 升序，空 `published_at` 使用 `created_at` 兜底。
- [ ] 商品列表分页加载更多不得出现重复、漏项或已加载商品顺序跳动。
- [ ] 首页“全部产品”、新品榜、热销榜、价格排序和明确的搜索相关性排序不得被 BUG-0091 默认排序修复误改。
- [ ] Web 管理端和展示端标准 Dialog / Modal 点击遮罩或弹窗外空白区域时必须保持打开。
- [ ] 表单弹窗、确认弹窗、详情/预览弹窗和含上传控件弹窗必须保留可见明确关闭入口。
- [ ] 确认弹窗点击外部不得关闭，也不得调用启停、删除、上下架、批量操作或设置保存等目标 API。
- [ ] REQ-0084 修改触及的管理端弹窗不得同时挂载通用 `modal-card` 与业务专属类，1440px computed width 和矮视口 body scroll 必须验收。
- [ ] REQ-0084 若触及上传控件，必须覆盖 `idle -> uploading -> done/failed`、同会话即时回显和失败态展示；若未触及上传链路，Docker `:3000` 上传边界需标记 N/A 原因。
- [ ] 真机验收不可用时必须在 acceptance-report 标记 blocked 或 follow_up，不得把 DevTools 截图写作真机通过。

## 8. 依赖关系

```text
REQ-0081-release-image-build-governance
└── update-release-image-build-governance
    ├── product-release-management
    │   └── release gates: image_required / image_prepare / image_build
    ├── deployment-image-build
    │   ├── image-build-plan.json
    │   └── image-manifest.json
    ├── deployment
    │   └── Compose / Dockerfile / schema / migration 输入一致性
    └── agent-workflow-tooling
        ├── /image-prepare
        └── /image-build

REQ-0082-admin-category-name-special-characters
└── update-admin-category-name-special-characters
    ├── tile-category-management
    │   ├── create/update API validation
    │   ├── OpenAPI / Orval contract
    │   └── database constraint check
    ├── web-admin
    │   ├── CategoryFormModal
    │   ├── category list/tree/selector
    │   └── admin-list/admin-modal cross-cutting AC
    └── miniapp / web-catalog
        └── category display compatibility

REQ-0083-miniapp-brand-list-category-summary
└── update-miniapp-brand-list-category-summary
    ├── miniapp-brand-list-page
    │   ├── keep existing top brand swiper
    │   ├── single brand row layout
    │   └── DevTools 320/375/430 pt evidence
    ├── backend / api
    │   ├── public brand productCount
    │   └── leafCategoryNames aggregation
    └── safety / analytics
        ├── secure Logo URL
        └── non-blocking brand row analytics

REQ-0084-web-modal-disable-outside-close
└── update-web-modal-disable-outside-close
    ├── web-client
    │   ├── standard Dialog / Modal outside click disabled
    │   ├── admin form / confirm / upload dialogs
    │   └── web catalog detail / preview dialogs
    └── design-system
        ├── shared Dialog default behavior
        ├── explicit close affordances
        └── admin-modal / media-upload cross-cutting gates

REQ-0085-miniapp-global-home-floating-button
└── add-miniapp-global-home-floating-button
    ├── miniapp-global-custom-navigation-bar
    │   ├── home hidden / non-home visible
    │   ├── switchTab / reLaunch home navigation strategy
    │   ├── duplicate tap guard
    │   └── DevTools 320/375/430 pt evidence
    └── miniapp pages
        ├── search result page
        ├── category product list page
        ├── brand detail page
        └── SKU detail page fixed action-bar avoidance

BUG-0093-miniapp-category-secondary-grid-name-full-display
└── fix-miniapp-category-secondary-grid-name-display
    └── miniapp-category-list-page
        ├── secondary grid: 2 columns
        ├── skeleton grid: 2 columns
        ├── full secondary name display
        └── secondary category route unchanged

BUG-0091-miniapp-product-list-sort-consistency
└── fix-miniapp-product-list-sort-consistency
    └── miniapp-product-list-page
        ├── search result default sorting
        ├── primary / secondary category product list sorting
        ├── brand detail product Tab sorting baseline
        ├── pagination stable secondary sort
        └── home all-products unchanged

BUG-0090-admin-sku-list-publish-sort-order
└── fix-admin-sku-list-publish-sort-order
    └── tile-sku-management
        ├── backend default ordering by status + business time
        ├── published SKU: published_at DESC
        ├── unpublished SKU: created_at DESC
        ├── stable fallback ordering for null/equal timestamps
        └── web admin list pagination and date columns unchanged
```

## 9. 发布计划

本 Sprint 完成后应进入产品版本发布流程，优先纳入下一次包含部署治理能力与管理端类目规则优化的版本计划。发布前需要运行 OpenSpec validate、相关 pytest、前端测试、release validator、image plan/manifest validator、敏感信息扫描，以及 Docker Compose config 静态校验；若执行真实镜像构建，还需运行 `/image-build <version>` 并记录 manifest。

REQ-0083 若涉及公开品牌列表 API 契约扩展，还需在发布说明中明确小程序品牌列表页的用户可见变化与接口兼容边界；若仅小程序端消费既有字段，则发布说明记录为小程序体验优化。REQ-0084 发布说明应记录为 Web 弹窗交互体验优化：管理端与展示端标准 Dialog / Modal 点击外部空白区域不再自动关闭，并保留明确关闭入口；若实现保持前端交互层调整，则不标记 API、数据库、Orval、小程序或 Docker 影响。REQ-0085 发布说明应记录为小程序导航体验优化；若实现不新增接口、数据库或管理配置，则不标记 API、数据库或 Orval 影响。BUG-0093 发布说明应记录为小程序分类页体验修复；若实现保持样式和路由层调整，则不标记 API、数据库或 Orval 影响。BUG-0091 发布说明应记录为小程序搜索/分类商品列表排序一致性修复；若实现仅调整后端默认排序且不改变请求/响应字段，API 契约可标记为语义修复但仍需补后端排序测试。BUG-0090 发布说明应记录为管理端 SKU 列表默认排序修复；若仅修改默认排序 SQL 且不改变请求/响应字段，则不标记 API、数据库或 Orval 影响。

## 10. 关联文档

| 类型 | 路径 |
|---|---|
| Requirement | `issues/requirements/archive/REQ-0081-release-image-build-governance/requirement.md` |
| Acceptance | `issues/requirements/archive/REQ-0081-release-image-build-governance/acceptance.md` |
| Requirement Trace | `issues/requirements/archive/REQ-0081-release-image-build-governance/trace.md` |
| OpenSpec Change | `openspec/archive/2026-07-29-update-release-image-build-governance/` |
| Requirement | `issues/requirements/archive/REQ-0082-admin-category-name-special-characters/requirement.md` |
| Acceptance | `issues/requirements/archive/REQ-0082-admin-category-name-special-characters/acceptance.md` |
| Requirement Trace | `issues/requirements/archive/REQ-0082-admin-category-name-special-characters/trace.md` |
| OpenSpec Change | `openspec/archive/2026-07-31-update-admin-category-name-special-characters/` |
| Requirement | `issues/requirements/archive/REQ-0083-miniapp-brand-list-category-summary/requirement.md` |
| Acceptance | `issues/requirements/archive/REQ-0083-miniapp-brand-list-category-summary/acceptance.md` |
| Requirement Trace | `issues/requirements/archive/REQ-0083-miniapp-brand-list-category-summary/trace.md` |
| OpenSpec Change | `openspec/archive/2026-07-31-update-miniapp-brand-list-category-summary/` |
| Requirement | `issues/requirements/archive/REQ-0084-web-modal-disable-outside-close/requirement.md` |
| Acceptance | `issues/requirements/archive/REQ-0084-web-modal-disable-outside-close/acceptance.md` |
| Requirement Trace | `issues/requirements/archive/REQ-0084-web-modal-disable-outside-close/trace.md` |
| OpenSpec Change | `openspec/archive/2026-07-31-update-web-modal-disable-outside-close/` |
| Requirement | `issues/requirements/archive/REQ-0085-miniapp-global-home-floating-button/requirement.md` |
| Acceptance | `issues/requirements/archive/REQ-0085-miniapp-global-home-floating-button/acceptance.md` |
| Requirement Trace | `issues/requirements/archive/REQ-0085-miniapp-global-home-floating-button/trace.md` |
| OpenSpec Change | `openspec/archive/2026-07-31-add-miniapp-global-home-floating-button/` |
| Bug | `issues/bugs/archive/BUG-0093-miniapp-category-secondary-grid-name-full-display/bug.md` |
| Bug Acceptance | `issues/bugs/archive/BUG-0093-miniapp-category-secondary-grid-name-full-display/acceptance.md` |
| Bug Trace | `issues/bugs/archive/BUG-0093-miniapp-category-secondary-grid-name-full-display/trace.md` |
| OpenSpec Change | `openspec/archive/2026-07-30-fix-miniapp-category-secondary-grid-name-display/` |
| Bug | `issues/bugs/archive/BUG-0091-miniapp-product-list-sort-consistency/bug.md` |
| Bug Acceptance | `issues/bugs/archive/BUG-0091-miniapp-product-list-sort-consistency/acceptance.md` |
| Bug Trace | `issues/bugs/archive/BUG-0091-miniapp-product-list-sort-consistency/trace.md` |
| OpenSpec Change | `openspec/archive/2026-07-30-fix-miniapp-product-list-sort-consistency/` |
| Bug | `issues/bugs/archive/BUG-0090-admin-sku-list-publish-sort-order/bug.md` |
| Bug Acceptance | `issues/bugs/archive/BUG-0090-admin-sku-list-publish-sort-order/acceptance.md` |
| Bug Trace | `issues/bugs/archive/BUG-0090-admin-sku-list-publish-sort-order/trace.md` |
| OpenSpec Change | `openspec/archive/2026-07-31-fix-admin-sku-list-publish-sort-order/` |
| Sprint YAML | `iterations/archive/sprint-014/sprint.yaml` |
| Release Rules | `rules/release.md` |
| Deployment Docs | `docs/08-production-image-release.md` |

## 11. 关闭记录

| 时间 | 命令 | 结论 |
|---|---|---|
| 2026-07-31 08:14:33 | /sprint-archive sprint-014 | 9/9 Change 已归档；readiness PASS；Issue promote 无待迁移项；Sprint 状态切换为 completed/archive。 |

## 12. 复盘回链

| 时间 | 命令 | 文档 |
|---|---|---|
| 2026-07-31 08:18:50 | /sprint-exps sprint-014 | `docs/knowledge-base/retrospectives/sprint-014-retrospective.md` |
