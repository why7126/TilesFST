---
bug_id: BUG-0046-system-settings-reset-confirm-ui-inconsistency
title: 系统设置恢复默认二次确认弹窗 UI 不一致
severity: medium
status: pending_review
owner: product
discovered_at: 2026-06-28 17:53:48
environment: local|docker
related_requirement: REQ-0017-system-settings
related_change: add-system-settings
related_bug: BUG-0037-tile-spec-status-confirm-ui-inconsistency
---

# 缺陷说明

「系统设置」页点击底部「恢复默认」时，二次确认使用浏览器原生 `window.confirm`，而非管理端其它页面采用的 Design System 确认弹窗（`modal-backdrop` + `.btn` / `.btn.primary`）。样式、层级与交互与品牌/用户/SKU/Banner/瓷砖规格等列表页状态变更确认不一致，破坏管理端 UI/UE 统一性。

同页 Tab 切换时在 dirty 态亦使用 `window.confirm`（放弃未保存修改），建议一并纳入本 BUG 修复范围。

> **Scope 说明**：本 BUG 聚焦 **确认交互 UI 对齐**；不包含 reset API 逻辑、审计写入或表单刷新行为。

# 复现步骤

1. 以 `admin` 登录 Web 管理端。
2. 进入「系统设置 → 基础信息」（`/admin/settings/basic`）。
3. 点击底部「恢复默认」按钮。
4. 观察弹出的是浏览器原生 confirm 对话框（非页面内 modal）。
5. （可选）修改字段后不保存，切换 Tab，观察 dirty 切换 confirm 亦为原生对话框。
6. 对比：瓷砖规格页启用/停用 → 页面内 `modal-backdrop` 确认弹窗。

# 期望结果

- 「恢复默认」**MUST** 使用与管理端一致的确认弹窗（标题、正文、取消/确认按钮、DS semantic token）。
- Tab 切换 dirty 放弃确认 **SHOULD** 使用同一 modal 模式（与 `BUG-0037` 修复模式一致）。
- **MUST NOT** 使用 `window.confirm` / `window.alert` 作为用户可见确认。
- 确认后 reset API 调用与表单刷新行为 **MUST** 保持不变。

# 实际结果

- `handleReset` 使用 `window.confirm('确定恢复该分组为默认配置吗？此操作不可撤销。')`（L176）。
- `handleTabChange` 使用 `window.confirm('有未保存的修改，确定放弃并切换分组吗？')`（L163）。
- 无 `modal-backdrop` 结构，无 DS 按钮样式。

# 影响范围

| 范围 | 影响 |
|---|---|
| Web 管理端 `/admin/settings/*` | 确认交互与全站不一致 |
| `admin` 角色 | 唯一可访问者 |
| REQ-0017 AC-011 | 要求「恢复默认」二次确认，未限定必须为 DS modal；与用户/项目惯例需 reconcile |
| 后端 / API / 数据库 | 无 |
| 店主端 / 小程序 | 无 |

**关联修复参考**

| 项 | 说明 |
|---|---|
| BUG-0037 | 瓷砖规格启用/停用/删除确认弹窗 UI 不一致（已修复） |
| BUG-0017 | 用户重置密码确认弹窗 UI 不一致（已修复） |
| 列表页模式 | `BrandManagementPage`、`TileSpecManagementPage` 等 inline modal |

# 严重等级说明

严重程度为 `medium`。

理由：

- **不阻塞功能**：confirm 仍可完成操作。
- **100% 稳定复现**：点击恢复默认或 dirty 切换 Tab 即触发。
- **影响 UX 一致性**：管理端 DS 统一性受损，用户感知明显。
- **修复面中等**：新增/复用 modal 状态与 JSX；更新 vitest（mock 不再依赖 `window.confirm`）。

# 代码线索

| 线索 | 路径 |
|---|---|
| 恢复默认 confirm | `src/web/src/pages/admin/SystemSettingsPage.tsx`（L175–195） |
| Tab 切换 confirm | 同文件（L161–167） |
| 参考 modal 实现 | `src/web/src/pages/admin/TileSpecManagementPage.tsx` |
| 样式 | `src/web/src/features/admin/styles/admin-home.css`（`.modal-backdrop`） |
| 建议 Change | `fix-system-settings-reset-confirm-ui` |

# 分类结论

| 判断 | 结论 |
|---|---|
| 需求 vs 缺陷 | 缺陷（UI/UE 与管理端惯例不一致） |
| 根因类型 | 实现时采用快捷 `window.confirm`，未 port DS modal |
| 是否回归 | 否 |
| 建议修复 Change | `fix-system-settings-reset-confirm-ui` |
