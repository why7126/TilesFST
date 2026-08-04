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

品牌证书文件上传 MUST 通过后端授权上传接口完成，MUST 校验 MIME Type、扩展名、文件大小和对象 Key 前缀。证书上传 MUST 支持 PDF、JPG、PNG、WebP，PDF 等文档类证书 MUST 按文件类资源保存，图片类证书 MUST 按图片类资源保存。图片类证书 MUST 支持多图上传、唯一主图、缩略图 URL、原图 URL 和受控预览；PDF 证书 MUST 支持受控 URL 预览。上传响应与证书详情响应 MUST NOT 暴露对象存储凭据、未授权 raw URL、本机路径或用户原始文件名作为对象 key。

#### Scenario: 上传证书多图图片

- **WHEN** 已授权管理端用户上传合法 JPG、PNG 或 WebP 证书图片
- **THEN** 系统 MUST 返回可用于证书图片数组保存的文件引用、受控读取 URL、缩略图引用、文件名、MIME 和大小
- **AND** 图片类证书对象 Key MUST 使用 `images/` 标准图片前缀
- **AND** 缩略图对象 Key MUST 与原图保持同一图片资源归属
- **AND** 上传控件 MUST 在同一会话中即时回显图片卡片
- **AND** 上传失败原因 MUST 展示在上传控件或对应图片卡片内。

#### Scenario: 上传 PDF 证书文件

- **WHEN** 已授权管理端用户上传合法 PDF 证书文件
- **THEN** 系统 MUST 返回可用于证书文件保存的文件引用、受控读取 URL、文件名、MIME 和大小
- **AND** PDF 证书对象 Key MUST 使用 `files/` 前缀
- **AND** 系统 MUST NOT 为 PDF 证书生成图片缩略图 key
- **AND** PDF 证书 MUST 支持新窗口或等价受控 URL 预览。

#### Scenario: 编辑已有证书图片回显

- **GIVEN** 已有品牌证书存在一张或多张图片
- **WHEN** 管理员打开该证书编辑弹窗
- **THEN** 图片区域 MUST 正常展示图片列表
- **AND** 每张图片 MUST 使用可受控读取的缩略图 URL、原图 URL 或稳定占位展示
- **AND** 图片类证书 key 不符合 `images/` 标准前缀时 MUST 通过迁移或兼容读取策略处理，并在验收证据中记录
- **AND** 预览、删除和设为主图入口 MUST 可见且不遮挡图片主体识别
- **AND** MUST NOT 展示对象 key、内部路径、原始文件名或无意义文件名噪音

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

系统 MUST 在管理端提供 `/admin/brand-certificates` 页面。页面 MUST 作为独立一级品牌证书管理页，左侧导航 MUST 独立高亮“品牌证书”，并 MUST 提供指标概览、即时筛选、证书列表、分页、新增/编辑弹窗、预览、显示/隐藏和删除入口。页面 MUST 不展示品牌摘要栏或品牌详情面包屑。证书列表中的证书字段 MUST 仅展示证书主图和证书名称；当无主图或主图不可读时 MUST 展示稳定占位并保持证书名称可读。证书列表的证书字段 MUST NOT 展示图片名称、文件名称、对象 key、原始 URL、上传控件内部文案或文件就绪文案。

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

#### Scenario: 证书列表字段隐藏文件名噪音

- **GIVEN** 品牌证书列表项包含证书主图、证书名称、图片文件名、证书文件名、对象 key 或原始 URL
- **WHEN** 管理端用户查看 `/admin/brand-certificates` 列表
- **THEN** 证书字段 MUST 展示证书主图和证书名称
- **AND** 证书字段 MUST NOT 展示图片名称、文件名称、对象 key、原始 URL、上传组件内部文案或文件就绪文案
- **AND** 列表排序、筛选、分页和编辑入口 MUST 保持可用

#### Scenario: 证书列表无主图占位

- **GIVEN** 品牌证书列表项没有可展示主图
- **WHEN** 管理端用户查看证书字段
- **THEN** 页面 MUST 展示稳定占位
- **AND** 证书名称 MUST 仍清晰可读
- **AND** 页面 MUST NOT 使用图片文件名、证书文件名、对象 key 或原始 URL 替代证书名称

### Requirement: 品牌证书新增编辑弹窗

系统 MUST 提供新增和编辑品牌证书弹窗。弹窗 MUST 宽 760px，最大高度 `calc(100vh - 80px)`，头部和底部固定，主体区域可滚动。弹窗 MUST 支持所属品牌、证书名称、排序、类型、编号、发证机构、证书文件或图片列表、长期有效、生效日期、到期日期、前台展示和备注字段。弹窗 MUST 支持证书多张图片上传、主图设置、删除图片和主图兜底规则。编辑已有证书时，弹窗 MUST 区分已有文件回显态与本次上传完成态，MUST 正常回显已有图片列表、唯一主图状态、缩略图或原图预览入口，并 MUST NOT 显示 `证书文件已就绪`、对象 key、原始文件名或无意义文件名噪音。

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

#### Scenario: 编辑已有证书文件回显

- **GIVEN** 已有品牌证书存在 PDF、兼容文件或受控文件预览引用
- **WHEN** 管理员打开该证书编辑弹窗
- **THEN** 文件区域 MUST 以已有文件回显态展示文件占位、预览入口或替换入口
- **AND** MUST NOT 显示 `证书文件已就绪`
- **AND** 文件缺失、上传失败、格式不兼容或预览不可用时 MUST 保留稳定错误提示

#### Scenario: 编辑已有证书图片回显

- **GIVEN** 已有品牌证书存在一张或多张图片
- **WHEN** 管理员打开该证书编辑弹窗
- **THEN** 图片区域 MUST 正常展示图片列表
- **AND** 每张图片 MUST 使用可受控读取的缩略图 URL、原图 URL 或稳定占位展示
- **AND** 唯一主图 MUST 正确标识，非主图 MUST 不被误标为主图
- **AND** 预览、删除和设为主图入口 MUST 可见且不遮挡图片主体识别
- **AND** MUST NOT 展示对象 key、内部路径、原始文件名或无意义文件名噪音

#### Scenario: 编辑已有证书图片保存后回显

- **GIVEN** 管理员在证书编辑弹窗中新增、替换、删除图片或设置主图
- **WHEN** 保存成功并再次打开同一证书编辑弹窗
- **THEN** 图片数量、图片顺序、主图状态、预览信息和操作状态 MUST 与保存结果一致
- **AND** MUST NOT 出现图片信息全部消失、主图状态错乱或对象 key 噪音

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

### Requirement: 管理端品牌证书页面组件化应用

系统 MUST 将品牌证书通用组件或等价展示方法应用到现有 `/admin/brand-certificates` 页面。组件化 MUST 保持页面筛选、分页、权限判断、保存、删除、显示/隐藏确认、固定 toast、指标卡 DOM 和弹窗宽度行为不回归。多图能力上线后，页面 MUST 使用主图作为列表缩略图，并在弹窗文件展示区呈现图片列表、主图标记、上传状态和删除/设主图操作。编辑已有证书时，页面 MUST 将详情数据归一化为文件卡片和图片卡片展示模型，确保保存后再次打开弹窗仍正确回显图片数量、顺序、主图状态和预览信息。

#### Scenario: 弹窗多图区域应用

- **WHEN** 管理端用户打开新增或编辑品牌证书弹窗
- **THEN** 证书文件展示区 MUST 支持多张图片卡片、唯一主图标记、上传进度、失败原因、删除入口和设为主图入口
- **AND** 保存证书后再次打开弹窗 MUST 回显图片数量、图片顺序和主图标记
- **AND** “支持 JPG / PNG / WebP，最多 9 张”或等价上传说明下方 MUST NOT 额外展示图片文件名文本列表
- **AND** 移除文件名文本列表 MUST NOT 影响图片卡片、主图标记、删除入口、设为主图入口、继续添加图片、上传进度或失败提示

#### Scenario: 编辑弹窗详情数据归一化

- **GIVEN** 管理端品牌证书详情响应包含文件字段、图片数组、缩略图引用、原图引用和主图标记
- **WHEN** 页面打开编辑弹窗并初始化表单
- **THEN** 页面 MUST 将详情数据归一化为文件卡片和图片卡片展示模型
- **AND** 归一化结果 MUST 保留图片 ID、稳定预览 URL、缩略图 URL、排序和 `is_main`
- **AND** 缺失缩略图时 MUST 回退原图或统一占位
- **AND** 前端 MUST NOT 用对象 key、内部路径或原始文件名猜测运营展示文案

