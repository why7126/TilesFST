---
bug_id: BUG-0026-change-password-cancel-confirm-redundant
status: pending_review
created_at: 2026-06-28 13:06:10
updated_at: 2026-06-28 13:06:10
root_cause_type: code
---

# 根因分析

## 1. 直接原因

### 1.1 `requestClose` 对 dirty 表单调用 `window.confirm`

`ChangePasswordModal.tsx` L101 定义 `isDirty`：任一密码字段非空即为 true。

L103–108 的 `requestClose` 在 `isDirty` 时调用浏览器原生确认框：

```tsx
const requestClose = useCallback(() => {
  if (isDirty && !window.confirm('当前填写内容尚未保存，确认关闭吗？')) {
    return;
  }
  onClose();
}, [isDirty, onClose]);
```

### 1.2 所有关闭入口共用 `requestClose`

以下路径均触发上述逻辑（有输入时必弹 confirm）：

| 入口 | 绑定 |
|---|---|
| footer「取消」 | L226 `onClick={requestClose}` |
| 右上角 × | L172 |
| Esc | L114–117 `keydown` 监听 |
| 遮罩点击 | L157 `onClick={requestClose}` |

### 1.3 测试固化当前行为

`ChangePasswordModal.test.tsx` L62–70 用例 `confirms before closing when form is dirty` 断言 `window.confirm` **必须**被调用，与产品期望相反，缺陷未在 CI 中被视为失败。

## 2. 根本原因

### 2.1 REQ-0015 交付时按规格实现脏关闭 guard

REQ-0015 `FR-003`、`acceptance.md` AC-007 与 `openspec/specs/admin-password-change`「关闭与脏确认」Scenario 明确要求：表单有输入时关闭前 MUST 二次确认。`add-admin-password-change` change 提案亦列出「脏关闭二次确认」。实现与归档 spec **一致**，属按规格交付，非实现疏漏。

### 2.2 与管理端弹窗 UX 模式不一致

同项目 `BrandFormModal`、`UserFormModal`、`TileSkuFormModal` 均直接 `onClose()`，无 dirty guard。改密弹窗为全项目 **唯一** 使用 `window.confirm` 的位置；危险操作（如删除用户）已采用应用内 Confirm Modal 而非原生对话框。REQ-0015 的脏关闭 guard 与既有管理端表单模式冲突，造成 UX 不一致。

### 2.3 改密场景无「未保存草稿」语义

密码弹窗数据仅存于组件内存，未提交不落库；关闭后 `useEffect`（L80–90）在 `open` 时 reset。用户点击「取消」已是明确放弃意图，二次 confirm 无实质数据保护价值，仅增加交互步骤。

### 2.4 非回归：自 REQ-0015 交付起即存在

行为自 `ChangePasswordModal` 引入即存在，非近期变更回归。

## 3. 触发条件

满足以下条件时可 **100% 稳定复现**：

1. 以 `admin` 或 `employee` 登录 Web 管理端。
2. 打开「修改密码」弹窗（侧栏菜单或 REQ-0014 个人资料页入口）。
3. 在「原密码」「新密码」或「确认新密码」任一字段输入至少一个字符。
4. 点击「取消」、×、Esc 或遮罩。

**不触发 confirm 的路径：** 三字段均为空时关闭 → 直接 `onClose()`（L104 条件不满足）。

## 4. 分类结论

| 维度 | 结论 |
|---|---|
| 缺陷分类 | code / frontend-ux（含 design/spec 对齐） |
| 是否接口缺陷 | 否 |
| 是否数据库缺陷 | 否 |
| 是否权限缺陷 | 否 |
| 是否回归 | 否 |
| 主要修复面 | `ChangePasswordModal.tsx`、`ChangePasswordModal.test.tsx`；OpenSpec delta MODIFIED REQ-0015 脏关闭 Scenario |
| 关联 BUG | BUG-0024、BUG-0025（同弹窗，可合并 change） |
| 建议 Change | `fix-change-password-modal-errors`（与 BUG-0024/0025 合并编排） |

## 5. 后续修复建议

1. 删除 `isDirty` 与 `window.confirm`；`requestClose` 直接调用 `onClose()`。
2. 更新 Vitest：dirty 表单点击「取消」/ × **MUST NOT** 调用 `window.confirm`；`onClose` **MUST** 被调用。
3. OpenSpec fix change delta **MODIFIED** `admin-password-change`「关闭与脏确认」Scenario；同步 REQ-0015 AC-007、AC-040 文案。
4. 保留 `open` 时 reset 逻辑，确保再次打开表单为空。
5. 与 BUG-0024/0025 合并为同一 `fix-change-password-modal-errors` change，tasks 中分列 scope。
