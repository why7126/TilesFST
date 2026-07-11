# 设计系统规范

## Purpose
定义工业石材暗色旗舰风 Design Token、shadcn/ui 基础组件、复合 UI、预览页、校验脚本和治理文档要求，确保 Web UI 一致使用语义 token。
## Requirements
### Requirement: Design Token 层

Web 客户端 MUST 在 `src/web/src/styles/globals.css` 定义 Design Token，映射 `rules/ui-design.md` 色彩、圆角与字距规范，并通过 Tailwind `@theme` 暴露为 semantic utility classes。

#### Scenario: 页面底色 token 可用

- **WHEN** 开发者需要设置页面背景
- **THEN** MUST 使用 semantic class（如 `bg-page`）或 CSS variable `--color-page`
- **AND** 值 MUST 为 `#18160F`

#### Scenario: 品牌金 token 可用

- **WHEN** 开发者需要设置主 CTA 或强调色
- **THEN** MUST 使用 `bg-brand-gold` 或 `text-brand-gold`
- **AND** 值 MUST 为 `#C8A055`

#### Scenario: 边框 token 分级

- **WHEN** 开发者需要设置分割线或输入框边框
- **THEN** MUST 可使用 `border-default`（`rgba(255,255,255,0.07)`）、`border-strong`（`0.18`）、`border-hover`（`0.28`）、`border-focus`（`rgba(200,160,85,0.7)`）

#### Scenario: 圆角 token

- **WHEN** 开发者设置按钮或输入框圆角
- **THEN** MUST 使用 `rounded-industrial`（2px）或 `rounded-card`（3px）
- **AND** MUST NOT 使用 shadcn 默认大圆角（如 `rounded-md`/`rounded-lg`）作为生产组件默认

### Requirement: 禁止裸 Hex 色值（新代码）

Design System 落地后，新增或修改的 Web UI 代码 MUST NOT 在 JSX/TSX 中硬编码 `#18160F`、`#C8A055` 等 design token 对应 Hex 值，MUST 使用 semantic token class 或 CSS variable。

#### Scenario: 新组件使用 token

- **WHEN** 开发者新增 UI 组件
- **THEN** 样式 MUST 引用 Design Token semantic class
- **AND** MUST NOT 内联 `#18160F` 等 Hex 字符串

### Requirement: shadcn/ui 基础组件

Web 客户端 MUST 初始化 shadcn/ui，并在 `src/web/src/components/ui/` 提供以下基础组件：Button、Input、Checkbox、Label、Separator。

#### Scenario: 组件目录存在

- **WHEN** Design System Change 实现完成
- **THEN** `src/web/src/components/ui/button.tsx` 等文件 MUST 存在
- **AND** `components.json` MUST 存在并配置正确

#### Scenario: Button 主 CTA 样式

- **WHEN** 使用 Button `variant="default"`
- **THEN** 按钮 MUST 为金色实底（`bg-brand-gold`）、深色文字（`text-page`）
- **AND** 圆角 MUST 为 2px
- **AND** hover 态 MUST 可感知（亮度或透明度变化）

#### Scenario: Input 工业风样式

- **WHEN** 渲染 Input 组件
- **THEN** 背景 MUST 为透明
- **AND** 默认边框 MUST 使用 `border-strong`
- **AND** focus 态边框 MUST 使用 `border-focus`
- **AND** 默认高度 MUST 支持 `h-16`（64px）尺寸 variant 或 class

#### Scenario: Checkbox 选中态

- **WHEN** Checkbox 被选中
- **THEN** 背景 MUST 为品牌金填充
- **AND** 勾选图标 MUST 为深色，符合 `rules/ui-design.md` §5.6

### Requirement: cn 工具函数

Web 客户端 MUST 提供 `cn()` 工具（clsx + tailwind-merge），供 shadcn 组件与业务组件合并 className。

#### Scenario: cn 可用

- **WHEN** UI 组件需要合并 Tailwind class
- **THEN** MUST 从 `src/web/src/shared/lib/cn.ts` 导入 `cn`
- **AND** 冲突 class MUST 按 tailwind-merge 规则解析

### Requirement: 路径别名

Web 项目 MUST 配置 `@/` 路径别名指向 `src/`，与 shadcn/ui 默认 import 路径一致。

#### Scenario: 别名解析

- **WHEN** 代码 import `@/components/ui/button`
- **THEN** TypeScript 与 Vite MUST 正确解析到 `src/components/ui/button`

### Requirement: 复合 UI 组件（最小集）

Web 客户端 MUST 提供可复用复合组件：`IconInput`（带左侧图标的输入框封装）与 `DividerText`（居中分割文案），供后续登录页与其他表单复用。

#### Scenario: IconInput 结构

- **WHEN** 使用 IconInput
- **THEN** MUST 支持左侧 icon slot、placeholder、error 态
- **AND** MUST 基于 shadcn Input 构建，而非裸 `<input>`

#### Scenario: DividerText 结构

- **WHEN** 使用 DividerText 渲染「其他登录方式」类文案
- **THEN** MUST 展示左右分割线 + 居中弱色文字
- **AND** 分割线 MUST 使用 `border-default` 语义

### Requirement: Design System 预览与验收

Web 客户端 MUST 提供 Design System 预览入口（开发环境路由 `/design-system` 或等效页面），展示 Token 样本与基础组件的全部交互状态。

#### Scenario: 预览页可访问

- **WHEN** 开发环境启动 Web 应用
- **THEN** 用户 MUST 可访问 `/design-system`
- **AND** 页面 MUST 展示 Button、Input、Checkbox 的 default / hover / focus / disabled / error 状态样本

### Requirement: 构建与 Docker 兼容

Design System 实现 MUST 不破坏现有 Web 生产构建与 Docker 镜像构建。

#### Scenario: 本地构建通过

- **WHEN** 运行 `npm run build`（在 `src/web`）
- **THEN** 构建 MUST 成功完成

#### Scenario: Docker Web 构建通过

- **WHEN** 运行 `docker compose build web`
- **THEN** Web 镜像构建 MUST 成功

### Requirement: 文档同步

Design System 落地后 MUST 同步更新相关文档。

#### Scenario: Web README 更新

- **WHEN** Change 完成
- **THEN** `src/web/README.md` MUST 说明 token 位置、shadcn 添加组件命令、禁止裸 Hex 约定

#### Scenario: ui-design 互链

- **WHEN** Change 完成
- **THEN** `rules/ui-design.md` MUST 补充指向 `src/web/src/styles/globals.css` 的 token 实现说明（或互链段落）

### Requirement: Design System 校验脚本

The project MUST provide `scripts/validate-design-system.py` to detect Hex hardcoding, arbitrary Tailwind color values, and unauthorized native HTML controls outside allowed Design System paths.

#### Scenario: 校验脚本存在

- **WHEN** a developer lists `scripts/validate-design-system.py`
- **THEN** the file MUST exist and be executable via `python scripts/validate-design-system.py`

#### Scenario: 基线校验通过

- **WHEN** `python scripts/validate-design-system.py` runs on the repository baseline after Sprint-000 governance fixes
- **THEN** it MUST exit with code 0
- **AND** MUST report Design System validation passed

#### Scenario: token 定义路径豁免

- **WHEN** the validator scans `globals.css`, token definition files, or `/design-system` preview fixtures
- **THEN** those paths MUST be exempt from Hex hardcoding rules as documented in the script

### Requirement: Design System AI 提示词

The project MUST maintain `src/shared/design-system/prompts/` with documented prompts for page, form, and table generation plus UI review rules for AI-assisted development.

#### Scenario: 提示词文件存在

- **WHEN** a developer lists `src/shared/design-system/prompts/`
- **THEN** MUST find at least `generate-page.md`, `generate-form.md`, `generate-table.md`, and `review-ui.md`

#### Scenario: 提示词引用语义 token

- **WHEN** a developer reads the prompt files
- **THEN** instructions MUST require semantic token classes and shared/ui component priority
- **AND** MUST NOT encourage bare Hex or ad-hoc native controls in production UI

### Requirement: Design System 治理文档

Sprint-000 MUST register Design System governance artifacts linking rules, shared tokens, Web styles, validation, and preview entry.

#### Scenario: Shared design-system README

- **WHEN** a developer reads `src/shared/design-system/spec.md` or equivalent README under `src/shared/design-system/`
- **THEN** MUST find token source-of-truth paths and consumption guidance for Web

#### Scenario: Sprint trace 关联

- **WHEN** a developer reads `issues/requirements/archive/REQ-0000-build-design-system/trace.md`
- **THEN** MUST find `change_id: build-design-system` and iteration `sprint-000`

### Requirement: 管理端列表基础组件展示

Design System SHALL provide a development preview or admin design acceptance area for reusable admin list foundation components and the `AdminListPage` page-level template contract. The preview SHALL cover `MetricCard`, `MetricCardGrid`, pagination-window examples, and a complete admin list page sample without introducing new color tokens.

#### Scenario: 展示指标卡基础状态
- **WHEN** 开发者或评审人员访问 `/design-system` 或等效管理端设计验收区
- **THEN** 页面 SHALL 展示 `MetricCard` / `MetricCardGrid` 的正常数值、空值或 loading 占位、danger 描述状态
- **AND** 示例 SHALL 覆盖 2、3、4 个指标卡布局

#### Scenario: 展示分页窗口边界
- **WHEN** 开发者或评审人员查看管理端列表基础组件示例
- **THEN** 页面 SHALL 展示分页窗口在首页附近、居中页和末页附近的最多 5 个页码示例
- **AND** 示例 SHALL 保留 `.page-summary`、`.page-right`、`.page-buttons`、`.page-size-wrap` DOM 契约

#### Scenario: 展示 AdminListPage 页面样例
- **WHEN** 开发者或评审人员访问 `/design-system` 的 AdminListPage 验收样例
- **THEN** 页面 SHALL 展示标题模块、指标卡模块、筛选/搜索模块、表格列表模块、sticky action column 与分页模块
- **AND** 模块顺序 SHALL 为「标题模块 → 指标卡模块 → 筛选/搜索模块 → 列表模块」
- **AND** 示例 SHALL 标注 BUG-0055 涉及页面矩阵：`/admin/tile-skus`、`/admin/brands`、`/admin/tile-categories`、`/admin/tile-specs`、`/admin/banners`、`/admin/users`、`/admin/logs` 与 `/admin/api-docs`

#### Scenario: 展示 AdminListPage 边界态
- **WHEN** 开发者或评审人员查看 AdminListPage 验收样例
- **THEN** 页面 SHALL 展示 loading、empty、error、单页分页和多页分页边界态
- **AND** 单页分页 SHALL 仍展示上一页/下一页禁用态和当前页 `1`

### Requirement: 管理端列表组件语义样式

Design System SHALL require admin list foundation components and the `AdminListPage` template to use semantic token classes, CSS variables, `cn()` class merging, or existing admin list classes, and SHALL NOT introduce raw Hex colors or one-off hardcoded color values in Web UI implementation.

#### Scenario: 新增指标卡组件样式
- **WHEN** 开发者实现或修改 `MetricCard`、`MetricCardGrid` 或 pagination-window presentation
- **THEN** implementation SHALL use semantic token classes or existing admin classes for color, border, radius, typography, and spacing
- **AND** TSX/CSS implementation SHALL NOT add raw Hex values or token-equivalent hardcoded `rgba(...)` colors

#### Scenario: 类名合并
- **WHEN** admin list foundation components accept custom `className`
- **THEN** implementation SHALL merge classes through `cn()` from `@/shared/lib/cn`

#### Scenario: AdminListPage 模板样式
- **WHEN** 开发者实现或修改 `AdminListPage`、`AdminListPageContent` 或等价模板组合
- **THEN** implementation SHALL use semantic token classes such as `bg-page`, `bg-surface`, `text-primary`, `text-secondary`, `border-border-default`, `rounded-card`, or existing admin list classes
- **AND** implementation SHALL merge configurable class names through `cn()`
- **AND** implementation SHALL NOT copy raw Hex values from the prototype into TSX/CSS

### Requirement: 管理端列表组件测试治理

Design System SHALL include test expectations for admin list foundation components and the `AdminListPage` template so DOM contracts remain stable across list pages.

#### Scenario: 指标卡渲染测试
- **WHEN** `MetricCard` is rendered in tests
- **THEN** tests SHALL assert label, value, description, and `.metric-card`, `.metric-label`, `.metric-value`, `.metric-desc` DOM classes

#### Scenario: 展示页结构测试
- **WHEN** the design-system or admin design acceptance example renders foundation components
- **THEN** tests SHOULD assert the example includes normal, empty/loading, danger, and multi-card states

#### Scenario: AdminListPage 模板结构测试
- **WHEN** `AdminListPage` or an equivalent template composition is rendered in tests
- **THEN** tests SHALL assert the module order is title, metrics, filters, list, and pagination
- **AND** tests SHALL assert pagination includes `page-summary`, `page-right`, `page-buttons`, and current `page-btn active` or equivalent roles/classes
- **AND** tests SHALL assert rows with actions expose a sticky action column contract

### Requirement: Web 多主题 Design Token

Web Design System MUST support four theme modes: `system`, `dark_flagship`, `comfort_dark`, and `light`. Theme modes MUST be implemented through semantic tokens and theme-scoped CSS variables, not business-component raw Hex values. Existing industrial stone dark values remain the `dark_flagship` mode baseline; `comfort_dark` and `light` MUST provide complete token values for page, surface, text, border, accent, focus, danger, success, warning, shadow, and overlay semantics.

#### Scenario: 主题模式完整

- **WHEN** Web initializes Design System tokens
- **THEN** `system`, `dark_flagship`, `comfort_dark`, and `light` modes SHALL be available
- **AND** each mode SHALL define complete semantic token values for core page, surface, text, border, accent, focus, feedback, shadow, and overlay semantics.

#### Scenario: 暗色旗舰保持品牌基线

- **WHEN** the active mode is `dark_flagship`
- **THEN** the visual result SHALL preserve the existing industrial stone flagship dark brand baseline
- **AND** existing semantic classes such as `bg-page`, `text-primary`, `text-brand-gold`, and `border-border-default` SHALL continue to resolve without business-page rewrites.

#### Scenario: 业务 UI 禁止裸 Hex

- **WHEN** business Web pages or components are modified for this change
- **THEN** they MUST consume semantic tokens or Design System utilities
- **AND** they MUST NOT introduce raw Hex color values in business UI code.

### Requirement: Design System 主题预览与舒适度验收

The `/design-system` page MUST provide a theme preview surface for all supported theme modes and include representative tile SKU components used in REQ-0020 acceptance.

#### Scenario: 主题切换可预览

- **WHEN** a user opens `/design-system`
- **THEN** the page SHALL allow switching among `system`, `dark_flagship`, `comfort_dark`, and `light`
- **AND** token previews and representative components SHALL update immediately.

#### Scenario: 瓷砖 SKU 组件覆盖

- **WHEN** `/design-system` is used for REQ-0020 acceptance
- **THEN** it SHALL include representative previews for buttons, inputs, tables, dialogs, toast, media upload state, and tile SKU list/form/modal components
- **AND** those previews SHALL be usable to verify login/list/form/modal comfort regressions across themes.

### Requirement: Clipboard 复制交互治理

Design System governance SHALL document or preview the Web admin Clipboard copy pattern so future copy interactions reuse the shared helper or an equivalent best-practice instead of duplicating page-local Clipboard API branching.

#### Scenario: 复制 helper 使用边界可查

- **WHEN** developers read the Web README, Design System notes, or change design produced by this change
- **THEN** they SHALL find that the Clipboard helper owns copy result normalization
- **AND** callers own toast, dialog text, usage events, and business-specific side effects.

#### Scenario: Design System 约束保持

- **WHEN** an implementation adds or modifies copy buttons, toast feedback, or modal copy status text
- **THEN** it SHALL use existing admin UI patterns, semantic token classes, CSS variables, or existing admin classes
- **AND** it SHALL NOT add raw Hex colors or one-off hardcoded design colors in production Web UI.

#### Scenario: 复制交互不引入新 UI 体系

- **WHEN** copy feedback is implemented for admin list rows or admin modal dialogs
- **THEN** it SHALL use existing fixed toast, `role="status"`, modal help text, or equivalent existing Design System feedback patterns
- **AND** it SHALL NOT introduce a new global toast/dialog library for this change.

### Requirement: Clipboard 横切验收

Design System acceptance SHALL include cross-cutting checks for admin list and admin modal copy interactions where this change touches those surfaces.

#### Scenario: 管理端列表复制反馈无布局位移

- **WHEN** an admin list page copy action succeeds, fails, or falls back to manual copy
- **THEN** feedback SHALL NOT push the page hero, filters, table, or pagination in document flow
- **AND** pagination DOM SHALL remain aligned with the admin list baseline when the page is touched by this change.

#### Scenario: 管理端弹窗复制反馈不破坏弹窗布局

- **WHEN** generated-password copy feedback is shown inside a modal
- **THEN** modal width, body scroll, input visibility, and footer button reachability SHALL remain stable
- **AND** implementation SHALL NOT combine generic `modal-card` with a feature-specific modal card class in a way that reintroduces CSS cascade width overrides.

