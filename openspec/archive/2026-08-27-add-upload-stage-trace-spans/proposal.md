---
change_id: add-upload-stage-trace-spans
source_requirement: REQ-0123-upload-stage-trace-spans
sprint: sprint-026
created_at: 2026-08-25 18:58:00
updated_at: 2026-08-25 18:58:00
---

# 上传链路阶段级耗时写入 Task Trace Spans

## 背景

头像上传与通用图片上传已经包含文件读取、原图写入、派生图生成和派生图写入等多个阶段，但排障时仍主要依赖分散日志和人工拼接。将关键阶段耗时写入 Task Trace spans，可以让慢上传、对象存储抖动、派生图生成失败等问题具备稳定、可查询、可测试的结构化事实源。

## 变更内容

- 为头像上传分支接入阶段级 trace spans，覆盖文件读取、原图对象写入，以及适用的派生图生成和写入阶段。
- 为通用图片上传分支接入阶段级 trace spans，成功路径必须覆盖 `file_read`、`original_put_object`、`thumbnail_generate`、`thumbnail_put_object`、`display_generate`、`display_put_object`。
- 明确每个 span 至少记录阶段名、耗时、状态、开始/结束时间、失败错误摘要和必要脱敏 metadata。
- 明确失败时保留已完成阶段与失败阶段 spans；后续未执行阶段需要记录 `skipped` 或具备可解释的缺省语义。
- 保留日志作为辅助排查信息，但验收事实源以 Task Trace spans 为准。
- 不新增前端直传对象存储，不改变现有对象 key、Bucket 与 MinIO 前缀策略。

## 能力范围

### 新增能力

无。

### 修改能力

- `product-usage-logging`：扩展 Task Trace 对上传阶段级 spans 的要求。
- `media-multi-variant-images`：要求通用图片上传在 original、thumbnail、display 全链路记录阶段 spans。
- `admin-profile-page`：要求管理员头像上传链路记录阶段 spans，并在失败时保留可定位事实。

## 影响

- 后端：影响媒体上传服务、头像上传服务、对象存储适配层调用周边计时与 trace 写入。
- 对象存储：不改变 Bucket、key、ACL 或前缀，仅记录 `put_object` 阶段耗时和失败状态。
- API：默认不改变上传接口响应；若实现阶段新增 `trace_id`、`spans` 或查询字段，必须同步 OpenAPI、Orval、API 文档和测试。
- 数据库：默认复用现有 Task Trace 持久化；若现有结构不足，必须在实现前补充 schema、迁移、数据库文档与回滚方案。
- Web 管理端：默认不新增可见 UI；若展示 spans，必须遵守 Design System semantic token 与权限边界。
- 小程序 / 店主 Web：不涉及。
- Docker Compose：默认不涉及。
