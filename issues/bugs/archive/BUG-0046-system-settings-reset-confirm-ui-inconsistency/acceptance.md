---
bug_id: BUG-0046-system-settings-reset-confirm-ui-inconsistency
status: pending_review
created_at: 2026-06-28 18:35:49
updated_at: 2026-06-28 18:35:49
related_requirement: REQ-0017-system-settings
related_bug: BUG-0037-tile-spec-status-confirm-ui-inconsistency
---

# 回归验收标准

> Golden Reference：`TileSpecManagementPage` / `TileCategoryManagementPage` 启停 confirm modal。修复 MUST NOT 回归 reset API 与 Tab 切换逻辑。

## AC-001 恢复默认 MUST 使用 DS confirm modal

**Given** `admin` 在 `/admin/settings/basic`  
**When** 点击「恢复默认」  
**Then** MUST NOT 调用 `window.confirm`  
**And** MUST 展示 `role="dialog"`、`aria-modal="true"` 的页面内 modal  
**And** 标题 MUST 含「恢复默认」语义  
**And** 正文 MUST 含「确定恢复该分组为默认配置吗？此操作不可撤销。」（或等价）  
**And** 底部 MUST 含「取消」与主按钮「确认恢复」

- [ ] AC-001

## AC-002 确认后 MUST 调用 reset API

**Given** 恢复默认 modal 已打开  
**When** 点击「确认恢复」  
**Then** MUST 调用 `POST /api/v1/admin/system-settings/{group}/reset`  
**And** 表单 MUST 刷新为默认值  
**And** MUST 展示成功提示

- [ ] AC-002

## AC-003 modal MUST 可取消且无副作用

**Given** 恢复默认 modal 已打开  
**When** 点击「取消」或遮罩  
**Then** modal MUST 关闭  
**And** MUST NOT 调用 reset API

- [ ] AC-003

## AC-004 dirty Tab 切换 MUST 使用 DS modal（SHOULD）

**Given** 表单 dirty  
**When** 点击其它 Tab  
**Then** SHOULD 使用同类 modal 替代 `window.confirm`  
**And** 取消 MUST 停留当前 Tab；确认 MUST 放弃修改并切换

- [ ] AC-004

## AC-005 视觉 MUST 对齐 Golden Reference

**Given** 修复完成  
**When** 对比系统设置 confirm 与瓷砖规格启停 modal  
**Then** MUST 使用 `modal-backdrop`、`btn`、`btn primary`  
**And** MUST NOT 新增裸 Hex

- [ ] AC-005

## AC-006 测试 MUST 覆盖 dialog

**Given** `/opsx-apply` 完成  
**When** vitest 触发恢复默认  
**Then** MUST 断言 dialog 可见  
**And** `window.confirm` MUST NOT 被调用

- [ ] AC-006
