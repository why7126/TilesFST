# object-storage Delta

## MODIFIED Requirements

### Requirement: 媒体对象必须可受控读取

系统 SHALL 通过后端受控接口读取媒体对象，保护对象存储访问边界，并 SHALL 支持图片缓存、列表缩略图、媒体观测和视频 Range 请求。商品列表缩略图、品牌图片缩略图、Banner 图片缩略图和图片类品牌证书缩略图 SHALL 与原图位于同一对象目录或等价可追溯对象路径，并 SHALL 通过文件名差异区分缩略图与原图；历史 `thumbnails/` 前缀 MAY 作为兼容读取或迁移来源，但新生成的列表缩略图 SHALL NOT 依赖 `thumbnails/default/tiles/pending/` 作为最终存储位置。系统 SHALL 生成真实轻量缩略图：对于尺寸大于缩略图目标尺寸的支持图片，缩略图 SHALL 经过后端图片处理生成，像素宽高 SHALL 小于或等于约定最大宽高，且 SHALL NOT 只是原图 bytes 的复制品。系统 SHALL 支持全局缩略图体积目标上限 effective 配置：当 `media.thumbnail_max_size_kb` 为 `0` 时 SHALL 保持当前不限制体积的生成模式；当该值为正整数时，SKU 图片、SKU 暂存图片正式化、品牌 Logo、Banner 图片、品牌证书图片和维护任务重生成的图片缩略图 SHALL 读取同一全局策略，并通过质量递减、必要时尺寸收缩等方式尽量不超过目标体积。无法达到目标体积时 SHALL NOT 阻断原图上传或业务保存，且 SHALL 记录 warning 或可复核失败原因。缩略图 Key / URL 规则 SHALL 保持同目录 `.thumb` 推导约定稳定，不得因体积上限配置要求新增业务表 `thumbnail_key` 字段或改变客户端受控 `/media/...` 读取方式。针对 `BUG-0116-prod-media-historical-object-drift`，系统 SHALL 支持对 SKU 商品图片、品牌 Logo 和品牌证书图片的历史缩略图漂移进行 dry-run 审计、受控回填、二次审计和幂等重复执行；独立历史缩略图重生成任务 SHALL 覆盖 SKU、品牌 Logo 和品牌证书图片三类对象。针对 `BUG-0126-miniapp-brand-media-slow-load`，系统 SHALL 将品牌列表 Banner、品牌 Logo、品牌分类商品卡片主图和图片类品牌证书纳入品牌链路媒体性能审计。

#### Scenario: BUG-0126 品牌链路媒体审计覆盖

- **GIVEN** 生产等价数据库与对象存储配置可用
- **WHEN** 运维执行 BUG-0126 品牌链路媒体性能 dry-run 审计
- **THEN** 输出 SHALL 覆盖品牌列表 Banner、品牌 Logo、品牌分类商品卡片主图和图片类品牌证书
- **AND** 输出 SHALL 分别统计原图存在、缩略图存在、缩略图 bytes、原图 bytes、疑似复制原图、疑似体积无收益、需要生成或重生成、跳过、失败原因和重试候选摘要
- **AND** dry-run SHALL NOT 写数据库或对象存储
- **AND** 输出 SHALL NOT 包含生产密钥、数据库 DSN、Authorization header、Cookie、`.env` 内容、本机绝对路径或真实客户数据。

#### Scenario: BUG-0126 历史缩略图回填和二次审计

- **GIVEN** BUG-0126 dry-run 已确认需要回填或重生成的品牌链路图片
- **WHEN** 运维在完成备份后执行受控 apply
- **THEN** 系统 SHALL 仅为需要处理且原图可读的图片生成或重生成同目录 `.thumb` 缩略图
- **AND** 缩略图 SHALL 由后端图片处理逻辑生成，SHALL NOT 只是原图 bytes 复制品
- **AND** 重复执行 SHALL 保持幂等，不破坏已合格缩略图
- **AND** 二次审计 SHALL 输出剩余缺失、失败、blocked 和已达标摘要。

#### Scenario: /media 图片读取缓存与回退可观测

- **WHEN** 小程序通过 `/media/{object_key}` 请求品牌链路图片或 `.thumb` 缩略图
- **THEN** 后端或网关 SHALL 返回适合图片资源的缓存头、网关缓存或 CDN 策略证据
- **AND** 媒体读取日志或等价观测 SHALL 能区分请求 key、实际 resolved key、content length、MIME 和耗时
- **AND** 当 `.thumb` 缺失并回退原图时 SHALL 记录回退事件
- **AND** 验收 SHALL NOT 将回退原图视为缩略图性能通过。
