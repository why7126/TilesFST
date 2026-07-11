---
requirement_id: REQ-0013-admin-shell-padding-refine
title: 管理端 Shell 内外边距收窄与内容区 fluid 布局
terminal: web-admin
version: v1
status: done
owner: product
source: issues/requirements/archive/REQ-0013-admin-shell-padding-refine/capture.md
priority: P1
parent_requirement: REQ-0004-admin-home
updated_at: 2026-07-11 17:18:39
---

# REQ-0013 管理端 Shell 内外边距收窄与内容区 fluid 布局

## 1. 需求背景

管理端经 `REQ-0004-admin-home` 落地的 `AdminLayout` 壳层沿用原型 `admin-home.html` 的 spacing 与内容宽度策略：

- 侧栏 `.sidebar` 水平 padding 18px，在 264px 列宽下菜单文案与列边缘留白过多；
- 主内容 `.main-content` 使用 `padding: 48px 56px 72px`；
- `.content-inner` 固定 `max-width: 1080px` 且居中，与外层 padding 叠加后在宽屏（≥1440px）形成明显左右对称暗区；
- 瓷砖 SKU 列表页另设 `max-width: 1120px` override，与全局 shell 策略分裂。

产品反馈（`/admin/tile-skus` 宽屏截图）：侧栏与主内容区「红框区域」过宽，列表/表格信息密度偏低。

`/req-explore` 曾确认：本需求为 **REQ-0004** 的布局 refine；**不改动**侧栏列宽 264↔72（`REQ-0011` 契约）。后续用户反馈升级为 `BUG-0054-admin-content-padding-too-large`，并通过已归档 OpenSpec Change `fix-admin-content-padding-too-large` 落地。当前事实源以该 BUG / Change 为准：主内容区采用 `24px 24px 48px`，content-inner 采用 `min(1440px, 100%)`，原 `32px 32px 72px` / `min(1400px, 100%)` 方案不再作为验收目标。

## 2. 目标用户

- **后台管理员 / 内部员工**：在 `/admin/*` 各页面浏览列表、Dashboard 与表单；需要宽屏下更充分利用横向空间，减少无效留白。

## 3. 范围

### 3.1 本期包含

- `admin-home.css` 统一管理端 shell spacing token（desktop / tablet / mobile 三档）
- 侧栏 **expanded** 与 **collapsed** 态 padding 收窄（列宽 264px / 72px 不变）
- 侧栏内部 `.sidebar-head`、`.nav-title`、`.nav-item` 等水平 padding **联动收紧**，避免 6px 壳层与 14px 分区标题错位
- 主内容 `.main-content` 上/左右/下 padding 收窄为当前落地值：desktop `24px 24px 48px`
- `.content-inner` 统一 fluid：`max-width: min(1440px, 100%)`；`margin: 0 auto` 保留
- 删除 `tile-sku-management.css` 中 `:has(.sku-page-hero) .content-inner { max-width: 1120px }`
- ≤1023px / ≤639px 响应式 padding **联动调整**（tablet 侧栏勿沿用 desktop 6px）
- Prototype（`/req-complete` 补齐）：expanded 1440/1920、collapsed、≤1023 一帧 + context.md（历史参考；最终验收以 BUG-0054 当前实现为准）
- Vitest 回归：`AdminSidebar` collapse、`AdminLayout` smoke；AdminLayout 样式静态断言覆盖旧 padding / 旧 max-width 清理

### 3.2 本期不包含

- 侧栏列宽 `--admin-sidebar-width`（264px ↔ 72px）变更
- 折叠 chevron 行为、localStorage 持久化（`REQ-0011`）
- 导航项真实 SVG/Lucide 图标（`BUG-0021`）
- ≤1023px 侧栏 grid 结构、隐藏 user menu、chevron 禁用逻辑变更（`REQ-0011`）
- 店主端、微信小程序
- 后端 / API / 数据库 / Orval
- 单页业务内容（指标数量、表格列定义）变更

## 4. 功能要求

### FR-001 主内容区 padding（desktop >1023px）

- `.main-content` padding MUST 自 `48px 56px 72px` 调整为当前落地值 **`24px 24px 48px`**。
- 原探索阶段的 `32px 32px 72px` / bottom 72px 要求已被 `BUG-0054` 修订，不再作为验收目标。
- 主内容区 MUST 仍 `overflow: auto`；不得因 padding 变更引入横向滚动条（内容本身超宽除外）。

### FR-002 侧栏 padding — expanded（desktop >1023px）

- `.sidebar` padding 当前落地为 **`30px 10px 18px`**（仅收窄水平方向），比 REQ-0004 原始 `30px 18px 18px` 更紧凑。
- `.sidebar-head`、`.nav-title`、`.nav-item` 等子元素水平 padding MUST 在 prototype 定稿值内联动收紧，满足：
  - 最长菜单文案（如「Banner 管理」）在 264px 列内不异常换行；
  - 分区标题与 nav 项左缘视觉对齐，不得出现「壳层 6px、title 14px」明显阶梯错位；
  - chevron（`REQ-0011`）不遮挡品牌区与 version badge。
- 侧栏 **列宽 MUST 保持 264px**。

### FR-003 侧栏 padding — collapsed（desktop >1023px）

- `[data-sidebar-state='collapsed'] .sidebar` padding 当前落地为 **`16px 10px 18px`**。
- collapsed padding 维持与现有居中、avatar、toggle、nav-icon 表现兼容；原 `12px 6px 14px` 不再作为最终验收值。
- **列宽 MUST 保持 72px**；`.nav-scroll` MUST NOT 出现横向滚动条。
- 34px avatar、16px nav-icon、28px toggle MUST 在 72px 列内正常居中展示；`AdminUserMenu` dropdown 行为 MUST 与 `REQ-0011` 一致。

### FR-004 Content-inner fluid — 当前策略

- `.content-inner` MUST 使用统一规则：

```css
max-width: min(1440px, 100%);
margin: 0 auto;
```

- MUST **删除** `tile-sku-management.css` 中对 `.content-inner` 的 `1120px` override。
- MUST NOT 在其他页面 CSS 中重新引入 divergent `max-width`（列表/ Dashboard 共用 shell token）。
- 在 1920×1080 expanded 侧栏下，content-inner 受 **1440px** 软 cap 限制；在 1440×1024 下随可用宽度 fluid。

### FR-005 响应式 padding 联动

视口 **≤1023px**（tablet / 窄桌面）：

- MUST 联动调整 `.sidebar` 与 `.main-content` padding；**MUST NOT** 对全宽侧栏 grid 沿用 desktop 紧凑水平 padding。
- 当前落地：sidebar **`22px 20px`**；main-content **`20px 16px 40px`**。
- MUST 保持 `REQ-0011` 既有结构：侧栏置顶、双列 nav、隐藏 sidebar-user、chevron 隐藏。

视口 **≤639px**（mobile）：

- MUST 联动调整 main-content padding；当前落地为 **`16px 12px 32px`**。
- Dashboard metric/quick grid 既有 `@media` 列数规则 MUST 不受影响。

### FR-006 全站回归与验收基准页

- 下列页面 MUST 在 **1440×1024** 与 **1920×1080** 下并排验收（expanded；SKU 另验 collapsed）：

| 路由 | 页面 | 覆盖点 |
|------|------|--------|
| `/admin/tile-skus` | 瓷砖 SKU 列表 | 宽表格、筛选条；曾 1120 override |
| `/admin/users` | 用户管理 | 列表页 DOM 基准（`admin-list-page-consistency`） |
| `/admin/dashboard` | 管理首页 | metric/quick 四列 grid |

- 验收时 content 区左右视觉 gutter SHOULD 显著小于变更前 1080px 居中方案；最终阈值以 `BUG-0054` 的当前实现与静态测试为准。
- 所有其他 `/admin/*` 页面 SHOULD smoke：无布局错位、无 shell 横向溢出。

### FR-007 测试

- MUST 回归现有 Vitest：`AdminSidebar.collapse.test.tsx`、`AdminLayout.test.tsx`。
- SHOULD 断言 collapsed 态 `.nav-scroll` 无 `scrollWidth > clientWidth`（或等价 class/DOM 约束）。
- MUST NOT 破坏 `localStorage` 侧栏折叠偏好（`REQ-0011`）。

## 5. UI / UE 约束

- MUST 使用 `admin-home.css` admin semantic token（`--admin-line`、`--admin-gold` 等）；**禁止**新增裸 Hex / rgba。
- 对 `REQ-0004-admin-home`、`REQ-0011-admin-sidebar-expand-collapse` 原型为 **MODIFIED**（padding / content max-width），**非**列宽或折叠交互变更。
- Prototype 优先级（`/req-complete`）：
  1. `prototype/web/admin-shell-padding-refine.html`
  2. `prototype/web/admin-shell-padding-refine-context.md`
  3. PNG Golden（1440 expanded、1920 expanded、collapsed SKU 示意、≤1023 一帧）
- 动画：侧栏 padding 变更 SHOULD 与现有 `--admin-sidebar-width` transition（220ms）协调；尊重 `prefers-reduced-motion`。

## 6. 依赖与实施顺序

| 依赖 | 说明 |
|------|------|
| **REQ-0004-admin-home** | 父需求；AdminLayout / admin-home.css 壳层 |
| **REQ-0011-admin-sidebar-expand-collapse** | collapsed 态与 72px 列宽；本 REQ 仅 MODIFIED padding |
| `docs/knowledge-base/best-practices/admin-list-page-consistency.md` | 用户管理为列表验收基准 |
| `rules/ui-design.md` | Token 与管理端视觉 |

**实际 OpenSpec change**：`fix-admin-content-padding-too-large`（来源 BUG-0054，已归档）。

## 7. 关联需求与缺陷

| ID | 关系 |
|---|---|
| REQ-0004-admin-home | 父需求；原 1080px / 18px padding 来源 |
| REQ-0011-admin-sidebar-expand-collapse | 侧栏宽与折叠；collapsed padding MODIFIED |
| BUG-0021-sidebar-menu-icons-indistinguishable | 并行；不在本 REQ 范围 |

## 8. 状态

```yaml
requirement_id: REQ-0013-admin-shell-padding-refine
priority: P1
status: done
iteration: sprint-004
owner: product
parent_requirement: REQ-0004-admin-home
openspec_change: fix-admin-content-padding-too-large
target_clients:
  web_admin: 本期
  web_catalog: 不涉及
  wechat_miniapp: 不涉及
```
