## ADDED Requirements

### Requirement: 管理端品牌证书通用组件

系统 MUST 在管理端沉淀品牌证书通用业务组件或等价展示方法，覆盖证书缩略图、证书摘要、有效期文本、有效状态 Badge、前台展示状态 Badge、预览入口和文件卡片。组件 MUST 面向展示模型和回调设计，MUST NOT 内置筛选、分页、权限判断、保存、删除、显示/隐藏接口调用、上传 API 调用或全局 toast。

#### Scenario: 展示证书缩略图与摘要

- **WHEN** 管理端页面或弹窗传入证书文件 URL、文件名、MIME Type、证书名称、证书编号和可选品牌名称
- **THEN** 图片证书 MUST 展示稳定尺寸缩略图
- **AND** PDF 证书 MUST 展示统一 `PDF` 文件占位
- **AND** 文件 URL 为空、文件类型未知或图片加载失败时 MUST 展示统一文件占位且不显示浏览器破图
- **AND** 证书名称 MUST 作为主文本展示
- **AND** 证书编号为空时 MUST 展示文件名作为辅助文本
- **AND** 可选品牌名称 MUST 仅作为附加文本展示，不得内置品牌筛选、导航或接口调用
- **AND** 长文本 MUST 使用现有管理端列表截断规则，不撑破表格或弹窗布局

#### Scenario: 展示有效期与状态 Badge

- **WHEN** 管理端页面或弹窗展示品牌证书有效期和有效状态
- **THEN** 有效期文本 MUST 覆盖长期有效、起止日期、仅到期日期和未设置
- **AND** 有效状态 Badge MUST 覆盖 `PERMANENT`、`VALID`、`EXPIRING_SOON`、`EXPIRED`、`UNSET`
- **AND** 有效状态 MUST 复用服务端返回字段，前端不得作为唯一事实源重新计算状态
- **AND** 未知有效状态 MUST 降级展示原始状态文本且不得导致页面渲染失败

#### Scenario: 展示前台展示状态

- **WHEN** 管理端页面或弹窗展示证书 `is_visible`
- **THEN** 展示状态 Badge MUST 展示前台展示或前台隐藏
- **AND** 展示状态 Badge MUST 与管理端既有启用/禁用视觉语义一致
- **AND** 组件 MUST NOT 内置显示或隐藏接口调用

#### Scenario: 触发证书预览

- **WHEN** 管理端用户点击缩略图、按钮、链接或等价预览入口
- **THEN** 组件 MUST 提供统一预览触发能力，并由调用方决定入口渲染形态
- **AND** 图片和 PDF v1 MUST 可通过新窗口打开受控文件 URL
- **AND** 文件 URL 缺失时 MUST 阻止预览并返回可由页面展示的失败原因
- **AND** 预览失败提示 SHOULD 复用 `文件暂时无法预览，请稍后重试或下载查看`
- **AND** 组件 MUST NOT 绕过后端鉴权或生成未授权对象存储直连地址

#### Scenario: 展示证书文件卡片状态

- **WHEN** 新增或编辑证书弹窗展示证书文件卡片
- **THEN** 文件卡片 MUST 支持 `idle`、`uploading`、`done`、`failed` 四类状态
- **AND** `idle` 状态 MUST 展示未上传提示
- **AND** `uploading` 状态 MUST 展示文件名、进度和保存阻塞提示能力
- **AND** `done` 状态 MUST 展示缩略图或文件类型、文件名、文件大小、重新上传和删除入口
- **AND** `failed` 状态 MUST 展示失败原因和重新上传入口
- **AND** 文件卡片 MUST 只负责展示和触发回调，不得直接调用上传 API

### Requirement: 管理端品牌证书页面组件化应用

系统 MUST 将品牌证书通用组件或等价展示方法应用到现有 `/admin/brand-certificates` 页面。组件化 MUST 保持页面筛选、分页、权限判断、保存、删除、显示/隐藏确认、固定 toast、指标卡 DOM 和弹窗宽度行为不回归。

#### Scenario: 列表列使用通用展示

- **WHEN** 管理端用户访问 `/admin/brand-certificates` 并查看证书列表
- **THEN** “证书”列 MUST 使用通用证书缩略图与证书摘要
- **AND** “有效期”列 MUST 使用通用有效期展示方法
- **AND** “有效状态”列 MUST 使用通用有效状态 Badge
- **AND** “前台展示”列 MUST 使用通用展示状态 Badge
- **AND** 操作列中的编辑、显示/隐藏、删除仍 MUST 由页面容器控制

#### Scenario: 弹窗文件展示区使用通用文件卡片

- **WHEN** 管理端用户打开新增或编辑品牌证书弹窗
- **THEN** 证书文件展示区 MUST 使用或对齐通用文件卡片
- **AND** 上传 API、进度计算、错误映射、保存阻塞和成功/失败 toast MUST 继续由页面容器负责
- **AND** 文件卡片在窄视口下 MUST 可换行，不遮挡上传、重新上传或删除入口

#### Scenario: 组件化不回归横切 UI 验收

- **WHEN** 在 1440x1024 视口验收组件化后的品牌证书页
- **THEN** 分页 DOM MUST 保持左侧 `page-summary`、右侧 `page-right` 页码和每页条数结构
- **AND** 指标卡 MUST 继续使用 `.metric-label`、`.metric-value`、`.metric-desc` 或等价 DS 结构
- **AND** 成功/失败反馈 MUST 使用 fixed toast 且不得通过文档流 notice 推挤页面布局
- **AND** 显示/隐藏、删除等状态或危险操作 MUST 使用 DS confirm modal，代码中不得出现 `window.confirm`
- **AND** 新增/编辑证书弹窗 TSX MUST NOT 同时挂载通用 `modal-card` 与证书专属 modal class
- **AND** 1440 视口下新增/编辑证书弹窗 Computed width MUST 与既有 REQ-0038 设计一致
- **AND** 矮视口下证书弹窗 body MUST 可滚动，头部和底部固定，无内容被遮挡或按钮不可达

#### Scenario: 组件化遵守 Design System 和契约边界

- **WHEN** 实现或验收品牌证书通用组件
- **THEN** 组件视觉 MUST 延续管理端“工业石材 · 暗色旗舰风”
- **AND** 新增样式 MUST 使用 Design System semantic token 或既有管理端 Badge、文本、边框语义
- **AND** 新增样式 MUST NOT 包含裸 Hex 或硬编码 token 对应 `rgba(...)`
- **AND** 缩略图、文件卡片、Badge 和操作入口在 1440px 管理端列表视口下 MUST 保持稳定尺寸
- **AND** 组件内部 MUST NOT 呈现解释组件如何使用的说明性文案，只呈现证书业务状态
- **AND** 组件导出路径 MUST 清晰，后续管理端页面不得从 `BrandCertificateManagementPage.tsx` 复制内部实现
