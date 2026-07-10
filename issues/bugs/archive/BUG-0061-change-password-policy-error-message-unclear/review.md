---
bug_id: BUG-0061-change-password-policy-error-message-unclear
title: 修改密码安全策略错误提示不清晰评审记录
status: approved
decision: approve
severity: medium
owner: product
reviewed_at: 2026-07-06 23:51:35
created_at: 2026-07-06 23:51:35
updated_at: 2026-07-06 23:51:35
related_requirement: REQ-0015-password-change
related_change: null
---

# 缺陷评审记录

## 1. 评审结论

结论：`approved`，确认需要修复。

BUG-0061 属于已交付管理端修改密码能力的可用性与错误反馈缺陷。当前后端密码策略校验可以拒绝不合规密码，但错误信息无法说明具体失败项；前端规则提示也未与当前有效策略保持一致，用户在失败后缺少明确修改方向。

该问题不构成安全绕过，但会显著增加内部用户修改密码的试错成本，并可能在密码策略配置更严格时被放大。

## 2. 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | `bug.md`、`root-cause.md` 已说明前端静态规则与后端可配置策略不一致，后端策略失败被合并为泛化 `policy`。 |
| 严重等级合理 | 通过 | `medium` 合理；不阻断登录、不绕过权限，但影响管理端改密可用性。 |
| 回归验收明确 | 通过 | `acceptance.md` 已覆盖长度、大小写、数字、特殊字符、弱密码、同原密码、动态策略、API 表达与测试。 |
| 是否需 hotfix 路径 | 不需要 | 当前不是生产阻断或安全事故，建议按常规 fix Change 进入开发。 |

## 3. 评审意见

- 后续修复不得放宽密码策略或绕过后端校验。
- 若 API 响应结构新增策略失败详情，必须同步 OpenAPI、Orval、`docs/03-api-index.md`、错误码/治理文档与后端/前端测试。
- 前端规则展示应以当前有效策略为准，避免继续硬编码与后端不一致的固定规则。
- 修复范围应覆盖 Web 管理端修改密码弹窗和后端策略失败表达；不涉及小程序、店主展示端、数据库 schema、MinIO 或 Docker Compose。

## 4. 后续动作

建议下一步执行：

```text
/bug-opsx BUG-0061
```

建议 Change ID：

```text
fix-change-password-policy-error-message
```

