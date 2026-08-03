## MODIFIED Requirements

### Requirement: SKU 图片与视频上传

系统 MUST 支持 SKU 图片与视频经后端授权上传至 MinIO。图片 MIME MUST 包含 JPG、PNG、WebP；视频 MUST 支持 MP4（见 `rules/media.md`）。前端 MUST NOT 直连未授权对象存储。每个 SKU MUST 支持多张图片并指定一张主图；MUST 支持多个视频。SKU 弹窗商品图片区 MUST 支持移除任意已添加图片。设置某张图片为主图后，该图片 MUST 立即成为唯一主图并移动到图片列表第一位；移除当前主图后，如果仍有其它图片，系统 MUST 自动选择新主图并将其置于第一位。图片移除 MUST 只解除 SKU 关联，不触发对象存储物理删除。当主图原图对象存在时，系统 SHOULD 为列表场景生成同目录文件名差异化缩略图，并 SHALL 支持历史公开 SKU 主图缩略图回填。

新建 SKU 前允许图片上传接口暂时返回 `images/default/tiles/pending/...`；但当图片被绑定到 SKU、保存为 SKU 图片或 SKU 发布为公开商品时，系统 MUST 将 pending 图片正式化到可追溯到该 SKU 的正式商品图片目录，或以等价方式保证公开商品主图不长期引用 `images/default/tiles/pending/...`。正式化 MUST 同步处理原图、同目录缩略图和 `tile_images` 数据引用，并 MUST 保持主图唯一、图片顺序和移除关联语义不变。

#### Scenario: SKU 编码稳定

- **WHEN** 运营更新商品名称、品牌、类目、规格、价格、图片或视频
- **THEN** 系统 MUST 保持既有 `sku_code` 不变

#### Scenario: 主图标记

- **WHEN** SKU 有多张图片且其中一张 `is_main=1`
- **THEN** 列表与详情 MUST 将该图作为主图缩略图
- **AND** 同一 SKU MUST NOT 有多张 `is_main=1`（业务层保证唯一）

#### Scenario: 主图缩略图生成

- **WHEN** 管理端上传图片并将其关联为 SKU 主图
- **THEN** 系统 SHOULD 在原图对象写入成功后生成同目录文件名差异化的列表缩略图
- **AND** 缩略图生成失败 SHALL 可观测、可重试，并 SHALL NOT 删除或破坏原图对象
- **AND** 后续公开列表 SHALL NOT 因缩略图生成失败返回已知不可访问的缩略图 URL。

#### Scenario: 新建 SKU pending 主图保存后正式化

- **GIVEN** 管理端新建 SKU 时先上传主图，上传阶段返回 `images/default/tiles/pending/<uuid>.<ext>`
- **WHEN** 用户保存 SKU 且该图片被绑定到新建 SKU
- **THEN** 保存后的 `tile_images.object_key` MUST NOT 继续使用 `images/default/tiles/pending/`
- **AND** 对象 key MUST 位于可追溯到该 SKU 的正式商品图片目录
- **AND** `/media/{object_key}` MUST 可读取该图片。

#### Scenario: 编辑 SKU pending 图片保存后正式化

- **GIVEN** 已存在 SKU
- **WHEN** 用户编辑该 SKU 并提交仍位于 `images/default/tiles/pending/` 的新增图片
- **THEN** 保存后该图片 MUST 被正式化到该 SKU 的正式商品图片目录
- **AND** 再次 GET SKU 详情时 `images[].object_key` MUST 与数据库一致
- **AND** 主图唯一、图片顺序和被移除图片解除关联语义 MUST 保持不变。

#### Scenario: 发布 SKU 不允许公开 pending 主图

- **GIVEN** SKU 已设置主图
- **WHEN** 用户调用发布接口
- **THEN** 发布成功后的公开商品主图 MUST NOT 位于 `images/default/tiles/pending/`
- **AND** 如果主图正式化失败，系统 MUST 阻止发布或回滚到发布前状态
- **AND** 系统 MUST NOT 出现数据库引用已更新但对象不可访问的半成功状态。

#### Scenario: 历史主图缩略图回填

- **GIVEN** 生产或体验版存在公开 SKU 主图
- **WHEN** 运维或管理员执行历史缩略图回填
- **THEN** 系统 SHALL 为原图存在但缩略图缺失的主图补齐同目录缩略图
- **AND** 回填 SHALL 输出总数、成功数、失败数和失败原因摘要
- **AND** 回填日志 SHALL NOT 输出密钥、Authorization header、Cookie、`.env` 内容或本机绝对路径。

#### Scenario: 历史公开 SKU pending 主图迁移

- **GIVEN** 存量公开 SKU 主图仍位于 `images/default/tiles/pending/`
- **WHEN** 运维或管理员执行迁移脚本 dry-run
- **THEN** dry-run MUST 输出待迁移数量、目标 key、缺失对象数量、缩略图处理计划和风险摘要
- **AND** dry-run MUST NOT 写数据库或对象存储
- **WHEN** 运维或管理员执行迁移脚本 apply
- **THEN** 系统 MUST 一致迁移原图、同目录缩略图和 `tile_images` 数据引用
- **AND** 迁移 MUST 可重入，重复执行不得重复复制或破坏已迁移数据。
