## MODIFIED Requirements

### Requirement: 媒体对象必须可受控读取

系统 SHALL 通过后端受控接口读取媒体对象，保护对象存储访问边界，并 SHALL 支持图片缓存、列表缩略图、媒体观测和视频 Range 请求。商品列表缩略图、品牌图片缩略图、Banner 图片缩略图和图片类品牌证书缩略图 SHALL 与原图位于同一对象目录或等价可追溯对象路径，并 SHALL 通过文件名差异区分缩略图与原图；历史 `thumbnails/` 前缀 MAY 作为兼容读取或迁移来源，但新生成的列表缩略图 SHALL NOT 依赖 `thumbnails/default/tiles/pending/` 作为最终存储位置。系统 SHALL 生成真实轻量缩略图：对于尺寸大于缩略图目标尺寸的支持图片，缩略图 SHALL 经过后端图片处理生成，像素宽高 SHALL 小于或等于约定最大宽高，且 SHALL NOT 只是原图 bytes 的复制品。系统 SHALL 支持全局缩略图体积目标上限 effective 配置：当 `media.thumbnail_max_size_kb` 为 `0` 时 SHALL 保持当前不限制体积的生成模式；当该值为正整数时，SKU 图片、SKU 暂存图片正式化、品牌 Logo、Banner 图片、品牌证书图片和维护任务重生成的图片缩略图 SHALL 读取同一全局策略，并通过质量递减、必要时尺寸收缩等方式尽量不超过目标体积。无法达到目标体积时 SHALL NOT 阻断原图上传或业务保存，且 SHALL 记录 warning 或可复核失败原因。缩略图 Key / URL 规则 SHALL 保持同目录 `.thumb` 推导约定稳定，不得因体积上限配置要求新增业务表 `thumbnail_key` 字段或改变客户端受控 `/media/...` 读取方式。针对 `BUG-0116-prod-media-historical-object-drift`，系统 SHALL 支持对 SKU 商品图片、品牌 Logo 和品牌证书图片的历史缩略图漂移进行 dry-run 审计、受控回填、二次审计和幂等重复执行；独立历史缩略图重生成任务 SHALL 覆盖 SKU、品牌 Logo 和品牌证书图片三类对象。

#### Scenario: BUG-0116 历史缩略图审计覆盖三类对象

- **GIVEN** 生产等价数据库与对象存储配置可用
- **WHEN** 运维执行 BUG-0116 历史缩略图审计 dry-run
- **THEN** 输出 SHALL 分别统计 SKU 商品图片、品牌 Logo 和品牌证书图片
- **AND** 输出 SHALL 包含原图存在、缩略图存在、疑似同 size、疑似同 bytes、需要生成或重生成、跳过、失败原因和重试候选摘要
- **AND** dry-run SHALL NOT 写数据库或对象存储
- **AND** 输出 SHALL NOT 包含生产密钥、数据库 DSN、Authorization header、Cookie、`.env` 内容、本机绝对路径或真实客户数据。

#### Scenario: BUG-0116 历史缩略图回填幂等

- **GIVEN** BUG-0116 dry-run 已确认可回填的 SKU 商品图片、品牌 Logo 或品牌证书图片
- **WHEN** 运维在完成备份后执行受控 apply
- **THEN** 系统 SHALL 仅为需要处理且原图可读的图片生成或重生成同目录 `.thumb` 缩略图
- **AND** 缩略图 SHALL 由后端图片处理逻辑生成，SHALL NOT 只是原图 bytes 复制品
- **AND** 重复执行 SHALL 保持幂等，不破坏已合格缩略图
- **AND** 对原图缺失、MIME 不支持、对象存储不可用或 provider 能力不足的记录 SHALL 输出 fail 或 blocked 摘要。

#### Scenario: 新上传图片按全局体积目标生成缩略图

- **GIVEN** `media.thumbnail_max_size_kb` effective 值为 `20`
- **WHEN** `admin` 上传 SKU 图片、品牌 Logo、Banner 图片或图片类品牌证书
- **THEN** 上传接口 SHALL 先写入原图对象
- **AND** 后续生成的同目录 `.thumb` 缩略图 SHALL 读取全局体积目标并尽量不超过 20KB
- **AND** 上传响应 SHALL 继续返回既有 `object_key`、`url`、`thumbnail_key` 和 `thumbnail_url` 语义
- **AND** 客户端 SHALL 继续通过 `/media/{object_key}` 或 `/media/{thumbnail_key}` 受控读取对象。

#### Scenario: 缩略图未达标不阻断上传

- **GIVEN** `media.thumbnail_max_size_kb` effective 值为正整数
- **AND** 上传图片因透明 PNG、高细节纹理或编码限制无法达到目标体积
- **WHEN** 缩略图生成过程完成
- **THEN** 原图上传和业务保存 SHALL NOT 失败
- **AND** 系统 SHALL 写入当前最佳缩略图或按既有失败策略跳过缩略图
- **AND** 系统 SHALL 记录 warning、任务链路信息或维护任务失败原因，便于后续排查。

#### Scenario: 缩略图 Key 规则保持稳定

- **GIVEN** 原图对象 Key 为 `images/default/tiles/1/main.webp`
- **WHEN** 系统生成缩略图
- **THEN** 缩略图 Key SHALL 继续为 `images/default/tiles/1/main.thumb.webp` 或等价同目录 `.thumb` 规则
- **AND** 系统 SHALL NOT 因体积上限配置新增业务表 `thumbnail_key`
- **AND** 已有展示端基于原图 Key 推导 `.thumb` URL 的逻辑 SHALL 保持兼容。
