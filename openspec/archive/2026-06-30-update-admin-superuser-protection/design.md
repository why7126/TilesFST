---
change_id: update-admin-superuser-protection
title: 管理端超级管理员账号保护设计
created_at: 2026-06-30 18:26:13
updated_at: 2026-06-30 18:26:13
source_requirement: REQ-0019-admin-superuser-protection
status: proposed
---

## Context

REQ-0019 是 `REQ-0005-user-management` 的 refinement，并关联 `REQ-0015-password-change`。项目已有 `ADMIN_USERNAME`、`ADMIN_INITIAL_PASSWORD`、`ADMIN_RESET_PASSWORD_ON_STARTUP` 等运维级默认管理员配置。现有角色模型只有 `admin` / `employee` / `store_owner`，评审结论明确不新增 `super_admin` 或 `root`。

该 change 影响后端保护边界、API 响应字段、管理端用户列表 UI、个人改密流程、错误码治理和测试。实现阶段不得绕过 OpenSpec；本阶段不写 `src/`。

## Goals / Non-Goals

**Goals:**

- 以 `settings.admin_username` 作为唯一事实源识别受保护账号。
- 在后端强制拒绝会破坏保底管理员账号的管理端操作。
- 将受保护状态暴露给前端，前端只消费 `is_protected` / `protected_reason`，不硬编码 `admin`。
- 默认禁止受保护账号本人通过管理端个人改密入口修改密码。
- 保留 `.env` 级运维恢复能力和既有角色模型。
- 补齐 API、Orval、错误码、pytest、Vitest 和管理端列表横切验收。

**Non-Goals:**

- 不新增角色枚举、权限组、完整 RBAC 或多超级管理员管理。
- 不改变店主 Web 展示端或微信小程序。
- 不修改数据库表结构。
- 不移除 `ADMIN_RESET_PASSWORD_ON_STARTUP` 等部署恢复机制。
- 不新增独立用户管理页面或重做用户管理视觉。

## Decisions

### D1. UI 策略：CSS Port 增量

采用 CSS Port 增量策略：继续复用 `UserManagementPage` 与 `user-management.css`，只增加受保护行状态、按钮禁用和原因提示。优先级：

1. `REQ-0005` 用户管理页面既有实现与 PNG Golden。
2. `issues/requirements/archive/REQ-0019-admin-superuser-protection/prototype/web/admin-superuser-protection.html` 的受保护行增量状态。
3. `prototype/web/admin-superuser-protection-context.md`。
4. `issues/.../acceptance.md`。
5. `docs/knowledge-base/best-practices/admin-list-page-consistency.md`。
6. `rules/ui-design.md`。
7. `openspec/specs/` 已归档能力。

理由：REQ-0019 只改变用户管理列表中的操作态，不需要新增模板或页面。这样可降低 Sprint 002/003 反复出现的列表分页、toast、confirm 回归风险。

### D2. 后端保护：服务层统一判定

后端应提供单一 helper / service 方法判断受保护账号：

```text
normalized(user.username) == normalized(settings.admin_username or "admin")
```

比较前必须对配置值 `strip()`，并遵循现有用户名大小写规范。所有用户列表、详情和破坏性操作共用该判定，避免多处写死字符串。

### D3. API 字段：后端返回保护标识

用户列表和详情的用户对象必须新增：

```json
{
  "is_protected": true,
  "protected_reason": "系统保底管理员账号不允许执行该操作"
}
```

普通用户返回 `is_protected=false`，`protected_reason=null`。前端不得从 username 或 role 推导保护状态。

### D4. 错误码：新增稳定业务错误

建议新增业务错误码 `30060`，HTTP 403，语义为“受保护系统账号不可操作”。最终实现必须同时登记到 `src/backend/app/core/error_codes.py` 和 `docs/standards/error-codes.md`。错误响应仍为统一 `{ code, message, data }`。

### D5. 本人改密默认拒绝

评审确认默认禁止受保护账号本人通过 `POST /api/v1/admin/profile/password` 改密。拒绝发生在更新 `password_hash` 和递增 `token_version` 前。`.env` 级启动恢复能力不属于管理端用户操作，必须保留。

## Conflict Resolution

| 来源 | 结论 |
|---|---|
| HTML prototype | 只表达受保护账号行置灰、保护徽章或原因提示；不覆盖 REQ-0005 页面整体布局 |
| PNG | 当前未导出，trace 已标记为非阻塞；实现阶段可补导出，但不得阻塞 change 创建 |
| context.md | 明确复用 `UserManagementPage` 与 `user-management.css`，不得硬编码 `admin` |
| acceptance.md | 后端强制保护优先于前端置灰；前端普通用户流程不回归 |
| admin-list best-practice | 分页 DOM、fixed toast、DS confirm modal 保持不变；禁止 `window.confirm` |
| ui-design.md | 不新增裸 Hex；样式复用既有 semantic token / CSS variables |

无冲突需要 REMOVED；本 change 使用 MODIFIED delta 扩展既有 requirement。

## Risks / Trade-offs

| 风险 | 缓解 |
|---|---|
| 只做前端置灰，API 仍可绕过 | 后端 service/router 对编辑、重置、状态变更、本人改密全部强制拒绝 |
| 前端硬编码 `admin` 与部署配置不一致 | 只消费 `is_protected` / `protected_reason`；测试断言不出现 username hard-code 判断 |
| 新增角色导致 RBAC 范围扩大 | 明确不新增角色，仍使用 `admin` 角色 + 账号保护标识 |
| 受保护账号本人改密策略有争议 | 采用评审默认拒绝；后续如改变策略需新评审或 update change |
| 列表 UI 改动引发分页/confirm/toast 回归 | 引用 admin-list best-practice，Vitest 覆盖置灰、普通用户 confirm 和分页 DOM |

## Migration Plan

1. `/opsx-apply update-admin-superuser-protection` 实现后端字段、保护拦截和错误码。
2. 重新导出 OpenAPI 并执行 Orval。
3. 更新管理端用户列表和改密弹窗错误展示。
4. 补充 pytest 与 Vitest。
5. 运行 OpenSpec validate、API governance 验证、相关后端/前端测试。
6. 验收通过后 `/opsx-archive update-admin-superuser-protection`。

## Open Questions

- 错误码最终数值建议为 `30060`，实现阶段可按 `docs/standards/error-codes.md` 当前分段确认。
- PNG Golden 可在实现验收阶段补导出；不是 req-opsx 创建 change 的阻塞项。
