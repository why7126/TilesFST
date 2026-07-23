---
change_id: fix-login-page-tool-selector-alignment
status: proposed
created_at: 2026-07-21 14:41:52
updated_at: 2026-07-21 23:00:30
source: bug
source_bug: BUG-0071-login-page-theme-language-selector-misalignment
related_requirement: null
iteration: sprint-010
capabilities:
  - web-client
---

# Trace - fix-login-page-tool-selector-alignment

## 来源

| 类型 | ID | 说明 |
|---|---|---|
| BUG | `BUG-0071-login-page-theme-language-selector-misalignment` | 登录页右上角主题选择模块与语言选择模块没有对齐 |
| Capability | `web-client` | Web 管理端登录页工具区布局规范 |

## Bug Analysis Report

| 项 | 内容 |
|---|---|
| 现象 | Web 管理端登录页右上角主题选择模块与语言选择模块没有对齐 |
| 复现 | 打开 `/admin/login`，对比语言选择模块和主题选择模块的顶部位置、右侧边界与视觉基线 |
| 影响 | 登录页首屏辅助工具区错位，降低管理端入口页视觉一致性和专业感 |
| 根因分类 | design / ux |
| 严重等级 | medium |
| Hotfix | 不需要 |

## 状态记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-21 23:00:30 | /opsx-apply | 完成登录页工具区布局修复、前端回归测试与桌面/窄屏截图验收；等待 Workflow Sync 标记 applied |
| 2026-07-21 14:57:57 | /sprint-propose | 纳入 sprint-010 正式范围 |
| 2026-07-21 14:41:52 | /bug-opsx | 创建修复 Change，状态 proposed |

## 实现与验收证据

| 类型 | 证据 |
|---|---|
| 实现 | `LoginPage.tsx` 将 `ThemeSwitcher` 与 `LanguageSwitcher` 统一放入 `.login-tools`；`LoginFormPanel.tsx` 不再单独定位语言按钮；`login-page.css` 统一控件高度、右侧边界、间距和窄屏纵向布局。 |
| 回归测试 | `pnpm --dir src/web exec vitest run src/features/auth/components/LoginPage.test.tsx src/features/auth/components/LoginFormPanel.test.tsx src/features/auth/components/LoginForm.test.tsx src/features/theme/ThemeContext.test.tsx`，4 files / 18 tests passed。 |
| 视觉证据 | Playwright CLI 截图：`/private/tmp/login-tools-desktop.png`、`/private/tmp/login-tools-mobile.png`。桌面工具区右上水平对齐；窄屏工具区位于标题上方，不遮挡标题、表单或安全提示。 |
| API / Orval | 本次仅调整 Web 登录页 DOM/CSS 和前端测试，不修改认证 API、响应字段、数据库或 Orval 生成物。 |
| 知识库 | 本次为登录页局部布局收敛，无跨模块复用事故模式，不新增 `docs/knowledge-base/incidents/`。 |
