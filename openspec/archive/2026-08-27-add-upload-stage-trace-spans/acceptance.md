---
change_id: add-upload-stage-trace-spans
source_requirement: REQ-0123-upload-stage-trace-spans
sprint: sprint-026
created_at: 2026-08-25 18:58:00
updated_at: 2026-08-25 18:58:00
---

# 验收

## 必须验收

- 头像上传成功路径可以在 Task Trace spans 中看到 `file_read` 与 `original_put_object`，并按实际派生策略看到派生阶段或跳过原因。
- 通用图片上传成功路径可以在 Task Trace spans 中看到 `file_read`、`original_put_object`、`thumbnail_generate`、`thumbnail_put_object`、`display_generate`、`display_put_object`。
- 每个 span 包含阶段名、耗时、状态和脱敏错误摘要字段；成功阶段耗时为非负毫秒值。
- 对象存储写入失败时，trace 保留失败前已完成阶段和失败阶段。
- 派生图生成失败或跳过时，trace 能区分 `failed` 与 `skipped`，且错误摘要不泄露敏感信息。
- 上传仍通过后端鉴权与对象存储适配层完成，不引入前端直连对象存储。

## 非目标确认

- 不要求新增管理端 UI。
- 不要求新增监控平台或图表系统。
- 不改变 MinIO Bucket、对象 key 策略或多规格图片 URL 语义。
- 默认不要求 Orval；只有 API 响应或查询契约变化时才需要生成。
