# AI 生成表单提示词

表单页 MUST 使用：

- `Input`、`Label`、`Checkbox`、`Button` from `@/components/ui`
- `IconInput`、`DividerText` from `@/shared/ui`（登录等场景）
- `AdminEditPage` 模板（管理端表单）

## 规则

- 错误提示使用 `text-error` 或 DS 约定色，禁止裸 Hex
- 聚焦态仅金色边框，无多余 ring-offset
- 主 CTA 使用金色实底 Button variant
- 字段校验在组件层或 feature 层，不在模板层写死业务

## 禁止

- 原生 `<input>` / `<button>` 直接写样式
- 自定义未登记间距/圆角
