---
purpose: Web展示端与管理端说明
content: 说明本目录职责、Design System 使用约定
source: AI自动生成，人工确认
update_method: 目录职责变化时更新
created_at: 2026-06-13 00:00:00
updated_at: 2026-07-12 00:00:00
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

### Clipboard 复制 helper

Web 管理端复制文本统一使用 `src/shared/lib/clipboard.ts` 的 `copyTextToClipboard`。helper 只负责归一化文本、调用 Clipboard API、返回 `success` / `failed` / `unavailable` / `empty` 结构化结果，并可选执行手动选择 fallback；调用方负责 toast、`role="status"` 文案、dialog、业务 DOM 和埋点。

调用方文案、fallback、敏感值分类、checklist、示例与反例见 [`../../docs/knowledge-base/best-practices/clipboard-fallback.md`](../../docs/knowledge-base/best-practices/clipboard-fallback.md)。

约束：

1. 调用方不得重复散落 `navigator.clipboard?.writeText` 分支，除非有明确平台差异说明。
2. helper 和调用方不得记录随机密码、token、Authorization、Cookie、对象存储 key 等敏感复制内容。
3. Clipboard API 不可用或写入失败时，调用方必须提供明确手动复制路径；密码等输入型场景应聚焦并选中文本。

## 产品静态 Logo

产品自身的静态 Logo 文件位于 `public/logos/`，由 Vite 构建时原样复制到站点根路径 `/logos/`。这些文件用于管理端品牌区与浏览器标签图标，不走 MinIO，也不属于门店品牌 Logo 上传资源。

| 文件 | 用途 |
|---|---|
| `public/logos/64x64.png` | 管理端品牌区 40x40 展示图；浏览器 favicon 默认尺寸 |
| `public/logos/128x128.png` | 高分屏或浏览器自动选择的 favicon 备用尺寸 |
| `public/logos/256x256.png` | Apple touch icon 与更高分辨率入口图标 |

维护约定：

1. 管理端 Shell 品牌区优先引用 `/logos/64x64.png`，避免大图缩放造成额外体积。
2. `index.html` 中的 `icon` / `apple-touch-icon` 必须与 `public/logos/` 内实际文件保持一致。
3. 旧的 `public/images/` 产品 Logo 文件已废弃并删除，新增代码不得继续引用该类路径。
4. 门店或业务品牌 Logo 上传仍走后端授权与 MinIO `/media/` 访问链路，不得与产品静态 Logo 混用。

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
- Golden reference：`issues/requirements/archive/REQ-0001-user-login/prototype/web/user-login.png`
- 品牌字体：`font-brand`（Cormorant Garamond，见 `index.html` + `globals.css`）
- 组件树：`LoginFormPanel` / `LoginHeader` / `LoginForm`
- 登录页专用样式：`src/features/auth/styles/login-page.css`（自 `user-login.html` port）
