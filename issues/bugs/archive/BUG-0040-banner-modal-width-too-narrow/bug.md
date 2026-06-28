---
bug_id: BUG-0040-banner-modal-width-too-narrow
title: Banner弹窗宽度偏小未对齐SKU弹窗
severity: medium
status: approved
owner: product
discovered_at: 2026-06-28 17:28:15
environment: local|docker
related_requirement: REQ-0016-banner-management
related_change: null
---

# 缺陷说明

Web 管理端 Banner 新增/编辑弹窗（`BannerFormModal`）整体宽度为 **640px**（`.banner-modal-card { width: 640px }`），明显窄于瓷砖 SKU 弹窗的 **880px**（`.sku-modal-card`）。Banner 弹窗含双列表单、图片上传区、SKU 图库选图、有效期区间与运营备注等字段，在 640px 下横向空间偏紧，与管理端同类「复杂表单」弹窗（SKU）体验不一致。

当前 640px 按 REQ-0016 四套 `banner-management-modal-*.html` 与 `openspec/specs/web-client/spec.md`（`fix-banner-admin-ui` 归档）**有意交付**；BUG-0033 已在 640px 内修复滚动与 textarea 宽度。本缺陷诉求为 **管理端弹窗宽度统一**：对齐 SKU 弹窗 880px，属于 UX 策略变更，**与现行 spec「Banner 弹窗 MUST 640px」冲突**，修复须通过 `/bug-opsx` MODIFIED `web-client` delta spec。

# 复现步骤

1. 以 admin 或 employee 登录 Web 管理端（local `5173` 或 Docker `3000`）。
2. 进入「Banner 管理」→ 点击「+ 新增 Banner」或某行「编辑」，打开 Banner 弹窗。
3. 观察弹窗整体宽度与表单、图片区横向留白。
4. 进入「瓷砖 SKU 管理」→ 打开新增/编辑 SKU 弹窗。
5. 并排对比两弹窗宽度（约 640px vs 880px）。
6. 可选：对照 `banner-management-modal-sku-detail.html`（640px）与 `tile-sku-management` 原型 / `.sku-modal-card`（880px）。

# 期望结果

- Banner 弹窗宽度与 SKU 弹窗一致：**880px**（`max-width: 100%` 响应式保留）。
- 头/尾固定、`.modal-body` 可纵向滚动等行为保持（BUG-0033 验收不退化）。
- 双列 `banner-form-grid`、图片上传区、Combobox、有效期字段在加宽后有足够横向空间，视觉与 SKU 弹窗同属「管理端大表单」档位。
- `/bug-opsx` 后 `web-client` spec 更新为 880px（或「与 SKU 弹窗同宽」），acceptance 以 SKU 弹窗并排 + 功能回归为准；modal HTML/PNG Golden（640px）作为历史参考，由 delta 消化。

# 实际结果

- `banner-management.css`：

```css
.admin-shell .banner-modal-card {
  width: 640px;
  max-width: 100%;
  max-height: 92vh;
  ...
}
```

- `tile-sku-management.css` → `.sku-modal-card { width: 880px; ... }`。
- 用户感知 Banner 弹窗明显更窄、内容拥挤；与 capture.md 一致。

# 影响范围

| 范围 | 影响 |
|---|---|
| Web 管理端 / Banner 弹窗 | 新增、编辑弹窗宽度与横向布局 |
| OpenSpec | `openspec/specs/web-client/spec.md` Banner 弹窗宽度 MUST 640px → 需 MODIFIED |
| 原型验收 | 四套 `banner-management-modal-*.html` / PNG 为 640px；修复后 1440 并排验收基准改为与 SKU 弹窗对齐 |
| 关联 BUG | BUG-0033（640px 内溢出已修）；加宽后须回归滚动与底栏 |
| 关联 Change | `add-banner-management`、`fix-banner-admin-ui`（640px 为当时 spec） |
| 关联需求 | REQ-0016-banner-management |

不影响 API、SQLite、权限、小程序或店主端。

# 严重等级说明

严重程度为 `medium`。

理由：

- 不阻断保存/取消（BUG-0033 已修滚动）；主要为横向空间与跨页弹窗一致性。
- 变更涉及 **规范层**（640 → 880），非单纯 CSS 一行修改；须在 bug-review / bug-opsx 确认偏离 modal 原型的产品决策。
- 实现工作量小（主要为 CSS，可选对齐 `.sku-modal-card` 的 head/footer 规则）；可与 BUG-0039 合并为 `fix-banner-*` change。

# 代码线索

| 线索 | 路径 |
|---|---|
| Banner 弹窗组件 | `src/web/src/features/admin/components/BannerFormModal.tsx` |
| Banner 弹窗宽度 | `src/web/src/features/admin/styles/banner-management.css` → `.banner-modal-card` |
| SKU 弹窗宽度参考 | `src/web/src/features/admin/styles/tile-sku-management.css` → `.sku-modal-card` |
| 默认 modal 宽度 | `src/web/src/features/admin/styles/user-management.css` → `.modal-card`（520px） |
| 现行 spec | `openspec/specs/web-client/spec.md`（Banner 640px） |
| 弹窗原型（640px） | `issues/requirements/archive/REQ-0016-banner-management/prototype/web/banner-management-modal-*.html` |
| 弹窗测试 | `src/web/src/features/admin/components/BannerFormModal.test.tsx` |
