# 设计：管理后台主题入口与模式收敛

## 1. 决策

采用“既有主题能力收敛”策略：保留现有 `ThemeProvider`、本地存储、账号级同步和 CSS token 解析机制，收敛可见模式与入口，不重做主题体系。

核心决策：

- 管理端主题入口属于用户偏好，放入 `AdminUserMenu` 展开层。
- 控件使用按钮完成二态切换，不使用四项下拉选择器。
- 可见业务模式只保留 `dark_flagship` 与 `system`。
- 历史 `light` 归一为 `system`，历史 `comfort_dark` 归一为 `dark_flagship`。
- `system` 继续通过 `prefers-color-scheme` 解析实际 `light` / `dark`，因此 Design Token 仍需保留可解析的 `light` CSS 变量，但不作为独立用户选项暴露。

## 2. 冲突处理

事实源优先级：

```text
prototype/web/context.md > acceptance.md > requirement.md > rules/ui-design.md > openspec/specs
```

冲突与处理：

| 冲突 | 处理 |
|---|---|
| `web-client` 当前要求主题选择器位于侧边栏用户区上方 | 本 Change 修改为用户菜单展开层内的主题按钮，并移除侧边栏独立选择器。 |
| `web-client` / `design-system` / `auth` 当前声明四种主题模式 | 本 Change 收敛用户可选/API 支持值为 `system` 与 `dark_flagship`，并定义历史值兼容归一。 |
| `design-system` 当前要求 `/design-system` 可切换四种模式 | 本 Change 要求预览入口仅暴露当前支持的两种模式；系统浅色解析仍需可验收。 |
| 用户要求“不需要显示开关文案”与可访问性要求存在张力 | 可见界面不展示额外说明文案，但按钮必须提供 `aria-label` 或 tooltip。 |

## 3. UI Contract

| 项 | 合同 |
|---|---|
| 页面与入口 | 适用于所有 `AdminLayout` 管理端页面；入口位于侧边栏底部用户菜单展开层。 |
| 信息架构 | 侧边栏保留用户菜单触发器；移除独立 `sidebar-theme` 区域；用户菜单内新增主题行。 |
| 控件形态 | 用户菜单每个菜单项使用独立合适图标；主题行采用左侧主题图标 + 「界面主题」文字 + 右侧二态 switch 样式切换按钮，不使用 Select。 |
| 可见文案 | 按用户要求不在主题开关旁展示“暗色旗舰 / 跟随系统”等额外模式说明文案，仅保留菜单项名称「界面主题」。 |
| 可访问性 | 按当前状态提供 `aria-label` 或 tooltip，例如“切换到跟随系统”“切换到暗色旗舰”。 |
| 视觉 token | 使用 Design System semantic token 或既有 admin token；禁止新增裸 Hex。 |
| 交互状态 | 覆盖 hover、focus、active、键盘触发、同步失败反馈、侧边栏收起态和窄屏状态。 |
| Mock/API 边界 | UI 可先基于本地主题上下文实现；完成前必须接入 `PATCH /api/v1/auth/me/theme`。 |
| 权限规则 | 仅影响已登录管理端用户菜单；未认证登录页仍只使用本地主题初始化，不调用账号 API。 |
| 一致性参照 | 以 `issues/requirements/archive/REQ-0109-admin-theme-user-menu-modes/prototype/web/context.md` 与 `acceptance.md` 为验收参照。 |

## 4. API 与兼容策略

- `PATCH /api/v1/auth/me/theme` 请求枚举收敛为 `system` 与 `dark_flagship`。
- `GET /api/v1/auth/me` 的 `data.theme_mode` 返回值必须为 `system` 或 `dark_flagship`。
- 若数据库或本地存储中存在历史 `light`，读取时归一为 `system`。
- 若数据库或本地存储中存在历史 `comfort_dark`，读取时归一为 `dark_flagship`。
- 其他未知值按现有错误码策略拒绝写入；读取侧应回退为稳定默认值，避免页面未知主题。
- 同步 OpenAPI、Orval 和前后端测试，确保生成类型不继续暴露 `comfort_dark` / 独立 `light`。

## 5. 验证策略

- 前端 Vitest：用户菜单按钮渲染、点击切换、`aria-label` / tooltip、侧边栏收起态。
- 前端主题单元测试：`THEME_MODES`、`normalizeThemeMode`、`resolveThemeMode`、登录前初始化脚本。
- 后端 pytest：主题偏好合法值、历史值兼容、非法值处理、`GET /auth/me` 返回归一值。
- 生成校验：导出 OpenAPI 并运行 Orval，确认类型同步。
- UI 证据：记录 1440px 用户菜单展开层、暗色旗舰状态、跟随系统浅色解析状态；确认无重叠和无裸 Hex。

## 6. 不做事项

- 不新增数据库表。
- 不调整 MinIO、对象存储、Docker Compose 或 Nginx。
- 不新增小程序主题能力。
- 不把主题偏好升级为系统设置。
