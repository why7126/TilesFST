---
bug_id: BUG-0046-system-settings-reset-confirm-ui-inconsistency
status: captured
created_at: 2026-06-28 17:53:48
updated_at: 2026-06-28 17:53:48
severity_hint: medium
environment: local|docker
related_requirement: REQ-0017-system-settings
related_bug: BUG-0037-tile-spec-status-confirm-ui-inconsistency
captured_via: capture
classification_rationale: 「恢复默认」使用浏览器原生 confirm，与管理端其它二次确认弹窗（AlertDialog）样式不一致
---

# 现象

「系统设置」页点击「恢复默认」时，二次确认使用浏览器原生 `window.confirm` 弹窗，与管理端类目/规格/用户等页面的 Design System 确认弹窗样式不一致。

# 复现步骤

1. 以 `admin` 登录 Web 管理端。
2. 进入「系统设置」任意可编辑 Tab（如 `/admin/settings/basic`）。
3. 点击底部「恢复默认」按钮。
4. 观察确认交互样式，并与瓷砖类目/规格页状态变更确认弹窗对比。

# 期望 vs 实际

| | 说明 |
|---|---|
| **期望** | 使用与管理端一致的 AlertDialog / 确认弹窗组件（标题、正文、取消/确认按钮、DS Token）。 |
| **实际** | 弹出浏览器原生 confirm 对话框，样式与交互与其它管理端页面不一致。 |

# 初步线索

- `SystemSettingsPage.tsx` 约 176 行：`window.confirm('确定恢复该分组为默认配置吗？…')`。
- 同文件 Tab 切换亦使用 `window.confirm`（约 163 行），可能一并纳入修复范围。
- 参考：`BUG-0037`、`BUG-0017` 同类确认弹窗 UI 不一致修复模式。

# 附件

- screenshots/
- logs/
