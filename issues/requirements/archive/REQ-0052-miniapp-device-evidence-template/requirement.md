---
requirement_id: REQ-0052-miniapp-device-evidence-template
title: 小程序 DevTools/真机验收 evidence 模板
terminal: miniapp
version: v1
status: done
owner: product
source: capture.md
priority: P1
parent_requirement:
created_at: 2026-07-19 17:05:33
updated_at: 2026-07-19 19:05:20
---

# REQ-0052 小程序 DevTools/真机验收 evidence 模板

## 1. 需求背景

微信小程序相关需求已经覆盖首页、自定义导航栏、SKU 详情页、分类列表、搜索和商品列表等多条链路。部分变更虽然能通过静态测试、脚本测试或文件结构检查，但仍需要微信开发者工具或真机确认实际运行效果，例如：

- 自定义导航栏是否避让微信原生胶囊和状态栏。
- fixed header 是否遮挡页面内容。
- 首页、列表页、详情页在 320、375、430 pt 等宽度下是否布局稳定。
- 微信开发者工具实际加载的 `.js` 运行入口是否与 `.ts` 业务逻辑一致。
- 真机截图、录屏、页面路径、基础库版本和剩余风险是否可复核。

历史 Sprint 中已有“DevTools/真机待人工验收”的残留项，但这些证据常散落在 OpenSpec `tasks.md`、需求 `acceptance.md`、Sprint `acceptance-report.md` 或归档备注中。散落记录会导致后续复盘难以判断：哪些是自动化已覆盖，哪些是真实设备已验收，哪些只是待人工 follow-up。

本需求用于建立一套面向微信小程序 DevTools 预览和真机验收的可复用 evidence 模板，作为后续小程序需求、OpenSpec Change、Sprint 验收报告和归档结论的共同证据口径。

## 2. 目标用户

| 用户 | 诉求 |
|---|---|
| 产品 / 需求负责人 | 能区分自动化通过、DevTools 通过、真机通过和仍待人工验收的状态，避免发布说明误写。 |
| 小程序开发 | 在实现阶段知道需要记录哪些设备、页面、基础库、截图和剩余风险。 |
| 测试 / 验收人员 | 按统一模板记录 DevTools 和真机验收结论，减少散落备注。 |
| AI / Codex Agent | 在后续 `/req-complete`、`/req-opsx`、`/opsx-apply`、`/sprint-archive` 中引用同一 evidence 事实源，不把静态检查误当真实设备验收。 |

## 3. 需求目标

- 建立一套可复制的 `miniapp_device_evidence` 模板。
- 模板 MUST 覆盖微信开发者工具预览和真机验收两类人工设备证据。
- 模板 MUST 明确自动化/静态测试 evidence 与 DevTools/真机 evidence 的边界。
- 模板 MUST 支持记录设备、环境、页面、视口、安全区、截图/录屏、执行人、结论、阻塞项和剩余风险。
- 模板 SHOULD 沉淀到长期治理文档，优先考虑 `docs/standards/miniapp-device-evidence-template.md`。
- 后续小程序 REQ、OpenSpec Change、Sprint 验收报告和归档结论 SHOULD 引用该模板，而不是在多个文档中重复发散。

## 4. 范围

### 4.1 本期包含

| 范围 | 说明 |
|---|---|
| 模板结构 | 定义小程序设备验收 evidence 的字段、状态、结论和剩余风险记录方式。 |
| DevTools evidence | 覆盖微信开发者工具预览、基础库版本、页面路径、模拟器设备、视口宽度和截图记录。 |
| 真机 evidence | 覆盖设备型号、系统版本、微信版本、基础库版本、页面路径、安全区、截图或录屏记录。 |
| 自动化边界 | 明确静态测试、脚本测试、截图自动化与人工设备验收的关系，禁止混淆结论。 |
| N/A / blocked 判定 | 支持记录本 Change 不需要真机验收、设备不可用、外部依赖阻塞或仅需后续 follow-up 的原因。 |
| 引用方式 | 明确后续 `acceptance.md`、OpenSpec `tasks.md`、Change trace、Sprint `acceptance-report.md` 可引用该模板。 |

### 4.2 本期不包含

| 不包含 | 说明 |
|---|---|
| 实现具体小程序功能 | 本需求不新增或修改首页、导航栏、列表页、详情页、搜索、收藏等业务能力。 |
| 自动化截图工具链 | 本需求不要求新增 Playwright、小程序自动化、截图采集或真机云测能力。 |
| 回填全部历史证据 | sprint-008 等历史残留可作为参考，不要求一次性补齐所有历史 DevTools/真机证据。 |
| 修改小程序源码 | 本需求不修改 `src/miniapp/` 页面、组件、样式、服务或配置。 |
| 修改 API / DB / Orval | 本需求只定义验收证据模板，不新增后端接口、数据库结构或 Web API 客户端生成物。 |
| 修改 Docker Compose | 本需求不影响 Docker Compose、Nginx、MinIO 或环境变量。 |

## 5. 功能要求

### FR-001 模板基础结构

模板 MUST 以小程序 Change 或页面验收对象为单位，至少包含：

- `template_ref`：模板文档路径。
- `target`：需求、BUG 或 Change ID。
- `pages`：被验收页面路径、页面标题和关键场景。
- `evidence_items`：按 DevTools、真机、自动化或 N/A 分组的证据项。
- `summary`：最终结论、阻塞项和剩余风险。

模板 SHOULD 使用 YAML 或 Markdown 表格提供可复制结构，便于放入 `acceptance.md`、OpenSpec `tasks.md` 或 Sprint 验收报告。

### FR-002 evidence 状态

每条 evidence MUST 支持以下状态之一：

```yaml
status: required | passed | failed | blocked | not_applicable | follow_up
```

状态含义：

| 状态 | 含义 |
|---|---|
| `required` | 已识别必须补齐，尚未执行或未记录。 |
| `passed` | 已验收通过，并有截图、录屏、命令摘要或人工记录。 |
| `failed` | 已验收失败，必须记录失败表现和后续处理。 |
| `blocked` | 设备、账号、环境、网络、版本或外部依赖阻塞。 |
| `not_applicable` | 当前 Change 不需要该类设备验收，必须写明原因。 |
| `follow_up` | 可发布但保留人工后续确认，必须写明风险和责任人。 |

### FR-003 DevTools evidence

DevTools evidence MUST 支持记录：

- 微信开发者工具版本或可识别版本摘要。
- 基础库版本。
- 模拟器设备或 viewport 宽度，例如 320、375、430 pt。
- 页面路径和关键 query 参数。
- 验收场景，例如首页首屏、自定义导航栏、分类列表、SKU 详情页。
- 截图或录屏的仓库相对路径，或无法保存截图时的人工摘要。
- 验收结论、失败表现、阻塞项和剩余风险。

若 DevTools 仅确认页面可打开，不足以代表真机安全区、原生胶囊或真实触控表现，模板 MUST 要求结论中明确“不等同于真机验收”。

### FR-004 真机 evidence

真机 evidence MUST 支持记录：

- 设备型号。
- 系统类型与版本，例如 iOS / Android。
- 微信版本。
- 小程序基础库版本。
- 页面路径、关键 query 参数和用户状态。
- 视口宽度、安全区、状态栏和胶囊避让结论。
- 截图或录屏的仓库相对路径，或无法保存文件时的人工摘要。
- 执行人、执行时间、验收结论和剩余风险。

涉及自定义导航栏、固定头部、触控区域、分享/返回/关闭、图片预览或页面滚动的 Change，SHOULD 至少保留一条真机 evidence；若不能执行，MUST 标记 `blocked` 或 `follow_up`，不得写作“真机通过”。

### FR-005 自动化与人工设备证据边界

模板 MUST 区分以下证据来源：

| 来源 | 可证明 | 不可替代 |
|---|---|---|
| 静态测试 | 文件存在、模板非空、配置合理、规则约束 | 不证明 DevTools 实际渲染通过 |
| 脚本/单元测试 | 数据转换、组件逻辑、页面配置或回归条件 | 不证明真机安全区和微信原生能力 |
| DevTools 预览 | 开发者工具中的页面加载和模拟器布局 | 不等同于真实设备触控、系统安全区和微信版本差异 |
| 真机验收 | 指定设备上的真实运行表现 | 不覆盖所有设备和系统组合 |

没有 DevTools 或真机记录时，Sprint 验收报告、release note 或 Change trace MUST 避免写成“设备验收已完成”。

### FR-006 截图、录屏和敏感信息

模板 MUST 要求截图、录屏和报告路径使用仓库相对路径或稳定 artifact 引用，不记录本机绝对路径。

证据记录 MUST 避免包含：

- token、Cookie、Authorization header。
- `.env` 内容、真实密钥、数据库 DSN 或 MinIO 凭据。
- 真实客户数据、未脱敏手机号、地址或个人隐私。
- 大段日志、完整构建输出或无法复核的口头描述。

若截图包含敏感信息，MUST 先脱敏或仅记录摘要和不可公开原因。

### FR-007 N/A 与 follow-up 规则

模板 MUST 要求每个 `not_applicable`、`blocked` 或 `follow_up` 状态填写原因。

N/A 示例：

- 仅修改小程序静态测试，不改变真实页面渲染。
- 仅更新后端字段过滤，不影响小程序 UI 或交互。
- 仅新增模板文档，不涉及小程序运行时代码。

follow-up 示例：

- 已通过静态测试和 DevTools 预览，但缺少真机安全区验收。
- 已验证 375 pt，尚未覆盖 320 pt 或 430 pt。
- 当前无 Android 真机，只完成 iOS 真机验收。

### FR-008 引用与沉淀位置

模板 SHOULD 优先沉淀为长期标准文档：

```text
docs/standards/miniapp-device-evidence-template.md
```

后续小程序相关需求或 Change SHOULD 在以下位置引用该模板：

- REQ `acceptance.md` 的测试与验证章节。
- OpenSpec Change `tasks.md` 的人工验收任务。
- OpenSpec Change `trace.md` 或 `acceptance.md` 的 evidence 摘要。
- Sprint `acceptance-report.md` 的设备验收结果。
- Release note 的剩余风险或人工 follow-up 说明。

若后续需要让 `/req-complete`、`/opsx-apply` 或 `/sprint-archive` 自动提示该模板，应作为实现阶段的明确任务纳入 OpenSpec Change。

### FR-009 历史残留处理

模板 SHOULD 允许引用历史 Sprint 中的设备验收残留作为需求来源和风险案例。

本需求不强制回填历史 evidence；若后续团队决定回填，SHOULD 以单独任务或变更记录方式处理，避免把历史补录和模板建设混在一个交付闭环中。

## 6. UI / UE 约束

本需求不直接交付小程序可见页面，但模板 MUST 体现小程序 UI/UE 验收关注点：

- 自定义导航栏、状态栏、微信原生胶囊、返回/分享/关闭能力必须区分 DevTools 与真机结论。
- 固定头部、底部操作区、列表滚动和弹窗类交互需关注 320、375、430 pt 等常见宽度。
- 页面截图应尽量覆盖首屏、滚动后状态、空状态、异常状态和关键交互反馈。
- 模板文本应短、清晰、可复制，避免把验收说明写成无法执行的长段落。

## 7. 依赖与实施顺序

| 依赖 | 说明 |
|---|---|
| `rules/requirement-management.md` | REQ 生命周期、状态和评审门禁。 |
| `rules/document-governance.md` | 模板文档 frontmatter、时间和长期文档维护规则。 |
| `rules/directory-structure.md` | 长期标准文档、issues、OpenSpec 与 Sprint 的目录边界。 |
| `docs/standards/xl-admin-page-acceptance-template.md` | evidence、N/A reason、remaining risk 字段设计参考。 |
| `iterations/archive/sprint-008/acceptance-report.md` | DevTools/真机验收残留案例来源。 |
| `issues/requirements/archive/REQ-0048-miniapp-global-custom-navigation-bar` | 自定义导航栏真机避让与返回行为验收参考。 |
| `issues/requirements/archive/REQ-0050-miniapp-brand-header-page-title-rules` | 小程序 brand-header 页面标题和 DevTools/真机验证参考。 |

建议实施顺序：

1. 确认模板最终沉淀位置，优先 `docs/standards/miniapp-device-evidence-template.md`。
2. 明确 evidence 状态、必填字段、N/A / blocked / follow-up 规则。
3. 设计可复制 YAML / Markdown 表格模板。
4. 在 `/req-complete` 中补齐用户故事、业务流程和验收标准。
5. 评审通过后通过 OpenSpec Change 实现模板文档和必要的流程引用。

**建议 OpenSpec change 命名**：`add-miniapp-device-evidence-template`。

## 8. 关联需求

| 需求 / 模块 | 关系 |
|---|---|
| REQ-0039 XL 管理端页面分层验收模板 | evidence 字段、N/A 判定、remaining risk 和标准文档沉淀方式参考。 |
| REQ-0048 小程序全局自定义导航栏 | 真机避让、返回行为和 DevTools/真机验收残留案例。 |
| REQ-0050 小程序 brand-header 页面标题规则 | 后续首页双行文案和非首页标题规则需要 DevTools 或真机验证。 |
| BUG-0065 小程序首页预览运行入口修复 | DevTools 实际运行入口与静态测试边界的风险案例。 |

## 9. 状态

```yaml
requirement_id: REQ-0052-miniapp-device-evidence-template
priority: P1
status: done
iteration: sprint-009
owner: product
parent_requirement: null
openspec_change: null  # 建议 add-miniapp-device-evidence-template
target_clients:
  web_admin: 不涉及
  web_catalog: 不涉及
  wechat_miniapp: 本期模板服务对象
api_change: false
database_change: false
upload_change: false
orval_required: false
docker_compose_required: false
```
