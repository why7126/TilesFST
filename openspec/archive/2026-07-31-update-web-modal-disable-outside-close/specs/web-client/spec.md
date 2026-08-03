## ADDED Requirements

### Requirement: Web 标准弹窗外部点击关闭策略

Web 客户端 MUST 在管理端和店主 Web 展示端标准 Dialog / Modal 中禁用点击遮罩或弹窗外空白区域自动关闭。标准 Dialog / Modal MUST 保留明确关闭入口，且禁用外部点击关闭不得改变业务保存、确认、上传、滚动、焦点和错误展示能力。本能力 MUST NOT 修改后端 API、数据库、OpenAPI、Orval、MinIO、Nginx、Docker Compose 或微信小程序能力。

#### Scenario: 管理端标准弹窗外部点击不关闭

- **WHEN** 已登录 `admin` 或 `employee` 打开管理端新增、编辑、详情、确认、上传或设置确认类标准 Dialog / Modal
- **THEN** 用户点击遮罩或弹窗外空白区域时弹窗 MUST 保持打开
- **AND** 弹窗内已输入字段、已选择项、上传状态和滚动位置 MUST 保持不变
- **AND** 弹窗 MUST 继续提供关闭图标、取消按钮、返回按钮或业务完成关闭等明确关闭入口

#### Scenario: 展示端标准弹窗外部点击不关闭

- **WHEN** 店主 Web 展示端用户打开商品详情、品牌详情、图片预览、联系或咨询类标准 Dialog / Modal
- **THEN** 用户点击遮罩或弹窗外空白区域时弹窗 MUST 保持打开
- **AND** 弹窗内滚动、图片切换、链接点击和键盘焦点 MUST 保持可用
- **AND** 弹窗 MUST 提供可见关闭图标或等价明确关闭入口

#### Scenario: 确认弹窗必须显式选择

- **WHEN** 用户打开删除、启停、上下架、批量操作或系统设置类确认 Dialog / Modal
- **THEN** 点击遮罩或弹窗外空白区域 MUST NOT 关闭弹窗
- **AND** 用户 MUST 通过取消按钮、关闭图标、Esc 键或确认按钮结束本次确认流程
- **AND** 取消或关闭 MUST NOT 调用目标业务 API
- **AND** 确认 MUST 沿用既有 API 调用、成功反馈和失败处理

#### Scenario: 上传弹窗状态不因外部点击丢失

- **WHEN** 用户在品牌 Logo、Banner 图片、SKU 图片/视频、证书图片、用户头像或等价上传控件所在弹窗中选择文件
- **THEN** 上传控件 MUST 保持 `idle -> uploading -> done/failed` 或等价状态机
- **AND** 点击遮罩或弹窗外空白区域 MUST NOT 关闭弹窗或重置上传状态
- **AND** 上传成功后 MUST 同会话即时回显缩略图、文件卡片或已上传状态
- **AND** 上传失败信息 MUST 展示在上传控件附近、既有错误区域或 fixed toast 中

#### Scenario: 轻量浮层不默认纳入

- **WHEN** 页面包含 Popover、Dropdown、Tooltip、Select 下拉层、日期选择器或等价轻量浮层
- **THEN** 本弹窗策略 MUST NOT 默认改变这些轻量浮层的外部点击关闭行为
- **AND** 若后续需求决定纳入轻量浮层，MUST 通过独立 REQ 或本 Change 的显式例外清单定义组件范围和验收方式

#### Scenario: 前端测试覆盖关闭策略

- **WHEN** 实现或回归本 Change
- **THEN** 前端测试 MUST 至少覆盖一个表单弹窗和一个确认弹窗的外部点击不关闭行为
- **AND** 测试 MUST 覆盖明确关闭入口仍可关闭弹窗
- **AND** 如触及上传弹窗，测试或验收记录 MUST 覆盖外部点击不打断上传状态机

## MODIFIED Requirements

### Requirement: 品牌列表启停二次确认

Web 客户端 MUST 在 `/admin/brands` 品牌列表页为行内「启用」与「停用」操作提供二次确认，以降低误触风险。启停确认 MUST 复用与同页「删除品牌」确认框相同的 modal 结构（`modal-backdrop` + `modal-card` + head/body/footer）。用户点击「启用」或「停用」时 MUST NOT 直接调用 enable/disable API；MUST 先展示确认弹窗，仅在用户点击「确认启用」或「确认停用」后调用 API。删除操作 MUST 仍使用独立「删除品牌」确认弹窗，MUST NOT 与启停确认合并。本能力 MUST NOT 修改品牌 API、数据库、权限边界或 Orval 生成接口。

#### Scenario: 停用须先确认

- **WHEN** 用户在品牌列表行点击「停用」
- **THEN** MUST 展示停用确认弹窗，MUST NOT 直接调用 `POST /api/v1/admin/brands/{id}/disable`
- **AND** 弹窗标题 MUST 为「停用品牌」
- **AND** 正文 MUST 为「确认停用品牌「{name}」？停用后前台将不再展示该品牌。」（`{name}` 为该行品牌名称）

#### Scenario: 启用须先确认

- **WHEN** 用户在品牌列表行点击「启用」
- **THEN** MUST 展示启用确认弹窗，MUST NOT 直接调用 `POST /api/v1/admin/brands/{id}/enable`
- **AND** 弹窗标题 MUST 为「启用品牌」
- **AND** 正文 MUST 为「确认启用品牌「{name}」？」

#### Scenario: 确认弹窗按钮与取消

- **WHEN** 启停确认弹窗展示
- **THEN** 底部 MUST 含「取消」与「确认停用」或「确认启用」（主按钮）
- **WHEN** 用户点击「取消」、× 或 ESC
- **THEN** MUST 关闭弹窗且 MUST NOT 改变品牌状态或调用 API
- **WHEN** 用户点击遮罩或弹窗外空白区域
- **THEN** 弹窗 MUST 保持打开且 MUST NOT 改变品牌状态或调用 API

#### Scenario: 确认后调用 API 并刷新

- **WHEN** 用户在停用确认弹窗点击「确认停用」
- **THEN** MUST 调用 disable API 并展示 Toast「品牌已停用」，并刷新列表与指标卡 summary
- **WHEN** 用户在启用确认弹窗点击「确认启用」
- **THEN** MUST 调用 enable API 并展示 Toast「品牌已启用」，并刷新列表与指标卡 summary

#### Scenario: 删除确认独立

- **WHEN** 用户点击行内「删除」
- **THEN** MUST 仍使用独立「删除品牌」确认弹窗
- **AND** 启停确认 state MUST NOT 与删除确认 state 共用

#### Scenario: 无障碍与样式

- **WHEN** 启停确认弹窗展示
- **THEN** MUST 设置 `role="dialog"`、`aria-modal="true"`，标题 MUST 有 `aria-labelledby`
- **AND** TSX MUST NOT 包含裸 Hex；样式 MUST 复用既有 modal 与 brand-management CSS Port

#### Scenario: 品牌管理其他能力不回退

- **WHEN** 用户执行查询、重置、分页、新增、编辑、删除品牌或上传 Logo
- **THEN** 既有功能 MUST 保持可用
- **AND** `admin` 与 `employee` MUST 可维护品牌

### Requirement: SKU 弹窗内容溢出与滚动修复

Web 客户端 MUST 修复 `/admin/tile-skus` 新增/编辑 SKU 弹窗（`TileSkuFormModal`）的内容溢出缺陷：当表单内容高度超过视口允许的最大弹窗高度时，弹窗 MUST 保持页眉与页脚固定可见，且主体内容区 MUST 提供垂直滚动以访问全部字段与操作按钮。修复 MUST NOT 修改 SKU API、数据库结构、权限边界、Orval 生成接口或 MinIO 对象存储策略。

#### Scenario: 矮视口下弹窗主体可滚动

- **WHEN** 已登录 `admin` 或 `employee` 在视口高度 ≤900px 时打开「新增SKU」或「编辑SKU」弹窗
- **THEN** 弹窗 `.modal-body`（或等价内容 wrapper）MUST 支持垂直滚动
- **AND** 用户 MUST 能滚动至 SKU 图片、SKU 视频与备注说明字段

#### Scenario: 页眉页脚固定可见

- **WHEN** 弹窗内容超出可视高度且用户滚动主体区域
- **THEN** 标题、副标题与关闭按钮 MUST 保持可见
- **AND** 「取消 / 保存草稿 / 创建SKU（或保存）」footer MUST 保持可见且可点击

#### Scenario: 弹窗尺寸约束不变

- **WHEN** 用户打开 SKU 弹窗
- **THEN** 弹窗宽度 MUST 仍为 880px（`max-width: 100%` 响应式除外）
- **AND** 弹窗 `max-height` MUST NOT 超过视口（如 `calc(100vh - 64px)`）

#### Scenario: 关闭交互不回退

- **WHEN** 用户在弹窗内滚动
- **THEN** ESC、点击 × 或底部取消按钮 MUST 仍可正常关闭弹窗
- **AND** MUST NOT 因滚动导致意外关闭
- **WHEN** 用户点击遮罩或弹窗外空白区域
- **THEN** 弹窗 MUST 保持打开，且已填写字段、上传状态和滚动上下文 MUST 保持不变

#### Scenario: SKU 表单功能保持可用

- **WHEN** 用户在修复后的弹窗中填写并保存
- **THEN** 保存草稿、创建 SKU、编辑更新、图片/视频上传 MUST 继续可用
- **AND** MUST NOT 变更 API 请求参数或响应结构

### Requirement: Web 管理端表单弹窗与抽屉移动端基础可用

Web 管理端表单页、业务弹窗、确认弹窗与日志详情抽屉 MUST 在 `375px` 宽度及移动视口高度下保持可读、可滚动、可关闭和可提交。适用范围 MUST 包含品牌、Banner、类目、规格、SKU、用户、重置密码、修改密码、系统设置确认、日志详情抽屉以及已有上传控件所在弹窗或表单。

#### Scenario: 业务弹窗窄屏可操作

- **WHEN** 用户在 `375px` 宽度打开新增、编辑、状态确认、删除、重置密码、修改密码或系统设置确认弹窗
- **THEN** 弹窗 MUST 不超出视口宽度
- **AND** 头部标题、关闭按钮、内容区和底部操作区域 MUST 可访问
- **AND** 矮视口下弹窗 body MUST 可滚动，底部主操作按钮不得丢失
- **AND** 点击遮罩或弹窗外空白区域 MUST NOT 关闭弹窗

#### Scenario: 宽弹窗保留专属宽度策略

- **WHEN** 用户在移动视口打开 SKU、Banner 或等价大表单弹窗
- **THEN** 弹窗 MUST 保留专属 card class 或等价宽度策略，MUST NOT 同时挂载通用 `modal-card` 与专属类导致 CSS 层叠覆盖
- **AND** 实现验收 MUST 检查 computed width 与 max-width，而不只检查源 CSS
- **AND** 关闭按钮、取消按钮和主操作按钮 MUST 可点击

#### Scenario: 表单和设置页移动端可读

- **WHEN** 用户在移动视口访问 `/admin/profile` 或 `/admin/settings/:tab`
- **THEN** 主信息、账号安全、设置导航、配置字段、保存、重置和确认入口 MUST 单列或等价可读布局展示
- **AND** 全页主要保存 CTA MUST 仅保留一处
- **AND** dirty Tab 切换、恢复默认、修改密码取消等风险操作 MUST 使用 DS modal，MUST NOT 使用 `window.confirm` 或 `window.alert`

#### Scenario: 日志详情抽屉移动端可关闭可滚动

- **WHEN** 用户在手机宽度打开 `/admin/logs` 的日志详情抽屉
- **THEN** 抽屉 MUST 可关闭
- **AND** 详情内容 MUST 可滚动查看
- **AND** 抽屉宽度 MUST NOT 导致页面整体横向失控滚动

#### Scenario: 上传控件移动端状态不回归

- **WHEN** 用户在移动视口使用品牌 Logo、Banner 图片、SKU 图片/视频或用户头像等已有上传控件
- **THEN** 上传控件 MUST 保持 `idle -> uploading -> done/failed` 或等价状态机可见
- **AND** 同会话上传成功后 MUST 即时回显缩略图或文件卡片
- **AND** 上传失败信息 MUST 展示在控件附近、既有错误区域或 fixed toast 中，且不得遮挡底部操作按钮
- **AND** 本 Change MUST NOT 新增媒体 API、存储桶、上传大小限制、Nginx 或 Docker 配置
