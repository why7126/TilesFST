---
note: workflow-sync — workflow-sync 自动同步 — 0/0 Change archived；0 applied；Sprint `planning`
sprint_id: sprint-009
status: planning
lifecycle_stage: change
created_at: 2026-07-19 12:50:12
updated_at: 2026-07-19 15:52:45
---

# sprint-009 迭代规划

## 1. Sprint 目标

本 Sprint 聚焦微信小程序商品浏览、分类入口、搜索体验修复、首页推荐入口路由修复与顶部导航文案规则收束，将 `REQ-0049-miniapp-product-card-component`、`REQ-0050-miniapp-brand-header-page-title-rules`、`REQ-0051-category-list-product-list-entry-by-level`、`BUG-0066-search-component-prototype-deviation` 与 `BUG-0067-home-recommendation-list-entry-routing` 纳入正式迭代范围。各项均需先创建对应 OpenSpec Change 后再进入实现。

正式目标：

- `REQ-0049-miniapp-product-card-component`：沉淀微信小程序商品卡片组件，统一商品核心信息展示、图片占位、点击跳转、卡片级异常处理和列表场景复用。
- `REQ-0050-miniapp-brand-header-page-title-rules`：收束小程序 `brand-header` 页面标题规则，首页展示两行品牌文案，非首页仅展示一行页面标题并保留返回、状态栏和微信原生胶囊避让。
- `REQ-0051-category-list-product-list-entry-by-level`：补齐分类列表页一级分类聚合商品列表入口与二级分类精确商品列表入口，明确 `categoryLevel` 参数、聚合查询语义、空状态和埋点上下文。
- `BUG-0066-search-component-prototype-deviation`：修复微信小程序搜索组件与 REQ-0046 原型差异，补齐搜索首页、联想、结果、筛选和无结果 5 个状态的原型对齐验收。
- `BUG-0067-home-recommendation-list-entry-routing`：修复首页新品榜、热销榜和推荐模块「查看更多」入口误跳搜索页的问题，确保进入对应商品列表页并补静态回归断言。

## 2. Scope

| 类型 | 编号 | 标题 | 状态 | 估算 | 说明 |
|---|---|---|---|---:|---|
| REQ | REQ-0049-miniapp-product-card-component | 微信小程序商品卡片组件 | approved | 1.0 人天 | 已评审通过；待 `/req-opsx` 创建 Change |
| REQ | REQ-0050-miniapp-brand-header-page-title-rules | 小程序 brand-header 页面标题规则 | approved | 1.0 人天 | 已评审通过；待 `/req-opsx` 创建 Change |
| REQ | REQ-0051-category-list-product-list-entry-by-level | 分类列表页支持一二级分类商品列表入口 | approved | 3.0 人天 | 已评审通过；待 `/req-opsx` 创建 Change |
| BUG | BUG-0066-search-component-prototype-deviation | 搜索组件整体交互与原型差异较大 | approved | 3.0 人天 | 已评审通过；待 `/bug-opsx` 创建修复 Change |
| BUG | BUG-0067-home-recommendation-list-entry-routing | 首页推荐模块查看更多和榜单入口误跳搜索页 | approved | 1.0 人天 | 已评审通过；待 `/bug-opsx` 创建修复 Change |

BUG：`BUG-0066` 与 `BUG-0067` 已纳入正式范围，优先级高于新增体验能力；`BUG-0066` 修复前不得将当前搜索页作为 REQ-0046 的最终原型验收证据，`BUG-0067` 修复前不得将首页新品/热销入口作为商品列表页承接验收证据。

Change：暂未纳入。`REQ-0049`、`REQ-0050`、`REQ-0051`、`BUG-0066` 与 `BUG-0067` 的 OpenSpec Change 均尚未创建，执行开发前必须先运行 `/req-opsx REQ-0049-miniapp-product-card-component`、`/req-opsx REQ-0050-miniapp-brand-header-page-title-rules`、`/req-opsx REQ-0051-category-list-product-list-entry-by-level`、`/bug-opsx BUG-0066-search-component-prototype-deviation` 与 `/bug-opsx BUG-0067-home-recommendation-list-entry-routing`，并将生成的 Change 回填到本 Sprint。

## 3. 工作量与容量

| 项 | 值 |
|---|---:|
| 开发人数 | 2 |
| 测试人数 | 1 |
| Sprint 容量 | 30 人天 |
| 已纳入估算 | 9.0 人天 |
| 容量占用 | 30.00% |
| fix 缓冲 | 21.0 人天 |
| fix 缓冲比例 | 70.00% |

容量门禁：Pass。估算低于容量，且 fix 缓冲满足 SHOULD >= 30% 建议。`BUG-0067` 为 S 级首页推荐入口路由修复，新增 1.0 人天后总占用为 9.0/30.0 人天。

## 4. 里程碑

| 里程碑 | 目标日期 | 说明 |
|---|---|---|
| Sprint 规划完成 | 2026-07-19 12:50:12 | 纳入 `REQ-0049` |
| 范围更新 | 2026-07-19 13:28:32 | 纳入 `BUG-0066` 搜索组件原型偏差修复 |
| 范围更新 | 2026-07-19 14:37:36 | 纳入 `REQ-0050` brand-header 页面标题规则 |
| 范围更新 | 2026-07-19 15:12:56 | 纳入 `REQ-0051` 分类列表页一二级分类商品列表入口 |
| 范围更新 | 2026-07-19 15:52:45 | 纳入 `BUG-0067` 首页推荐入口路由修复 |
| OpenSpec Change 创建 | 2026-07-31 18:00:00 | 运行 `/req-opsx REQ-0049-miniapp-product-card-component`、`/req-opsx REQ-0050-miniapp-brand-header-page-title-rules`、`/req-opsx REQ-0051-category-list-product-list-entry-by-level`、`/bug-opsx BUG-0066-search-component-prototype-deviation` 与 `/bug-opsx BUG-0067-home-recommendation-list-entry-routing` |
| 实现与自测 | 2026-08-08 18:00:00 | 完成商品卡片组件、brand-header 标题规则、分类入口聚合查询、搜索组件原型偏差修复、首页推荐入口路由修复、联调和基础测试 |
| 验收收口 | 2026-08-14 18:00:00 | 完成 acceptance 对照、原型对齐证据与 Sprint 收口 |

## 5. 风险

| 风险 | 影响 | 应对 |
|---|---|---|
| Change 尚未创建 | 无法进入实现与 `/opsx-apply` | 先运行 `/req-opsx REQ-0049-miniapp-product-card-component`，并回填 `changes[]` |
| brand-header 标题规则 Change 尚未创建 | `REQ-0050` 虽已纳入 Sprint，但无法进入 `/opsx-apply` | 先运行 `/req-opsx REQ-0050-miniapp-brand-header-page-title-rules`，并回填 `changes[]` |
| 分类入口 Change 尚未创建 | `REQ-0051` 虽已纳入 Sprint，但无法进入 `/opsx-apply` | 先运行 `/req-opsx REQ-0051-category-list-product-list-entry-by-level`，并回填 `changes[]` |
| BUG 修复 Change 尚未创建 | BUG-0066 虽已纳入 Sprint，但无法进入 `/opsx-apply` | 先运行 `/bug-opsx BUG-0066-search-component-prototype-deviation`，并回填 `changes[]` |
| 首页推荐入口修复 Change 尚未创建 | BUG-0067 虽已纳入 Sprint，但无法进入 `/opsx-apply` | 先运行 `/bug-opsx BUG-0067-home-recommendation-list-entry-routing`，并回填 `changes[]` |
| 商品卡片与父级列表边界混淆 | 可能把筛选、分页、列表容器重新纳入本 REQ | 以 `REQ-0049` acceptance 和 review 条件通过项为边界，只实现单个商品卡片 |
| 搜索修复范围扩散 | 可能把后台搜索配置、热门词管理或自然语言搜索并入本 BUG | 以 `BUG-0066` acceptance 非目标为边界，仅修复小程序搜索原型偏差 |
| 导航规则范围扩散 | 可能把全局导航重设计、底部 TabBar 或后台文案配置并入 REQ-0050 | 以 REQ-0050 acceptance 为边界，只收束首页两行和非首页单行标题规则 |
| 一级分类聚合语义被误实现 | 可能只查询直接挂载在一级分类下的商品，漏掉下属二级分类商品 | REQ-0051 design.md 必须明确 `categoryLevel=primary` 子分类展开与聚合查询策略 |
| 小程序已有原型文件多版本并存 | 视觉验收基准可能不一致 | 以后续 Change design 明确 prototype 优先级，并引用 `prototype/miniapp/` 现有文件 |

## 6. 知识库承接

| 来源 | 承接项 | 本 Sprint 处理 |
|---|---|---|
| `docs/knowledge-base/retrospectives/sprint-007-retrospective.md` | Workflow Sync 与 AI usage hook 成功路径保持 compact summary | 本 Sprint 命令输出只报告摘要、计数、warning 和 recommended action |
| `docs/knowledge-base/retrospectives/sprint-007-retrospective.md` | XL 业务能力前置拆层验收 | 本 Sprint 当前 9.0 人天；后续若 Change 扩大到 API/DB/上传/Web，必须重新估算并拆层 |
| `docs/knowledge-base/retrospectives/sprint-007-retrospective.md` | 归档路径残留检查 | Sprint 收尾阶段关注 `iterations/change/<sprint>` 旧路径残留 |
| `docs/knowledge-base/retrospectives/sprint-008-retrospective.md` | 小程序运行事实源漂移预防 | BUG-0067 修复必须同步 `.ts` 与实际加载 `.js`，并补静态测试防止首页入口再次误跳搜索页 |
| `docs/knowledge-base/retrospectives/sprint-008-retrospective.md` | 页面组件边界重叠预防 | BUG-0067 仅修首页推荐入口路由，不扩大到商品列表页 UI、后端 section 语义或推荐算法 |

## 7. 横切预防清单

| 标签 | 适用性 | 验收 gate |
|---|---|---|
| admin-list | N/A | 微信小程序商品卡片，不涉及管理端列表页 |
| admin-form | N/A | 不涉及管理端表单页 |
| admin-modal | N/A | 不涉及管理端弹窗 |
| media-upload | N/A | 本 REQ 不涉及图片/视频上传链路，仅消费商品图展示 |
| miniapp-prototype-alignment | applicable | BUG-0066 修复必须逐项对照 REQ-0046 的 5 个 HTML/PNG 原型与 AC-BUG-001 至 AC-BUG-014 |
| miniapp-navigation-title | applicable | REQ-0050 实现必须逐页对照首页双行、非首页单行、返回按钮、状态栏和微信原生胶囊避让 AC |
| miniapp-category-product-entry | applicable | REQ-0051 实现必须对照一级分类聚合、二级分类精确、`categoryLevel` 参数、空状态、防重复点击和埋点 AC |
| miniapp-home-recommendation-routing | applicable | BUG-0067 修复必须对照 AC-BUG-001 至 AC-BUG-008，确保新品/热销入口进入商品列表页且搜索场景不回归 |

## 8. 依赖 ASCII 树

```text
sprint-009
├── REQ-0049 微信小程序商品卡片组件
│   ├── parent: REQ-0047 商品列表页通用组件并应用
│   ├── depends-on: REQ-0044 微信小程序 SKU 详情页
│   ├── related: REQ-0045 分类列表页
│   ├── related: REQ-0046 搜索通用组件并应用
│   └── next: /req-opsx REQ-0049-miniapp-product-card-component
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
├── BUG-0066 搜索组件整体交互与原型差异较大
│   ├── related_requirement: REQ-0046 搜索通用组件并应用
│   ├── source_change: add-miniapp-search-component
│   └── next: /bug-opsx BUG-0066-search-component-prototype-deviation
└── BUG-0067 首页推荐模块查看更多和榜单入口误跳搜索页
    ├── related_requirement: REQ-0047 商品列表页通用组件并应用
    ├── source_change: add-miniapp-product-list-component
    ├── affected-entry: 新品榜 / 热销榜 / 新品推荐查看更多 / 热销推荐查看更多
    └── next: /bug-opsx BUG-0067-home-recommendation-list-entry-routing
```

## 9. 发布计划

本 Sprint 当前为小程序商品浏览体验增强、分类入口补齐、顶部导航规则收束、搜索体验修复与首页推荐入口路由修复。若 `REQ-0049`、`REQ-0050`、`REQ-0051`、`BUG-0066` 与 `BUG-0067` 完成实现与验收，可在后续版本公告中归入“微信小程序商品浏览、分类导航、首页推荐入口与搜索体验优化”。

## 10. 关联文档

| 类型 | 路径 |
|---|---|
| REQ trace | `issues/requirements/review/REQ-0049-miniapp-product-card-component/trace.md` |
| REQ requirement | `issues/requirements/review/REQ-0049-miniapp-product-card-component/requirement.md` |
| REQ acceptance | `issues/requirements/review/REQ-0049-miniapp-product-card-component/acceptance.md` |
| 原型 | `issues/requirements/review/REQ-0049-miniapp-product-card-component/prototype/miniapp/` |
| REQ trace | `issues/requirements/review/REQ-0050-miniapp-brand-header-page-title-rules/trace.md` |
| REQ requirement | `issues/requirements/review/REQ-0050-miniapp-brand-header-page-title-rules/requirement.md` |
| REQ acceptance | `issues/requirements/review/REQ-0050-miniapp-brand-header-page-title-rules/acceptance.md` |
| 原型 | `issues/requirements/review/REQ-0050-miniapp-brand-header-page-title-rules/prototype/miniapp/` |
| REQ trace | `issues/requirements/review/REQ-0051-category-list-product-list-entry-by-level/trace.md` |
| REQ requirement | `issues/requirements/review/REQ-0051-category-list-product-list-entry-by-level/requirement.md` |
| REQ acceptance | `issues/requirements/review/REQ-0051-category-list-product-list-entry-by-level/acceptance.md` |
| 原型 | `issues/requirements/review/REQ-0051-category-list-product-list-entry-by-level/prototype/miniapp/` |
| BUG trace | `issues/bugs/review/BUG-0066-search-component-prototype-deviation/trace.md` |
| BUG bug.md | `issues/bugs/review/BUG-0066-search-component-prototype-deviation/bug.md` |
| BUG acceptance | `issues/bugs/review/BUG-0066-search-component-prototype-deviation/acceptance.md` |
| BUG source prototype | `issues/requirements/archive/REQ-0046-search-component-application/prototype/` |
| BUG trace | `issues/bugs/review/BUG-0067-home-recommendation-list-entry-routing/trace.md` |
| BUG bug.md | `issues/bugs/review/BUG-0067-home-recommendation-list-entry-routing/bug.md` |
| BUG acceptance | `issues/bugs/review/BUG-0067-home-recommendation-list-entry-routing/acceptance.md` |

## 11. 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-19 15:52:45 | /sprint-propose | 纳入 BUG-0067，容量估算更新为 9.0/30.0 人天 |
| 2026-07-19 15:12:56 | /sprint-propose | 纳入 REQ-0051，容量估算更新为 8.0/30.0 人天 |
| 2026-07-19 14:37:36 | /sprint-propose | 纳入 REQ-0050，容量估算更新为 5.0/30.0 人天 |
| 2026-07-19 13:28:32 | /sprint-propose | 纳入 BUG-0066，容量估算更新为 4.0/30.0 人天 |
| 2026-07-19 12:50:12 | /sprint-propose | 创建 sprint-009，纳入 REQ-0049 |
