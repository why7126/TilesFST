---
bug_id: BUG-0142-admin-avatar-upload-storage-put-slow
title: 管理端头像上传小文件对象存储写入耗时 30 秒以上
severity: high
status: done
owner:
discovered_at: 2026-08-25 17:40:13
environment: docker
related_requirement:
related_change: fix-admin-avatar-webp-thumbnail-timeout
updated_at: 2026-08-27 23:14:36
created_at: 2026-08-25 17:47:58
---

# 现象

管理端上传 127KB 级 WebP 头像时，`POST /api/v1/admin/uploads` 最终返回 200，但接口等待约 31.74 秒。历史 `task_trace` 证据显示，同一路径下存在两次 WebP 头像上传慢请求：

- `task_upload_image_9a87068374164c4b`：`size_bytes=127458`，`storage_put_object=32205ms`，请求总耗时约 `32258ms`。
- `task_upload_image_801e8a0d425e42b3`：`size_bytes=135026`，`storage_put_object=31700ms`，请求总耗时约 `31733ms`。

同一环境下，约 146KB JPEG 头像上传和约 142KB WebP 对照上传未稳定复现 30 秒级等待，说明该问题可能与特定 WebP 样本、对象存储连接状态、串行派生图写入或观测口径混合有关。

补充浏览器证据见 `screenshots/network-upload-31s.png`：Network 面板显示 `localhost:3000` 的 `POST uploads` 返回 200，等待时间为 `31.74 秒`；后续头像 WebP 图片请求返回 200，大小约 `135.37 KB`。

阶段级日志详情见 `screenshots/log-detail-stage-timing-thumbnail-generate-28s.png`：同一次上传中 `original_put_object=151ms`、`thumbnail_generate=28464ms`、`thumbnail_put_object=87ms`，确认主要慢点为头像缩略图生成，而不是对象存储 put。

# 复现步骤

1. 使用管理端账号登录。
2. 进入支持头像上传的管理端页面。
3. 选择约 127KB 的 WebP 头像文件并发起上传。
4. 观察浏览器 Network 中 `POST /api/v1/admin/uploads` 的响应状态和等待时间。
5. 查看后端 `task_trace` 和 `request_logs`，重点关注 `storage_put_object`、`api_response` 与请求总耗时。

# 期望 vs 实际

期望：

- 127KB 级头像上传应在可接受时间内完成。
- 对象存储写入、头像缩略图和展示图派生不应导致 30 秒级阻塞。
- 观测数据应能区分原图写入、派生图生成和派生图写入耗时。

实际：

- WebP 头像上传接口返回 200，但存在约 31.7 秒等待。
- 阶段级日志详情确认 `thumbnail_generate` 为主要慢点；外层 `storage_put_object` 为累计耗时，容易误导为对象存储 put 慢。
- 当前复现中同路径 JPEG / WebP 对照请求未稳定复现 30 秒级耗时。

# 影响范围

- 管理端个人头像上传体验。
- 后端上传接口 `POST /api/v1/admin/uploads`。
- Backend 到对象存储的 `put_object` 链路。
- 头像上传后的 thumbnail / display 派生图生成与多对象写入链路。
- 管理后台上传任务追踪与日志审计中慢 span 的定位准确性。

# 严重等级说明

严重等级暂定为 `high`。接口最终成功返回，不属于不可用或数据丢失；但小文件头像上传出现 30 秒级等待，会明显破坏管理端交互体验，也可能掩盖对象存储或派生图链路的系统性慢点。该问题需要在根因补齐阶段确认是否稳定复现、是否只影响 WebP、是否存在对象存储连接重试或串行派生写入放大。
openspec_changes:
  - change_id: fix-admin-avatar-webp-thumbnail-timeout
    type: update
    status: archived
