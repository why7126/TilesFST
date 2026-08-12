## MODIFIED Requirements

### Requirement: 管理端 Banner 管理页

Web 客户端 MUST 提供 Banner 管理页，路由为 `/admin/banners`，视觉 MUST 高保真对齐 `issues/requirements/archive/REQ-0016-banner-management/prototype/web/banner-management-list.html` 与 `banner-management-list.png` 的 CSS Port 策略（**展示位置独立列**与第一列仅标题为 BUG-0039 策略 delta，MUST 以本 requirement 为准）。页面 MUST 复用 `AdminLayout`（264px Sidebar、右侧独立滚动、主内容最大宽度 1080px）。`admin` 与 `employee` MUST 可访问；`store_owner` MUST NOT 访问。列表表格 MUST NOT 展示与 page-hero 重复的「Banner 列表」section 标题或「当前显示 X-Y / N」toolbar 统计行。列表底部分页 MUST 复用与用户管理页一致的标准 DOM 与样式（`pagination` + `page-summary` + `page-right` + `page-buttons` + `page-size-wrap`），MUST NOT 使用 `banner-pagination` / `table-toolbar` 范围行结构。展示端筛选、表格和弹窗文案 MUST 仅表达“小程序”；展示位置 MUST 仅表达“首页轮播”和“品牌列表页轮播”。Banner 列表 MUST 以缩略图、展示位置、跳转类型、跳转目标、排序或更新时间提供记录识别上下文；如继续展示 `title`，该文案 MUST 降级为内部识别信息，MUST NOT 表达为运营必须维护的前台标题。

#### Scenario: Banner 列表页布局

- **WHEN** 已登录 `admin` 或 `employee` 访问 `/admin/banners`
- **THEN** 页面 MUST 展示 page-hero（眉标 `OPERATIONS / BANNER MANAGEMENT`、标题「Banner 管理」、说明、「＋ 新增 Banner」）
- **AND** MUST 展示 4 指标卡（Banner 总数/当前筛选/已上线/待生效）
- **AND** MUST 展示关键词、展示端、展示位置、状态、时间状态筛选与 Banner 表格、分页
- **AND** 展示端控件 MUST 仅表达“小程序”
- **AND** 展示位置控件 MUST 仅提供“首页轮播”和“品牌列表页轮播”
- **AND** 表格 MUST 含 Banner 缩略图（86×38）与识别上下文、**展示位置**、展示端、跳转类型、状态、有效期、排序、更新时间、操作
- **AND** 第一列 MUST NOT 只依赖人工标题识别 Banner
- **AND** 关键词搜索 placeholder SHOULD 不再强调“标题”
- **AND** MUST NOT 展示「Banner 列表」section 标题或「当前显示 … / …」toolbar 行。

### Requirement: Banner 新增编辑弹窗

Web 客户端 MUST 提供 `BannerFormModal`，宽 **880px**（与瓷砖 SKU 弹窗 `.sku-modal-card` 一致，`max-width: 100%` 响应式保留）、最大高度 92vh、内容区可滚动（头尾固定）。弹窗 MUST 按 `jump_type` 展示条件字段：`SKU_DETAIL`（关联 SKU + 图库选图）、`BRAND_DETAIL`（关联品牌 + 品牌 Logo 取图）、`EXTERNAL_LINK`（HTTPS 外链）、`TOPIC_PAGE`（关联专题）、`NO_JUMP`（无跳转目标）。弹窗 MUST NOT 展示状态编辑或状态策略说明块。弹窗 MUST NOT 展示“Banner 标题”输入框、标题必填提示或标题重复提示；保存时若 API 仍要求 `title`，Web 客户端 MUST 自动生成或保留内部标题并提交，且该内部标题 MUST NOT 作为小程序前台主标题。Banner 图片模块 MUST NOT 展示冗余来源首行标题（如「自定义上传 / SKU 主图」）；自定义上传按钮 MUST 使用「选择/更换/上传中」文案并对齐 `BrandFormModal` 的 `hidden` file input 模式。展示端 MUST 默认为“小程序”且不得保存为其他端；展示位置 MUST 仅允许“首页轮播”和“品牌列表页轮播”。关联 SKU、关联品牌与关联专题 MUST 为单一可搜索选择控件（Combobox），MUST NOT 分离为独立搜索框与下拉框。运营备注 `textarea` MUST 占满整行且 placeholder 字号与同弹窗 input 一致。有效期 MUST 为单字段区间「{开始} 至 {结束}」，格式 `YYYY-MM-DD HH:mm`（分钟精度），MUST NOT 使用原生 `<input type="datetime-local">` 作为最终方案。视觉 MUST 对齐管理端大表单弹窗基准（宽度与 SKU 弹窗一致）。

#### Scenario: Banner 弹窗公共字段

- **WHEN** 用户打开新增或编辑 Banner 弹窗
- **THEN** MUST 展示展示端、展示位置、Banner 图片、跳转类型、排序、有效期、运营备注
- **AND** MUST NOT 展示“Banner 标题”输入框
- **AND** MUST NOT 展示“Banner 标题不能为空”或“同一展示端 + 展示位置下标题不可重复”等运营可见提示
- **AND** 展示端 MUST 为“小程序”且不可改为其他端
- **AND** 展示位置 MUST 仅提供“首页轮播”和“品牌列表页轮播”
- **AND** 新增 Banner 默认展示位置 SHOULD 为“首页轮播”
- **AND** 主按钮 MUST 为「保存 Banner」品牌金样式。

#### Scenario: 隐藏标题后保存

- **GIVEN** 用户已完成 Banner 图片、展示位置、跳转类型、排序和有效期等字段
- **WHEN** 用户点击「保存 Banner」
- **THEN** Web 客户端 MUST 不因标题为空阻断保存
- **AND** 如请求体仍需要 `title`，Web 客户端 MUST 自动提交内部标题
- **AND** 保存失败时 MUST NOT 要求运营填写隐藏标题字段。
