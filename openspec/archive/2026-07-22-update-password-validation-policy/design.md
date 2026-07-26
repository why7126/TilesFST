## Context

`REQ-0063-password-validation-policy-simplification` 已评审通过，来源于 `REQ-0015-password-change` 的策略调整。现有 `auth`、`admin-password-change`、`user-management` specs 仍描述 effective 密码策略，可能包含大小写、特殊字符或更高最小长度。新需求要求基础策略更简单：5-32 位、包含英文字符、包含数字。

本 change 是跨后端认证、管理端修改密码弹窗、用户创建/重置密码生成的规范更新。实现阶段不得绕过既有鉴权、受保护账号、限流、弱密码表和 token_version 失效能力。

## Goals / Non-Goals

**Goals:**

- 建立统一的新密码基础策略：长度 5-32，ASCII 英文字符 `A-Z` / `a-z` 至少 1 个，ASCII 数字 `0-9` 至少 1 个。
- 让修改本人密码、创建用户、重置密码等设置新密码入口共享同一策略。
- 让前端字段提示和后端 API message/失败项一致，清除旧的“至少 8 位”、大小写、特殊字符提示。
- 保留 `trace.md` 中的 knowledge-base refs，供实现阶段处理管理端表单/弹窗横切验收。

**Non-Goals:**

- 不新增忘记密码、多因素认证、短信/邮箱验证。
- 不批量重置历史已设置密码。
- 不移除弱密码表、限流、原密码校验、新旧密码不得相同、token_version 失效。
- 不新增数据库字段。

## Decisions

### D1. 密码基础策略固定为 ASCII 英文 + ASCII 数字

新策略默认使用 ASCII 字母和 ASCII 数字判断，避免 Unicode 分类导致前后端正则、Python 校验和测试结果不一致。符号允许与英文/数字共同出现；空格、中文、全角数字等非 ASCII 字符不作为英文/数字满足项。

替代方案：继续使用 system_settings 的大小写/特殊字符开关。放弃原因是它与 REQ-0063 的“简化”目标冲突，并会继续造成提示和后端策略漂移。

### D2. 统一公共校验/生成入口

后续实现应优先调整现有 `validate_password()` 或等价公共函数，并让修改密码、创建用户、重置密码复用。随机初始密码和重置密码的生成器必须生成满足 5-32 位、英文、数字的结果。

替代方案：分别在每个 API 路由实现局部正则。放弃原因是多入口规则漂移风险高。

### D3. UI 策略采用 Design System 更新，不做 CSS Port 重构

本需求不新增独立页面，仅修改既有管理端密码字段提示。实现阶段应复用现有弹窗和表单组件，不改 token，不引入新视觉系统。

Conflict Resolution:

- 优先级：`prototype/web/password-policy-hints.html` > `prototype/web/context.md` > `acceptance.md` > `rules/ui-design.md` > archived specs。
- 原型仅约束字段提示位置和 520px 修改密码弹窗策略，不要求新增页面。
- 现有 spec 中大小写/特殊字符和 dynamic effective 策略说明被本 change 的 MODIFIED requirements 覆盖。

Knowledge-base refs:

- `docs/knowledge-base/best-practices/admin-form-page-consistency.md`
- `docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md`
- `docs/knowledge-base/retrospectives/sprint-008-retrospective.md`

## Risks / Trade-offs

- [Risk] 降低最小长度到 5 可能降低密码强度 → Mitigation: 保留弱密码表、限流、原密码校验和 token 失效；实现阶段补充边界测试。
- [Risk] 旧文案散落在前端组件或测试中 → Mitigation: tasks 要求搜索并清除“8-32 位”、大小写、特殊字符旧提示。
- [Risk] 随机密码生成仍按旧策略生成过长或要求特殊字符 → Mitigation: user-management delta spec 明确生成密码也必须满足新策略。
- [Risk] API failure data 字段变化影响前端 → Mitigation: 后续实现如改 schema，必须同步 OpenAPI/Orval 和 API 文档。

## Migration Plan

1. 更新公共密码校验/生成策略和测试。
2. 更新修改密码、用户创建/重置密码相关后端路径。
3. 更新管理端字段提示和前端测试。
4. 如 OpenAPI/错误码文档受影响，同步生成与文档。
5. 回归登录、修改密码、创建用户、重置密码、旧 token 失效和受保护账号测试。

Rollback: 恢复公共密码策略函数和前端提示到旧规则；不涉及数据库回滚。

## Open Questions

- 空格、中文、全角数字是否允许作为额外字符？本 change 默认不将其计入英文/数字满足项，是否允许作为密码内容由实现评审最终确认。
- 弱密码表是否需要新增 5-7 位常见弱密码样例？
