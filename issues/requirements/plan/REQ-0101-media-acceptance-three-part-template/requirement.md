---
requirement_id: REQ-0101-media-acceptance-three-part-template
title: 媒体类需求三段验收模板
terminal: multi
version: v1
status: pending_review
owner: product
source: capture.md
priority: P1
parent_requirement:
created_at: 2026-08-06 11:20:03
updated_at: 2026-08-06 11:26:00
---

# REQ-0101 媒体类需求三段验收模板

## 1. 需求背景

Sprint 020 同时覆盖了管理端图片密集列表缩略图展示、全局缩略图生成体积策略、历史对象维护或重生成入口。媒体类能力跨越 API 字段、Orval 类型、前端列表渲染、上传链路、缩略图生成、DB 记录、对象存储 key/prefix 与维护任务，验收证据如果只按“媒体 key/object/URL/render”横向检查，容易分散在多个需求、BUG、Change 或 Sprint 报告中。

当前已有 `REQ-0090` 媒体五联验收模板和 `REQ-0091` 媒体类 BUG 四联验收模板，分别解决媒体链路通用检查和 BUG 修复闭环问题。REQ-0101 需要补齐的是更贴近缩略图与历史对象治理场景的证据组织方式：将媒体类需求与 BUG 的验收证据强制拆成“列表展示字段”“生成策略”“历史对象维护或重生成”三段，并为每段明确 API、Orval、DB、对象存储与 admin web 列表影响。

## 2. 目标用户

| 用户 | 诉求 |
|---|---|
| 产品负责人 | 在媒体类需求评审和验收时快速看清列表展示、生成策略、历史对象维护是否分别闭环。 |
| 测试人员 | 使用固定三段模板收集证据，避免只验收上传成功或 URL 可访问而遗漏列表字段、生成降级或历史重生成。 |
| 后端 / 平台开发 | 明确 media upload、缩略图生成、维护任务、DB 字段和对象存储 key/prefix 的验收责任。 |
| Web 管理端开发 | 明确列表响应字段、Orval 类型、fallback 规则和截图证据要求。 |
| 发布 / Sprint 负责人 | 在 Sprint 验收和 release note 中用统一口径说明媒体类改动的影响矩阵与遗留范围。 |

## 3. 需求目标

- 建立一份媒体类需求与 BUG 可复用的三段验收模板。
- 模板 MUST 将验收证据拆分为“列表展示字段”“生成策略”“历史对象维护或重生成”三段。
- 模板 MUST 要求每段明确 API、Orval、DB、对象存储、admin web 列表影响；不涉及时必须写明“不涉及”。
- 模板 SHOULD 与 `REQ-0090` 媒体五联验收模板、`REQ-0091` 媒体类 BUG 四联验收模板互补，而不是替代它们。
- 模板 MUST 保持轻量，适合嵌入 REQ acceptance、BUG acceptance、OpenSpec tasks、Sprint 验收报告或发布检查清单。

## 4. 范围

### 4.1 本期包含

| 范围 | 说明 |
|---|---|
| 三段证据结构 | 定义列表展示字段、生成策略、历史对象维护或重生成三段验收内容。 |
| 影响矩阵 | 要求 API、Orval、DB、对象存储、admin web 列表逐项标注是否涉及及证据要求。 |
| 适用条件 | 明确哪些媒体类 REQ/BUG 必须启用三段模板，哪些仅沿用五联或四联即可。 |
| 验收状态字段 | 每段支持 `pass`、`fail`、`n/a`、`blocked`，并要求记录证据入口和阻塞原因。 |
| 与既有模板关系 | 说明本模板与媒体五联、BUG 四联的复用边界。 |
| Sprint 020 案例沉淀 | 将缩略图列表展示、全局体积策略、历史重生成作为模板设计来源案例。 |

### 4.2 本期不包含

| 不包含 | 说明 |
|---|---|
| 新增媒体上传能力 | 本需求只定义验收模板，不新增上传接口、上传页面或上传适配层。 |
| 新增缩略图生成能力 | 不实现新的尺寸、体积、格式转换或生成策略，只要求后续相关需求说明生成证据。 |
| 新增历史对象维护任务 | 不实现扫描、dry-run、apply、重生成或迁移任务，只要求相关需求验收时记录维护证据。 |
| 修改已归档 Sprint 范围 | 不重新打开 `sprint-020`，仅将其作为模板来源案例。 |
| 替代 REQ/BUG 生命周期 | 不替代 `/req-complete`、`/bug-complete`、评审、OpenSpec 或 Workflow Sync。 |
| 强制自动化检查 | 本期定义结构化证据，不要求实现 CI、脚本、接口自动巡检或 Docker Compose 任务。 |

## 5. 功能要求

### FR-001 模板载体与触发条件

- 系统 MUST 提供一份“媒体类需求三段验收模板”，供媒体相关 REQ、BUG、OpenSpec Change、Sprint 验收和发布检查复用。
- 模板 MUST 使用 Markdown 结构，便于复制到 `acceptance.md`、BUG 验收、OpenSpec `tasks.md` 或 Sprint `acceptance-report.md`。
- 只要需求或 BUG 涉及媒体 URL、对象 key、缩略图、上传、对象存储、列表图片展示、历史资源维护任一项，模板 MUST 启用。
- 若媒体条目只涉及通用 key/object/URL/render 检查且没有列表字段、生成策略或历史对象维护，MAY 仅引用 `REQ-0090` 或 `REQ-0091`，但必须说明不启用三段模板的原因。
- 模板 MUST 不记录真实客户数据、真实密钥、内部绝对路径、Authorization header、Cookie 或 `.env` 内容。

### FR-002 列表展示字段证据段

- 模板 MUST 要求记录 admin web 列表使用的媒体字段、缩略图字段、原图字段和 fallback 字段。
- 列表展示字段段 MUST 明确 API 响应是否新增或调整字段；涉及时必须提供字段名、接口入口和响应样例或 Schema 说明。
- 列表展示字段段 MUST 明确 Orval 是否需要同步；涉及时必须记录生成结果、前端使用的类型或 API client 变化。
- 列表展示字段段 MUST 明确前端列表 fallback 规则，例如优先缩略图、缺失或失败时回退原图、仍失败时显示占位或空态。
- 列表展示字段段 SHOULD 记录至少一个列表截图、DOM/页面入口或测试断言，用于证明列表实际使用目标字段。
- 若本次媒体能力不涉及 admin web 列表，模板 MUST 记录 `n/a` 原因。

### FR-003 生成策略证据段

- 模板 MUST 要求记录缩略图或衍生媒体对象的生成触发时机，例如上传时、保存时、维护任务、手动重生成或懒生成。
- 生成策略段 MUST 明确尺寸、体积、格式、质量、命名约定和 key/URL 推导是否变化。
- 生成策略段 MUST 明确失败降级行为，例如不阻断原图上传、记录 warning、保留旧缩略图、回退原图 URL 或提示用户。
- 生成策略段 MUST 明确可观测证据，包括日志、任务追踪、错误码、测试断言或对象存储检查结果。
- 若涉及全局配置或系统设置，生成策略段 MUST 记录默认值、生效范围、增量或存量影响，以及配置变更后的生效边界。
- 若本次媒体能力不涉及新生成或重生成策略，模板 MUST 记录 `n/a` 原因。

### FR-004 历史对象维护或重生成证据段

- 模板 MUST 要求记录历史对象维护的适用范围，例如 SKU、品牌、证书、Banner、视频或其他媒体类型。
- 历史对象维护段 MUST 明确是否提供 dry-run、apply、批量范围、过滤条件、权限边界和幂等性说明。
- 历史对象维护段 MUST 明确对象存储 key/prefix 影响，包括是否保持既有 `.thumb` 或等价命名约定。
- 历史对象维护段 MUST 记录执行结果证据，例如扫描数量、成功数量、失败数量、失败原因、跳过原因和重试建议。
- 历史对象维护段 MUST 明确是否修改 DB 记录；不修改时必须写明“只改对象内容或派生对象，不改业务表记录”。
- 若本次媒体能力只影响增量上传且不处理历史对象，模板 MUST 记录“不自动重写历史对象”及后续维护入口判断。

### FR-005 影响矩阵

- 模板 MUST 包含固定影响矩阵，字段至少包括：`API`、`Orval`、`DB`、`对象存储`、`admin web 列表`。
- 每个影响项 MUST 填写 `是`、`否` 或 `待确认`，不得留空。
- 每个影响项 MUST 填写证据要求；不涉及时必须写明“不涉及原因”。
- API 涉及时 MUST 记录请求入口、响应字段、错误码或兼容性说明。
- Orval 涉及时 MUST 记录 OpenAPI 生成与前端类型同步结果。
- DB 涉及时 MUST 记录表、字段、迁移或“不改表”的判断。
- 对象存储涉及时 MUST 记录 key/prefix、object 是否写入、URL 可访问性和权限边界。
- admin web 列表涉及时 MUST 记录列表页面、字段选择、fallback 规则和截图或测试证据。

### FR-006 状态、失败和阻塞记录

- 模板 MUST 为三段证据分别提供状态：`pass`、`fail`、`n/a`、`blocked`。
- `fail` 状态 MUST 记录实际结果、期望结果、影响范围、复现入口和建议后续命令。
- `blocked` 状态 MUST 记录阻塞原因，例如测试环境缺失、对象存储不可用、体验版未上传、历史样例不足或接口尚未合并。
- 失败或阻塞记录 SHOULD 能独立转化为后续 `/bug-capture` 或 `/capture` 输入。
- 模板 SHOULD 支持一次记录多个媒体样例，但每个样例必须能独立追踪。

### FR-007 与既有媒体验收模板协同

- 模板 MUST 明确它不替代 `REQ-0090` 的 key/object/URL/thumbnail benefit/miniapp render 检查。
- 模板 MUST 明确它不替代 `REQ-0091` 的 BUG key/object/URL/render 修复闭环。
- 当媒体条目同时涉及通用链路和三段证据时，验收文档 SHOULD 先使用三段结构组织证据，再在每段中引用五联或四联检查项。
- 对 BUG 场景，模板 MUST 要求保留原 BUG 场景、修复前后对照和回归证据。
- 对需求场景，模板 MUST 要求保留业务目标、用户收益和“不包含范围”说明。

### FR-008 后续落点与工作流集成

- `/req-complete` 阶段 SHOULD 生成可直接复用的验收模板章节或 acceptance 草稿结构。
- 后续 `/req-opsx` MUST 明确最终落点，例如 `rules/media.md`、`rules/object-storage.md`、`docs/knowledge-base`、issue acceptance 模板或命令 Skill 模板。
- 若模板接入 BUG 验收流程，MUST 明确与 `/bug-complete`、`/bug-review` 的关系。
- 若模板接入 Sprint 或 Release 检查流程，MUST 明确哪些媒体变更触发三段模板，以及是否要求发布前复核。
- 模板集成不得手工编辑 Workflow Sync 管辖的 Sprint Scope marker 块。

## 6. UI / UE 约束

- 本需求本身不新增 Web 管理端、店主端或小程序页面。
- 若后续在管理端、发布工具或验收工具中展示该模板，应优先采用紧凑表格、分段检查清单或可折叠面板。
- 模板中的状态、影响矩阵和证据入口应清晰可扫读，适合产品、测试、开发共同使用。
- 如果模板最终落入 Web UI，必须遵守 Design System semantic token，不得直接写裸 Hex。
- 不应在页面中写大量解释性帮助文案；模板字段本身应足够明确。

## 7. 非功能约束

- MUST 遵守上传安全规则，不记录真实密钥、原始本地路径或真实客户数据。
- MUST 遵守 MinIO 单桶 + 前缀策略，不因模板新增 Bucket 或绕过后端适配层。
- MUST 遵守媒体模块边界，后续如实现自动化检查，应优先复用 media / object storage 相关服务或测试辅助能力。
- MUST 保持模板轻量，适合作为媒体类需求或 BUG 的验收记录，不应变成难以执行的大型审计表。
- SHOULD 为后续自动化、发布检查和 Sprint 验收保留结构化字段。

## 8. 关联需求与规范

| 类型 | ID / 文件 | 关系 |
|---|---|---|
| 关联需求 | `REQ-0090-media-five-point-acceptance-template` | 提供媒体通用 key/object/URL/thumbnail benefit/miniapp render 检查维度。 |
| 关联需求 | `REQ-0091-media-bug-four-point-acceptance-template` | 提供媒体类 BUG 修复后的 key/object/URL/render 闭环思路。 |
| 关联需求 | `REQ-0098-admin-media-list-thumbnails` | Sprint 020 中列表缩略图字段与 fallback 证据的来源案例。 |
| 关联需求 | `REQ-0099-global-thumbnail-size-limit` | Sprint 020 中生成策略、全局配置和历史重生成证据的来源案例。 |
| 关联 Sprint | `sprint-020` | 已归档 Sprint，暴露媒体验收证据分散问题。 |
| 关联规范 | `rules/media.md` | 后续模板落点可能需要补充媒体类验收规则。 |
| 关联规范 | `rules/object-storage.md` | object key、MinIO 访问和单桶策略的事实规范。 |
| 关联文档 | `docs/07-object-storage-strategy.md` | 对象存储策略与排查说明可引用三段验收模板。 |

## 9. 状态块

```yaml
requirement_id: REQ-0101-media-acceptance-three-part-template
status: pending_review
lifecycle_stage: plan
readiness: Partially Ready
next_command: /req-review REQ-0101-media-acceptance-three-part-template --approve
notes:
  - 已根据 capture 与 req-explore 结论生成 requirement.md。
  - 本需求聚焦验收模板治理，不直接修改 media upload、缩略图生成、DB、对象存储或 admin web 列表实现。
  - 已补齐 user-stories、business-flow、acceptance、trace 与 prototype 策略。
  - 命中的 best-practices 当前为 draft，因此 readiness 为 Partially Ready。
  - 后续 req-opsx 需要明确是否更新 rules/media.md、rules/object-storage.md、docs/knowledge-base 或 issue acceptance 模板。
```
