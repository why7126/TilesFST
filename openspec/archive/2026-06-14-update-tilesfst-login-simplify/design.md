## 设计

### 原型优先级（Conflict Resolution）

本 change 为 REQ-0002 产品策略变更，优先级：

```text
1. issues/requirements/archive/REQ-0002-product-brand-login-simplify/acceptance.md
2. issues/requirements/archive/REQ-0002-product-brand-login-simplify/requirement.md
3. issues/requirements/archive/REQ-0001-user-login/prototype/web/user-login.html（布局/CSS Port，品牌名与企微以 REQ-0002 为准）
4. rules/ui-design.md
5. openspec/specs/web-client/spec.md（归档前）
```

### Conflict Resolution

| 项 | REQ-0001 原型 | REQ-0002 | 决议 |
|---|---|---|---|
| Logo / 主标题 | STONEX / 瓷砖信息管理平台 | TilesFST | REQ-0002 |
| 企微入口 | `.third-party` + `.wecom` | 移除 | REQ-0002 REMOVED |
| 整页滚动 | 未强制 | 禁止 | REQ-0002 ADDED |

### 实现策略

- **品牌**：用户可见文案替换为 TilesFST；Design System 预览页 STONEX 命名不在本 change 范围。
- **登录简化**：删除 `ThirdPartyLoginSection` 组件链；保留 CSS Port 与 auth store 冻结。
- **视口锁定**：`.login-shell { position: fixed; inset: 0; overflow: hidden }` + `html:has(.login-shell) body { overflow: hidden }`。

### Goals

- Spec 与实现一致；可追溯 REQ-0002。
- 登录认证行为零回归。

### Non-Goals

- 企业微信 OAuth。
- 更新 REQ-0001 原型 HTML/PNG 文件。
- 店主端 / 小程序 rebranding。

### Auth 冻结

`features/auth/store`、`hooks/useAuth`、login API 调用 **MUST NOT** 变更。

### 验收 Gate

- 1280×720 视口：无 `document.documentElement` 纵向 scrollbar。
- 登录页无「企业微信登录」DOM。
- 品牌文案 spot-check：index.html、AuthBrandPanel、AdminLayout、main.py。
