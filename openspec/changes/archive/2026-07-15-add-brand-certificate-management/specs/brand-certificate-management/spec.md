## ADDED Requirements

### Requirement: 管理端品牌证书数据模型

系统 MUST 维护品牌证书主数据，建立 `brand 1:N brand_certificate` 关系。每条证书 MUST 关联且仅关联一个品牌，MUST 支持证书名称、排序、类型、编号、发证机构、文件元数据、长期有效标记、生效日期、到期日期、前台展示状态、备注、软删除、创建时间和更新时间。系统 MUST 支持同品牌内证书名称唯一性校验，并 MUST 在品牌存在未删除证书时阻止删除品牌或要求先迁移/删除证书。

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

### Requirement: 管理端品牌证书列表与筛选 API

系统 MUST 提供管理端品牌证书列表 API，允许已授权管理端用户按关键词、所属品牌、证书类型、有效状态、展示状态、页码和每页条数查询证书。响应 MUST 包含分页列表、分页信息和指标汇总，并 MUST 返回服务端计算的有效状态。

#### Scenario: 查询证书列表

- **WHEN** 已授权管理端用户请求 `GET /api/v1/admin/brand-certificates`
- **THEN** 系统 MUST 返回 HTTP 200
- **AND** 响应 MUST 包含 `items`、`pagination` 和 `summary`
- **AND** 列表项 MUST 包含证书文件可预览 URL 或等价受控读取引用

#### Scenario: 筛选条件生效

- **WHEN** 请求携带 `keyword`、`brand_id`、`type`、`validity_status` 或 `display_status`
- **THEN** 系统 MUST 按条件过滤品牌证书
- **AND** `keyword` MUST 支持证书名称、证书编号和发证机构模糊搜索

#### Scenario: 非管理端用户被拒绝

- **WHEN** 未认证用户或无管理端权限用户请求品牌证书列表 API
- **THEN** 系统 MUST 返回 HTTP 401 或 403

### Requirement: 管理端品牌证书创建与更新 API

系统 MUST 提供创建、详情和更新品牌证书 API。创建和更新 MUST 校验证书名称、排序、类型、文件、日期、品牌存在性和同品牌名称唯一性。非长期有效证书 MUST 填写到期日期；长期有效开启时系统 MUST 清空或忽略生效日期和到期日期。

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

### Requirement: 品牌证书文件上传与预览

系统 MUST 支持品牌证书文件经后端鉴权上传至 MinIO 单桶。证书文件 MUST 支持 JPG、PNG、WebP 和 PDF，单文件最大 20MB。上传链路 MUST 校验 MIME、大小和对象 Key，MUST 返回可受控读取的 `file_url`、`file_key`、文件名、MIME 和大小。前端 MUST NOT 直连未授权对象存储。

#### Scenario: 上传合法证书文件

- **WHEN** 已授权管理端用户上传合法 JPG、PNG、WebP 或 PDF 证书文件
- **THEN** 系统 MUST 将对象写入 `MINIO_BUCKET`
- **AND** MUST 返回 `file_key` 和可读取的 `file_url`
- **AND** 对象 Key MUST NOT 使用用户原始文件名

#### Scenario: 上传文件类型非法

- **WHEN** 用户上传非 JPG、PNG、WebP 或 PDF 文件
- **THEN** 系统 MUST 返回 HTTP 400
- **AND** 错误码 MUST 为 `CERTIFICATE_FILE_TYPE_INVALID` 或统一文件类型错误码

#### Scenario: 上传文件过大

- **WHEN** 用户上传超过 20MB 的证书文件
- **THEN** 系统 MUST 返回 HTTP 400
- **AND** 错误码 MUST 为 `CERTIFICATE_FILE_TOO_LARGE` 或统一文件大小错误码
- **AND** Web Docker 入口 MUST NOT 以 Nginx 413 作为业务校验结果

#### Scenario: 预览证书文件

- **WHEN** 管理员点击图片证书或 PDF 证书的预览入口
- **THEN** 图片证书 MUST 支持大图预览
- **AND** PDF 证书 MUST 支持新窗口或等价受控 URL 预览
- **AND** 预览失败时 MUST 展示稳定错误提示

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

系统 MUST 提供新增和编辑品牌证书弹窗。弹窗 MUST 宽 760px，最大高度 `calc(100vh - 80px)`，头部和底部固定，主体区域可滚动。弹窗 MUST 支持所属品牌、证书名称、排序、类型、编号、发证机构、证书文件、长期有效、生效日期、到期日期、前台展示和备注字段。

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

品牌证书管理页 MUST 遵守管理端列表页、弹窗宽度 CSS 层叠和媒体上传全链路最佳实践。实现 MUST 使用 semantic token 和现有 DS / shared 组件，MUST 不复制原型裸 Hex，MUST 不使用 `window.confirm`。

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
