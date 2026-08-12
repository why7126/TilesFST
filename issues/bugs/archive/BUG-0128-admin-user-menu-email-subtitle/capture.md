---
bug_id: BUG-0128-admin-user-menu-email-subtitle
status: done
created_at: 2026-08-11 21:43:22
updated_at: 2026-08-11 23:22:58
severity_hint: low
environment: local
related_requirement:
related_bug:
lifecycle_stage: plan
---

# 现象

管理后台用户菜单栏在用户资料未设置邮箱时仍显示邮箱样式的副标题，例如由用户名拼接出的 `username@tilesfst.com`。用户期望菜单栏只显示用户昵称；如果昵称为空，则显示用户名，不需要副标题。

# 复现步骤

1. 使用后台管理员或运营账号登录管理后台。
2. 确认当前用户资料中的邮箱为空。
3. 查看左侧侧边栏底部用户菜单触发区。
4. 观察用户名称下方是否仍显示邮箱样式副标题。

# 期望 vs 实际

- 期望：用户菜单栏只显示用户昵称；当昵称为空时显示用户名；不展示邮箱、伪邮箱或任何副标题。
- 实际：用户菜单栏在邮箱为空时仍通过前端兜底显示 `username@tilesfst.com` 形式的副标题，容易让用户误以为资料中存在真实邮箱。

# 影响范围

- 管理后台侧边栏用户菜单触发区。
- 用户资料为空邮箱场景下的身份展示一致性。
- 前端用户展示工具函数与相关组件测试预期。

# 初步线索

- `/explore` 只读排查确认，后端 `ProfileMe.email` 为可空字段，服务层原样返回 `user.email`。
- 前端 `AdminUserMenu` 使用 `getUserEmail(user?.username, profileEmail)` 生成菜单副标题。
- `getUserEmail()` 在邮箱为空时会拼接 `${username}@tilesfst.com`，导致出现伪邮箱。
- 当前问题可以通过调整菜单栏展示策略闭环，不涉及后端数据模型变更。

# 建议验收或复现要点

- [ ] 用户资料 `display_name` 非空时，用户菜单栏仅显示昵称，不显示副标题。
- [ ] 用户资料 `display_name` 为空且 `username` 非空时，用户菜单栏仅显示用户名，不显示副标题。
- [ ] 用户资料 `email` 非空时，用户菜单栏仍不显示邮箱副标题。
- [ ] 不再出现 `username@tilesfst.com` 或 `admin@tilesfst.com` 形式的前端伪邮箱。
- [ ] 更新或补充 `AdminUserMenu` / `user-display` 相关前端测试。

# 附件

- 暂无。
