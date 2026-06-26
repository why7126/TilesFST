## Why

`add-brand-management`（REQ-0005）与多项品牌 fix change 已落地 `/admin/brands`，但行内「启用」「停用」仍为点击即调 API，误触风险较高；删除操作已有独立确认弹窗。产品要求 **启停均增加二次确认**（REQ-0008-brand-status-confirm），交互与文案对齐同页删除确认及已归档 `fix-tile-category-management-refine` 类目启停模式。本 change 为 **fix-*** 专项，在不动 API、删除规则、弹窗字段与权限前提下增加启停确认前置步骤。

## What Changes

- **启停二次确认（O-01）**：点击「启用」「停用」弹出确认框（复用删除 modal 结构）；确认后调用 enable/disable；取消/遮罩/×/ESC 不请求。
- **文案**：停用「确认停用品牌「{name}」？停用后前台将不再展示该品牌。」；启用「确认启用品牌「{name}」？」
- **状态机**：独立 `statusConfirmTarget`（与 `deleteTarget` 分离）；确认后 Toast「品牌已启用/已停用」并刷新列表与 summary。
- **测试**：vitest 覆盖启停确认 DOM 与 API 调用时机；build 通过。

## Capabilities

### New Capabilities

（无）

### Modified Capabilities

- `web-client`：ADDED「品牌列表启停二次确认」—— `/admin/brands` 列表行启停须二次确认，复用 modal 结构，删除确认独立。

## Impact

| 影响面 | 说明 |
|---|---|
| 后端 | 无变更 |
| 前端 Web 管理端 | `BrandManagementPage.tsx` |
| API / Orval | 无 |
| 数据库 | 无 |
| Design System | 无新 Token；复用既有 `modal-*` 与 `brand-management.css` |
| 测试 | `BrandManagementPage.test.tsx` 更新/新增 |
| Docker | web 镜像重建（可选） |
| 依赖 | `add-brand-management` 基线；参考 `fix-tile-category-management-refine`（已 archive） |
