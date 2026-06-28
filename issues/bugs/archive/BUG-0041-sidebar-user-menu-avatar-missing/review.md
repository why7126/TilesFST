---
bug_id: BUG-0041-sidebar-user-menu-avatar-missing
review_id: REV-BUG-0041-001
status: approved
reviewed_at: 2026-06-28 18:35:30
reviewer: ai-agent
decision: approve
severity: medium
hotfix_required: false
---

# 缺陷评审

## 1. 评审结论

`BUG-0041-sidebar-user-menu-avatar-missing` 评审通过，状态变更为 `approved`。

该缺陷应进入修复流程，后续可执行：

```text
/bug-opsx BUG-0041-sidebar-user-menu-avatar-missing
```

建议修复 Change：

```text
fix-sidebar-user-menu-avatar
```

## 2. 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | 100% 稳定复现；`root-cause.md` 已明确渲染层（仅 initials）与数据层（Layout 未传 `avatar_url`）双重缺口，并排除 API/MinIO 问题。 |
| 严重等级合理 | 通过 | `medium` 合理；不阻断登录/导航/Profile 上传，属 REQ-0014 交付后侧栏 UX 一致性缺陷。 |
| 回归验收明确 | 通过 | `acceptance.md` AC-001～AC-011 覆盖 avatar 展示、fallback、Profile 上传后即时刷新、collapsed、纯前端范围、vitest、tablet 回归。 |
| 是否需 hotfix 路径 | 不需要 | 非阻断；纯前端 `AdminLayout` + `AdminUserMenu` + CSS，无 API/DB 变更。 |

## 3. 批准理由

1. Profile 页与用户列表已支持 `avatar_url` 回显，侧栏仍为 initials，用户预期侧栏同步展示本人头像。
2. 修复路径清晰：复用现有 `GET /profile/me`，扩展 Layout profile 预取 plumbing，无需扩展 auth `UserProfile`。
3. 参考实现已存在（`UserManagementPage` img + fallback），实现成本低、风险可控。
4. AC-004 明确要求 Profile 上传后侧栏即时更新，避免「半修复」验收缺口。

## 4. 修复门禁

| 项目 | 结论 |
|---|---|
| 是否允许 `/bug-opsx` | 是 |
| 是否允许进入 Sprint | 是 |
| 建议 Change ID | `fix-sidebar-user-menu-avatar` |
| Change 类型 | `fix-*` |

## 5. 修复范围建议

1. `AdminLayout`：从 `fetchProfileMe()` 缓存 `avatarUrl`，传入 `AdminSidebar` / `AdminUserMenu`。
2. `AdminUserMenu`：`avatarUrl` 存在时渲染 `<img>` + initials fallback；`onError` 回退。
3. `admin-home.css`：补充 `.sidebar-user .avatar img` 样式（34×34px、`object-fit: cover`）。
4. Profile 上传成功 → 触发 Layout refetch 或共享 profile cache（满足 AC-004）。
5. `AdminUserMenu.test.tsx`：新增 avatar 渲染与 fallback 用例。
6. **不**扩展 auth schema；**不**改 ≤1023px 隐藏 `sidebar-user` 行为。

## 6. 后续动作

1. 执行 `/bug-opsx BUG-0041-sidebar-user-menu-avatar-missing`。
2. `/opsx-apply` → 按 AC-001～AC-011 验收 → `/opsx-archive`。
3. 可与 BUG-0021（侧栏 icon）同 Sprint、独立 Change 并行开发。
