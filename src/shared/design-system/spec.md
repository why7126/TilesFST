---
purpose: Design System 可执行总说明
content: 设计定位、Token、组件、模板与禁止事项摘要
source: rules/ui-design.md
update_method: UI 规范或代码资产变更时同步更新
note: 上游规范来源为 rules/ui-design.md
---

# Design System 总说明

## 设计定位

**工业石材 · 暗色旗舰风** — 面向瓷砖零售与企业管理的 B2B 数据平台视觉语言。

## 设计关键词

暗色旗舰、工业精度、品牌金点缀、石材质感、数据密度适中。

## 代码资产位置

| 层级 | 路径 |
|------|------|
| TS Token | `src/shared/design-system/tokens/` |
| Web CSS 变量 | `src/web/src/styles/globals.css` |
| Tailwind | `src/web/tailwind.config.ts` |
| shadcn 基础 | `src/web/src/components/ui/` |
| 复合 UI | `src/web/src/shared/ui/` |
| 业务组件 | `src/web/src/shared/business/` |
| 页面模板 | `src/web/src/shared/templates/` |
| 预览验收 | `/design-system`（开发环境） |

## 色彩系统（语义 Token）

| 语义 | 用途 |
|------|------|
| `bg-page` | 页面底色 |
| `bg-surface` | 卡片/面板 |
| `bg-deep` | 深层背景 |
| `text-primary` | 主文字 |
| `text-secondary` | 次要文字 |
| `text-muted` | 弱化文字 |
| `text-brand-gold` | 品牌金强调 |
| `border-border-default` | 默认边框 |
| `border-border-strong` | 强边框 |
| `border-border-focus` | 聚焦边框 |

## 字体与间距

- 品牌字体：`font-brand`、`tracking-brand`
- 正文：系统 sans-serif
- 间距/圆角：见 `tokens/spacing.ts`、`tokens/radius.ts`

## 组件规范

1. 优先复用 `templates` → `business` → `shared/ui` → `components/ui`
2. 禁止在业务页面硬编码 Hex 或 `bg-[#xxxxxx]`
3. 禁止绕过 DS 使用裸 `button`/`input`/`select`

## 页面布局

- 店主端：`LandingPage`、`ListPage`、`DetailPage`
- 管理端：`AdminListPage`、`AdminEditPage`

## 禁止事项

- 裸 Hex 颜色
- 未登记 Token
- 在 `features/` 或 `pages/` 重复实现已有 DS 组件
- 仅暗色写死（须支持 `.light` 预留）

## AI Prompt

见 `src/shared/design-system/prompts/`。
