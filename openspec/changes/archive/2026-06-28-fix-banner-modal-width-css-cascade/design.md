## Context

- **BUG**: BUG-0048（medium，BUG-0040 follow-up 回归）
- **Related REQ**: `REQ-0016-banner-management`
- **Parent BUG / Change**: BUG-0040、`fix-banner-list-and-modal-ui`
- **Target files**: `BannerFormModal.tsx`；`BannerFormModal.test.tsx`；可选 `banner-management.css`

### 原型 / 验收优先级（MUST）

```text
1. issues/bugs/archive/BUG-0048-banner-modal-width-css-cascade-overridden/acceptance.md
2. DevTools Computed width + Styles 面板层叠（运行时真相）
3. TileSkuFormModal + .sku-modal-card（880px 对照）
4. openspec/changes/fix-banner-list-and-modal-ui/specs/web-client/spec.md（880px 策略）
5. rules/ui-design.md
```

## Bug Analysis Report

| 项 | 内容 |
|---|---|
| 现象 | 源 CSS 880px，浏览器 Computed ≈ 520px |
| 直接原因 | `className="modal-card banner-modal-card"` + `.admin-shell .modal-card { 520px }` 后于 bundle 覆盖 |
| 根因类型 | code / frontend-css |
| 对比 | SKU 仅用 `sku-modal-card`，无冲突 |
| 测试 gap | Vitest 仅断言 `banner-management.css` 源字符串 |

## Goals / Non-Goals

**Goals:**

- Banner 弹窗运行时 Computed width **880px**（视口 ≥ 880px）。
- 消除 `modal-card` 与 `banner-modal-card` 双类名层叠冲突。
- Vitest 覆盖完整 CSS 冲突栈。
- BUG-0033 滚动、textarea、footer 无回归。
- 闭环 BUG-0048 AC-001～AC-010。

**Non-Goals:**

- 重新 debate 640→880 策略（已由 BUG-0040 / `fix-banner-list-and-modal-ui` 确立）。
- API、Orval、数据库、权限变更。
- 全站统一 admin modal token 重构（可选后续 REQ）。
- 修改 `system-settings.css` / `user-management.css` 全局 `.modal-card`（除非移除 Banner 双类名不足）。

## Decisions

### D1：移除外层 `modal-card` 类（首选）

- **选择**：`BannerFormModal` 外层仅 `banner-modal-card`（对齐 `TileSkuFormModal` → `sku-modal-card`）。
- **理由**：最小 diff；根因即双类名命中 520px 规则；内部仍可用 `.modal-head` / `.modal-body` / `.modal-footer` 结构类。
- **备选**：保留双类名 + `.admin-shell .modal-card.banner-modal-card { width: 880px }` 提高特异性 — 仅在 D1 不足时采用。

### D2：Vitest 导入完整 CSS 栈

- import `user-management.css`、`system-settings.css`、`banner-management.css`（与生产 bundle 冲突源一致）。
- 断言 `.banner-modal-card` 在 `.admin-shell` 下渲染后宽度行为（`getComputedStyle` 或等价）。
- **禁止**仅 `expect(bannerCss).toMatch(/880px/)` 作为 pass 条件。

### D3：与 `fix-banner-list-and-modal-ui` 归档顺序

- 本 change **SHOULD** apply 并完成验收后，与 `fix-banner-list-and-modal-ui` **一并** archive（或本 change 先 apply，父 change 待 6.1 条件满足再 archive）。
- `fix-banner-list-and-modal-ui` tasks 6.1 **MUST NOT** 在 BUG-0048 未 pass 时勾选。

### D4：验收基准

- DevTools Computed `width` 880px + Banner vs SKU 并排。
- 不以源 CSS regex 或 640px modal PNG 为 pass gate。

## Risks / Trade-offs

| 风险 | 缓解 |
|---|---|
| 移除 `modal-card` 丢失通用 modal  padding/阴影 | `.banner-modal-card` 已定义完整卡片样式；对照 SKU |
| 其他页面 modal 仍 520px | 本 BUG 范围仅 Banner；不改动全局 |
| BUG-0033 回归 | AC-005 显式回归滚动/footer/textarea |
| 测试环境无 JSDOM computed style | 可断言 className 不含 `modal-card` + import CSS 顺序 smoke |

## Test Plan

- Vitest：`BannerFormModal.test.tsx` — 无 `modal-card` 双类名；完整 CSS 栈宽度断言。
- 手工：DevTools Computed 880px；Styles 面板确认非 `.modal-card` 520px 生效。
- 手工：Banner vs SKU 并排；四套 jump_type 滚动到底。
- `cd src/web && pnpm vitest run BannerFormModal && pnpm build`

## Migration Plan

1. Apply 代码与测试。
2. 验收 BUG-0048 AC + BUG-0033 回归。
3. 更新 change / BUG trace。
4. Archive 本 change；随后 archive `fix-banner-list-and-modal-ui`（若尚未）。

## Open Questions

（无 — review 已批准移除 `modal-card` 方案。）
