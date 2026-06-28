---
bug_id: BUG-0047-system-settings-save-tip-layout-shift
title: 系统设置保存成功提示导致下方内容位移
severity: medium
status: pending_review
owner: product
discovered_at: 2026-06-28 17:53:48
environment: local|docker
related_requirement: REQ-0017-system-settings
related_change: add-system-settings
related_bug: BUG-0015-admin-list-status-tips-layout-shift
---

# 缺陷说明

「系统设置」页保存成功后，在 `summary-grid` 与 `settings-layout` 之间条件渲染 `settings-save-tip` 提示条。tip 插入文档流并带有 `margin-top` / `padding`，导致下方 Tab 导航、表单面板与底部操作区发生明显上下位移（layout shift）。与管理端列表页通过 `AdminLayout` + `AdminToast` 固定层展示状态提示、以及个人资料页通过 `.save-tip.is-hidden` 预留占位的模式不一致。

> **Scope 说明**：本 BUG 聚焦 **保存/恢复成功提示的展示方式**；不包含 error tip、dirty badge 或 PATCH 逻辑。

# 复现步骤

1. 以 `admin` 登录 Web 管理端。
2. 进入「系统设置 → 基础信息」（`/admin/settings/basic`）。
3. 修改「平台名称」等字段，点击「保存设置」（页头或底部均可）。
4. 观察保存成功提示出现时，下方 `settings-layout` 是否向下跳动。
5. 等待 tip 消失或切换 Tab 后，观察内容是否回弹。

# 期望结果

- 保存成功提示 **MUST** 采用与管理端其它页面一致的非推挤模式，例如：
  - **方案 A**：复用 `AdminLayout` 的 `AdminToast`（与品牌/用户/SKU 列表页一致）；或
  - **方案 B**：Profile 式 `.save-tip.is-hidden` 预留占位（始终占 DOM，空态 `visibility: hidden`）；或
  - **方案 C**：fixed overlay toast region。
- 提示出现/消失时 **MUST NOT** 导致主内容区 layout shift。
- 成功/失败文案语义 **MUST** 保持不变（如「设置已保存并立即生效」）。

# 实际结果

- L841：`{saveTip ? <div className="settings-save-tip">{saveTip}</div> : null}` 条件插入 DOM。
- `.settings-save-tip` 含 `margin-top: 12px; padding: 10px 14px`（`system-settings.css` L501–509）。
- 恢复默认成功亦设置 `saveTip`（L185），同样触发位移。

# 影响范围

| 范围 | 影响 |
|---|---|
| Web 管理端 `/admin/settings/*` | 保存/恢复后页面跳动，UX 不佳 |
| `admin` 角色 | 唯一可访问者 |
| REQ-0017 AC-012 | 原要求 inline save-tip 风格；与 BUG-0015 修复方向及用户反馈需 reconcile |
| OpenSpec | `add-system-settings` spec 要求 inline save-tip |
| 后端 / API / 数据库 | 无 |

**关联修复参考**

| 项 | 说明 |
|---|---|
| BUG-0015 | 管理端四列表页 status tips layout shift（已修复 → AdminToast） |
| BUG-0003 | 品牌页 save-tip 推挤（已修复） |
| ProfilePage | `.save-tip.is-hidden` 占位模式（`profile-page.css` L167–174） |
| AdminLayout | `AdminToast` + `.admin-toast-region` fixed 层 |

# 严重等级说明

严重程度为 `medium`。

理由：

- **不阻塞功能**：保存仍成功，tip 仍可见。
- **100% 稳定复现**：每次保存/恢复默认均触发。
- **影响 UX**：明显 layout shift，降低专业感；与全站 tip 模式不一致。
- **修复面中等**：CSS/组件结构调整 + 测试；可能需 OpenSpec MODIFIED 若放弃 inline tip。

# 代码线索

| 线索 | 路径 |
|---|---|
| 条件渲染 tip | `src/web/src/pages/admin/SystemSettingsPage.tsx`（L841, L211, L185） |
| tip 样式 | `src/web/src/features/admin/styles/system-settings.css`（L501–509） |
| AdminToast 参考 | `src/web/src/pages/admin/AdminLayout.tsx`、`AdminToast.tsx` |
| Profile 占位参考 | `src/web/src/pages/admin/ProfilePage.tsx`（L308） |
| 建议 Change | `fix-system-settings-save-tip-layout-shift` |

# 分类结论

| 判断 | 结论 |
|---|---|
| 需求 vs 缺陷 | 缺陷（交互与管理端惯例不一致） |
| 根因类型 | inline 条件渲染 tip 占文档流，无 reserved/fixed 层 |
| 是否回归 | 否 |
| 建议修复 Change | `fix-system-settings-save-tip-layout-shift` |
