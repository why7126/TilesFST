---
bug_id: BUG-0074-prod-theme-preference-sync-toast-persistent
status: done
created_at: 2026-07-21 15:01:54
updated_at: 2026-07-22 08:56:27
classification: code/ux/production-config
related_requirement:
related_change: fix-theme-preference-sync-toast-persistent
---

# Root Cause - BUG-0074 生产环境主题偏好同步失败提示持续不消失

## 直接原因

当前缺陷由两个可分层处理的问题组成：

1. 账号偏好同步失败后，前端会展示“主题已在本机生效，但账号偏好同步失败，请稍后重试”。
2. 管理端 Toast 展示状态没有自动清除机制，导致该错误提示写入 `toast` state 后持续存在。

已从代码路径定位到常驻提示的直接原因：

- `ThemeContext` 在主题偏好同步失败时设置错误文案，并保留本机主题生效。
- `AdminLayout` 监听到 `themeError` 后执行 `setToast(themeError)`，随后清空 ThemeContext error。
- `AdminLayout` 仅对 `notice` 设置了 3200ms 自动清除计时器，没有对 `toast` 设置同等生命周期。
- `AdminToast` 是纯展示组件，不负责自动关闭或手动关闭。

因此，一旦生产环境触发主题偏好同步失败，Toast 消息会一直保留在 `AdminLayout` 的本地状态中，直到页面刷新、布局卸载或其他逻辑显式覆盖该状态。

## 根本原因

根本原因是主题错误提示复用了全局管理端 Toast 展示能力，但 Toast 生命周期没有统一治理：

- 管理端存在多处 `AdminToast` 使用场景，但组件本身没有统一的 `duration`、`onClose` 或自动销毁策略。
- `AdminLayout` 中普通占位提示 `notice` 有自动消失逻辑，而主题同步错误转入 `toast` 后没有对应清理逻辑。
- 现有主题切换测试覆盖了“同步失败时本机主题仍生效并展示错误文案”，但没有覆盖错误提示自动消失或可关闭。
- 生产同步失败的接口原因缺少现场证据，导致错误提示路径被触发后没有足够诊断信息帮助用户或运维定位。

## 触发条件

满足以下条件时可触发：

1. 用户已登录生产环境 Web 管理端。
2. 用户切换界面主题。
3. 前端调用 `PATCH /api/v1/auth/me/theme` 保存账号主题偏好。
4. 该请求失败、返回非成功响应，或响应 envelope 缺少 `data`。
5. `ThemeContext` 设置同步失败文案，`AdminLayout` 将该文案写入 `toast` state。
6. 页面没有后续逻辑清空该 `toast` state。

## 生产同步失败待确认原因

账号偏好同步失败本身仍需生产证据确认，优先排查：

| 方向 | 说明 |
|---|---|
| 鉴权 | 请求是否携带有效 Authorization Header，是否返回 401 / 403 |
| 路由 | 生产后端是否部署 `PATCH /api/v1/auth/me/theme`，Nginx `/api/` 反代是否正确 |
| 数据库 | 生产 `users` 表是否已包含 `theme_mode` 字段，迁移是否执行成功 |
| 响应契约 | 响应是否符合 `ApiResponse<UserProfile>` envelope，`data.theme_mode` 是否存在 |
| 服务异常 | 后端是否记录 500、数据库写入失败或用户记录读取失败 |

## 分类

| 分类 | 判断 |
|---|---|
| code | 是。`AdminLayout` 的 `toast` 状态缺少自动清除或关闭控制 |
| ux | 是。错误提示常驻会干扰用户继续操作并造成异常持续存在的感知 |
| production-config | 可能。账号偏好同步失败可能来自生产部署、鉴权、反代或数据库迁移差异 |
| api | 可能。若生产接口缺失、响应 envelope 异常或错误码不符合契约，需要同步 API 侧修复 |
| db | 可能。若生产缺少 `users.theme_mode` 字段或迁移未生效，需要同步数据库修复 |
| security | 否。当前缺陷不要求放宽认证或权限；排查鉴权失败时不得绕过安全校验 |

## 影响判断

该问题发生在生产环境 Web 管理端，影响主题偏好保存与错误反馈体验。它不阻断本机主题切换，也不直接阻断核心管理功能；但常驻错误提示会持续污染管理端反馈区，账号偏好保存失败还可能导致刷新、重新登录或跨设备访问时主题不一致。

修复时应同时覆盖：

- Toast 生命周期：错误提示可自动消失或可关闭。
- 同步失败诊断：能从 Network/日志明确失败状态和错误码。
- 偏好保存链路：生产 `PATCH /api/v1/auth/me/theme` 成功写入并返回用户主题偏好。
