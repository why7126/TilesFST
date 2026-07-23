## ADDED Requirements

### Requirement: Web 管理端移动端基础适配矩阵

Web 客户端 MUST 为当前已实现的 Web 管理端 `/admin/*` 页面提供移动端基础可用验收矩阵。适用页面 MUST 包含 `/admin/login`、`/admin/dashboard`、`/admin/brands`、`/admin/banners`、`/admin/tile-categories`、`/admin/tile-specs`、`/admin/tile-skus`、`/admin/profile`、`/admin/users`、`/admin/logs`、`/admin/api-docs`、`/admin/settings/:tab` 与 `/admin/forbidden`。本能力 MUST 仅作用于 Web 管理端，MUST NOT 修改店主 Web 展示端、微信小程序、后端 API、数据库、OpenAPI、Orval、Docker Compose、Nginx、MinIO 或媒体上传后端链路。

#### Scenario: 移动端验收视口覆盖

- **WHEN** 实现或验收本 Change
- **THEN** MUST 覆盖 `375x812`、`390x844`、`768x1024` 与 `1440x1024` 视口
- **AND** `1440x1024` MUST 作为桌面回归视口
- **AND** 验收记录 MUST 标明每个视口是否存在页面级横向溢出、控件重叠、弹窗不可关闭、底部按钮不可达、筛选或分页不可操作。

#### Scenario: 非目标端和后端契约不受影响

- **WHEN** 本 Change 实现完成
- **THEN** 店主 Web 展示端与微信小程序页面 MUST 不受影响
- **AND** 后端 API 请求、响应、错误码、OpenAPI、Orval、SQLite/MySQL schema、Pydantic Schema、Docker Compose、MinIO 与媒体上传后端链路 MUST 保持不变
- **AND** 若实现阶段发现必须触及上述范围，MUST 回到需求评审或拆分独立 REQ/Change。

#### Scenario: 登录和无权限页移动端回归

- **WHEN** 用户在 `375x812` 或 `390x844` 访问 `/admin/login`
- **THEN** 登录页 MUST 保持 `<1024px` 单栏契约，左侧品牌区隐藏，登录表单居中且最大宽度不超过既有约束
- **AND** 账号、密码、记住登录状态、登录按钮和语言占位 MUST 可见且可操作
- **WHEN** 用户在移动视口访问 `/admin/forbidden`
- **THEN** 无权限页文案和返回或跳转入口 MUST 可读、可点击且不溢出。

### Requirement: Web 管理端列表与分页移动端基础可用

Web 管理端列表型页面 MUST 在手机和小屏平板视口下保持筛选区、指标卡、表格、分页和行内操作基础可用。适用页面 MUST 包含 `/admin/brands`、`/admin/banners`、`/admin/tile-categories`、`/admin/tile-specs`、`/admin/tile-skus`、`/admin/users`、`/admin/logs` 与 `/admin/api-docs`。列表页 MUST 保留既有管理端列表横切一致性契约，包括模块顺序、指标卡 DOM、固定 toast、DS confirm modal、固定操作列与统一分页 DOM。

#### Scenario: 筛选区移动端降级

- **WHEN** 用户在 `≤1023px` 视口访问任一适用列表页
- **THEN** 筛选区 MUST 降为 2 列、1 列或等价适配布局
- **AND** 在 `≤639px` 视口下筛选输入框、选择框、重置按钮和其他筛选控件 MUST 不重叠、不超出父容器且可键盘聚焦
- **AND** 筛选控件变化或重置后 MUST 保持既有业务筛选行为和权限边界。

#### Scenario: 表格滚动限制在容器内

- **WHEN** 任一适用列表页的表格内容宽于移动视口
- **THEN** 横向滚动 MUST 限制在 `table-card` 或等价表格容器内
- **AND** 页面 body、Shell、`.main-content` 与 `.content-inner` MUST NOT 出现不可控横向滚动
- **AND** 关键标识列、状态列和操作列 MUST 可访问；隐藏次要列时 MUST NOT 隐藏核心操作。

#### Scenario: 分页移动端可操作

- **WHEN** 任一适用列表页在 `375px` 宽度展示分页
- **THEN** 分页 MUST 使用左侧 `page-summary` 与右侧 `page-right` 的统一结构
- **AND** `.page-buttons`、上一页、下一页、每页条数和总数摘要 MUST 可换行或分组展示
- **AND** 页码和每页条数控件 MUST 不互相覆盖，且可点击页码数量仍 MUST 不超过 5 个。

#### Scenario: 列表横切 AC 保持

- **WHEN** 本 Change 触及任一适用列表页
- **THEN** 指标卡 MUST 保留 `.metric-label`、`.metric-value`、`.metric-desc` 或等价共享结构
- **AND** 操作成功或失败反馈 MUST 使用 fixed toast 或等价固定反馈区域，不得用文档流 notice 推挤 hero、筛选区或表格
- **AND** 启停、上下架、冻结、删除、重置密码等风险操作 MUST 使用 DS confirm modal，MUST NOT 使用 `window.confirm`。

### Requirement: Web 管理端表单弹窗与抽屉移动端基础可用

Web 管理端表单页、业务弹窗、确认弹窗与日志详情抽屉 MUST 在 `375px` 宽度及移动视口高度下保持可读、可滚动、可关闭和可提交。适用范围 MUST 包含品牌、Banner、类目、规格、SKU、用户、重置密码、修改密码、系统设置确认、日志详情抽屉以及已有上传控件所在弹窗或表单。

#### Scenario: 业务弹窗窄屏可操作

- **WHEN** 用户在 `375px` 宽度打开新增、编辑、状态确认、删除、重置密码、修改密码或系统设置确认弹窗
- **THEN** 弹窗 MUST 不超出视口宽度
- **AND** 头部标题、关闭按钮、内容区和底部操作区域 MUST 可访问
- **AND** 矮视口下弹窗 body MUST 可滚动，底部主操作按钮不得丢失。

#### Scenario: 宽弹窗保留专属宽度策略

- **WHEN** 用户在移动视口打开 SKU、Banner 或等价大表单弹窗
- **THEN** 弹窗 MUST 保留专属 card class 或等价宽度策略，MUST NOT 同时挂载通用 `modal-card` 与专属类导致 CSS 层叠覆盖
- **AND** 实现验收 MUST 检查 computed width 与 max-width，而不只检查源 CSS
- **AND** 关闭按钮、取消按钮和主操作按钮 MUST 可点击。

#### Scenario: 表单和设置页移动端可读

- **WHEN** 用户在移动视口访问 `/admin/profile` 或 `/admin/settings/:tab`
- **THEN** 主信息、账号安全、设置导航、配置字段、保存、重置和确认入口 MUST 单列或等价可读布局展示
- **AND** 全页主要保存 CTA MUST 仅保留一处
- **AND** dirty Tab 切换、恢复默认、修改密码取消等风险操作 MUST 使用 DS modal，MUST NOT 使用 `window.confirm` 或 `window.alert`。

#### Scenario: 日志详情抽屉移动端可关闭可滚动

- **WHEN** 用户在手机宽度打开 `/admin/logs` 的日志详情抽屉
- **THEN** 抽屉 MUST 可关闭
- **AND** 详情内容 MUST 可滚动查看
- **AND** 抽屉宽度 MUST NOT 导致页面整体横向失控滚动。

#### Scenario: 上传控件移动端状态不回归

- **WHEN** 用户在移动视口使用品牌 Logo、Banner 图片、SKU 图片/视频或用户头像等已有上传控件
- **THEN** 上传控件 MUST 保持 `idle -> uploading -> done/failed` 或等价状态机可见
- **AND** 同会话上传成功后 MUST 即时回显缩略图或文件卡片
- **AND** 上传失败信息 MUST 展示在控件附近、既有错误区域或 fixed toast 中，且不得遮挡底部操作按钮
- **AND** 本 Change MUST NOT 新增媒体 API、存储桶、上传大小限制、Nginx 或 Docker 配置。

### Requirement: Web 管理端移动端 smoke 验收

Web 管理端移动端适配实现 MUST 补充 Playwright 或等价浏览器 smoke 验收。smoke MUST 以固定视口和必测页面矩阵验证基础可用性，并在 Change trace 或等价验收记录中说明结果、N/A 理由和剩余风险。

#### Scenario: 必测页面 smoke 覆盖

- **WHEN** 实现阶段运行移动端 smoke 验收
- **THEN** 必测路由 MUST 至少包含 `/admin/login`、`/admin/dashboard`、`/admin/tile-skus`、`/admin/brands`、`/admin/users`、`/admin/logs` 与 `/admin/settings/basic`
- **AND** smoke MUST 覆盖 `375x812`、`390x844`、`768x1024` 与 `1440x1024`
- **AND** 每个必测路由 MUST 记录页面级横向溢出、控件重叠、弹窗不可关闭、底部按钮不可达、筛选或分页不可操作检查结果。

#### Scenario: 测试命令和截图证据

- **WHEN** 本 Change apply 完成
- **THEN** `pnpm --dir src/web test` 或项目等价前端测试 MUST 通过；若只执行子集，MUST 在 trace 中记录原因和剩余风险
- **AND** SHOULD 补充移动端 Playwright screenshot、trace 或等价截图，覆盖至少一个宽表格页面、一个业务弹窗、一个 Shell/Dashboard 页面和一个设置或表单页面
- **AND** 本 Change 不要求 Orval；若实现阶段改 API，MUST 重新运行 OpenAPI/Orval 门禁。
