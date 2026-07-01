---
bug_id: BUG-0050-user-create-validation-message-unclear
title: 创建用户校验失败未明确提示具体问题点 - 临时规避
severity: medium
status: pending_review
owner: product
created_at: 2026-06-30 18:11:55
updated_at: 2026-06-30 18:11:55
related_requirement: REQ-0005-user-management
---

# 临时规避方案

## 管理员操作规避

在修复前，后台管理员创建用户时可按以下规则自行检查用户名：

- 长度为 4-32 位。
- 必须以小写字母开头。
- 只能包含小写字母、数字、`_`、`-`、`.`。
- 不使用连续两个及以上特殊符号，例如 `__`、`--`、`..`。
- 不使用系统保留字，例如 `admin`、`root`、`system`、`test`、`user`。

推荐格式示例：

```text
store_user_01
operator01
demo-user.01
```

## 客服/运营说明

如果创建失败但界面仅展示泛化失败文案，可先按用户名规则调整后重试。若仍失败，再检查是否为用户名重复或角色参数异常。

## 技术规避

修复前不建议通过临时绕过后端校验创建用户。所有用户创建仍必须走 `POST /api/v1/admin/users`，保持管理员鉴权与服务端校验。

## 风险

该规避方案依赖人工理解规则，不能消除体验问题；仍可能导致管理员重复试错。因此该 BUG 仍需进入后续修复流程。
