## MODIFIED Requirements

### Requirement: 管理端瓷砖类目管理页

Web 客户端 MUST 提供瓷砖类目管理页，路由为 `/admin/tile-categories`，视觉 MUST 高保真对齐 **`REQ-0007-tile-category-management-refine`** 目录下 v2 context（相对 `REQ-0005-tile-category-management/prototype/web/tile-category-management.html` 的 CSS Port diff）与 `tile-category-management-add.html` 弹窗策略。页面 MUST 复用 `AdminLayout`（264px Sidebar、右侧独立滚动、主内容宽度跟随全局 Admin Shell `content-inner` 策略，MUST NOT 重新锁定为 1080px）。`admin` 与 `employee` MUST 可访问；`store_owner` MUST NOT 访问。新增类目表单 MUST 与小程序分类交互保持一致，最多只允许创建两级类目。左侧类目树节点右侧计数 MUST 显示下一层级类目数量，不得显示商品数量；“全部类目”入口右侧计数 MUST 显示顶层类目数量。

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

#### Scenario: 类目树节点显示直接子类目数量

- **GIVEN** 管理端类目树节点存在直接子类目数量字段
- **WHEN** Web 管理端渲染该节点右侧数字
- **THEN** 节点右侧数字 MUST 使用直接子类目数量
- **AND** MUST NOT 使用 `sku_count` 或其他商品数量字段

#### Scenario: 全部类目入口显示顶层类目数量

- **GIVEN** 管理端类目树存在“全部类目”入口
- **WHEN** Web 管理端渲染该入口右侧数字
- **THEN** 该数字 MUST 等于顶层类目数量
- **AND** MUST NOT 显示商品总数
- **AND** 该入口右侧数字 MUST 与一级类目节点右侧数字保持同列视觉对齐
- **AND** 该入口文字 MUST 与类目树标题文字保持左对齐
- **AND** 当该入口处于选中态时，选中边框 MUST 完整包住入口文字和右侧数字

#### Scenario: 叶子类目显示 0

- **GIVEN** 某类目没有直接子类目
- **WHEN** Web 管理端渲染该节点右侧数字
- **THEN** 节点右侧数字 MUST 显示 `0`
- **AND** 即使该类目有关联商品，也 MUST NOT 在该位置显示商品数量

#### Scenario: 新增类目最多两级

- **WHEN** 用户打开新增类目弹窗
- **THEN** 上级类目下拉框 MUST 仅允许选择“无上级”或一级类目
- **AND** 页面 MUST 展示“当前最多支持二级类目”或等价提示
- **AND** 页面 MUST NOT 允许选择二级类目作为上级。
