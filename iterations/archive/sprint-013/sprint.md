---
note: workflow-sync — workflow-sync 自动同步 — 8/8 Change archived；0 applied；Sprint `completed`
sprint_id: sprint-013
title: Sprint 013 类目名称、备注展示、证书多图、证书详情、品牌排序、SKU 时间列与证书图片噪音修复
status: completed
lifecycle_stage: archive
created_at: 2026-07-28 00:24:49
updated_at: 2026-07-29 09:31:30
owner: product
---

# Sprint 013 类目名称、备注展示、证书多图、证书详情、品牌排序、SKU 时间列与证书图片噪音修复

## 1. Sprint 目标

本 Sprint 聚焦 `REQ-0077-category-name-max-length-15`、`BUG-0086-miniapp-sku-detail-remark-not-shown`、`REQ-0078-certificate-multiple-images-main-image`、`REQ-0080-miniapp-certificate-detail-page`、`BUG-0087-miniapp-brand-detail-product-tab-sort-order`、`REQ-0079-admin-sku-list-published-at` 与 `BUG-0089-admin-certificate-edit-image-filename-noise`：完成类目名称 15 字符规则闭环，修复小程序 SKU 详情页备注说明未展示问题，将管理端品牌证书增强为多图上传、唯一主图和主图缩略图展示，新增小程序证书详情页承接证书列表/品牌详情/分享入口，修正品牌详情页商品 Tab 排序，在管理端 SKU 列表新增发布时间列，并移除品牌证书新增/编辑弹窗图片说明下方的冗余文件名文本。

正式范围：

- `REQ-0077-category-name-max-length-15`
- `BUG-0086-miniapp-sku-detail-remark-not-shown`
- `REQ-0078-certificate-multiple-images-main-image`
- `REQ-0080-miniapp-certificate-detail-page`
- `REQ-0079-admin-sku-list-published-at`
- `BUG-0087-miniapp-brand-detail-product-tab-sort-order`
- `BUG-0089-admin-certificate-edit-image-filename-noise`

### REQ-0077-category-name-max-length-15 要点

- 类目名称新增 / 编辑允许 1-15 个用户可见字符。
- 16 字符及以上必须被前端和后端拒绝，错误提示表达「类目名称最多 15 个字符」。
- 不改变字符集、同层级唯一、编码自动生成、层级、排序权重、启停删除等规则。
- 需要确认 `tile_categories.name`、OpenAPI/Orval、测试夹具与展示端布局均无 10 字符残留。

### BUG-0086-miniapp-sku-detail-remark-not-shown 要点

- 小程序 SKU 详情页必须展示已维护的公开备注说明。
- 若 SKU 详情接口缺少备注说明字段，需同步 API / OpenAPI / Orval / docs / 后端契约测试。
- 备注为空时不得出现 `null`、`undefined`、字段名、异常空白卡片或布局错位。
- 回归商品主图、轮播图/视频、品牌入口、收藏、分享和异常态。

### REQ-0078-certificate-multiple-images-main-image 要点

- 管理端品牌证书新增 / 编辑弹窗支持多张图片上传、唯一主图、设置主图、删除主图兜底和删除全部图片空状态。
- 管理端证书列表和默认预览入口优先使用主图缩略图，主图加载失败时展示稳定占位。
- 后端需扩展或兼容品牌证书图片数组、主图、排序、旧单文件和 PDF/文档占位策略。
- 上传仍走后端鉴权、MIME/大小校验和对象存储适配层，不前端直连未授权对象存储。
- 需要同步 API、数据库、OpenAPI/Orval、上传/对象存储文档、后端 pytest、前端 Vitest 与 Docker Web 上传边界验收。

### REQ-0080-miniapp-certificate-detail-page 要点

- 小程序新增证书详情页，承接证书列表页、品牌详情页证书区域和微信分享入口。
- 证书列表卡片主点击改为进入详情页；详情页内保留图片预览、PDF 受控打开、品牌入口和分享能力。
- 后端需提供或扩展公开证书详情接口，过滤隐藏、软删除和不可公开品牌证书，不暴露后台备注、审计字段、对象 Key、未授权 URL 或敏感信息。
- 详情页复用商品详情页的大媒体区、信息分区、品牌入口、分享和错误态体验，但不引入收藏、推荐、价格、购物、购买、库存或询价。
- 需要同步 OpenAPI/Orval 或小程序服务层、API 文档、后端 pytest、小程序静态测试，并按 miniapp-custom-navigation 记录 DevTools/真机 evidence。

### REQ-0079-admin-sku-list-published-at 要点

- 管理端瓷砖 SKU 列表在“更新时间”前新增“发布时间”列。
- 发布时间格式、空值占位和视觉样式与更新时间保持一致。
- 实现阶段必须确认发布时间字段来源，不得直接用更新时间冒充发布时间。
- 若列表响应缺少发布时间字段，需同步后端响应、Pydantic Schema、OpenAPI/Orval、接口文档和测试。
- 不新增发布时间筛选、排序、导出、发布流程、小程序或店主端展示。

### BUG-0087-miniapp-brand-detail-product-tab-sort-order 要点

- 品牌详情页商品 Tab 仅召回当前品牌下可公开 SKU。
- `GET /api/v1/miniapp/products?brandId=<brandId>` 品牌过滤场景默认按发布时间升序、ID 升序返回。
- 发布时间使用现有 `tiles.published_at`；历史空值使用 `tiles.created_at` 兜底，不新增数据库字段。
- 保持搜索页相关性排序、新品榜近 90 天召回、热销榜 `hot_score DESC` 和普通商品列表排序不变。

### BUG-0089-admin-certificate-edit-image-filename-noise 要点

- 管理端品牌证书新增 / 编辑弹窗中，证书图片上传说明下方不得展示 `cover.webp`、`page-2.webp` 等文件名文本列表。
- 保留图片缩略图、主图标记、删除、设为主图、继续添加、上传进度和失败提示能力。
- 修复范围限定在 Web 管理端前端组件和 Vitest 回归，不改变后端 API、数据库、小程序或对象存储链路。
- 已通过 `/bug-opsx BUG-0089` 创建修复 Change，并已在 Sprint 归档前完成 apply/archive。

## 2. Scope

| 类型 | 编号 | 标题 | 状态 | 估算 | 说明 |
|---|---|---|---|---:|---|
| REQ | REQ-0077-category-name-max-length-15 | 类目名称输入最多 15 个字符 | done | 3.0 人天 | archived `update-category-name-max-length-15`（2026-07-28 00:24:49） |
| REQ | REQ-0078-certificate-multiple-images-main-image | 证书支持多图上传与主图设置 | done | 8.0 人天 | archived `update-certificate-multiple-images-main-image`（2026-07-29 00:10:51） |
| REQ | REQ-0079-admin-sku-list-published-at | 管理端瓷砖 SKU 列表新增发布时间列 | done | 1.0 人天 | archived `update-admin-sku-list-published-at`（2026-07-28 23:45:00） |
| REQ | REQ-0080-miniapp-certificate-detail-page | 微信小程序新增证书详情页 | done | 5.0 人天 | archived `add-miniapp-certificate-detail-page`（2026-07-29 08:24:32） |
| BUG | BUG-0086-miniapp-sku-detail-remark-not-shown | 小程序商品详情页备注说明信息没有显示 | done | 1.0 人天 | archived `fix-miniapp-sku-detail-remark-display`（2026-07-29 00:09:26） |
| BUG | BUG-0087-miniapp-brand-detail-product-tab-sort-order | 品牌详情页商品 Tab 排序未按发布时间升序和 ID 升序 | done | 1.0 人天 | archived `fix-miniapp-brand-detail-product-sort-order`（2026-07-29 07:54:14） |
| BUG | BUG-0088-admin-sku-edit-save-extra-step | 管理端 SKU 编辑保存成功后未直接关闭弹窗 | done | 1.0 人天 | archived `fix-admin-sku-edit-save-extra-step`（2026-07-28 23:34:32） |
| BUG | BUG-0089-admin-certificate-edit-image-filename-noise | 管理端证书编辑弹窗图片下方显示无意义文件名 | done | 0.5 人天 | archived `fix-admin-certificate-image-filename-noise`（2026-07-29 08:57:31） |

<!-- workflow-sync:scope-requirements:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| REQ-0077 | 类目名称输入最多 15 个字符 | P1 | done | archived `update-category-name-max-length-15`（2026-07-28 00:24:49） |
| REQ-0078 | 证书支持多图上传与主图设置 | P1 | done | archived `update-certificate-multiple-images-main-image`（2026-07-29 00:10:51） |
| REQ-0079 | 管理端瓷砖 SKU 列表新增发布时间列 | P1 | done | archived `update-admin-sku-list-published-at`（2026-07-28 23:45:00） |
| REQ-0080 | 微信小程序新增证书详情页 | P1 | done | archived `add-miniapp-certificate-detail-page`（2026-07-29 08:24:32） |
<!-- workflow-sync:scope-requirements:end -->

<!-- workflow-sync:scope-bugs:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| BUG-0086 | 小程序商品详情页备注说明信息没有显示 | medium | done | archived `fix-miniapp-sku-detail-remark-display`（2026-07-29 00:09:26） |
| BUG-0087 | 品牌详情页商品 Tab 排序未按发布时间升序和 ID 升序 | medium | done | archived `fix-miniapp-brand-detail-product-sort-order`（2026-07-29 07:54:14） |
| BUG-0088 | 管理端 SKU 编辑保存成功后未直接关闭弹窗 | medium | done | archived `fix-admin-sku-edit-save-extra-step`（2026-07-28 23:34:32） |
| BUG-0089 | 管理端证书编辑弹窗图片下方显示无意义文件名 | low | done | archived `fix-admin-certificate-image-filename-noise`（2026-07-29 08:57:31） |
<!-- workflow-sync:scope-bugs:end -->

<!-- workflow-sync:scope-changes:start -->
| Change ID | 关联需求 | 状态 | Sprint 目标 |
|---|---|---|---|
| `update-category-name-max-length-15` | REQ-0077-category-name-max-length-15 | archived | archived `update-category-name-max-length-15`（2026-07-28 00:24:49） |
| `fix-miniapp-sku-detail-remark-display` | BUG-0086-miniapp-sku-detail-remark-not-shown | archived | archived `fix-miniapp-sku-detail-remark-display`（2026-07-29 00:09:26） |
| `update-certificate-multiple-images-main-image` | REQ-0078-certificate-multiple-images-main-image | archived | archived `update-certificate-multiple-images-main-image`（2026-07-29 00:10:51） |
| `fix-miniapp-brand-detail-product-sort-order` | BUG-0087-miniapp-brand-detail-product-tab-sort-order | archived | archived `fix-miniapp-brand-detail-product-sort-order`（2026-07-29 07:54:14） |
| `update-admin-sku-list-published-at` | REQ-0079-admin-sku-list-published-at | archived | archived `update-admin-sku-list-published-at`（2026-07-28 23:45:00） |
| `fix-admin-sku-edit-save-extra-step` | BUG-0088-admin-sku-edit-save-extra-step | archived | archived `fix-admin-sku-edit-save-extra-step`（2026-07-28 23:34:32） |
| `add-miniapp-certificate-detail-page` | REQ-0080-miniapp-certificate-detail-page | archived | archived `add-miniapp-certificate-detail-page`（2026-07-29 08:24:32） |
| `fix-admin-certificate-image-filename-noise` | BUG-0089-admin-certificate-edit-image-filename-noise | archived | archived `fix-admin-certificate-image-filename-noise`（2026-07-29 08:57:31） |
<!-- workflow-sync:scope-changes:end -->

BUG：`BUG-0086`、`BUG-0087`、`BUG-0088`、`BUG-0089` 已纳入正式范围，优先级高于新增体验能力；当前完成度与验收风险以 Scope 表状态、关联 Change 和 acceptance-report 为准。

Change：已回填 8 个范围项关联 Change；8 archived，0 applied，0 in_progress，0 proposed。所有已纳入范围项均已关联 Change；执行开发与归档时以 Scope 表逐项状态为准。

## 3. 工作量与容量

| 项 | 值 |
|---|---:|
| developers | 2 |
| testers | 1 |
| capacity_person_days | 30 |
| estimated_story_points | 20.5 |
| estimated_person_days | 20.5 |
| capacity_usage | 68.33% |
| fix_buffer_person_days | 9.5 |
| fix_buffer_ratio | 31.67% |

容量门禁：Pass。`project.yaml` 未提供显式 Sprint 容量，沿用 sprint-012 已确认容量基线 2 dev + 1 tester / 30 人天。本 Sprint 当前纳入 4 个 REQ 与 4 个 BUG，估算 20.5 人天，占用 68.33%，fix buffer 9.5 人天 / 31.67%，满足容量门禁。

## 4. 里程碑

| 阶段 | 目标日期 | 交付 |
|---|---|---|
| 规划确认 | 2026-07-28 00:24:49 | Sprint 四件套、REQ/Change trace 同步 |
| 实现完成 | 2026-08-04 18:00:00 | 后端/API、Web 管理端、OpenAPI/Orval、测试与展示回归完成 |
| 验收归档 | 2026-08-11 18:00:00 | Change archive、REQ archive、发布说明与验收报告闭环 |

## 5. 风险

| 风险 | 缓解 |
|---|---|
| 10 字符常量在前端、后端、测试夹具或文档中残留 | apply 阶段使用 targeted `rg` 搜索 `max_length=10`、`maxLength: 10`、旧错误文案，并用 15/16 字符测试覆盖 |
| 数据库字段实际存在小于 15 的约束 | apply 前检查 SQLite schema 与 MySQL migration；若存在约束，补 migration 和 docs |
| 15 字符类目名称导致管理端/小程序/Web 展示布局拥挤 | 使用中文与英文数字 15 字符样例做列表、类目树、分类入口和筛选入口回归 |
| 小范围弹窗校验改动触发 CSS cascade 回归 | 执行 admin-modal 横切 AC：单一专属类、computed width、矮视口滚动 |
| 小程序详情页备注说明字段来源不清，误用内部备注 | 实现阶段先确认接口字段公开边界，只展示允许公开的商品/SKU 备注说明 |
| 备注说明长文本导致移动端详情信息区拥挤 | 使用包含长备注与空备注的 SKU 样例回归 320-430px 视口展示 |
| 证书多图改造影响 API/DB/Orval/旧数据兼容面较宽 | apply 阶段先落数据兼容设计和 Schema，再同步 OpenAPI/Orval、docs 与测试夹具 |
| 多图上传同会话回显或主图缩略图加载失败 | 复用 media-upload best-practice，覆盖 idle/uploading/done/failed、即时回显和稳定占位测试 |
| 原型 HTML 中 880px 弹窗宽度与现有 spec 760px 冲突 | 按 Change design 决议保持 760px，HTML 仅作为状态布局参考；通过 computed width 验收 |
| 小程序证书详情新增接口可能扩大 API/DB/对象存储改动面 | apply 阶段先确认现有品牌证书数据和图片组字段是否足够；字段不足时同步 Schema、OpenAPI/Orval、数据库文档和测试 |
| 证书列表主点击从预览改为详情页可能影响快速预览体验 | 详情页首屏提供明确预览/打开文件入口，并保留图片原生预览、PDF 受控打开和失败降级 |
| 分享直达证书详情无页面栈导致返回失败 | 按 miniapp-custom-navigation best-practice 实现返回兜底，并记录 DevTools 320/375/430 pt 与真机/blocked evidence |
| 品牌商品排序修复误影响普通商品列表、搜索、新品榜或热销榜 | apply 阶段把品牌过滤默认排序限定在 `brandId` 场景，并补充品牌排序、分页稳定、搜索/榜单不回归测试 |
| 发布时间事实字段被误用 | BUG-0087 使用 `tiles.published_at` 排序，历史空值才用 `created_at` 兜底；禁止使用 `updated_at` 冒充发布时间 |
| 管理端 SKU 列表新增时间列导致宽表拥挤 | 复用现有横向滚动/列宽策略，在 1440x1024 与窄屏视口验收发布时间和更新时间不重叠、不遮挡操作列 |
| 发布时间字段来源被误用为更新时间 | `update-admin-sku-list-published-at` apply 阶段先确认字段来源，禁止直接使用 `updated_at` 冒充发布时间 |
| 证书图片冗余文件名修复误伤上传状态机 | 修复仅移除说明下方文件名文本列表，保留图片卡片、主图、删除、设主图、上传进度和失败提示，并补充组件测试 |

## 6. 知识库承接

| 来源 | 承接动作 |
|---|---|
| `docs/knowledge-base/retrospectives/sprint-012-retrospective.md` | 保持薄片化 scope，避免把类目名称长度调整扩大为类目体系重构；归档前检查 acceptance 是否残留 stale 文案。 |
| `docs/knowledge-base/retrospectives/sprint-012-retrospective.md` | BUG-0086 修复保持薄片化，先验证字段链路和公开边界，避免扩大为详情页重构。 |
| `docs/knowledge-base/best-practices/admin-list-page-consistency.md` | 类目列表回归分页 DOM、fixed toast、DS confirm、指标卡结构。 |
| `docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md` | 类目弹窗回归单一专属类、computed width、CSS 栈测试和矮视口滚动。 |
| `docs/knowledge-base/best-practices/admin-list-page-consistency.md` | 品牌证书列表回归分页 DOM、fixed toast、DS confirm、指标卡结构。 |
| `docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md` | 品牌证书弹窗保持 760px computed width、单一专属类和矮视口滚动。 |
| `docs/knowledge-base/best-practices/admin-media-upload-chain.md` | 证书多图上传覆盖上传状态机、同会话即时回显、Docker Web 边界上传和 MinIO 单桶路径。 |
| `docs/knowledge-base/best-practices/miniapp-custom-navigation.md` | REQ-0080 证书详情页覆盖分享直达、返回兜底、状态栏/胶囊 reserve、页面 offset 和 DevTools/真机 evidence。 |
| `docs/knowledge-base/retrospectives/sprint-012-retrospective.md` | REQ-0080 横跨 API、DB、对象存储和小程序页面，apply 阶段需保持薄片化并避免把范围扩大到证书真伪校验、SKU 绑定或管理端维护。 |
| `docs/knowledge-base/retrospectives/sprint-012-retrospective.md` | BUG-0087 修复限定在品牌过滤排序与分页稳定性，避免扩大为商品列表排序体系重构。 |
| `docs/knowledge-base/best-practices/miniapp-custom-navigation.md` | 小程序品牌详情页回归时保持运行入口、导航和页面状态不因前端顺序确认产生额外跳转回归。 |
| `docs/knowledge-base/best-practices/admin-list-page-consistency.md` | SKU 列表新增发布时间列时回归分页 DOM、fixed toast、DS confirm、指标卡结构和无 `window.confirm`。 |
| `docs/knowledge-base/retrospectives/sprint-012-retrospective.md` | REQ-0079 保持列级薄片，不扩大为发布时间筛选、排序、导出或发布流程改造。 |
| `docs/knowledge-base/best-practices/admin-form-page-consistency.md` | BUG-0089 修复禁止新增文档流提示块或图片文件名文本列表，避免弹窗内容被无任务价值信息推挤。 |
| `docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md` | BUG-0089 回归品牌证书弹窗 760px computed width、矮视口滚动和单一专属类不回归。 |
| `docs/knowledge-base/best-practices/admin-media-upload-chain.md` | BUG-0089 修复保留证书图片上传状态机、同会话即时回显、失败原因和主图/删除操作。 |

## 7. 横切预防清单

- [ ] 管理端类目列表分页 DOM 继续对齐用户管理基准：左侧 `page-summary`，右侧 `page-right`。
- [ ] 管理端列表操作反馈使用 fixed toast，不出现文档流 notice 推挤布局。
- [ ] 类目启停、删除等状态或危险操作继续使用 Design System confirm modal，无 `window.confirm`。
- [ ] 摘要指标卡如被触达，DOM 保持 `.metric-label` / `.metric-value` / `.metric-desc`。
- [ ] `CategoryFormModal` 或等价弹窗 TSX 不同时挂载通用 `modal-card` 与专属类。
- [ ] 1440px 视口验收弹窗 computed width，720px 以下验收 body scroll。
- [ ] 归档前检查 acceptance/report 是否残留“待实现/待测试/planned”等 stale 文案。
- [ ] 小程序详情页回归公开字段边界：不得展示内部备注、原始 object key、Authorization header、Cookie 或敏感配置。
- [ ] 小程序详情页备注说明非空/空态各至少一条样例验收。
- [ ] 品牌证书多图上传控件覆盖 `idle -> uploading -> done / failed`，失败原因在控件内展示。
- [ ] 同一会话内上传成功后，证书列表或弹窗刷新即时回显主图缩略图和图片卡片。
- [ ] Docker Web 入口 `http://localhost:3000` 下完成证书图片边界上传：合法小图成功，超限图片返回业务错误而非 Nginx 413。
- [ ] 新上传不得写入 `data/uploads/`，对象存储路径遵守 MinIO 单桶策略。
- [ ] 小程序证书详情页主点击链路：证书列表卡片进入详情页，详情页内执行图片预览或 PDF 受控打开。
- [ ] 小程序证书详情页不展示收藏、推荐、价格、购物、购买、库存、促销或询价模块。
- [ ] 小程序证书详情页按 miniapp-custom-navigation 覆盖分享直达、返回兜底、胶囊 reserve、页面 offset 与截图 evidence。
- [ ] 证书详情 API 不暴露后台备注、审计字段、对象 Key、本机路径、Authorization header、Cookie、密钥或 `.env` 内容。
- [ ] 小程序品牌详情页商品 Tab 保持接口返回顺序展示，不做前端跨页重排。
- [ ] `/api/v1/miniapp/products?brandId=...` 排序修复不影响搜索页、新品榜、热销榜和普通商品列表。
- [ ] 管理端 SKU 列表新增“发布时间”后，分页 DOM 继续对齐用户管理基准。
- [ ] 管理端 SKU 列表新增时间列后，fixed toast 不造成页面头部、筛选区或表格纵向位移。
- [ ] 管理端 SKU 列表实现不引入 `window.confirm`；如触及危险状态操作，继续使用 DS confirm modal。
- [ ] 1440x1024 与窄屏视口下，“发布时间”和“更新时间”两列不重叠、不遮挡核心字段和操作列。
- [ ] 品牌证书图片上传说明下方不展示图片文件名文本列表。
- [ ] 品牌证书图片上传控件仍保留图片卡片、主图标记、删除、设为主图、继续添加、上传进度和失败提示。

## 8. 依赖 ASCII 树

```text
sprint-013
├── REQ-0077-category-name-max-length-15
│   └── update-category-name-max-length-15
│       ├── backend/api validation
│       ├── web admin CategoryFormModal
│       ├── OpenAPI / Orval / docs
│       ├── tests / fixtures
│       └── miniapp + web catalog layout regression
└── BUG-0086-miniapp-sku-detail-remark-not-shown
    └── fix-miniapp-sku-detail-remark-display
        ├── SKU detail API public remark field check
        ├── miniapp data mapping
        ├── miniapp detail template display
        └── empty remark + non-regression validation
└── REQ-0078-certificate-multiple-images-main-image
    └── update-certificate-multiple-images-main-image
        ├── brand certificate data model / compatibility
        ├── backend API / schema / storage validation
        ├── web admin certificate list + modal multi image UI
        ├── OpenAPI / Orval / docs
        └── pytest / Vitest / Docker upload boundary
└── REQ-0080-miniapp-certificate-detail-page
    └── add-miniapp-certificate-detail-page
        ├── backend public certificate detail API / safe URL filtering
        ├── miniapp certificate-detail route + page
        ├── certificate list card navigation to detail
        ├── share / brand entry / media preview / PDF open
        └── pytest / miniapp static tests / DevTools + device evidence
└── BUG-0087-miniapp-brand-detail-product-tab-sort-order
    └── fix-miniapp-brand-detail-product-sort-order
        ├── backend miniapp products brandId sort
        ├── publish time field mapping
        ├── pagination stability tests
        └── miniapp brand-detail product tab smoke
└── REQ-0079-admin-sku-list-published-at
    └── update-admin-sku-list-published-at
        ├── admin SKU list response published time field check
        ├── web admin SKU table published time column
        ├── OpenAPI / Orval / docs if contract changes
        └── admin-list layout and Vitest regression
└── BUG-0089-admin-certificate-edit-image-filename-noise
    └── pending /bug-opsx fix Change
        ├── web admin CertificateImageGrid filename meta removal
        ├── image card / main / remove / set-main non-regression
        └── BrandCertificateComponents Vitest coverage
```

## 9. 发布计划

- 发布类型：小版本功能修正 / 主数据与小程序详情体验优化。
- 发布说明重点：类目名称最多支持 15 个字符；运营可使用更完整的类目名称。
- 发布说明补充：小程序商品详情页展示已维护的备注说明，商品公开资料更完整。
- 发布说明补充：品牌证书支持多张图片和主图设置，管理端列表优先展示主图缩略图。
- 发布说明补充：微信小程序新增证书详情页，可从证书列表、品牌详情和分享入口查看单张证书完整信息。
- 发布说明补充：小程序品牌详情页商品 Tab 按发布时间升序、ID 升序稳定展示。
- 发布说明补充：管理端瓷砖 SKU 列表新增发布时间列，便于区分首次发布和后续更新时间。
- 发布说明补充：管理端品牌证书图片上传区移除无意义文件名文本，保持弹窗信息更清爽。
- 发布前置：后端、Web 管理端、OpenAPI/Orval、数据库/上传文档、管理端展示、小程序/Web 展示回归、小程序备注说明非空/空态验收、证书图片 Docker Web 上传边界、小程序证书详情 DevTools/真机 evidence、品牌商品排序与分页回归、SKU 发布时间列展示与空值回归、证书图片上传控件文件名隐藏与操作不回归全部通过。

## 10. 关联文档

| 类型 | 路径 |
|---|---|
| REQ | `issues/requirements/archive/REQ-0077-category-name-max-length-15/` |
| REQ | `issues/requirements/archive/REQ-0078-certificate-multiple-images-main-image/` |
| REQ | `issues/requirements/archive/REQ-0080-miniapp-certificate-detail-page/` |
| REQ | `issues/requirements/archive/REQ-0079-admin-sku-list-published-at/` |
| BUG | `issues/bugs/archive/BUG-0086-miniapp-sku-detail-remark-not-shown/` |
| BUG | `issues/bugs/archive/BUG-0087-miniapp-brand-detail-product-tab-sort-order/` |
| BUG | `issues/bugs/archive/BUG-0089-admin-certificate-edit-image-filename-noise/` |
| Change | `openspec/archive/2026-07-28-update-category-name-max-length-15/` |
| Change | `openspec/archive/2026-07-28-fix-miniapp-sku-detail-remark-display/` |
| Change | `openspec/archive/2026-07-28-update-certificate-multiple-images-main-image/` |
| Change | `openspec/archive/2026-07-29-add-miniapp-certificate-detail-page/` |
| Change | `openspec/archive/2026-07-28-fix-miniapp-brand-detail-product-sort-order/` |
| Change | `openspec/archive/2026-07-28-update-admin-sku-list-published-at/` |
| Spec | `openspec/specs/tile-category-management/spec.md` |
| Spec | `openspec/specs/miniapp-sku-detail-page/spec.md` |
| Spec | `openspec/specs/brand-certificate-management/spec.md` |
| Spec | `openspec/specs/miniapp-certificate-list-page/spec.md` |
| Spec | `openspec/specs/tile-sku-management/spec.md` |
| Spec | `openspec/specs/miniapp-brand-detail-home-page/spec.md` |
| Best Practice | `docs/knowledge-base/best-practices/admin-list-page-consistency.md` |
| Best Practice | `docs/knowledge-base/best-practices/admin-form-page-consistency.md` |
| Best Practice | `docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md` |
| Best Practice | `docs/knowledge-base/best-practices/admin-media-upload-chain.md` |
| Best Practice | `docs/knowledge-base/best-practices/miniapp-custom-navigation.md` |
| Retrospective | `docs/knowledge-base/retrospectives/sprint-013-retrospective.md` |

## 11. 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-28 22:52:21 | `/sprint-propose` | 纳入 REQ-0078 与 Change update-certificate-multiple-images-main-image，容量更新为 12/30 人天。 |
| 2026-07-28 22:51:35 | `/sprint-propose` | 纳入 BUG-0086 与 Change fix-miniapp-sku-detail-remark-display |
| 2026-07-28 00:24:49 | `/sprint-propose` | 创建 sprint-013，纳入 REQ-0077 与 Change update-category-name-max-length-15 |
| 2026-07-28 23:02:00 | `/sprint-propose` | 纳入 BUG-0087 与 Change fix-miniapp-brand-detail-product-sort-order，容量更新为 13/30 人天。 |
| 2026-07-28 23:03:00 | `/sprint-propose` | 纳入 REQ-0079 与 Change update-admin-sku-list-published-at，容量更新为 14/30 人天。 |
| 2026-07-29 08:24:32 | `/sprint-propose` | 纳入 REQ-0080 与 Change add-miniapp-certificate-detail-page，容量更新为 20/30 人天。 |
| 2026-07-29 08:38:46 | `/sprint-propose` | 纳入 BUG-0089，容量更新为 20.5/30 人天。 |
| 2026-07-29 09:24:09 | `/sprint-archive` | Sprint 013 关闭：8/8 Change 已归档，readiness 与 issue promotion gate 通过，目录准备迁入 `iterations/archive/sprint-013/`。 |
| 2026-07-29 09:31:30 | `/sprint-exps` | 生成 Sprint 013 复盘并回链 `docs/knowledge-base/retrospectives/sprint-013-retrospective.md`。 |
