## MODIFIED Requirements

### Requirement: 管理端列表页横切一致性

Web 客户端 MUST 统一管理端列表型页面的模块顺序、筛选/搜索交互、表格最后一列固定浮动和分页页码呈现。适用页面 MUST 包含 `/admin/tile-skus`、`/admin/brands`、`/admin/tile-categories`、`/admin/tile-specs`、`/admin/banners`、`/admin/users`、`/admin/logs` 与 `/admin/api-docs`。上述页面 MUST 按「标题模块 → 指标卡模块 → 筛选/搜索模块 → 列表模块」顺序展示；筛选/搜索模块 MUST 以瓷砖 SKU 页为交互和样式基线但 MUST NOT 展示【查询】或【搜索】显式提交按钮；重置按钮 MUST 保持统一尺寸和样式；列表最后一列 MUST 使用以接口文档页为基线的固定浮动操作列；分页 MUST 最多展示 5 个可点击页码。新增或迁移管理端列表页 MUST 优先复用 `AdminListPage` 或等价 Design System 模板组合，不得在业务页面内重复实现已有列表页骨架、分页 DOM、sticky action column 或 fixed toast 契约。

#### Scenario: 列表页模块顺序统一

- **WHEN** 已登录管理端用户访问任一适用页面
- **THEN** 页面 MUST 先展示标题模块
- **AND** 标题模块之后 MUST 展示指标卡模块
- **AND** 指标卡模块之后 MUST 展示筛选/搜索模块
- **AND** 筛选/搜索模块之后 MUST 展示列表模块
- **AND** 列表模块上方 MUST NOT 展示重复的列表标题、旧版 table toolbar 或割裂的 section heading。

#### Scenario: 筛选区无查询按钮

- **WHEN** 用户查看任一适用页面的筛选/搜索模块
- **THEN** 页面 MUST NOT 展示文案为「查询」或「搜索」的显式提交按钮
- **AND** 页面 MUST 展示统一形态的「重置」按钮
- **AND** 筛选控件变化 MUST 将当前页重置为 1 并刷新或重新计算列表结果。

#### Scenario: 日志审计状态结果筛选使用下拉

- **WHEN** 用户查看 `/admin/logs` 的状态 / 结果筛选项
- **THEN** 页面 MUST 使用下拉选择交互，而不是自由输入框
- **AND** 下拉 MUST 同时支持 `result=success`、`result=failed` 与常见 HTTP status code 精确筛选
- **AND** 常见 HTTP status code MUST 至少包含 200、201、204、301、302、304、400、401、403、404、409、422、429、500、502、503、504
- **AND** 若当前列表数据出现上述静态集合未覆盖的状态码，页面 SHOULD 将该状态码补充为可选项。

#### Scenario: 日志审计操作者筛选使用可搜索单选下拉

- **WHEN** 用户查看 `/admin/logs` 的操作者筛选项
- **THEN** 页面 MUST 使用单选可搜索下拉，而不是 User ID 自由输入框
- **AND** 下拉 MUST 支持按用户名称和账号模糊搜索
- **AND** 候选项 MUST 只展示账号和用户名称两行，不展示角色或状态
- **AND** 已选态 MUST 展示用户名称或名称加账号，不展示裸 User ID
- **AND** 清空或重置后 MUST 恢复全部操作者筛选。

#### Scenario: 日志审计时间范围使用固定最近窗口

- **WHEN** 用户查看 `/admin/logs` 的时间范围筛选项
- **THEN** 页面 MUST 提供最近5分钟、最近10分钟、最近30分钟、最近1小时、最近3小时、最近6小时、最近12小时、最近1天、最近2天、最近3天和最近7天
- **AND** 页面 MUST NOT 提供全部时间选项
- **AND** 默认时间范围 MUST 为最近1天。

#### Scenario: 日志审计操作者候选状态可用

- **WHEN** `/admin/logs` 操作者候选处于加载中、无结果或加载失败状态
- **THEN** 下拉控件 MUST 展示可感知状态
- **AND** 候选失败反馈 MUST 使用 fixed toast 或等价固定层时不得造成 hero、筛选区或表格纵向位移
- **AND** 页面 MUST 允许用户继续使用日志类型、状态、时间范围、Task Trace ID、路径 / Request ID 等其他筛选。

#### Scenario: 重置按钮统一

- **WHEN** 用户对比任一适用页面的筛选/搜索模块
- **THEN** 重置按钮 MUST 使用统一高度、padding、圆角、字号、边框和图标策略
- **AND** 点击重置 MUST 清空或恢复默认筛选条件
- **AND** 点击重置 MUST 将当前页重置为 1。

#### Scenario: 最后一列固定浮动

- **WHEN** 任一适用页面的列表存在操作列
- **THEN** 最后一列表头和单元格 MUST 在横向滚动时保持可见
- **AND** 固定列 MUST 使用与接口文档页一致的右侧背景、左侧分割线和阴影层次
- **AND** 行 hover 时固定列背景 MUST 与当前行 hover 状态协调
- **AND** 固定列内的编辑、启停、删除、查看、重置密码等操作权限、禁用态和确认流程 MUST 不回退。

### Requirement: Web 管理端列表与分页移动端基础可用

Web 管理端列表型页面 MUST 在手机和小屏平板视口下保持筛选区、指标卡、表格、分页和行内操作基础可用。适用页面 MUST 包含 `/admin/brands`、`/admin/banners`、`/admin/tile-categories`、`/admin/tile-specs`、`/admin/tile-skus`、`/admin/users`、`/admin/logs` 与 `/admin/api-docs`。列表页 MUST 保留既有管理端列表横切一致性契约，包括模块顺序、指标卡 DOM、固定 toast、DS confirm modal、固定操作列与统一分页 DOM。

#### Scenario: 筛选区移动端降级

- **WHEN** 用户在 `≤1023px` 视口访问任一适用列表页
- **THEN** 筛选区 MUST 降为 2 列、1 列或等价适配布局
- **AND** 在 `≤639px` 视口下筛选输入框、选择框、重置按钮和其他筛选控件 MUST 不重叠、不超出父容器且可键盘聚焦
- **AND** 筛选控件变化或重置后 MUST 保持既有业务筛选行为和权限边界。

#### Scenario: 日志审计操作者下拉移动端可用

- **WHEN** 用户在 `≤639px` 视口访问 `/admin/logs` 并打开操作者下拉
- **THEN** 下拉面板 MUST 限制在筛选控件或视口可用宽度内
- **AND** 用户名称、账号、加载态、空态和错误态 MUST 不与后续筛选项或表格内容重叠
- **AND** 选择或清空操作者后页面 body、Shell、`.main-content` 与 `.content-inner` MUST NOT 出现不可控横向滚动。

#### Scenario: 表格滚动限制在容器内

- **WHEN** 任一适用列表页的表格内容宽于移动视口
- **THEN** 横向滚动 MUST 限制在 `table-card` 或等价表格容器内
- **AND** 页面 body、Shell、`.main-content` 与 `.content-inner` MUST NOT 出现不可控横向滚动
- **AND** 关键标识列、状态列和操作列 MUST 可访问；隐藏次要列时 MUST NOT 隐藏核心操作。

#### Scenario: 分页移动端可操作

- **WHEN** 任一适用列表页在 `375px` 宽度展示分页
- **THEN** 分页 MUST 使用左侧 `page-summary` 与右侧 `page-right` 的统一结构
- **AND** `.page-buttons`、上一页、下一页、每页条数和总数摘要 MUST 可换行或分组展示
- **AND** 页码和每页条数控件 MUST 不互相覆盖，且可点击页码数量仍 MUST 不超过 5 个。

#### Scenario: 列表横切 AC 保持

- **WHEN** 本 Change 触及任一适用列表页
- **THEN** 指标卡 DOM MUST 使用 `.metric-label`、`.metric-value`、`.metric-desc`
- **AND** 操作成功或失败反馈 MUST 不引起 hero、筛选区、表格或分页纵向位移
- **AND** 页面实现 MUST NOT 使用 `window.confirm` 或 `window.alert`。
