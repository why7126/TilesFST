---
change_id: update-admin-theme-user-menu-modes
status: archived
type: update
created_at: 2026-08-11 09:06:12
updated_at: 2026-08-11 09:26:44
source_requirement: REQ-0109-admin-theme-user-menu-modes
source_sprint: sprint-022
knowledge_base_refs: []
ui_contract:
  required: true
  source: issues/requirements/archive/REQ-0109-admin-theme-user-menu-modes/prototype/web/context.md
---

# Trace

## 变更记录

| 时间 | 事件 | 说明 |
|---|---|---|
| 2026-08-11 09:06:12 | req.opsx | 基于 REQ-0109 创建 OpenSpec Change。 |
| 2026-08-11 09:19:40 | opsx.apply | 实现管理后台主题入口迁移、两模式收敛、历史值归一、OpenAPI/Orval 生成与测试验证。 |
| 2026-08-11 09:26:44 | opsx.modify | 按验收参照图返修用户菜单：每个菜单项提供独立图标，主题行调整为左图标 + 「界面主题」文字 + 右侧 switch。 |

## UI 证据计划

- Skeleton：用户菜单展开层新增主题按钮，侧边栏独立主题选择器移除。
- 截图：1440px 管理端用户菜单展开层、暗色旗舰状态、跟随系统浅色解析状态。
- 交互：鼠标点击、键盘触发、侧边栏收起态、同步失败 toast 或等价反馈。
- 样式：主题按钮和菜单状态不得新增裸 Hex，computed style 应来自 semantic/admin token。

## UI 证据

- 1440px 等价 UI 证据：`AdminLayout.test.tsx` 覆盖管理端 Shell 渲染时侧边栏不再出现独立「界面主题」选择器，用户菜单展开后出现无文案主题按钮，且按钮 class 为 `theme-toggle`。
- 暗色旗舰状态：`AdminLayout.test.tsx`、`AdminUserMenu.test.tsx` 与 `ThemeContext.test.tsx` 覆盖点击用户菜单主题按钮或主题控件后 `data-theme-mode="dark_flagship"`、`data-theme="dark"`、本地存储写入 `dark_flagship`。
- 跟随系统浅色解析状态：`ThemeContext.test.tsx` 覆盖历史 `light` 归一为 `system`，`resolveThemeMode` 保留 `system` 下依据 `prefers-color-scheme` 解析浅/暗色；`ThemeSwitcher` 用户可选项仅剩 `system` / `dark_flagship`。
- 同步失败反馈：`AdminLayout.test.tsx` 与 `ThemeContext.test.tsx` 覆盖账号主题偏好同步失败时本地主题保持生效，并展示可自动消退的管理端 toast。
- 样式证据：`rg -n "#[0-9a-fA-F]{3,8}" src/web/src/features/admin/styles/admin-home.css src/web/src/features/admin/components/AdminUserMenu.tsx src/web/src/features/admin/components/AdminSidebar.tsx src/web/src/features/theme/theme.ts` 无命中，主题按钮使用 `var(--admin-gold)` 等语义/admin token。

## 验证记录

- `pnpm --dir src/web exec vitest run src/features/theme/ThemeContext.test.tsx src/features/admin/components/AdminUserMenu.test.tsx src/features/admin/components/AdminLayout.test.tsx src/features/auth/components/LoginPage.test.tsx src/pages/dev/DesignSystemPage.test.tsx`：5 个文件、26 个用例通过。
- `uv run pytest tests/integration/api/test_auth_theme_preference.py`：6 个用例通过。
- `scripts/generate-openapi-client.sh`：OpenAPI 与 Orval 生成成功，生成类型仅暴露 `system` / `dark_flagship`。
- `openspec validate update-admin-theme-user-menu-modes --strict`：通过。
- `python scripts/validate-openspec-language.py`：通过。

## 验收返修证据

- 反馈：用户菜单栏的界面主题样式需参照图，且每个菜单都要有独立合适的图标。
- 调整：`AdminUserMenu.tsx` 使用 `UserRound`、`KeyRound`、`SunMoon`、`LogOut` 分别对应个人资料、密码修改、界面主题、退出登录；主题项保留可访问名称「切换到暗色旗舰 / 切换到跟随系统」，可见结构为左侧主题图标、文字「界面主题」、右侧 switch 样式按钮。
- 视觉/交互等价证据：`AdminUserMenu.test.tsx` 与 `AdminLayout.test.tsx` 覆盖四个菜单项均含 `svg` 图标、主题项含 `.theme-switch-track`、可见「界面主题」、不显示「暗色旗舰」模式文案，并保持点击切换到 `dark_flagship`。
- 样式证据：主题 switch 使用 `var(--admin-gold-bg)`、`var(--admin-gold-border)`、`var(--admin-gold)`、`var(--admin-sidebar-bg)` 等既有 admin token；未新增 API、DB、权限、Docker、MinIO 或小程序行为。
