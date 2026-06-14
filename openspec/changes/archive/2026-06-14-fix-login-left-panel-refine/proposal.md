## Why

REQ-0003 追溯补登：Sprint 001 登录页在 REQ-0002（TilesFST Logo、无企微、视口锁定）落地后，产品方反馈四项左栏/表单问题：

1. 左栏白色主标题应为 **「瓷砖信息管理后台」**（金色 Logo **TilesFST** 保留）— 与 REQ-0002 将主标题也改为 TilesFST 冲突。
2. **忘记密码** 本期暂不开放，须隐藏入口（REQ-0001/0002 spec 仍要求占位链接可见）。
3. Logo 与下方眉标间距过大。
4. 统计卡「126 / 门店同步」被 `.material-board`（CALACATTA）遮挡。

前序 `update-tilesfst-login-simplify` 解决了品牌与企微，但未覆盖上述布局与文案分层；需 **fix-*** change 修正 `web-client` spec 与实现。

## What Changes

- `AuthBrandPanel`：`.brand-title` →「瓷砖信息管理后台」；`.logo` 保持 TilesFST。
- `LoginForm`：移除或隐藏「忘记密码？」入口；`.form-options` 布局微调。
- `login-page.css`：收紧 `.brand-top` 间距；调整 `.stats-card` / `.material-board` 避免遮挡。
- 更新 Vitest：`LoginPage.test.tsx`、`LoginForm.test.tsx`。
- **MODIFIED** `web-client` spec：管理端登录页、占位功能、可访问性 Tab 序、DS 实现、PNG gate。

## Capabilities

### New Capabilities

（无）

### Modified Capabilities

- `web-client`：MODIFIED 管理端登录页、登录页 PNG 验收 gate、登录页控件原型形态、占位功能、可访问性、管理端登录页 Design System 实现。

## Impact

| 影响面 | 说明 |
|---|---|
| Web 管理端 | 登录页 presentation only |
| Backend / API / DB / Orval | 无 |
| Auth 逻辑 | 冻结（store、login API、路由守卫不变） |
| Design System | 继续 CSS Port；`validate-design-system.py` 须 pass |
| 文档 | REQ-0003 trace、sprint-001 acceptance-report（tasks 内） |

## Out of Scope

- 忘记密码完整流程（后续独立 REQ）
- 全站 rebranding（顶栏/browser title 仍为 TilesFST）
