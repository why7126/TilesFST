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

#### Scenario: 图片证书返回受控缩略图
- **GIVEN** 公开证书列表中存在图片类品牌证书，且证书存在可信主图记录、可信 `file_key` 或可兼容旧单文件图片来源
- **WHEN** 小程序请求 `GET /api/v1/miniapp/certificates`
- **THEN** 后端 SHALL 为该图片证书返回非空 `thumbnail_url` 或等价受控卡片小图 URL
- **AND** `thumbnail_url` SHALL 指向后端受控 `/media/` URL、对象存储适配层生成的公开安全 URL 或等价受控读取 URL
- **AND** URL 语义 SHALL 对应同目录 `.thumb.webp` 或等价轻量缩略图
- **AND** 响应 SHALL NOT 暴露 `file_key`、raw object key、bucket、内部 endpoint、Authorization header、Cookie、密钥、`.env` 内容或本机路径。

#### Scenario: 图片证书缺少可信缩略图时保持占位语义
- **GIVEN** 图片类证书缺少可信媒体 key、缩略图对象不存在、对象不可读或媒体类型证据不足
- **WHEN** 后端生成公开证书列表响应
- **THEN** 后端 MAY 返回 `thumbnail_url: null`
- **AND** 小程序 SHALL 展示统一“证书”占位或受控失败态
- **AND** 小程序 SHALL NOT 使用 `file_url`、原图、原始文件 URL 或 raw object URL 作为列表卡片图片 fallback。

### Requirement: 证书卡片展示

小程序 SHALL 使用移动端两列证书卡片展示公开证书摘要，并对图片、PDF 和缺失文件稳定降级。图片证书卡片 SHALL 优先使用后端受控真实缩略图或等价卡片小图；预览或详情入口 SHALL 使用原图、原文件或等价安全引用。证书卡片缺少缩略图、缩略图不可读或图片加载失败时 SHALL 展示统一占位或受控失败态，SHALL NOT 在卡片图片 `src` 中 fallback 到 `file_url`、原图或原始文件 URL。

#### Scenario: 展示证书文件占位

- **WHEN** 证书文件为图片、PDF、缺失或未知类型
- **THEN** 图片证书 SHALL 优先展示稳定比例真实缩略图
- **AND** PDF 证书 SHALL 展示统一 PDF 占位
- **AND** 文件缺失、类型未知、缩略图加载失败或图片加载失败时 SHALL 展示统一占位或受控失败态
- **AND** 卡片展示 SHALL NOT 因缺少缩略图而请求 `file_url`、原图或原始文件 URL
- **AND** 页面 SHALL NOT 出现浏览器破图、卡片高度跳动或文本遮挡
- **AND** 证书详情页、图片预览或文件打开 SHALL NOT 被强制降级为卡片缩略图。

#### Scenario: 证书卡片缩略图字段一致

- **WHEN** 小程序公开证书列表响应提供缩略图 URL、文件类型和等价卡片媒体引用
- **THEN** 证书列表卡片 SHALL 优先读取缩略图 URL 或等价小图引用
- **AND** 证书列表接口 SHOULD NOT 为每个列表 item 下发未被列表卡片渲染使用的原文件 URL
- **AND** 缩略图不可用时 SHALL 按统一策略展示 PDF 占位、缺失占位或其他稳定占位
- **AND** 小程序 SHALL NOT 在缩略图可用或缺失时直接使用原图或原文件 URL 作为图片证书卡片展示图。
