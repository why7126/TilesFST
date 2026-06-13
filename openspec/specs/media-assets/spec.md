---
purpose: 媒体资源正式能力规范
content: 规定瓷砖图片、视频、缩略图、处理产物在对象存储中的行为规范
source: AI自动生成，人工确认
update_method: 媒体能力变更完成并归档时更新
note: V5 使用单 Bucket + 对象前缀策略
---

# Capability: Media Assets

## Requirements

### Requirement: 单项目单Bucket存储

系统 SHALL 使用一个 MinIO Bucket 存储本项目所有对象资源。

默认 Bucket 名称 SHALL 由环境变量 `MINIO_BUCKET` 提供。

#### Scenario: 上传瓷砖图片

- GIVEN 系统配置了 `MINIO_BUCKET`
- WHEN 用户上传瓷砖图片
- THEN 系统 SHALL 将原始图片存储到 `original/` 前缀下
- AND 系统 SHALL 将缩略图存储到 `thumbnails/` 前缀下

#### Scenario: 上传瓷砖视频

- GIVEN 系统配置了 `MINIO_BUCKET`
- WHEN 用户上传瓷砖视频
- THEN 系统 SHALL 将原始视频存储到 `videos/` 前缀下
- AND 如生成封面，系统 SHALL 将封面存储到 `videos/covers/` 前缀下
- AND 如生成转码文件，系统 SHALL 将转码结果存储到 `videos/transcoded/` 前缀下

### Requirement: 禁止随意新增业务Bucket

系统 SHALL NOT 为图片、视频、缩略图分别创建独立业务 Bucket，除非 OpenSpec Change 明确批准。
