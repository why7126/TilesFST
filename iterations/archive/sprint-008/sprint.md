---
note: workflow-sync — workflow-sync 自动同步 — 11/11 Change archived；0 applied；Sprint `completed`
title: Sprint 008 规划
purpose: 纳入 XL 管理端页面分层验收模板、Agent 上下文预算治理、微信小程序首页首期闭环、自定义导航栏与首页样式信息架构优化，并承接品牌证书后续运营观察点
content: Sprint 008 规划四件套
source: /sprint-propose
update_method: 需求、BUG 或 Change 正式纳入 Sprint 时同步更新
created_at: 2026-07-16 08:59:46
updated_at: 2026-07-19 15:35:19
---

# Sprint 008 规划

## 1. Sprint 目标

本 Sprint 已于 2026-07-19 15:31:45 强制关闭。正式交付范围纳入 `REQ-0039` / `REQ-0040` / `REQ-0041` / `REQ-0042` / `REQ-0043` / `REQ-0044` / `REQ-0045` / `REQ-0046` / `REQ-0047` / `REQ-0048` / `BUG-0065` 及已存在的对应 Change，目标是沉淀 XL 管理端页面分层验收模板，完善规则/Skill 已读摘要复用的 Agent 上下文预算治理，交付微信小程序首页首期闭环，在此基础上推进首页品牌自定义导航栏、全局自定义导航栏、深色视觉与信息架构优化，新增微信小程序 SKU 详情页、分类列表页、搜索通用组件与商品列表页通用组件，并修复小程序首页预览运行入口脱节问题。

正式目标：

- `REQ-0039`：沉淀 XL 管理端页面分层验收模板。
- `add-xl-admin-page-acceptance-template`：新增 OpenSpec capability `xl-admin-page-acceptance-template`，实现长期模板文档、gate 矩阵和知识库横切引用。
- `REQ-0040`：将规则/Skill 已读摘要复用机制纳入命令上下文预算治理。
- `update-rule-skill-summary-reuse-context-budget`：更新 `agent-workflow-tooling` 能力，覆盖摘要复用、失效条件、命令 Skill 模板与预算校验。
- `REQ-0041`：新增微信小程序首页，覆盖首页、搜索、商品详情、门店信息、分享、咨询和热销行为统计首期闭环。
- `add-miniapp-home`：新增 `miniapp-home` 能力并扩展 `product-usage-logging`，实现公开首页聚合、行为事件和小程序端页面验收。
- `REQ-0042`：纳入微信小程序首页品牌自定义导航栏，明确当前搜索框上方 `brand-header` 品牌展示部分、右侧原生分享 / 关闭按钮、门店信息排除和搜索框下置边界。
- `add-miniapp-custom-navigation-bar`：已由 `/req-opsx REQ-0042` 创建；后续 `/opsx-apply` 必须明确品牌展示、右侧原生分享/关闭、门店信息排除、搜索框下置和真机避让验收。
- `REQ-0043`：优化微信小程序首页样式与信息架构，覆盖深色品牌视觉、品牌 Header、四入口导航、新品/热销推荐、全部产品瀑布流、TabBar 目标文案和埋点预留。
- `update-miniapp-home-style-optimization`：更新 `miniapp-home` 与 `product-usage-logging` 能力，明确首页深色视觉、全部产品瀑布流、TabBar 安全降级和首页行为事件边界。
- `REQ-0044`：新增微信小程序瓷砖 SKU 详情页，覆盖 SKU 详情展示、图片/视频混合轮播、图片全屏预览、收藏、分享、品牌入口、同系列/同品牌推荐和异常状态。
- `add-miniapp-sku-detail-page`：已由 `/req-opsx REQ-0044` 创建；后续 `/opsx-apply` 必须明确小程序详情页 API、媒体 URL 安全、收藏/分享 contract、DB/Orval/docs/tests 同步边界。
- `REQ-0045`：新增微信小程序分类列表页，覆盖 TabBar 分类频道、一级/二级分类双栏浏览、分类树数据、缓存版本号、二级分类跳转、异常状态、埋点和小程序视觉验收。
- `add-miniapp-category-list-page`：已由 `/req-opsx REQ-0045` 创建；后续 `/opsx-apply` 必须明确分类树接口、缓存版本号、双栏交互、二级分类跳转、异常状态、埋点和小程序视觉验收边界。
- `REQ-0046`：新增微信小程序搜索通用组件并应用，覆盖搜索入口组件、搜索首页、实时联想、完整搜索结果、筛选抽屉、无结果状态、搜索埋点和小程序搜索原型验收。
- `add-miniapp-search-component`：已由 `/req-opsx REQ-0046` 创建；后续 `/opsx-apply` 必须明确搜索入口组件、搜索首页、联想、结果、筛选、无结果、埋点和小程序原型验收边界。
- `REQ-0047`：新增微信小程序商品列表页通用组件并应用，覆盖商品列表容器、商品卡片、分类/搜索/品牌/推荐入口复用、筛选排序、分页加载、状态治理、埋点和小程序原型验收。
- `add-miniapp-product-list-component`：已由 `/req-opsx REQ-0047` 创建；后续 `/opsx-apply` 必须明确商品列表容器、商品卡片、筛选排序、分页加载、状态治理、埋点和小程序原型验收边界。
- `REQ-0048`：纳入微信小程序全局自定义导航栏，覆盖首页保留当前品牌 `brand-header`、非首页复用同一导航模块并新增左侧返回按钮、右侧避让微信原生分享 / 关闭胶囊、状态栏避让和 fixed header 内容不遮挡。
- `add-miniapp-global-custom-navigation-bar`：已由 `/req-opsx REQ-0048` 创建；后续 `/opsx-apply` 必须明确非首页返回、原生胶囊避让、状态栏避让、fixed header 内容不遮挡和真机 / 微信开发者工具验收。
- `BUG-0065`：修复微信小程序首页预览效果与 REQ-0041 原型和验收差异明显的问题。
- `fix-miniapp-home-preview-runtime-entry`：修复小程序首页运行入口脱节，确保微信开发者工具实际加载首页业务逻辑并补充回归测试。

本 Sprint 继续承接 `sprint-007` 复盘行动项 `A-005`，但以下品牌证书能力后续运营观察点仍为待评审产品输入，不纳入正式范围：

- 过期证书提醒：观察证书临期/过期后的运营提醒入口、提醒阈值、提醒对象和是否影响前台展示。
- 证书类型统计：观察按质量体系、产品检测、绿色环保、荣誉资质等类型的统计口径、筛选入口和运营看板价值。
- 批量维护：观察批量显示/隐藏、批量改类型、批量更新有效期或批量下架的操作风险、二次确认和审计要求。

## 2. Scope

<!-- workflow-sync:scope-requirements:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| REQ-0039 | XL 管理端页面分层验收模板 | P1 | done | archived `add-xl-admin-page-acceptance-template`（2026-07-16 09:24:12） |
| REQ-0040 | 规则/Skill 已读摘要复用纳入命令上下文预算治理 | P1 | done | archived `update-rule-skill-summary-reuse-context-budget`（2026-07-16 09:23:05） |
| REQ-0041 | 微信小程序首页 | P1 | done | archived `add-miniapp-home`（2026-07-16 10:46:52） |
| REQ-0042 | 微信小程序首页品牌自定义导航栏 | P1 | done | archived `add-miniapp-custom-navigation-bar`（2026-07-19 09:49:14） |
| REQ-0043 | 微信小程序首页样式与信息架构优化 | P1 | done | archived `update-miniapp-home-style-optimization`（2026-07-18 16:09:56） |
| REQ-0044 | 微信小程序新增瓷砖 SKU 详情页 | P1 | done | archived `add-miniapp-sku-detail-page`（2026-07-18 19:54:32） |
| REQ-0045 | category list page | P1 | done | archived `add-miniapp-category-list-page`（2026-07-19 01:20:00） |
| REQ-0046 | 微信小程序搜索通用组件并应用 | P1 | done | archived `add-miniapp-search-component`（2026-07-19 13:53:18） |
| REQ-0047 | 微信小程序商品列表页通用组件并应用 | P1 | done | archived `add-miniapp-product-list-component`（2026-07-19 01:50:36） |
| REQ-0048 | 小程序全局自定义导航栏 | P1 | done | archived `add-miniapp-global-custom-navigation-bar`（2026-07-19 12:03:19） |
<!-- workflow-sync:scope-requirements:end -->

<!-- workflow-sync:scope-bugs:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| BUG-0065 | 微信小程序首页预览效果与 REQ-0041 原型和验收差异明显 | high | done | archived `fix-miniapp-home-preview-runtime-entry`（2026-07-16 13:18:30） |
<!-- workflow-sync:scope-bugs:end -->

<!-- workflow-sync:scope-changes:start -->
| Change ID | 关联需求 | 状态 | Sprint 目标 |
|---|---|---|---|
| `add-xl-admin-page-acceptance-template` | REQ-0039-xl-admin-page-layered-acceptance-template | archived | archived `add-xl-admin-page-acceptance-template`（2026-07-16 09:24:12） |
| `update-rule-skill-summary-reuse-context-budget` | REQ-0040-rule-skill-read-summary-reuse-context-budget | archived | archived `update-rule-skill-summary-reuse-context-budget`（2026-07-16 09:23:05） |
| `add-miniapp-home` | REQ-0041-miniapp-home | archived | archived `add-miniapp-home`（2026-07-16 10:46:52） |
| `update-miniapp-home-style-optimization` | REQ-0043-miniapp-home-style-optimization | archived | archived `update-miniapp-home-style-optimization`（2026-07-18 16:09:56） |
| `fix-miniapp-home-preview-runtime-entry` | REQ-0041-miniapp-home | archived | archived `fix-miniapp-home-preview-runtime-entry`（2026-07-16 13:18:30） |
| `add-miniapp-custom-navigation-bar` | REQ-0042-custom-navigation-bar | archived | archived `add-miniapp-custom-navigation-bar`（2026-07-19 09:49:14） |
| `add-miniapp-sku-detail-page` | REQ-0044-miniapp-sku-detail-page | archived | archived `add-miniapp-sku-detail-page`（2026-07-18 19:54:32） |
| `add-miniapp-category-list-page` | REQ-0045-category-list-page | archived | archived `add-miniapp-category-list-page`（2026-07-19 01:20:00） |
| `add-miniapp-search-component` | REQ-0046-search-component-application | archived | archived `add-miniapp-search-component`（2026-07-19 13:53:18） |
| `add-miniapp-product-list-component` | REQ-0047-product-list-common-component-application | archived | archived `add-miniapp-product-list-component`（2026-07-19 01:50:36） |
| `add-miniapp-global-custom-navigation-bar` | REQ-0048-miniapp-global-custom-navigation-bar | archived | archived `add-miniapp-global-custom-navigation-bar`（2026-07-19 12:03:19） |
<!-- workflow-sync:scope-changes:end -->

## 3. 工作量

| 项 | 数值 | 说明 |
|---|---:|---|
| 团队容量 | 30.0 人天 | 沿用上一 Sprint 团队配置：2 名开发、1 名测试 |
| 正式范围估算 | 36.0 人天 | REQ-0039 为 S=1.0；REQ-0040 为 M=3.0；REQ-0041 为 XL=8.0；REQ-0042 为 S=1.0；REQ-0043 为 L=5.0；REQ-0044 为 L=5.0；REQ-0045 为 M=3.0；REQ-0046 为 L=5.0；REQ-0047 为 M=3.0；REQ-0048 为 S=1.0；BUG-0065 为 S=1.0 |
| 容量占用 | 120.00% | `36.0 / 30.0`，达到但未超过 120% 硬阻断阈值 |
| fix 缓冲 | -6.0 人天 / -20.00% | 低于 SHOULD >= 30% 建议，需冻结范围外扩并优先收敛已纳入小程序能力 |

容量门禁：通过但有容量风险。REQ-0039、REQ-0040、REQ-0041、REQ-0042、REQ-0043、REQ-0044、REQ-0045、REQ-0046、REQ-0047、REQ-0048 与 BUG-0065 均已评审通过；估算 36.0 人天超过 30.0 人天容量，达到但未超过 36.0 人天硬阻断阈值。品牌证书观察点因未评审，不计入正式工作量。`add-miniapp-home` 为 add-* 主能力且估算 8.0 人天，超过 SHOULD <= 6 的建议阈值，需在实现阶段按 Backend/API、Miniapp、Docs/Tests 分层推进。REQ-0048 按 S=1.0 人天纳入，OpenSpec Change `add-miniapp-global-custom-navigation-bar` 已创建；后续若再新增范围，将超过硬阻断阈值，应拆分 Sprint 或移出低优先级项。BUG-0065 使用 fix 缓冲 1.0 人天，修复面限定为小程序运行入口和回归测试。

## 4. fix 缓冲

当前 Sprint 纳入 36.0 人天正式范围，fix 缓冲为 -6.0 人天 / -20.00%，低于 SHOULD >= 30% 建议且已达到 120% 容量上限。BUG-0065 已使用 1.0 人天 fix 缓冲，用于修复小程序首页运行入口脱节；REQ-0042 使用 1.0 人天自定义导航栏 refinement 预算，需限制为首页品牌展示、原生分享/关闭避让、门店信息排除和搜索框下置；REQ-0048 使用 1.0 人天全局导航栏 refinement 预算，必须复用 REQ-0042 的导航模块和已纳入页面，不扩展 API/DB、后台配置或新增业务页面；REQ-0043 使用 5.0 人天小程序体验优化预算，重点留给视觉适配、瀑布流状态、TabBar 降级和 320-430 pt 验收；REQ-0044 使用 5.0 人天 SKU 详情页预算，需严格控制购物、询价、库存、在线下单等范围外能力；REQ-0045 使用 3.0 人天分类列表页预算，需复用分类树数据与小程序现有视觉基础；REQ-0046 使用 5.0 人天搜索体验预算，必须保留小程序单端范围；REQ-0047 使用 3.0 人天商品列表页预算，必须复用分类、搜索和 SKU 详情链路。后续若品牌证书观察点或其他范围转为 REQ 并通过评审，应优先移出低优先级项或拆分 Sprint 后再纳入。

## 5. 里程碑

| 目标日期 | 里程碑 | 验收口径 |
|---|---|---|
| 2026-07-17 18:00:00 | XL 验收模板文档落地 | `docs/standards/` 或等价模板位置存在，覆盖七层 gate 与 N/A 判定 |
| 2026-07-18 12:00:00 | OpenSpec 校验与 trace 同步 | `add-xl-admin-page-acceptance-template` tasks 完成，OpenSpec validate 通过 |
| 2026-07-19 18:00:00 | Agent 上下文预算治理落地 | `rules/agent-context-budget.md`、命令 Skill、校验脚本和测试完成 |
| 2026-07-24 18:00:00 | 小程序后端契约与行为事件落地 | 首页聚合、公开字段过滤、usage event 字典和热销排序测试完成 |
| 2026-07-28 18:00:00 | 小程序首页首期闭环验收 | 首页、搜索、商品详情、门店信息、分享、咨询和 320-430 pt 布局验收完成 |
| 2026-07-29 18:00:00 | 小程序首页预览缺陷修复 | BUG-0065 修复完成，运行入口、首屏模块和回归测试通过 |
| 2026-07-29 12:00:00 | 小程序首页样式与信息架构优化 Change 创建 | `update-miniapp-home-style-optimization` 已创建，明确视觉、瀑布流、TabBar 和埋点实现边界 |
| 2026-07-29 15:00:00 | 小程序首页自定义导航栏 Change 创建 | `REQ-0042` 完成 `/req-opsx`，明确品牌展示、原生分享/关闭避让、门店信息排除和搜索框下置边界 |
| 2026-07-30 12:00:00 | 小程序首页体验优化验收 | 深色视觉、四入口、新品/热销、全部产品瀑布流、TabBar 安全降级和埋点预留验收完成 |
| 2026-07-30 15:00:00 | 小程序 SKU 详情页 Change 创建与设计确认 | `add-miniapp-sku-detail-page` 完成 `/req-opsx`，明确 API、媒体、收藏、分享、推荐和异常状态边界 |
| 2026-07-30 17:00:00 | 小程序 SKU 详情页验收准备 | SKU 详情展示、图片/视频浏览、收藏、分享、品牌/推荐跳转、异常状态和安全 URL 验收口径齐全 |
| 2026-07-30 17:30:00 | 小程序分类列表页 Change 创建与设计确认 | `add-miniapp-category-list-page` 完成 `/req-opsx`，明确分类树接口、缓存版本号、双栏交互、二级分类跳转和异常状态边界 |
| 2026-07-30 18:00:00 | 小程序分类列表页验收准备 | 分类 Tab、一级/二级分类、缓存刷新、图片占位、跳转防抖、埋点和视觉验收口径齐全 |
| 2026-07-30 18:00:00 | 小程序搜索通用组件 Change 创建 | `add-miniapp-search-component` 已创建，明确搜索入口组件、搜索首页、联想、结果、筛选、无结果、埋点和小程序原型验收边界 |
| 2026-07-30 18:00:00 | 小程序商品列表页通用组件 Change 创建 | `add-miniapp-product-list-component` 已创建，明确商品列表容器、商品卡片、筛选排序、分页加载和小程序原型验收边界 |
| 2026-07-30 18:00:00 | 小程序全局自定义导航栏 Change 创建 | `add-miniapp-global-custom-navigation-bar` 已创建，明确非首页返回、原生胶囊避让、状态栏避让和内容不遮挡边界 |
| 2026-07-18 18:00:00 | 品牌证书观察点产品澄清 | 明确提醒、统计、批量维护是否拆分为独立 REQ，输出 capture 输入 |
| 2026-07-22 18:00:00 | 待评审范围确认 | 若形成 REQ，完成 `/req-generate`、`/req-complete`、`/req-review` |
| 2026-07-30 18:00:00 | Sprint 范围复核 | 仅将 approved/in_sprint 的 REQ/BUG/Change 纳入正式范围 |

## 6. 风险

| 风险 | 说明 | 缓解 |
|---|---|---|
| 观察点被误当成交付承诺 | 三项仍是复盘行动项，不是已评审需求 | `sprint.yaml` 正式范围仅包含 REQ-0039；观察点先 `/req-capture` |
| 模板 Change 范围扩大到命令自动化 | REQ-0039 当前只承诺模板文档和规范，若改技能会扩大影响面 | 自动套模板仅作为后续确认项；本 Sprint 先落文档/规范 |
| 摘要复用机制过度概括 | REQ-0040 若缺少失效条件，可能漏读高风险门禁 | AC 必须覆盖文件变更、任务风险升级、用户要求重读和失败诊断补读 |
| Skill 批量更新噪音 | 多个命令 Skill 更新可能产生无关差异 | 使用统一短句模板，不复制长规则或长脚本 |
| 小程序 Change 偏大 | `add-miniapp-home` 同时涉及 Backend/API、DB/usage event、小程序 UI、测试和视觉验收 | 实现阶段按 tasks 分层推进，先后端契约和公开字段过滤，再小程序页面闭环，最后文档/测试/验收证据 |
| 小程序首页运行入口脱节 | BUG-0065 暴露 `.ts` 业务逻辑与微信开发者工具实际加载 `.js` 脱节 | `fix-miniapp-home-preview-runtime-entry` 必须先确认运行事实源，再补静态测试和微信开发者工具预览证据 |
| 小程序公开字段边界 | 首页聚合和商品详情若复用后台数据，可能误暴露内部字段或未授权素材 | API schema 和测试必须覆盖 public-field filtering、安全图片 URL、无 raw object key |
| 行为统计隐私边界 | 分享、咨询、详情访问事件若字段过宽，可能写入不必要个人信息 | 事件字典只允许必要商品 ID、页面标识、client type、时间上下文，拒绝 token/cookie/raw payload |
| REQ-0043 Change 待实现 | 已评审 REQ 已纳入 Sprint 且 Change 已创建，apply 前需保持 Sprint 双向追溯 | 下一步 `/opsx-apply update-miniapp-home-style-optimization`，并按 Change tasks 分层开发 |
| 首页体验优化与首期闭环重叠 | REQ-0043 是 REQ-0041 的 refinement，若边界不清可能重复改同一模块 | Change 设计中明确复用 REQ-0041 能力，只做视觉、信息架构、瀑布流和安全降级优化 |
| REQ-0042 Change 待实现 | 需求与 Change 已纳入 Sprint，apply 前仍需确认双向追溯完整 | 执行 `/opsx-apply add-miniapp-custom-navigation-bar` 或 `/sprint-apply sprint-008`，并按 tasks 分层开发 |
| 自定义导航栏与原生系统按钮冲突 | REQ-0042 要求右侧分享/关闭使用小程序原生能力，品牌内容若不避让可能重叠 | Change design 必须处理状态栏高度、右侧原生按钮避让、320-430 pt 宽度和禁止手绘胶囊门禁 |
| REQ-0044 Change 待实现 | 需求与 Change 已纳入 Sprint，apply 前仍需确认双向追溯完整 | 执行 `/opsx-apply add-miniapp-sku-detail-page` 或 `/sprint-apply sprint-008`，并按 tasks 分层开发 |
| fix 缓冲低于建议 | 加入 REQ-0044 后 fix 缓冲为 23.33%，低于 SHOULD >= 30% | 严控 SKU 详情页范围，不纳入购物、询价、库存、在线下单；若出现 P0/P1 缺陷，优先拆出低优先级范围 |
| SKU 详情页 API/DB 边界扩大 | 媒体、收藏、分享、推荐可能牵动接口、数据库和对象存储 URL 策略 | Change 设计必须先确认复用还是新增接口；涉及 contract 时同步 OpenAPI、Orval、docs、测试 |
| REQ-0045 Change 待实现 | 需求与 Change 已纳入 Sprint，apply 前仍需确认双向追溯完整 | 执行 `/opsx-apply add-miniapp-category-list-page` 或 `/sprint-apply sprint-008`，并按 tasks 分层开发 |
| 分类页与商品列表页边界混淆 | 分类页只展示分类结构，若加入商品卡、筛选排序或热门分类会扩大范围 | Change design 必须保留 Out of Scope：不展示商品、价格、收藏、筛选排序和热门分类 |
| 分类树接口与缓存策略不清 | 分类页要求一次返回两级类目与版本号，可能涉及 API contract 或复用现有分类接口 | `/req-opsx` 设计先确认复用或新增；新增/调整 API 时同步 OpenAPI、Orval、docs 和测试 |
| REQ-0046 Change 待实现 | 需求与 Change 已纳入 Sprint，apply 前仍需确认双向追溯完整 | 执行 `/opsx-apply add-miniapp-search-component` 或 `/sprint-apply sprint-008`，并按 tasks 分层开发 |
| Sprint 容量超载 | 纳入 REQ-0046 后估算 31.0 / 30.0 人天，fix 缓冲为 -1.0 人天 | 冻结新增范围；若出现 P0/P1 缺陷，优先延期 REQ-0046 或拆分搜索筛选/埋点范围 |
| 搜索范围重新外溢到管理端 | REQ-0046 评审要求仅保留小程序搜索；若设计阶段恢复搜索配置中心会扩大 API/管理端范围 | `/req-opsx` design 必须保持 Out of Scope：Web 管理后台、店主 Web、后台搜索配置中心和 `/api/admin/search/*` |
| REQ-0047 Change 待实现 | 需求与 Change 已纳入 Sprint，apply 前仍需确认双向追溯完整 | 执行 `/opsx-apply add-miniapp-product-list-component` 或 `/sprint-apply sprint-008`，并按 tasks 分层开发 |
| 商品列表页范围外溢 | 商品列表可能诱导加入后台商品管理、店主 Web 商品列表、购物/询价/收藏等范围外能力 | Change design 必须保持小程序单端范围，并明确不做后台商品管理、店主 Web、购物车、询价、在线下单和收藏 |
| 商品列表与分类/搜索职责重叠 | 分类页、搜索结果和商品列表组件若边界不清，可能重复实现筛选、分页和跳转逻辑 | 设计阶段明确商品列表容器只承接列表展示与状态机，分类页负责分类结构，搜索组件负责关键词与结果入口 |
| REQ-0048 Change 待实现 | 需求与 Change 已纳入 Sprint，apply 前仍需确认双向追溯完整 | 执行 `/opsx-apply add-miniapp-global-custom-navigation-bar` 或 `/sprint-apply sprint-008`，并按 tasks 分层开发 |
| 全局导航栏范围外溢 | 非首页统一导航可能扩展为后台配置、全站重设计或新增业务页面 | Change design 必须保持 REQ-0048 范围：复用导航模块、非首页返回、原生胶囊避让、状态栏避让和内容不遮挡 |
| 自定义导航栏范围外溢 | 原型可能诱导模拟系统胶囊或全局自定义导航 | 本期不强制 `navigationStyle: custom`；如采用必须参考 REQ-0042 并补安全区适配 |
| 批量维护扩大权限与审计面 | 批量显示/隐藏或批量更新有效期会影响前台露出与审计链路 | 后续 PRD 必须补权限、二次确认、审计与回滚验收 |
| 统计口径不清 | 证书类型统计可能涉及类型枚举、长期有效、过期状态交叉口径 | 评审前先明确统计维度与后台列表/指标卡呈现方式 |

## 7. 知识库承接

来自 `docs/knowledge-base/retrospectives/sprint-007-retrospective.md`：

- `A-003`：沉淀 XL 管理端页面分层验收模板，覆盖 DB/API/上传/Orval/Web/Docker/横切 UI gate。本 Sprint 已纳入 `REQ-0039`。
- `A-004`：将规则/Skill 已读摘要复用机制纳入命令上下文预算治理，减少连续命令重复读取。本 Sprint 已纳入 `REQ-0040`。
- `A-005`：为品牌证书能力补充后续运营验收观察点：过期证书提醒、证书类型统计、批量维护。
- 品牌证书管理已形成上传、预览、状态筛选和过期提醒模式，可作为后续运营能力的产品输入。
- `REQ-0041`、`REQ-0042`、`REQ-0043`、`REQ-0044`、`REQ-0045`、`REQ-0046`、`REQ-0047` 与 `REQ-0048` 参考 Sprint 007 中 XL 能力分层验收、成功路径摘要输出和范围控制经验；本次小程序需求不命中管理端 best-practice 标签，但实现必须保留 API / DB / 小程序 / 测试分层证据。

适用最佳实践：

- `docs/knowledge-base/best-practices/admin-list-page-consistency.md`：证书类型统计若进入列表或指标卡，必须沿用 MetricCard、分页 DOM、fixed toast 与 DS confirm。
- `docs/knowledge-base/best-practices/admin-form-page-consistency.md`：批量维护若产生批量表单或设置项，必须避免重复 CTA、原生 confirm 和 layout shift。
- `docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md`：批量维护弹窗必须使用专属 modal class，并验证 computed width。
- `docs/knowledge-base/best-practices/admin-media-upload-chain.md`：若批量维护涉及证书文件替换或上传，必须覆盖上传状态机、MinIO 回显和 Docker `:3000` 上传边界。

## 8. 横切预防清单

| 标签 | Gate 摘要 | 当前状态 |
|---|---|---|
| admin-list | 指标卡 DOM、分页 DOM、fixed toast、DS confirm | REQ-0039 模板必须纳入 |
| admin-form | 单一保存 CTA、DS confirm、fixed toast | REQ-0039 模板必须纳入 |
| admin-modal | 禁止 `modal-card` 与专属类双挂载；验收 computed width | REQ-0039 模板必须纳入 |
| media-upload | 上传状态机、即时回显、后端校验、Docker `:3000` 边界 | REQ-0039 模板必须纳入；具体页面可按 N/A 判定 |
| agent-context-budget | 规则/Skill 摘要复用、失效补读、成功路径紧凑输出 | REQ-0040 必须纳入 |
| miniapp-home | 公开字段过滤、安全图片 URL、原生小程序触控与视口、分享/咨询/热销统计、不做项证据 | REQ-0041 必须纳入；管理端 best-practices 为 N/A |
| miniapp-custom-navigation | 首页 brand-header 品牌展示、原生分享/关闭按钮避让、门店信息排除、搜索框下置、禁止手绘系统胶囊 | REQ-0042 / `add-miniapp-custom-navigation-bar` 必须纳入 |
| miniapp-home-style | 深色品牌视觉、真实小程序导航环境、全部产品瀑布流、TabBar 安全降级、非持久化收藏边界、敏感信息埋点过滤 | REQ-0043 / `update-miniapp-home-style-optimization` 必须纳入 |
| miniapp-sku-detail | 详情字段完整展示、图片/视频混合轮播、图片预览、收藏/分享、推荐去重、安全媒体 URL、购物/询价/库存不做项 | REQ-0044 / `add-miniapp-sku-detail-page` 必须纳入；管理端 best-practices 为 N/A |
| miniapp-category-list | TabBar 分类频道、一级/二级分类双栏、分类树版本缓存、二级分类跳转、图片占位、触控与视口、埋点过滤、不做商品列表页 | REQ-0045 / `add-miniapp-category-list-page` 必须纳入；管理端 best-practices 为 N/A |
| miniapp-search | 搜索入口组件、搜索首页、实时联想、类型 Tab、筛选抽屉、无结果、搜索埋点、44px 触控、管理端搜索配置中心不做项 | REQ-0046 / `add-miniapp-search-component` 必须纳入；管理端 best-practices 为 N/A |
| miniapp-product-list | 商品列表容器、商品卡片、分类/搜索/品牌/推荐入口复用、筛选排序、分页加载、空/错/无更多状态、商品列表埋点、后台商品管理不做项 | REQ-0047 / `add-miniapp-product-list-component` 必须纳入；管理端 best-practices 为 N/A |
| miniapp-global-navigation | 首页保留 brand-header、非首页左侧返回、右侧微信原生胶囊避让、状态栏避让、fixed header 内容不遮挡 | REQ-0048 / `add-miniapp-global-custom-navigation-bar` 必须纳入；管理端 best-practices 为 N/A |
| miniapp-runtime-entry | 微信开发者工具实际运行脚本、`.ts`/`.js` 同步策略、空模板回归测试 | BUG-0065 必须纳入；apply 前须确认 Sprint 双向追溯 |

## 9. 依赖 ASCII 树

```text
sprint-008
├── REQ-0039 xl admin page layered acceptance template
│   └── add-xl-admin-page-acceptance-template
│       ├── docs/standards template
│       ├── DB/API/upload/Orval/Web/Docker gates
│       └── admin-list/form/modal/media-upload X-cut gates
├── REQ-0040 rule/skill summary reuse context budget
│   └── update-rule-skill-summary-reuse-context-budget
│       ├── rules/agent-context-budget.md
│       ├── .agents/skills/*/SKILL.md
│       └── scripts/validate-agent-context-budget.py
├── REQ-0041 miniapp home
│   └── add-miniapp-home
│       ├── backend miniapp home aggregation
│       ├── product usage events and hot ranking
│       ├── src/miniapp home/search/detail/store pages
│       └── docs, OpenAPI/Orval if API changes, tests and visual evidence
├── REQ-0042 miniapp custom navigation bar
│   └── next: /req-opsx REQ-0042-custom-navigation-bar
│       ├── home brand-header brand display
│       ├── native share and close controls
│       ├── exclude store-link and openStoreInfo default navigation
│       └── keep search box below custom navigation
├── REQ-0043 miniapp home style and IA optimization
│   └── update-miniapp-home-style-optimization
│       ├── dark brand visual system
│       ├── StoreHeader/SearchBar/HeroBanner/QuickEntryGrid
│       ├── new/hot product cards and all-product waterfall
│       ├── TabBar labels with safe fallback pages
│       └── miniapp visual, behavior event and non-scope validation
├── REQ-0044 miniapp SKU detail page
│   └── add-miniapp-sku-detail-page
│       ├── detail fields and public data contract
│       ├── image/video mixed gallery and fullscreen preview
│       ├── favorite/share/brand/recommend interactions
│       ├── unavailable, failed media and network states
│       └── API/DB/Orval/docs/tests sync boundary
├── REQ-0045 miniapp category list page
│   └── add-miniapp-category-list-page
│       ├── TabBar category channel and split view
│       ├── primary/secondary category tree and sort order
│       ├── category tree API reuse/new contract and version cache
│       ├── secondary category jump debounce and page restore
│       └── skeleton, empty, image failure, network failure and analytics
├── REQ-0046 miniapp search component and application
│   └── add-miniapp-search-component
│       ├── search entry component and source scope
│       ├── search home, history, hot keywords and recent browse
│       ├── realtime suggestions with debounce and request ordering
│       ├── result tabs, SKU cards, filter drawer and empty state
│       └── analytics and miniapp prototype validation
├── REQ-0047 miniapp product list common component and application
│   └── add-miniapp-product-list-component
│       ├── product list container and reusable state machine
│       ├── product card, stable image ratio and SKU detail navigation
│       ├── category/search/brand/recommend entry contexts
│       ├── filter drawer, sort, pagination and refresh
│       └── analytics, empty/error/no-more states and miniapp prototype validation
├── BUG-0065 miniapp home preview deviation
│   └── fix-miniapp-home-preview-runtime-entry
│       ├── miniapp runtime entry source strategy
│       ├── non-empty page scripts for home/search/detail/store
│       ├── static regression tests for .ts/.js drift
│       └── WeChat Developer Tools preview evidence
└── deferred A-005 brand certificate operations observations
    ├── expired certificate reminder
    ├── certificate type statistics
    └── batch maintenance
        └── next: /req-capture -> /req-complete -> /req-review
```

## 10. 发布计划

本 Sprint 当前包含两个文档/治理型发布对象、七个小程序业务能力发布对象和一个小程序首页缺陷修复对象：XL 管理端页面分层验收模板、规则/Skill 已读摘要复用上下文预算治理、微信小程序首页首期闭环、微信小程序首页品牌自定义导航栏、微信小程序首页样式与信息架构优化、微信小程序 SKU 详情页、微信小程序分类列表页、微信小程序搜索通用组件、微信小程序商品列表页通用组件、BUG-0065 小程序首页预览运行入口修复。三项品牌证书观察点在形成 approved REQ 并进入 OpenSpec Change 前，不进入 release note 的正式发布范围。

## 11. 延后项（待评审）

| 来源 | 优先级 | 观察点 | 下一步 |
|---|---|---|---|
| `sprint-007` 复盘 `A-005` | P2 | 过期证书提醒、证书类型统计、批量维护 | `/req-capture` 后补齐 PRD、验收与评审 |

## 12. 关联文档

- `docs/knowledge-base/retrospectives/sprint-007-retrospective.md`
- `issues/requirements/archive/REQ-0039-xl-admin-page-layered-acceptance-template/`
- `openspec/changes/archive/2026-07-16-add-xl-admin-page-acceptance-template/`
- `issues/requirements/archive/REQ-0040-rule-skill-read-summary-reuse-context-budget/`
- `openspec/changes/archive/2026-07-18-update-rule-skill-summary-reuse-context-budget/`
- `issues/requirements/archive/REQ-0041-miniapp-home/`
- `openspec/changes/archive/2026-07-17-add-miniapp-home/`
- `issues/requirements/archive/REQ-0042-custom-navigation-bar/`
- `issues/requirements/archive/REQ-0043-miniapp-home-style-optimization/`
- `openspec/changes/archive/2026-07-18-update-miniapp-home-style-optimization/`
- `issues/requirements/archive/REQ-0044-miniapp-sku-detail-page/`
- `issues/requirements/archive/REQ-0045-category-list-page/`
- `openspec/changes/archive/2026-07-18-add-miniapp-category-list-page/`
- `issues/requirements/archive/REQ-0046-search-component-application/`
- `openspec/changes/archive/2026-07-19-add-miniapp-search-component/`
- `issues/requirements/archive/REQ-0047-product-list-common-component-application/`
- `issues/bugs/archive/BUG-0065-miniapp-home-preview-deviation/`
- `openspec/changes/archive/2026-07-17-fix-miniapp-home-preview-runtime-entry/`
- `issues/requirements/archive/REQ-0038-brand-certificate-management/`
- `openspec/changes/archive/2026-07-15-add-brand-certificate-management/`
- `docs/knowledge-base/best-practices/admin-list-page-consistency.md`
- `docs/knowledge-base/best-practices/admin-form-page-consistency.md`
- `docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md`
- `docs/knowledge-base/best-practices/admin-media-upload-chain.md`
- `docs/knowledge-base/retrospectives/sprint-008-retrospective.md`

## 13. 关闭记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-19 15:31:45 | /sprint-archive | 用户确认直接关闭；11/11 Change 已归档，`BUG-0065` 已提升至 archive；微信开发者工具/真机视口验收残留作为人工 follow-up。 |
| 2026-07-19 15:38:56 | /sprint-exps | 生成 Sprint 008 迭代经验复盘并回链知识库。 |
