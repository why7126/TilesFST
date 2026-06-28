---
bug_id: BUG-0048-banner-modal-width-css-cascade-overridden
status: pending_review
created_at: 2026-06-28 18:42:00
updated_at: 2026-06-28 18:42:00
root_cause_type: code
---

# 根因分析

## 1. 直接原因

### 1.1 Banner 弹窗同时挂载 `modal-card` 与 `banner-modal-card`

`BannerFormModal.tsx` L311：

```tsx
className="modal-card banner-modal-card"
```

对比 `TileSkuFormModal.tsx` L342 仅使用 `className="sku-modal-card"`，**不**挂载通用 `modal-card` 类。Banner 弹窗因此同时命中两条等特异性宽度规则。

### 1.2 全局 `.admin-shell .modal-card { width: 520px }` 在 bundle 层叠中后于 880px 规则

多处 admin 样式重复定义通用 modal 宽度：

| 文件 | 选择器 | width |
|---|---|---|
| `user-management.css` L379 | `.admin-shell .modal-card` | 520px |
| `system-settings.css` L589 | `.admin-shell .modal-card` | 520px |
| `banner-management.css` L136 | `.admin-shell .banner-modal-card` | 880px |

`BannerManagementPage.tsx` 按序 import `user-management.css` → `banner-management.css`；但 SPA 生产 bundle 会合并各路由 CSS chunk，`system-settings.css`（及其他含 `.modal-card` 的 stylesheet）在 **全站 bundle 顺序上可能晚于** `banner-management.css`。当两条规则特异性均为 `(0, 2, 0)` 时，**后出现的** `.admin-shell .modal-card { width: 520px }` 覆盖 `.banner-modal-card { width: 880px }`。

DevTools 表现：元素 class 含 `modal-card banner-modal-card`，Computed `width` ≈ **520px**，生效规则来自 `.admin-shell .modal-card`。

### 1.3 Vitest 未覆盖运行时层叠结果

`BannerFormModal.test.tsx` L119–120 仅断言 `banner-management.css` **源文件**含 `880px` 字符串：

```typescript
expect(bannerCss).toMatch(/\.admin-shell \.banner-modal-card\s*\{[^}]*width:\s*880px/);
```

未在 import 完整 admin CSS 栈（含 `user-management.css` / `system-settings.css`）后断言 DOM Computed width，导致 BUG-0040 apply 阶段测试 pass 但浏览器仍 520px。

## 2. 根本原因

### 2.1 管理端 modal 宽度缺乏统一组件/类名约束

各 feature 分别定义 `.modal-card`（520px 通用）、`.sku-modal-card`（880px）、`.banner-modal-card`（880px）。Banner 弹窗沿用早期「modal-card + 页面专属后缀类」模式，而 SKU 已演进为 **单一专属类**，避免与全局 520px 冲突。

### 2.2 BUG-0040 修复仅改 CSS 数值，未消除类名冲突

`fix-banner-list-and-modal-ui` tasks 3.1 将 `.banner-modal-card` 从 640px 改为 880px，**未**移除冗余 `modal-card` 类，**未**验证生产 bundle 层叠顺序。修复停留在「源文件声明正确」，未闭环「运行时 Computed 正确」。

### 2.3 测试策略与验收基准 gap

BUG-0040 acceptance（AC-001/002）要求 Computed 880px 与 SKU 并排一致，但自动化测试降级为源 CSS regex，manual 验收在 apply 时未用 DevTools 核对 Computed，遗漏层叠问题。

## 3. 触发条件

满足以下条件 **100% 稳定复现**（local dev 与 Docker 构建产物均适用）：

1. 以 admin 登录 Web 管理端。
2. 生产/开发 bundle 已包含 `system-settings.css` 或任一晚于 `banner-management.css` 的 `.admin-shell .modal-card` 规则（典型 SPA 全站构建均满足）。
3. 打开 Banner 新增/编辑弹窗。
4. 视口宽度 ≥ 880px。

SKU 弹窗在同条件下仍为 880px（无 `modal-card` 类，不受 520px 规则影响）。

## 4. 分类结论

| 维度 | 结论 |
|---|---|
| 缺陷分类 | code / frontend-css（类名 + 层叠顺序） |
| 是否接口缺陷 | 否 |
| 是否数据库缺陷 | 否 |
| 是否权限缺陷 | 否 |
| 是否回归 | **是**（相对 BUG-0040 验收意图与 AC-001/002） |
| 主要修复面 | `BannerFormModal.tsx`（移除 `modal-card`）；可选 `.banner-modal-card` 特异性加固；Vitest 层叠断言 |
| 关联 BUG | BUG-0040（父项）、BUG-0033（加宽后滚动回归） |
| 建议 Change | `fix-banner-modal-width-css-cascade` 或并入 `fix-banner-list-and-modal-ui` 补修 |

## 5. 后续修复建议

1. **首选**：`BannerFormModal.tsx` 移除 `modal-card`，仅保留 `banner-modal-card`（对齐 `TileSkuFormModal` → `sku-modal-card` 模式）。
2. **可选加固**：`.admin-shell .modal-card.banner-modal-card { width: 880px }` 或统一 admin modal 宽度 token，避免多文件重复 `.modal-card`。
3. **测试**：Vitest import `user-management.css` + `system-settings.css` + `banner-management.css`，断言 `.banner-modal-card` Computed width 880px；或 `pnpm build` 后抽测 bundle。
4. **回归**：BUG-0033 滚动/footer/textarea；BUG-0040 AC-001～010 全部重验。
5. **不**重新 debate 640→880 策略（已由 BUG-0040 / delta spec 确立）。
