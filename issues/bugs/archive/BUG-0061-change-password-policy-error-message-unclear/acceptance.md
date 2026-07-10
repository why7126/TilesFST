---
bug_id: BUG-0061-change-password-policy-error-message-unclear
title: 修改密码安全策略错误提示不清晰验收标准
status: pending_review
severity: medium
owner: product
created_at: 2026-07-06 23:48:02
updated_at: 2026-07-07 00:21:09
related_requirement: REQ-0015-password-change
related_change: fix-change-password-policy-error-message
---

# 回归验收标准

> 修复本缺陷 MUST 让用户在修改密码失败时明确知道具体不满足哪一条密码安全策略，并能据此完成修改。

## AC-001 长度不足 MUST 展示具体原因

- GIVEN 用户已打开 Web 管理端“修改密码”弹窗。
- WHEN 用户输入正确原密码，并输入长度小于当前有效最小长度的新密码。
- THEN 页面 MUST 展示“至少需要 N 位字符”或等价文案。
- AND 文案中的 N MUST 与当前有效密码策略一致。
- AND 不得仅展示“新密码不符合安全策略”。

- [x] AC-001

## AC-002 缺少大写字母 MUST 展示具体原因

- GIVEN 当前有效密码策略要求包含大写字母。
- WHEN 用户提交的新密码缺少大写字母。
- THEN 页面 MUST 明确提示“需要包含大写字母”或等价文案。

- [x] AC-002

## AC-003 缺少小写字母 MUST 展示具体原因

- GIVEN 当前有效密码策略要求包含小写字母。
- WHEN 用户提交的新密码缺少小写字母。
- THEN 页面 MUST 明确提示“需要包含小写字母”或等价文案。

- [x] AC-003

## AC-004 缺少数字 MUST 展示具体原因

- GIVEN 当前有效密码策略要求包含数字。
- WHEN 用户提交的新密码缺少数字。
- THEN 页面 MUST 明确提示“需要包含数字”或等价文案。

- [x] AC-004

## AC-005 缺少特殊字符 MUST 展示具体原因

- GIVEN 当前有效密码策略要求包含特殊字符。
- WHEN 用户提交的新密码缺少特殊字符。
- THEN 页面 MUST 明确提示“需要包含特殊字符”或等价文案。

- [x] AC-005

## AC-006 弱密码 MUST 保留明确提示

- GIVEN 用户输入命中弱密码表的新密码。
- WHEN 提交修改密码表单。
- THEN 页面 MUST 展示“密码过于常见，请更换”或等价文案。
- AND 不得降级为泛化策略失败提示。

- [x] AC-006

## AC-007 新密码与原密码相同 MUST 保留明确提示

- GIVEN 用户输入的新密码与原密码相同。
- WHEN 提交修改密码表单。
- THEN 页面 MUST 展示“新密码不能与原密码相同”或等价文案。

- [x] AC-007

## AC-008 前端规则展示 MUST 与当前有效策略一致

- GIVEN 管理员在系统设置中调整密码最小长度或复杂度开关。
- WHEN 用户打开修改密码弹窗。
- THEN 弹窗展示的密码规则 MUST 与当前有效策略一致。
- AND 不得继续固定展示与后端不一致的旧规则。

- [x] AC-008

## AC-009 API 错误表达 MUST 支持前端展示具体失败项

- GIVEN 新密码不满足一项或多项策略。
- WHEN 调用 `POST /api/v1/admin/profile/password`。
- THEN API MUST 返回可被前端识别的具体失败信息。
- AND 若变更响应结构，MUST 同步 OpenAPI、Orval、`docs/03-api-index.md` 与错误码/治理文档。

- [x] AC-009

## AC-010 原密码错误、限流与受保护账号提示 MUST 无回归

- GIVEN 用户触发原密码错误、改密限流或系统保底管理员账号禁止改密。
- WHEN API 返回对应错误码。
- THEN 页面 MUST 继续展示对应明确文案。
- AND 不得误显示为密码策略失败。

- [x] AC-010

## AC-011 测试覆盖 MUST 补齐

- MUST 补充后端测试，覆盖长度不足、缺少大写、缺少小写、缺少数字、缺少特殊字符时的策略失败详情。
- MUST 补充前端测试，覆盖修改密码弹窗展示具体失败原因。
- MUST 保留既有成功改密、原密码错误、弱密码、与原密码相同、限流等回归用例。

- [x] AC-011

## AC-012 非目标范围

- 本缺陷修复不得放宽密码安全策略。
- 本缺陷修复不得绕过后端校验。
- 本缺陷修复不得记录或持久化明文密码。
- 本缺陷修复不涉及小程序、店主展示端、数据库 schema、MinIO 或 Docker Compose 配置。

- [x] AC-012
