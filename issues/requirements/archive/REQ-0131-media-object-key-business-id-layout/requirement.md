---
requirement_id: REQ-0131-media-object-key-business-id-layout
title: 统一媒体对象 Key 按业务对象 id 分目录
terminal: multi
version: v1
status: done
owner: product
source: capture.md
priority: P1
parent_requirement: REQ-0012-object-storage-key-layout
created_at: 2026-08-29 19:18:29
updated_at: 2026-08-29 23:24:36
related_change: update-media-object-key-business-id-layout
---

# REQ-0131 统一媒体对象 Key 按业务对象 id 分目录

## 1. 需求背景

当前媒体对象存储已采用单 Bucket + 标准前缀策略。SKU 图片和 SKU 视频已具备 `pending` 到 `tiles/{tile_id}` 正式目录的生命周期治理；品牌 Logo、品牌证书、Banner、头像等媒体则主要按资源类型目录与 uuid 文件名组织。

这种差异在运行上可用，但在长期治理上容易产生两个问题：一是新增媒体类型时不清楚是否需要按业务对象 id 分目录；二是生产迁移、缩略图回填、对象审计和问题排查时，无法从 key 结构稳定判断媒体与业务对象的归属关系。

本需求用于统一媒体对象 Key 的业务 id 目录策略，将所有新增媒体类型纳入“上传前 pending、保存后 formalize、读取保持旧 key 兼容、迁移必须可审计”的规则，并同步补齐文档、规范和验收口径。

## 2. 目标用户

| 角色 | 诉求 |
|---|---|
| 企业管理端用户 | 上传 Logo、证书、Banner、SKU 图片和视频后，媒体能稳定归属到对应业务对象，不影响后续展示。 |
| 微信小程序用户 | 商品、品牌、证书等媒体展示不因对象 Key 调整出现 404、空白图或加载异常。 |
| 店主 / 展示端访问者 | 公开媒体 URL 在升级后保持可读，历史图片和文件继续可展示。 |
| 后端 / 媒体能力开发 | 有统一的对象 Key 目录矩阵、生成方法、formalize 流程和旧 key 兼容边界。 |
| 实施 / 运维 | 能按 dry-run、apply、二次审计、回滚边界执行历史对象迁移。 |
| 测试 / 发布负责人 | 能用统一验收模板验证 key、object、URL、render、迁移和兼容性。 |

## 3. 需求目标

- 统一所有媒体对象 Key 的业务对象 id 目录策略。
- 明确“业务对象 id”默认等于业务表主键，例如 `user_id`、`brand_id`、`banner_id`、`tile_id`、`certificate_id`。
- 对业务对象创建前上传的媒体，建立统一 `pending` 暂存与保存后 formalize 规则。
- 保持旧媒体读取兼容，避免旧版本媒体显示因 Key 策略调整中断。
- 提供存量媒体迁移的 dry-run、apply、二次审计、幂等和回滚边界。
- 补齐对象 Key 策略矩阵、媒体规范、对象存储规范、维护 Runbook 和 OpenSpec 规格。
- 明确 API、DB、Orval、Task Trace、请求日志、Web、小程序和发布验收影响。

## 4. 范围

### 4.1 本期包含

| 范围 | 说明 |
|---|---|
| 对象 Key 策略矩阵 | 覆盖头像、品牌 Logo、Banner 图片、SKU 图片、SKU 视频、品牌证书图片、品牌证书 PDF/文档和后续媒体类型。 |
| 业务 id 目录规则 | 明确每类媒体的业务对象 id、正式目录、暂存目录、正式化触发和派生图位置。 |
| 新上传 key 生成 | 新上传或新保存媒体按业务对象 id 目录生成或正式化。 |
| 旧媒体读取兼容 | 旧 key 继续可通过数据库保存引用和 `/media/{object_key}` 或等价受控 URL 读取。 |
| 存量迁移策略 | 提供历史对象从旧目录迁移到业务 id 目录的 dry-run、apply、二次审计、幂等和回滚要求。 |
| 派生图同步 | 图片原图、`.thumb.webp`、`.display.webp` 必须保持同一业务对象目录或等价可追溯目录。 |
| 文档与规范落地 | 同步长期文档、rules、media runbook、OpenSpec specs 和发布验收口径。 |
| 观测与审计 | 上传、formalize、迁移和维护任务必须记录脱敏 Trace、请求日志或维护摘要。 |

### 4.2 本期不包含

| 不包含 | 说明 |
|---|---|
| 直接删除旧对象 | 旧对象清理必须单独确认，不混入普通迁移。 |
| 破坏旧客户端 URL | 前端、小程序和历史 API 响应不得被迫按新路径重新拼接 URL。 |
| 前端直连对象存储 | 仍禁止前端、管理端或小程序绕过后端鉴权直接写入对象存储。 |
| 新建媒体资产中心 | 本需求聚焦 Key 策略和兼容迁移，不默认建设独立 UI 管理平台。 |
| 视频转码、多清晰度播放 | 只涉及视频对象 Key 目录，不新增视频转码或多清晰度能力。 |
| 生产立即全量迁移 | PRD 阶段不执行生产迁移；后续 Change 必须提供受控步骤和人工确认。 |
| 保存完整 object key 到日志 | 维护输出、Trace 和请求日志只记录脱敏 key 摘要、前缀、hash、数量和失败分类。 |

## 5. 功能要求

### FR-001 业务对象 id 目录模型

- 系统 MUST 定义统一的媒体对象 Key 目录模型。
- “业务对象 id”默认 MUST 使用业务表主键或等价稳定对象 id。
- 同一媒体对象的原图、缩略图、展示图或文件派生对象 MUST 能追溯到同一业务对象。
- 目录模型 MUST 区分租户、媒体大类、业务对象类型、业务对象 id 和媒体用途。
- 新 Key MUST 不使用用户原始文件名、临时路径、本机绝对路径或不可脱敏业务文本。
- Key 生成 MUST 由后端媒体服务负责，客户端不得提交最终对象存储路径。

建议目标矩阵如下，后续完整文档可在 OpenSpec 阶段确认：

| 媒体类型 | 业务对象 id | 目标目录 |
|---|---|---|
| 用户头像 | `user_id` | `images/default/user-avatars/{user_id}/{uuid}.{ext}` |
| 品牌 Logo | `brand_id` | `images/default/brand-logos/{brand_id}/{uuid}.{ext}` |
| Banner 图片 | `banner_id` | `images/default/banners/{banner_id}/{uuid}.{ext}` |
| SKU 图片 | `tile_id` | `images/default/tiles/{tile_id}/{uuid}.{ext}` |
| SKU 视频 | `tile_id` | `videos/default/tiles/{tile_id}/{uuid}.{ext}` |
| 品牌证书图片 | `certificate_id` | `images/default/brand-certificates/{certificate_id}/{uuid}.{ext}` |
| 品牌证书 PDF/文档 | `certificate_id` | `files/default/brand-certificates/{certificate_id}/{uuid}.{ext}` |

### FR-002 pending 与 formalize 生命周期

- 当媒体上传时业务对象 id 已存在，系统 SHOULD 直接生成正式业务 id 目录 Key。
- 当媒体上传时业务对象 id 尚不存在，系统 MUST 使用对应媒体类型的 `pending` 目录。
- 业务对象保存成功后，系统 MUST 将 pending 媒体 formalize 到正式业务 id 目录，并同步业务表中的媒体引用。
- formalize MUST 同步处理原图、缩略图、展示图和必要的文件元数据。
- formalize 失败 MUST 返回可诊断错误或记录可追踪失败原因，不得让业务记录引用不存在对象。
- 重复 formalize MUST 幂等，已迁移成功的对象不得被重复破坏。

### FR-003 旧媒体读取兼容

- 系统 MUST 保持旧 key 的受控读取兼容。
- 旧版本数据库中已保存的 `object_key`、`file_key`、`logo_object_key`、`avatar_object_key` 等引用，仍 MUST 可通过 `/media/{object_key}` 或等价受控 URL 读取。
- 展示链路 MUST 优先消费后端返回的 URL 或数据库保存的完整 key，不得按新目录规则重新推导旧媒体路径。
- 旧 key 兼容策略 MUST 明确支持周期、迁移前后显示行为和异常降级。
- 若对象不存在、权限异常或派生图缺失，系统 MUST 返回或展示明确 fallback，而不是因新目录策略静默 404。

### FR-004 存量媒体迁移

- 系统 MUST 提供存量媒体迁移方案，用于将历史资源类型目录 key 迁移到业务 id 目录。
- 迁移 MUST 覆盖原图、缩略图、展示图、视频对象和证书文件等关联对象。
- 迁移 MUST 默认 dry-run，输出待迁移数量、跳过数量、失败分类、目标冲突、对象缺失和风险摘要。
- apply MUST 显式触发，并要求数据库备份和对象存储 bucket/prefix 备份已完成。
- 迁移 MUST 支持二次审计，确认数据库引用、对象存在性、URL 可读性和端侧展示不回退。
- 迁移 MUST 幂等复跑，已迁移或不适用对象必须可解释跳过。
- 旧对象删除或清理 MUST 作为单独高风险动作确认，不得默认执行。

### FR-005 派生图同目录归属

- 图片媒体的 `.thumb.webp` 与 `.display.webp` MUST 与原图位于同一业务对象目录或等价可追溯目录。
- 迁移原图时 MUST 同步迁移已存在的派生图，或在迁移后通过维护任务补齐。
- 派生图不存在或生成失败时，系统 MUST 记录脱敏 warning、Task Trace span 或维护任务失败分类。
- 列表、卡片、小 Logo 和证书卡片目标场景不得把原图 fallback 写作性能验收通过。
- PDF/文档类证书不得生成图片缩略图或展示图，除非后续独立需求明确引入 PDF 首图渲染能力。

### FR-006 API、URL 与客户端边界

- API 响应 MUST 继续返回受控媒体 URL 或可生成受控 URL 的 key 字段。
- 客户端 MUST 消费后端返回字段，不得拼接对象存储 endpoint、bucket 或业务 id 目录。
- 若 API 字段、URL 语义或响应结构变化，MUST 同步 OpenAPI、Orval、API 文档和前后端测试。
- 后端 MUST 区分原图 URL、缩略图 URL、展示图 URL、文件预览 URL 和对象存储直出 URL。
- 错误响应不得暴露 raw object URL、对象存储凭据、内部 endpoint、bucket 权限细节或完整 object key。

### FR-007 数据库引用与一致性

- 数据库仍以业务表媒体字段保存媒体事实引用，字段包括但不限于 `object_key`、`file_key`、`logo_object_key`、`avatar_object_key`、`image_object_key`。
- 若引入额外媒体映射表、迁移状态表或对象别名表，MUST 同步 SQLite/MySQL schema、迁移、数据库设计文档和测试。
- 业务记录写入非空媒体 key 前 SHOULD 校验对象存在；关键身份或公开展示媒体 SHOULD 校验受控 URL 可读。
- 迁移时 MUST 保证数据库引用与对象存储目标 key 一致，避免记录指向旧 key 但对象只存在新目录。
- 数据库和对象存储之间的 drift 必须可通过审计脚本或维护任务识别。

### FR-008 文档、规范和发布治理

- 本需求落地时 MUST 更新对象 Key 策略矩阵，并明确每类媒体是否支持 pending、formalize、迁移和派生图。
- 文档同步 SHOULD 覆盖 `rules/object-storage.md`、`rules/media.md`、`docs/07-object-storage-strategy.md`、`docs/standards/batch-image-processing-runbook.md`、OpenSpec object-storage/media specs 和发布验收模板。
- 文档 MUST 明确旧 key 兼容与清理边界，不得让旧媒体显示风险仅存在于实现代码中。
- 发布前 MUST 记录 key、object、URL、render、migration、rollback 的验收摘要。
- 版本使用文档或 Runbook 投影不得包含真实 `.env`、密钥、生产私有域名、本机绝对路径或真实客户数据。

### FR-009 观测、审计与脱敏

- 上传、formalize、迁移和维护任务 SHOULD 接入 Task Trace 或等价维护摘要。
- 请求日志、任务链路和维护输出 MUST 使用稳定 `resource_type`、`resource_id`、状态、数量、失败分类和脱敏 key 摘要。
- 日志和报告不得保存完整 object key、完整请求体、完整响应体、Authorization header、Cookie、Token、access key、secret key 或真实 `.env` 内容。
- 维护任务失败必须能区分对象存储不可达、object missing、target exists、DB update failed、thumbnail missing、display missing、unsupported media type 等分类。
- 产品数据采集失败不得阻断主业务流程；但迁移审计失败不得被当作迁移通过。

## 6. UI / UE 约束

- 本需求默认不新增用户可见 UI。
- 管理端上传、编辑、预览、列表回显和删除入口的现有交互不应因 Key 策略变化而回退。
- 小程序和店主展示端不应感知对象 Key 目录变化，用户可见表现应保持媒体正常展示、预览和失败占位。
- 若后续新增迁移任务页面、审计报告页或媒体资产管理页，必须单独声明 UI 范围、权限、Design System 复用和脱敏展示规则。
- 用户界面不得展示 object key、内部路径、对象存储 endpoint、bucket、异常堆栈或维护脚本内部输出。

## 7. 非功能约束

- MUST 继续遵守 MinIO/S3 兼容对象存储单 Bucket 策略。
- MUST 继续通过后端授权上传和受控媒体读取，禁止客户端未授权直连对象存储。
- MUST 保持上传 MIME、扩展名、大小、权限和对象 key 安全校验。
- MUST 保持新旧 key 的读取兼容与可回滚迁移路径。
- MUST 支持 SQLite 本地/demo 与 MySQL 生产环境的引用一致性验证。
- MUST 为生产迁移提供备份、dry-run、apply、二次审计和失败恢复说明。
- SHOULD 避免一次性全量迁移导致长事务、大量对象复制或不可控代理流量。
- SHOULD 支持按媒体类型、业务对象、数量限制或前缀分批迁移。

## 8. 关联需求与规范

| 关联项 | 关系 | 说明 |
|---|---|---|
| REQ-0012-object-storage-key-layout | 父需求 | 本需求是对象存储 Key 布局的进一步统一。 |
| REQ-0115-media-multi-variant-images | 关联能力 | 图片派生图必须保持同一业务对象目录或可追溯目录。 |
| REQ-0122-batch-image-processing-runbook | 关联运维 | 存量对象迁移、二次审计和回滚步骤需要投影到 Runbook。 |
| REQ-0130-media-maintenance-progress-output | 关联运维 | 批量迁移和审计需要进度、失败分类和脱敏摘要。 |
| `rules/object-storage.md` | 关联规范 | 需要同步单桶、前缀、业务 id 目录和旧 key 兼容规则。 |
| `rules/media.md` | 关联规范 | 需要同步媒体上传、派生图、证书图片/PDF 分流和验收规则。 |
| `docs/07-object-storage-strategy.md` | 关联文档 | 需要补齐完整媒体 Key 策略矩阵和迁移说明。 |
| `docs/standards/product-data-collection-observability.md` | 横切门禁 | 上传、迁移、维护任务和请求日志需声明适用层级与脱敏边界。 |

## 9. 状态块

```yaml
requirement_id: REQ-0131-media-object-key-business-id-layout
status: done
lifecycle_stage: review
readiness: Partially Ready
next_command: /opsx-archive REQ-0131-media-object-key-business-id-layout
iteration: sprint-027
related_change: update-media-object-key-business-id-layout
openspec_changes:
  - change_id: update-media-object-key-business-id-layout
    type: update
    status: archived
product_data_collection_observability:
  applicable: true
  affected_layers:
    - request_logs
    - task_traces
    - task_trace_spans
    - backend_api
    - web_admin_request_flow
    - wechat_miniapp_request_flow
    - maintenance_jobs
  reason: 本需求涉及媒体上传、业务对象保存后 formalize、存量对象迁移、维护任务审计、受控媒体 URL 和数据库媒体引用一致性，需要记录请求日志、任务链路、流程节点和脱敏维护摘要。
  validation: 已在 requirement.md、trace.md 与 acceptance.md 声明适用层级；后续 OpenSpec Change 必须补齐具体字段、脱敏规则、测试和验收证据。
decisions:
  key_layout_direction: all_media_business_id_directory
  legacy_read_compatibility: required
  migration_mode: dry_run_apply_audit_with_backup
open_questions:
  - 业务对象创建前上传是否所有媒体统一进入 pending 目录，还是部分媒体改为保存业务对象后再上传。
  - 存量媒体是否要求在首个版本中迁移，还是先只改新上传并保留旧 key 兼容。
  - 旧对象保留周期、清理窗口和回滚责任由谁确认。
  - 是否新增媒体别名表或迁移状态表，还是继续只更新既有业务字段。
notes:
  - 已根据 capture 生成 requirement.md。
  - 已补齐 user-stories、business-flow、acceptance、trace 扩展信息和无新增 UI 的原型策略。
  - 本需求不执行对象迁移、不修改上传代码、不改 OpenSpec specs。
  - Readiness 为 Partially Ready：命中的 media-upload best-practice 为 draft，且本需求默认不新增 UI 原型 PNG。
```
