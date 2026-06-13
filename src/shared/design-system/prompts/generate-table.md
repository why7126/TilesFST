# AI 生成表格/列表提示词

管理端列表 MUST 优先使用 `AdminListPage` 模板。

## 组件

- 搜索：`SearchBar` from `@/shared/ui`
- 分页：`Pagination` from `@/shared/ui`
- 状态：`Badge` from `@/shared/ui`
- 操作按钮：shadcn `Button` outline/ghost variants

## 规则

- 表头与行使用 `bg-surface`、`border-border-default`
- 空状态使用 DS Empty 模式（或模板内约定）
- 不引入未登记的表格库，除非 OpenSpec Change 明确

## 数据

模板仅负责布局；数据请求放在 `features/` 或 `services/`，通过 Orval 生成客户端。
