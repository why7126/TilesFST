---
change_id: fix-upload-size-limit-consistency
type: fix
status: archived
created_at: 2026-07-21 15:23:55
updated_at: 2026-07-21 23:00:59
source_bug: BUG-0073-video-upload-23m-file-fails
related_requirement: null
iteration: sprint-010
---

# Change Trace

## 来源

| 类型 | ID / 路径 | 说明 |
|---|---|---|
| BUG | `BUG-0073-video-upload-23m-file-fails` | 上传约 23M 文件失败，图片、视频和文档均受影响 |

## 状态

```yaml
change_id: fix-upload-size-limit-consistency
type: fix
status: archived
source_bug: BUG-0073-video-upload-23m-file-fails
related_requirement: null
iteration: sprint-010
tasks:
  total: 22
  completed: 22
```

## 验收证据

| 时间 | 类型 | 说明 |
|---|---|---|
| 2026-07-21 23:00:59 | 自动化测试 | 后端上传 / 系统设置 / 对象存储聚焦测试 50 passed；前端系统设置与证书上传组件测试 15 passed |
| 2026-07-21 23:00:59 | 配置与文档 | 新增 `MAX_FILE_SIZE_MB` / `media.max_file_size_mb`，同步 `.env.example`、生产 Docker Compose、Nginx 注释、部署文档、上传标准和 API 索引 |
| 2026-07-21 23:00:59 | 知识库评估 | 本次沿用 `admin-media-upload-chain.md` 既有最佳实践，无新增独立 incident 知识库条目 |

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-21 15:23:55 | /bug-opsx | 从 BUG-0073 创建 OpenSpec fix Change |
| 2026-07-21 15:28:53 | /sprint-propose sprint-010 | 纳入 sprint-010 正式范围 |
| 2026-07-21 23:00:59 | /opsx-apply | 完成上传大小限制一致性修复、测试与文档同步 |
