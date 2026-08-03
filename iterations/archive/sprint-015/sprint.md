---
note: workflow-sync — workflow-sync 自动同步 — 6/6 Change archived；0 applied；Sprint `completed`
sprint_id: sprint-015
title: Sprint 015 管理端修复与小程序品牌列表体验优化
status: completed
lifecycle_stage: archive
created_at: 2026-07-31 15:17:00
updated_at: 2026-07-31 23:09:20
owner: product
---

# Sprint 015 管理端修复与小程序品牌列表体验优化

## 1. Sprint 目标

本 Sprint 聚焦四个管理端修复、一个小程序品牌列表体验优化与一个小程序商品卡片图片回归修复：修复管理后台瓷砖 SKU 页类目筛选只能选择一级类目的问题，统一管理端筛选条件下拉框位置和 UI 样式，移除管理后台瓷砖 SKU 列表「素材」列中对已有图片 SKU 的「主图已设」冗余标签，修正管理端类目树右侧计数口径，按新版设计稿优化微信小程序品牌列表页 UI 与品牌/类目入口交互，并修复商品列表图片加载优化后大面积显示“暂无图片”的媒体链路回归。

正式范围：

- `REQ-0086-miniapp-brand-list-ui-interaction-optimization`
- `BUG-0096-admin-sku-category-filter-only-top-level`
- `BUG-0097-admin-sku-material-main-image-tag-redundant`
- `BUG-0095-admin-category-tree-count-shows-product-count`
- `BUG-0094-miniapp-list-images-not-loading-after-speed-fix`
- `BUG-0098-admin-filter-dropdown-ui-consistency`

### BUG-0096-admin-sku-category-filter-only-top-level 要点

- 管理后台瓷砖 SKU 页类目筛选改为级联选择控件，展示完整类目树。
- 支持选择一级、二级、三级或更深层级类目。
- 选择父类目时，SKU 列表包含该父类目自身及所有子孙类目的 SKU。
- 保留「全部类目」/清空选择与重置筛选能力。
- 修复可能影响管理端 SKU 列表 API 的 `category_id` 过滤语义；若参数语义或参数名变化，必须同步 API 文档、OpenAPI、Orval 和前后端测试。

### REQ-0086-miniapp-brand-list-ui-interaction-optimization 要点

- 小程序品牌列表页按新版设计稿优化自定义导航、品牌 Hero、品牌矩阵标题、单品牌卡片和底部 TabBar 安全区。
- 品牌卡片上行作为品牌详情入口，下行类目胶囊作为品牌 + 类目商品列表入口。
- 类目胶囊点击需携带 `brandId` 与 `categoryId`，并阻止触发品牌详情跳转。
- DevTools evidence 覆盖 320、375、390、430 pt；真机不可用时标记 `blocked` 或 `follow_up`。
- 若接口缺少类目 ID 等字段，需同步 API、OpenAPI、Orval、小程序调用类型、文档和测试。

### BUG-0097-admin-sku-material-main-image-tag-redundant 要点

- 管理后台瓷砖 SKU 列表素材列只展示图片数量与视频数量。
- 素材列不再展示「主图已设」「缺主图」或其他素材状态标签。
- SKU 列表不再展示素材完整度条件筛选，列表请求不提交 `material_completeness`。
- 缺图、缺视频或素材不完整状态仍可通过图片/视频数量识别。
- 修复不改变 API、数据库、Orval、小程序、对象存储或 Docker Compose。

### BUG-0095-admin-category-tree-count-shows-product-count 要点

- 管理端类目树普通节点右侧数字显示直接子类目数量，不显示商品数量。
- 叶子类目右侧数字显示 `0`。
- “全部类目”入口右侧数字显示顶层类目数量。
- 修复优先聚焦 Web 管理端类目树字段绑定；如 OpenAPI/Orval 缺少直接子类目数量字段，则同步 API 契约和后端接口测试。

### BUG-0094-miniapp-list-images-not-loading-after-speed-fix 要点

- 小程序首页、商品列表、搜索结果页和品牌详情商品区中有真实主图的商品卡片恢复展示真实图片。
- 商品列表 `cover_image` 优先返回可访问的同目录缩略图 URL，缩略图缺失时回退原主图或占位。
- `images/default/tiles/pending/<uuid>.<ext>` 主图的缩略图与原图同目录存储，仅通过文件名差异区分。
- 补齐历史公开 SKU 主图缩略图，并输出可审计的回填结果。
- 保留 `BUG-0092` 的懒加载和列表图片性能优化，避免恢复图片展示后首屏外图片全量请求。

### BUG-0098-admin-filter-dropdown-ui-consistency 要点

- 以瓷砖类目页筛选下拉为管理端筛选区交互和视觉基准。
- 统一品牌、类目、规格、品牌证书、Banner、用户、系统设置、日志审计、接口文档和界面主题等页面的筛选下拉位置、尺寸、弹层对齐、选项状态和重置表现。
- 修复应优先复用统一筛选控件、筛选栏模板或 shared/admin UI 封装。
- 使用 Design System semantic token，避免页面级裸 Hex 和一次性下拉样式分化。
- 保持既有筛选字段、查询参数、接口请求和查询结果语义不变；不涉及 API、数据库、Orval、小程序或 Docker Compose。

## 2. Scope

| 类型 | 编号 | 标题 | 状态 | 估算 | 说明 |
|---|---|---|---|---:|---|
| REQ | REQ-0086-miniapp-brand-list-ui-interaction-optimization | 微信小程序品牌列表页 UI 与交互体验优化 | done | 3 人天 | archived `update-miniapp-brand-list-ui-interaction-optimization`（2026-07-31 21:19:20） |
| BUG | BUG-0096-admin-sku-category-filter-only-top-level | 管理后台瓷砖 SKU 页类目筛选只能选择一级类目 | done | 3 人天 | archived `fix-admin-sku-category-cascade-filter`（2026-07-31 21:25:00） |
| BUG | BUG-0097-admin-sku-material-main-image-tag-redundant | 管理后台瓷砖 SKU 素材列不应显示冗余的主图已设标签 | done | 0.5 人天 | archived `fix-admin-sku-material-main-image-tag`（2026-07-31 15:36:22） |
| BUG | BUG-0095-admin-category-tree-count-shows-product-count | 管理端类目树右侧计数显示为商品数量而非下级类目数量 | done | 1 人天 | archived `fix-admin-category-tree-count`（2026-07-31 17:29:59） |
| BUG | BUG-0094-miniapp-list-images-not-loading-after-speed-fix | 小程序商品列表图片加载优化后全部显示暂无图片 | done | 3 人天 | archived `fix-miniapp-product-card-thumbnails`（2026-07-31 21:33:42） |
| BUG | BUG-0098-admin-filter-dropdown-ui-consistency | 管理端筛选条件下拉框位置和 UI 样式不统一 | done | 3 人天 | archived `fix-admin-filter-dropdown-ui-consistency`（2026-07-31 23:00:57） |

<!-- workflow-sync:scope-requirements:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| REQ-0086 | 微信小程序品牌列表页 UI 与交互体验优化 | P1 | done | archived `update-miniapp-brand-list-ui-interaction-optimization`（2026-07-31 21:19:20） |
<!-- workflow-sync:scope-requirements:end -->

<!-- workflow-sync:scope-bugs:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| BUG-0096 | 管理后台瓷砖 SKU 页类目筛选只能选择一级类目 | medium | done | archived `fix-admin-sku-category-cascade-filter`（2026-07-31 21:25:00） |
| BUG-0097 | 管理后台瓷砖 SKU 素材列不应显示冗余的主图已设标签 | low | done | archived `fix-admin-sku-material-main-image-tag`（2026-07-31 15:36:22） |
| BUG-0095 | 管理端类目树右侧计数显示为商品数量而非下级类目数量 | medium | done | archived `fix-admin-category-tree-count`（2026-07-31 17:29:59） |
| BUG-0094 | 小程序商品列表图片加载优化后全部显示暂无图片 | high | done | archived `fix-miniapp-product-card-thumbnails`（2026-07-31 21:33:42） |
| BUG-0098 | 管理端筛选条件下拉框位置和 UI 样式不统一 | medium | done | archived `fix-admin-filter-dropdown-ui-consistency`（2026-07-31 23:00:57） |
<!-- workflow-sync:scope-bugs:end -->

<!-- workflow-sync:scope-changes:start -->
| Change ID | 关联需求 | 状态 | Sprint 目标 |
|---|---|---|---|
| `fix-admin-sku-category-cascade-filter` | BUG-0096-admin-sku-category-filter-only-top-level | archived | archived `fix-admin-sku-category-cascade-filter`（2026-07-31 21:25:00） |
| `fix-admin-sku-material-main-image-tag` | BUG-0097-admin-sku-material-main-image-tag-redundant | archived | archived `fix-admin-sku-material-main-image-tag`（2026-07-31 15:36:22） |
| `fix-admin-category-tree-count` | BUG-0095-admin-category-tree-count-shows-product-count | archived | archived `fix-admin-category-tree-count`（2026-07-31 17:29:59） |
| `update-miniapp-brand-list-ui-interaction-optimization` | REQ-0086-miniapp-brand-list-ui-interaction-optimization | archived | archived `update-miniapp-brand-list-ui-interaction-optimization`（2026-07-31 21:19:20） |
| `fix-miniapp-product-card-thumbnails` | BUG-0094-miniapp-list-images-not-loading-after-speed-fix | archived | archived `fix-miniapp-product-card-thumbnails`（2026-07-31 21:33:42） |
| `fix-admin-filter-dropdown-ui-consistency` | BUG-0098-admin-filter-dropdown-ui-consistency | archived | archived `fix-admin-filter-dropdown-ui-consistency`（2026-07-31 23:00:57） |
<!-- workflow-sync:scope-changes:end -->

Change：已纳入 5 个修复范围项和 1 个需求优化项关联 Change。执行开发与归档时以 Scope 表逐项状态为准。

## 3. 工作量与容量

| 项 | 值 |
|---|---:|
| developers | 2 |
| testers | 1 |
| capacity_person_days | 30 |
| estimated_story_points | 13.5 |
| estimated_person_days | 13.5 |
| capacity_usage | 45.00% |
| fix_buffer_person_days | 16.5 |
| fix_buffer_ratio | 55.00% |

容量门禁：Pass。`project.yaml` 未提供显式 Sprint 容量，沿用 sprint-014 已确认容量基线 2 dev + 1 tester / 30 人天。本 Sprint 当前纳入 1 个 P1 REQ、5 个 BUG 与 6 个 Change，估算 13.5 人天，占用 45.00%，满足容量硬门禁，fix buffer 16.5 人天 / 55.00%，仍满足建议缓冲。

## 4. 里程碑

| 阶段 | 目标日期 | 交付 |
|---|---|---|
| 规划确认 | 2026-07-31 15:17:00 | Sprint 四件套、BUG/Change trace 同步 |
| 实现完成 | 2026-08-04 18:00:00 | 管理端 SKU 类目级联筛选与子树过滤、管理端筛选下拉 UI 一致性、SKU 列表素材列渲染、类目树计数字段绑定、小程序品牌列表 UI/交互、商品卡片缩略图生成/回填与相关测试完成 |
| 验收归档 | 2026-08-14 18:00:00 | Change archive、REQ/BUG archive、验收报告闭环 |

## 5. 风险

| 风险 | 缓解 |
|---|---|
| SKU 页父类目筛选继续沿用精确匹配，导致父类目结果不完整 | 后端或前端必须明确解析子树范围；测试覆盖父类目包含所有子孙类目 SKU |
| 类目级联控件影响筛选区布局或重置行为 | 视检 SKU 页筛选区，测试覆盖选择父类目、子类目和清空类目 |
| `category_id` 参数语义变化引发调用方理解偏差 | 若调整接口语义或参数名，同步 docs/03-api-index.md、OpenAPI、Orval 和前端调用说明 |
| 移除所有素材状态标签与素材完整度筛选后，运营误以为主图状态不可见 | 保留图片数量、视频数量；素材列只保留数量信息 |
| 实现误删缺图或素材不完整提示 | 测试覆盖缺图、缺视频或素材不完整仍可识别 |
| 管理端列表布局出现细微抖动 | 验收覆盖素材列行高、列宽、状态列和操作列无遮挡 |
| 类目树计数修复误改 `sku_count` 商品数量语义 | 明确 `sku_count` 只用于商品/SKU 统计和删除规则，类目树右侧计数使用直接子类目数量字段 |
| “全部类目”入口继续显示商品总数 | 页面测试覆盖顶层类目数量，Scope 验收明确不显示商品总数 |
| 小程序品牌列表类目标签点击误触品牌详情 | 实现中阻止事件冒泡，测试覆盖品牌入口与类目入口跳转边界 |
| 新版 Hero 与既有品牌轮播能力边界不清 | OpenSpec design 明确 Hero 可作为轮播视觉呈现但不得破坏轮播数据、跳转和安全降级 |
| 小程序设备 evidence 延后 | 继承 sprint-014 经验，DevTools 320/375/390/430 pt 必须记录；真机不可用只能标记 blocked 或 follow_up |
| 商品卡片缩略图继续返回不可访问 URL | 后端列表 `cover_image` 必须先确认同路径缩略图可访问，缺失时回退原主图或占位；测试覆盖 pending 主图 |
| 历史缩略图回填漏扫公开 SKU | 回填脚本支持 dry-run、统计摘要、失败清单和可重入；验收覆盖 pending 主图与已绑定 tile_id 路径 |
| 恢复图片展示导致 BUG-0092 性能回退 | 保留小程序商品卡片 `lazy-load` 或等价延迟加载，测试覆盖首屏外图片不在初始化阶段全量请求 |
| 管理端筛选下拉统一时误改筛选语义 | 明确 BUG-0098 不改变 API 字段、查询参数和结果语义；页面测试覆盖选择、清空、重置和分页重置 |
| 横向统一下拉样式引入页面级布局裁切 | 以瓷砖类目页为基准，复核弹层挂载、z-index、overflow、桌面与窄屏视口 |
| 页面级 CSS 继续分化 | 使用 shared/admin UI、Design System semantic token 和 `cn()`，避免裸 Hex 与一次性 dropdown 样式 |

## 6. 知识库承接

| 来源 | 承接动作 |
|---|---|
| `docs/knowledge-base/retrospectives/sprint-014-retrospective.md` | 承接 T-014-001 容量冻结线：新增 BUG-0096 后 sprint-015 占用 25.00%，仍远低于 85% 冻结线，允许纳入正式范围。 |
| `docs/knowledge-base/best-practices/admin-list-page-consistency.md` | 管理端 SKU 页筛选控件改为级联选择后，仍需保持筛选区、表格卡片、分页、fixed toast、操作列和重置行为一致性。 |
| `docs/knowledge-base/retrospectives/sprint-014-retrospective.md` | 承接 T-014-001 的容量冻结提醒：本 Sprint 新增 BUG-0096 后仍保持低容量占用，但后续继续扩围需重新计算容量与 fix buffer。 |
| `docs/knowledge-base/retrospectives/sprint-014-retrospective.md` | 承接 T-014-004 的分段执行建议：apply 阶段只读 SKU 列表渲染、前端测试和相关 CSS 片段，不展开无关 API/DB/小程序上下文。 |
| `docs/knowledge-base/best-practices/admin-list-page-consistency.md` | 管理端 SKU 列表回归需保持分页 DOM、表格卡片、fixed toast、操作列和列表布局一致性；本 BUG 重点检查素材列变更不影响这些横切基线。 |
| `docs/knowledge-base/best-practices/admin-list-page-consistency.md` | 管理端类目树修复需保持类目管理页列表/树联动、筛选上下文和布局基线，不因计数字段调整引入页面结构回归。 |
| `docs/knowledge-base/best-practices/miniapp-custom-navigation.md` | REQ-0086 需覆盖小程序状态栏、微信胶囊 reserve、返回兜底、页面 offset、TabBar/Safe Area 和 320/375/390/430 pt evidence。 |
| `docs/knowledge-base/retrospectives/sprint-014-retrospective.md` | 承接“小程序列表类需求在 propose 阶段写清公开口径、点击区域、排序字段和空态”的经验，REQ-0086 已在 OpenSpec design/spec/tasks 中明确类目 ID、点击边界、空态和设备验收。 |
| `docs/knowledge-base/best-practices/admin-media-upload-chain.md` | BUG-0094 涉及对象存储缩略图生成、`/media/{object_key}` 读取和历史回填，需按媒体上传全链路检查 object_key、受控读取、日志脱敏和对象存储写入。 |
| `docs/knowledge-base/retrospectives/sprint-014-retrospective.md` | 承接 BUG-0092 图片加载经验：性能优化必须有可访问 URL 回退和真机/体验版 evidence，不得只看接口字段存在。 |
| `docs/knowledge-base/best-practices/admin-list-page-consistency.md` | BUG-0098 需继承管理端列表页一致性基线，筛选下拉统一时同步复核筛选区、表格卡片、分页、fixed toast、操作列和重置行为。 |
| `docs/knowledge-base/retrospectives/sprint-014-retrospective.md` | 承接 T-014-001 容量冻结线：新增 BUG-0098 后 sprint-015 占用 45.00%，仍低于 85% 冻结线，允许纳入正式范围。 |

## 7. 横切预防清单

- [ ] admin-list：SKU 页类目级联筛选控件不破坏筛选区对齐、表格卡片、分页、状态列和操作列。
- [ ] admin-list：父类目筛选必须包含所有子孙类目 SKU，子类目筛选不得返回无关兄弟类目。
- [ ] admin-list：素材列变更后，表格卡片内不新增重复标题或文档流提示。
- [ ] admin-list：分页 DOM、状态列、操作列和 toast 行为不因素材列渲染调整而回归。
- [ ] UI：移除素材状态标签后，图片/视频数量是素材列唯一信息。
- [ ] UI：类目树右侧计数只表达直接子类目数量；商品数量如需展示必须使用独立位置或标签。
- [ ] API：若 `children_count` 需要补齐到 OpenAPI，必须同步 Orval、API 文档和后端接口测试。
- [ ] miniapp：品牌列表页自定义导航、微信胶囊 reserve、底部 TabBar/Safe Area 在 320/375/390/430 pt 视口不遮挡。
- [ ] miniapp：品牌卡片上行点击进入品牌详情，下行类目胶囊点击进入品牌 + 类目商品列表，类目点击不冒泡。
- [ ] miniapp：若品牌列表接口缺少 `categoryId`，同步 API、OpenAPI、Orval、小程序调用类型和测试。
- [ ] miniapp-media：商品卡片 `cover_image` 必须是可访问的列表图片 URL，pending 主图不得机械映射到不可访问的 `thumbnails/default/tiles/pending/`。
- [ ] media-upload：缩略图生成与历史回填遵守单 Bucket + 对象前缀策略，回填日志不得泄露密钥、Cookie、`.env` 或本机路径。
- [ ] media-upload：`/media/{object_key}` 受控读取对同路径缩略图和原主图均可观测，失败时有统计摘要和 SKU 定位。
- [ ] 测试：前端回归覆盖素材列只显示图片/视频数量、素材完整度筛选控件已移除且请求不提交 `material_completeness`。
- [ ] 测试：前端回归覆盖一级类目、叶子类目和“全部类目”三类计数。
- [ ] 测试：小程序静态测试覆盖 Hero、品牌矩阵、品牌卡片上下分区、类目胶囊、TabBar 选中态和运行入口一致性。
- [ ] 测试：后端覆盖 pending 原图、同路径缩略图、缩略图缺失回退、历史回填幂等和对象存储失败摘要。
- [ ] 测试：小程序商品卡片保留 `lazy-load`，首屏外商品图片不在页面初始化时全量请求。
- [ ] admin-list：BUG-0098 覆盖页面筛选下拉位置、尺寸、弹层对齐、选项状态和重置表现与瓷砖类目页一致。
- [ ] design-system：筛选下拉使用 semantic token、CSS variables、`cn()` 或 existing admin classes，不新增裸 Hex 或一次性颜色。
- [ ] UI：下拉弹层不被表格、页面容器、滚动区、弹窗或 sticky action column 裁切。
- [ ] 测试：前端覆盖筛选下拉打开、选择、清空、重置、禁用、空态、加载态和已选中态。
- [ ] 测试：确认 BUG-0098 不改变既有筛选字段、查询参数、接口请求和查询结果语义。

## 8. 依赖 ASCII 树

```text
BUG-0096-admin-sku-category-filter-only-top-level
└── fix-admin-sku-category-cascade-filter
    ├── 管理端 SKU 页类目级联选择控件
    ├── 父类目子树过滤
    ├── API / OpenAPI / Orval 条件同步
    └── TileSkuManagementPage / 后端筛选回归测试

BUG-0097-admin-sku-material-main-image-tag-redundant
└── fix-admin-sku-material-main-image-tag
    ├── 管理端 SKU 列表素材列渲染
    └── TileSkuManagementPage 前端回归测试

BUG-0095-admin-category-tree-count-shows-product-count
└── fix-admin-category-tree-count
    ├── 管理端类目树计数字段绑定
    ├── 全部类目顶层类目数量展示
    └── CategoryTree / TileCategoryManagementPage 回归测试

REQ-0086-miniapp-brand-list-ui-interaction-optimization
└── update-miniapp-brand-list-ui-interaction-optimization
    ├── 小程序品牌列表页新版 UI
    ├── 品牌入口 / 类目胶囊点击边界
    ├── 条件 API / OpenAPI / Orval 同步
    └── 小程序 320/375/390/430 pt evidence

BUG-0094-miniapp-list-images-not-loading-after-speed-fix
└── fix-miniapp-product-card-thumbnails
    ├── 同路径缩略图 key helper
    ├── 新主图缩略图生成
    ├── 历史公开 SKU 主图缩略图回填
    ├── 小程序首页 / 商品列表 cover_image 可访问回退
    └── 后端媒体测试 / 小程序静态测试 / BUG-0092 性能回归

BUG-0098-admin-filter-dropdown-ui-consistency
└── fix-admin-filter-dropdown-ui-consistency
    ├── 管理端筛选下拉统一基准
    ├── Design System / shared admin UI 收敛
    ├── 品牌 / 类目 / 规格 / 证书 / Banner / 用户 / 设置 / 日志 / 接口文档 / 主题页面回归
    └── 前端组件测试 / 页面 smoke / 视觉裁切验收
```

## 9. 发布计划

本 Sprint 包含管理端 Web 展示/筛选修复、小程序品牌列表体验优化与小程序商品卡片图片恢复修复，适合随下一次常规产品发布交付；不需要数据库迁移。BUG-0094 需要对象存储历史缩略图回填 dry-run 与执行摘要；BUG-0098 不应改变 API、数据库或 Orval。若 SKU 列表类目筛选参数语义、类目树直接子类目数量字段、品牌列表类目 ID 字段或公开列表 `cover_image` URL 语义需要补齐到 OpenAPI，则本 Sprint 需同步 Orval 后再发布。

## 9.1 关闭记录

2026-07-31 23:07:14：`/sprint-archive sprint-015` 执行关闭。Readiness 校验 PASS，6/6 Change 已归档，1 个 REQ 与 5 个 BUG 已处于 archive/done，Sprint 目录归档至 `iterations/archive/sprint-015/`。

## 10. 关联文档

- `docs/knowledge-base/retrospectives/sprint-015-retrospective.md`
- `issues/bugs/archive/BUG-0097-admin-sku-material-main-image-tag-redundant/`
- `openspec/archive/2026-07-31-fix-admin-sku-material-main-image-tag/`
- `issues/bugs/archive/BUG-0096-admin-sku-category-filter-only-top-level/`
- `openspec/archive/2026-07-31-fix-admin-sku-category-cascade-filter/`
- `issues/bugs/archive/BUG-0095-admin-category-tree-count-shows-product-count/`
- `openspec/archive/2026-07-31-fix-admin-category-tree-count/`
- `issues/requirements/archive/REQ-0086-miniapp-brand-list-ui-interaction-optimization/`
- `openspec/archive/2026-07-31-update-miniapp-brand-list-ui-interaction-optimization/`
- `issues/bugs/archive/BUG-0094-miniapp-list-images-not-loading-after-speed-fix/`
- `openspec/archive/2026-07-31-fix-miniapp-product-card-thumbnails/`
- `issues/bugs/archive/BUG-0098-admin-filter-dropdown-ui-consistency/`
- `openspec/archive/2026-07-31-fix-admin-filter-dropdown-ui-consistency/`
- `openspec/specs/tile-sku-management/spec.md`
- `openspec/specs/tile-category-management/spec.md`
- `openspec/specs/design-system/spec.md`
- `openspec/specs/miniapp-brand-list-page/spec.md`
- `openspec/specs/miniapp-product-list-page/spec.md`
- `openspec/specs/miniapp-home/spec.md`
- `openspec/specs/object-storage/spec.md`
- `openspec/specs/web-client/spec.md`
- `docs/knowledge-base/best-practices/admin-list-page-consistency.md`
- `docs/knowledge-base/best-practices/miniapp-custom-navigation.md`
