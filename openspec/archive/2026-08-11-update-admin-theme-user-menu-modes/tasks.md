## 1. 后端主题偏好 API

- [x] 1.1 收敛主题偏好 schema / enum，使 `UserProfile.theme_mode` 与 `PATCH /api/v1/auth/me/theme` 返回值只暴露 `system`、`dark_flagship`。
- [x] 1.2 实现历史 `light` → `system`、`comfort_dark` → `dark_flagship` 的读取或写入兼容归一。
- [x] 1.3 保持非法主题值使用统一错误响应，且不修改已保存偏好。
- [x] 1.4 确认不需要新增数据库表或 migration；如现有字段保留旧值，使用兼容映射处理。

## 2. Web 主题模型与登录初始化

- [x] 2.1 收敛前端 `THEME_MODES` 与标签映射，只保留 `system`、`dark_flagship`。
- [x] 2.2 更新 `normalizeThemeMode`，覆盖历史 `light` 与 `comfort_dark` 兼容归一。
- [x] 2.3 更新 `resolveThemeMode` 与系统偏好监听，确保 `system` 可解析浅色/暗色，`dark_flagship` 始终解析暗色。
- [x] 2.4 更新 `src/web/index.html` 登录前主题初始化脚本，避免首屏主题闪烁或未知模式。

## 3. Web 管理端用户菜单 UI

- [x] 3.1 从 `AdminSidebar` 或相关布局中移除独立 `ThemeSwitcher` / `sidebar-theme` 展示。
- [x] 3.2 在 `AdminUserMenu` 展开层中新增主题切换按钮，不在按钮旁展示额外开关说明文案。
- [x] 3.3 为按钮提供图标、状态样式、`aria-label` 或 tooltip，支持鼠标和键盘触发。
- [x] 3.4 验证个人资料、密码修改、退出登录、点击外部关闭和侧边栏收起态不回退。
- [x] 3.5 使用 Design System semantic token 或既有 admin token，不新增裸 Hex。

## 4. OpenAPI / Orval / 文档

- [x] 4.1 导出 OpenAPI，确认主题偏好请求与响应枚举同步收敛。
- [x] 4.2 运行 Orval，更新 Web generated 类型。
- [x] 4.3 更新 API 索引或相关 API 文档中的主题偏好说明。
- [x] 4.4 更新 `/design-system` 或等价预览入口，确认只暴露当前支持的两种用户可选模式。

## 5. 测试与视觉证据

- [x] 5.1 补充后端 pytest：合法值、历史值兼容、非法值拒绝、`GET /auth/me` 返回归一值。
- [x] 5.2 补充前端 Vitest：用户菜单按钮渲染、点击切换、`aria-label` / tooltip、侧边栏收起态。
- [x] 5.3 补充前端主题单元测试：`THEME_MODES`、历史值兼容、系统偏好解析、登录初始化脚本。
- [x] 5.4 记录 1440px 用户菜单展开层、暗色旗舰状态、跟随系统浅色解析状态的截图或等价 UI 证据。
- [x] 5.5 运行相关后端测试、Web 测试、OpenAPI/Orval 生成校验、`python scripts/validate-openspec-language.py`。

## 验收返修记录

- [x] 2026-08-11 09:26:44 用户反馈用户菜单栏界面主题需参照图调整；已改为「左图标 + 文字 + 右侧切换按钮」主题行，并为个人资料、修改密码、界面主题、退出登录分别提供独立合适图标。
