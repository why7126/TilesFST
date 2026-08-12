---
requirement_id: REQ-0109-admin-theme-user-menu-modes
status: pending_review
created_at: 2026-08-11 08:51:10
updated_at: 2026-08-11 08:51:10
owner: product
source: requirement.md
---

# REQ-0109 原型策略

## 1. 原型类型

本需求为现有管理后台用户菜单的小交互调整，不要求独立 HTML 原型；实现阶段应基于真实 `AdminUserMenu`、`AdminSidebar` 与主题上下文完成 UI Skeleton 和视觉验收。

## 2. UI Contract

| 区域 | 要求 |
|---|---|
| 侧边栏底部 | 移除独立主题选择器，保留用户菜单入口。 |
| 用户菜单展开层 | 增加主题切换按钮，不展示额外开关说明文案。 |
| 主题按钮 | 使用图标和状态样式表达当前模式；`aria-label` / tooltip 表达“切换到暗色旗舰”或“切换到跟随系统”。 |
| 菜单项 | 个人资料、密码修改、退出登录位置和点击行为不回退。 |
| 侧边栏收起态 | 头像入口仍可打开菜单，主题按钮仍可触发。 |

## 3. 视觉验收视口

- 1440px 桌面管理端：用户菜单展开层、主题按钮、当前状态样式。
- 侧边栏收起态桌面：头像菜单展开和主题按钮触发。
- 窄屏管理端：不破坏既有响应式布局。

## 4. Mock / API 边界

- UI Skeleton 可先使用本地主题上下文 mock。
- 实现完成前必须接入真实 `PATCH /api/v1/auth/me/theme` 同步逻辑。
- 主题同步失败态可通过 mock rejected promise 验证 toast 或等价反馈。

## 5. 证据要求

- 截图：至少包含 1440px 用户菜单展开层、暗色旗舰状态、跟随系统浅色解析状态。
- 样式证据：确认主题按钮未新增裸 Hex，computed style 使用 DS/admin token 解析结果。
- 测试证据：前端主题枚举、用户菜单按钮交互、API/Orval 类型同步。

