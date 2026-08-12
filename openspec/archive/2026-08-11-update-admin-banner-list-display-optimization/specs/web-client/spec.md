## MODIFIED Requirements

### Requirement: 管理端列表页横切一致性

Web 客户端 MUST 统一管理端列表型页面的模块顺序、筛选/搜索交互、表格最后一列固定浮动和分页页码呈现。适用页面 MUST 包含 `/admin/tile-skus`、`/admin/brands`、`/admin/tile-categories`、`/admin/tile-specs`、`/admin/banners`、`/admin/users`、`/admin/logs` 与 `/admin/api-docs`。上述页面 MUST 按「标题模块 → 指标卡模块 → 筛选/搜索模块 → 列表模块」顺序展示；筛选/搜索模块 MUST 以瓷砖 SKU 页为交互和样式基线但 MUST NOT 展示【查询】或【搜索】显式提交按钮；重置按钮 MUST 保持统一尺寸和样式；列表最后一列 MUST 使用以接口文档页为基线的固定浮动操作列；分页 MUST 最多展示 5 个可点击页码。新增或迁移管理端列表页 MUST 优先复用 `AdminListPage` 或等价 Design System 模板组合，不得在业务页面内重复实现已有列表页骨架、分页 DOM、sticky action column 或 fixed toast 契约。

`/admin/banners` 列表 MUST 将 Banner 列作为图片识别列，仅展示主图、缩略图或缺图 fallback，不得展示标题、内部识别、展示位置、状态、排序、跳转类型或更新时间等文字。`/admin/banners` MUST 新增独立“跳转对象”列，展示管理端 Banner API 返回的跳转对象文案。新增列后展示位置、展示端、跳转类型、状态、有效期、排序、更新时间和操作列 MUST 保留。

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

#### Scenario: Banner 列仅展示图片

- **WHEN** 已登录管理端用户访问 `/admin/banners`
- **THEN** Banner 列 MUST 仅渲染主图、缩略图或缺图 fallback
- **AND** Banner 列 MUST NOT 渲染标题、内部识别或其他文本
- **AND** 图片加载失败时 MUST 沿用既有 fallback，不得显示浏览器默认破图。

#### Scenario: Banner 跳转对象列

- **WHEN** `/admin/banners` 列表项包含跳转对象展示字段
- **THEN** 表格 MUST 展示独立“跳转对象”列
- **AND** 品牌详情 MUST 显示品牌名称
- **AND** SKU 详情 MUST 显示 SKU 名称且不显示 SKU 编码
- **AND** 专题页 MUST 显示专题名称
- **AND** 外部链接 MUST 显示链接地址
- **AND** 无跳转 MUST 显示 `-`。

#### Scenario: Banner 跳转对象长文本不撑宽表格

- **WHEN** 跳转对象为长外部链接或长名称
- **THEN** 单元格 MUST 使用截断、title tooltip 或等价方式保留完整可访问信息
- **AND** 表格、分页、筛选区和 sticky 操作列 MUST 不被撑破、遮挡或错位。

#### Scenario: Banner 列表字段不换行

- **WHEN** 管理员查看 `/admin/banners` 列表
- **THEN** 除“有效期”列可保留起止时间换行展示外，所有表头字段 MUST 单行展示
- **AND** Banner 列、展示位置、展示端、跳转类型、跳转对象、状态、排序、更新时间和操作列字段 MUST 单行展示，不得自动换行。
