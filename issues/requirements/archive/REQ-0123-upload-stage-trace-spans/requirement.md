---
requirement_id: REQ-0123-upload-stage-trace-spans
title: 上传链路阶段级耗时写入 trace spans
terminal: web-admin
version: v1
status: done
owner: product
source: capture.md
priority: P1
parent_requirement: REQ-0115-media-multi-variant-images
created_at: 2026-08-25 18:40:27
updated_at: 2026-08-27 23:07:46
related_change: add-upload-stage-trace-spans
---

# REQ-0123 上传链路阶段级耗时写入 trace spans

## 1. 需求背景

近期头像上传链路出现小文件上传耗时异常，排查时只能从接口耗时、对象存储写入日志和人工复现结果中拼接判断。当前媒体上传链路已经包含文件读取、原图写入、缩略图生成、缩略图写入、展示图生成、展示图写入等多个阶段，但缺少一份可被任务追踪系统稳定消费的阶段级耗时事实源。

仅依赖日志会让排查成本偏高：日志可能分散在不同模块，无法稳定绑定同一次上传任务，也不便于后续在管理端、维护任务或 AI 分析中按阶段统计。将关键阶段耗时写入 task trace spans，可以让头像上传和通用图片上传在发生慢上传、对象存储抖动、图片生成耗时异常或派生对象失败时快速定位瓶颈。

本需求用于明确上传链路的阶段级可观测性能力：头像上传和通用图片上传都需要产出结构化 trace spans，至少覆盖 `file_read`、`original_put_object`、`thumbnail_generate`、`thumbnail_put_object`、`display_generate`、`display_put_object` 六个阶段。日志仍可保留，但不能作为唯一事实源。

## 2. 目标用户

| 用户 | 诉求 |
|---|---|
| 企业管理端用户 | 上传头像、品牌图、SKU 图等图片时获得稳定体验；异常时能被快速定位并修复。 |
| 后端 / 媒体能力开发 | 能按阶段判断慢上传来自文件读取、对象存储写入、图片派生生成还是派生对象写入。 |
| 运维 / 发布负责人 | 能在发布验收、线上排障和对象存储波动排查时查看结构化耗时证据。 |
| 测试负责人 | 能围绕两条上传分支和六个关键阶段收集一致的回归证据。 |
| 产品 / 项目负责人 | 能判断上传性能问题是个别缺陷、基础设施波动还是媒体处理能力瓶颈。 |

## 3. 需求目标

- 头像上传链路 MUST 记录阶段级耗时 trace spans。
- 通用图片上传链路 MUST 记录阶段级耗时 trace spans。
- trace spans MUST 至少覆盖 `file_read`、`original_put_object`、`thumbnail_generate`、`thumbnail_put_object`、`display_generate`、`display_put_object`。
- 每个 span MUST 能表达阶段名称、耗时、成功/失败状态和失败错误摘要。
- 已完成阶段的 spans MUST 在后续阶段失败时仍可追踪。
- 日志 MAY 继续输出阶段信息，但 task trace spans MUST 是阶段耗时的结构化事实源。
- 后续实现 SHOULD 复用现有 task trace 能力；若现有结构不足，必须在 OpenSpec 阶段明确 API、DB、Schema 和兼容性影响。

## 4. 范围

### 4.1 本期包含

| 范围 | 说明 |
|---|---|
| 头像上传分支 | 管理端当前登录用户头像上传需要记录阶段级 spans。 |
| 通用图片上传分支 | 复用媒体上传能力的通用图片上传入口需要记录阶段级 spans。 |
| 文件读取阶段 | 记录从上传文件流读取到后端可处理内容的耗时，阶段名为 `file_read`。 |
| 原图写入阶段 | 记录原图对象写入对象存储的耗时，阶段名为 `original_put_object`。 |
| 缩略图生成阶段 | 记录 thumbnail 派生图生成耗时，阶段名为 `thumbnail_generate`。 |
| 缩略图写入阶段 | 记录 thumbnail 派生对象写入对象存储的耗时，阶段名为 `thumbnail_put_object`。 |
| 展示图生成阶段 | 记录 display 派生图生成耗时，阶段名为 `display_generate`。 |
| 展示图写入阶段 | 记录 display 派生对象写入对象存储的耗时，阶段名为 `display_put_object`。 |
| 失败保留 | 任一阶段失败时，已完成阶段和失败阶段的 span 仍应保留。 |
| 测试证据 | 后续实现需覆盖头像上传和通用图片上传两条分支的 span 生成与失败保留。 |

### 4.2 本期不包含

| 不包含 | 说明 |
|---|---|
| 直接修复单个慢上传缺陷 | `BUG-0142-admin-avatar-upload-storage-put-slow` 负责具体慢上传问题排查和修复；本需求提供可观测性基础。 |
| 新建独立性能监控平台 | 本期只要求写入 task trace spans，不建设独立监控后台或图表系统。 |
| 强制管理端 UI 展示 spans | 是否在管理端展示阶段耗时需后续确认；本需求先保证后端结构化 trace 可用。 |
| 改变对象 key 策略 | 本需求不改变 `thumbnail / display / original` 对象 key 和 MinIO 前缀策略。 |
| 新增前端直传对象存储 | 上传仍通过后端鉴权和对象存储适配层。 |
| 视频上传阶段追踪 | 本需求只覆盖头像上传与通用图片上传，不覆盖视频转码、封面生成或多清晰度处理。 |
| 强制新增数据库表 | 优先复用现有 task trace；若必须新增存储结构，后续 OpenSpec 阶段再明确。 |

## 5. 功能要求

### FR-001 统一 span 模型

系统 MUST 为上传链路记录结构化 trace span。每个 span SHOULD 至少包含：

| 字段 | 说明 |
|---|---|
| `name` | 阶段名称，例如 `file_read`。 |
| `duration_ms` | 阶段耗时，单位毫秒。 |
| `status` | 阶段结果，例如 `success`、`failed`、`skipped`。 |
| `started_at` / `ended_at` | 如 task trace 已支持时间戳，SHOULD 记录阶段开始和结束时间。 |
| `error_code` / `error_message` | 失败时记录脱敏错误摘要，不暴露密钥、内部路径或完整堆栈。 |
| `metadata` | 可选，记录对象规格、MIME、大小区间或跳过原因等脱敏信息。 |

span 字段命名和持久化格式 MUST 在后续 OpenSpec 阶段与现有 task trace 能力对齐，避免引入无法被现有工具读取的孤立结构。

### FR-002 头像上传分支覆盖

头像上传分支 MUST 在同一次上传任务或请求追踪中记录阶段级 spans。

- 成功路径 MUST 至少产生 `file_read` 与 `original_put_object`。
- 若头像上传链路会生成 thumbnail 或 display 派生图，MUST 记录对应 `thumbnail_generate`、`thumbnail_put_object`、`display_generate`、`display_put_object`。
- 若头像入口因业务策略不生成某类派生图，MUST 以 `skipped` 或等价方式记录跳过原因，或在后续 Change 中明确该阶段不适用。
- 头像上传失败时，已完成阶段的 spans MUST 保留，失败阶段 MUST 可定位。

### FR-003 通用图片上传分支覆盖

通用图片上传分支 MUST 在同一次上传任务或请求追踪中记录阶段级 spans。

- 成功路径 MUST 覆盖 `file_read`、`original_put_object`、`thumbnail_generate`、`thumbnail_put_object`、`display_generate`、`display_put_object`。
- 支持 WebP 派生策略的入口 SHOULD 在 span metadata 中记录派生规格或输出 MIME 的脱敏摘要。
- 对于 SVG、PDF 或不适用派生图的格式，系统 MUST 保留可定位的跳过状态或错误状态，不得静默缺失关键阶段解释。
- 通用图片上传不得因为记录 spans 而绕过文件大小、MIME Type、扩展名或鉴权校验。

### FR-004 阶段边界与计时口径

系统 MUST 明确阶段开始和结束边界，避免不同实现对耗时口径理解不一致。

推荐口径：

| 阶段 | 计时边界 |
|---|---|
| `file_read` | 从接收上传文件流读取开始，到后端获得可用于校验和处理的文件内容结束。 |
| `original_put_object` | 从调用对象存储适配层写入原图开始，到对象存储确认写入或失败结束。 |
| `thumbnail_generate` | 从开始生成 thumbnail 派生图开始，到生成结果或失败结束。 |
| `thumbnail_put_object` | 从调用对象存储适配层写入 thumbnail 开始，到对象存储确认写入或失败结束。 |
| `display_generate` | 从开始生成 display 派生图开始，到生成结果或失败结束。 |
| `display_put_object` | 从调用对象存储适配层写入 display 开始，到对象存储确认写入或失败结束。 |

后续实现 MAY 增加额外阶段，例如 `validate_file`、`db_update`、`url_build`，但不得缺少本需求要求的六个基础阶段。

### FR-005 失败与降级记录

任一阶段失败时，系统 MUST 记录失败阶段 span，并保留失败前已经完成的 spans。

- 原图写入失败时，后续派生阶段可不执行，但 trace MUST 能看到失败停在 `original_put_object`。
- 缩略图生成失败时，trace MUST 能看到 `thumbnail_generate` 的失败状态，并说明后续 `thumbnail_put_object` 是跳过还是未执行。
- 展示图生成失败时，trace MUST 能看到 `display_generate` 的失败状态，并说明后续 `display_put_object` 是跳过还是未执行。
- 派生图失败是否阻断上传结果，应继续遵守媒体多规格能力既有降级策略，并在后续 Change 中明确。
- 错误摘要必须脱敏，不得包含真实 `.env`、AccessKey、SecretKey、Authorization header、Cookie、本机绝对路径或未脱敏内部对象路径。

### FR-006 task trace 接入方式

阶段耗时 SHOULD 写入既有 task trace spans 或等价任务追踪结构，而不是只写普通日志。

- 如果现有 task trace 已支持 spans，后续实现 MUST 复用该结构。
- 如果现有 task trace 只支持文本记录或状态事件，后续 OpenSpec MUST 明确扩展方式。
- 如果上传链路当前没有 task id，后续设计 MUST 明确如何建立 trace id、request id 或 upload id 与 spans 的关联。
- 日志 MAY 输出同样的阶段耗时摘要，用于本地调试和临时排查；但验收不能只依赖日志。

### FR-007 查询、展示与接口边界

本需求优先要求后端可记录、可追踪、可测试。是否对外暴露 trace spans 需要后续阶段确认。

- 若上传接口响应新增 `trace_id`、`spans` 或耗时摘要，MUST 同步 OpenAPI、Orval、API 文档和测试。
- 若通过既有任务查询接口读取 spans，MUST 明确查询权限、响应 Schema 和错误码。
- 若仅内部可观测，不对前端暴露，后续实现记录必须说明事实源路径、测试入口和排障使用方式。
- 管理端 UI 若展示阶段耗时，MUST 使用紧凑表格或折叠明细，不展示内部对象 key、堆栈或敏感配置。

### FR-008 测试与验收证据

后续实现 MUST 提供聚焦测试，证明两条上传分支都能产出 spans。

- 头像上传成功路径测试 SHOULD 验证阶段名称集合和耗时字段存在。
- 通用图片上传成功路径测试 MUST 验证六个基础阶段均出现。
- 对象存储写入失败测试 SHOULD 验证失败阶段和已完成阶段均被保留。
- 派生图生成跳过或失败测试 SHOULD 验证 `skipped` / `failed` 状态和脱敏错误摘要。
- 若 API 或 DB 无变化，测试说明中 MUST 明确不需要 Orval 或迁移的原因。

## 6. UI / UE 约束

- 本需求默认不新增用户可见 UI。
- 若管理端后续展示上传 trace，应使用紧凑、可扫描的阶段列表，字段包括阶段、耗时、状态和错误摘要。
- 阶段耗时展示不应阻塞上传主流程，也不应让普通管理用户看到内部对象 key、完整堆栈或基础设施敏感信息。
- 管理端 UI 如有新增或调整，必须遵守 Design System semantic token，不得使用裸 Hex。
- 小程序和店主 Web 本期不需要展示上传阶段耗时。

## 7. 非功能约束

- MUST 遵守上传安全规则：鉴权、文件大小、MIME Type、扩展名、对象 key 安全和错误脱敏。
- MUST 继续通过后端媒体服务和对象存储适配层访问 MinIO，不得让前端直连未授权对象存储。
- MUST 遵守 MinIO 单 Bucket + 前缀策略，不因 trace spans 新增对象存储 bucket。
- SHOULD 控制 trace 写入开销，不能让阶段记录本身显著拖慢小文件上传。
- SHOULD 使用单调时钟或等价可靠计时方式记录耗时，避免系统时间跳变影响 `duration_ms`。
- SHOULD 在高并发上传时保证同一次上传的 spans 顺序和归属稳定。
- MUST 保持日志和 trace 中的错误摘要脱敏。
- 涉及 API 变更时 MUST 同步 OpenAPI / Orval / docs / tests。
- 涉及 DB 变更时 MUST 同步 SQLite/MySQL schema、数据库文档和测试；若不涉及，必须在实现记录中说明。

## 8. 数据与接口影响

| 范围 | 影响 |
|---|---|
| SQLite/MySQL | 默认优先复用现有 task trace 存储；若新增 spans 表、JSON 字段或任务记录字段，需在 OpenSpec 阶段明确 schema、迁移与回滚。 |
| Pydantic Schema | 若上传响应或任务查询响应新增 trace 字段，需同步 Schema；若仅内部记录，则不影响对外 Schema。 |
| OpenAPI / Orval | 仅在 API 响应契约变化时需要同步；如果 spans 只写入内部 task trace 且不对前端暴露，则可说明不涉及。 |
| 后端媒体模块 | 需要在头像上传与通用图片上传链路增加阶段计时和 trace span 写入。 |
| 对象存储 | 不改变对象 key 和 bucket；仅记录原图、thumbnail、display 写入阶段耗时和失败状态。 |
| Web 管理端 | 默认不新增 UI；若展示 trace，需要新增或复用查询入口。 |
| 店主 Web | 不涉及。 |
| 小程序 | 不涉及。 |

## 9. 关联需求与缺陷

| 类型 | ID / 文件 | 关系 |
|---|---|---|
| 父需求 | `REQ-0115-media-multi-variant-images` | 已建立 `thumbnail / display / original` 三规格资源模型，本需求补齐上传阶段耗时追踪。 |
| 关联需求 | `REQ-0120-webp-derived-image-variants` | WebP 派生图生成阶段需要纳入 `thumbnail_generate` 和 `display_generate` 计时。 |
| 关联需求 | `REQ-0117-media-maintenance-storage-unreachable-summary` | 媒体维护任务已有对象存储不可达摘要经验，可作为错误分类和脱敏输出参考。 |
| 关联 BUG | `BUG-0142-admin-avatar-upload-storage-put-slow` | 头像上传小文件对象存储写入慢问题暴露阶段级耗时缺口。 |
| 关联规范 | `rules/media.md` | 后续实现需遵守媒体上传、派生图和验收规则。 |
| 关联规范 | `rules/object-storage.md` | 后续实现需遵守对象存储适配层、key、bucket 和错误脱敏规则。 |

## 10. 状态块

```yaml
requirement_id: REQ-0123-upload-stage-trace-spans
status: done
lifecycle_stage: review
readiness: Partially Ready
next_command: /opsx-archive REQ-0123-upload-stage-trace-spans
notes:
  - 已根据 capture 生成 requirement.md。
  - 本需求聚焦头像上传和通用图片上传的阶段级耗时 trace spans。
  - 已补齐 user-stories、business-flow、acceptance 与 prototype 策略。
  - 已创建 OpenSpec Change `add-upload-stage-trace-spans`。
  - Readiness 为 Partially Ready：命中的 media-upload best-practice 为 draft，且本需求默认不新增独立 UI，HTML/PNG 原型暂不生成。
  - 评审已通过，并已纳入 sprint-026 正式范围。
  - 后续 req-opsx 需确认 trace spans 是否复用现有 task trace 存储结构，以及是否需要 API、DB 或管理端 UI 暴露。
```
openspec_changes:
  - change_id: add-upload-stage-trace-spans
    type: update
    status: archived
