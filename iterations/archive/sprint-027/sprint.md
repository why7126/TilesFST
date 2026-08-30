---
note: workflow-sync — workflow-sync 自动同步 — 3/3 Change archived；0 applied；Sprint `completed`
title: sprint-027 规划
created_at: 2026-08-29 18:13:44
updated_at: 2026-08-30 09:11:14
---

# sprint-027 规划

## 1. 目标

### Sprint 目标编号列表

- REQ-0130-media-maintenance-progress-output
- REQ-0131-media-object-key-business-id-layout
- BUG-0146-batch-media-maintenance-banner-variants

### REQ-0130-media-maintenance-progress-output 要点

为生产媒体维护 CLI 增加可选进度输出能力，优先覆盖 `backfill-image-variants`、`backfill-brand-certificate-thumbnails` 和 `media-drift-reconcile`。实现应保持默认 stdout 最终 JSON 兼容，开启进度后将任务名、阶段、总量、已完成数量、成功/失败/跳过数量和进度百分比输出到 stderr 或等价隔离通道，并遵守对象存储与生产命令脱敏边界。

### REQ-0131-media-object-key-business-id-layout 要点

统一所有媒体对象 Key 按业务对象 id 分目录，覆盖头像、品牌 Logo、Banner 图片、SKU 图片、SKU 视频、品牌证书图片与证书文件。实现应保留旧数据库引用读取兼容，明确 pending 到业务 id 目录 formalize 时机，补齐存量迁移 dry-run/apply/audit/rollback，保持派生图与原图目录可追溯，并同步对象存储、媒体、批处理 Runbook 和产品数据采集与链路观测验收摘要。

### BUG-0146-batch-media-maintenance-banner-variants 要点

修复批量媒体维护命令未覆盖 Banner 自定义上传图的问题，使历史 Banner 能被 `backfill-image-variants`、缩略图专项任务和 `media-drift-reconcile` 识别并补齐同目录 `.thumb.webp` / `.display.webp`。实现应保留 dry-run/apply/幂等证据，生产 JSON 输出保持脱敏，并在 apply 后补充 `/media` URL 与 Web 或小程序 Banner render evidence。

## 2. Scope

| 类型 | 编号 | 标题 | 状态 | 估算 | 说明 |
|---|---|---|---|---:|---|
| REQ | REQ-0130-media-maintenance-progress-output | 媒体维护任务进度输出 | done | 1 人天 | archived `add-media-maintenance-progress-output`（2026-08-29 21:46:01） |
| REQ | REQ-0131-media-object-key-business-id-layout | 统一媒体对象 Key 按业务对象 id 分目录 | done | 3 人天 | archived `update-media-object-key-business-id-layout`（2026-08-29 23:14:05） |
| BUG | BUG-0146-batch-media-maintenance-banner-variants | 批量媒体维护命令未覆盖 Banner 自定义上传图 | done | 1 人天 | archived `fix-media-maintenance-banner-variants`（2026-08-30 08:22:53） |

<!-- workflow-sync:scope-requirements:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| REQ-0130 | 媒体维护任务进度输出 | P1 | done | archived `add-media-maintenance-progress-output`（2026-08-29 21:46:01） |
| REQ-0131 | 统一媒体对象 Key 按业务对象 id 分目录 | P1 | done | archived `update-media-object-key-business-id-layout`（2026-08-29 23:14:05） |
<!-- workflow-sync:scope-requirements:end -->

<!-- workflow-sync:scope-bugs:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| BUG-0146 | 批量媒体维护命令未覆盖 Banner 自定义上传图 | high | done | archived `fix-media-maintenance-banner-variants`（2026-08-30 08:22:53） |
<!-- workflow-sync:scope-bugs:end -->

<!-- workflow-sync:scope-changes:start -->
| Change ID | 关联需求 | 状态 | Sprint 目标 |
|---|---|---|---|
| `add-media-maintenance-progress-output` | REQ-0130-media-maintenance-progress-output | archived | archived `add-media-maintenance-progress-output`（2026-08-29 21:46:01） |
| `fix-media-maintenance-banner-variants` | BUG-0146-batch-media-maintenance-banner-variants | archived | archived `fix-media-maintenance-banner-variants`（2026-08-30 08:22:53） |
| `update-media-object-key-business-id-layout` | REQ-0131-media-object-key-business-id-layout | archived | archived `update-media-object-key-business-id-layout`（2026-08-29 23:14:05） |
<!-- workflow-sync:scope-changes:end -->

REQ：`REQ-0130`、`REQ-0131` 已纳入正式范围；BUG：`BUG-0146` 已纳入正式范围，优先级高于新增体验能力；当前完成度与验收风险以 Scope 表状态、关联 Change 和 acceptance-report 为准。

Change：已回填 3 个范围项关联 Change，另有 0 个纯 Change；3 archived，0 applied，0 in_progress，0 proposed。Sprint 范围内 Change 已全部归档，Sprint 已关闭。

## 3. 工作量与容量

| 项 | 值 |
|---|---:|
| 容量基线 | 30 人天 |
| 估算 | 5 SP / 5 人天 |
| 容量占用 | 16.67% |
| fix 缓冲 | 25 人天 / 83.33% |

容量门禁通过。`project.yaml` 未提供显式 Sprint 容量，沿用最近已归档 Sprint 的确认容量基线：2 dev + 1 tester / 30 人天。本 Sprint 当前纳入 2 个 P1 媒体治理/运维需求和 1 个 high 生产媒体缺陷，合计估算 5 人天，占用 16.67%。

## 4. 里程碑

| 阶段 | 目标 |
|---|---|
| OpenSpec | 基于 REQ-0131 创建对象存储 Key 统一 Change，基于 BUG-0146 创建修复 Change，并回填本 Sprint scope；REQ-0130 的 Change 已存在并处于 applied，后续完成归档收尾。 |
| 实现 | 统一媒体业务对象 id 目录、pending/formalize、旧 key 兼容和迁移任务；为媒体维护 CLI 增加 Banner 候选覆盖，确保历史 Banner 能生成 `.thumb.webp` 与 `.display.webp`。 |
| 验证 | 验证新旧媒体 URL 可读、迁移 dry-run/apply/audit/rollback、Banner 幂等、`/media` URL 不再 fallback 原图、端侧 render evidence、安全脱敏、Runbook 与测试覆盖。 |
| 归档 | 完成 Change apply/archive 后，回填 REQ 验收与 Sprint 收尾。 |

## 5. 风险

- 若进度输出混入 stdout，会破坏现有 `jq`、生产脚本和审计归档。
- 若进度行输出真实 object key、endpoint、`.env` 或异常堆栈，可能违反生产媒体维护脱敏边界。
- `backfill-image-variants` 一个源图可能对应 thumbnail/display 两类写入，进度口径需要避免误导执行者。
- `media-drift-reconcile` 是聚合任务，阶段级进度和子任务 item 级进度需要在 Change 设计中明确取舍。
- Banner 派生图缺失会被 `/media` fallback 的 HTTP 200 掩盖，验收必须检查 `Content-Type`、`Content-Length` 和 `x-media-fallback`。
- 统一业务对象 id 目录若错误改写旧数据库引用，可能导致历史媒体不可见；REQ-0131 Change 必须保留旧 key 读取兼容，并把清理旧对象列为独立高风险确认动作。
- 存量迁移涉及 DB 引用与对象存储复制，必须先 dry-run 和备份确认，再 apply/audit，避免批量误写不可回滚。

## 6. 知识库承接

- 最近复盘 `docs/knowledge-base/retrospectives/sprint-025-retrospective.md` 提醒媒体维护必须保持 dry-run/apply/幂等证据、对象存储脱敏输出和 Runbook 边界。
- 最近复盘 `docs/knowledge-base/retrospectives/sprint-026-retrospective.md` 提醒媒体类问题需要端到端证据闭环，不能只看接口或字段成功。
- `docs/knowledge-base/best-practices/admin-media-upload-chain.md` 命中 REQ-0131 的 `media-upload` 横切标签：上传状态机、即时回显、对象 Key 与 `/media` 代理一致性、Docker Web 上传边界、历史 key 兼容或迁移证据必须转入 Change 验收。
- 本 Sprint 不新增管理端页面、列表或弹窗；REQ-0131 会影响既有上传入口和端侧媒体消费策略，BUG-0146 涉及历史媒体维护和端侧证据。
- 复盘已沉淀到 `docs/knowledge-base/retrospectives/sprint-027-retrospective.md`；生产 no-fallback 与公开 API 字段一致性补证作为后续行动项保留。

## 7. 横切预防清单

| 标签 | 适用性 | 验收 gate |
|---|---|---|
| admin-list | N/A | 不新增管理端列表页。 |
| admin-form | N/A | 不新增管理端表单页或设置页。 |
| admin-modal | N/A | 不新增管理端弹窗。 |
| media-upload | 适用 | REQ-0131 涉及上传 Key 归属、pending/formalize、即时回显、旧 key 兼容和端侧禁止拼接 URL；必须覆盖 Docker Web 边界或记录 N/A。 |
| media-maintenance | 适用 | 保持 stdout JSON 兼容；生产输出脱敏；覆盖存量迁移与 Banner dry-run/apply/audit/幂等；Runbook 与测试同步。 |
| product-data-collection-observability | 适用 | REQ-0131 已声明 request_logs、task_traces、task_trace_spans、backend_api、web_admin_request_flow、wechat_miniapp_request_flow、maintenance_jobs；Change 必须补齐脱敏字段与验证摘要。 |

## 8. 依赖

```text
REQ-0097-prod-compose-media-maintenance-job
  ├─ REQ-0130-media-maintenance-progress-output
  │   └─ add-media-maintenance-progress-output（archived）
  ├─ REQ-0131-media-object-key-business-id-layout
  │   └─ update-media-object-key-business-id-layout（archived）
  └─ BUG-0146-batch-media-maintenance-banner-variants
      └─ fix-media-maintenance-banner-variants（archived）

## 11. 关闭记录

- 2026-08-30 08:42:16：`/sprint-archive sprint-027` 关闭 Sprint；3/3 Change 已归档，REQ-0130、REQ-0131、BUG-0146 已迁入 Issue archive。BUG-0146 的生产 no-fallback 与公开 API 字段一致性补证保留为发布/运维窗口 follow-up，不阻断 Sprint 文档归档。
```

## 9. 发布计划

本 Sprint 变更属于后端媒体维护 CLI 运维体验增强、媒体对象存储 Key 治理和生产媒体性能缺陷修复。若最终进入产品版本发布，发布说明应标注新上传 Key 归属策略、旧媒体兼容边界、是否执行存量迁移或旧对象清理，以及 Banner 历史派生图补齐修复；默认不新增管理端、店主 Web 或小程序页面。

## 10. 关联文档

- `issues/requirements/archive/REQ-0130-media-maintenance-progress-output/`
- `issues/requirements/archive/REQ-0131-media-object-key-business-id-layout/`
- `issues/bugs/archive/BUG-0146-batch-media-maintenance-banner-variants/`
- `docs/07-object-storage-strategy.md`
- `rules/object-storage.md`
- `rules/media.md`
- `docs/standards/production-media-maintenance-runbook.md`
- `docs/standards/batch-image-processing-runbook.md`
