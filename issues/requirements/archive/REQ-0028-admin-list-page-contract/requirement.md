---
requirement_id: REQ-0028-admin-list-page-contract
title: AdminListPage 模板与管理端列表页契约
terminal: web-admin
version: v1
status: done
owner: product
source: capture.md
priority: P1
parent_requirement: REQ-0000-build-design-system
created_at: 2026-07-05 07:56:30
updated_at: 2026-07-11 08:52:43
---

# REQ-0028 AdminListPage 模板与管理端列表页契约

## 1. 需求背景

Web 管理端已经有多个列表型页面，包括瓷砖 SKU、瓷砖品牌、瓷砖类目、瓷砖规格、Banner 管理、用户管理、日志审计和接口文档。BUG-0055 已经修复了这些页面在模块顺序、筛选/搜索交互、固定操作列和分页窗口上的横切不一致问题，但根因并不只是某个页面样式写错，而是管理端列表页缺少统一模板、DOM 契约、设计验收页和新增页面门禁。

当前仓库已有 `src/web/src/shared/templates/admin-list-page.tsx` 与 `AdminListPageContent` 类型，但它仍偏向轻量示例，只覆盖标题、搜索和简单行列表，尚不能承载 BUG-0055 沉淀出的完整管理端列表页结构：标题模块、指标卡模块、筛选/搜索模块、列表模块、分页模块和 sticky action column。后续若继续由各页面自行拼装，管理端列表体验仍会回到“逐页修复、局部对齐、局部漂移”的状态。

本需求将 Sprint 004 复盘行动项 A-002 产品化：落地 `AdminListPage` 模板、管理端列表页契约与 `/design-system` 验收样例，让后续新增或改造管理端列表页有明确的可复用事实源。

## 2. 目标用户

| 用户 | 诉求 |
|---|---|
| 企业内部管理员 | 在不同管理列表页之间获得一致的信息密度、筛选行为、操作列可达性和分页体验 |
| 企业内部运营人员 | 使用品牌、类目、SKU、Banner 等列表页时减少学习成本和误操作 |
| 前端开发人员 | 新增管理端列表页时优先复用统一模板，不再复制页面局部 DOM 与样式 |
| 测试 / QA | 用统一 DOM 契约和设计验收页检查管理端列表页是否回归 |
| 产品负责人 | 将 BUG-0055 经验沉淀为 Design System 能力，而不是一次性修复记录 |

## 3. 范围

### 3.1 本期包含

- 升级或重定义 `AdminListPage` 模板，使其覆盖管理端列表页标准结构：
  - 标题模块；
  - 指标卡模块；
  - 筛选/搜索模块；
  - 列表 / 表格模块；
  - 分页模块；
  - 固定浮动操作列契约。
- 扩展 `AdminListPageContent` 或等价类型，使模板输入能够描述标题、主操作、指标卡、筛选项、表格列、行操作、分页状态和空 / 加载 / 错误态。
- 在 `/design-system` 验收页增加 AdminListPage 样例，展示管理端列表页的完整模块顺序、筛选区、表格、分页和操作列。
- 将 BUG-0055 的横切规则沉淀为模板契约和验收要点，覆盖至少以下页面矩阵：
  - `/admin/tile-skus`
  - `/admin/brands`
  - `/admin/tile-categories`
  - `/admin/tile-specs`
  - `/admin/banners`
  - `/admin/users`
  - `/admin/logs`
  - `/admin/api-docs`
- 明确新增管理端列表页的复用门禁：优先使用 `AdminListPage` 或等价模板，不得在页面内重复实现已有列表骨架。
- 明确与 `REQ-0029-admin-list-foundation-components` 的边界：MetricCard、分页窗口算法等基础组件可由 REQ-0029 独立承接，但 REQ-0028 必须定义它们在 AdminListPage 中的组合位置和验收关系。
- 更新设计验收和文档类事实源的需求范围，后续 `/req-complete` 阶段再补齐 acceptance、prototype 或 checklist。

### 3.2 本期不包含

- 不在 PRD 阶段修改 `src/`、`openspec/` 或实际页面代码。
- 不要求本需求直接重做 BUG-0055 已修复的 8 个页面；实现阶段可选择 1-2 个代表页面作为模板迁移示范。
- 不包含 `MetricCard` 的完整字段能力、分页窗口工具算法的独立组件规格；这些细节优先由 `REQ-0029-admin-list-foundation-components` 承接。
- 不新增或修改后端 API。
- 不修改数据库表结构、索引或迁移脚本。
- 不涉及 MinIO、图片、视频、文件上传或对象存储策略。
- 不影响店主 Web 展示端和微信小程序。
- 不调整 Docker Compose、环境变量或部署方式。

## 4. 信息架构

```text
Design System / Web Admin
├── shared templates
│   └── AdminListPage
│       ├── page-hero
│       │   ├── eyebrow / title / description
│       │   └── primary actions
│       ├── metric-strip
│       │   └── MetricCard[]（可由 REQ-0029 组件化）
│       ├── filter-bar
│       │   ├── keyword / select / date / status filters
│       │   └── reset action
│       ├── table-card
│       │   ├── table header
│       │   ├── table rows
│       │   └── sticky action column
│       └── pagination
│           ├── page-summary
│           └── page-right / page-buttons / page-size
└── /design-system
    └── AdminListPage 验收样例
        ├── 标准密度列表
        ├── loading / empty / error 示例
        └── 分页边界示例（1、5、6+ 页）
```

## 5. 功能要求

### FR-001 AdminListPage 模板结构

- MUST 提供统一的管理端列表页模板或等价模板组合，覆盖标题、指标卡、筛选/搜索、列表和分页模块。
- MUST 默认约束模块顺序为「标题模块 → 指标卡模块 → 筛选/搜索模块 → 列表模块」。
- MUST 支持页面主操作入口，例如新增、刷新、导出、跳转文档等；具体操作是否展示由业务页面传入。
- MUST 支持紧凑管理端信息密度，不得采用营销页、Landing Page 或大面积装饰性布局。
- MUST 允许业务页面按领域提供列定义、筛选项、行操作和空态文案，但不得绕过模板重建基础布局。

### FR-002 列表页契约与类型

- MUST 扩展 `AdminListPageContent` 或建立等价类型，描述页面标题、说明、主操作、指标卡、筛选区、表格列、行数据、行操作、分页状态和状态态。
- MUST 明确表格列和行操作的最小字段，例如列 key、标题、渲染策略、对齐方式、宽度建议、是否属于操作列。
- MUST 支持空数据、加载中、请求失败和权限受限等状态的呈现入口。
- SHOULD 支持业务页面以组合方式插入少量领域特有内容，但该扩展点不得破坏模块顺序和分页 / 操作列契约。
- SHOULD 为模板输出稳定 DOM 标识或 class 契约，供 Vitest/Testing Library 和视觉验收定位。

### FR-003 筛选/搜索契约

- MUST 支持关键词、下拉、日期范围、状态 / 结果等常见筛选控件组合。
- MUST 保留统一「重置」动作，并约束按钮尺寸、圆角、字号、边框和图标策略。
- MUST NOT 在默认管理端列表筛选区展示「查询」或「搜索」显式提交按钮，除非后续评审明确豁免。
- MUST 支持筛选条件变化后将页码重置为第 1 页，并刷新或重新计算列表结果。
- SHOULD 支持筛选项配置化，避免每个页面重新实现筛选 grid、按钮组和重置行为。

### FR-004 表格与 sticky action column

- MUST 支持管理端表格卡片结构，列表模块上方不得出现重复的列表标题、旧版 table toolbar 或割裂 section heading。
- MUST 支持最后一列固定浮动操作列，用于编辑、查看、启停、删除、重置密码等操作。
- MUST 保证表头最后一列和表体最后一列固定行为一致，避免横向滚动时错位。
- MUST 保持行 hover、禁用态、权限态和确认流程的视觉协调，不得因模板化导致既有业务规则回退。
- SHOULD 将 sticky action column 契约沉淀为模板默认能力，而不是页面局部 CSS 约定。

### FR-005 分页契约

- MUST 支持统一分页结构：左侧 `page-summary`，右侧 `page-right`。
- MUST 支持 `page-buttons`、`page-btn`、`active` 或等价统一 class 契约。
- MUST 支持最多展示 5 个可点击页码，不包含上一页 / 下一页按钮。
- MUST 支持总页数为 1 时仍展示统一分页结构，上一页 / 下一页为禁用态，页码 `1` 为当前态。
- MUST 支持切换每页显示条数后将当前页重置为第 1 页。
- SHOULD 与 `REQ-0029-admin-list-foundation-components` 的分页窗口工具复用，避免页面内重复实现页码窗口算法。

### FR-006 设计验收页

- MUST 在 `/design-system` 中增加 AdminListPage 验收样例或 Admin 管理端列表章节。
- MUST 展示至少一个完整列表样例，包含标题、指标卡、筛选区、表格、sticky 操作列和分页。
- SHOULD 展示 loading、empty、error、单页分页、多页分页等边界态。
- SHOULD 展示与 BUG-0055 相关的 8 页面矩阵说明，帮助开发和 QA 判断哪些业务页应使用该模板。
- MUST 使用 Design System semantic token class，不得在 TSX/CSS 中新增裸 Hex 色值。

### FR-007 回归测试与门禁

- MUST 为 AdminListPage 模板或等价组合补充前端测试，覆盖模块顺序、筛选重置、分页窗口和 sticky action column 契约。
- MUST 为 `/design-system` 的 AdminListPage 样例保持可渲染状态，避免新增模板后验收页缺失。
- SHOULD 建立跨页面一致性测试矩阵，至少覆盖 BUG-0055 提到的 8 类管理端列表页面中已迁移或已对齐的页面。
- SHOULD 在后续 `/req-complete` 阶段将测试矩阵拆入 acceptance 和 test-plan，作为 `/opsx-apply` 验收门禁。

## 6. UI 约束

- MUST 继承管理端暗色旗舰风与现有 Admin Shell。
- MUST 优先使用 `src/web/src/shared/templates/`、`src/web/src/shared/ui/`、`src/web/src/components/ui/` 中的既有能力。
- MUST 使用 semantic token class，例如 `bg-page`、`bg-surface`、`text-primary`、`text-secondary`、`border-border-default`、`rounded-card`、`rounded-industrial`。
- MUST 使用 `cn()` 合并 className。
- MUST 保持管理端列表页高密度、可扫描、适合反复操作的工作台风格。
- MUST 在 1366px、1440px、1920px 常见桌面宽度下避免筛选区、表格和分页重叠、裁切或错位。
- SHOULD 保留与 `user-management.css`、`admin-home.css`、`api-docs.css` 等既有管理端样式的兼容策略，迁移时逐步收敛而不是一次性破坏所有页面。

## 7. 权限与安全

- MUST 不改变管理端既有认证与角色权限边界。
- MUST 不因模板化暴露店主端、小程序或未授权用户不可见的管理端数据。
- MUST 保持行操作的权限、禁用态、二次确认和危险操作保护。
- MUST 不展示真实密钥、数据库连接串、MinIO 凭据、Token、Cookie 或真实客户数据。

## 8. 关联需求、BUG 与文档

| 关联项 | 关系 |
|---|---|
| `REQ-0000-build-design-system` | 父需求；本需求属于 Design System / 页面模板治理扩展 |
| `REQ-0029-admin-list-foundation-components` | 子需求；承接 MetricCard 与分页窗口工具等基础组件抽象 |
| `BUG-0055-admin-list-layout-unification` | 经验来源；提供 8 页面矩阵、sticky action column、分页窗口和筛选区一致性规则 |
| `openspec/specs/web-client/spec.md` | 已有管理端列表页横切一致性正式能力，后续 Change 需要与其对齐 |
| `docs/knowledge-base/best-practices/admin-list-page-consistency.md` | 管理端列表页最佳实践，后续完成阶段建议同步更新 |
| `rules/ui-design.md` | 视觉与组件规则来源 |
| `src/web/README.md` | Web Design System 使用约定 |
| `src/web/src/pages/dev/DesignSystemPage.tsx` | 设计验收页入口 |
| `src/web/src/shared/templates/admin-list-page.tsx` | 现有 AdminListPage 初始模板 |
| `src/shared/templates/types.ts` | 跨端模板类型定义位置 |

## 9. 状态块

```yaml
status: done
readiness: Partially Ready
next_step: archived
openspec_change: add-admin-list-page-contract
needs_prototype: true
needs_api_change: false
needs_database_change: false
needs_orval: false
needs_docker_validation: optional
```

## 10. 待完善项

- `/req-complete` 阶段补齐 user-stories、business-flow、acceptance、trace 与 prototype。
- 确认 AdminListPage 首批迁移页面：仅做设计验收样例，还是选择 `/admin/users`、`/admin/tile-skus` 或 `/admin/api-docs` 作为模板迁移示范。
- 确认 `REQ-0029-admin-list-foundation-components` 与本需求的 Sprint 编排顺序；若先做 REQ-0029，则本需求可直接组合基础组件。
- 确认是否同步更新 `docs/knowledge-base/best-practices/admin-list-page-consistency.md` 与 `src/shared/design-system/spec.md`。
- 确认是否需要在 `/design-system` 中提供截图或并排对照验收材料。
