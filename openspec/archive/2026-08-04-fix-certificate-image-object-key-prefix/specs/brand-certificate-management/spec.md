## MODIFIED Requirements

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
