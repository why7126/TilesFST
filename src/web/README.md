---
purpose: Web展示端与管理端说明
content: 说明本目录职责、Design System 使用约定
source: AI自动生成，人工确认
update_method: 目录职责变化时更新
note: AI新增文件前必须确认目录边界
---

# Web展示端与管理端说明

本目录职责请参考 `rules/directory-structure.md`。

## Design System

工业石材 · 暗色旗舰风 Design Token 与 shadcn/ui 基础组件。

### Token 位置

- **TypeScript Token（单一事实源）**：`../shared/design-system/tokens/`
- **颜色 CSS Variables（Web 权威）**：`src/styles/globals.css`（`:root` 暗色 + `.light` 浅色）
- **间距/圆角/字体（自动生成）**：`src/styles/tokens.generated.css`
- **规范来源**：`rules/ui-design.md`
- **预览页**：开发环境访问 `/design-system`

同步 CSS：

```bash
cd src/web
pnpm sync:tokens
```

`pnpm build` 使用已提交的 `tokens.generated.css`（Docker 构建上下文为 `src/web`，不含 `src/shared`）。修改 Token 后 MUST 运行 `pnpm sync:tokens` 并提交生成的 CSS 文件。

### 目录结构

```text
src/
├── components/ui/       # shadcn 基础组件（button, input, checkbox, label, separator）
├── shared/
│   ├── lib/cn.ts        # className 合并工具
│   └── ui/              # 复合组件（icon-input, divider-text）
└── styles/
    ├── globals.css      # Tailwind @theme + utilities
    └── tokens.generated.css  # 由 sync:tokens 生成，勿手工编辑
../shared/design-system/tokens/  # TS Token 单一事实源
```

### 使用约定

1. **禁止裸 Hex**：新增 UI 代码 MUST NOT 硬编码 `#18160F`、`#C8A055` 等 token 色值，使用 semantic class（如 `bg-page`、`text-brand-gold`、`border-strong`）。
2. **Token 修改**：编辑 `src/shared/design-system/tokens/`，然后运行 `pnpm sync:tokens`。
3. **TypeScript 引用**：`import { getColorTokens } from '@shared/design-system/tokens'`。
4. **className 合并**：使用 `cn()` from `@/shared/lib/cn`。
5. **圆角**：按钮/输入框使用 `rounded-industrial`（2px），卡片使用 `rounded-card`（3px）。
6. **组件导入**：从 `@/components/ui/*` 导入 shadcn 组件。

### 添加 shadcn 组件

```bash
cd src/web
npx shadcn@latest add <component-name>
```

配置见根目录 `components.json`（style: new-york，Tailwind v4）。

### 本地开发

```bash
pnpm dev          # 本地（pnpm）
npm run build     # 生产构建（Docker 同样使用 npm）
pnpm test         # 单元测试
```

### 相关 OpenSpec

- `openspec/changes/archive/2026-06-13-add-design-system` — Design System 建立
- `openspec/changes/archive/2026-06-13-refactor-login-ui` — 登录页 DS 组件化
- `openspec/changes/fix-login-pixel-fidelity` — 登录页 PNG 像素级对齐

### 登录页视觉

- 路由：`/admin/login`
- Golden reference：`issues/requirements/REQ-0001-user-login/prototype/web/user-login.png`
- 品牌字体：`font-brand`（Cormorant Garamond，见 `index.html` + `globals.css`）
- 组件树：`LoginFormPanel` / `LoginHeader` / `LoginForm` / `ThirdPartyLoginSection`
- 登录页专用样式：`src/features/auth/styles/login-page.css`（自 `user-login.html` port）
