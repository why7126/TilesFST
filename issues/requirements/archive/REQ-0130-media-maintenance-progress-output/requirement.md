---
requirement_id: REQ-0130-media-maintenance-progress-output
title: 媒体维护任务进度输出
terminal: multi
version: v1
status: done
owner: product
source: capture.md
priority: P1
parent_requirement: REQ-0097-prod-compose-media-maintenance-job
created_at: 2026-08-29 18:05:37
updated_at: 2026-08-29 23:04:06
related_change: add-media-maintenance-progress-output
---

# REQ-0130 媒体维护任务进度输出

## 1. 需求背景

生产媒体维护任务已经支持通过后端包内 CLI 执行 dry-run / apply，覆盖 `backfill-image-variants`、`backfill-brand-certificate-thumbnails`、`media-drift-reconcile` 等批量图片派生图与对象漂移处理场景。实际生产执行时，单次任务可能扫描数百到数千个对象，且 apply 会持续读取原图、生成 WebP 派生图并写入对象存储。

当前命令默认在执行结束后输出完整 JSON。该行为适合脚本解析和审计归档，但在长时间运行时，执行者无法判断任务是否仍在推进、已完成多少对象、失败是否持续增加，也难以预估剩余时间。本需求希望在不破坏现有 JSON stdout 契约的前提下，为媒体维护任务增加可选进度输出能力。

## 2. 目标用户

| 角色 | 诉求 |
|---|---|
| 实施 / 运维 | 执行生产媒体维护 apply 时，能看到总量、已处理数量、失败数量和进度百分比，判断任务是否卡住。 |
| 后端 / 媒体能力开发 | 在保持 CLI JSON 兼容的同时，为长耗时任务提供统一进度输出机制。 |
| 测试 / 验收 | 能验证默认输出不变、开启进度后输出位置正确、失败计数和完成计数准确。 |
| 发布负责人 | 能将进度输出方式写入 Runbook，减少生产执行过程中的口头确认成本。 |

## 3. 范围

### 3.1 本期包含

- 为媒体维护 CLI 设计可选进度输出能力，优先覆盖 `backfill-image-variants`、`backfill-brand-certificate-thumbnails` 和 `media-drift-reconcile`。
- 进度信息至少包含任务名、总量、已完成数量、成功数量、失败数量、跳过数量和进度百分比。
- 默认不启用进度输出时，命令 stdout 仍保持现有完整 JSON 输出，兼容 `jq`、生产脚本和审计归档。
- 启用进度输出后，进度信息不得污染最终 JSON stdout；推荐输出到 stderr。
- 聚合任务 `media-drift-reconcile` 需要表达子任务阶段，便于执行者知道当前处于正式化、迁移、派生图回填或对象 key 审计阶段。
- 进度输出必须遵守生产媒体维护脱敏规则，不输出真实 object key、数据库连接串、`.env`、Authorization header、Cookie、access key、secret key 或生产私有敏感信息。
- 同步更新相关 Runbook、测试和维护命令帮助信息。

### 3.2 本期不包含

- 不新增管理端批处理页面、任务看板、WebSocket、SSE 或后台任务队列。
- 不新增任务进度持久化表，不写入数据库任务状态。
- 不改变现有维护任务的对象处理策略、缩略图生成规则、display 图生成规则或对象 key 迁移规则。
- 不改变 `--apply --confirm-backup` 的生产写入门禁。
- 不新增对象删除、回滚执行或自动重试调度能力。
- 不要求在本需求阶段直接修改 `src/`、OpenSpec 或生产部署文件。

## 4. 功能要求

### FR-001 可选进度参数

媒体维护 CLI MUST 提供可选进度输出开关。推荐参数为 `--progress`，用于在任务执行过程中输出进度信息。

未传入进度参数时，现有命令行为和最终 JSON 输出 MUST 保持兼容。已依赖 stdout 解析 JSON 的生产命令、Runbook 示例、`jq` 管道和自动化脚本不应因本需求受到破坏。

### FR-002 stdout / stderr 边界

最终任务结果 JSON MUST 继续输出到 stdout。

进度信息 SHOULD 输出到 stderr，避免与 stdout JSON 混杂。若后续设计需要机器可读进度格式，也应明确其输出通道、开关和兼容策略，不能默认改变现有 stdout 契约。

### FR-003 进度字段

进度输出 SHOULD 至少包含以下字段或等价信息：

| 字段 | 说明 |
|---|---|
| `task` | 当前维护任务名。 |
| `stage` | 当前阶段；聚合任务中用于区分子任务。 |
| `total` | 当前任务或当前阶段需要处理的总数。 |
| `completed` | 已完成处理数量，包含成功、失败和跳过。 |
| `success` | 已成功处理数量。 |
| `failed` | 已失败数量。 |
| `skipped` | 已跳过数量。 |
| `progress_percent` | 已完成百分比，建议保留两位小数。 |

当任务无法在启动前精确知道总量时，输出应明确 `total` 的计算口径或使用阶段级总量，避免展示误导性百分比。

### FR-004 任务覆盖

`backfill-brand-certificate-thumbnails` MUST 在扫描和重生成缩略图过程中支持进度输出。

`backfill-image-variants` MUST 在扫描和生成 `.thumb.webp` / `.display.webp` 派生图过程中支持进度输出，并能反映单个原图可能产生多个写入的情况。

`media-drift-reconcile` MUST 至少展示 4 个子任务阶段级进度：SKU pending 主图正式化、证书图片 key 迁移、缩略图回填和对象 key 审计。若子任务内部支持细粒度进度，聚合任务可以透传该子任务进度。

### FR-005 dry-run 与 apply 行为

进度输出 SHOULD 同时支持 dry-run 和 apply。dry-run 中的进度代表审计扫描进度；apply 中的进度代表实际处理和写入进度。

apply 模式下，失败项数量必须随处理过程更新。若出现失败，进度输出可以继续展示已完成数量，但最终是否继续执行仍由维护任务既有中止策略和失败处理规则决定。

### FR-006 脱敏与安全

进度输出 MUST 只包含任务名、阶段名、计数、百分比和枚举化状态，不得输出真实对象 key、文件名、客户信息、数据库连接串、对象存储 endpoint、access key、secret key、Authorization header、Cookie、真实 `.env` 内容或本机绝对路径。

如需要定位失败对象，仍应使用最终 JSON 中既有的脱敏 hash、标准前缀和失败原因枚举，不应通过进度行泄露更多信息。

### FR-007 Runbook 与帮助信息

后续实现 MUST 更新生产媒体维护 Runbook，说明进度参数的使用方式、stdout / stderr 边界、适用任务、示例输出和日志采集注意事项。

维护 CLI help 文案 SHOULD 标明进度参数不会改变最终 JSON stdout，便于运维在生产命令中安全使用。

### FR-008 测试覆盖

后续实现 MUST 补充聚焦测试，至少覆盖：

- 默认不启用进度输出时，stdout JSON 结构保持兼容。
- 启用进度输出时，进度写入 stderr，stdout 仍可被 JSON 解析。
- `backfill-image-variants` 的 `completed`、`success`、`failed`、`skipped` 和百分比计算正确。
- `media-drift-reconcile` 能输出阶段级进度。
- 异常或失败 item 不会泄露真实 object key 或敏感配置。

## 5. UI 约束

本需求不新增 Web、管理端或小程序 UI。进度输出属于命令行交互，不涉及 Design System、页面布局、视觉组件或端侧路由。

命令行展示应保持紧凑、可复制、可被日志系统采集。进度行不得使用难以解析的动态终端控制符作为唯一输出方式；如使用覆盖式进度条，也应保留可读的普通日志行方案。

## 6. 关联需求

| 关联项 | 关系 | 说明 |
|---|---|---|
| REQ-0097-prod-compose-media-maintenance-job | 父需求 | 媒体维护任务生产执行入口与备份确认门禁是本需求的基础。 |
| REQ-0122-batch-image-processing-runbook | 关联 Runbook | 后续实现需要同步批量图片处理 Runbook，说明进度输出用法。 |
| REQ-0115-media-multi-variant-images | 关联媒体能力 | `backfill-image-variants` 处理的 `.thumb.webp` / `.display.webp` 属于多规格图片能力。 |
| REQ-0120-webp-derived-image-variants | 关联派生能力 | 进度输出覆盖 WebP 派生图生成和历史回填过程。 |
| `rules/media.md` | 关联规范 | 后续实现需遵守生产媒体维护输出脱敏和验收摘要要求。 |
| `rules/object-storage.md` | 关联规范 | 后续实现不得泄露对象存储密钥、真实 key 或私有连接信息。 |

## 7. 状态块

```yaml
requirement_id: REQ-0130-media-maintenance-progress-output
status: done
lifecycle_stage: review
readiness: Ready
next_command: /opsx-archive REQ-0130-media-maintenance-progress-output
iteration: sprint-027
related_change: add-media-maintenance-progress-output
openspec_changes:
  - change_id: add-media-maintenance-progress-output
    type: update
    status: archived
decisions:
  output_channel: stderr_for_progress_stdout_for_final_json
  default_behavior: keep_existing_json_output
  preferred_flag: --progress
open_questions:
  - 进度输出是否需要同时提供机器可读 JSON Lines 格式，还是先仅提供文本进度行。
  - 聚合任务是否只展示阶段级进度，还是透传每个子任务的 item 级进度。
notes:
  - 已补齐 user-stories、business-flow、acceptance 和 trace；已创建 OpenSpec Change，尚未修改后端媒体维护 CLI。
  - 2026-08-29 18:11:19 评审通过，后续先纳入 Sprint，再创建 OpenSpec Change。
  - 2026-08-29 18:59:38 已通过 /req-opsx 创建 add-media-maintenance-progress-output，下一步进入 /opsx-apply。
product_data_collection_observability:
  applicable: false
  affected_layers: []
  reason: 本需求仅描述媒体维护 CLI 的进度输出，不新增 API、DB、请求日志、行为埋点、Task Trace、Web 请求封装、小程序请求封装或 App 请求封装；若后续实现改为持久化任务进度或写入任务追踪表，需在 Change 阶段重新评估。
  validation: req-generate、req-complete 与 req-opsx 阶段已声明不适用原因；后续若持久化进度或写入任务追踪表需重新评估。
```
