---
requirement_id: REQ-0096-miniapp-network-panel-release-checklist
title: 小程序网络面板验证纳入发布准备清单
terminal: miniapp
version: v1
status: done
owner: product
source: capture.md
priority: P1
parent_requirement:
created_at: 2026-08-04 08:32:00
updated_at: 2026-08-04 09:29:31
---

# REQ-0096 小程序网络面板验证纳入发布准备清单

## 1. 需求背景

小程序发布前现有 `/miniapp-prepare` 流程已经覆盖生产环境策略切换、`urlCheck=true`、小程序静态测试、生产接口 smoke，以及上传开发版本和设置体验版的人工 checklist。但这些自动化和流程动作仍不能完全证明体验版中的真实网络链路已经符合发布要求。

微信小程序的真实运行链路可能受到合法域名、体验版环境策略、基础库、手机网络、图片/视频资源域名、后端代理或对象存储 URL 策略影响。若只记录“静态测试通过”或“生产接口 smoke 通过”，发布负责人仍可能遗漏以下问题：

- DevTools 或体验版实际请求仍指向本地或错误环境。
- 体验版请求域名未命中生产合法域名。
- API HTTP 状态为 200，但业务 `code` 或页面错误态异常。
- 图片、证书、视频等资源在接口 smoke 之外加载失败。
- 网络失败、资源失败或权限失败没有进入发布前阻断或 follow-up 记录。

本需求用于将 DevTools 与体验版网络面板验证纳入 release/miniapp 准备清单，复用现有小程序设备 evidence 口径，并补齐发布前 Network evidence 的人工确认入口。

## 2. 目标用户

| 用户 | 诉求 |
|---|---|
| 发布负责人 | 在提审或发布前明确知道小程序体验版的请求环境、接口状态和资源加载是否已确认。 |
| 测试 / 验收人员 | 按固定清单在 DevTools 和体验版中检查 Network evidence，避免遗漏页面或资源类型。 |
| 小程序开发 | 能快速定位环境策略、合法域名、接口状态码、业务错误码或资源 URL 问题。 |
| 产品负责人 | 能区分自动化 smoke 通过、DevTools Network 通过、体验版 Network 通过和仍待 follow-up 的状态。 |
| AI / Codex Agent | 在后续 release、miniapp、Sprint 或 OpenSpec 流程中引用统一清单，不把静态测试误写成真实网络链路已通过。 |

## 3. 需求目标

- 将小程序 DevTools 网络面板验证纳入发布准备清单。
- 将小程序体验版网络面板或等价体验路径验证纳入发布准备清单。
- 明确 Network evidence 与现有静态测试、生产接口 smoke、DevTools/真机设备 evidence 的边界。
- 支持记录请求域名、API 环境、HTTP 状态、业务 code、静态资源和媒体资源加载结论。
- 支持 `passed`、`failed`、`blocked`、`follow_up`、`not_applicable` 等发布准备结论。
- 不新增自动抓包、自动截图、云真机或小程序运行时代码能力。

## 4. 范围

### 4.1 本期包含

| 范围 | 说明 |
|---|---|
| DevTools Network checklist | 在微信开发者工具中检查关键页面请求、域名、状态码、业务响应和资源加载。 |
| 体验版 Network checklist | 在体验版或手机体验路径中确认生产域名、接口可达和资源加载表现。 |
| 发布准备输出 | `/miniapp-prepare` 或 release/miniapp 准备输出需要提示 Network evidence 必验项和记录口径。 |
| 验证结果记录 | `/miniapp-confirm` 或发布记录需要承接 Network evidence 的通过、阻塞、失败和 follow-up 摘要。 |
| 关键路径范围 | 至少覆盖首页、分类/品牌入口、品牌列表、SKU 列表、SKU 详情、证书列表或证书详情等公开浏览链路。 |
| 资源类型范围 | 覆盖 API 请求、图片、视频、证书图片、静态资源和受控媒体 URL 的加载结论。 |
| 安全边界 | 证据记录不得包含 token、Cookie、Authorization header、`.env`、真实密钥、真实用户隐私或未脱敏完整日志。 |

### 4.2 本期不包含

| 不包含 | 说明 |
|---|---|
| 自动抓包或 HAR 导出工具 | 本需求只要求人工 Network evidence 清单，不要求自动采集或解析网络日志。 |
| 云真机或自动截图能力 | 不新增真机云测、自动截图、录屏或微信开发者工具自动化。 |
| 小程序业务功能改造 | 不新增或修改小程序页面、组件、样式、路由、服务或状态管理。 |
| 后端 API 改造 | 不新增接口、响应字段、错误码或鉴权逻辑。 |
| 数据库或 Orval 改造 | 不涉及数据库结构、迁移、OpenAPI schema 或 Orval 生成物。 |
| 替代设备 evidence 模板 | 本需求复用并扩展现有 evidence 口径，不替代 `docs/standards/miniapp-device-evidence-template.md`。 |
| 回填历史发布证据 | 不强制补录历史 release 或 Sprint 中缺失的 Network evidence。 |

## 5. 功能要求

### FR-001 发布准备清单必须包含 DevTools Network 验证

系统 MUST 在小程序发布准备清单中明确要求执行 DevTools 网络面板验证。

DevTools Network 验证 MUST 至少记录：

- 微信开发者工具版本或可识别版本摘要。
- 小程序基础库版本。
- 运行策略或环境策略，例如 `prod`、`auto` 或等价说明。
- `urlCheck` 状态。
- 被验证页面路径和关键 query。
- 请求域名是否为生产域名。
- 关键 API 的 HTTP 状态和业务响应状态。
- 图片、证书、视频或静态资源是否加载成功。
- 验证结论和剩余风险。

若 DevTools 只能证明开发者工具预览，不足以代表体验版或真机网络表现，结论 MUST 明确“不等同于体验版或真机网络验收”。

### FR-002 发布准备清单必须包含体验版 Network 验证

系统 MUST 在小程序发布准备清单中明确要求执行体验版 Network 验证，或记录无法执行体验版验证的阻塞原因。

体验版 Network 验证 MUST 至少覆盖：

- 微信公众平台已将最新开发版本设为体验版。
- 手机已删除旧体验版入口并重新扫码最新体验版二维码。
- 体验版请求生产 API 域名。
- 首页和至少一个列表页能够正常加载。
- SKU 详情、证书详情或媒体资源页面中图片/视频/证书资源能够加载或展示明确失败态。
- 若体验版 Network 工具不可用，人工记录必须说明替代观察方式、验证入口和剩余风险。

体验版 Network 验证缺失时，不得写作 `passed`；只能记录为 `blocked`、`follow_up` 或明确的 `not_applicable`。

### FR-003 Network evidence 状态与阻断规则

Network evidence MUST 使用统一状态：

```yaml
status: required | passed | failed | blocked | not_applicable | follow_up
```

状态含义：

| 状态 | 含义 |
|---|---|
| `required` | 已识别为发布前必验，尚未执行或尚未记录。 |
| `passed` | 已验收通过，并有可复核摘要或证据入口。 |
| `failed` | 已验收失败，必须记录失败表现、影响范围和处理建议。 |
| `blocked` | 账号、设备、体验版、域名、网络、后端服务或外部依赖阻塞。 |
| `not_applicable` | 当前发布不涉及小程序运行态或网络链路，必须写明原因。 |
| `follow_up` | 可发布但保留后续人工补证，必须写明剩余风险和责任人。 |

以下情况 SHOULD 阻断发布准备通过：

- 生产 API smoke 失败。
- DevTools 或体验版实际请求仍指向本地或非预期环境。
- 关键 API 返回非 2xx HTTP 状态且页面无可接受降级。
- 关键业务响应失败且影响首页、列表或详情主路径。
- 图片、视频或证书资源域名不合法，导致关键页面核心内容不可用。

以下情况 MAY 记录为 follow-up，但必须显式说明风险：

- DevTools Network 已通过，但体验版 Network 因账号或设备原因暂未补齐。
- 体验版主路径已通过，但部分非核心页面或非本次变更页面未逐项覆盖。
- 真机 Network 证据不可保存，只能提供人工摘要。

### FR-004 关键页面与资源范围

Network checklist SHOULD 将页面分为“必验主路径”和“按发布范围扩展路径”。

必验主路径 SHOULD 包含：

| 页面 / 场景 | 关注点 |
|---|---|
| 首页 | 首页聚合接口、Banner、推荐商品、静态资源和错误态。 |
| 分类或品牌入口 | 列表入口跳转、分页请求、空态和网络失败提示。 |
| 品牌列表或品牌详情 | 品牌 Logo、品牌商品列表、类目汇总和图片资源。 |
| SKU 列表 | 商品卡片、主图/缩略图、分页和接口状态。 |
| SKU 详情 | 商品详情接口、图片、视频、备注、失败态和受控媒体 URL。 |
| 证书列表或证书详情 | 证书图片、证书文件、空态和资源加载失败态。 |

若某次发布不包含部分页面，记录 SHOULD 使用 `not_applicable` 并说明原因，而不是删除检查项。

### FR-005 与现有 evidence 模板复用

本需求 SHOULD 复用 `docs/standards/miniapp-device-evidence-template.md` 的证据状态、页面路径、环境字段和安全边界。

后续实现 MAY 扩展该模板或新增相邻小节，表达以下来源：

```yaml
source: network_devtools | network_trial
```

Network evidence 与设备 evidence 的关系：

| 证据 | 可证明 | 不可替代 |
|---|---|---|
| 静态测试 | 文件结构、运行入口、配置和约束 | 不证明真实网络请求通过 |
| 生产接口 smoke | 指定接口在服务端或脚本层可达 | 不证明小程序体验版实际请求链路通过 |
| DevTools Network | 开发者工具中页面请求、域名、接口和资源加载 | 不等同于体验版或真实手机网络表现 |
| 体验版 Network | 体验版真实入口下的生产请求链路 | 不覆盖所有设备、网络运营商和微信版本 |
| 真机设备 evidence | 真实渲染、触控、安全区和微信原生能力 | 不自动证明全部请求和媒体资源都可达 |

### FR-006 `/miniapp-prepare` 输出要求

后续实现中，`/miniapp-prepare` 或等价准备命令 SHOULD 在成功输出中包含 Network checklist。

输出 SHOULD 包含：

- 已完成自动门禁：prod 策略、`urlCheck=true`、静态测试、生产接口 smoke。
- 待人工执行：上传开发版本、设置体验版、重新扫码体验版。
- 待人工执行：DevTools Network 检查。
- 待人工执行：体验版 Network 检查。
- 下一步：使用 `/miniapp-confirm` 记录验证结论，或在阻塞时记录 blocked/follow_up。

命令不得把人工 Network checklist 的未执行状态写作自动通过。

### FR-007 `/miniapp-confirm` 记录要求

后续实现中，`/miniapp-confirm` 或等价确认命令 SHOULD 支持在 notes 或结构化输出中承接 Network evidence 摘要。

确认记录 SHOULD 至少表达：

- 渠道：`trial` 或 `release`。
- 版本号或发布对象。
- 验证结果：`passed`、`blocked` 或 `follow_up`。
- DevTools Network 结论。
- 体验版 Network 结论。
- 失败项、阻塞项、剩余风险和下一步。

记录 MUST 不包含敏感信息、微信会话密钥、Cookie、Authorization header、`.env` 内容或真实用户隐私。

### FR-008 release/miniapp 文档与模板同步

后续实现 SHOULD 同步更新相关技能、脚本、README、标准文档或 release 准备模板，使 Network checklist 能被发布负责人看见并复用。

可能受影响位置包括：

- `.agents/skills/miniapp-prepare/SKILL.md`
- `.agents/skills/miniapp-confirm/SKILL.md`
- `scripts/miniapp-env.py`
- `src/miniapp/README.md`
- `docs/standards/miniapp-device-evidence-template.md`
- release 或 Sprint 验收报告中的小程序发布准备说明

实际修改范围以后续 OpenSpec Change 为准。

## 6. UI / UE 约束

本需求不新增小程序可见 UI，也不修改 Web 管理端或店主 Web 页面。

Network checklist 作为命令输出或文档模板时应满足：

- 文案短、可勾选、可复制，适合发布前逐项确认。
- 页面路径、状态、证据和剩余风险应可扫读。
- 不用复杂表述替代明确结论；`blocked`、`failed`、`follow_up` 必须比“待确认”更具体。
- 涉及小程序页面时，应使用微信小程序页面路径和场景描述，不使用浏览器专属概念作为通过标准。

若后续将 checklist 展示在 Web UI 中，必须遵守 Design System semantic token，不得直接写裸 Hex。

## 7. 非功能约束

- MUST 遵守小程序平台限制和合法域名策略。
- MUST 遵守安全规则，不记录 token、Cookie、Authorization header、`.env`、真实密钥、真实客户数据或未脱敏日志。
- MUST 遵守媒体和对象存储规范，小程序资源加载继续通过后端受控 URL、代理 URL、签名 URL 或已批准的公开策略，不得绕过后端直连未授权对象存储。
- MUST 保持发布准备清单轻量，不把人工 Network evidence 扩展成无法执行的大型审计。
- SHOULD 支持后续自动化增强，但本期不强制实现自动抓包、截图或真机云测。

## 8. 关联需求与规范

| 类型 | ID / 文件 | 关系 |
|---|---|---|
| 关联需求 | `REQ-0052-miniapp-device-evidence-template` | 复用 DevTools/真机 evidence 状态、字段和安全边界。 |
| 关联需求 | `REQ-0091-media-bug-four-point-acceptance-template` | 媒体资源 render、URL、blocked/follow_up 记录可作为资源加载验证参考。 |
| 关联规范 | `docs/standards/miniapp-device-evidence-template.md` | 后续可扩展 Network evidence 来源或相邻小节。 |
| 关联规范 | `rules/media.md` | 小程序媒体资源展示、失败态和 evidence 记录要求。 |
| 关联规范 | `rules/object-storage.md` | 受控媒体 URL、合法域名、对象访问和安全边界。 |
| 关联脚本 | `scripts/miniapp-env.py` | 当前 `/miniapp-prepare` checklist 的实现位置。 |
| 关联文档 | `src/miniapp/README.md` | 小程序环境策略、`urlCheck` 和命令族说明。 |
| 来源复盘 | `docs/knowledge-base/retrospectives/sprint-014-retrospective.md` | 设备/Network evidence 应前置到发布流程，避免 archive 后遗漏。 |

## 9. 状态块

```yaml
requirement_id: REQ-0096-miniapp-network-panel-release-checklist
status: done
lifecycle_stage: plan
readiness: Ready
next_command: /req-opsx REQ-0096-miniapp-network-panel-release-checklist
notes:
  - 已完成 /req-review --approve，需求评审通过。
  - 后续 OpenSpec Change 应明确是否扩展 miniapp-device evidence 模板，或只更新 miniapp 命令 checklist。
  - 本需求不直接修改 API、数据库、Orval、小程序业务页面或 Docker Compose。
```
