## ADDED Requirements

### Requirement: 管理端瓷砖规格管理页

Web 客户端 MUST 提供瓷砖规格管理页，路由为 `/admin/tile-specs`，视觉 MUST 高保真对齐 `issues/requirements/archive/REQ-0009-tile-spec-management/prototype/web/tile-size-management.html` 与 `tile-size-management-modal.html` 的 CSS Port 策略。页面 MUST 复用 `AdminLayout`（264px Sidebar、右侧独立滚动、主内容最大宽度 1080px）。`admin` 与 `employee` MUST 可访问；`store_owner` MUST NOT 访问。

#### Scenario: 规格页布局

- **WHEN** 已登录 `admin` 或 `employee` 访问 `/admin/tile-specs`
- **THEN** 页面 MUST 展示 page-header（eyebrow「MASTER DATA」、标题「瓷砖规格」、说明、「＋ 新增瓷砖规格」）
- **AND** MUST 展示 4 指标卡（规格总数/启用规格/停用规格/未关联 SKU）、关键词+状态筛选、规格表格与分页
- **AND** MUST NOT 展示导出、批量操作、列表 section 标题行

#### Scenario: 筛选与分页

- **WHEN** 用户输入关键词或选择状态并点击查询
- **THEN** 系统 MUST 重置页码为 1 并重新加载列表
- **AND** 分页左侧 MUST 显示「共 {total} 条」
- **AND** 分页 MUST 支持页码与每页 20/50/100 条

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
- **AND** 字段 MUST 为：宽*、长*、只读尺寸名称、厚度、排序*、备注
- **AND** MUST NOT 展示状态、规格类型、单位选择、可编辑尺寸名称
- **AND** 宽长变化 MUST 实时生成 `{w}×{l}mm`；重复时 MUST 展示错误并禁止提交

#### Scenario: 规格管理 CSS Port

- **WHEN** 开发者查看规格管理页源码
- **THEN** 视觉样式 MUST 主要来自 `features/admin/styles/tile-spec-management.css`（或等价 port CSS）
- **AND** 颜色 MUST 通过 semantic token 引用 `globals.css`
- **AND** TSX MUST NOT 包含裸 Hex

#### Scenario: 未登录访问

- **WHEN** 未登录用户访问 `/admin/tile-specs`
- **THEN** 前端 MUST 跳转至 `/admin/login`

## MODIFIED Requirements

### Requirement: 管理端瓷砖 SKU 管理页

Web 客户端 MUST 提供瓷砖 SKU 管理页，路由为 `/admin/tile-skus`，视觉 MUST 高保真对齐 `issues/requirements/archive/REQ-0006-tile-sku-management/prototype/web/tile-sku-management-list.html` 与 `tile-sku-create-modal.html` 的 CSS Port 策略。页面 MUST 复用 `AdminLayout`（264px Sidebar、右侧独立滚动、主内容最大宽度 1120px）。`admin` 与 `employee` MUST 可访问；`store_owner` MUST NOT 访问。

#### Scenario: SKU 页布局

- **WHEN** 已登录 `admin` 或 `employee` 访问 `/admin/tile-skus`
- **THEN** 页面 MUST 展示 page-head（eyebrow「OPERATIONS / SKU」、标题「瓷砖SKU」、说明、「＋ 新增SKU」）
- **AND** MUST 展示 4 指标卡（SKU总数/已上架/待完善/草稿）、五维筛选区、SKU 表格与分页

#### Scenario: 筛选与分页

- **WHEN** 用户输入关键词或选择筛选项并点击查询或回车
- **THEN** 系统 MUST 重置页码为 1 并重新加载列表
- **AND** 分页左侧 MUST 显示「共 {total} 条」
- **AND** 分页 MUST 支持页码与每页 10/20/50/100 条；默认 20；切换 page_size MUST 重置页码为 1

#### Scenario: 列表列与价格格式

- **WHEN** 用户查看 SKU 表格
- **THEN** 列 MUST 包含：SKU信息、品牌/类目、规格/工艺、参考价格、素材、状态、更新时间、操作
- **AND** 参考价格 MUST 格式化为 `¥ 268.00` 样式（两位小数）

#### Scenario: 列表行上下架操作

- **WHEN** 列表行 `status` 为 `PUBLISHED`
- **THEN** 操作列 MUST 展示「编辑」与「下架」
- **AND** 「删除」MUST 展示但置灰，并提示已上架不可删
- **WHEN** 列表行 `status` 为 `DISABLED`（已下架）
- **THEN** 操作列 MUST 展示「编辑」与「恢复」（或等价「上架」文案）
- **AND** 点击 MUST 调用 `POST /api/v1/admin/tile-skus/{id}/publish` 并刷新列表
- **WHEN** 列表行 `status` 为 `DRAFT` 或 `NEEDS_COMPLETION`
- **THEN** 操作列 MUST 展示「编辑」与「上架」
- **AND** publish 按钮 MUST NOT 因 `canDeleteTileSku` 或 delete 按钮状态而被隐藏

#### Scenario: 新增编辑弹窗

- **WHEN** 用户点击「新增SKU」或行内「编辑」
- **THEN** MUST 打开宽 880px 弹窗，遮罩半透明，头尾固定、主体可滚动
- **AND** 字段顺序 MUST 为：SKU名称、SKU编码、所属品牌、所属类目、规格尺寸、表面工艺、主色系、参考价格（元）、SKU图片、SKU视频、备注说明
- **AND** 「规格尺寸」MUST 为 `<select>`，选项来自 `status=ENABLED` 的规格列表，按 `sort_order` 排序；MUST NOT 为自由文本 `<input>`
- **AND** MUST NOT 展示状态字段
- **AND** 标题 MUST 含「创建后默认草稿」提示
- **AND** 底部 MUST 为：取消、保存草稿、创建SKU
- **WHEN** SKU 无 `spec_id`（迁移失败）
- **THEN** MUST 展示提示要求选择规格；保存/创建前 MUST 校验已选规格

#### Scenario: 多图主图与多视频

- **WHEN** 用户在弹窗管理素材
- **THEN** MUST 支持多张图片缩略图网格、主图标签与「设为主图」
- **AND** MUST 支持多个视频文件卡片（名称、大小、删除、继续添加）
- **AND** 视频 MUST NOT 为必填

#### Scenario: 保存草稿与创建 SKU

- **WHEN** 用户点击「保存草稿」
- **THEN** MUST 以宽松校验提交（至少 SKU 名称）
- **WHEN** 用户点击「创建SKU」
- **THEN** MUST 校验全部必填项（含规格下拉）；成功 Toast「SKU创建成功，已保存为草稿」

#### Scenario: SKU 管理 CSS Port

- **WHEN** 开发者查看 SKU 管理页源码
- **THEN** 视觉样式 MUST 主要来自 `features/admin/styles/tile-sku-management.css`（或等价 port CSS）
- **AND** 颜色 MUST 通过 `var(--color-*)` 引用 `globals.css`
- **AND** TSX MUST NOT 包含裸 Hex

#### Scenario: 未登录访问

- **WHEN** 未登录用户访问 `/admin/tile-skus`
- **THEN** 前端 MUST 跳转至 `/admin/login`
