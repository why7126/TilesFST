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
系统 SHALL 提供公开证书列表 API 或等价后端能力，仅返回允许在小程序展示的证书数据。

#### Scenario: 查询公开证书列表
- **WHEN** 小程序请求 `GET /api/v1/miniapp/certificates` 或等价公开接口
- **THEN** 后端 SHALL 返回统一响应 envelope
- **AND** 响应 SHALL 包含证书列表和分页信息
- **AND** 列表项 SHALL 包含证书 ID、证书名称、证书类型、证书编号或发证机构、品牌 ID、品牌名称、文件 URL、文件名、MIME、有效期字段和有效状态。

#### Scenario: 过滤非公开证书
- **WHEN** 后端生成公开证书列表响应
- **THEN** 后端 SHALL 排除隐藏证书、软删除证书和所属品牌不可公开的证书
- **AND** 响应 SHALL NOT 暴露后台备注、审计字段、内部用户字段、原始对象 Key、Authorization header、Cookie、密钥或 `.env` 内容。

#### Scenario: 证书列表排序稳定
- **WHEN** 小程序请求分页或加载更多证书
- **THEN** 后端 SHALL 使用稳定排序返回结果
- **AND** 翻页或加载更多 SHALL NOT 出现重复、漏项或明显顺序跳变。

### Requirement: 证书卡片展示
小程序 SHALL 使用移动端两列证书卡片展示公开证书摘要，并对图片、PDF 和缺失文件稳定降级。

#### Scenario: 展示证书摘要
- **WHEN** 证书列表存在公开证书
- **THEN** 每行 SHALL 展示 2 个证书卡片
- **AND** 每张证书卡片 SHALL 仅展示证书名称、品牌名称和证书类型作为文本信息
- **AND** 页面 SHALL NOT 在卡片文本区展示搜索入口、筛选入口、证书编号、发证机构、有效期或有效状态。

#### Scenario: 展示证书文件占位
- **WHEN** 证书文件为图片、PDF、缺失或未知类型
- **THEN** 图片证书 SHALL 展示稳定比例缩略图
- **AND** PDF 证书 SHALL 展示统一 PDF 占位
- **AND** 文件缺失、类型未知或图片加载失败时 SHALL 展示统一占位
- **AND** 页面 SHALL NOT 出现浏览器破图、卡片高度跳动或文本遮挡。

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
小程序 SHALL 为公开证书提供图片或 PDF 文件预览能力，并在预览失败时稳定降级。

#### Scenario: 图片证书预览
- **WHEN** 用户点击图片证书缩略图、卡片主区域或查看入口
- **THEN** 小程序 SHALL 使用图片预览能力展示证书图片
- **AND** 预览失败时 SHALL 展示稳定错误提示
- **AND** 用户 SHALL 能返回证书列表继续浏览。

#### Scenario: PDF 证书预览
- **WHEN** 用户点击 PDF 证书
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

