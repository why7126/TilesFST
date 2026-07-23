## MODIFIED Requirements

### Requirement: 管理端瓷砖类目管理页

Web 客户端 MUST 提供瓷砖类目管理页，路由为 `/admin/tile-categories`，视觉 MUST 高保真对齐 **`REQ-0007-tile-category-management-refine`** 目录下 v2 context（相对 `REQ-0005-tile-category-management/prototype/web/tile-category-management.html` 的 CSS Port diff）与 `REQ-0067` 类目新增 / 编辑弹窗字段策略。页面 MUST 复用 `AdminLayout`（264px Sidebar、右侧独立滚动、主内容宽度跟随全局 Admin Shell `content-inner` 策略，MUST NOT 重新锁定为 1080px）。`admin` 与 `employee` MUST 可访问；`store_owner` MUST NOT 访问。

#### Scenario: 类目页布局

- **WHEN** 用户访问 `/admin/tile-categories`
- **THEN** 页面 MUST 展示 page-header（eyebrow「CATEGORY MANAGEMENT」、标题「瓷砖类目管理」、说明、「＋ 新增类目」）
- **AND** MUST 展示 4 指标卡、类目检索区（**无**外层 section 标题）、左侧类目树（280px）与右侧类目列表（**无**外层「类目列表」section 标题）

#### Scenario: 类目树与列表联动

- **WHEN** 用户点击左侧类目树节点
- **THEN** 右侧类目列表 MUST 按节点及其子孙范围刷新

#### Scenario: 类目列表名称列第二行仅展示编码

- **WHEN** 管理端类目列表展示类目名称列
- **THEN** 名称列第一行 MUST 展示类目名称
- **AND** 名称列第二行 MUST 仅展示系统类目编码
- **AND** 名称列第二行 MUST NOT 展示层级路径，例如 `父级类目 / 二级类目`

#### Scenario: 新增类目弹窗字段

- **WHEN** 用户点击「新增类目」
- **THEN** 系统 MUST 打开新增类目弹窗
- **AND** 弹窗 MUST 展示带必填标识的「上级类目」「类目名称」「排序权重」
- **AND** 弹窗 MUST NOT 展示可填写的「类目编码」输入项
- **AND** 弹窗 MUST 提示类目编码由系统自动生成或等价弱提示

#### Scenario: 编辑类目弹窗字段

- **WHEN** 用户点击类目行「编辑」
- **THEN** 系统 MUST 打开编辑类目弹窗
- **AND** 弹窗 MUST NOT 提供可编辑的「类目编码」输入项
- **AND** 本期 MUST NOT 允许通过编辑弹窗修改上级类目

#### Scenario: 上级类目选择

- **WHEN** 用户在新增类目弹窗选择上级类目
- **THEN** 下拉项 MUST 包含「无上级，创建一级类目」或等价顶级选项
- **AND** 下拉项 MUST 仅包含可作为上级的一级类目
- **AND** 二级类目 MUST NOT 出现在上级类目可选项中

#### Scenario: 类目名称本地校验

- **WHEN** 用户提交空名称、超过 10 个用户可见字符的名称，或包含中文/英文/数字之外字符的名称
- **THEN** 前端 MUST 阻止保存
- **AND** 错误提示 MUST 展示在类目名称字段或字段组下方

#### Scenario: 排序权重本地校验

- **WHEN** 用户提交空值、0、负数、小数或非数字排序权重
- **THEN** 前端 MUST 阻止保存
- **AND** 错误提示 MUST 展示在排序权重字段或字段组下方

#### Scenario: 创建请求不包含编码

- **WHEN** 用户提交新增类目弹窗
- **THEN** 前端调用创建 API 的 payload MUST NOT 包含用户填写的 `code`
- **AND** 前端 MUST 使用 Orval 生成类型或等价生成客户端契约

#### Scenario: 服务端错误展示

- **WHEN** 创建或更新 API 返回统一错误 envelope
- **THEN** 前端 MUST 优先展示 `message`
- **AND** 字段级错误 SHOULD 映射到对应字段
- **AND** 无法映射字段的错误 MUST 展示在弹窗固定错误区域或等价表单错误区

#### Scenario: 保存成功刷新

- **WHEN** 类目创建或更新成功
- **THEN** 弹窗 MUST 关闭
- **AND** 类目树、类目列表和页面统计 MUST 刷新

#### Scenario: 类目弹窗横切质量

- **WHEN** 开发者实现或回归类目新增 / 编辑弹窗
- **THEN** TSX MUST NOT 同时挂载通用 `modal-card` 与专属类
- **AND** 1440px 视口下 computed width MUST 为 560px 或 design/tasks 中批准的宽度
- **AND** 矮视口下弹窗 body MUST 可滚动且 footer 操作按钮始终可达
- **AND** 实现 MUST 使用 Design System semantic token 或既有管理端样式，MUST NOT 新增裸 Hex
