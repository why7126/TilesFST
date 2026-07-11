---
requirement_id: REQ-0032-clipboard-copy-helper-best-practice
title: Clipboard 复制交互沉淀共享 helper 或 best-practice
terminal: web-admin
version: v1
status: archived
owner: product
source: capture.md
priority: P1
parent_requirement: REQ-0000-build-design-system
created_at: 2026-07-11 16:00:27
updated_at: 2026-07-11 20:10:50
---

# REQ-0032 Clipboard 复制交互沉淀共享 helper 或 best-practice

## 1. 需求背景

Web 管理端已经出现多处复制交互，包括日志审计页复制 `request_id`、重置密码弹窗复制随机密码等。这些场景都需要调用浏览器 Clipboard API，并在复制成功、写入失败、API 不存在或需要用户手动复制时给出明确反馈。

当前复制逻辑分散在页面或组件内部：不同场景各自判断 `navigator.clipboard?.writeText`，各自处理失败提示和手动选择文本。短期看可以工作，但后续如果继续新增复制入口，例如复制接口路径、版本号、对象 key、日志字段或账号信息，就容易重复实现、文案漂移、测试遗漏，甚至在不支持 Clipboard API 的浏览器中出现无反馈的失败。

本需求将 Clipboard 复制交互沉淀为共享 helper 或前端最佳实践，优先服务 Web 管理端，并为店主 Web 端后续复用保留边界。目标不是引入新的 UI 体系，而是统一复制动作的结果判断、兜底策略和测试口径。

## 2. 目标用户

| 用户 | 诉求 |
|---|---|
| 企业内部管理员 / 运营人员 | 点击复制后获得明确反馈，失败时知道如何手动复制。 |
| 前端开发人员 | 新增复制入口时复用统一 helper，不再在页面内重复处理 Clipboard API 分支。 |
| QA / 测试人员 | 能用稳定用例覆盖成功、失败、API 不存在和手动复制兜底。 |
| 产品负责人 | 将已有复制交互经验沉淀为 Design System / 前端工程能力，减少体验漂移。 |

## 3. 需求目标

- Web 管理端复制文本能力必须有统一或等价的 helper / best-practice。
- 复制动作必须返回结构化结果，调用方能区分成功、失败、API 不存在、空值或需要手动复制。
- 手动复制兜底必须有明确策略，例如调用方传入 `fallbackSelect` 来选中文本。
- helper 不直接绑定 toast、dialog 或埋点体系，避免把业务事件耦合进通用工具。
- 现有日志审计复制 `request_id` 与重置密码复制随机密码可作为首批迁移或验收参考。

## 4. 范围

### 4.1 本期包含

| 范围 | 说明 |
|---|---|
| Web 管理端复制 helper | 提供 `copyTextToClipboard` 或等价工具，封装 Clipboard API 调用与结果归一化。 |
| 结构化结果 | 支持 `success`、`failed`、`unavailable`、`empty` 等状态，便于调用方展示不同反馈。 |
| 手动复制兜底 | 支持可选 fallback，例如聚焦并选中输入框文本，让用户使用 Command/Ctrl + C。 |
| 调用方提示约定 | 明确成功、失败、API 不存在、手动复制的推荐提示原则。 |
| 代表场景覆盖 | 至少以日志审计 `request_id` 和重置密码随机密码作为现有场景参考。 |
| 前端测试 | 覆盖 Clipboard API 成功、reject、API 不存在、空值和 fallback 调用。 |
| 文档或约定沉淀 | 在 Web README、Design System 说明或需求验收中记录使用边界。 |

### 4.2 本期不包含

| 不包含 | 说明 |
|---|---|
| 新增业务复制入口 | 本需求沉淀能力，不主动新增复制接口路径、对象 key 等业务入口。 |
| 引入新的 toast / dialog 体系 | 复制结果由调用方接入既有反馈组件，不新增全局提示库。 |
| 小程序 Clipboard API 适配 | 微信小程序复制接口差异较大，本期只记录边界，不纳入同一实现。 |
| 浏览器权限系统治理 | 不开发权限探测或权限弹窗，只处理 Clipboard API 调用结果。 |
| 后端 API 变更 | 不新增或修改后端接口。 |
| 数据库变更 | 不修改 SQLite / MySQL 表结构、迁移或初始化数据。 |
| Orval 生成 | 不涉及 OpenAPI 或前端接口类型生成。 |

## 5. 功能要求

### FR-001 共享复制 helper

- MUST 提供 Web 前端可复用的复制 helper 或等价 best-practice，优先放在共享前端工具边界中。
- MUST 接收待复制文本，并在调用前执行基本空值 / 空白字符串判断。
- MUST 使用 `navigator.clipboard.writeText` 时保持正确调用上下文，避免因 `this` 绑定导致浏览器兼容问题。
- MUST 在 Clipboard API 不存在时返回明确状态，而不是静默失败。
- MUST 在 Clipboard API reject 或抛错时返回失败状态，并允许调用方进入手动复制兜底。

### FR-002 结构化结果

helper 返回结果 MUST 能表达以下状态或等价语义：

| 状态 | 说明 |
|---|---|
| `success` | 自动复制成功。 |
| `failed` | Clipboard API 存在但写入失败。 |
| `unavailable` | 当前环境不存在可用 Clipboard API。 |
| `empty` | 待复制文本为空或仅包含空白。 |

结果 MAY 包含归一化后的文本、错误对象或失败原因，但不得把敏感值写入日志或错误消息。

### FR-003 手动复制兜底

- MUST 支持由调用方提供可选手动复制回调，例如 `fallbackSelect`。
- SHOULD 在 `failed` 与 `unavailable` 场景调用该回调，使用户可以直接使用 Command/Ctrl + C 复制已选中文本。
- SHOULD 保持 fallback 与 UI 解耦：helper 只触发回调，不直接操作特定 DOM 结构。
- MUST 保证 fallback 回调失败时不会中断调用方渲染；调用方仍可展示手动复制提示。

### FR-004 UI 反馈约定

- MUST 明确调用方根据结构化结果展示提示：
  - `success`：展示“已复制”类成功反馈；
  - `failed`：展示“自动复制失败，请手动复制”类提示；
  - `unavailable`：展示“当前浏览器无法自动复制，请手动复制”类提示；
  - `empty`：展示“当前内容为空，无法复制”或隐藏复制入口。
- MUST 保留业务语义，例如 `request_id 已复制`、`密码已复制`，不得把所有场景压成无法区分的通用文案。
- SHOULD 使用既有 `role="status"`、toast 或弹窗内帮助文案承载反馈，保证可访问性。
- MUST 不新增与现有暗色管理端风格冲突的视觉样式。

### FR-005 代表场景迁移策略

- SHOULD 将日志审计页复制 `request_id` 接入共享 helper，保持复制成功后埋点行为不变。
- SHOULD 将重置密码弹窗复制随机密码接入共享 helper，保留失败时选中密码输入框的手动复制体验。
- MUST 保证迁移后既有用户可见文案不发生无意回退。
- MUST 保证迁移后空 `request_id` 行不展示或不触发无效复制动作。

### FR-006 测试要求

- MUST 为 helper 增加前端单元测试，覆盖成功、Clipboard API reject、Clipboard API 不存在、空值和 fallback 调用。
- MUST 为代表调用方保留或补充测试，确认业务文案和埋点不回退。
- SHOULD 在测试中显式模拟 `navigator.clipboard` 缺失，避免只覆盖 happy path。
- SHOULD 覆盖 fallback 选择文本的行为，例如输入框 `focus()` 与 `select()` 被调用。

## 6. UI 约束

- 本需求不新增页面原型，不改变管理端整体布局。
- 复制按钮应优先使用现有按钮、图标按钮或业务页面已有样式，不新增裸 Hex 或孤立 CSS 主题。
- 反馈文案应接入现有 toast、`role="status"` 或弹窗内帮助文本。
- 对敏感内容，例如随机密码，失败时应优先选中当前可见输入框文本，而不是把敏感内容写入额外日志或全局状态。
- 移动端浏览器若不支持自动复制，应降级为清晰的手动复制提示，不得出现点击后无反馈。

## 7. 权限与安全

- MUST 不复制用户无权查看的内容；helper 只处理调用方已展示或已授权可用的文本。
- MUST 不在 helper 内记录复制内容、密码、token、Authorization、Cookie、对象存储 key 或其他敏感值。
- MUST 不通过后端接口绕过浏览器 Clipboard 限制。
- SHOULD 对随机密码等敏感内容保持现有安全提示，例如关闭后不可再次查看、复制后需安全交付。

## 8. 关联需求与规范

| 类型 | 关联项 | 说明 |
|---|---|---|
| 父需求 | `REQ-0000-build-design-system` | 前端 Design System / 交互治理父需求。 |
| 相关需求 | `REQ-0028-admin-list-page-contract` | 管理端横切交互与模板契约沉淀的相似治理模式。 |
| 相关需求 | `REQ-0024-product-usage-logging` | 日志审计复制 `request_id` 的埋点行为需保持兼容。 |
| 相关页面 | `src/web/src/pages/admin/LogAuditPage.tsx` | 现有复制 `request_id` 场景。 |
| 相关组件 | `src/web/src/features/admin/components/ResetPasswordDialog.tsx` | 现有复制随机密码与手动选择兜底场景。 |
| 相关说明 | `src/web/README.md` | Web Design System 与共享工具使用约定。 |

## 9. 风险与约束

| 风险 | 说明 | 缓解 |
|---|---|---|
| 过度抽象 | 复制场景差异较小，但 UI 提示和埋点差异较大。 | helper 只返回结果，不绑定 toast、文案或埋点。 |
| 敏感信息泄露 | 随机密码等内容若进入错误日志会扩大风险。 | helper 不记录复制文本，测试也避免输出敏感值。 |
| 浏览器兼容差异 | 非安全上下文、权限拒绝或旧浏览器可能无法自动复制。 | 使用 `unavailable` / `failed` 状态和手动复制 fallback。 |
| 迁移影响现有体验 | 已有页面文案、埋点、选中文本行为可能被通用化时丢失。 | 将日志审计和重置密码作为代表回归测试。 |
| 小程序差异 | 小程序复制 API 与浏览器不同。 | 本期明确不纳入小程序实现，后续单独评估。 |

## 10. 状态

```yaml
status: archived
lifecycle_stage: plan
next: /req-opsx REQ-0032-clipboard-copy-helper-best-practice
readiness: Ready
needs_prototype: false
needs_api_change: false
needs_database_change: false
needs_orval: false
needs_docker_validation: false
```
