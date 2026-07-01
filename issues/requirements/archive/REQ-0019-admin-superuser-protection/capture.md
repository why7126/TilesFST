---
req_id: REQ-0019-admin-superuser-protection
status: captured
created_at: 2026-06-30 11:03:01
updated_at: 2026-06-30 11:03:01
recorded_by: product
source: 反馈
priority_hint: P1
parent_requirement: REQ-0005-user-management
captured_via: capture
classification_rationale: 超级管理员编辑与密码重置保护属于用户管理权限策略扩展，尚需形成新行为约束。
---

# 一句话

管理端必须保护 `.env` 中配置的超级管理员账号（`ADMIN_USERNAME`，默认 `admin`）：任何用户均不允许编辑该账号，也不允许重置或修改该账号密码。

# 原始描述

`.env` 文件里面会配置一个超级管理员【`ADMIN_USERNAME`，默认是 `admin`】，任何用户均不允许对该用户进行编辑操作，也不允许重置和修改密码。

# 背景与关联

- 父需求：`REQ-0005-user-management`
- 涉及环境变量：`ADMIN_USERNAME`（默认 `admin`）
- 涉及能力：管理端用户编辑、重置密码、修改密码、用户列表操作可用性与后端权限校验
- 安全目标：超级管理员账号作为系统保底账号，不应被任何管理端用户误改、禁用或重置密码

# 待澄清

- [ ] “任何用户”是否包含超级管理员本人；若包含，超级管理员本人也不能通过个人资料/修改密码入口修改自身密码
- [ ] 对超级管理员账号的冻结、停用、删除操作是否也需要一并禁止
- [ ] 前端应隐藏操作按钮、置灰按钮并提示原因，还是允许点击后由后端返回明确错误
- [ ] 后端错误码与错误文案是否需要新增统一错误码

# 探索结论

（/req-explore 后人工确认写入）

# 分类说明（/capture）

该条目描述的是新的权限保护策略和系统行为约束，不是既有功能的单点异常，因此判定为 REQ。
