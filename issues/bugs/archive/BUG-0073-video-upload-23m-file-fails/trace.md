---
bug_id: BUG-0073-video-upload-23m-file-fails
status: done
lifecycle_stage: archive
severity: high
created_at: 2026-07-21 10:12:43
updated_at: 2026-07-22 09:21:38
lifecycle:
  captured: 2026-07-21 10:12:43
  generated: 2026-07-21 14:42:44
  completed: 2026-07-21 14:58:33
  reviewed: 2026-07-21 15:01:07
  approved: 2026-07-21 15:01:07
iteration: sprint-010
related_requirement: null
related_bug: null
related_change: fix-upload-size-limit-consistency
source_command: /capture
captured_via: capture
classification_rationale: 项目已有媒体上传与文件资料管理能力，约 23M 的图片、视频和文档等文件上传失败属于既有公共上传链路在文件大小、后端校验、网关限制或 MinIO 写入环节上的行为偏差，倾向记录为 BUG。
openspec_changes:
  - change_id: fix-upload-size-limit-consistency
    type: fix
    status: archived
related_bugs: []
---

```yaml
bug_id: BUG-0073-video-upload-23m-file-fails
status: done
severity: high
lifecycle_stage: archive
created_at: 2026-07-21 10:12:43
updated_at: 2026-07-21 15:28:53
lifecycle:
  captured: 2026-07-21 10:12:43
  generated: 2026-07-21 14:42:44
  completed: 2026-07-21 14:58:33
  reviewed: 2026-07-21 15:01:07
  approved: 2026-07-21 15:01:07
iteration: sprint-010
related_requirement: null
related_bug: null
related_change: fix-upload-size-limit-consistency
source_command: /capture
captured_via: capture
classification_rationale: 项目已有媒体上传与文件资料管理能力，约 23M 的图片、视频和文档等文件上传失败属于既有公共上传链路在文件大小、后端校验、网关限制或 MinIO 写入环节上的行为偏差，倾向记录为 BUG。
openspec_changes:
  - change_id: fix-upload-size-limit-consistency
    type: fix
    status: archived
related_bugs: []
scope:
  terminal: admin_web_or_miniapp_to_confirm
  module: media_upload
  media_type: image_video_document
  issue_type: upload_failure
readiness:
  capture: done
  bug: done
  root_cause: done
  workaround: done
  acceptance: done
  review: done
  trace: done
  next: opsx-apply
```

## 来源

| 类型 | ID / 路径 | 说明 |
|---|---|---|
| 用户反馈 | `/capture` | 上传 23M 的视频文件失败 |
| 用户补充 | `/bug-generate` | 不止视频，图片也有同样问题，文档预计也可能受影响 |

## 建议复现要点

| 要点 | 说明 |
|---|---|
| 上传入口 | 确认发生在管理端视频上传、商品/SKU 媒体上传、小程序上传或其他入口 |
| 文件信息 | 分别记录图片、视频、文档的文件大小、扩展名、MIME Type、编码信息和文件内容特征 |
| 前端表现 | 记录页面错误提示、进度条状态、是否超时或被前端大小校验拦截 |
| Network 响应 | 记录上传接口 URL、HTTP 状态码、响应 JSON、错误码和请求耗时 |
| 后端日志 | 对照 FastAPI 日志，确认是否为请求体过大、Pydantic 校验、MIME/扩展名限制、临时文件、MinIO 写入或超时错误 |
| 部署链路 | 若在 Docker/Nginx/代理环境复现，确认代理层请求体大小和超时配置 |

## 建议验收要点

| 验收点 | 说明 |
|---|---|
| 合法文件成功 | 符合系统限制的约 23M 图片、视频、文档文件可上传成功 |
| 错误可诊断 | 超过限制或格式不支持时返回明确错误码和用户可理解提示 |
| 存储可用 | 上传成功后媒体对象可通过后端授权链路读取，不绕过 MinIO 适配层 |
| 边界覆盖 | 覆盖小文件、约 23M 文件、超过上限文件、不支持格式的图片、视频、文档回归测试 |
| 配置一致 | 前端提示、后端校验、Docker/Nginx/MinIO 相关大小限制保持一致 |

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-22 09:21:03 | lifecycle-stage-migrate | review → archive（/opsx-archive fix-upload-size-limit-consistency） |
| 2026-07-22 09:20:43 | /opsx-archive | Change `fix-upload-size-limit-consistency` 已归档，状态同步完成。 |
| 2026-07-21 23:04:14 | /opsx-apply | Change `fix-upload-size-limit-consistency` apply 完成，待 archive。 |
| 2026-07-21 15:01:53 | lifecycle-stage-migrate | plan → review（/bug-review --approve） |
| 2026-07-21 10:12:43 | /capture | 记录上传 23M 视频文件失败缺陷 |
| 2026-07-21 14:42:44 | /bug-generate | 基于补充信息生成 bug.md，范围扩展为图片、视频和文档等公共上传链路，状态更新为 draft |
| 2026-07-21 14:58:33 | /bug-complete | 补齐 root-cause、workaround、acceptance，状态更新为 pending_review |
| 2026-07-21 15:01:07 | /bug-review --approve | 评审通过，允许进入 bug-opsx 与 Sprint 规划 |
| 2026-07-21 15:23:55 | /bug-opsx | 创建 OpenSpec Change `fix-upload-size-limit-consistency` |
| 2026-07-21 15:28:53 | /sprint-propose sprint-010 | 纳入 sprint-010 正式范围，关联 Change `fix-upload-size-limit-consistency` |

- 2026-07-22 09:20:43 workflow-sync：状态同步为 done（Change archived）
