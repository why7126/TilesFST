---
requirement_id: REQ-0117-media-maintenance-storage-unreachable-summary
title: 媒体维护 dry-run 增加对象存储不可达快速摘要
terminal: multi
version: v1
status: done
owner: product
source: capture.md
priority: P2
parent_requirement: REQ-0097-prod-compose-media-maintenance-job
created_at: 2026-08-22 17:11:30
updated_at: 2026-08-25 14:53:29
related_change: improve-media-maintenance-storage-unreachable-summary
---

# REQ-0117 媒体维护 dry-run 增加对象存储不可达快速摘要

## 1. 需求背景

生产媒体维护任务已经支持 dry-run、apply、脱敏输出、失败原因统计和媒体验收摘要。运维在执行 `bug-0116-media-drift`、`backfill-brand-certificate-thumbnails`、`backfill-image-variants` 等任务时，需要同时访问数据库与对象存储，并根据 dry-run 判断是否可以进入备份确认和 apply。

当前对象存储适配层会把连接失败、权限异常、endpoint 配置错误或 SDK 异常映射为 `STORAGE_UNAVAILABLE`。但维护任务中的对象存在性判断会把所有 `AppError` 简化为对象不存在，导致对象存储不可达时可能在 dry-run 结果中表现为大量 `missing_original`、`missing_thumbnail`、`object_exists=false` 或逐条失败。

这种输出不利于快速判断基础设施问题：运维可能误以为是历史对象漂移、对象缺失或缩略图缺失，继续深入明细排查，甚至错误推进 apply 判断。本需求用于定义对象存储不可达时的快速失败摘要，让 dry-run 更早、更清晰、更安全地提示“先修对象存储连接 / 权限 / endpoint，再处理媒体维护任务”。

## 2. 目标用户

| 角色 | 诉求 |
|---|---|
| 实施 / 运维 | 在生产或生产等价环境执行 dry-run 时，能快速识别 COS、MinIO 或 S3 兼容对象存储不可达，而不是逐条分析误导性的对象缺失。 |
| 发布负责人 | 能基于脱敏摘要判断当前环境是否可进入 apply 前置检查，避免在对象存储不可用时继续发布或维护操作。 |
| 后端开发 | 能有统一的失败分类和短路策略，避免每个媒体维护任务重复处理 `STORAGE_UNAVAILABLE`。 |
| 测试 / 验收 | 能用聚焦测试区分对象真实不存在和对象存储不可达两类结果，并验证敏感信息不泄露。 |

## 3. 范围

### 3.1 本期包含

- 媒体维护 dry-run 在对象存储不可达时输出快速失败摘要。
- 不可达摘要覆盖生产媒体维护入口中的对象读、对象元信息读取、对象存在性检查相关失败。
- 摘要使用枚举化失败原因，例如 `object_storage_unreachable` 或等价分类。
- 摘要必须脱敏，仅输出 provider、bucket hash、auto create bucket 策略、任务名、受影响任务、失败分类和建议动作等安全字段。
- 对象真实不存在仍保持对象缺失类统计，不得误归类为对象存储不可达。
- 聚合任务应在顶层 summary 或 acceptance summary 中明确阻断状态，便于运维先处理基础设施问题。
- 补充测试覆盖对象存储不可达、对象不存在、聚合任务输出和敏感信息输出保护。
- 同步更新生产媒体维护 runbook 或等价说明，使运维知道如何解读快速失败摘要。

### 3.2 本期不包含

- 不在 PRD 阶段直接修改源码、测试、OpenSpec 或部署文件。
- 不改变对象存储单 Bucket + 标准前缀策略。
- 不新增对象存储自动修复、自动建桶、自动切换 endpoint 或凭据轮换能力。
- 不执行任何生产 dry-run、apply、对象写入、对象删除或数据库写入。
- 不新增管理端 UI、任务队列、定时任务或可视化报表。
- 不改变媒体上传、公开 `/media/{object_key}` 读取或小程序展示链路。
- 不把真实 object key、生产 `.env`、密钥、连接串、客户数据或本机绝对路径写入维护输出。

## 4. 功能要求

### FR-001 对象存储不可达识别

媒体维护 dry-run MUST 区分对象真实不存在和对象存储不可达。

当对象存储适配层返回 `STORAGE_UNAVAILABLE` 或等价不可达错误时，维护任务 MUST 将其归类为对象存储不可达，而不是 `missing_original`、`missing_thumbnail` 或普通 `object_exists=false`。

对象不存在类错误，例如 `MEDIA_NOT_FOUND` 或 provider 的 NoSuchKey / NoSuchObject 映射，仍应保留为对象缺失统计。

### FR-002 快速失败摘要

当 dry-run 发现对象存储不可达时，系统 SHOULD 尽早返回快速失败摘要，避免继续逐条扫描大量对象。

快速失败摘要 SHOULD 包含：

| 字段 | 要求 |
|---|---|
| `status` | SHOULD 为 `blocked` 或等价阻断状态。 |
| `reason` | MUST 为枚举化原因，例如 `object_storage_unreachable`。 |
| `task` | MUST 标识当前维护任务。 |
| `affected_tasks` | 聚合任务 SHOULD 标识受影响子任务。 |
| `environment.object_storage_provider` | MUST 输出 provider 名称。 |
| `environment.object_storage_bucket_hash` | MUST 输出 bucket 脱敏 hash，不输出 bucket 原文。 |
| `environment.auto_create_bucket` | MUST 输出当前自动建桶策略。 |
| `recommended_action` | SHOULD 提示检查 endpoint、region、bucket、权限、网络和生产 env 注入。 |

如果任务在执行部分数据库扫描后才发现不可达，摘要 MAY 保留安全的数据库扫描计数，但 MUST 明确对象维度验收为 blocked。

### FR-003 聚合任务阻断语义

聚合任务 `bug-0116-media-drift` 或后续等价聚合入口 MUST 在顶层 summary 中表达对象存储不可达状态，避免仅在某个子任务明细中隐藏失败。

聚合任务 SHOULD 在发现统一不可达后停止后续对象相关子任务，或者将后续子任务标记为 skipped / blocked，并在顶层 `affected_tasks` 中列出。

聚合任务不得在对象存储不可达时输出“失败为 0 且可进入 apply”的结论。

### FR-004 验收摘要状态

维护任务的 `acceptance_summary.object.status` MUST 能表达对象存储不可达导致的阻断状态。

当对象存储不可达时：

- `key` 维度 MAY 继续根据数据库记录返回 pass、blocked 或 n/a，但必须说明对象维度不可验证。
- `object` 维度 MUST 为 blocked 或 fail，不得为 pass。
- `URL` 维度继续保持不调用 HTTP 媒体 URL 的 n/a 语义，除非后续任务明确增加 URL 检查。
- `thumbnail_benefit` 维度在无法读取原图或缩略图时 MUST 为 blocked 或 n/a，不得误报 pass。
- `render` 维度继续说明维护 JSON 不能替代端侧 evidence。

### FR-005 敏感信息保护

快速失败摘要、明细、日志和测试快照 MUST 继续遵守媒体维护输出脱敏要求。

输出 MUST NOT 包含：

- 对象存储 access key、secret key、session token。
- 数据库连接串、账号密码、Authorization header、Cookie。
- 生产 `.env` 原文。
- 本机绝对路径。
- 未脱敏 raw object key。
- 真实客户数据、客户媒体文件名或私有对象存储 URL。

系统 SHOULD 复用现有敏感输出保护机制，并为新增失败摘要补充测试。

### FR-006 运维解读与建议动作

生产媒体维护 runbook 或等价文档 SHOULD 说明对象存储不可达快速摘要的含义。

文档 SHOULD 引导运维按以下顺序排查：

1. 确认生产 env 指向预期 provider、endpoint、region 和 bucket。
2. 确认对象存储 bucket / prefix 快照与权限策略存在。
3. 确认后端容器网络能访问对象存储 endpoint。
4. 确认 access key / secret key 或云厂商凭据仍有效。
5. 修复后重新执行 dry-run，再判断是否可进入备份确认和 apply。

## 5. UI 约束

本需求默认不新增 Web、店主端或小程序 UI。

命令行 JSON 输出是本需求的主要用户界面。输出应保持结构稳定、字段语义清晰、便于复制到运维记录或验收文档中，同时严格脱敏。

如后续实现增加管理端维护任务状态页或审计报告页，必须另行明确权限、Design System 复用、敏感信息脱敏和 API/Orval 影响。

## 6. 关联需求

| 关联项 | 关系 | 说明 |
|---|---|---|
| REQ-0097-prod-compose-media-maintenance-job | 父需求 | 定义生产媒体维护任务安全执行、dry-run/apply、备份与验收摘要边界。 |
| REQ-0090-media-five-point-acceptance-template | 验收模板 | 媒体维护摘要需要继续覆盖 key、object、URL、thumbnail benefit、render 等维度。 |
| REQ-0091-media-bug-four-point-acceptance-template | 验收模板 | 媒体问题相关验收需区分 key、object、URL、render，不得用对象不可达替代对象缺失证据。 |
| REQ-0092-brand-certificate-image-thumbnails | 相关媒体能力 | 历史缩略图回填任务是本需求的主要受影响入口之一。 |
| REQ-0099-global-thumbnail-size-limit | 相关媒体策略 | 缩略图策略 dry-run 需要在对象存储不可达时明确阻断，而不是误报可重生成候选。 |

## 7. 状态块

```yaml
status: done
lifecycle_stage: review
next_command: /opsx-archive REQ-0117-media-maintenance-storage-unreachable-summary
related_change: improve-media-maintenance-storage-unreachable-summary
openspec_changes:
  - change_id: improve-media-maintenance-storage-unreachable-summary
    type: update
    status: archived
open_questions: []
decisions:
  - 本 Change 覆盖生产媒体维护对象相关 dry-run 入口，不新增 UI/API/DB。
  - 对象存储不可达采用首次确认后短路对象相关扫描，并返回 blocked 摘要。
  - 摘要可保留已完成的安全数据库计数，但对象维度必须标记 blocked。
  - recommended_action 先提供通用排查顺序；更细 provider 错误分类留给实现阶段在不泄密前提下扩展。
```
