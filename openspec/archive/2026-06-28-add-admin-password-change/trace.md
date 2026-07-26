---
change_id: add-admin-password-change
requirement_id: REQ-0015-password-change
status: archived
created_at: 2026-06-28 10:06:30
updated_at: 2026-06-28 12:52:00
---

# Change Trace — add-admin-password-change

## 关联

| 字段 | 值 |
|---|---|
| REQ | REQ-0015-password-change |
| Sprint | sprint-003 |
| 姊妹 | add-admin-profile-page（共用 modal hook） |

## PNG 并排验收 Checklist

| # | 检查项 | prototype | 实现 | Pass |
|---|---|---|---|---|
| 1 | 520px 居中弹窗 | password-change-modal.png | ChangePasswordModal.tsx | 待手动 |
| 2 | Sidebar 背景可见 | password-change-modal.png | AdminLayout is-modal-open blur | 待手动 |
| 3 | 三字段 + 显隐 | password-change-modal.png | PasswordField toggle | ✓ |
| 4 | 规则提示区 | password-change-modal.png | rule-list | ✓ |
| 5 | Footer 取消/保存 | password-change-modal.png | modal-footer | ✓ |
| 6 | 品牌金主按钮 | password-change-modal.png | btn primary | ✓ |
| 7 | semantic token | — | admin-* CSS vars | ✓ |

## 变更记录

| 日期 | 动作 | 说明 |
|---|---|---|
| 2026-06-28 12:52:00 | `openspec archive -y` | 合并 specs；归档至 `2026-06-28-add-admin-password-change` |
| 2026-06-28 12:45:00 | `/sprint-apply sprint-003` | 后端 API + JWT tv + 前端 Modal 联调完成 |
| 2026-06-28 10:06:30 | `/req-opsx` | 创建 change add-admin-password-change |
