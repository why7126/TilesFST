## MODIFIED Requirements

### Requirement: 品牌证书文件上传与预览
系统 MUST 支持品牌证书文件经后端鉴权上传至 MinIO/S3 兼容对象存储单桶。证书文件 MUST 支持 JPG、PNG、WebP 和 PDF；证书多图图片 MUST 支持 JPG、PNG 和 WebP。图片类证书上传 MUST 生成真实轻量缩略图或记录明确跳过原因；PDF 证书 MUST 继续使用文件类型占位或既有 PDF 占位策略，PDF 首页渲染缩略图不属于本能力范围。证书文件大小上限 MUST 使用文档 / 文件类 effective 上传限制，并 MUST 与管理端系统设置、前端提示、后端校验和部署代理配置一致；MUST NOT 仅使用不可配置的 20MB 硬编码作为大小限制事实源。上传链路 MUST 校验 MIME、大小和对象 Key，MUST 返回可受控读取的 `file_url`、`file_key`、文件名、MIME、大小和可用缩略图引用。前端 MUST NOT 直连未授权对象存储。

#### Scenario: 上传合法证书文件
- **WHEN** 已授权管理端用户上传合法 JPG、PNG、WebP 或 PDF 证书文件，且文件大小在文档 / 文件类 effective 上限内
- **THEN** 系统 MUST 将对象写入对象存储单桶
- **AND** MUST 返回 `file_key` 和可读取的 `file_url`
- **AND** 对象 Key MUST NOT 使用用户原始文件名。

#### Scenario: 图片证书真实缩略图生成
- **GIVEN** 已授权管理端用户上传合法 JPG、PNG 或 WebP 证书图片
- **WHEN** 后端完成原图对象写入
- **THEN** 系统 MUST 生成与原图可追溯的真实缩略图或记录明确跳过原因
- **AND** 对大于目标尺寸的图片，缩略图像素尺寸或文件体积 MUST 明显低于原图
- **AND** 缩略图 MUST NOT 是原图 bytes 复制品
- **AND** 缩略图生成失败 MUST NOT 阻断原图上传和证书保存。

#### Scenario: 上传约 23MB PDF 证书文件
- **GIVEN** effective 文档 / 文件上传上限大于等于 23MB
- **WHEN** 已授权管理端用户上传约 23MB 合法 PDF 证书文件
- **THEN** 上传 MUST 成功
- **AND** MUST NOT 被硬编码 20MB 限制拒绝。

#### Scenario: 上传文件类型非法
- **WHEN** 用户上传非 JPG、PNG、WebP 或 PDF 文件
- **THEN** 系统 MUST 返回 HTTP 400
- **AND** 错误码 MUST 为 `CERTIFICATE_FILE_TYPE_INVALID` 或统一文件类型错误码。

#### Scenario: 上传文件过大
- **WHEN** 用户上传超过文档 / 文件类 effective 上限的证书文件
- **THEN** 系统 MUST 返回 HTTP 400
- **AND** 错误码 MUST 为 `CERTIFICATE_FILE_TOO_LARGE` 或统一文件大小错误码
- **AND** 错误提示 MUST 包含当前有效大小限制或等价可诊断信息
- **AND** Web Docker 入口 MUST NOT 以 Nginx 413 作为业务校验结果。

#### Scenario: 预览证书文件
- **WHEN** 管理员点击图片证书或 PDF 证书的预览入口
- **THEN** 图片证书 MUST 支持大图预览并使用原图或原始受控 URL
- **AND** PDF 证书 MUST 支持新窗口或等价受控 URL 预览
- **AND** 预览失败时 MUST 展示稳定错误提示。

#### Scenario: 上传证书多图图片
- **WHEN** 已授权管理端用户上传合法 JPG、PNG 或 WebP 证书图片
- **THEN** 系统 MUST 返回可用于证书图片数组保存的文件引用、受控读取 URL、缩略图引用、文件名、MIME 和大小
- **AND** 上传控件 MUST 在同一会话中即时回显图片卡片
- **AND** 上传失败原因 MUST 展示在上传控件或对应图片卡片内。

#### Scenario: 预览证书主图和图片列表
- **WHEN** 管理员点击证书主图或默认预览入口
- **THEN** 系统 MUST 从主图开始预览图片证书
- **AND** 主图加载失败时 MUST 展示稳定占位和可恢复提示
- **AND** 预览和展示 MUST 使用后端控制的可读 URL 或签名 URL。

### Requirement: 管理端品牌证书列表与筛选 API
系统 MUST 提供管理端品牌证书列表 API，允许已授权管理端用户按关键词、所属品牌、证书类型、有效状态、展示状态、页码和每页条数查询证书。响应 MUST 包含分页列表、分页信息和指标汇总，并 MUST 返回服务端计算的有效状态。列表项 MUST 返回证书主图信息、主图缩略图读取引用或等价主图受控读取引用；当证书无主图图片时，MUST 返回既有证书文件可预览 URL 或等价受控读取引用作为兼容 fallback。图片类证书列表小图 SHOULD 优先使用真实缩略图，原图预览 SHALL 使用原图或原文件。

#### Scenario: 查询证书列表
- **WHEN** 已授权管理端用户请求 `GET /api/v1/admin/brand-certificates`
- **THEN** 系统 MUST 返回 HTTP 200
- **AND** 响应 MUST 包含 `items`、`pagination` 和 `summary`
- **AND** 列表项 MUST 包含证书文件可预览 URL 或等价受控读取引用
- **AND** 列表项 MUST 优先包含主图缩略图信息、缩略图 URL 或主图受控读取引用。

#### Scenario: 证书列表缩略图回退
- **GIVEN** 列表项图片类证书存在原图但缩略图不存在、损坏或不可读
- **WHEN** 管理端或后端生成列表展示模型
- **THEN** 系统 MUST 回退原图或统一占位
- **AND** 页面 MUST NOT 展示浏览器破图或导致卡片高度跳动
- **AND** 系统 SHOULD 记录可定位的脱敏失败原因。

#### Scenario: 筛选条件生效
- **WHEN** 请求携带 `keyword`、`brand_id`、`type`、`validity_status` 或 `display_status`
- **THEN** 系统 MUST 按条件过滤品牌证书
- **AND** `keyword` MUST 支持证书名称、证书编号和发证机构模糊搜索。

#### Scenario: 非管理端用户被拒绝
- **WHEN** 未认证用户或无管理端权限用户请求品牌证书列表 API
- **THEN** 系统 MUST 返回 HTTP 401 或 403。

### Requirement: 品牌证书横切 UI 验收
品牌证书管理页 MUST 遵守管理端列表页、弹窗宽度 CSS 层叠和媒体上传全链路最佳实践。实现 MUST 使用 semantic token 和现有 DS / shared 组件，MUST 不复制原型裸 Hex，MUST 不使用 `window.confirm`。多图上传和缩略图能力上线后，列表分页、指标卡、fixed toast、DS confirm、弹窗宽度、矮视口滚动、上传状态机、同会话回显和 Docker Web 上传边界验收 MUST 不回归。

#### Scenario: 列表页一致性验收
- **WHEN** 在 1440x1024 视口验收品牌证书页
- **THEN** 分页 DOM MUST 与用户管理基准一致
- **AND** 指标卡 MUST 使用 `.metric-label`、`.metric-value`、`.metric-desc` 或等价 DS 结构
- **AND** 成功/失败反馈 MUST 使用 fixed toast 且不造成布局位移。

#### Scenario: 弹窗层叠验收
- **WHEN** 验收新增或编辑证书弹窗
- **THEN** TSX MUST NOT 同时挂载通用 `modal-card` 与业务专属 modal class
- **AND** 1440 视口 Computed width MUST 为 760px
- **AND** 矮视口下弹窗 body MUST 可滚动且按钮可达。

#### Scenario: 上传链路验收
- **WHEN** 通过 Docker Web 入口 `http://localhost:3000` 上传证书边界文件
- **THEN** 合法小文件 MUST 上传成功并即时回显
- **AND** 超限文件 MUST 返回业务错误而非 Nginx 413
- **AND** 上传控件 MUST 覆盖 `idle → uploading → done / failed` 状态。

#### Scenario: 缩略图媒体五联验收
- **WHEN** 验收品牌证书图片缩略图能力
- **THEN** evidence MUST 覆盖对象 key 稳定且符合标准前缀
- **AND** 对象存储中原图和缩略图对象 MUST 可审计
- **AND** 后端 `/media/` 或等价受控 URL MUST 可访问
- **AND** 缩略图 MUST 证明真实尺寸或体积收益
- **AND** 管理端、小程序或店主端渲染 evidence MUST 覆盖缩略图、原图预览和失败占位。

#### Scenario: 多图上传横切验收
- **WHEN** 在新增或编辑证书弹窗验收多图上传控件
- **THEN** 图片卡片 MUST 覆盖 `idle → uploading → done / failed` 状态
- **AND** 同一会话内上传成功后列表或弹窗刷新 MUST 即时回显主图缩略图和图片卡片
- **AND** 多图区域在矮视口下 MUST 不遮挡头部、底部保存按钮或字段级错误
- **AND** 新上传 MUST NOT 写入 `data/uploads/`。

### Requirement: 管理端品牌证书通用组件
系统 MUST 在管理端沉淀品牌证书通用业务组件或等价展示方法，覆盖证书缩略图、证书摘要、有效期文本、有效状态 Badge、前台展示状态 Badge、预览入口、文件卡片、图片卡片和主图标记。组件 MUST 面向展示模型和回调设计，MUST NOT 内置筛选、分页、权限判断、保存、删除、显示/隐藏接口调用、上传 API 调用或全局 toast。图片证书的小图展示 SHOULD 优先使用真实缩略图，预览入口 SHALL 使用原图或原文件。

#### Scenario: 展示证书缩略图与摘要
- **WHEN** 管理端页面或弹窗传入证书文件 URL、缩略图 URL、文件名、MIME Type、证书名称、证书编号和可选品牌名称
- **THEN** 图片证书 MUST 展示稳定尺寸缩略图
- **AND** PDF 证书 MUST 展示统一 `PDF` 文件占位
- **AND** 文件 URL 为空、文件类型未知或图片加载失败时 MUST 展示统一文件占位且不显示浏览器破图
- **AND** 证书名称 MUST 作为主文本展示
- **AND** 证书编号为空时 MUST 展示文件名作为辅助文本
- **AND** 可选品牌名称 MUST 仅作为附加文本展示，不得内置品牌筛选、导航或接口调用
- **AND** 长文本 MUST 使用现有管理端列表截断规则，不撑破表格或弹窗布局。

#### Scenario: 触发证书预览
- **WHEN** 管理端用户点击缩略图、按钮、链接或等价预览入口
- **THEN** 组件 MUST 提供统一预览触发能力，并由调用方决定入口渲染形态
- **AND** 图片和 PDF v1 MUST 可通过新窗口打开受控原文件 URL
- **AND** 文件 URL 缺失时 MUST 阻止预览并返回可由页面展示的失败原因
- **AND** 预览失败提示 SHOULD 复用 `文件暂时无法预览，请稍后重试或下载查看`
- **AND** 组件 MUST NOT 绕过后端鉴权或生成未授权对象存储直连地址。

#### Scenario: 展示证书文件卡片状态
- **WHEN** 新增或编辑证书弹窗展示证书文件卡片
- **THEN** 文件卡片 MUST 支持 `idle`、`uploading`、`done`、`failed` 四类状态
- **AND** `done` 状态 MUST 展示缩略图或文件类型、文件名、文件大小、重新上传和删除入口
- **AND** `failed` 状态 MUST 展示失败原因和重新上传入口
- **AND** 文件卡片 MUST 只负责展示和触发回调，不得直接调用上传 API。

#### Scenario: 展示证书主图与图片卡片
- **WHEN** 管理端页面或弹窗传入证书图片列表
- **THEN** 组件或等价展示方法 MUST 优先展示 `is_main=true` 的主图缩略图
- **AND** 非主图图片 MUST 可展示稳定图片卡片和“设为主图”回调入口
- **AND** 主图标记、删除入口和预览入口 MUST 不遮挡图片主体识别
- **AND** 图片加载失败时 MUST 展示稳定占位且不显示浏览器破图。
