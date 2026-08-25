---
requirement_id: REQ-0122-batch-image-processing-runbook
title: 批量图片处理 Runbook
terminal: multi
version: v1
status: done
owner: product
source: capture.md
priority: P1
parent_requirement: REQ-0115-media-multi-variant-images
created_at: 2026-08-25 09:21:44
updated_at: 2026-08-25 14:53:29
related_change: add-batch-image-processing-runbook
---

# REQ-0122 批量图片处理 Runbook

## 1. 需求背景

媒体图片能力已经包含对象存储 key 规范、生产媒体维护任务、多规格 `thumbnail / display / original` 展示图和 WebP 派生图等能力。随着生产历史媒体对象、缩略图补齐、派生图生成和对象 key 迁移场景增多，单靠零散脚本说明难以支撑可审计、可复跑、可回滚的生产操作。

批量图片处理具备明显的生产风险：可能同时写数据库、写对象存储、改变端侧展示 URL 或影响已有媒体对象访问。执行者需要在操作前确认环境、备份、dry-run、权限和执行窗口；执行后需要提供对象存储抽样、接口或数据库校验、Web/小程序展示验证和失败清单。

本需求用于新增一份批量图片处理 Runbook，并明确长期技术文档与版本使用文档快照都需要投影：长期事实源沉淀在 `docs/`，对外或交付版本快照在 `releases/vX.Y.Z/usage-docs/` 中继承或投影。两类文档必须能追溯同一 Runbook 来源，避免版本发布时只存在临时操作说明或历史语义漂移。

## 2. 目标用户

| 角色 | 诉求 |
|---|---|
| 实施 / 运维 | 能按标准步骤执行批量图片转换、派生图生成、缩略图重建和对象 key 迁移，并具备明确回滚边界。 |
| 发布负责人 | 能确认 Runbook 与当前版本发布、部署矩阵、镜像证据和产品使用文档快照一致。 |
| 后端 / 媒体能力开发 | 能把脚本参数、对象 key、数据库回填、对象存储写入和失败处理边界解释清楚，减少口头交接。 |
| 测试 / 验收 | 能依据 Runbook 收集 dry-run、apply、对象存储、接口/数据库和端侧展示证据。 |
| 产品 / 业务负责人 | 能理解批量图片处理影响哪些展示链路，以及生产执行前后需要哪些人工确认。 |

## 3. 范围

### 3.1 本期包含

- 新增批量图片处理 Runbook 的 PRD、后续完整需求文档和 OpenSpec Change 输入。
- Runbook 覆盖图片转换脚本、`thumb/display` 派生生成、缩略图专项重建、对象 key 迁移、生产执行步骤、安全门禁和验收证据。
- 明确 Runbook 长期技术文档归属 `docs/`，并在需要生成或更新版本产品使用文档时投影到 `releases/vX.Y.Z/usage-docs/`。
- 明确 Runbook 与 `REQ-0115-media-multi-variant-images`、对象存储 key 规范、生产媒体维护任务和版本化使用文档治理的关联。
- 明确 Runbook 不得包含真实 `.env`、密钥、生产私有域名、Authorization header、Cookie、本机绝对路径或真实客户数据。
- 明确 Runbook 需要提供操作前、dry-run、apply、回滚和验收证据模板。
- 明确 Runbook 中每个处理任务对 API、数据库、Orval、Docker Compose、对象存储、Web、小程序和管理端的影响说明；不涉及项必须写“不涉及”。

### 3.2 本期不包含

- 不在 `/req-generate` 阶段直接生成最终 Runbook 正文。
- 不直接修改脚本、后端、前端、小程序、Docker Compose、OpenSpec spec 或发布产物。
- 不直接执行生产批量图片处理、对象迁移、缩略图重建或数据库写入。
- 不新增独立图片处理平台、可视化运维控制台、定时任务平台或云资源编排。
- 不新增视频转码、视频压缩、多清晰度、OCR、PDF 首页渲染缩略图等图片处理范围外能力。
- 不将 `releases/vX.Y.Z/usage-docs/` 作为长期 Runbook 唯一事实源；发布快照只能继承或投影长期事实。
- 不允许将真实生产执行报告、数据库备份、对象存储导出包或客户媒体对象提交到仓库。

## 4. 功能要求

### FR-001 Runbook 文档归属与投影

系统 MUST 新增批量图片处理 Runbook，并明确长期技术文档和版本使用文档快照双归属。

长期技术文档 SHOULD 位于 `docs/` 下合适的媒体、对象存储、部署或运维文档归属中，作为当前 Runbook 事实源。版本发布需要公开或交付使用文档时，Runbook MUST 投影或继承到 `releases/vX.Y.Z/usage-docs/`，并通过 manifest 记录来源、版本、更新时间和适用范围。

`releases/vX.Y.Z/usage-docs/` 中的 Runbook 快照不得反向覆盖长期技术文档，不得改写旧版本历史语义。若旧版本 Runbook 需要内容性更正，MUST 按版本化产品使用文档治理记录更正原因、范围和确认来源。

### FR-002 图片转换脚本说明

Runbook MUST 覆盖图片转换脚本的使用方式，包括输入范围、支持格式、输出格式、目标尺寸或体积策略、执行模式、日志位置和失败处理。

脚本说明 MUST 区分只读审计、dry-run 和写入型 apply。任何写对象存储或写数据库的命令示例 MUST 要求显式 apply 参数，并在执行前提示备份和安全门禁。

Runbook MUST 说明脚本是否仅使用现有能力，或需要后续新增/改造脚本。若脚本能力尚不存在，Runbook MUST 标注为后续治理范围，不得把未交付命令写成可直接生产执行的事实。

### FR-003 `thumb/display` 派生生成

Runbook MUST 说明 `thumbnail`、`display`、`original` 三类资源的生成关系、对象 key 规则、MIME/格式策略、尺寸或体积目标、失败降级和字段回填边界。

派生生成步骤 SHOULD 覆盖新上传图片和存量图片两类场景。存量图片处理 MUST 提供 dry-run 输出，包括待处理记录数、预计生成对象、跳过原因、目标 key 冲突和对象存储不可达摘要。

派生对象生成 MUST 遵守对象存储单 Bucket + 标准前缀策略，不得绕过后端媒体模块和对象存储适配层拼接不一致 key。

### FR-004 缩略图专项重建

Runbook MUST 提供缩略图专项重建章节，覆盖品牌 Logo、证书图片、SKU 商品图、Banner 或其他适用媒体类型。

专项重建 MUST 支持按媒体类型、业务对象、对象前缀、缺失派生图、失败记录或数量限制筛选范围。重复执行时 SHOULD 具备幂等性，已存在且符合规则的缩略图应跳过或按显式参数重建。

缩略图重建验收 MUST 覆盖缩略图真实存在、大小或体积收益、原图访问不受影响、端侧普通展示不再加载大图或原图的证据。

### FR-005 对象 key 迁移

Runbook MUST 覆盖对象 key 迁移的标准流程，包括迁移前盘点、映射规则、目标 key 冲突检查、dry-run、apply、数据库引用回填、兼容读取、回滚和二次审计。

对象 key 迁移 MUST 明确哪些前缀、媒体类型或历史对象属于本次迁移范围，哪些对象只审计不迁移。涉及 `files/` 与 `images/` 分类边界时，Runbook MUST 明确图片、PDF/文档证书和其他文件的归属规则。

迁移命令和报告 MUST 使用脱敏对象标识、统计和样例 hash，不得输出真实客户数据、对象存储密钥、私有 URL 或本机绝对路径。

### FR-006 生产执行步骤

Runbook MUST 提供生产执行步骤，至少覆盖：

- 执行环境确认，包括生产服务器或受控堡垒环境、Compose 文件、镜像版本、数据库类型和对象存储 provider。
- 执行前备份，包括 MySQL 快照或等价可恢复备份，以及对象存储 bucket、prefix 或受影响对象集合快照。
- dry-run 执行和结果复核，包括影响数量、失败摘要、风险提示和人工确认。
- apply 执行，包括执行窗口、分批参数、幂等策略、失败中止条件和日志保留。
- 执行后验收，包括对象存储抽样、数据库/接口校验、端侧展示检查、失败对象清单和回滚判断。
- 收尾记录，包括执行人、执行时间、命令参数、镜像 tag、Runbook 版本、证据路径和人工确认结论。

生产执行步骤 MUST 明确禁止在未备份、未 dry-run、未确认环境或未授权的情况下执行写入型命令。

### FR-007 安全门禁

Runbook MUST 建立安全门禁清单。门禁至少包括：

- 禁止提交真实 `.env`、密钥、数据库连接串、Authorization header、Cookie、本机绝对路径和真实客户数据。
- 禁止使用用户原始文件名作为对象 key。
- 禁止前端、管理端或小程序绕过后端鉴权直接访问未授权对象存储。
- 生产对象存储访问 MUST 使用最小权限凭据，并区分只读审计、写入对象、删除对象等权限。
- 写入型操作 MUST 要求 dry-run 通过、备份完成和人工确认。
- 删除对象或清理历史对象 MUST 作为高风险动作单独确认，不得混入普通迁移或重建步骤。
- 日志和报告 MUST 脱敏，不得泄露内部路径、私有 endpoint、密钥或客户身份信息。

### FR-008 验收证据模板

Runbook MUST 提供验收证据模板，支持批量图片处理完成后回填。

验收证据 SHOULD 覆盖：

- 执行摘要：任务类型、Runbook 版本、执行环境、命令参数、dry-run 与 apply 结果。
- 对象存储抽样：源 key、目标 key、对象存在性、MIME、大小、权限、派生关系和失败对象清单。
- 数据库或接口校验：记录字段、URL 字段、对象 key 字段、状态字段和错误码摘要。
- 端侧展示验证：管理端、店主 Web、小程序的列表、详情、预览或证书场景。
- thumbnail/display 收益：缩略图与展示图的体积、加载或展示收益说明。
- 安全复核：日志脱敏、密钥未泄露、真实客户数据未提交、对象存储权限未放宽。
- 回滚判断：是否需要回滚、是否保留失败项、是否需要后续 BUG 或 REQ。

验收模板 MUST 支持写明 blocked 补证项，不能因缺少生产截图或日志而伪造验收通过。

### FR-009 影响矩阵

Runbook MUST 对每类批量图片处理任务给出影响矩阵，覆盖 API、数据库、Orval、Docker Compose、对象存储、Web、小程序和管理端。

当某项不受影响时，Runbook MUST 明确写“不涉及”；当存在影响时，MUST 说明需要同步的文档、测试、OpenAPI/Orval、schema、部署说明或发布证据。

## 5. UI 约束

本需求默认不新增用户可见 UI，也不要求管理端新增可视化批处理页面。

Runbook 中如描述管理端、店主 Web 或小程序验收截图，应仅作为验收证据入口，不引入新的 UI 行为。若后续需要新增管理端批处理任务页、审计报告页、下载入口或状态看板，MUST 单独在 OpenSpec Change 中声明页面范围、权限边界、Design System 复用策略和脱敏规则。

命令行输出和文档表格 SHOULD 保持紧凑、可复制、可审计。任何 UI、日志或文档展示不得暴露对象存储密钥、真实生产私有域名、内部绝对路径、异常堆栈或客户身份信息。

## 6. 关联需求

| 关联项 | 关系 | 说明 |
|---|---|---|
| REQ-0012-object-storage-key-layout | 前置规则 | Runbook 中对象 key 迁移、前缀分类和单 Bucket 策略必须遵守该需求。 |
| REQ-0097-prod-compose-media-maintenance-job | 前置运维能力 | Runbook 生产执行步骤需复用生产维护任务的安全执行边界。 |
| REQ-0115-media-multi-variant-images | 父需求 | Runbook 需要覆盖 `thumbnail / display / original` 多规格图片能力和存量批量生成。 |
| REQ-0120-webp-derived-image-variants | 关联派生能力 | Runbook 需要覆盖 WebP 派生图生成、重建和验收证据。 |
| REQ-0088-versioned-product-usage-docs | 文档投影 | Runbook 需要在版本使用文档快照中投影或继承。 |
| `rules/media.md` | 关联规范 | 后续实现需同步媒体处理、派生图、验收和脚本说明边界。 |
| `rules/object-storage.md` | 关联规范 | 后续实现需同步对象 key、对象存储访问和迁移边界。 |
| `rules/document-governance.md` | 文档治理 | Runbook 长期文档与版本快照需要遵守事实唯一归属和版本投影规则。 |

## 7. 状态块

```yaml
requirement_id: REQ-0122-batch-image-processing-runbook
status: done
lifecycle_stage: archive
readiness: Partially Ready
next_command: /opsx-archive REQ-0122-batch-image-processing-runbook
iteration: sprint-025
related_change: add-batch-image-processing-runbook
openspec_changes:
  - change_id: add-batch-image-processing-runbook
    type: add
    status: archived
decisions:
  runbook_projection: docs_and_release_usage_docs
open_questions:
  - 批量处理脚本是否仅记录现有脚本用法，还是需要新增或改造脚本能力。
  - 对象 key 迁移是否要求支持生产可回滚执行，还是仅提供人工操作指南和验收模板。
  - Runbook 首个落地版本应绑定哪个产品版本的 usage-docs 快照。
notes:
  - 已确认 Runbook 最终归属为长期技术文档和版本使用文档快照两者都需要投影。
  - 已补齐 user-stories、business-flow、acceptance 和 trace 扩展信息；OpenSpec Change 已创建为 add-batch-image-processing-runbook。
  - Readiness 为 Partially Ready：命中的 media-upload best-practice 为 draft，且本需求默认不新增 UI 原型。
  - 评审已通过且已纳入 sprint-025，OpenSpec Change 已 apply，后续可执行 /opsx-archive REQ-0122-batch-image-processing-runbook。
```
