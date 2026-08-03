# miniapp-certificate-list-page Specification

## Purpose
TBD - created by archiving change add-miniapp-certificate-list-page. Update Purpose after archive.
## Requirements
### Requirement: 小程序公开证书列表页
系统 SHALL 提供微信小程序公开证书列表页，用于在 TabBar「证书」入口集中展示企业可公开证书，并替代建设中占位页。

#### Scenario: 用户进入证书 Tab
- **WHEN** 用户点击小程序底部 TabBar「证书」
- **THEN** 小程序 SHALL 进入 `pages/certificates/index`
- **AND** 页面 SHALL 展示真实证书列表页标题、列表容器和加载状态
- **AND** 页面 SHALL NOT 以“功能建设中”作为主体验。

#### Scenario: 首屏加载证书列表
- **WHEN** 用户首次进入证书列表页
- **THEN** 小程序 SHALL 请求公开证书列表数据
- **AND** 首屏加载期间 SHALL 展示与最终布局一致的骨架或加载状态
- **AND** 加载成功后 SHALL 展示证书卡片列表或空状态。

### Requirement: 公开证书列表 API
系统 SHALL 提供公开证书列表 API 或等价后端能力，仅返回允许在小程序展示的证书数据。图片类证书列表项 SHOULD 返回缩略图 URL 或等价小图读取引用，并保留原图/原文件预览引用；PDF 证书 SHALL 继续返回文件类型和受控文件 URL，不要求 PDF 首页图片缩略图。

#### Scenario: 查询公开证书列表
- **WHEN** 小程序请求公开证书列表
- **THEN** 后端 SHALL 返回成功响应
- **AND** 响应 SHALL 包含证书列表和分页信息
- **AND** 列表项 SHALL 包含证书 ID、证书名称、证书类型、证书编号或发证机构、品牌 ID、品牌名称、文件 URL、缩略图 URL 或等价小图引用、文件名、MIME、有效期字段和有效状态。

#### Scenario: 过滤非公开证书
- **WHEN** 后端生成公开证书列表响应
- **THEN** 后端 SHALL 排除隐藏证书、软删除证书和所属品牌不可公开的证书
- **AND** 响应 SHALL NOT 暴露后台内部字段、对象存储原始 key、Authorization header、Cookie 或敏感配置。

#### Scenario: 证书列表排序稳定
- **WHEN** 小程序请求分页或加载更多证书
- **THEN** 证书列表 SHALL 使用稳定排序
- **AND** 分页追加 SHALL NOT 重复、遗漏或顺序漂移。

### Requirement: 证书卡片展示

小程序 SHALL 使用移动端两列证书卡片展示公开证书摘要，并对图片、PDF 和缺失文件稳定降级。图片证书卡片 SHALL 优先使用后端受控真实缩略图；预览或详情入口 SHALL 使用原图、原文件或等价安全引用。

#### Scenario: 展示证书文件占位
- **WHEN** 证书文件为图片、PDF、缺失或未知类型
- **THEN** 图片证书 SHALL 优先展示稳定比例真实缩略图
- **AND** PDF 证书 SHALL 展示统一 PDF 占位
- **AND** 文件缺失、类型未知、缩略图加载失败或图片加载失败时 SHALL 展示统一占位或回退原图
- **AND** 页面 SHALL NOT 出现浏览器破图、卡片高度跳动或文本遮挡
- **AND** 证书详情页、图片预览或文件打开 SHALL NOT 被强制降级为卡片缩略图。

#### Scenario: 证书卡片缩略图字段一致
- **WHEN** 小程序公开证书列表响应提供缩略图 URL、文件类型和等价卡片媒体引用
- **THEN** 证书列表卡片 SHALL 优先读取缩略图 URL 或等价小图引用
- **AND** 证书列表接口 SHOULD NOT 为每个列表 item 下发未被列表卡片渲染使用的原文件 URL
- **AND** 缩略图不可用时 SHALL 按统一策略展示 PDF 占位、缺失占位或其他稳定占位
- **AND** 小程序 SHALL NOT 在缩略图可用时直接使用原图或原文件 URL 作为图片证书卡片首选展示图。

### Requirement: 证书列表状态
小程序证书列表页 SHALL 不提供搜索或筛选功能，并区分加载、空结果、网络失败和加载更多状态。

#### Scenario: 不展示搜索和筛选入口
- **WHEN** 用户进入证书列表页
- **THEN** 页面 SHALL NOT 展示搜索框、证书类型筛选、品牌筛选、有效状态筛选或清除筛选入口
- **AND** 小程序 SHALL 仅按分页请求公开证书列表。

#### Scenario: 下拉刷新与加载更多
- **WHEN** 用户下拉刷新或触底加载更多
- **THEN** 小程序 SHALL 分别处理刷新、首屏加载和加载更多状态
- **AND** 重复触发 SHALL NOT 产生并发重复请求
- **AND** 无更多数据时 SHALL 展示轻量提示。

#### Scenario: 空状态与错误状态
- **WHEN** API 返回空列表或请求失败
- **THEN** 页面 SHALL 展示“暂无公开证书”
- **AND** 网络失败 SHALL 保留可用已加载数据或缓存并提供重试入口
- **AND** 页面 SHALL NOT 白屏或长期停留在无反馈加载状态。

### Requirement: 证书文件预览
小程序 SHALL 为公开证书提供图片或 PDF 文件预览能力，并在预览失败时稳定降级。证书列表页卡片主区域 SHALL 进入证书详情页；图片预览和 PDF 打开能力 SHALL 在证书详情页内提供，也 MAY 保留明确的非主点击预览入口。

#### Scenario: 证书列表主点击进入详情页
- **WHEN** 用户点击证书列表页证书卡片主区域
- **THEN** 小程序 SHALL 携带 `certificateId` 和可用来源参数进入证书详情页
- **AND** 小程序 SHALL NOT 直接把卡片主点击绑定为图片预览或 PDF 打开。

#### Scenario: 图片证书预览
- **WHEN** 用户在证书详情页点击图片预览入口或当前图片
- **THEN** 小程序 SHALL 使用图片预览能力展示证书图片
- **AND** 多图证书 SHALL 从当前图片开始预览并支持左右切换
- **AND** 预览失败时 SHALL 展示稳定错误提示
- **AND** 用户 SHALL 能返回证书详情继续浏览。

#### Scenario: PDF 证书预览
- **WHEN** 用户在证书详情页点击 PDF 证书打开入口
- **THEN** 小程序 SHALL 通过受控 URL 打开、复制提示或项目确认的等价方式处理 PDF
- **AND** 处理失败时 SHALL 展示稳定错误提示
- **AND** 小程序 SHALL NOT 暴露未授权对象存储直连地址或原始 object key。

### Requirement: 证书列表视觉、导航与设备验收
小程序证书列表页 SHALL 延续用户侧深色高端展示体系，并满足自定义导航、TabBar 和移动端视口验收要求。

#### Scenario: 视觉与布局
- **WHEN** 用户查看证书列表页
- **THEN** 页面 SHALL 使用与现有小程序页面一致的深色背景、卡片层、主文字、辅助文字和品牌金语义
- **AND** 证书卡片 SHALL 使用移动端两列布局
- **AND** 页面 SHALL NOT 复用管理端表格结构。

#### Scenario: 自定义导航验收
- **WHEN** 证书列表页使用全局自定义导航栏
- **THEN** 页面 SHALL 按 `docs/knowledge-base/best-practices/miniapp-custom-navigation.md` 验收状态栏、胶囊 reserve、页面 offset 和 TabBar 遮挡
- **AND** 首屏、加载态、空状态、错误态和网络失败提示 SHALL NOT 被顶部导航或底部 TabBar 遮挡。

#### Scenario: 视口与设备 evidence
- **WHEN** 团队验收证书列表页
- **THEN** 验收 SHALL 覆盖 320、375、430 pt DevTools 视口
- **AND** 页面 SHALL 无横向滚动、内容重叠、关键文字溢出或按钮不可达
- **AND** 真机不可用时 SHALL 标记 blocked 或 follow_up，不得写作真机通过。

### Requirement: 证书列表埋点与隐私
系统 SHALL 记录证书列表核心浏览行为，并避免记录与证书浏览无关的个人敏感信息。

#### Scenario: 证书列表行为埋点
- **WHEN** 用户浏览、点击或预览证书
- **THEN** 系统 SHALL 记录页面曝光、证书点击、预览点击和加载失败事件
- **AND** 埋点参数 SHALL 包含 terminal、certificateId、brandId、certificateType、index、sourcePage、resultCount 和 requestId 中可用字段。

#### Scenario: 埋点隐私边界
- **WHEN** 系统记录证书列表相关日志或埋点
- **THEN** 日志和埋点 SHALL NOT 记录手机号、地址、客户姓名、Authorization header、Cookie、密钥、`.env` 内容或未脱敏个人隐私。

### Requirement: 小程序证书详情页
小程序 SHALL 提供公开证书详情页，用于展示单张证书的公开媒体、证书信息、所属品牌入口、分享能力和异常状态。证书详情页 SHALL 参照 SKU 详情页的大媒体区、信息分区、品牌入口、分享和错误态体验，但 SHALL NOT 引入收藏、推荐、价格、购物、购买、库存、促销或询价能力。

#### Scenario: 多入口进入证书详情页
- **WHEN** 用户从证书列表页、品牌详情页证书区域或微信分享卡片进入证书详情
- **THEN** 小程序 SHALL 携带 `certificateId` 或等价稳定 ID 进入证书详情页
- **AND** 页面 SHALL 记录可用来源参数
- **AND** 缺少、非法或不存在的 `certificateId` 时 SHALL 展示可恢复错误状态，而不是白屏或路由错误。

#### Scenario: 展示证书详情主体
- **WHEN** 证书详情加载成功
- **THEN** 页面 SHALL 展示证书名称、证书类型、证书编号、发证机构、有效状态、备注说明和公开说明中可用字段
- **AND** 证书名称和证书类型 SHALL 必须展示
- **AND** 页面标题 SHALL 固定为“证书详情”
- **AND** 证书名称面板 SHALL NOT 重复展示品牌名称
- **AND** 证书信息模块 SHALL NOT 展示有效期
- **AND** 空字段 SHALL 隐藏对应模块或展示安全占位
- **AND** 页面 SHALL NOT 展示 `null`、`undefined`、接口字段名或异常空白卡片。

#### Scenario: 展示证书媒体区
- **WHEN** 证书存在主图、多图、PDF 或旧单文件信息
- **THEN** 顶部媒体区 SHALL 优先展示证书主图
- **AND** 多图证书 SHALL 按主图优先、其余图片按排序值展示
- **AND** 仅一张图片时 SHALL NOT 强制自动轮播
- **AND** PDF 或未知文件类型 SHALL 使用稳定占位
- **AND** 文件缺失、图片加载失败或 PDF 打开失败 SHALL NOT 阻断证书文字信息浏览。

#### Scenario: 品牌入口
- **WHEN** 证书详情关联公开可访问品牌
- **THEN** 详情页 SHALL 在独立品牌入口面板展示品牌名称和清晰品牌入口
- **AND** 点击品牌入口 SHALL 使用 `brandId` 或既有品牌路由参数进入品牌主页
- **AND** 品牌不可公开或已停用时证书详情 SHALL 默认不可公开。

### Requirement: 公开证书详情 API
系统 SHALL 提供公开证书详情 API 或等价后端能力，用于返回单张公开证书详情页所需数据。详情响应 SHALL 使用统一响应 envelope，并 SHALL 由后端过滤隐藏、软删除和不可公开品牌证书。

#### Scenario: 查询公开证书详情
- **WHEN** 小程序请求 `GET /api/v1/miniapp/certificates/{certificateId}` 或等价公开详情接口
- **THEN** 后端 SHALL 返回统一响应 envelope
- **AND** 响应 SHALL 包含证书 ID、证书名称、证书类型、品牌 ID、品牌名称、证书编号、发证机构、有效期、有效状态、公开备注说明、公开说明、图片组或文件信息、分享信息中可用字段
- **AND** 公开备注说明空值或 `null` / `undefined` 占位值 SHALL 作为空值返回或展示为安全占位
- **AND** 响应 SHALL 支持旧单文件证书与多图证书兼容展示。

#### Scenario: 过滤不可公开证书详情
- **WHEN** 证书被隐藏、软删除、不存在或所属品牌不可公开
- **THEN** 后端 SHALL NOT 返回完整证书详情
- **AND** 小程序 SHALL 展示“证书暂不可查看”或等价状态
- **AND** 响应和页面 SHALL NOT 暴露后台备注、审计字段、内部用户字段、原始对象 Key、本机路径、Authorization header、Cookie、密钥或 `.env` 内容。

#### Scenario: 返回安全文件 URL
- **WHEN** 详情响应包含图片、PDF 或分享图
- **THEN** URL SHALL 来自后端授权、公开安全 URL 或对象存储适配层生成结果
- **AND** 小程序 SHALL NOT 直接使用未授权 object key 拼接对象存储地址
- **AND** 详情响应 SHALL NOT 暴露 bucket 名称、内部 endpoint 或原始 object key。

### Requirement: 证书详情分享
小程序证书详情页 SHALL 支持微信原生分享或等价分享能力，并保证分享路径可直达同一张证书详情。

#### Scenario: 分享证书详情
- **WHEN** 用户通过微信原生分享能力分享证书详情页
- **THEN** 小程序 SHALL 提供微信原生分享数据或等价分享能力
- **AND** 分享标题 SHALL 包含证书名称和品牌名称
- **AND** 分享路径 SHALL 携带 `certificateId` 和来源参数
- **AND** 分享图 SHALL 优先使用证书主图，主图缺失时使用稳定占位或品牌兜底图
- **AND** 页面 SHALL NOT 提供底部固定“分享证书”按钮
- **AND** 分享内容 SHALL NOT 包含内部备注、后台状态或不可公开字段。

#### Scenario: 分享直达证书详情
- **WHEN** 用户从微信分享卡片直达证书详情页
- **THEN** 页面 SHALL 按同一公开详情契约加载证书
- **AND** 无上一页页面栈时返回入口 SHALL 安全进入首页、证书列表或项目确认的安全入口
- **AND** 分享直达失败 SHALL 展示可恢复错误状态。

### Requirement: 证书详情视觉、导航与设备验收
小程序证书详情页 SHALL 延续用户侧深色高端展示体系，并满足自定义导航、移动端视口和设备 evidence 验收要求。

#### Scenario: 视觉与范围控制
- **WHEN** 用户查看证书详情页
- **THEN** 页面 SHALL 使用与现有小程序页面一致的深色背景、卡片层、主文字、辅助文字和品牌金语义
- **AND** 顶部媒体区 SHALL 采用大图布局
- **AND** 页面 SHALL NOT 使用小卡片包裹主媒体
- **AND** 页面 SHALL NOT 提供底部固定“预览文件”按钮
- **AND** 页面 SHALL NOT 展示价格、收藏、推荐、购物车、购买、询价、库存或促销模块。

#### Scenario: 自定义导航验收
- **WHEN** 证书详情页使用全局自定义导航栏
- **THEN** 页面 SHALL 按 `docs/knowledge-base/best-practices/miniapp-custom-navigation.md` 验收状态栏、胶囊 reserve、返回兜底、页面 offset 和分享直达路径
- **AND** 首屏、加载态、空状态、错误态和网络失败提示 SHALL NOT 被顶部导航或底部安全区遮挡。

#### Scenario: 视口与设备 evidence
- **WHEN** 团队验收证书详情页
- **THEN** 验收 SHALL 覆盖 320、375、430 pt DevTools 视口
- **AND** 页面 SHALL 无横向滚动、内容重叠、关键文字溢出或按钮不可达
- **AND** 真机不可用时 SHALL 标记 blocked 或 follow_up，不得写作真机通过。

### Requirement: 证书详情埋点与隐私
系统 SHALL 记录证书详情核心浏览行为，并避免记录与证书浏览无关的个人敏感信息。

#### Scenario: 证书详情行为埋点
- **WHEN** 用户浏览、切换媒体、预览图片、打开文件、点击品牌、分享或遇到加载失败
- **THEN** 系统 SHALL 记录详情曝光、媒体切换、图片预览、文件打开、品牌点击、分享点击和加载失败事件中适用事件
- **AND** 埋点参数 SHALL 包含 terminal、certificateId、brandId、certificateType、sourcePage、sourceModule 和 requestId 中可用字段。

#### Scenario: 证书详情埋点隐私边界
- **WHEN** 系统记录证书详情相关日志或埋点
- **THEN** 日志和埋点 SHALL NOT 记录手机号、地址、客户姓名、Authorization header、Cookie、密钥、`.env` 内容、未脱敏个人隐私或对象存储原始 Key。

### Requirement: 证书详情接口与测试同步
证书详情页涉及的 API、数据库、OpenAPI、Orval、小程序服务层、文档和测试 SHALL 保持同步。

#### Scenario: 契约同步
- **WHEN** 新增或调整公开证书详情接口、响应字段、证书图片组字段或分享字段
- **THEN** 后端 Schema、OpenAPI、Orval 或小程序服务层、API 文档和集成测试 SHALL 同步更新
- **AND** 若新增数据库字段或证书图片关系字段，SQLite/MySQL schema、migration、数据库文档和测试 SHALL 同步更新。

#### Scenario: 测试覆盖
- **WHEN** 证书详情页实现完成
- **THEN** 后端测试 SHALL 覆盖详情成功、不可公开过滤、旧单文件兼容、多图主图排序和安全文件 URL
- **AND** 小程序静态或页面测试 SHALL 覆盖详情路由、列表进入详情、媒体状态、分享、品牌入口、异常状态和范围外能力未出现
- **AND** 设备 evidence SHALL 覆盖正常、加载、错误、无图/PDF 和分享直达状态。

