## MODIFIED Requirements

### Requirement: 管理端瓷砖类目管理页

Web 客户端 MUST 提供瓷砖类目管理页，路由为 `/admin/tile-categories`，视觉 MUST 高保真对齐 **`REQ-0007-tile-category-management-refine`** 目录下 v2 context（相对 `REQ-0005-tile-category-management/prototype/web/tile-category-management.html` 的 CSS Port diff）与 `tile-category-management-add.html` 弹窗策略。页面 MUST 复用 `AdminLayout`（264px Sidebar、右侧独立滚动、主内容宽度跟随全局 Admin Shell `content-inner` 策略，MUST NOT 重新锁定为 1080px）。`admin` 与 `employee` MUST 可访问；`store_owner` MUST NOT 访问。

#### Scenario: 类目页布局

- **WHEN** 已登录 `admin` 或 `employee` 访问 `/admin/tile-categories`
- **THEN** 页面 MUST 展示 page-header（eyebrow「CATEGORY MANAGEMENT」、标题「瓷砖类目管理」、说明、「＋ 新增类目」）
- **AND** MUST 展示 4 指标卡、类目检索区（**无**外层 section 标题）、左侧类目树（280px）与右侧类目列表（**无**外层「类目列表」section 标题）
- **AND** MUST NOT 展示导出按钮或批量操作入口
- **AND** 页面内容宽度 MUST 跟随全局 Admin Shell 策略，不得通过页面级 `.content-inner` max-width 退回 1080px。

#### Scenario: 类目树与列表联动

- **WHEN** 用户点击左侧类目树节点
- **THEN** 右侧列表 MUST 以所选节点为上下文刷新
- **AND** 当前选中节点 MUST 有清晰 active 状态。

### Requirement: 管理端瓷砖品牌管理页

Web 客户端 MUST 提供瓷砖品牌管理页，路由为 `/admin/brands`，视觉 MUST 高保真对齐 `issues/requirements/archive/REQ-0005-brand-management/prototype/web/brand-management.html` 与 `brand-management-modal.html` 的 CSS Port 策略。页面 MUST 复用 `AdminLayout`（264px Sidebar、右侧独立滚动、主内容宽度跟随全局 Admin Shell `content-inner` 策略，MUST NOT 重新锁定为 1080px）。`admin` 与 `employee` MUST 可访问；`store_owner` MUST NOT 访问。

#### Scenario: 品牌页布局

- **WHEN** 已登录 `admin` 或 `employee` 访问 `/admin/brands`
- **THEN** 页面 MUST 展示 page-header（eyebrow「MASTER DATA」、标题「瓷砖品牌」、说明、「＋ 新增品牌」）
- **AND** MUST 展示 4 指标卡、筛选区、品牌表格与分页
- **AND** MUST NOT 展示导出按钮、批量操作、「品牌列表」「品牌检索」标题行
- **AND** 页面内容宽度 MUST 跟随全局 Admin Shell 策略，不得通过页面级 `.content-inner` max-width 退回 1080px。

### Requirement: 管理端瓷砖 SKU 管理页

Web 客户端 MUST 提供瓷砖 SKU 管理页，路由为 `/admin/tile-skus`，视觉 MUST 高保真对齐 `issues/requirements/archive/REQ-0006-tile-sku-management/prototype/web/tile-sku-management-list.html` 与 `tile-sku-create-modal.html` 的 CSS Port 策略。页面 MUST 复用 `AdminLayout`（264px Sidebar、右侧独立滚动、主内容宽度跟随全局 Admin Shell `content-inner` 策略，MUST NOT 保留 1120px 页面级 `content-inner` override）。`admin` 与 `employee` MUST 可访问；`store_owner` MUST NOT 访问。

#### Scenario: SKU 页布局

- **WHEN** 已登录 `admin` 或 `employee` 访问 `/admin/tile-skus`
- **THEN** 页面 MUST 展示 page-head（eyebrow「OPERATIONS / SKU」、标题「瓷砖SKU」、说明、「＋ 新增SKU」）
- **AND** MUST 展示 4 指标卡（SKU总数/已上架/待完善/草稿）、五维筛选区、SKU 表格与分页
- **AND** 页面内容宽度 MUST 跟随全局 Admin Shell 策略，不得通过 `:has(.sku-page-hero) .content-inner` 或等价规则退回 1120px。

#### Scenario: 筛选与分页

- **WHEN** 用户输入关键词或选择筛选项并点击查询或回车
- **THEN** 系统 MUST 重置页码为 1 并重新加载列表
- **AND** 分页左侧 MUST 显示「共 {total} 条」
- **AND** 分页 MUST 支持页码与每页 10/20/50/100 条；默认 20；切换 page_size MUST 重置页码为 1。
