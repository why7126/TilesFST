## MODIFIED Requirements

### Requirement: 品牌 Logo 上传
系统 MUST 支持品牌 Logo 经后端授权上传至 MinIO 单桶 `MINIO_BUCKET`，MIME 类型 MUST 包含 JPG、PNG、WebP。`logo_object_key` MUST 存于 `brands` 表；前端 MUST NOT 直连未授权对象存储。上传响应与品牌列表/详情响应 MUST 提供可被 Web 客户端实际加载的 `url`、`logo_url`、`thumbnail_url` 或等价 `preview_url`，并 MUST 符合对象存储单桶与标准业务前缀策略。系统 MUST 为新上传品牌图片生成真实轻量缩略图，品牌列表和小图预览 SHOULD 优先使用缩略图，原图预览 SHOULD 使用原图或原始受控 URL。管理后台品牌列表 Logo 列 MUST 将有效 Logo URL 渲染为图片或缩略图，MUST NOT 将 URL、对象 key、文件名或普通文本字段值作为用户可见文本展示。系统 MUST NOT 仅将品牌 Logo 保存到本地 `UPLOAD_DIR` 后即视为上传成功。对象存储写入链路修复后，品牌列表页和品牌编辑弹窗 MUST 仍能通过后端受控读取或安全 URL 展示 Logo；历史 `logo_object_key` MUST 有明确兼容、迁移、缩略图补齐或重新上传策略。

#### Scenario: 品牌列表返回并渲染可展示 Logo
- **GIVEN** 品牌记录存在 `logo_object_key`
- **WHEN** `admin` 或 `employee` 请求 `GET /api/v1/admin/brands` 并打开管理后台品牌列表
- **THEN** 响应中的品牌对象 MUST 包含可加载的 `logo_url`、`thumbnail_url` 或等价预览 URL
- **AND** Web 客户端 MUST 在品牌列表 Logo 列用该 URL 渲染图片或缩略图
- **AND** 列表小图 SHOULD 优先使用缩略图
- **AND** Web 客户端 MUST NOT 在 Logo 列直接显示图片 URL、对象 key、文件名或普通文本字段值
- **AND** 图片加载失败时 Web 客户端 MUST 展示稳定 fallback，不得造成布局跳动。

#### Scenario: 品牌列表未上传 Logo 占位
- **GIVEN** 品牌记录不存在 `logo_object_key` 或没有可展示 Logo URL
- **WHEN** `admin` 或 `employee` 打开管理后台品牌列表
- **THEN** Web 客户端 MUST 在 Logo 列展示设计系统内的合理占位状态
- **AND** MUST NOT 展示空白错位、破图图标、调试文案、对象 key 或内部路径。
