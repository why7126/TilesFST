## ADDED Requirements

### Requirement: 管理端瓷砖品牌管理页

Web 客户端 MUST 提供瓷砖品牌管理页，路由为 `/admin/brands`，视觉 MUST 高保真对齐 `issues/requirements/REQ-0005-brand-management/prototype/web/brand-management.html` 与 `brand-management-modal.html` 的 CSS Port 策略。页面 MUST 复用 `AdminLayout`（264px Sidebar、右侧独立滚动、主内容最大宽度 1080px）。`admin` 与 `employee` MUST 可访问；`store_owner` MUST NOT 访问。

#### Scenario: 品牌页布局

- **WHEN** 已登录 `admin` 或 `employee` 访问 `/admin/brands`
- **THEN** 页面 MUST 展示 page-header（eyebrow「MASTER DATA」、标题「瓷砖品牌」、说明、「＋ 新增品牌」）
- **AND** MUST 展示 4 指标卡、筛选区、品牌表格与分页
- **AND** MUST NOT 展示导出按钮、批量操作、「品牌列表」「品牌检索」标题行

#### Scenario: 筛选与分页

- **WHEN** 用户输入关键词或选择状态并点击查询
- **THEN** 系统 MUST 重置页码为 1 并重新加载列表
- **AND** 分页 MUST 支持跳页与每页显示数 20/50/100；切换 page_size MUST 重置页码为 1 并保留筛选条件

#### Scenario: 删除按钮规则

- **WHEN** 列表行 `sku_count` 为 0 且状态为停用
- **THEN** 「删除」MUST 可点击（风险色）
- **WHEN** 其他情况
- **THEN** 「删除」MUST 置灰且 hover 提示「仅允许删除未关联SKU且已停用的品牌」

#### Scenario: 新增编辑弹窗

- **WHEN** 用户点击「新增品牌」或行内「编辑」
- **THEN** MUST 打开宽 720px 弹窗，`max-height: calc(100vh - 96px)`，头尾固定、主体可滚动
- **AND** 字段顺序 MUST 为：名称+排序、简称+英文名、Logo、介绍（Logo 与介绍通栏同宽）
- **AND** MUST NOT 展示状态字段、创建默认状态提示、字段规则说明区块、国家/地区
- **AND** 品牌名称与排序 MUST 必填；排序 MUST 仅允许正整数

#### Scenario: 品牌管理 CSS Port

- **WHEN** 开发者查看品牌管理页源码
- **THEN** 视觉样式 MUST 主要来自 `features/admin/styles/brand-management.css`（或等价 port CSS）
- **AND** 颜色 MUST 通过 `var(--color-*)` 引用 `globals.css`
- **AND** TSX MUST NOT 包含裸 Hex

#### Scenario: 未登录访问

- **WHEN** 未登录用户访问 `/admin/brands`
- **THEN** 前端 MUST 跳转至 `/admin/login`
