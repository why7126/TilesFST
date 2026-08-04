---
change_id: fix-prod-media-historical-object-drift
status: applied
created_at: 2026-08-04 10:54:57
updated_at: 2026-08-04 11:14:44
source_bug: BUG-0116-prod-media-historical-object-drift
change_type: fix
related_bugs:
  - BUG-0116-prod-media-historical-object-drift
related_requirements:
  - REQ-0012-object-storage-key-layout
related_changes:
  - add-prod-media-maintenance-jobs
---

# Change Trace

```yaml
change_id: fix-prod-media-historical-object-drift
status: applied
source_bug: BUG-0116-prod-media-historical-object-drift
change_type: fix
impact:
  backend: true
  web: false
  miniapp: false
  admin: false
  database: true
  storage: true
  api: false
  deployment: true
  tests: true
capabilities:
  modified:
    - object-storage
    - media-acceptance-template
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-04 10:54:57 | `/bug-opsx` | 基于 BUG-0116 创建生产历史媒体对象与缩略图漂移修复 Change。 |
| 2026-08-04 11:14:44 | `/opsx-apply` | 完成 BUG-0116 生产历史媒体对象漂移维护入口、测试、文档与验收回填；真实生产 apply 证据待后续补齐。 |
| 2026-08-04 12:05:00 | `/opsx-modify` | 验收返修：新增 `deploy/scripts/media-maintenance.sh` 部署包装入口，后端维护模块继续作为镜像内真实执行入口。 |
| 2026-08-04 20:20:00 | `/opsx-modify` | 验收返修：真实 `deploy/**/*.env` 作为未跟踪本地/生产配置存在时不再阻塞目录结构与归档门禁；已跟踪或待提交时仍阻塞。 |
