---
requirement_id: REQ-0090-media-five-point-acceptance-template
title: 媒体五联验收模板
terminal: multi
version: v1
status: done
owner: product
source: capture.md
priority: P1
parent_requirement:
created_at: 2026-08-01 09:48:25
updated_at: 2026-08-01 11:38:21
---

# REQ-0090 媒体五联验收模板

## 1. 需求背景

平台已经围绕图片、视频、品牌 Logo、证书图片、SKU 图/视频等媒体能力建立了上传、对象存储、URL 访问和小程序展示链路。媒体链路跨越管理端、后端 media 模块、MinIO、数据库记录、店主展示端与微信小程序，任一节点不一致都可能导致“上传成功但展示失败”“对象存在但 URL 不可用”“缩略图收益不明确”“小程序端无法渲染”等问题。

当前已有对象存储 Key 规则、上传链路追踪、发布镜像治理等能力，但媒体类需求在验收时缺少一个固定、可复用的轻量模板，导致不同 REQ、BUG、Sprint 或 Release 对媒体检查项描述不一致。需要建立“媒体五联验收模板”，统一覆盖 `key`、`object`、`URL`、`thumbnail benefit` 与 `miniapp render` 五个维度，作为后续媒体相关需求、缺陷修复、回归测试和发布验收的标准入口。

## 2. 目标用户

| 用户 | 诉求 |
|---|---|
| 产品负责人 | 在需求验收时快速确认媒体链路是否覆盖关键体验与业务价值，不遗漏小程序展示或缩略图收益。 |
| 测试人员 | 使用统一模板执行媒体链路回归，减少每次临时编写验收清单的成本。 |
| 后端 / 平台开发 | 明确 object key、对象存储、URL 访问和权限策略的验收边界。 |
| 前端 / 小程序开发 | 明确媒体 URL、缩略图和失败态在 Web 与小程序端的渲染预期。 |
| 运维 / 发布负责人 | 在发布前用一致的媒体检查项确认 MinIO、域名、签名 URL 或静态资源策略没有断链。 |

## 3. 需求目标

- 建立一份可复用的媒体五联验收模板。
- 模板必须覆盖 `key`、`object`、`URL`、`thumbnail benefit`、`miniapp render` 五个检查维度。
- 模板应适用于媒体相关 REQ、BUG、OpenSpec Change、Sprint 验收和发布前检查。
- 模板应能指导人工验收，也应为后续自动化测试或脚本化检查预留结构。
- 模板不得绕过现有上传安全、MinIO 单桶前缀、鉴权、对象访问和小程序平台限制。

## 4. 范围

### 4.1 本期包含

| 范围 | 说明 |
|---|---|
| 五联验收维度定义 | 明确 key、object、URL、thumbnail benefit、miniapp render 的含义、检查方法和通过标准。 |
| 适用场景说明 | 覆盖图片、视频、Logo、证书图片、SKU 媒体等已有媒体链路，后续媒体类型可按同一结构扩展。 |
| 验收模板结构 | 定义可嵌入 `acceptance.md`、Sprint 验收报告或发布检查清单的 Markdown 模板。 |
| 失败记录格式 | 明确每个维度失败时应记录的对象标识、页面/接口、端、错误表现和排查线索。 |
| 小程序渲染要求 | 将微信小程序端媒体渲染、失败态和平台限制纳入固定验收维度。 |
| 缩略图收益表达 | 要求对缩略图存在的业务收益或体验收益给出可理解说明，避免“生成了但无人使用”。 |

### 4.2 本期不包含

| 不包含 | 说明 |
|---|---|
| 新增媒体上传能力 | 本需求只定义验收模板，不新增上传接口、上传页面或媒体类型。 |
| 新增缩略图生成流水线 | 可验收缩略图收益，但不在本需求中实现缩略图生成、压缩、裁剪或多规格输出。 |
| 新增视频转码能力 | 视频转码、压缩、多清晰度、封面增强仍需单独 OpenSpec Change。 |
| 替代对象存储规范 | 模板引用现有 MinIO 单桶前缀与 object key 规则，不重新定义存储架构。 |
| 替代自动化测试框架 | 本期可为自动化检查预留字段，但不强制实现测试脚本或 CI 门禁。 |

## 5. 功能要求

### FR-001 模板载体与复用方式

- 系统 MUST 提供一份“媒体五联验收模板”，供后续媒体相关需求、BUG、OpenSpec Change、Sprint 验收和发布检查复用。
- 模板 MUST 使用中文优先编写，检查项名称可保留英文关键字：`key`、`object`、`URL`、`thumbnail benefit`、`miniapp render`。
- 模板 SHOULD 采用 Markdown 结构，便于复制到 `acceptance.md`、`acceptance-report.md`、发布检查清单或测试用例说明。
- 模板 MUST 区分“检查项”“通过标准”“证据记录”“失败处理建议”四类信息。
- 模板 MUST 不包含真实客户数据、真实密钥、内部绝对路径、Authorization header、Cookie 或 `.env` 内容。

### FR-002 key 验收维度

- 模板 MUST 要求记录媒体对象的业务来源、媒体类型、`object_key` 或等价脱敏对象标识。
- `key` 检查 MUST 确认对象 key 命名稳定，符合 MinIO 单桶 + 前缀策略。
- `key` 检查 MUST 明确禁止使用用户原始文件名作为对象存储 key。
- `key` 检查 SHOULD 覆盖前缀、租户段、资源类型、UUID 或等价唯一标识、扩展名等关键组成。
- 若媒体来自历史对象或迁移对象，模板 MUST 要求记录旧 key 与新 key 的兼容或迁移状态。

### FR-003 object 验收维度

- 模板 MUST 要求确认对象存储中真实 object 存在，且与业务记录中的 key 能对应。
- `object` 检查 MUST 覆盖 MIME Type、文件大小、扩展名、安全校验和权限边界。
- `object` 检查 MUST 明确上传失败、对象不存在、对象大小为 0、类型不匹配、权限错误等失败状态的记录方式。
- 对视频、证书图片、品牌 Logo、SKU 图片等不同媒体类型，模板 SHOULD 允许记录业务类型和关联资源 ID。
- 模板 MUST 要求对象存储访问不暴露 MinIO 凭证或内部路径。

### FR-004 URL 验收维度

- 模板 MUST 要求检查后端响应、Web 端渲染或小程序端使用的媒体 URL 是否可访问。
- `URL` 检查 MUST 区分相对 URL、公开 URL、签名 URL 或代理 URL 的使用场景。
- `URL` 检查 MUST 验证 200/成功响应、404/对象缺失、403/权限不足、签名过期、域名配置错误等关键结果。
- URL 失败时，模板 MUST 要求记录页面或接口入口、错误码、HTTP 状态、用户可见表现和排查线索。
- 模板 MUST 要求前端不得直连未授权对象存储；媒体访问应遵循后端鉴权、代理或签名 URL 策略。

### FR-005 thumbnail benefit 验收维度

- 模板 MUST 要求说明缩略图或封面图在该场景中的实际收益。
- `thumbnail benefit` SHOULD 覆盖列表首屏加载、卡片渲染速度、弱网体验、带宽节省、后台预览效率、视频封面识别等收益类型。
- 若某媒体场景没有缩略图，模板 MUST 要求明确记录“不适用”原因，而不是留空。
- 若存在缩略图，模板 SHOULD 要求记录缩略图与原始媒体的关联关系、尺寸/比例策略和展示入口。
- 模板 MUST 避免将“缩略图已生成”作为唯一通过标准；必须说明用户或系统获得的具体收益。

### FR-006 miniapp render 验收维度

- 模板 MUST 要求检查微信小程序端能正确渲染相关媒体。
- `miniapp render` 检查 MUST 覆盖真机或等价小程序预览环境、生产/测试域名资源访问、图片或视频组件限制、失败态展示。
- 模板 MUST 要求小程序端不依赖 Web 浏览器专属 API。
- 对图片类媒体，模板 SHOULD 覆盖加载成功、占位图、预览或点击行为。
- 对视频类媒体，模板 SHOULD 覆盖播放入口、封面、全屏或失败提示等关键表现。
- 若本次媒体能力不涉及小程序，模板 MUST 要求记录“不适用”原因和影响判断。

### FR-007 证据与失败记录

- 模板 MUST 提供统一证据记录字段，包括媒体类型、业务资源、key、object 检查结果、URL 检查结果、小程序页面或组件、截图/日志位置。
- 每个维度 MUST 支持状态：`pass`、`fail`、`n/a`、`blocked`。
- 失败记录 MUST 能支撑后续 `/bug-capture`，至少包含失败现象、影响范围、复现入口、期望结果和实际结果。
- blocked 状态 MUST 记录阻塞原因，例如缺少测试资源、域名未配置、MinIO 环境不可用或小程序体验版未上传。
- 模板 SHOULD 支持一次记录多个媒体样例，但每个样例必须能独立追踪。

### FR-008 与后续工作流集成

- `/req-complete` 阶段 SHOULD 将该模板沉淀到验收文档或长期治理文档的合适位置。
- 后续 `/req-opsx` MUST 明确该模板最终落点，例如 `docs/knowledge-base`、`docs/standards`、`rules/media.md`、`rules/object-storage.md` 或 issue acceptance 模板。
- 若模板接入 Sprint 或 Release 检查流程，MUST 明确哪些媒体变更触发五联验收。
- 若后续实现自动化检查，MUST 另行说明 API、测试脚本、CI 或 Docker Compose 验证边界。
- 模板集成不得手工编辑 Workflow Sync 管辖的 Sprint Scope marker 块。

## 6. UI / UE 约束

- 本需求本身不新增 Web 管理端、店主端或小程序页面。
- 若后续在管理端或发布工具中展示该模板，界面应优先采用紧凑表格或检查清单，不做营销式页面。
- 模板中的状态表达应清晰可扫读，适合测试、产品和开发共同使用。
- 如果模板最终落入 Web UI，必须遵守 Design System semantic token，不得直接写裸 Hex。
- 小程序相关验收描述必须贴合微信小程序组件和域名访问限制，不使用浏览器专属术语作为通过标准。

## 7. 非功能约束

- MUST 遵守上传安全规则，不记录真实密钥、原始本地路径或真实客户数据。
- MUST 遵守 MinIO 单桶 + 前缀策略，不因模板新增 Bucket 或绕过后端适配层。
- MUST 遵守媒体模块边界，后续如实现自动化检查，应优先复用 media / object storage 相关服务或测试辅助能力。
- MUST 保持模板轻量，适合作为每个媒体样例的验收记录，不应变成无法执行的大型审计表。
- SHOULD 为后续自动化、发布检查和 Sprint 验收保留结构化字段。

## 8. 关联需求与规范

| 类型 | ID / 文件 | 关系 |
|---|---|---|
| 关联需求 | `REQ-0012-object-storage-key-layout` | key 与 object 检查应遵守对象存储 Key 和前缀规则。 |
| 关联需求 | `REQ-0069-upload-observability-trace-logs` | 上传链路追踪可为五联验收提供日志与耗时证据。 |
| 关联规范 | `rules/media.md` | 后续模板落点可能需要补充媒体治理规则。 |
| 关联规范 | `rules/object-storage.md` | object key、MinIO 访问和单桶策略的事实规范。 |
| 关联文档 | `docs/07-object-storage-strategy.md` | 对象存储策略与排查说明可引用五联验收模板。 |

## 9. 状态块

```yaml
requirement_id: REQ-0090-media-five-point-acceptance-template
status: done
lifecycle_stage: review
readiness: Partially Ready
next_command: /req-opsx REQ-0090-media-five-point-acceptance-template
notes:
  - 已补齐 user-stories、business-flow、acceptance、trace 和 prototype 策略。
  - Knowledge-base gate 已转化 media-upload 横切 AC；引用的 best-practices 当前为 draft，因此 readiness 为 Partially Ready。
  - 已通过需求评审；后续需在 req-opsx design 确认模板最终落点，以及是否接入 Sprint / Release 验收。
  - 若后续要自动化五联检查，需要在 OpenSpec design 中单独明确脚本、API 或 CI 范围。
```
