## MODIFIED Requirements

### Requirement: SKU 图片与视频上传

系统 MUST 支持 SKU 图片与视频经后端授权上传至 MinIO。图片 MIME MUST 包含 JPG、PNG、WebP；视频 MUST 支持 MP4（见 `rules/media.md`）。前端 MUST NOT 直连未授权对象存储。每个 SKU MUST 支持多张图片并指定一张主图；MUST 支持多个视频。SKU 弹窗商品图片区 MUST 支持移除任意已添加图片。设置某张图片为主图后，该图片 MUST 立即成为唯一主图并移动到图片列表第一位；移除当前主图后，如果仍有其它图片，系统 MUST 自动选择新主图并将其置于第一位。图片移除 MUST 只解除 SKU 关联，不触发对象存储物理删除。当主图原图对象存在时，系统 SHOULD 为列表场景生成同目录文件名差异化缩略图，并 SHALL 支持历史公开 SKU 主图缩略图回填。SKU 图片上传链路 SHALL 生成真实同目录缩略图；对于尺寸大于缩略图目标尺寸的支持图片，`.thumb` 对象 SHALL 经过后端 resize / compress 处理，SHALL NOT 只是原图 bytes 的复制品。

#### Scenario: SKU 编码稳定

- **WHEN** 运营更新商品名称、品牌、类目、规格、价格、图片或视频
- **THEN** 系统 MUST 保持既有 `sku_code` 不变

#### Scenario: 主图标记

- **WHEN** SKU 有多张图片且其中一张 `is_main=1`
- **THEN** 列表与详情 MUST 将该图作为主图缩略图

#### Scenario: SKU 图片上传生成真实缩略图

- **GIVEN** 管理端上传一张尺寸大于缩略图目标尺寸的 SKU 图片
- **WHEN** 上传接口成功写入原图对象
- **THEN** 后端 SHALL 在同目录写入 `.thumb` 缩略图对象
- **AND** 缩略图 SHALL 保持比例并限制在约定最大宽高内
- **AND** 缩略图 bytes SHALL NOT 与原图 bytes 完全一致
- **AND** 上传响应中的原图 `/media/{object_key}` SHALL 继续可读取。

#### Scenario: 缩略图生成失败边界

- **GIVEN** 原图上传成功但图片解码、resize 或重编码失败
- **WHEN** 后端处理 SKU 图片上传结果
- **THEN** 系统 SHALL 按 Change 实现中约定的失败策略返回错误或记录可观测告警
- **AND** 系统 SHALL NOT 产生原图不可访问、数据库引用半成功或前端直连对象存储的状态
- **AND** Task Trace 或日志 SHOULD 能定位缩略图处理阶段且不得泄露敏感信息。

#### Scenario: 历史 SKU 主图缩略图重生成

- **GIVEN** 存量 SKU 主图原图存在且 `.thumb` 对象缺失或疑似与原图相同
- **WHEN** 运维执行历史缩略图重生成 apply
- **THEN** 系统 SHALL 生成真实同目录 `.thumb` 对象
- **AND** 主图顺序、主图唯一、图片移除关联语义和 SKU 公开状态 SHALL 保持不变
- **AND** 重生成脚本 SHALL 支持 dry-run 和幂等执行。
