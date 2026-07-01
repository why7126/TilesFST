---
change_id: add-production-mysql-deployment
status: applied_partial
type: add
source_requirement: REQ-0018-production-mysql-deployment
created_at: 2026-06-29 09:55:35
updated_at: 2026-06-29 16:25:27
sprint: sprint-004
---

# Change Trace

## 来源

| 项 | 值 |
|---|---|
| REQ | `REQ-0018-production-mysql-deployment` |
| REQ 状态 | approved |
| Change 类型 | add |
| UI 原型 | N/A，无 UI 变更 |
| 建议下一步 | `/opsx-apply add-production-mysql-deployment` |

## Requirement Readiness Report

| 检查项 | 结果 |
|---|---|
| requirement.md | present |
| user-stories.md | present |
| business-flow.md | present |
| acceptance.md | present |
| trace.md | present |
| review.md | present / approved |
| prototype | N/A |
| readiness | Ready |

## Impact Analysis

```yaml
impact:
  backend: true
  web: false
  miniapp: false
  admin: indirect
  database: true
  storage: true
  api: false
capabilities:
  new:
    - database
    - deployment
  modified:
    - object-storage
    - testing
```

## Conflict Report

| 项 | 结果 |
|---|---|
| prototype/web | 不存在 |
| HTML > PNG 优先级 | N/A |
| acceptance 冲突 | 未发现 |
| UI Explore Gate | N/A |

## 变更记录

| 时间 | 动作 | 说明 |
|---|---|---|
| 2026-06-29 09:55:35 | `/req-opsx` | 创建 OpenSpec Change 并生成 proposal/design/specs/tasks |
| 2026-06-29 10:03:38 | `/sprint-propose sprint-004` | 纳入 sprint-004 正式规划 |
| 2026-06-29 10:35:38 | `/sprint-apply sprint-004` | 已实现 MySQL 配置/DDL/生产 Compose/文档/测试；生产外部 MySQL+MinIO 上传 smoke 待目标环境执行 |
| 2026-06-29 11:18:14 | `deployment-scenario-update` | 新增外部 MySQL + 外部 MinIO 生产 Compose 变体与部署文档 |
| 2026-06-29 16:21:57 | `local-external-smoke` | 本地 Docker MySQL `tilesfst` + 外部 MinIO 9000 完成 schema/seed/login/upload/media read smoke |
| 2026-06-29 16:25:27 | `restart-smoke` | 重启 backend/web/minio 后，同一 `/media/{object_key}` 仍可读取 |
