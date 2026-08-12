---
bug_id: BUG-0128-admin-user-menu-email-subtitle
title: 管理后台身份展示不应显示伪邮箱
severity: low
status: done
owner:
discovered_at: 2026-08-11 21:43:22
environment: local
related_requirement:
related_change: fix-admin-identity-fake-email-display
created_at: 2026-08-11 21:55:07
updated_at: 2026-08-11 23:22:44
lifecycle_stage: review
iteration: sprint-022
---

# 现象

管理后台在用户资料邮箱为空时，仍会在身份展示区域显示由前端拼接出的邮箱样式文本，例如 `username@tilesfst.com` 或 `admin@tilesfst.com`。当前已确认需要纳入同一修复范围的展示点包括：

- 左侧侧边栏底部用户菜单触发区。
- 个人资料页顶部身份栏。

用户菜单栏的目标展示是单行身份：优先显示用户昵称；当用户昵称为空时显示用户名；不需要邮箱副标题。个人资料页顶部身份栏不应展示由用户名拼接出的伪邮箱，避免让用户误以为资料中存在真实邮箱。

# 复现步骤

1. 使用后台管理员或运营账号登录管理后台。
2. 确认当前账号资料中的邮箱为空。
3. 查看左侧侧边栏底部用户菜单触发区。
4. 进入“个人资料”页面，查看顶部头像旁的身份信息区域。
5. 观察是否出现 `username@tilesfst.com`、`admin@tilesfst.com` 或其他前端拼接的邮箱样式文本。

# 期望 vs 实际

## 期望

- 用户菜单栏只显示用户昵称。
- 当用户昵称为空时，用户菜单栏显示用户名。
- 用户菜单栏不显示邮箱、伪邮箱或任何副标题。
- 个人资料页顶部身份栏不展示前端拼接的伪邮箱；邮箱为空时应省略邮箱片段或使用非误导性展示。
- 真实邮箱字段为空时，界面不应暗示系统已有真实邮箱。

## 实际

- 用户菜单栏通过前端兜底逻辑生成 `username@tilesfst.com` 或 `admin@tilesfst.com`。
- 个人资料页顶部身份栏在邮箱为空时也会拼接 `${username}@tilesfst.com`。
- 当前前端测试中存在伪邮箱兜底断言，旧预期会阻止修复落地。

# 影响范围

- 管理后台侧边栏用户菜单触发区。
- 管理后台个人资料页顶部身份栏。
- 前端用户展示工具函数与相关组件测试。
- 不涉及后端 API、数据库、小程序或对象存储。

# 严重等级说明

严重等级为 `low`。该问题不阻断登录、权限、资料维护或核心业务操作，但会造成用户资料语义误导：邮箱为空时界面显示伪邮箱，降低用户对个人资料真实性的信任。修复范围集中在 Web 前端展示逻辑和测试预期，适合按常规修复流程处理。

# 初步定位

- 后端个人资料响应中的 `email` 字段可为空，服务层原样返回 `user.email`，不会生成默认邮箱。
- `AdminUserMenu` 当前通过 `getUserEmail(user?.username, profileEmail)` 生成菜单副标题。
- `getUserEmail()` 在邮箱为空时返回 `${username}@tilesfst.com`，无用户名时返回 `admin@tilesfst.com`。
- `ProfilePage` 顶部身份栏当前使用 `profile.email?.trim() || `${profile.username}@tilesfst.com``，同样会生成伪邮箱。
- 修复时应同步调整相关测试，确保不再锁定伪邮箱兜底行为。
