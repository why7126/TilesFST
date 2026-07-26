## MODIFIED Requirements

### Requirement: 管理端瓷砖规格管理页

Web 客户端 MUST 提供瓷砖规格管理页，路由为 `/admin/tile-specs`，视觉 MUST 高保真对齐 `issues/requirements/archive/REQ-0009-tile-spec-management/prototype/web/tile-size-management.html` 与 `tile-size-management-modal.html` 的 CSS Port 策略。页面 MUST 复用 `AdminLayout`（264px Sidebar、右侧独立滚动、主内容最大宽度 1080px）。`admin` 与 `employee` MUST 可访问；`store_owner` MUST NOT 访问。列表底部分页 MUST 复用与用户管理页一致的标准 DOM 与样式（`pagination` + `page-summary` + `page-right` + `page-buttons` + `page-size-wrap`），MUST NOT 使用项目内未定义的 `pagination-bar` / `page-indicator` 结构。表单弹窗保存成功后 MUST 自动重新加载列表与 summary（Toast + 列表 refresh），行为 MUST 与品牌管理页一致。

#### Scenario: 规格页布局

- **WHEN** 已登录 `admin` 或 `employee` 访问 `/admin/tile-specs`
- **THEN** 页面 MUST 展示 page-header（eyebrow「MASTER DATA」、标题「瓷砖规格」、说明、「＋ 新增瓷砖规格」）
- **AND** MUST 展示 4 指标卡（规格总数/启用规格/停用规格/未关联 SKU）、关键词+状态筛选、规格表格与分页
- **AND** MUST NOT 展示导出、批量操作、列表 section 标题行

#### Scenario: 筛选与分页

- **WHEN** 用户输入关键词或选择状态并点击查询
- **THEN** 系统 MUST 重置页码为 1 并重新加载列表
- **AND** 分页左侧 MUST 显示「共 {total} 条」（`page-summary`）
- **AND** 分页 MUST 使用与用户管理页一致的 `page-buttons`（含当前页 `.page-btn.active`）与 `page-size-wrap`（「每页显示」+ 20/50/100 条选项）
- **AND** MUST NOT 使用 `{page} / {totalPages}` 文本指示器替代激活页码按钮

#### Scenario: 列表主列字号

- **WHEN** 用户查看规格表格「尺寸名称」列
- **THEN** 字号与字色 MUST 与同表标准数据列视觉 rhythm 协调
- **AND** MUST NOT 明显大于相邻宽度/长度/厚度列而造成表格层级失衡

#### Scenario: 启停二次确认

- **WHEN** 用户点击行内「启用」或「停用」
- **THEN** MUST 弹出二次确认（对齐 `BrandManagementPage` / REQ-0008）
- **AND** 确认后 MUST 调用 enable/disable API 并刷新列表

#### Scenario: 删除按钮规则

- **WHEN** 列表行 `sku_count` 为 0 且状态为停用
- **THEN** 「删除」MUST 可点击（风险色）
- **WHEN** 其他情况
- **THEN** 「删除」MUST 置灰且 hover 提示「仅允许删除未关联SKU且已停用的规格」

#### Scenario: 新增编辑弹窗

- **WHEN** 用户点击「新增瓷砖规格」或行内「编辑」
- **THEN** MUST 打开宽 720px 弹窗，头尾固定、主体可滚动
- **AND** 字段顺序 MUST 为：宽*、长*、只读尺寸名称（跨列）、厚度、排序*、备注（跨列）
- **AND** MUST NOT 展示状态、规格类型、单位选择、可编辑尺寸名称
- **AND** 宽长变化 MUST 实时生成 `{w}×{l}mm`；重复时 MUST 展示错误并禁止提交（服务端校验仍生效）
- **AND** 备注 `textarea` MUST 在跨列容器内占满整行宽度，固定高度，`resize: none`

#### Scenario: 保存后刷新列表

- **WHEN** 用户通过弹窗成功创建或更新规格
- **THEN** MUST 展示成功 Toast 并关闭弹窗
- **AND** MUST 无需整页刷新即更新列表行与「共 {total} 条」及 4 指标卡 summary
- **AND** MUST 调用与启停/删除相同的列表加载函数（如 `loadSpecs()`）

#### Scenario: 规格管理 CSS Port

- **WHEN** 开发者查看规格管理页源码
- **THEN** 视觉样式 MUST 主要来自 `features/admin/styles/tile-spec-management.css`（或等价 port CSS）
- **AND** 颜色 MUST 通过 semantic token 引用 `globals.css`
- **AND** TSX MUST NOT 包含裸 Hex

#### Scenario: 未登录访问

- **WHEN** 未登录用户访问 `/admin/tile-specs`
- **THEN** 前端 MUST 跳转至 `/admin/login`
