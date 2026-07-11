---
requirement_id: REQ-0036-clipboard-helper-best-practice-docs
title: Clipboard helper best-practice 文档
terminal: web-admin
version: v1
status: approved
owner: product
source: capture.md
priority: P2
parent_requirement: REQ-0032-clipboard-copy-helper-best-practice
created_at: 2026-07-11 23:42:20
updated_at: 2026-07-11 23:53:49
---

# REQ-0036 Clipboard helper best-practice 文档

## 1. 需求背景

`REQ-0032` 已将 Web 管理端 Clipboard 复制交互沉淀为共享 helper 或最佳实践，并覆盖结构化结果、fallback、调用方提示和敏感内容安全边界。随着后续管理端继续新增复制入口，单有 helper 代码仍不足以约束调用方如何写提示文案、何时启用手动复制兜底、哪些值不得复制或不得进入日志。

当前风险在调用方：不同页面可能复用同一个 helper，却写出不一致的成功/失败提示；可能在 Clipboard API 不可用时只提示失败而没有可操作 fallback；也可能将 Token、密码、签名 URL、客户隐私字段等敏感值作为普通文本处理，造成安全边界漂移。

本需求用于建立 Clipboard helper best-practice 文档，把调用方文案、fallback 策略和敏感值边界沉淀为可复用约定，供 Web 管理端后续复制入口、测试用例和代码评审使用。

## 2. 目标用户

| 用户 | 诉求 |
|---|---|
| 前端开发人员 | 新增复制入口时知道应使用哪些提示文案、fallback 分支和安全检查。 |
| QA / 测试人员 | 能按固定清单验证成功、失败、API 不可用、手动复制和敏感值边界。 |
| 产品负责人 | 能保证复制交互的用户文案一致，并避免敏感内容被错误暴露。 |
| 安全 / 技术负责人 | 能在文档中明确哪些值允许复制、哪些值必须禁用或脱敏处理。 |

## 3. 需求目标

- 建立一份 Clipboard helper best-practice 文档，作为调用方接入复制 helper 的默认参考。
- 明确调用方在 `success`、`failed`、`unavailable`、`empty` 等结果下的推荐文案和行为。
- 明确 fallback 策略，包括自动复制失败、Clipboard API 不存在、空值、手动选择文本等场景。
- 明确敏感值边界，避免密码、Token、密钥、Cookie、客户隐私和签名 URL 等内容被误复制、误日志化或误展示。
- 为后续测试、代码评审和需求验收提供 checklist，而不是依赖口头约定。

## 4. 范围

### 4.1 本期包含

| 范围 | 说明 |
|---|---|
| best-practice 文档 | 新增或更新长期文档，沉淀 Clipboard helper 调用方约定。 |
| 调用方文案 | 规定成功、失败、浏览器不支持、内容为空、需手动复制等提示原则。 |
| fallback 策略 | 规定何时触发手动选择文本、何时隐藏复制入口、何时提示用户手动复制。 |
| 敏感值边界 | 定义可复制、谨慎复制、禁止复制或必须脱敏的典型数据类别。 |
| 调用方 checklist | 为新增复制入口提供代码评审和 QA 验证清单。 |
| 关联 helper 说明 | 与 `REQ-0032` 已沉淀的 Clipboard helper 能力保持一致。 |

### 4.2 本期不包含

| 不包含 | 说明 |
|---|---|
| 新增 Clipboard helper 实现 | helper 能力已由 `REQ-0032` 承接，本需求只沉淀文档与调用方约定。 |
| 批量迁移所有复制入口 | 是否迁移历史页面由后续 OpenSpec Change 或专项修复决定。 |
| 新增业务复制入口 | 本需求不新增复制 Token、对象 Key、接口路径等业务入口。 |
| 小程序复制适配 | 微信小程序 Clipboard API 边界不同，本期仅可记录不适用说明。 |
| 后端 API 变更 | 不新增或修改后端接口。 |
| 数据库变更 | 不修改 SQLite / MySQL 表结构、迁移或初始化数据。 |
| Orval 生成 | 不涉及 OpenAPI 或前端接口类型生成。 |

## 5. 功能要求

### FR-001 文档落位与适用范围

- MUST 建立 Clipboard helper best-practice 文档，落位应符合 `docs/` 长期文档或 Web 前端说明的目录职责。
- MUST 在文档开头说明适用范围：优先适用于 Web 管理端调用浏览器 Clipboard API 的复制入口。
- MUST 明确该文档是调用方约定，不替代 `REQ-0032` 中 helper 的实现要求。
- SHOULD 从文档中链接或引用 `REQ-0032`、Web README、相关测试或 helper 文件路径，便于追溯。

### FR-002 调用方文案规范

文档 MUST 定义调用方针对结构化结果的推荐提示原则：

| 结果 | 推荐文案原则 |
|---|---|
| `success` | 使用业务语义，例如“request_id 已复制”“密码已复制”。 |
| `failed` | 告知自动复制失败，并提示用户手动复制。 |
| `unavailable` | 告知当前浏览器或环境无法自动复制，并提示手动复制。 |
| `empty` | 告知当前内容为空，或要求调用方隐藏 / 禁用复制入口。 |

- MUST 保留业务对象名称，不得所有场景都使用无法区分的“复制成功/复制失败”。
- MUST 避免在提示文案中直接回显敏感值。
- SHOULD 说明 toast、`role="status"`、弹窗帮助文案等反馈载体的选用原则。

### FR-003 fallback 策略

- MUST 说明自动复制失败或 Clipboard API 不可用时的降级路径。
- MUST 说明何时应调用 `fallbackSelect` 或等价回调，让用户可以手动复制可见文本。
- SHOULD 说明空值场景优先隐藏或禁用复制入口，而不是点击后再提示失败。
- SHOULD 说明 fallback 失败时调用方仍需给出清晰提示，不得让点击行为无反馈。
- MUST 不要求 helper 直接绑定 toast、dialog 或特定 DOM 结构，fallback 行为由调用方按场景接入。

### FR-004 敏感值边界

文档 MUST 定义至少三类复制边界：

| 类别 | 示例 | 处理原则 |
|---|---|---|
| 允许复制 | `request_id`、公开版本号、用户可见业务编号 | 可复制，但仍不得写入无关日志。 |
| 谨慎复制 | 随机密码、一次性凭证、对象存储签名 URL | 仅在用户已授权可见且业务明确需要时复制，并给出安全提示。 |
| 禁止或默认不复制 | AccessKey、SecretKey、Token、Cookie、Authorization、客户隐私原文 | 不提供复制入口，或必须脱敏 / 走专门安全流程。 |

- MUST 明确 helper 和调用方都不得将复制内容写入错误消息、埋点 payload、测试快照或控制台日志。
- MUST 明确复制入口不得绕过权限边界：只能复制用户已授权查看的内容。
- SHOULD 对签名 URL、临时密码等时效性敏感值说明有效期和二次展示边界。

### FR-005 调用方接入 checklist

best-practice 文档 MUST 提供调用方 checklist，至少覆盖：

- 复制内容是否为用户已授权可见。
- 复制内容是否属于允许 / 谨慎 / 禁止复制类别。
- 是否根据结构化结果提供不同提示。
- 是否有 `failed` 和 `unavailable` fallback。
- 空值时是否禁用或隐藏复制入口。
- 是否避免在日志、埋点、错误消息和测试输出中记录复制原文。
- 是否有成功、失败、API 不可用、空值和 fallback 的测试覆盖。

### FR-006 示例与反例

- SHOULD 提供 1-2 个推荐调用示例，例如复制 `request_id`、复制重置后的随机密码。
- SHOULD 提供反例说明，例如在 toast 中回显 Token、在埋点中记录复制内容、无 Clipboard API 时静默失败。
- MUST 保持示例使用脱敏或虚构值，不得引入真实密钥、真实客户数据或真实生产 URL。

## 6. UI 约束

- 本需求不新增页面、弹窗或视觉组件。
- 文档中的提示文案应遵守现有管理端语气：清晰、简短、可操作。
- 复制反馈应优先复用现有 toast、弹窗内提示或 `role="status"`；不因本文档新增独立视觉样式。
- 文档示例不得使用裸 Hex 或新增 Design System token。
- 对敏感值场景，文案必须强调“可见且授权”与“复制后安全交付”，避免暗示所有敏感内容都可复制。

## 7. 关联需求与文档

| 类型 | 关联项 | 说明 |
|---|---|---|
| 父需求 | `REQ-0032-clipboard-copy-helper-best-practice` | 已沉淀 Clipboard helper / best-practice 的实现与验收边界。 |
| 相关需求 | `REQ-0000-build-design-system` | 前端设计系统和交互治理父需求。 |
| 相关需求 | `REQ-0024-product-usage-logging` | 日志审计复制 `request_id` 与埋点边界。 |
| 相关文档 | `src/web/README.md` | 可作为 Web 前端共享工具和使用约定入口。 |
| 相关目录 | `docs/knowledge-base/best-practices/` | 可作为 best-practice 长期沉淀位置。 |
| 相关规则 | `rules/security.md` | 敏感信息、密钥、上传与权限边界。 |

## 8. 风险与约束

| 风险 | 说明 | 缓解 |
|---|---|---|
| 文档位置不清 | 若落在临时 README 或 issue 内，后续调用方难以发现。 | 在 OpenSpec 阶段确认长期文档位置，并从 Web README 或知识库入口链接。 |
| 文案继续漂移 | 文档只写原则但没有 checklist，评审时仍可能遗漏。 | 必须提供调用方 checklist 和示例/反例。 |
| 敏感值误复制 | 调用方可能把所有字符串都视作可复制文本。 | 明确允许、谨慎、禁止三类边界，并要求不记录复制原文。 |
| fallback 体验不一致 | 不同页面失败时反馈差异大。 | 固定结构化结果到调用方行为映射。 |
| 过度扩大范围 | 可能被误解为要重构所有现有复制入口。 | 本期只生成文档，不默认批量迁移历史页面。 |

## 9. 状态块

```yaml
status: approved
readiness: Ready
next_step: /req-opsx REQ-0036-clipboard-helper-best-practice-docs
expected_openspec_change: add-clipboard-helper-best-practice-docs
needs_prototype: false
needs_api_change: false
needs_database_change: false
needs_orval: false
needs_docker_validation: false
```

## 10. 待完善项

- `/req-complete` 阶段补充 user stories、business flow 和 acceptance。
- 评审阶段确认 best-practice 文档最终落位：`docs/knowledge-base/best-practices/`、`docs/standards/` 或 `src/web/README.md` 固定章节。
- OpenSpec 阶段确认是否只新增文档，还是同步更新 Web README 入口和相关检查清单。
