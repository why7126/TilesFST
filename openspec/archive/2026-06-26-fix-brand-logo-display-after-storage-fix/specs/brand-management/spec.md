# brand-management Specification Delta

## MODIFIED Requirements

### Requirement: 品牌 Logo 上传

系统 MUST 支持品牌 Logo 经后端授权上传至 MinIO 单桶 `MINIO_BUCKET`，MIME 类型 MUST 包含 JPG、PNG、WebP。`logo_object_key` MUST 存于 `brands` 表；前端 MUST NOT 直连未授权对象存储。上传响应与品牌列表/详情响应 MUST 提供可被 Web 客户端实际加载的 `url`、`logo_url` 或等价 `preview_url`，并 MUST 符合对象存储单桶与标准业务前缀策略。系统 MUST NOT 仅将品牌 Logo 保存到本地 `UPLOAD_DIR` 后即视为上传成功。对象存储写入链路修复后，品牌列表页和品牌编辑弹窗 MUST 仍能通过后端受控读取或安全 URL 展示 Logo；历史 `logo_object_key` MUST 有明确兼容、迁移或重新上传策略。

#### Scenario: 上传 Logo 成功

- **WHEN** `admin` 或 `employee` 上传合法图片至品牌上传端点
- **THEN** 系统返回 object_key
- **AND** 系统 MUST 将对象写入 `MINIO_BUCKET`
- **AND** object_key MUST 使用 `original/` 标准前缀
- **AND** 系统返回可被浏览器实际加载的 URL 引用
- **AND** 创建/更新品牌时可写入 `logo_object_key`

#### Scenario: 品牌列表返回可展示 Logo

- **GIVEN** 品牌记录存在 `logo_object_key`
- **WHEN** `admin` 或 `employee` 请求 `GET /api/v1/admin/brands`
- **THEN** 响应中的品牌对象 MUST 包含可加载的 `logo_url` 或等价预览 URL
- **AND** Web 客户端 MUST 能用该 URL 展示 Logo
- **AND** 图片加载失败时 Web 客户端 MUST 展示稳定 fallback，不得造成布局跳动

#### Scenario: 编辑品牌回显 Logo

- **GIVEN** 品牌记录存在 `logo_object_key`
- **WHEN** `admin` 或 `employee` 请求品牌详情或打开编辑弹窗所需数据
- **THEN** 系统 MUST 提供可加载的 Logo URL
- **AND** Web 客户端 MUST 能回显当前 Logo

#### Scenario: 新上传 Logo 保存后仍可见

- **WHEN** `admin` 或 `employee` 在品牌编辑弹窗上传并保存新的 Logo
- **THEN** 弹窗预览 MUST 立即显示新 Logo
- **AND** 关闭并重新打开编辑弹窗后 MUST 回显新 Logo
- **AND** 刷新品牌列表后 MUST 展示新 Logo

#### Scenario: 历史 Logo 数据兼容

- **GIVEN** 品牌记录存在对象存储修复前写入的 `logo_object_key`
- **WHEN** 系统展示品牌列表或编辑弹窗
- **THEN** 系统 MUST 尝试按当前媒体读取策略解析该 key
- **AND** 若对象不存在或不可读取，系统 MUST 使用稳定 fallback
- **AND** 修复说明 MUST 记录是否需要重新上传或执行迁移

#### Scenario: 非法 MIME 被拒绝

- **WHEN** 上传非 JPG/PNG/WebP 文件
- **THEN** 系统 MUST 返回 HTTP 400
- **AND** 错误码 MUST 表示文件类型不允许

#### Scenario: 媒体访问安全

- **WHEN** 用户请求品牌 Logo 媒体 URL
- **THEN** 系统 MUST 校验 object_key 或签名有效性
- **AND** MUST 从 MinIO 受控读取对象或返回安全签名 URL
- **AND** MUST 防止路径穿越、绝对路径读取和内部路径泄露
- **AND** MUST NOT 暴露真实 AccessKey、SecretKey 或未授权对象存储地址
