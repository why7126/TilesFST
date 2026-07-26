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

#### Scenario: 分页最多五个可点击页码

- **WHEN** 任一适用页面展示分页
- **THEN** 分页 MUST 使用左侧 `page-summary` 与右侧 `page-right` 的统一结构
- **AND** 页码按钮 MUST 使用 `page-buttons`、`page-btn`、`active` 或等价统一 class
- **AND** 可点击页码数量 MUST 不超过 5 个，不包含上一页/下一页按钮
- **AND** 总页数为 1 时 MUST 仍展示统一分页结构，上一页/下一页为禁用态，页码 `1` 为当前态
- **AND** 切换每页显示条数 MUST 将页码重置为 1。

#### Scenario: 新增管理端列表页复用模板

- **WHEN** 开发者新增或重构管理端列表型页面
- **THEN** 页面 MUST 优先使用 `AdminListPage` 或等价模板组合承载标题、指标卡、筛选/搜索、列表和分页模块
- **AND** 页面 MUST NOT 在业务页面内重复实现已有分页 DOM、sticky action column、固定 toast 或列表骨架
- **AND** 业务页面 MAY 通过列定义、筛选项、行操作、状态态文案或受控 slot 插入领域内容，但 MUST NOT 破坏模块顺序、分页结构或操作列契约。

#### Scenario: 非目标端不受影响

- **WHEN** 本修复完成
- **THEN** 店主 Web 展示端和微信小程序 MUST 不受此列表页一致性修复影响
- **AND** 后端 API、数据库、MinIO、媒体上传和 Docker Compose MUST 不因本修复发生契约变化。
