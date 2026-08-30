---
change_id: update-media-object-key-business-id-layout
type: update
status: applied
created_at: 2026-08-29 19:45:00
updated_at: 2026-08-29 23:14:05
source_requirement: REQ-0131-media-object-key-business-id-layout
sprint: sprint-027
---

# Change Trace

```yaml
change_id: update-media-object-key-business-id-layout
type: update
status: applied
created_at: 2026-08-29 19:45:00
updated_at: 2026-08-29 23:14:05
source_requirement: REQ-0131-media-object-key-business-id-layout
sprint: sprint-027
product_data_collection_observability:
  status: applicable
  affected_layers:
    - request_logs
    - task_traces
    - task_trace_spans
    - backend_api
    - web_admin_request_flow
    - wechat_miniapp_request_flow
    - maintenance_jobs
  reason: 本 Change 涉及媒体上传、业务对象保存后 formalize、存量对象迁移、维护任务审计、受控媒体 URL 和数据库媒体引用一致性。
  validation: apply 阶段已补齐脱敏字段、失败分类、OpenAPI/Orval 同步、对象 key 与维护任务聚焦测试；2026-08-29 返修已覆盖 UUID 用户头像迁移、扁平业务媒体类型目录矩阵、本地后端容器 media-drift-reconcile dry-run、批量/生产 Runbook 的 5 阶段和 progress 口径同步；本次补齐 Pillow 图片上传测试、管理端 Vitest、小程序媒体测试、Docker Compose 当前运行状态和门禁校验。生产 media-drift-reconcile apply 仍需发布前备份确认，不在普通验收返修中擅自执行。
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-29 23:14:05 | `/opsx-modify` | 验收返修：补齐 Pillow 图片上传测试、管理端媒体 Vitest、小程序媒体测试、OpenSpec/语言/观测门禁和 Docker Compose 当前状态证据；REQ acceptance 已补 `result: passed` 证据摘要，机器回填块等待 `/opsx-archive` 正式关闭；保留生产 apply 备份确认边界。 |
| 2026-08-29 22:18:26 | `/opsx-modify` | 验收返修：将最终对象目录矩阵调整为扁平业务媒体类型目录，pending 统一为同类资源 `pending/`，旧/过渡目录作为兼容来源，并补充 `avartars` 错误拼写审计。 |
| 2026-08-29 21:39:22 | `/opsx-modify` | 验收返修：同步批量图片处理与生产媒体维护 Runbook，补齐 `media-drift-reconcile` 5 阶段、`--progress`、`business_id_media_key_migration`、UUID 用户头像迁移和业务对象 id 目录验收口径。 |
| 2026-08-29 21:31:09 | `/opsx-modify` | 验收返修：修正业务对象媒体迁移对 UUID 用户 id 的整数转换崩溃，补充 UUID 用户头像迁移测试；本地后端容器重建后 `media-drift-reconcile --progress` dry-run 5/5 阶段完成且 `failed=0`。 |
| 2026-08-29 21:14:09 | `/opsx-modify` | 验收返修：修正生产媒体维护 Runbook 中 `media-drift-reconcile` 进度阶段数量残留文案，统一为 5 个聚合阶段。 |
| 2026-08-29 20:09:36 | `/opsx-apply` | 实现统一业务对象 id 目录 builder、新上传 pending/正式目录、保存后 formalize、存量迁移任务、文档规范与聚焦测试；端侧 render/Network 验收与 PIL 依赖测试待补。 |
| 2026-08-29 19:45:00 | `/req-opsx` | 基于 REQ-0131 创建统一媒体对象 Key 按业务对象 id 分目录的 OpenSpec Change。 |
