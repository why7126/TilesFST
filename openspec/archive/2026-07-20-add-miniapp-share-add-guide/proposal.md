## Why

用户进入微信小程序后，容易不知道如何通过右上角微信原生入口将小程序添加到“我的小程序”，导致下次找回路径不清晰。新增轻量引导语可以降低用户找回成本，同时保留用户手工关闭权，避免形成持续打扰。

## What Changes

- 新增小程序“添加到我的小程序”引导能力：用户进入小程序时，在右上角微信原生菜单 / 分享入口附近展示轻量引导语。
- 引导语必须避让微信原生胶囊、状态栏、自定义导航栏和首屏内容，不得手绘模拟微信系统按钮或胶囊。
- 用户必须可以手工关闭引导语；关闭后至少当前会话内不再展示，后续可按评审确认扩展为当天或长期记忆。
- 默认使用小程序本地状态承接关闭记忆，不新增 API、数据库、Web 管理端配置或 Orval 变更。
- 后续实现必须按小程序自定义导航 best-practice 与设备 evidence 模板记录 DevTools / 真机验收边界。

## Capabilities

### New Capabilities

- `miniapp-share-add-guide`: 小程序添加到“我的小程序”引导语展示、胶囊避让、手工关闭、频率控制、安全降级和设备验收契约。

### Modified Capabilities

- 无。现有 `miniapp-home`、`miniapp-global-custom-navigation-bar`、`miniapp-device-evidence-template` 作为布局、胶囊避让和 evidence 依赖引用，本 Change 不直接修改其正式需求。

## Impact

- 小程序：预计影响 `src/miniapp` 首页或共享引导组件、全局入口逻辑和本地关闭状态存储。
- API：默认不新增或修改接口；若后续实现引入服务端控制或埋点，必须另行同步 OpenAPI、Orval、docs 和测试。
- 数据库：默认不新增表、字段或迁移。
- Web / 管理端：不涉及。
- 测试：后续实现需补充小程序静态测试、DevTools 320/375/430 pt evidence、真机 evidence 或明确 blocked/follow_up。
