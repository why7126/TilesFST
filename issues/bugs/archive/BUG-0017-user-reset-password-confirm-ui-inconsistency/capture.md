---
bug_id: BUG-0017-user-reset-password-confirm-ui-inconsistency
status: captured
created_at: 2026-06-27 12:03:34
updated_at: 2026-06-27 12:03:34
severity_hint: medium
environment: local|docker
related_requirement: REQ-0005-user-management
related_bug: BUG-0016-admin-list-status-action-confirm-missing
captured_via: capture
classification_rationale: 用户列表「重置密码」已有二次确认，但弹窗 UI/UE 与类目启用/停用确认弹窗不一致；属管理端确认 Dialog 视觉/交互规范偏差，与 BUG-0016（缺确认）为不同修复面，故独立追踪。
---

# 现象

用户管理列表页「重置密码」操作的二次确认弹窗，在布局、按钮样式、文案结构、标题区 Typography 等方面，与瓷砖类目列表「启用/停用」二次确认弹窗的 UI/UE 设计方案不一致，破坏管理端确认 Dialog 统一性。

# 复现步骤

1. 以 admin 登录管理端。
2. 进入「用户管理」列表页，对某用户点击「重置密码」。
3. 观察弹出的二次确认弹窗（标题、描述、主/次按钮、间距、圆角等）。
4. 进入「瓷砖类目」列表页，对某停用类目点击「启用」（或对已启用类目点击「停用」）。
5. 观察二次确认弹窗样式。
6. 并排对比两弹窗的 UI/UE 是否一致。

# 期望 vs 实际

| | 说明 |
|---|---|
| **期望** | 重置密码确认弹窗 MUST 与类目启用/停用确认弹窗采用同一 Confirm Dialog 组件与 Design System 规范（标题区、按钮层级、间距、semantic token）。 |
| **实际** | 两弹窗视觉与交互形态明显不一致。 |

# 附件

- 暂无截图。
