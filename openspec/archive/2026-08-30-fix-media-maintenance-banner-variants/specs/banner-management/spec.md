## ADDED Requirements

### Requirement: Banner 自定义上传图必须支持历史派生图维护

Banner 自定义上传图 MUST 能被生产媒体维护作业识别和补齐历史派生图。系统 MUST 使用 `banners.image_object_key` 作为 Banner 历史图片候选来源，并 SHOULD 优先限定为 `image_source = 'custom_upload'` 或 `images/default/banners/` 标准目录，避免重复处理引用 SKU 主图、SKU 图册图或品牌 Logo 的 Banner 图片。

#### Scenario: Banner 自定义上传图进入维护候选

- **WHEN** 数据库存在 Banner 自定义上传图
- **AND** `image_object_key` 指向 `images/default/banners/` 下的 JPEG、PNG 或 WebP 原图
- **THEN** 生产媒体维护任务 MUST 将该记录作为历史图片派生图候选
- **AND** 候选来源 MUST 可在脱敏输出中与 SKU、品牌 Logo 和证书来源区分
- **AND** 同一 object key 被多个业务记录引用时 MUST 去重处理。

#### Scenario: Banner 历史派生图补齐不改变配置

- **WHEN** 维护任务补齐 Banner `.thumb.webp` 或 `.display.webp`
- **THEN** 系统 MUST NOT 修改 Banner 标题、展示位置、跳转类型、上下线状态、排序、有效期或 `image_object_key`
- **AND** 系统 MUST NOT 删除 Banner 原图
- **AND** 若 Banner 已迁入业务 id 目录，系统 MAY 生成旧无 id URL 的 `.thumb.webp` 与 `.display.webp` alias 以兼容历史访问路径
- **AND** 管理端和小程序继续通过既有 Banner 配置读取图片 URL。
