---
bug_id: BUG-0041-sidebar-user-menu-avatar-missing
status: pending_review
created_at: 2026-06-28 18:05:06
updated_at: 2026-06-28 18:05:06
---

# 临时规避方案

## 1. 可用性规避

该缺陷不阻断登录、导航、个人资料编辑或头像上传，当前可继续使用：

1. **以 Profile 页查看头像**：侧栏「个人资料」→ `/admin/profile`，身份条可正常展示与更换头像。
2. **以用户列表确认头像**（admin）：「用户管理」列表第一列已支持 `avatar_url` 图片回显。
3. **识别侧栏 initials**：侧栏仍显示昵称、邮箱与首字母占位，可用于确认当前登录账号。

## 2. 操作规避

若需在侧栏区域「看到」最新头像，可临时：

1. 上传/更换头像后 **硬刷新页面**（F5 / Cmd+R），使 `AdminLayout` 重新 mount 并 refetch profile（修复前仍只显示 initials，**不能**真正看到图片）。
2. 无其他有效操作可令侧栏显示头像图片——规避**不能**达成期望 UX，仅保证功能链路可用。

> 说明：因渲染层根本未实现 `<img>`，即使硬刷新也无法在侧栏看到头像；唯一可靠阅读区为 Profile 页与用户列表。

## 3. 风险说明

上述规避只能保证：

- 头像上传、持久化、Profile 展示正常。
- 侧栏菜单（个人资料、密码修改、退出）可用。

**不能**消除：

- 侧栏与 Profile/列表的头像展示不一致。
- 用户无法在全局 shell 识别本人头像。
- 上传后侧栏无视觉反馈（始终 initials）。

仍建议进入 `/bug-review BUG-0041 --approve`，通过 `fix-sidebar-user-menu-avatar` OpenSpec Change 正式修复。
