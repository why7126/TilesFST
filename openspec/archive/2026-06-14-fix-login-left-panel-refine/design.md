## Context

- **需求来源**：`issues/requirements/archive/REQ-0003-login-left-panel-refine/`
- **前序 change**：`update-tilesfst-login-simplify`（REQ-0002）、`fix-login-pixel-fidelity`（REQ-0001 视觉）
- **当前实现**：CSS Port + `AuthBrandPanel` / `LoginForm`；主标题为 TilesFST；忘记密码按钮可见 noop
- **约束**：`rules/ui-design.md` 登录专章；REQ-0002 视口无滚动 MUST 保留

## 原型优先级

本 REQ **无独立 prototype/**；视觉以 **REQ-0001 `user-login.html` 结构 + REQ-0003 acceptance** 为准：

```text
1. issues/requirements/archive/REQ-0003-login-left-panel-refine/acceptance.md
2. issues/requirements/archive/REQ-0003-login-left-panel-refine/requirement.md
3. issues/requirements/archive/REQ-0001-user-login/prototype/web/user-login.html（结构参考）
4. rules/ui-design.md
5. openspec/specs/web-client/spec.md（归档态，本 change MODIFIED）
```

## Conflict Resolution（相对 REQ-0002 / 主 spec）

| 检查项 | REQ-0002 / 当前 spec | REQ-0003 | 决议 |
|---|---|---|---|
| `.logo` | TilesFST | TilesFST | 不变 |
| `.brand-title` | TilesFST | 瓷砖信息管理后台 | **REQ-0003** |
| 忘记密码 | 占位可见 | 隐藏 | **REQ-0003** |
| 视口无滚动 | MUST | MUST | REQ-0002 保留 |
| user-login.html 忘记密码 link | HTML 有 | 产品要求隐藏 | **REQ-0003** 覆盖 HTML（管理端策略） |

## Decisions

### D1：实现策略 — CSS Port 延续（Path A）

- **决策**：仅改 `AuthBrandPanel.tsx`、`LoginForm.tsx`、`login-page.css`；不引入 shadcn 表单 primitive。
- **理由**：与 REQ-0001/0002 已选 CSS Port 一致；变更范围小。
- **Auth 冻结**：不修改 `useAuth`、login API、token、路由守卫。

### D2：忘记密码隐藏方式

- **决策**：从 `LoginForm` **不渲染**「忘记密码？」节点（优于 `display:none`，利于 a11y Tab 序）。
- **备选**：CSS 隐藏 — 不利于可访问性与测试清晰度。

### D3：左栏间距

- **决策**：通过 `.brand-top` `margin-bottom` 或 `.brand-content` 负/零 margin 收紧 Logo 与眉标间距；目标约 12–16px 视觉 gap（较当前明显减小）。
- **约束**：不得触发左栏 overflow 或页面级滚动。

### D4：统计卡遮挡

- **决策**：优先 **上移 `.stats-card`**（减小 `margin-top` 或增加 `brand-content` 纵向压缩）并/或 **降低 `.material-board` 的 `bottom`**，确保 `z-index` 下 stats 文字可读；保留材质拼贴。
- **验收视口**：1440×1024；第三格「126 / 门店同步」完整可见。

## Goals / Non-Goals

**Goals：** FR-001 ~ FR-004 全部满足；Vitest + validate-design-system pass；REQ-0002 回归 pass。

**Non-Goals：** 忘记密码 API/页面；修改 `index.html` / AdminLayout 品牌。

## 验收 Gate

1440×1024 目视 checklist（写入 trace.md）：

1. Logo TilesFST 金色
2. 主标题「瓷砖信息管理后台」白色
3. Logo 与眉标间距紧凑
4. 统计三格均可读（126 不被 CALACATTA 遮）
5. 右栏无「忘记密码？」
6. 记住我 + 登录按钮正常
7. 无企微入口
8. 无页面级纵向滚动（1280×720 复验）

## Test Design

- `LoginPage.test.tsx`：主标题文案、无忘记密码
- `LoginForm.test.tsx`：query 不到「忘记密码？」
- `validate-design-system.py`：baseline pass
