## ADDED Requirements

### Requirement: 品牌 Logo 上传

系统 MUST 支持品牌 Logo 经后端授权上传至 MinIO 或受控开发存储，MIME 类型 MUST 包含 JPG、PNG、WebP。`logo_object_key` MUST 存于 `brands` 表；前端 MUST NOT 直连未授权对象存储。上传响应与品牌列表/详情响应 MUST 提供可被 Web 客户端实际加载的 `url`、`logo_url` 或等价 `preview_url`，并 MUST 符合对象存储单桶与业务前缀策略。

#### Scenario: 上传 Logo 成功

- **WHEN** `admin` 或 `employee` 上传合法图片至品牌上传端点
- **THEN** 系统返回 object_key
- **AND** 系统返回可被浏览器实际加载的 URL 引用
- **AND** 创建/更新品牌时可写入 `logo_object_key`

#### Scenario: 品牌列表返回可展示 Logo

- **GIVEN** 品牌记录存在 `logo_object_key`
- **WHEN** `admin` 或 `employee` 请求 `GET /api/v1/admin/brands`
- **THEN** 响应中的品牌对象 MUST 包含可加载的 `logo_url` 或等价预览 URL
- **AND** Web 客户端 MUST 能用该 URL 展示 Logo

#### Scenario: 编辑品牌回显 Logo

- **GIVEN** 品牌记录存在 `logo_object_key`
- **WHEN** `admin` 或 `employee` 请求品牌详情或打开编辑弹窗所需数据
- **THEN** 系统 MUST 提供可加载的 Logo URL
- **AND** Web 客户端 MUST 能回显当前 Logo

#### Scenario: 非法 MIME 被拒绝

- **WHEN** 上传非 JPG/PNG/WebP 文件
- **THEN** 系统 MUST 返回 HTTP 400
- **AND** 错误码 MUST 表示文件类型不允许

#### Scenario: 媒体访问安全

- **WHEN** 用户请求品牌 Logo 媒体 URL
- **THEN** 系统 MUST 校验 object_key 或签名有效性
- **AND** MUST 防止路径穿越、绝对路径读取和内部路径泄露
- **AND** MUST NOT 暴露真实 AccessKey、SecretKey 或未授权对象存储地址
