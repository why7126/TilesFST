---
bug_id: BUG-0074-prod-theme-preference-sync-toast-persistent
status: done
review_result: approved
reviewed_at: 2026-07-21 15:23:20
reviewer: AI
created_at: 2026-07-21 15:23:20
updated_at: 2026-07-22 08:56:27
related_requirement:
related_change: fix-theme-preference-sync-toast-persistent
---

# Review - BUG-0074 生产环境主题偏好同步失败提示持续不消失

## 评审结论

结论：`approved`，确认需要修复。

该缺陷发生在生产环境 Web 管理端主题切换链路，已具备明确用户反馈、复现路径、初步根因分析、临时规避方案和回归验收标准。问题不阻断本机主题立即生效，但会造成账号偏好同步失败提示常驻，并可能导致刷新、重新登录或跨设备访问时主题偏好不一致。

## 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | 常驻提示路径已从 `ThemeContext`、`AdminLayout`、`AdminToast` 的状态流转定位；生产同步失败原因仍需 Network/日志确认 |
| 严重等级合理 | 通过 | `medium` 合理：不阻断核心业务，但发生在生产环境并影响用户体验与账号偏好一致性 |
| 回归验收明确 | 通过 | acceptance 已覆盖主题本机生效、账号偏好保存、失败提示自动消失、未登录不调用同步接口、异常场景与生产证据 |
| 是否需 hotfix 路径 | 建议常规修复，必要时可小范围热修 | 若生产大量用户受影响，可先热修 Toast 自动消失；同步失败根因需结合生产证据决定是否扩大修复 |

## 修复建议

优先修复前端 Toast 生命周期问题：

1. 为 `AdminLayout` 的 `toast` 增加自动清除机制，或为 `AdminToast` 增加统一 `duration` / `onClose` 能力。
2. 补充主题同步失败提示自动消失或可关闭的前端测试。
3. 保持同步失败时本机主题已生效的既有行为。

同步排查生产保存失败：

1. 收集 `PATCH /api/v1/auth/me/theme` 的生产 Network 状态码、响应体和后端日志。
2. 确认生产后端路由、Nginx `/api/` 反代、Authorization Header、`users.theme_mode` 字段和响应 envelope。
3. 若仅修复前端 Toast 生命周期，不需要 OpenAPI / Orval；若修复涉及接口字段、响应结构或错误码，必须同步 OpenAPI、Orval、接口文档和测试。

## 后续动作

下一步可执行：

```bash
/bug-opsx BUG-0074
```

创建 OpenSpec Change 后，再纳入 Sprint 并进入实现。
