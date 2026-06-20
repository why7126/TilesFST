## MODIFIED Requirements

### Requirement: 管理端瓷砖类目管理页

Web 客户端 MUST 提供瓷砖类目管理页，路由为 `/admin/tile-categories`，视觉 MUST 高保真对齐 **`REQ-0007-tile-category-management-refine`** 目录下 v2 context（相对 `REQ-0005-tile-category-management/prototype/web/tile-category-management.html` 的 CSS Port diff）与 `tile-category-management-add.html` 弹窗策略。页面 MUST 复用 `AdminLayout`（264px Sidebar、右侧独立滚动、主内容最大宽度 1080px）。`admin` 与 `employee` MUST 可访问；`store_owner` MUST NOT 访问。

#### Scenario: 类目页布局

- **WHEN** 已登录 `admin` 或 `employee` 访问 `/admin/tile-categories`
- **THEN** 页面 MUST 展示 page-header（eyebrow「CATEGORY MANAGEMENT」、标题「瓷砖类目管理」、说明、「＋ 新增类目」）
- **AND** MUST 展示 4 指标卡、类目检索区（**无**外层 section 标题）、左侧类目树（280px）与右侧类目列表（**无**外层「类目列表」section 标题）
- **AND** MUST NOT 展示导出按钮或批量操作入口

#### Scenario: 类目树与列表联动

- **WHEN** 用户点击类目树节点
- **THEN** 右侧列表 MUST 刷新为该节点及其子级类目
- **AND** 表格工具栏 MUST 同步当前节点名称与记录数（`cat-table-toolbar`）

#### Scenario: 筛选与分页

- **WHEN** 用户输入关键词或选择状态/层级并点击查询
- **THEN** 系统 MUST 重置页码为 1 并重新加载列表
- **AND** 分页 MUST 支持每页显示数 10/20/50；切换 page_size MUST 重置页码为 1 并保留筛选条件
- **AND** 分页左侧 MUST 展示「共 {total} 个类目」（`total` 与 API 列表总数一致）
- **AND** 分页右侧 MUST 展示页码控件与「每页显示」条数选择（选项文案「10 条」「20 条」「50 条」）
- **AND** MUST NOT 展示「当前显示 x-y / N 条」「x-y / N」等 v1 分页文案

#### Scenario: 列表工具栏

- **WHEN** 用户查看列表工具栏
- **THEN** MUST 仅展示「调整排序」按钮（右侧）
- **AND** 左侧 MUST 展示树上下文标题与「共 {total} 条记录」
- **AND** MUST NOT 展示「导出」

#### Scenario: 列表行启停操作

- **WHEN** 列表行状态为 `ENABLED`
- **THEN** 操作列 MUST 展示「编辑」与「停用」
- **AND** MUST NOT 展示「删除」
- **WHEN** 列表行状态为 `DISABLED`
- **THEN** 操作列 MUST 展示「编辑」与「启用」（无论 `sku_count` 是否为 0）
- **WHEN** 用户点击「启用」或「停用」
- **THEN** MUST 先展示启停确认弹窗，MUST NOT 直接调用 API
- **WHEN** 用户在确认弹窗点击「确认启用」或「确认停用」
- **THEN** MUST 调用 `POST /api/v1/admin/tile-categories/{id}/enable` 或 `.../disable` 并刷新列表与树
- **WHEN** 用户取消或关闭确认弹窗
- **THEN** MUST NOT 改变类目状态

#### Scenario: 启停确认弹窗

- **WHEN** 用户触发启停确认
- **THEN** MUST 展示与「删除类目」确认框相同结构的 modal（`modal-backdrop` + `modal-card`）
- **AND** 停用标题 MUST 为「停用类目」；启用标题 MUST 为「启用类目」
- **AND** 正文 MUST 含类目 `{name}`；停用 MUST 含前台不可见说明
- **AND** 底部 MUST 含「取消」与「确认停用」/「确认启用」

#### Scenario: 删除入口规则

- **WHEN** 列表行 `sku_count` 为 0 且状态为停用
- **THEN** MUST 展示可点击「删除」（风险色），且 **同时** MUST 展示「启用」
- **WHEN** 列表行处于启用状态
- **THEN** MUST NOT 展示删除入口
- **WHEN** 列表行停用且 `sku_count > 0`
- **THEN** MAY 展示置灰「删除」并提示规则；MUST 仍展示可点击「启用」
- **AND** 删除 MUST 仍使用独立「删除类目」确认弹窗，MUST NOT 与启停确认合并

#### Scenario: 新增编辑弹窗

- **WHEN** 用户点击「新增类目」或行内「编辑」
- **THEN** MUST 打开宽 560px 居中弹窗，暗色遮罩 + blur
- **AND** 字段 MUST 一行一个：上级类目、类目名称、类目编码、排序权重、类目描述、状态（Switch）
- **AND** 类目名称、编码、排序 MUST 必填；排序 MUST 仅允许正整数
- **AND** 选择三级类目作为上级时 MUST 禁止保存子级

#### Scenario: 类目管理 CSS Port

- **WHEN** 开发者查看类目管理页源码
- **THEN** 视觉样式 MUST 主要来自 `features/admin/styles/tile-category-management.css`（或等价 port CSS）
- **AND** 颜色 MUST 通过 `var(--color-*)` 引用 `globals.css`
- **AND** TSX MUST NOT 包含裸 Hex
- **AND** 分页 SHOULD 复用与 `UserManagementPage` 一致的 DOM class（`.pagination`、`.page-summary`、`.page-right`）或等价样式

#### Scenario: 未登录访问

- **WHEN** 未登录用户访问 `/admin/tile-categories`
- **THEN** 前端 MUST 跳转至 `/admin/login`

#### Scenario: 调整排序占位

- **WHEN** 用户点击「调整排序」且本期未实现 reorder
- **THEN** 系统 MAY 展示 Toast「排序调整功能即将上线」
- **AND** MUST NOT 抛出未捕获错误
