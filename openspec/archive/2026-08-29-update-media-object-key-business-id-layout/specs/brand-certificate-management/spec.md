## MODIFIED Requirements

### Requirement: 品牌证书文件上传与预览

品牌证书文件上传 MUST 通过后端授权上传接口完成，MUST 校验 MIME Type、扩展名、文件大小和对象 Key 前缀。证书上传 MUST 支持 PDF、JPG、PNG、WebP，PDF 等文档类证书 MUST 按文件类资源保存，图片类证书 MUST 按图片类资源保存。图片类证书 MUST 支持多图上传、唯一主图、缩略图 URL、原图 URL 和受控预览；PDF 证书 MUST 支持受控 URL 预览。上传响应与证书详情响应 MUST NOT 暴露对象存储凭据、未授权 raw URL、本机路径或用户原始文件名作为对象 key。

新上传证书图片在 `certificate_id` 已存在时 MUST 写入 `images/default/brand-certificates/{certificate_id}/{uuid}.{ext}`；新上传证书 PDF 或文档在 `certificate_id` 已存在时 MUST 写入 `files/default/brand-certificates/{certificate_id}/{uuid}.{ext}`。证书创建前上传的图片和文件 MUST 使用对应 pending 目录，并在证书创建成功后 formalize 到证书业务对象 id 目录。历史证书图片和文件 key MUST 保持读取兼容，迁移时必须保持图片与 PDF/文档分流。

#### Scenario: 上传证书多图图片

- **WHEN** 已授权管理端用户上传合法 JPG、PNG 或 WebP 证书图片
- **THEN** 系统 MUST 返回可用于证书图片数组保存的文件引用、受控读取 URL、缩略图引用、文件名、MIME 和大小
- **AND** 当 `certificate_id` 已存在时图片类证书对象 Key MUST 使用 `images/default/brand-certificates/{certificate_id}/`
- **AND** 当 `certificate_id` 尚未存在时图片类证书对象 Key MUST 使用证书图片 pending 目录
- **AND** 缩略图对象 Key MUST 与原图保持同一证书目录或等价可追溯目录
- **AND** 上传控件 MUST 在同一会话中即时回显图片卡片。

#### Scenario: 上传证书 PDF 或文档

- **WHEN** 已授权管理端用户上传合法 PDF 或文档类证书文件
- **THEN** 系统 MUST 按文件类资源保存并返回受控预览 URL
- **AND** 当 `certificate_id` 已存在时 object key MUST 使用 `files/default/brand-certificates/{certificate_id}/`
- **AND** PDF 或文档类证书 MUST NOT 生成图片缩略图或展示图
- **AND** 历史 `files/default/brand-certificates/` 文件 key 在迁移前 MUST 继续可读。

#### Scenario: 证书保存后正式化

- **GIVEN** 新建证书表单引用 pending 图片或文件
- **WHEN** 证书创建成功并获得 `certificate_id`
- **THEN** 系统 MUST 将证书图片 formalize 到 `images/default/brand-certificates/{certificate_id}/`
- **AND** 系统 MUST 将证书 PDF 或文档 formalize 到 `files/default/brand-certificates/{certificate_id}/`
- **AND** 证书主图、图片排序、文件预览和历史单文件兼容语义 MUST 保持不变。
