---
requirement_id: REQ-0117-media-maintenance-storage-unreachable-summary
title: 媒体维护 dry-run 增加对象存储不可达快速摘要 - 验收标准
acceptance_status: passed
created_at: 2026-08-22 17:14:59
updated_at: 2026-08-25 14:51:36
---

# 验收标准

## 功能 AC

- [ ] AC-001 媒体维护 dry-run 必须区分对象真实不存在和对象存储不可达；`MEDIA_NOT_FOUND`、NoSuchKey 或 NoSuchObject 仍归入对象缺失统计。
- [ ] AC-002 当对象存储适配层返回 `STORAGE_UNAVAILABLE` 或等价不可达错误时，维护任务必须归类为 `object_storage_unreachable` 或等价枚举，不得写作 `missing_original`、`missing_thumbnail` 或普通 `object_exists=false`。
- [ ] AC-003 对象存储不可达时，dry-run 应尽早返回 blocked 快速摘要，避免继续逐条扫描大量对象。
- [ ] AC-004 快速摘要至少包含任务名、失败枚举、provider、bucket 脱敏 hash、auto create bucket 策略、受影响任务和建议动作。
- [ ] AC-005 聚合任务必须在顶层 summary 或 acceptance summary 表达 blocked，不得仅在子任务明细里隐藏不可达失败。
- [ ] AC-006 聚合任务在对象存储不可达时不得输出“失败为 0 且可进入 apply”的结论。
- [ ] AC-007 `acceptance_summary.object.status` 在对象存储不可达时必须为 blocked 或 fail；`thumbnail_benefit` 在无法读取对象时不得误报 pass。
- [ ] AC-008 快速摘要、明细、日志和测试快照不得输出 access key、secret key、数据库连接串、Authorization header、Cookie、生产 `.env` 原文、本机绝对路径、未脱敏 raw object key、真实客户数据或私有对象存储 URL。
- [ ] AC-009 补充聚焦测试覆盖对象存储不可达、对象真实不存在、聚合任务顶层阻断语义和敏感输出保护。
- [ ] AC-010 生产媒体维护 runbook 或等价文档必须说明 `object_storage_unreachable` 的解读方式和排查顺序。

## 运维排查 AC

- [ ] AC-OPS-001 blocked 摘要的 `recommended_action` 应提示检查 endpoint、region、bucket、权限、网络和生产 env 注入。
- [ ] AC-OPS-002 对象存储不可达时必须停止 apply 判断；修复对象存储环境后重新执行 dry-run，再决定是否进入备份确认和 apply。
- [ ] AC-OPS-003 如果任务在发现不可达前已完成部分数据库扫描，可以保留安全计数，但必须明确对象维度不可验证。
- [ ] AC-OPS-004 runbook 应承接 sprint-019 复盘经验，继续要求 dry-run、快照、apply、二次审计、失败恢复和脱敏输出证据。

## 文档与治理 AC

- [ ] AC-DOC-001 后续 OpenSpec Change 必须同步 `docs/standards/production-media-maintenance-runbook.md` 或等价生产媒体维护说明。
- [ ] AC-DOC-002 若新增或调整维护 JSON 字段，必须在设计和测试计划中说明字段含义、脱敏策略、兼容性和样例。
- [ ] AC-DOC-003 若涉及 API、DB schema、Orval 或前端 UI 变化，必须在后续 Change 中明确同步项；本需求默认不新增对外 API、不改 DB、不改 Orval、不新增 UI。
- [ ] AC-DOC-004 若对象存储适配层新增通用健康探测接口，必须说明 MinIO、S3 兼容 provider 与腾讯云 COS 的适配边界。

## 横切 AC（knowledge-base）

本 REQ 为后端 / 运维 CLI 需求，不新增管理端列表、表单、弹窗或媒体上传 UI，因此知识库 UI 横切标签为 N/A，无 AC-XCUT 条目。

| 标签 | 引用文档 | 写入 AC 条数 | 说明 |
|---|---|---:|---|
| 无匹配 | N/A | 0 | 不涉及 admin-list、admin-form、admin-modal、media-upload。 |

复盘经验已转化为功能与运维 AC：

| 来源 | 转化到 |
|---|---|
| `docs/knowledge-base/retrospectives/sprint-019-retrospective.md` 媒体治理从单点 BUG 升级为生产维护能力 | AC-003、AC-005、AC-006 |
| `docs/knowledge-base/retrospectives/sprint-019-retrospective.md` 媒体验收证据需要 key/object/URL/render 与 dry-run/apply | AC-007、AC-OPS-004 |
| `docs/knowledge-base/retrospectives/sprint-019-retrospective.md` 生产媒体维护 runbook 应覆盖 dry-run、快照、apply、二次审计和脱敏输出 | AC-010、AC-OPS-004、AC-DOC-001 |

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-22 19:38:52
accepted_by: workflow-sync
source_change: improve-media-maintenance-storage-unreachable-summary
source_sprint: sprint-025
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

