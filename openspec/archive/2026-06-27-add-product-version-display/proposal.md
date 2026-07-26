## Why

REQ-0010-product-version-display 要求 Web 管理端与店主端在侧边栏顶部展示**人工维护**的产品版本号（如 `v0.0.1`），便于运维、客服与店主报障时对齐系统版本。当前 `AdminSidebar` 仅有 `TILESFST` logo 文案，店主端 `Sidebar` 无品牌头，且无统一产品版本常量。

## What Changes

- 新增 `src/shared/` 单一产品版本常量（如 `PRODUCT_VERSION = 'v0.0.1'`），管理端与店主端共用。
- 管理端 `AdminSidebar` 顶部：产品名 + 右侧 version pill（参照 SoulKing 参考图布局）。
- 店主端 `Sidebar` 顶部：品牌名 + 同一 version pill（筛选区之上）。
- 新增可复用 `ProductVersionBadge`（或等价组件）；semantic token 样式；`aria-label` 可访问性。
- Vitest：`AdminSidebar`、店主端 `Sidebar` 渲染含版本文案。
- **不** 变更后端 API、数据库、Orval、MinIO、登录页/页脚版本展示。

## Capabilities

### New Capabilities

（无新 capability 目录；行为归入 `admin-dashboard` 与 `web-client` delta。）

### Modified Capabilities

- `admin-dashboard`：MODIFIED「管理端 Sidebar 品牌与导航」— 增加产品版本 pill。
- `web-client`：ADDED「产品版本常量与 Web 端展示」— 跨端单一事实源、店主端侧栏版本展示、发版人工更新约束。

## Impact

| 影响面 | 说明 |
|---|---|
| 后端 | 无 |
| 前端 Web 管理端 | `AdminSidebar`、`admin-home.css`（brand-head） |
| 前端 Web 店主端 | `shared/ui/sidebar.tsx` 或封装 brand-head；`LandingPage` / `ListPage` 经 `CatalogBody` |
| `src/shared/` | 新增 `product-version.ts`（或等价） |
| 数据库 | 无 |
| API / Orval | 无 |
| Design System | 复用 semantic token badge；无新 Token |
| 测试 | vitest admin sidebar + catalog sidebar |
| Docker | 可选 `pnpm build`；无 compose 变更 |
| 发版 | release checklist 增加「更新 PRODUCT_VERSION」 |

## 风险

- 与 npm `package.json` / FastAPI `version` 混淆：spec 明确 MUST NOT 读取。
- 店主端 Sidebar 增量 brand-head 可能影响筛选区间距：design 约束 padding。
