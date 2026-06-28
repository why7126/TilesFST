---
bug_id: BUG-0017-user-reset-password-confirm-ui-inconsistency
status: pending_review
created_at: 2026-06-27 13:29:34
updated_at: 2026-06-27 13:29:34
root_cause_type: code/design/frontend-ui
---

# 根因分析

## 1. 分类

| 项 | 值 |
|---|---|
| 缺陷类型 | **code / design / frontend-ui**（管理端重置密码确认 UI 未对齐 DS confirm modal） |
| 引入阶段 | 用户管理初版 `add-user-management`；`fix-admin-list-status-action-confirm` 有意保留 `window.confirm` |
| 责任模块 | `UserManagementPage.tsx`（`handleResetPassword`） |
| 关联后端 | 无缺陷；`POST .../reset-password` 与 `ResetPasswordDialog` 结果弹窗正常 |

## 2. 直接原因

### 2.1 重置密码确认仍使用 `window.confirm`

`UserManagementPage.tsx` 中 `handleResetPassword` 在 API 调用前执行浏览器原生确认：

```tsx
const handleResetPassword = async (user: UserAdminItem) => {
  if (!window.confirm(`确认为用户 ${user.username} 重置密码？`)) return;
  try {
    const password = await resetUserPassword(user.id);
    setResetPassword(password);
    setNotice('密码已重置');
  } catch (err) {
    setNotice(getErrorMessage(err, '重置密码失败'));
  }
};
```

未设置 `resetPasswordConfirmTarget`（或等价 state），也未渲染与同页 `statusConfirmTarget` / `deleteTarget` 一致的 confirm modal。

### 2.2 同页其他操作已 modal 化，重置密码路径未迁移

BUG-0016 / `fix-admin-list-status-action-confirm` 为冻结/解冻/删除增加了 inline DS modal，但 change scope **显式排除**重置密码 confirm UI（归 BUG-0017）。修复后同页操作列内并存两套确认形态，视觉分裂加剧。

### 2.3 测试未覆盖重置密码 confirm 路径

`UserManagementPage.test.tsx` 覆盖冻结/删除 modal（含「删除 MUST NOT 调用 `window.confirm`」），但**无**重置密码用例；`resetUserPassword` 虽被 mock，确认交互未被门禁约束。

## 3. 根本原因

### 3.1 确认 UI 统一为「按操作专项交付」，重置密码被延后

管理端 confirm modal 模式在品牌（REQ-0008）、类目（REQ-0007）、用户冻结/删除（BUG-0016）中分 change 落地，**无**横切「所有危险操作 MUST DS modal」的共享组件或 CI 检查。`add-user-management` 初版采用 `window.confirm` 作为低成本确认；后续专项未纳入重置密码，形成遗留。

### 3.2 OpenSpec / 父需求对 confirm 形态粒度不足

- REQ-0005 `acceptance.md` AC-021 要求「重置前弹出确认」，**未**规定 MUST NOT 使用 `window.confirm` 或 MUST 复用 `modal-backdrop` 结构。
- `openspec/specs/web-client/spec.md` 用户冻结/解冻/删除 requirement 将重置密码 confirm **单独标注**为 BUG-0017，形成文档上已知但未修复的缺口。

### 3.3 结果弹窗与确认弹窗职责分离，易误判「已统一」

`ResetPasswordDialog`（展示随机密码）已是 DS modal，与 BUG-0017 无关。开发者或验收方可能仅验证「重置后有弹窗」，未区分**重置前确认**与**重置后展示**两阶段 UI。

## 4. 触发条件

满足以下条件即可 **100%** 稳定复现：

1. `admin` 登录 Web 管理端（local 或 Docker）；
2. 进入 `/admin/users`；
3. 对任意非 `deleted` 用户点击「重置密码」；
4. 出现浏览器原生 `window.confirm`，而非页面内 `role="dialog"` modal。

**对照（Golden Reference）**：`/admin/tile-categories` 启停确认使用 DS modal（`TileCategoryManagementPage.tsx` L423–466）。

## 5. 非根因（排除）

| 假设 | 结论 |
|---|---|
| API 或权限错误 | 否；确认后 API 与结果弹窗正常 |
| modal CSS 未加载 | 否；重置前路径未渲染 confirm modal JSX |
| `ResetPasswordDialog` 缺陷 | 否；结果弹窗已 DS modal，非本 BUG |
| BUG-0016 回退 | 否；冻结/删除 modal 仍正常 |
| 后端缺少 confirm | 否；纯前端 confirm 形态问题 |

## 6. 分类结论

| 维度 | 结论 |
|---|---|
| 缺陷分类 | code / design / frontend-ui |
| 是否接口缺陷 | 否 |
| 是否数据库缺陷 | 否 |
| 是否权限缺陷 | 否 |
| 是否 Design System 缺陷 | 是，confirm Dialog 未横向对齐 |
| 主要修复面 | `UserManagementPage` 重置前 confirm modal；Vitest；OpenSpec delta |

## 7. 修复建议（供 bug-opsx）

1. 新增 `resetPasswordConfirmTarget`；按钮 `onClick` → 打开 modal，确认后调用 `resetUserPassword`。
2. Modal 结构对齐 `statusConfirmTarget` 与 `TileCategoryManagementPage` 启停确认。
3. 文案：标题「重置密码」；正文含用户名与「将生成新随机密码」后果说明；按钮「取消」/「确认重置」。
4. Vitest：确认前 `resetUserPassword` mock MUST NOT 调用；取消后不调用；确认后调用并触发结果弹窗 state。
5. OpenSpec change：`fix-user-reset-password-confirm-ui`；MODIFIED `web-client` 重置密码确认 requirement。
