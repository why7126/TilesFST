---
requirement_id: REQ-0010-product-version-display
title: Web 端产品版本号展示（管理端 + 店主端侧边栏）
terminal: multi
version: v1
status: in_sprint
owner: product
source: issues/requirements/archive/REQ-0010-product-version-display/capture.md
priority: P2
parent_requirement:
iteration: sprint-002
---

# REQ-0010 Web 端产品版本号展示

## 1. 需求背景

瓷砖信息管理平台需要在 Web 前端向用户展示**产品版本号**，便于内部运维、客服与店主在报障或沟通时快速对齐当前使用的产品版本。

版本号由**人工维护与更新**（发版时手动修改单一常量），**不**采用 CI 构建号、Git commit、npm `package.json` 版本或 FastAPI OpenAPI 版本自动注入。

产品方已确认：

- **展示范围**：管理端 + 店主端（Web catalog）
- **版本格式**：SemVer 风格，如 `v0.0.1`（带 `v` 前缀）
- **仅展示产品版本**，不展示 API / 后端版本
- **展示位置**：各端侧边栏顶部**产品名称**旁，参照竞品 SoulKing 侧边栏头部——产品名右侧以小号圆角 badge 展示版本号

当前代码现状：

- 管理端 `AdminSidebar` 顶部仅有 `.logo` 文案 `TILESFST`，无版本信息。
- 店主端 `Sidebar`（`src/web/src/shared/ui/sidebar.tsx`）为筛选侧栏，尚无产品名称 + 版本头部区域；顶部品牌目前在 `SiteNav` 中。

## 2. 目标用户

- **后台管理员 / 内部员工**：在管理端各页面侧边栏可见产品版本。
- **瓷砖零售店店主**：在店主端（目录/展示页）侧边栏可见同一产品版本。

## 3. 范围

### 3.1 本期包含

- 单一**产品版本**人工维护源（跨端共用）
- 管理端侧边栏头部：产品名称 + 版本 badge（FR-001）
- 店主端侧边栏头部：产品名称 + 版本 badge，视觉与管理端语义一致（FR-002）
- 版本 badge 样式：小号圆角 pill、muted 边框/背景、不抢主品牌视觉（FR-003）
- Vitest 覆盖两端侧边栏版本文案渲染

### 3.2 本期不包含

- 登录页、页脚、关于页版本展示
- API / 后端 / OpenAPI 版本展示或 `/health` 版本字段
- CI/CD 自动递增版本号
- 微信小程序
- 版本历史、更新日志、强制升级逻辑
- 管理端侧边栏折叠/展开交互（参考图右侧 chevron 可后续迭代）

## 4. 功能要求

### FR-001 产品版本人工维护（单一事实源）

- MUST 在 `src/shared/` 提供单一常量（或等价模块）定义产品版本，例如 `PRODUCT_VERSION = 'v0.0.1'`。
- 管理端与店主端 MUST 引用同一常量，保证两端展示一致。
- MUST NOT 读取 `package.json`、`pyproject.toml`、FastAPI `version` 或构建时 Git 信息作为产品版本。
- 发版流程 MUST 包含人工更新该常量（可在 release checklist / acceptance 中验收）。

### FR-002 管理端侧边栏版本展示

- 在 `AdminSidebar` 顶部 logo 区域，将现有单一 `.logo` 文案扩展为**产品名称 + 版本 badge** 横向排列。
- 产品名称 MUST 保持现有品牌呈现（`TILESFST`、`font-brand`、金色品牌调性）。
- 版本 badge MUST 紧贴产品名称右侧（同一行），垂直居中对齐，参照参考图 SoulKing + `v0.0.6` 布局。
- 版本文案 MUST 为 FR-001 常量值，格式如 `v0.0.1`。
- 所有 `/admin/*` authenticated 页面（经 `AdminLayout`）MUST 可见该版本 badge。
- MUST NOT 展示 API 版本或其他技术版本号。

### FR-003 店主端侧边栏版本展示

- 店主端使用侧边栏的页面（`LandingPage`、`ListPage` 等经 `CatalogBody` / `Sidebar` 渲染的模板）MUST 在侧边栏**顶部**增加产品名称 + 版本 badge 头部区域。
- 布局语义 MUST 与管理端一致：产品名左、版本 pill 紧邻右侧；位于侧边栏最上方（筛选区块之上）。
- 产品名称 SHOULD 与店主端品牌一致（默认 `STONEX` 或模板 `content` 中已有品牌名；实现时以 Design System 店主端品牌为准）。
- 版本值 MUST 与管理端共用 FR-001 常量。
- MUST NOT 仅在 `SiteNav` 顶栏展示而侧边栏缺失（本需求明确要求侧边栏位置）。

### FR-004 版本 badge 视觉规范

- Badge MUST 为小号圆角 pill（如 `rounded-industrial` 或等价 DS 圆角）。
- 字号 SHOULD 约 10–11px，颜色使用 semantic token：`text-muted` / `text-subtle`，边框 `border-border-default` 或 `border-border-chip`，背景 `bg-surface` 或透明 + 边框。
- MUST NOT 使用裸 Hex / rgba 硬编码。
- Badge MUST 可访问：版本区域 SHOULD 提供 `aria-label` 或可见文本，使读屏能获知产品版本（如「产品版本 v0.0.1」）。

### FR-005 测试与回归

- MUST 新增或扩展 Vitest：管理端 `AdminSidebar` 渲染含版本常量文案。
- MUST 新增或扩展 Vitest：店主端 `Sidebar`（或封装头部组件）渲染含同一版本文案。
- 修改版本常量后，测试 MUST 能反映新值（通过 import 常量断言，避免硬编码 duplicate）。

## 5. UI / UE 约束

- 参照产品提供的 SoulKing 侧边栏参考图：产品名 + 右侧小号版本 pill，位于侧边栏顶部左上角区域。
- 管理端继承 `admin-home.css` 与 `AdminLayout` 壳层；店主端继承 `Sidebar` / DS semantic token。
- 版本 badge 为**辅助信息**，不得挤压导航项、用户菜单或筛选区布局；窄屏下 product name + badge 可换行，但 badge 仍须紧跟产品名语义组。
- 禁止在 TSX/CSS 中新增裸 Hex。

## 6. 关联需求

| 需求 / 模块 | 关系 |
|---|---|
| REQ-0004-admin-home | 管理端布局壳层、`AdminSidebar` 挂载点 |
| 店主端 Landing / List 模板 | `Sidebar`、`CatalogBody` 挂载点 |
| `rules/ui-design.md` | Token、字号、品牌字体规范 |
| `rules/release.md` | 发版时人工更新版本常量检查项 |

## 7. 状态

```yaml
requirement_id: REQ-0010-product-version-display
priority: P2
status: in_sprint
iteration: sprint-002
owner: product
parent_requirement:
openspec_change: null  # 建议 add-product-version-display
target_clients:
  web_admin: 本期
  web_catalog: 本期
  wechat_miniapp: 不涉及
```
