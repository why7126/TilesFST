## Why

产品方确认对外品牌统一为 **TilesFST**，且管理端登录页应仅保留账号密码路径、在常见桌面视口下无页面级纵向滚动。上述变更已在 `src/` 追溯实现，需通过 OpenSpec 将 `web-client` spec 与 REQ 文档对齐，避免与 REQ-0001 中企微/STONEX 要求冲突。

## What Changes

- 用户可见产品名统一为 **TilesFST**（页面标题、登录左栏、管理端顶栏、OpenAPI 标题）。
- 登录页 **移除** 企业微信登录入口与第三方分割区。
- 登录页 **锁定视口**，禁止 `html`/`body` 页面级纵向滚动（100vh 内展示表单与安全说明）。
- **BREAKING（相对 REQ-0001 原型）**：不再要求登录页展示企微按钮；Logo 文案由 STONEX 改为 TilesFST。

## Capabilities

### New Capabilities

（无）

### Modified Capabilities

- `web-client`：MODIFIED 管理端登录页、静态资源、PNG 验收 gate、占位功能、可访问性 Tab 顺序、DS 实现间距；REMOVED 企业微信图标视觉 requirement 及企微相关 scenario。

## Impact

- **Web 管理端**：登录页 presentation、品牌文案；auth 逻辑不变。
- **Backend**：仅 FastAPI 文档标题字符串。
- **API / DB / Orval / Docker**：无行为变更。
- **Spec**：`openspec/specs/web-client/spec.md` 归档时合并 delta。
- **文档**：REQ-0002、`iterations/archive/sprint-001`、`rules/ui-design.md` 登录专章企微条目（tasks 内更新）。
