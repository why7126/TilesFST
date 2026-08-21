---
requirement_id: REQ-0111-miniapp-media-four-part-acceptance-practice
title: 沉淀小程序媒体四联验收最佳实践
terminal: multi
version: v1
status: done
owner: product
source: capture.md
priority: P1
parent_requirement:
created_at: 2026-08-12 14:26:05
updated_at: 2026-08-12 22:03:11
---

# REQ-0111 沉淀小程序媒体四联验收最佳实践

## 1. 需求背景

BUG-0125 与 BUG-0126 均暴露出同一类媒体验收盲区：媒体性能和小程序渲染验收不能只确认 `object_key` 存在、对象存储中有 object，或接口返回了 `.thumb` URL。小程序真实体验还取决于 URL 是否通过后端受控链路可访问、是否实际命中轻量资源、是否发生 fallback、DevTools / 真机 / 体验版 Network 中的资源大小和耗时是否符合预期，以及页面 render、预览、播放、占位和失败态是否闭环。

项目当前已有 `REQ-0090` 媒体五联验收模板、`REQ-0091` 媒体类 BUG 四联验收模板、`REQ-0101` 媒体类需求三段验收模板，以及 `docs/standards/miniapp-device-evidence-template.md` 的小程序设备与 Network evidence 规范。REQ-0111 不再新增一个泛化模板，而是将 BUG-0125 / BUG-0126 的实际经验沉淀为小程序媒体场景的最佳实践、验收引用入口、测试 helper 和审计 helper，使后续媒体类需求与缺陷能够按 key / object / URL / render 四联形成可复核证据链。

## 2. 目标用户

| 用户 | 诉求 |
|---|---|
| 产品负责人 | 在媒体性能需求、BUG 验收和 Sprint 验收中判断证据是否真的覆盖小程序用户体验，而不只是对象存在。 |
| 测试人员 | 使用固定四联口径和 helper 快速检查 key、object、URL、render 证据，识别 `.thumb` 回退原图、URL 可访问但加载慢、真机证据缺失等风险。 |
| 小程序开发 | 明确页面 `<image>`、预览、视频 poster、lazy-load、fallback 与 Network evidence 的验收要求。 |
| 后端 / 媒体开发 | 明确 `/media/{object_key}`、resolved key、fallback、MIME、大小、缓存响应头、审计脚本和脱敏输出的证据边界。 |
| 发布 / Sprint 负责人 | 在发布前识别仍需补齐的 DevTools、真机、体验版 Network evidence 和历史对象审计回填策略。 |

## 3. 需求目标

- 沉淀一份小程序媒体四联验收最佳实践，明确 key、object、URL、render 四个维度的证据最小集。
- 将 BUG-0125、BUG-0126 作为案例写入 `docs/knowledge-base`，说明“对象存在不等于性能验收通过”的判断原则。
- 补齐小程序 DevTools / 真机 / 体验版 Network evidence 与媒体验收模板之间的引用关系。
- 提供测试 helper，用于在自动化测试中表达小程序媒体 URL、缩略图、预览 URL、视频 poster、fallback 和页面绑定断言。
- 提供审计 helper，用于 dry-run 抽样检查历史媒体对象的 key / object / URL / render 相关风险，并输出脱敏统计摘要。
- 保持治理落点轻量，不直接实现新的上传、缩略图生成、CDN、缓存或对象存储 provider 能力。

## 4. 范围

### 4.1 本期包含

| 范围 | 说明 |
|---|---|
| 知识库沉淀 | 在 `docs/knowledge-base` 记录 BUG-0125、BUG-0126 的媒体性能验收教训、复盘结论和后续检查口径。 |
| 验收规范补充 | 补充或引用 `rules/media.md`、`rules/object-storage.md`、媒体四联模板和小程序 evidence 模板，明确小程序媒体四联证据最小集。 |
| 小程序 Network evidence 规则 | 明确 DevTools Network、真机、体验版 Network 的适用边界、必须记录字段、blocked / follow-up 处理方式。 |
| 测试 helper | 提供测试侧 helper 或断言辅助，覆盖缩略图 URL、预览 URL、视频 poster、fallback、页面绑定和媒体代理 URL 语义。 |
| 审计 helper | 提供 dry-run 审计辅助，抽样或批量检查历史媒体对象的 object 存在性、缩略图收益、URL 访问语义、fallback 标记和脱敏统计。 |
| 历史对象审计与回填策略 | 明确审计结果如何判断是否需要回填、重生成、apply、幂等验证和备份确认。 |
| 安全脱敏边界 | 明确 helper 输出不得泄露真实 object key 全量值、密钥、`.env`、Authorization header、Cookie、本机绝对路径或真实客户数据。 |

### 4.2 本期不包含

| 不包含 | 说明 |
|---|---|
| 新增媒体上传能力 | 不新增上传接口、上传 UI、前端直传或对象存储凭证下发。 |
| 新增缩略图生成能力 | 不新增尺寸、体积、格式转换、视频转码或自动生成流水线；只定义验收与审计判断。 |
| 新增 CDN / 网关缓存能力 | 不实现 CDN、反向代理缓存或生产网关配置；仅要求记录缓存证据或剩余风险。 |
| 自动真机云测 | 不新增真机自动化平台；无法执行真机时按 blocked 或 follow-up 记录。 |
| 已归档 BUG 返修 | 不重新打开 BUG-0125、BUG-0126；仅将其作为最佳实践来源案例。 |
| 生产批量写入默认执行 | 审计 helper 默认 dry-run；写入 DB 或对象存储必须另行设计 apply、备份确认和幂等验证。 |

## 5. 功能要求

### FR-001 最佳实践文档

- 系统 MUST 在 `docs/knowledge-base` 沉淀小程序媒体四联验收最佳实践。
- 文档 MUST 以 BUG-0125 和 BUG-0126 为来源案例，说明 `.thumb` URL 存在、object 存在或接口测试通过仍可能遗漏真实性能问题。
- 文档 MUST 明确 key -> object -> URL -> render 的证据链路，并说明任一环节不能替代后续环节。
- 文档 MUST 说明小程序媒体与 Web 媒体验收的差异，包括合法域名、基础库、DevTools 与真机差异、体验版 Network、组件 lazy-load、图片预览和视频 poster。
- 文档 MUST 提供可复制的验收记录片段，适合写入 REQ / BUG acceptance、OpenSpec tasks、Sprint acceptance report 或发布检查清单。

### FR-002 小程序媒体四联证据最小集

- `key` 维度 MUST 记录业务资源、媒体类型、脱敏 key 摘要、标准前缀、原图 / 缩略图 / 视频 / poster 关系。
- `object` 维度 MUST 记录 object 是否存在、MIME、大小、扩展名、权限边界、缩略图收益或无收益原因。
- `URL` 维度 MUST 记录 URL 类型、入口接口或页面、HTTP 状态、业务错误码、受控 `/media` 访问、resolved / fallback 结论和缓存相关证据。
- `render` 维度 MUST 记录小程序页面路径、组件、DevTools / 真机 / 体验版 evidence、展示 / 预览 / 播放 / 占位 / 失败态结论。
- 每个维度 MUST 使用 `pass`、`fail`、`n/a` 或 `blocked`，不得留空；`blocked` 不得视为通过。

### FR-003 Network evidence 规则

- 小程序媒体性能相关验收 MUST 至少记录 DevTools Network 或体验版 Network evidence；影响真实用户体感的高风险场景 SHOULD 补充真机 evidence。
- Network evidence MUST 记录页面路径、场景、请求域名、HTTP 状态、业务响应状态、资源加载结论、资源大小或耗时摘要。
- DevTools Network MUST 明确“不等同于体验版或真机网络验收”。
- 缺少体验版或真机条件时 MUST 标记 `blocked` 或 `follow_up`，并记录责任环境、重试条件和发布前承接方式。
- 自动化测试、静态检查、接口 smoke 或 `urlCheck=true` MUST NOT 自动替代 Network evidence。

### FR-004 测试 helper

- 系统 SHOULD 提供测试 helper，用于复用小程序媒体 URL 与页面绑定断言。
- helper SHOULD 支持断言图片展示 URL 优先使用缩略图，预览 URL 保留原图。
- helper SHOULD 支持断言视频播放 URL 不被替换，视频 poster / cover URL 优先使用轻量图片。
- helper SHOULD 支持断言小程序页面模板绑定展示 URL、preview URL、fallback 和 lazy-load 策略。
- helper SHOULD 支持断言 `/media/{object_key}` 或等价受控 URL 不暴露 raw object key，不直连未授权对象存储。
- helper MUST 只服务测试和验收表达，不得绕过 API、DB、对象存储或真实端侧 evidence。

### FR-005 审计 helper

- 系统 SHOULD 提供审计 helper，用于 dry-run 检查历史媒体对象的四联风险。
- 审计 helper MUST 默认 dry-run，不得默认写入数据库或对象存储。
- 审计 helper SHOULD 支持按资源类型抽样或批量检查，例如 SKU 图片、SKU 视频 poster、品牌 Logo、Banner、品牌证书、小程序商品卡片图。
- 审计 helper SHOULD 输出 object 存在性、MIME、大小、缩略图是否存在、缩略图是否明显轻量、URL 是否可能 fallback、失败原因枚举和统计摘要。
- 审计 helper MUST 输出脱敏摘要，使用 key hash、标准前缀、资源类型、计数和失败原因枚举；不得输出真实 object key 全量值或敏感配置。
- 若后续需要 apply 回填或重生成，helper MUST 要求显式参数、备份确认、幂等验证和失败重试策略。

### FR-006 历史对象审计与回填策略

- 最佳实践 MUST 明确历史对象审计结果如何分类：已闭环、缺缩略图、缩略图无收益、URL fallback、object 缺失、权限异常、证据不足。
- 对缺缩略图或缩略图无收益的历史对象，MUST 明确是否需要独立回填 / 重生成 Change，而不得在验收文档中直接视为通过。
- 涉及生产写入时，MUST 要求先完成 MySQL 与对象存储 bucket / prefix 备份确认。
- 回填或重生成结果 MUST 记录 dry-run、apply、幂等性、成功数量、失败数量、跳过数量和失败原因。
- 只读审计和批处理摘要 MUST NOT 替代小程序受影响页面的 render evidence。

### FR-007 与既有模板和规则协同

- REQ-0111 MUST 明确不替代 `REQ-0090` 媒体五联、`REQ-0091` 媒体类 BUG 四联、`REQ-0101` 媒体三段验收模板。
- 媒体类 BUG 修复仍 MUST 引用 `docs/standards/media-bug-four-point-acceptance-template.md`。
- 媒体类通用能力、发布验收或缩略图收益验收 SHOULD 引用 `docs/standards/media-five-point-acceptance-template.md`。
- 涉及列表字段、生成策略、历史对象维护的需求或 BUG SHOULD 同时引用 `REQ-0101` 的三段组织方式。
- 小程序 DevTools / 真机 / 体验版 evidence MUST 引用 `docs/standards/miniapp-device-evidence-template.md`。

### FR-008 工作流落点

- `/req-complete` 阶段 SHOULD 补齐 user stories、业务流程和 acceptance，明确 helper、文档、规范和验收证据的交付项。
- `/req-opsx` 阶段 MUST 明确是否更新 `rules/media.md`、`rules/object-storage.md`、`docs/standards`、`docs/knowledge-base`、测试 helper 或审计 helper。
- 若涉及 API 或 DB 结构变化，后续 OpenSpec Change MUST 单独说明请求、响应、错误码、表结构、Pydantic Schema、OpenAPI、Orval 和测试影响。
- 若仅新增测试 helper 或审计 helper 且不改变运行时 API / DB，MUST 在设计中明确“不影响生产运行时能力”。
- Workflow Sync 管辖的 Sprint Scope marker 块不得手工编辑。

## 6. UI / UE 约束

- 本需求本身不新增 Web 管理端、店主 Web 或小程序页面。
- 若后续在文档站、管理端或验收工具中展示最佳实践，应使用紧凑表格、分段清单和状态字段，避免长段说明压过证据本身。
- 小程序 render evidence 应关注用户可见行为：首屏加载、滚动懒加载、图片预览、视频 poster、失败占位、点击与跳转是否退化。
- 如果后续涉及 Web UI 展示，必须遵守 Design System semantic token，禁止裸 Hex。

## 7. 非功能约束

- MUST 遵守 MinIO 单桶 + 前缀策略，前端和小程序不得直连未授权对象存储。
- MUST 遵守媒体安全规则，不记录真实客户数据、真实密钥、Authorization header、Cookie、`.env` 内容、本机绝对路径或完整敏感 object key。
- helper 输出 MUST 可用于验收复核，但不得保存大段 Network 日志、HAR 原文或不可公开运维地址。
- 审计 helper MUST 可在本地 / 测试 / 生产等价环境区分运行模式，生产写入必须显式确认。
- 测试 helper SHOULD 可复用，避免每个媒体需求重复编写 `.thumb`、preview、poster、fallback 断言。
- 文档与 helper SHOULD 保持轻量，优先解决“证据可复核”和“验收不漏链路”的问题。

## 8. 关联需求与规范

| 类型 | ID / 文件 | 关系 |
|---|---|---|
| 关联 BUG | `BUG-0125-miniapp-sku-detail-media-original-load` | SKU 详情页原图加载慢案例，暴露详情页展示 URL 与预览 URL 未分离。 |
| 关联 BUG | `BUG-0126-miniapp-brand-media-slow-load` | 品牌链路媒体加载慢案例，暴露 `.thumb` 存在不等于真实轻量命中。 |
| 关联 BUG | `BUG-0110-miniapp-card-banner-thumbnail-usage` | 小程序卡片 / Banner 缩略图治理的上游相关缺陷。 |
| 关联需求 | `REQ-0090-media-five-point-acceptance-template` | 媒体通用 key / object / URL / thumbnail benefit / miniapp render 检查。 |
| 关联需求 | `REQ-0091-media-bug-four-point-acceptance-template` | 媒体类 BUG 修复后的 key / object / URL / render 闭环。 |
| 关联需求 | `REQ-0101-media-acceptance-three-part-template` | 媒体类需求与 BUG 的证据组织方式。 |
| 关联文档 | `docs/standards/miniapp-device-evidence-template.md` | 小程序 DevTools、真机、Network evidence 记录规范。 |
| 关联规范 | `rules/media.md` | 媒体能力、四联验收和 AI 更新规则。 |
| 关联规范 | `rules/object-storage.md` | 对象存储 key、object、URL、权限和生产维护边界。 |

## 9. 状态块

```yaml
requirement_id: REQ-0111-miniapp-media-four-part-acceptance-practice
status: archived
lifecycle_stage: review
readiness: Ready
next_command: /req-opsx REQ-0111
notes:
  - 已根据 capture、req-explore 结论和用户补充生成 requirement.md。
  - 本需求不仅包含知识库与验收规范沉淀，也包含测试 helper 和审计 helper 的实现范围。
  - 本需求不直接新增上传、缩略图生成、CDN、缓存或对象存储 provider 能力。
  - 已补齐 user-stories、business-flow、acceptance 与 trace；本需求不需要 prototype。
  - 已纳入 sprint-023，下一步创建 OpenSpec Change。
```
