# brand-certificate-management Specification

## Purpose
定义管理端品牌证书主数据、上传、API、页面、权限与横切 UI 验收要求，用于支撑品牌资质、检测报告、荣誉证书等文件的结构化维护与前台展示控制。
## Requirements
### Requirement: 管理端品牌证书数据模型

系统 MUST 维护品牌证书主数据，建立 `brand 1:N brand_certificate` 关系。每条证书 MUST 关联且仅关联一个品牌，MUST 支持证书名称、排序、类型、编号、发证机构、文件元数据、证书图片列表、唯一主图、长期有效标记、生效日期、到期日期、前台展示状态、备注、软删除、创建时间和更新时间。系统 MUST 支持同品牌内证书名称唯一性校验，并 MUST 在品牌存在未删除证书时阻止删除品牌或要求先迁移/删除证书。系统 MUST 兼容既有单文件证书数据，并 MUST 在有图片列表时保证同一证书仅有一张主图。

#### Scenario: 创建证书数据

- **WHEN** 管理端提交合法品牌、证书名称、排序、类型和证书文件元数据
- **THEN** 系统 MUST 创建品牌证书记录
- **AND** 记录 MUST 保存 `brand_id`
- **AND** 一个证书 MUST NOT 同时关联多个品牌

#### Scenario: 同品牌证书名称重复

- **GIVEN** 品牌 A 已存在未删除证书“ISO 9001 质量管理体系认证”
- **WHEN** 管理员为品牌 A 创建或更新同名未删除证书
- **THEN** 系统 MUST 拒绝请求
- **AND** 返回错误码 `CERTIFICATE_NAME_DUPLICATED`

#### Scenario: 删除品牌存在证书

- **GIVEN** 品牌存在未删除品牌证书
- **WHEN** 管理员请求删除该品牌
- **THEN** 系统 MUST 阻止删除或要求先迁移/删除证书
- **AND** MUST NOT 静默级联删除证书文件和证书记录

#### Scenario: 保存证书多张图片

- **WHEN** 管理端提交包含多张证书图片的创建或更新请求
- **THEN** 系统 MUST 保存图片文件引用、展示 URL 或受控读取引用、文件名、MIME、大小、`is_main` 和 `sort_order`
- **AND** 有图片时 MUST 保证 `is_main=true` 必须且只能出现一次
- **AND** 图片排序 MUST 与保存 payload 的 `sort_order` 一致

#### Scenario: 兼容旧单文件证书

- **GIVEN** 既有品牌证书仅保存单文件字段且没有图片列表
- **WHEN** 管理端查询列表或详情
- **THEN** 系统 MUST 返回可兼容展示的证书文件信息
- **AND** 图片文件 MAY 作为默认主图展示模型返回
- **AND** PDF 或文档文件 MUST 继续使用文件占位或等价兼容展示

### Requirement: 管理端品牌证书列表与筛选 API

系统 MUST 提供管理端品牌证书列表 API，允许已授权管理端用户按关键词、所属品牌、证书类型、有效状态、展示状态、页码和每页条数查询证书。响应 MUST 包含分页列表、分页信息和指标汇总，并 MUST 返回服务端计算的有效状态。列表项 MUST 返回证书主图信息或等价主图缩略图读取引用；当证书无主图图片时，MUST 返回既有证书文件可预览 URL 或等价受控读取引用作为兼容 fallback。

#### Scenario: 查询证书列表

- **WHEN** 已授权管理端用户请求 `GET /api/v1/admin/brand-certificates`
- **THEN** 系统 MUST 返回 HTTP 200
- **AND** 响应 MUST 包含 `items`、`pagination` 和 `summary`
- **AND** 列表项 MUST 包含证书文件可预览 URL 或等价受控读取引用
- **AND** 列表项 MUST 优先包含主图缩略图信息或主图受控读取引用

#### Scenario: 筛选条件生效

- **WHEN** 请求携带 `keyword`、`brand_id`、`type`、`validity_status` 或 `display_status`
- **THEN** 系统 MUST 按条件过滤品牌证书
- **AND** `keyword` MUST 支持证书名称、证书编号和发证机构模糊搜索

#### Scenario: 非管理端用户被拒绝

- **WHEN** 未认证用户或无管理端权限用户请求品牌证书列表 API
- **THEN** 系统 MUST 返回 HTTP 401 或 403

### Requirement: 管理端品牌证书创建与更新 API

系统 MUST 提供创建、详情和更新品牌证书 API。创建和更新 MUST 校验证书名称、排序、类型、文件或图片列表、日期、品牌存在性和同品牌名称唯一性。非长期有效证书 MUST 填写到期日期；长期有效开启时系统 MUST 清空或忽略生效日期和到期日期。创建和更新 MUST 支持证书图片数组，MUST 校验主图唯一性、图片排序、文件引用合法性和图片数量上限。

#### Scenario: 创建证书成功

- **WHEN** 已授权管理端用户提交合法 `POST /api/v1/admin/brand-certificates`
- **THEN** 系统 MUST 返回 HTTP 200 或 201
- **AND** 响应 MUST 包含创建后的证书对象
- **AND** `is_visible` 默认值 MUST 为 true

#### Scenario: 更新证书所属品牌

- **WHEN** 已授权管理端用户通过 `PUT /api/v1/admin/brand-certificates/{certificate_id}` 修改 `brand_id`
- **THEN** 系统 MUST 校验目标品牌存在
- **AND** MUST 重新校验目标品牌下证书名称唯一性

#### Scenario: 日期顺序非法

- **WHEN** 非长期有效证书的到期日期早于生效日期
- **THEN** 系统 MUST 返回 HTTP 400
- **AND** 错误码 MUST 为 `CERTIFICATE_DATE_INVALID`

#### Scenario: 文件缺失

- **WHEN** 创建证书请求未提供合法证书文件元数据
- **THEN** 系统 MUST 返回 HTTP 400
- **AND** 错误码 MUST 为 `CERTIFICATE_FILE_REQUIRED`

#### Scenario: 创建多图证书成功

- **WHEN** 已授权管理端用户提交合法证书图片数组，且数组中包含唯一主图
- **THEN** 系统 MUST 保存证书和图片列表
- **AND** 响应 MUST 返回图片数量、图片顺序和主图标记
- **AND** 再次查询证书详情 MUST 与保存结果一致

#### Scenario: 主图状态非法

- **WHEN** 创建或更新请求中的图片数组存在多个主图，或有图片但没有主图
- **THEN** 系统 MUST 返回 HTTP 400
- **AND** 错误码 MUST 为 `CERTIFICATE_MAIN_IMAGE_INVALID` 或等价统一校验错误码

#### Scenario: 图片文件引用非法

- **WHEN** 创建或更新请求中的图片文件引用不属于后端上传链路可识别对象
- **THEN** 系统 MUST 返回 HTTP 400
- **AND** MUST NOT 保存前端伪造的对象存储路径或未授权 URL

### Requirement: 品牌证书文件上传与预览

系统 MUST 支持品牌证书文件经后端鉴权上传至 MinIO/S3 兼容对象存储单桶。证书文件 MUST 支持 JPG、PNG、WebP 和 PDF；证书多图图片 MUST 支持 JPG、PNG 和 WebP。证书文件大小上限 MUST 使用文档 / 文件类 effective 上传限制（例如 `media.max_file_size_mb` merge `MAX_FILE_SIZE_MB`），并 MUST 与管理端系统设置、前端提示、后端校验和部署代理配置一致；MUST NOT 仅使用不可配置的 20MB 硬编码作为大小限制事实源。上传链路 MUST 校验 MIME、大小和对象 Key，MUST 返回可受控读取的 `file_url`、`file_key`、文件名、MIME 和大小。前端 MUST NOT 直连未授权对象存储。

#### Scenario: 上传合法证书文件

- **WHEN** 已授权管理端用户上传合法 JPG、PNG、WebP 或 PDF 证书文件，且文件大小在文档 / 文件类 effective 上限内
- **THEN** 系统 MUST 将对象写入对象存储单桶
- **AND** MUST 返回 `file_key` 和可读取的 `file_url`
- **AND** 对象 Key MUST NOT 使用用户原始文件名

#### Scenario: 上传约 23MB PDF 证书文件

- **GIVEN** effective 文档 / 文件上传上限大于等于 23MB
- **WHEN** 已授权管理端用户上传约 23MB 合法 PDF 证书文件
- **THEN** 上传 MUST 成功
- **AND** MUST NOT 被硬编码 20MB 限制拒绝

#### Scenario: 上传文件类型非法

- **WHEN** 用户上传非 JPG、PNG、WebP 或 PDF 文件
- **THEN** 系统 MUST 返回 HTTP 400
- **AND** 错误码 MUST 为 `CERTIFICATE_FILE_TYPE_INVALID` 或统一文件类型错误码

#### Scenario: 上传文件过大

- **WHEN** 用户上传超过文档 / 文件类 effective 上限的证书文件
- **THEN** 系统 MUST 返回 HTTP 400
- **AND** 错误码 MUST 为 `CERTIFICATE_FILE_TOO_LARGE` 或统一文件大小错误码
- **AND** 错误提示 MUST 包含当前有效大小限制或等价可诊断信息
- **AND** Web Docker 入口 MUST NOT 以 Nginx 413 作为业务校验结果

#### Scenario: 预览证书文件

- **WHEN** 管理员点击图片证书或 PDF 证书的预览入口
- **THEN** 图片证书 MUST 支持大图预览
- **AND** PDF 证书 MUST 支持新窗口或等价受控 URL 预览
- **AND** 预览失败时 MUST 展示稳定错误提示

#### Scenario: 上传证书多图图片

- **WHEN** 已授权管理端用户上传合法 JPG、PNG 或 WebP 证书图片
- **THEN** 系统 MUST 返回可用于证书图片数组保存的文件引用、受控读取 URL、文件名、MIME 和大小
- **AND** 上传控件 MUST 在同一会话中即时回显图片卡片
- **AND** 上传失败原因 MUST 展示在上传控件或对应图片卡片内

#### Scenario: 预览证书主图和图片列表

- **WHEN** 管理员点击证书主图或默认预览入口
- **THEN** 系统 MUST 从主图开始预览图片证书
- **AND** 主图加载失败时 MUST 展示稳定占位和可恢复提示
- **AND** 预览和展示 MUST 使用后端控制的可读 URL 或签名 URL

### Requirement: 品牌证书展示控制、删除与审计

系统 MUST 支持品牌证书显示、隐藏和软删除。显示/隐藏与删除操作 MUST 经过权限校验，并 MUST 写入审计记录。删除后证书 MUST 不再出现在店主端可展示数据中，但对象存储文件不应立即物理删除。

#### Scenario: 隐藏证书

- **WHEN** 已授权管理端用户请求隐藏证书
- **THEN** 系统 MUST 将证书设置为不可前台展示
- **AND** MUST 写入审计记录

#### Scenario: 显示证书

- **WHEN** 已授权管理端用户请求显示证书
- **THEN** 系统 MUST 将证书设置为可前台展示
- **AND** MUST 写入审计记录

#### Scenario: 软删除证书

- **WHEN** 已授权管理端用户删除证书
- **THEN** 系统 MUST 软删除证书记录
- **AND** 店主端可展示数据 MUST 不再包含该证书
- **AND** MUST 写入审计记录

### Requirement: 管理端品牌证书页面

系统 MUST 在管理端提供 `/admin/brand-certificates` 页面。页面 MUST 作为独立一级品牌证书管理页，左侧导航 MUST 独立高亮“品牌证书”，并 MUST 提供指标概览、即时筛选、证书列表、分页、新增/编辑弹窗、预览、显示/隐藏和删除入口。页面 MUST 不展示品牌摘要栏或品牌详情面包屑。

#### Scenario: 打开品牌证书页面

- **WHEN** 管理端用户访问 `/admin/brand-certificates`
- **THEN** 左侧导航 MUST 高亮“品牌证书”
- **AND** 页面 MUST 展示标题、说明、新增证书按钮、四个指标卡、筛选区、列表和分页
- **AND** 页面 MUST NOT 展示品牌摘要栏

#### Scenario: 品牌快捷入口筛选

- **WHEN** 用户从品牌列表页点击某品牌的证书快捷入口
- **THEN** 系统 MUST 跳转到 `/admin/brand-certificates?brand_id={brand_id}`
- **AND** 品牌证书页 MUST 自动应用所属品牌筛选

#### Scenario: 筛选即时生效

- **WHEN** 用户输入关键词或改变下拉筛选
- **THEN** 关键词 MUST 在 300ms 防抖后生效
- **AND** 下拉筛选 MUST 立即生效
- **AND** 当前页 MUST 重置为第 1 页
- **AND** 筛选条件 MUST 同步到 URL Query

#### Scenario: 分页结构

- **WHEN** 页面展示分页
- **THEN** 左侧 MUST 显示 `共 x 个证书`
- **AND** 右侧 MUST 显示上一页、页码、下一页和每页显示 20/50/100 条
- **AND** MUST NOT 展示跳页输入框

### Requirement: 品牌证书新增编辑弹窗

系统 MUST 提供新增和编辑品牌证书弹窗。弹窗 MUST 宽 760px，最大高度 `calc(100vh - 80px)`，头部和底部固定，主体区域可滚动。弹窗 MUST 支持所属品牌、证书名称、排序、类型、编号、发证机构、证书文件或图片列表、长期有效、生效日期、到期日期、前台展示和备注字段。弹窗 MUST 支持证书多张图片上传、主图设置、删除图片和主图兜底规则。

#### Scenario: 打开新增证书弹窗

- **WHEN** 用户点击“新增证书”
- **THEN** 系统 MUST 打开新增证书弹窗
- **AND** 弹窗 MUST 展示所属品牌、证书名称、排序、类型和证书文件等必填字段

#### Scenario: 长期有效联动

- **WHEN** 用户开启长期有效
- **THEN** 生效日期和到期日期 MUST 被清空并禁用
- **AND** 用户关闭长期有效后日期字段 MUST 恢复可编辑

#### Scenario: 保存失败

- **WHEN** 保存证书失败
- **THEN** 弹窗 MUST 保持打开
- **AND** MUST 保留用户输入和上传结果
- **AND** MUST 展示服务端错误

#### Scenario: 字段级校验提示

- **WHEN** 用户提交新增或编辑证书弹窗且品牌、名称、排序、类型、证书文件或日期存在本地校验错误
- **THEN** 系统 MUST 将错误提示展示在对应字段、字段组或上传对象下方
- **AND** MUST NOT 仅将字段级错误集中展示在弹窗底部或全局 toast

#### Scenario: 第一张图片默认主图

- **WHEN** 证书还没有任何图片且第一张图片上传成功
- **THEN** 弹窗 MUST 自动将该图片标记为主图
- **AND** 主图标记 MUST 在弹窗内即时可见

#### Scenario: 设置主图并前置

- **WHEN** 用户将非主图图片设置为主图
- **THEN** 该图片 MUST 成为唯一主图
- **AND** 原主图 MUST 取消主图标记
- **AND** 新主图 MUST 移动到图片列表第一位

#### Scenario: 删除图片与主图兜底

- **WHEN** 用户删除非主图图片
- **THEN** 当前主图 MUST 保持不变
- **AND** 剩余图片顺序 MUST 保持稳定
- **WHEN** 用户删除当前主图且仍有其他图片
- **THEN** 当前主图后一张图片 MUST 优先成为新主图；否则删除后列表第一张图片 MUST 成为新主图
- **AND** 新主图 MUST 在弹窗内即时可见

#### Scenario: 删除全部图片

- **WHEN** 用户删除最后一张图片
- **THEN** 图片区域 MUST 进入空状态
- **AND** MUST 不再显示主图标记
- **AND** MUST 保留继续添加图片入口

### Requirement: 品牌证书权限与前端操作可见性

系统 MUST 定义品牌证书权限点，并在后端 API 与前端操作入口中执行权限约束。无权限用户 MUST 不能越权创建、更新、显示、隐藏或删除证书。

#### Scenario: 无创建权限

- **WHEN** 用户没有 `brand_certificate:create` 权限
- **THEN** 前端 MUST 隐藏新增证书按钮
- **AND** 后端 MUST 拒绝创建请求

#### Scenario: 无更新权限

- **WHEN** 用户没有 `brand_certificate:update` 权限
- **THEN** 前端 MUST 隐藏编辑入口或展示只读状态
- **AND** 后端 MUST 拒绝更新请求

#### Scenario: 无删除权限

- **WHEN** 用户没有 `brand_certificate:delete` 权限
- **THEN** 前端 MUST 隐藏删除入口
- **AND** 后端 MUST 拒绝删除请求

### Requirement: 品牌证书横切 UI 验收

品牌证书管理页 MUST 遵守管理端列表页、弹窗宽度 CSS 层叠和媒体上传全链路最佳实践。实现 MUST 使用 semantic token 和现有 DS / shared 组件，MUST 不复制原型裸 Hex，MUST 不使用 `window.confirm`。多图上传能力上线后，列表分页、指标卡、fixed toast、DS confirm、弹窗宽度、矮视口滚动和 Docker Web 上传边界验收 MUST 不回归。

#### Scenario: 列表页一致性验收

- **WHEN** 在 1440x1024 视口验收品牌证书页
- **THEN** 分页 DOM MUST 与用户管理基准一致
- **AND** 指标卡 MUST 使用 `.metric-label`、`.metric-value`、`.metric-desc` 或等价 DS 结构
- **AND** 成功/失败反馈 MUST 使用 fixed toast 且不造成布局位移

#### Scenario: 弹窗层叠验收

- **WHEN** 验收新增或编辑证书弹窗
- **THEN** TSX MUST NOT 同时挂载通用 `modal-card` 与业务专属 modal class
- **AND** 1440 视口 Computed width MUST 为 760px
- **AND** 矮视口下弹窗 body MUST 可滚动且按钮可达

#### Scenario: 上传链路验收

- **WHEN** 通过 Docker Web 入口 `http://localhost:3000` 上传证书边界文件
- **THEN** 合法小文件 MUST 上传成功并即时回显
- **AND** 超限文件 MUST 返回业务错误而非 Nginx 413
- **AND** 上传控件 MUST 覆盖 `idle → uploading → done / failed` 状态

#### Scenario: 多图上传横切验收

- **WHEN** 在新增或编辑证书弹窗验收多图上传控件
- **THEN** 图片卡片 MUST 覆盖 `idle → uploading → done / failed` 状态
- **AND** 同一会话内上传成功后列表或弹窗刷新 MUST 即时回显主图缩略图和图片卡片
- **AND** 多图区域在矮视口下 MUST 不遮挡头部、底部保存按钮或字段级错误
- **AND** 新上传 MUST NOT 写入 `data/uploads/`

### Requirement: 管理端品牌证书通用组件

系统 MUST 在管理端沉淀品牌证书通用业务组件或等价展示方法，覆盖证书缩略图、证书摘要、有效期文本、有效状态 Badge、前台展示状态 Badge、预览入口、文件卡片、图片卡片和主图标记。组件 MUST 面向展示模型和回调设计，MUST NOT 内置筛选、分页、权限判断、保存、删除、显示/隐藏接口调用、上传 API 调用或全局 toast。

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

#### Scenario: 展示证书主图与图片卡片

- **WHEN** 管理端页面或弹窗传入证书图片列表
- **THEN** 组件或等价展示方法 MUST 优先展示 `is_main=true` 的主图缩略图
- **AND** 非主图图片 MUST 可展示稳定图片卡片和“设为主图”回调入口
- **AND** 主图标记、删除入口和预览入口 MUST 不遮挡图片主体识别
- **AND** 图片加载失败时 MUST 展示稳定占位且不显示浏览器破图

### Requirement: 管理端品牌证书页面组件化应用

系统 MUST 将品牌证书通用组件或等价展示方法应用到现有 `/admin/brand-certificates` 页面。组件化 MUST 保持页面筛选、分页、权限判断、保存、删除、显示/隐藏确认、固定 toast、指标卡 DOM 和弹窗宽度行为不回归。多图能力上线后，页面 MUST 使用主图作为列表缩略图，并在弹窗文件展示区呈现图片列表、主图标记、上传状态和删除/设主图操作。

#### Scenario: 弹窗多图区域应用

- **WHEN** 管理端用户打开新增或编辑品牌证书弹窗
- **THEN** 证书文件展示区 MUST 支持多张图片卡片、唯一主图标记、上传进度、失败原因、删除入口和设为主图入口
- **AND** 保存证书后再次打开弹窗 MUST 回显图片数量、图片顺序和主图标记
- **AND** “支持 JPG / PNG / WebP，最多 9 张”或等价上传说明下方 MUST NOT 额外展示图片文件名文本列表
- **AND** 移除文件名文本列表 MUST NOT 影响图片卡片、主图标记、删除入口、设为主图入口、继续添加图片、上传进度或失败提示

