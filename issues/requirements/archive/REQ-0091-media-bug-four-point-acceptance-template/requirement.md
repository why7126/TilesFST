---
requirement_id: REQ-0091-media-bug-four-point-acceptance-template
title: 媒体类 BUG 四联验收模板
terminal: multi
version: v1
status: done
owner: product
source: capture.md
priority: P1
parent_requirement:
created_at: 2026-08-01 09:50:43
updated_at: 2026-08-01 11:14:55
---

# REQ-0091 媒体类 BUG 四联验收模板

## 1. 需求背景

平台媒体链路覆盖管理端上传、后端 media 模块、MinIO 对象存储、业务记录、Web 展示端与微信小程序渲染。媒体类 BUG 常见表现包括对象 key 与业务记录不一致、对象存储中 object 缺失、URL 无法访问、端侧渲染失败或失败态不可诊断。

当前已有媒体五联验收模板用于一般媒体能力交付和发布检查，但 BUG 修复场景更强调“原问题是否被复现、修复后是否闭环、回归证据是否足以避免再次发生”。因此需要建立一份更聚焦的“媒体类 BUG 四联验收模板”，用于媒体类缺陷修复、回归和发布前确认，统一检查 `key`、`object`、`URL` 与 `render` 四个维度。

## 2. 目标用户

| 用户 | 诉求 |
|---|---|
| 产品负责人 | 快速确认媒体类 BUG 修复是否覆盖原始问题和用户可见影响。 |
| 测试人员 | 使用固定模板执行媒体缺陷回归，减少遗漏 key、object、URL 或端侧渲染证据。 |
| 后端 / 平台开发 | 明确对象 key、对象存在性、URL 生成和权限策略的修复验收边界。 |
| 前端 / 小程序开发 | 明确修复后各端媒体渲染、失败态和降级表现的验收要求。 |
| 发布负责人 | 在发布前确认媒体类 BUG 修复不会引入对象存储、域名、签名 URL 或小程序资源访问回归。 |

## 3. 需求目标

- 建立一份可复用的媒体类 BUG 四联验收模板。
- 模板必须覆盖 `key`、`object`、`URL`、`render` 四个检查维度。
- 模板应适用于媒体类 BUG 的复现确认、修复验收、回归测试和发布前检查。
- 模板应能记录原 BUG 场景、修复证据、失败态和阻塞原因。
- 模板不得绕过现有上传安全、MinIO 单桶前缀、鉴权、对象访问和小程序平台限制。

## 4. 范围

### 4.1 本期包含

| 范围 | 说明 |
|---|---|
| 四联验收维度定义 | 明确 key、object、URL、render 的含义、检查方法和通过标准。 |
| BUG 场景记录 | 要求记录原始 BUG 表现、复现入口、影响端和修复后的对照结果。 |
| 验收模板结构 | 定义可嵌入 BUG `acceptance.md`、回归测试清单、Sprint 验收报告或发布检查清单的 Markdown 模板。 |
| 证据记录格式 | 明确每个维度需要记录的对象标识、页面/接口、HTTP 状态、截图或日志线索。 |
| 端侧渲染要求 | 覆盖管理端、店主 Web 展示端和微信小程序端的媒体渲染与失败态检查。 |
| 失败与阻塞处理 | 统一记录 `fail`、`blocked` 与 `n/a` 的原因，便于后续重新 capture 或继续排查。 |

### 4.2 本期不包含

| 不包含 | 说明 |
|---|---|
| 新增媒体上传能力 | 本需求只定义 BUG 验收模板，不新增上传接口、上传页面或媒体类型。 |
| 新增对象存储能力 | 不新增 Bucket、对象迁移、签名 URL 策略或 MinIO 适配层能力。 |
| 新增缩略图或视频转码能力 | 缩略图生成、视频转码、压缩、多清晰度仍需单独需求或 OpenSpec Change。 |
| 替代 BUG 生命周期 | 模板服务于媒体类 BUG 验收，不替代 `/bug-capture`、`/bug-complete`、`/bug-review` 等流程。 |
| 强制自动化测试实现 | 本期可预留结构化字段，但不要求实现脚本、CI 门禁或自动化验收工具。 |

## 5. 功能要求

### FR-001 模板载体与复用方式

- 系统 MUST 提供一份“媒体类 BUG 四联验收模板”，供后续媒体类缺陷修复和回归复用。
- 模板 MUST 使用中文优先编写，检查项名称可保留英文关键字：`key`、`object`、`URL`、`render`。
- 模板 SHOULD 采用 Markdown 结构，便于复制到 BUG 验收、Sprint 验收报告、发布检查清单或测试用例说明。
- 模板 MUST 区分“原 BUG 场景”“检查项”“通过标准”“证据记录”“失败或阻塞处理”五类信息。
- 模板 MUST 不包含真实客户数据、真实密钥、内部绝对路径、Authorization header、Cookie 或 `.env` 内容。

### FR-002 原 BUG 场景记录

- 模板 MUST 要求记录 BUG 编号、标题、严重等级、影响范围和复现入口。
- 模板 MUST 要求记录修复前的实际结果和修复后的期望结果。
- 模板 SHOULD 要求记录触发媒体问题的业务资源，例如品牌 Logo、SKU 图片、SKU 视频、证书图片或 Banner 图片。
- 模板 MUST 支持记录受影响端，包括 Web 管理端、店主 Web 展示端、微信小程序端或后端接口。
- 若原 BUG 仅在特定环境复现，模板 MUST 要求记录环境信息，例如本地、测试、体验版或生产。

### FR-003 key 验收维度

- `key` 检查 MUST 确认修复后业务记录中的媒体 key 稳定可追溯。
- `key` 检查 MUST 确认对象 key 符合 MinIO 单桶 + 前缀策略。
- `key` 检查 MUST 明确禁止使用用户原始文件名、本机绝对路径或临时路径作为对象存储 key。
- `key` 检查 SHOULD 覆盖媒体类型、业务资源 ID、前缀、唯一标识和扩展名等关键信息。
- 若 BUG 修复涉及历史 key 兼容或迁移，模板 MUST 要求记录旧 key、新 key 和兼容结果。

### FR-004 object 验收维度

- `object` 检查 MUST 确认对象存储中真实 object 存在，且与业务记录中的 key 能对应。
- `object` 检查 MUST 覆盖 MIME Type、文件大小、扩展名、权限边界和对象可读性。
- `object` 检查 MUST 支持记录对象不存在、大小为 0、类型不匹配、权限错误、存储环境不可用等失败状态。
- 对图片、视频、证书图片、品牌 Logo 等不同媒体类型，模板 SHOULD 允许记录关联资源 ID 和媒体用途。
- 模板 MUST 要求对象存储验收不暴露 MinIO 凭证、内部路径或未脱敏日志。

### FR-005 URL 验收维度

- `URL` 检查 MUST 确认接口响应、Web 页面或小程序端使用的媒体 URL 可访问。
- `URL` 检查 MUST 区分相对 URL、公开 URL、签名 URL、代理 URL 或静态资源 URL 的使用场景。
- `URL` 检查 MUST 验证成功响应、对象缺失、权限不足、签名过期、域名配置错误等关键结果。
- URL 失败时，模板 MUST 要求记录页面或接口入口、HTTP 状态、业务错误码、用户可见表现和排查线索。
- 模板 MUST 要求前端不得直连未授权对象存储；媒体访问应遵循后端鉴权、代理或签名 URL 策略。

### FR-006 render 验收维度

- `render` 检查 MUST 确认受影响端能正确渲染媒体及失败态。
- Web 管理端 render 检查 SHOULD 覆盖上传后预览、列表缩略展示、详情或编辑弹窗中的展示效果。
- 店主 Web 展示端 render 检查 SHOULD 覆盖公开页面、商品卡片、详情页或媒体预览入口。
- 微信小程序 render 检查 MUST 覆盖真机或等价预览环境、合法域名资源访问、图片/视频组件限制和失败态展示。
- 模板 MUST 要求小程序端不依赖 Web 浏览器专属 API。
- 若某端不受本次 BUG 影响，模板 MUST 要求记录 `n/a` 原因和影响判断。

### FR-007 证据、状态与失败处理

- 模板 MUST 为每个维度提供统一状态：`pass`、`fail`、`n/a`、`blocked`。
- 模板 MUST 要求记录证据，包括媒体类型、业务资源、key、object 检查结果、URL 检查结果、渲染入口、截图或日志位置。
- `fail` 状态 MUST 记录实际结果、期望结果、复现步骤和影响范围。
- `blocked` 状态 MUST 记录阻塞原因，例如缺少测试资源、域名未配置、MinIO 环境不可用或小程序体验版未上传。
- 失败记录 MUST 能支撑后续 `/bug-capture` 或原 BUG 返修，至少包含可复现入口和排查线索。

### FR-008 与后续工作流集成

- `/req-complete` 阶段 SHOULD 将该模板沉淀到验收文档或长期治理文档的合适位置。
- 后续 `/req-opsx` MUST 明确模板最终落点，例如 `docs/knowledge-base`、`docs/standards`、`rules/media.md`、`rules/object-storage.md` 或 BUG acceptance 模板。
- 若模板接入 Sprint 或 Release 检查流程，MUST 明确哪些媒体类 BUG 触发四联验收。
- 若后续实现自动化检查，MUST 另行说明 API、测试脚本、CI 或 Docker Compose 验证边界。
- 模板集成不得手工编辑 Workflow Sync 管辖的 Sprint Scope marker 块。

## 6. UI / UE 约束

- 本需求本身不新增 Web 管理端、店主端或小程序页面。
- 若后续在管理端、发布工具或验收工具中展示该模板，界面应优先采用紧凑表格或检查清单。
- 模板中的状态表达应清晰可扫读，适合测试、产品和开发共同使用。
- 如果模板最终落入 Web UI，必须遵守 Design System semantic token，不得直接写裸 Hex。
- 小程序相关验收描述必须贴合微信小程序组件和域名访问限制，不使用浏览器专属术语作为通过标准。

## 7. 非功能约束

- MUST 遵守上传安全规则，不记录真实密钥、原始本地路径或真实客户数据。
- MUST 遵守 MinIO 单桶 + 前缀策略，不因模板新增 Bucket 或绕过后端适配层。
- MUST 遵守媒体模块边界，后续如实现自动化检查，应优先复用 media / object storage 相关服务或测试辅助能力。
- MUST 保持模板轻量，适合作为单个媒体类 BUG 的验收记录，不应变成无法执行的大型审计表。
- SHOULD 为后续自动化、发布检查和 Sprint 验收保留结构化字段。

## 8. 关联需求与规范

| 类型 | ID / 文件 | 关系 |
|---|---|---|
| 关联需求 | `REQ-0090-media-five-point-acceptance-template` | 本需求聚焦媒体类 BUG 四联验收，可复用通用媒体验收模板的 key、object、URL 与端侧渲染思路。 |
| 关联需求 | `REQ-0012-object-storage-key-layout` | key 与 object 检查应遵守对象存储 Key 和前缀规则。 |
| 关联需求 | `REQ-0069-upload-observability-trace-logs` | 上传链路追踪可为媒体 BUG 验收提供日志与请求证据。 |
| 关联规范 | `rules/media.md` | 后续模板落点可能需要补充媒体类 BUG 验收规则。 |
| 关联规范 | `rules/object-storage.md` | object key、MinIO 访问和单桶策略的事实规范。 |
| 关联文档 | `docs/07-object-storage-strategy.md` | 对象存储策略与排查说明可引用四联验收模板。 |

## 9. 状态块

```yaml
requirement_id: REQ-0091-media-bug-four-point-acceptance-template
status: done
lifecycle_stage: plan
readiness: Ready
next_command: /sprint-propose <sprint-id> --requirement REQ-0091-media-bug-four-point-acceptance-template
notes:
  - 已完成 /req-opsx，OpenSpec Change 为 add-media-bug-four-point-acceptance-template。
  - Workflow Sync 已将带 Change 的 REQ 派生到 Sprint 流程；后续已纳入 sprint-017 并归档闭环。
  - 后续需确认四联验收是否固定为 key、object、URL、render，以及是否区分 Web 管理端、店主 Web 展示端和微信小程序端。
  - 若后续要自动化四联检查，需要在 OpenSpec design 中单独明确脚本、API 或 CI 范围。
  - knowledge_base_refs 已写入 trace.md，后续 /req-opsx 的 design.md 必须引用。
```
