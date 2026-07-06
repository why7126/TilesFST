---
purpose: UI设计规范
content: Web / 管理端 / 店主端 UI 方向、Design Token、组件复用与登录页约束
source: AI自动生成初稿，项目团队确认
update_method: 项目初始化后由人工确认；后续由AI辅助更新并经人工Review
created_at: 2026-06-13 00:00:00
updated_at: 2026-07-06 23:14:24
note: UI、Design System、前端样式任务必须读取
version: 1.0
---

# UI设计规范

Web 使用 React + Tailwind + shadcn/ui。管理端强调表格、筛选、表单效率；店主端强调图片浏览、移动端体验和询价转化。

视觉方向：**工业石材 · 暗色旗舰风**。关键词：工业感、克制、精密、高端。深色背景衬托材质纹理；品牌金只用于价格、强调词、主 CTA 和激活态；圆角接近直角。

## 1. Token 与资源地图

| 层级 | 路径 | 用途 |
|---|---|---|
| TS Token | `src/shared/design-system/tokens/` | 跨端 token 单一事实源 |
| Tailwind Config | `src/shared/design-system/tokens/tailwind.config.ts` | Web Tailwind 扩展 |
| CSS 颜色 | `src/web/src/styles/globals.css` | Web 颜色变量权威定义 |
| CSS 非颜色 | `src/web/src/styles/tokens.generated.css` | `pnpm sync:tokens` 生成 |
| shadcn 基础组件 | `src/web/src/components/ui/` | Button/Input/Label 等 |
| 复合 UI | `src/web/src/shared/ui/` | SearchBar/Sidebar/Pagination/Badge/Card 等 |
| 业务组件 | `src/web/src/shared/business/` | ProductCard/FeaturedCard/ProductGrid/TextureRow |
| 页面模板 | `src/web/src/shared/templates/` | Landing/List/Detail/Admin 页面骨架 |
| 预览页 | `/design-system` | 开发环境验收 |
| 使用说明 | `src/web/README.md`、`src/shared/README.md` | 组件与跨端约定 |

修改 Token 流程：

```text
1. 若设计语义变更，先更新本文件
2. 更新 src/shared/design-system/tokens/*.ts
3. 颜色同步 src/web/src/styles/globals.css
4. 非颜色执行 cd src/web && pnpm sync:tokens
5. 提交 tokens.generated.css
6. 新 token/组件同步 /design-system 预览
```

## 2. 强制样式规则（MUST）

- Web UI 新增/修改代码 MUST 使用 semantic token class，禁止在 TSX/CSS 中新增裸 Hex 或 token 对应的硬编码 `rgba(...)`。
- 常用 class：`bg-page`、`bg-surface`、`bg-deep`、`text-primary`、`text-secondary`、`text-muted`、`text-brand-gold`、`border-border-default`、`border-border-strong`、`border-border-focus`、`rounded-industrial`、`rounded-card`。
- `className` 合并 MUST 使用 `cn()` from `@/shared/lib/cn`。
- 默认暗色；浅色通过 `.light` 或 `[data-theme="light"]` 预留，禁止写死仅暗色 Hex。
- Logo/品牌名使用 `font-brand`、`tracking-brand`；正文使用系统 sans-serif。
- 新 shadcn 组件需 override 为 DS Token 后再使用。

## 3. 组件选用优先级（Web）

```text
1. src/web/src/shared/templates/     # 整页/管理端页面骨架
2. src/web/src/shared/business/      # 商品/目录等领域组件
3. src/web/src/shared/ui/            # 复合 UI
4. src/web/src/components/ui/        # shadcn 基础组件
5. 新增组件（必须经 OpenSpec Change）
```

不得在 `features/` 或 `pages/` 内重复实现已有 DS 组件。

## 4. 视觉规格摘要

### 色彩

| 语义 | 值/说明 |
|---|---|
| 页面底色 | `#18160F`，通过 token 使用 |
| 卡片/侧栏/搜索底色 | `#211E16`，通过 token 使用 |
| 页脚/深色底 | `#100F0A`，通过 token 使用 |
| 主文字 | `#EDE8DF`，通过 token 使用 |
| 次/弱文字 | 主文字 alpha 0.5 / 0.3 / 0.25，通过 token 使用 |
| 品牌金 | `#C8A055`，仅用于价格、主 CTA、强调、激活态 |
| 热销/警示 | 红橙语义 token |
| 分割线 | 白色 alpha 0.07 / 0.1 / 0.18，通过 token 使用 |

### 字体、间距、圆角

| 项 | 规则 |
|---|---|
| Hero 标题 | 约 38px / 400 |
| 页面标题 | 约 22px / 400 |
| 卡片标题 | 约 18-20px / 400 |
| 正文 | 约 13px，line-height 1.8 |
| 标签/眉标 | 9-10px，letter-spacing 0.12-0.18em |
| 页面内边距 | 约 28px |
| 卡片内边距 | 14-20px |
| 区块间距 | 24-32px |
| 圆角 | 按钮 2px、卡片/搜索 3px、Badge 1-2px |
| 分割线 | 优先 0.5px 或 token border |

## 5. 店主端页面结构

推荐结构：Nav → Hero → Data Strip → Search Bar → Filter Chips → Sidebar + Product Grid → Texture Row → Pagination → Footer。

- Hero：左文案/数据，右材质拼贴；主 CTA 用品牌金，次 CTA 用描边/幽灵按钮。
- SearchBar：品类下拉、文本输入、AI 找砖入口、搜索按钮四段式。
- ProductCard：图片 hover 轻微放大、信息区展示徽章/名称/规格/价格/操作。
- FeaturedCard：可跨列，左图右信息，适合高价值产品。
- TextureRow：横向色块作为材质/色系导航。
- Footer：品牌简介 + 链接分组 + 版权/社交入口。

## 6. 管理端页面结构

- 列表页优先 `AdminListPage` + 搜索/筛选/分页/表格或卡片表格。
- 表单页优先 `AdminEditPage` + shadcn `Input` / `Label` / `Checkbox`，保存 CTA 固定清晰。
- 弹窗 CRUD 遵守 `admin-modal` best practice，避免宽度和 CSS cascade 回归。
- 媒体上传遵守 `media-upload` best practice、MinIO 单桶策略和后端授权上传链路。

## 7. 交互规则

| 组件 | 规则 |
|---|---|
| 产品图 | hover `scale(1.03)`，约 0.4s ease |
| 导航链接 | hover 转主文字；active 主文字 + 品牌金下划线 |
| 筛选标签 | active 品牌金底/边/文字 |
| 图标按钮 | hover 使用轻微白色 alpha 背景 |
| 分页 | active 品牌金实底 + 深色文字 |
| Badge | 低高度、小字号、近直角，按现货/新品/热销语义 token |

## 8. 登录页（Web 管理端）

最高视觉源：

```text
issues/requirements/archive/REQ-0001-user-login/prototype/web/user-login.html
issues/requirements/archive/REQ-0001-user-login/prototype/web/user-login.png
issues/requirements/archive/REQ-0002-product-brand-login-simplify
src/web/src/features/auth/styles/login-page.css
```

实现策略（MUST）：

- 登录页从 `user-login.html` CSS Port 到专用 `login-page.css`；React 只负责 DOM 与 auth 交互。
- 颜色引用 `globals.css` 的 `--color-*`；TSX 禁止裸 Hex；材质 tile 渐变可用 scoped CSS variables。
- 表单使用原生 `<input>` / `<button>` + port CSS class；不得套用 shadcn 默认皮相。
- 左栏使用 CSS 材质拼贴 `.material-board`；不得用 JPG 全屏铺底替代。
- 桌面 ≥1024px 左右 50% 分屏；移动隐藏左栏，表单居中，max-width 520px。
- TilesFST Logo 使用 `var(--font-brand)` / `font-brand`、`letter-spacing: 0.16em`、品牌金。
- `.login-shell` 锁定视口，禁止页面级纵向滚动；不提供企微/第三方登录；禁止 notice 横幅和版权 footer 回归。
- 输入框透明底 + emphasis 边框，focus 纯品牌金；主按钮金色实底；语言切换在右上角。

## 9. 验收

- UI 任务前读取本文件相关章节，并检查可复用模板/组件。
- UI 变更完成前访问或等价验证 `/design-system`；登录页和有 prototype 的页面需按 HTML > PNG > context > acceptance > 本文件优先级验收。
- Change 输出需说明是否影响 Web / 管理端 / 小程序、是否修改 token、是否运行 `pnpm sync:tokens`、是否存在裸 Hex。
