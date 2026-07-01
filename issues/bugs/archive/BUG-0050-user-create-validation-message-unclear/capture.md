---
bug_id: BUG-0050-user-create-validation-message-unclear
status: captured
created_at: 2026-06-30 11:03:01
updated_at: 2026-06-30 11:03:01
severity_hint: medium
environment: local|docker
related_requirement: REQ-0005-user-management
related_bug:
captured_via: capture
classification_rationale: 用户创建已有校验规则，但失败时未明确指出具体不符合项，属于既有用户管理能力的反馈缺陷。
---

# 现象

创建用户时，当输入不符合规范，界面未明确显示具体问题点，导致用户无法根据错误提示优化输入。

# 复现步骤

1. 进入管理端用户管理页。
2. 打开创建用户入口。
3. 输入小于 4 位的用户名并提交。
4. 观察创建失败后的错误提示。

# 期望 vs 实际

- 期望：当用户名小于 4 位时，明确提示类似“用户名长度不能小于 4 位”，并能让用户知道需要修改哪个字段。
- 实际：校验失败提示不明确，未指出具体不符合规范的字段和原因。

# 附件

暂无。

# 待澄清

- [ ] 是否所有用户创建字段校验都需要字段级错误提示，而不仅是用户名长度
- [ ] 前端是否需要在提交前即时校验，还是仅展示后端返回的字段级错误
- [ ] 错误文案是否需与 API 错误码治理统一

# 分类说明（/capture）

`REQ-0005-user-management` 已约定用户名 4-32 位等规则，当前问题是既有创建用户能力在校验失败时未明确反馈，因此判定为 BUG。
