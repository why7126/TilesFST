## MODIFIED Requirements

### Requirement: 管理端 Banner 管理页

Web 客户端 MUST 提供 Banner 管理页，路由为 `/admin/banners`，视觉 MUST 高保真对齐 `issues/requirements/archive/REQ-0016-banner-management/prototype/web/banner-management-list.html` 与 `banner-management-list.png` 的 CSS Port 策略（**展示位置独立列**与第一列仅标题为 BUG-0039 策略 delta，MUST 以本 requirement 为准）。页面 MUST 复用 `AdminLayout`（264px Sidebar、右侧独立滚动、主内容最大宽度 1080px）。`admin` 与 `employee` MUST 可访问；`store_owner` MUST NOT 访问。列表表格 MUST NOT 展示与 page-hero 重复的「Banner 列表」section 标题或「当前显示 X-Y / N」toolbar 统计行。列表底部分页 MUST 复用与用户管理页一致的标准 DOM 与样式（`pagination` + `page-summary` + `page-right` + `page-buttons` + `page-size-wrap`），MUST NOT 使用 `banner-pagination` / `table-toolbar` 范围行结构。展示端筛选、表格和弹窗文案 MUST 仅表达“小程序”；展示位置 MUST 仅表达“首页轮播”和“品牌列表页轮播”。

#### Scenario: Banner 列表页布局

- **WHEN** 已登录 `admin` 或 `employee` 访问 `/admin/banners`
- **THEN** 页面 MUST 展示 page-hero（眉标 `OPERATIONS / BANNER MANAGEMENT`、标题「Banner 管理」、说明、「＋ 新增 Banner」）
- **AND** MUST 展示 4 指标卡（Banner 总数/当前筛选/已上线/待生效）
- **AND** MUST 展示关键词、展示端、展示位置、状态、时间状态筛选与 Banner 表格、分页
- **AND** 展示端控件 MUST 仅显示“小程序”或等价只读表达
- **AND** 展示位置控件 MUST 仅提供“首页轮播”和“品牌列表页轮播”
- **AND** 表格 MUST 含 Banner 缩略图（86×38）与标题、**展示位置**、展示端、跳转类型、状态、有效期、排序、更新时间、操作
- **AND** 第一列 MUST 仅展示缩略图与 Banner 标题，MUST NOT 在同一单元格叠放展示位置副文案
- **AND** MUST NOT 展示导出、批量操作
- **AND** MUST NOT 展示「Banner 列表」section 标题或「当前显示 … / …」toolbar 行。

#### Scenario: 展示位置独立列

- **WHEN** 管理员查看 Banner 列表表格
- **THEN** MUST 存在表头「展示位置」
- **AND** 单元格 MUST 展示 `position` 对应中文文案「首页轮播」或「品牌列表页轮播」
- **AND** 「展示位置」列 MUST 与「展示端」列语义区分，MUST NOT 重复展示同一信息。

#### Scenario: 筛选与分页

- **WHEN** 用户输入筛选条件并点击查询
- **THEN** 系统 MUST 重置页码为 1 并重新加载列表
- **AND** 分页左侧 MUST 显示「共 {total} 个 Banner」（`page-summary`）
- **AND** 分页 MUST 使用与用户管理页一致的 `page-buttons`（含当前页 `.page-btn.active`）与 `page-size-wrap`（「每页显示」+ 10/20/50 条选项）
- **AND** MUST NOT 使用连续多页码条替代单页 active 按钮模式
- **AND** `total` MUST 仅统计小程序两个轮播位置范围内的 Banner。

#### Scenario: 上线与下线二次确认

- **WHEN** 用户点击行内「上线」或「下线」
- **THEN** MUST 弹出二次确认（对齐 `BrandManagementPage` / REQ-0008）
- **AND** 确认后 MUST 调用 online/offline API 并刷新列表。

#### Scenario: 删除按钮规则

- **WHEN** 列表行 `status=ONLINE`
- **THEN** 「删除」MUST 不可点；提示「已上线 Banner 需先下线后删除」
- **WHEN** `status` 为 `DRAFT`、`OFFLINE` 或 `EXPIRED`
- **THEN** 「删除」MUST 可点击且二次确认。

#### Scenario: Banner 管理 CSS Port

- **WHEN** 开发者查看 Banner 管理页源码
- **THEN** 视觉样式 MUST 主要来自 `features/admin/styles/banner-management.css`
- **AND** 颜色 MUST 通过 semantic token 引用 `globals.css`
- **AND** TSX MUST NOT 包含裸 Hex。

#### Scenario: 未登录访问

- **WHEN** 未登录用户访问 `/admin/banners`
- **THEN** 前端 MUST 跳转至 `/admin/login`。

#### Scenario: 管理端列表横切质量

- **WHEN** 开发者实现 Banner 管理范围收敛
- **THEN** 分页 DOM MUST 对齐用户管理基准
- **AND** 指标卡 MUST 使用 `.metric-label`、`.metric-value`、`.metric-desc` 或共享 `MetricCard`
- **AND** 保存、删除、上线、下线反馈 MUST 使用 fixed toast 或等价固定反馈
- **AND** 状态/危险操作 MUST 使用 DS confirm modal
- **AND** MUST NOT 使用 `window.confirm` 或会造成 layout shift 的文档流 notice。

### Requirement: Banner 新增编辑弹窗

Web 客户端 MUST 提供 `BannerFormModal`，宽 **880px**（与瓷砖 SKU 弹窗 `.sku-modal-card` 一致，`max-width: 100%` 响应式保留）、最大高度 92vh、内容区可滚动（头尾固定）。弹窗 MUST 按 `jump_type` 展示条件字段：`SKU_DETAIL`（关联 SKU + 图库选图）、`BRAND_DETAIL`（关联品牌 + 品牌 Logo 取图）、`EXTERNAL_LINK`（HTTPS 外链）、`TOPIC_PAGE`（关联专题）、`NO_JUMP`（无跳转目标）。弹窗 MUST NOT 展示状态编辑或状态策略说明块。Banner 图片模块 MUST NOT 展示冗余来源首行标题（如「自定义上传 / SKU 主图」）；自定义上传按钮 MUST 使用「选择/更换/上传中」文案并对齐 `BrandFormModal` 的 `hidden` file input 模式。展示端 MUST 默认为“小程序”且不得保存为其他端；展示位置 MUST 仅允许“首页轮播”和“品牌列表页轮播”。关联 SKU、关联品牌与关联专题 MUST 为单一可搜索选择控件（Combobox），MUST NOT 分离为独立搜索框与下拉框。运营备注 `textarea` MUST 占满整行且 placeholder 字号与同弹窗 input 一致。有效期 MUST 为单字段区间「{开始} 至 {结束}」，格式 `YYYY-MM-DD HH:mm`（分钟精度），MUST NOT 使用原生 `<input type="datetime-local">` 作为最终方案。视觉 MUST 对齐管理端大表单弹窗基准（宽度与 SKU 弹窗一致）。

#### Scenario: 公共字段

- **WHEN** 用户打开新增或编辑 Banner 弹窗
- **THEN** MUST 展示 Banner 标题、展示端、展示位置、Banner 图片、跳转类型、排序、有效期、运营备注
- **AND** 展示端 MUST 显示为“小程序”且不得出现 Web 首页、专题页等旧选项
- **AND** 展示位置 MUST 仅提供“首页轮播”和“品牌列表页轮播”
- **AND** 新增 Banner 默认展示位置 SHOULD 为“首页轮播”
- **AND** 主按钮 MUST 为「保存 Banner」品牌金样式
- **AND** 弹窗主体超出视口时 MUST 可纵向滚动且 footer 操作按钮始终可达。

#### Scenario: jump_type 切换

- **WHEN** 用户切换跳转类型
- **THEN** MUST 清空不兼容的跳转目标字段
- **AND** MUST 展示对应该类型的条件块。

#### Scenario: Banner 弹窗横切质量

- **WHEN** 开发者实现或回归 Banner 弹窗
- **THEN** TSX MUST NOT 同时挂载通用 `modal-card` 与 `banner-modal-card`
- **AND** 1440px 视口下 Computed width MUST 符合 Banner/SKU 大弹窗基准
- **AND** 矮视口下 body 必须可滚动，footer 主操作按钮始终可达。

#### Scenario: Banner 图片上传回归

- **WHEN** 用户在 Banner 弹窗选择图片
- **THEN** 上传控件 MUST 呈现 `idle -> uploading -> done/failed` 状态机
- **AND** 成功后 MUST 在同一会话即时回显缩略图或文件卡片
- **AND** 失败信息 MUST 显示在上传控件附近
- **AND** Docker Web `:3000` 边界下小文件上传必须成功，超限文件必须返回业务错误而非 Nginx 413。
