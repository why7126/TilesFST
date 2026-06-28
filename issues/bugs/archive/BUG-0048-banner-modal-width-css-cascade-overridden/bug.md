---
bug_id: BUG-0048-banner-modal-width-css-cascade-overridden
title: Banner弹窗880px样式被modal-card全局规则层叠覆盖
severity: medium
status: approved
owner: product
discovered_at: 2026-06-28 18:10:30
environment: local|docker
related_requirement: REQ-0016-banner-management
related_change: fix-banner-list-and-modal-ui
related_bug: BUG-0040-banner-modal-width-too-narrow
---

# 缺陷说明

BUG-0040 在 `fix-banner-list-and-modal-ui` 中已将 `.banner-modal-card` 宽度改为 **880px**，但 Banner 新增/编辑弹窗在浏览器中 **Computed width 仍约 520px**，与瓷砖 SKU 弹窗（880px）并排对比明显偏窄。源 CSS 已声明 880px，样式未生效的根因是 **CSS 层叠**：`BannerFormModal` 同时挂载 `modal-card` 与 `banner-modal-card` 两个类名，生产 bundle 中较晚出现的 `.admin-shell .modal-card { width: 520px }`（来自 `system-settings.css` / `user-management.css`）覆盖了 `.banner-modal-card` 的 880px 规则。SKU 弹窗仅使用 `sku-modal-card`，无此冲突。

本缺陷为 **BUG-0040 修复未闭环的回归**，非新的宽度策略变更；880px 目标与 BUG-0040 / `web-client` delta spec 一致。

# 复现步骤

1. 以 admin 登录 Web 管理端（本地 dev `5173` 或 Docker `3000`）。
2. 进入「Banner 管理」，点击「新增 Banner」或某行「编辑」，打开弹窗。
3. DevTools 选中 `.banner-modal-card`，查看 Computed → `width`（约 **520px**，非 880px）。
4. 进入「瓷砖 SKU 管理」，打开新增/编辑弹窗，对比 `.sku-modal-card` 的 `width`（**880px**）。
5. 可选：在 Styles 面板确认 `.admin-shell .modal-card` 的 `width: 520px` 为生效规则。

# 期望结果

- Banner 弹窗外卡片 Computed `width` 为 **880px**（`max-width: 100%` 在窄视口下保留）。
- 与 SKU 弹窗并排视觉一致，横向空间满足双列表单、图片上传、SKU 图库选图等字段布局。
- BUG-0033 已验收的滚动、头/尾固定、底栏等行为 **MUST NOT** 退化。
- Vitest / 构建产物层叠断言 **MUST** 覆盖「全 bundle 生效宽度」，而非仅断言源 CSS 文件含 880px 字符串。

# 实际结果

- `BannerFormModal.tsx` L311：`className="modal-card banner-modal-card"`（双类名）。
- `banner-management.css` L136–147 已声明：

```css
.admin-shell .banner-modal-card {
  width: 880px;
  max-width: 100%;
  ...
}
```

- 生产 CSS bundle 层叠顺序下，`.admin-shell .modal-card { width: 520px }`（`system-settings.css` L589、`user-management.css` L379）后于或与 `.banner-modal-card` 同特异性时覆盖宽度。
- 浏览器 Computed width ≈ **520px**；用户感知 Banner 弹窗仍明显窄于 SKU 弹窗。
- `BannerFormModal.test.tsx` 当前仅断言 `banner-management.css` 源文件含 880px，**未**覆盖 bundle 层叠结果。

# 影响范围

| 范围 | 影响 |
|---|---|
| Web 管理端 / Banner 弹窗 | 新增、编辑弹窗实际宽度仍为 520px，横向布局偏紧 |
| BUG-0040 验收 | 880px 修复意图未在运行时生效，属回归 |
| OpenSpec | `fix-banner-list-and-modal-ui` 待补修后 archive；无需重新 debate 640→880 策略 |
| Vitest | 需补充层叠/构建宽度断言，防止同类回归 |
| 关联 BUG | BUG-0040（父项）、BUG-0033（加宽后须回归滚动） |
| 关联 Change | `fix-banner-list-and-modal-ui`（in progress）；建议 follow-up `fix-banner-modal-width-css-cascade` |

不影响 API、SQLite、权限、小程序或店主端。

# 严重等级说明

严重程度为 `medium`。

理由：

- **不阻断功能**：弹窗可打开、保存、取消；主要为宽度与跨页弹窗一致性未达成。
- **100% 稳定复现**：凡 bundle 含 `system-settings.css` 或 `user-management.css` 的 `.modal-card` 规则即触发。
- **回归性质**：BUG-0040 已 approved 并部分实现，运行时未达验收意图。
- **修复面小**：移除冗余 `modal-card` 类、提高 `.banner-modal-card` 特异性，或统一 modal 宽度 token；工作量低于原始策略变更。

# 代码线索

| 线索 | 路径 |
|---|---|
| Banner 弹窗组件（双类名） | `src/web/src/features/admin/components/BannerFormModal.tsx` L311 |
| Banner 880px 声明 | `src/web/src/features/admin/styles/banner-management.css` L136–147 |
| 覆盖源 modal-card 520px | `src/web/src/features/admin/styles/system-settings.css` L589；`user-management.css` L379 |
| SKU 弹窗参考（无冲突） | `src/web/src/features/admin/styles/tile-sku-management.css` → `.sku-modal-card` |
| 现有测试（仅源 CSS） | `src/web/src/features/admin/components/BannerFormModal.test.tsx` L120 |
| 父缺陷 | `issues/bugs/archive/BUG-0040-banner-modal-width-too-narrow/` |
| 建议 Change | `fix-banner-modal-width-css-cascade` |

# 分类结论

| 判断 | 结论 |
|---|---|
| 需求 vs 缺陷 | 缺陷（BUG-0040 修复未闭环） |
| 根因类型 | frontend-css（双类名 + 全局 `.modal-card` 重复定义 + bundle 层叠顺序） |
| 是否回归 | 是（相对 BUG-0040 验收意图） |
| 建议修复 Change | `fix-banner-modal-width-css-cascade` 或并入 `fix-banner-list-and-modal-ui` 补修 |
