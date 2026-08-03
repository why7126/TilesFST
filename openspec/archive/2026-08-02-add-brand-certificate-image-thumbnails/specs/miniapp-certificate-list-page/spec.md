## MODIFIED Requirements

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
小程序 SHALL 使用移动端两列证书卡片展示公开证书摘要，并对图片、PDF 和缺失文件稳定降级。图片证书卡片 SHOULD 优先使用后端受控真实缩略图；预览或详情入口 SHALL 使用原图、原文件或等价安全引用。

#### Scenario: 展示证书摘要
- **WHEN** 证书列表存在公开证书
- **THEN** 每行 SHALL 展示 2 个证书卡片
- **AND** 每张证书卡片 SHALL 仅展示证书名称、品牌名称和证书类型作为文本信息
- **AND** 页面 SHALL NOT 在卡片文本区展示搜索入口、筛选入口、证书编号、发证机构、有效期或有效状态。

#### Scenario: 展示证书文件占位
- **WHEN** 证书文件为图片、PDF、缺失或未知类型
- **THEN** 图片证书 SHALL 优先展示稳定比例真实缩略图
- **AND** PDF 证书 SHALL 展示统一 PDF 占位
- **AND** 文件缺失、类型未知、缩略图加载失败或图片加载失败时 SHALL 展示统一占位或回退原图
- **AND** 页面 SHALL NOT 出现浏览器破图、卡片高度跳动或文本遮挡。

#### Scenario: 证书卡片媒体安全
- **WHEN** 小程序展示证书图片、缩略图或 PDF 占位
- **THEN** 图片与文件 URL SHALL 是公开安全 URL 或后端授权 URL
- **AND** 小程序 SHALL NOT 暴露未授权对象存储直连地址、原始 object key、Authorization header 或 Cookie。
