---
purpose: 共享类型与SDK说明
content: 说明本目录职责、边界和AI新增文件规则
source: AI自动生成，人工确认
update_method: 目录职责变化时更新
note: AI新增文件前必须确认目录边界
---

# 共享类型与SDK说明

本目录职责请参考 `rules/directory-structure.md`。

## Design System Tokens

跨端 Design Token 单一事实源：

```text
src/shared/design-system/tokens/
├── colors.ts
├── spacing.ts
├── radius.ts
├── typography.ts
├── shadows.ts
├── css.ts          # 生成 Web CSS 变量
└── index.ts
```

Web 端通过 `pnpm sync:tokens`（在 `src/web`）同步到 `src/web/src/styles/tokens.generated.css`。

业务与页面模板：

```text
src/shared/business/types.ts       # 目录业务类型
src/shared/templates/types.ts      # 页面模板类型
src/web/src/shared/business/       # ProductCard、ProductGrid 等
src/web/src/shared/templates/      # LandingPage、ListPage 等
```

TypeScript 导入：

```typescript
import { getColorTokens, spacingScale } from '@shared/design-system/tokens';
```
