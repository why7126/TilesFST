---
bug_id: BUG-0043-system-settings-duplicate-save-buttons
title: 系统设置页页头与底部重复保存设置按钮
severity: low
status: pending_review
owner: product
discovered_at: 2026-06-28 17:53:48
environment: local|docker
related_requirement: REQ-0017-system-settings
related_change: add-system-settings
related_bug: BUG-0023-profile-duplicate-save-buttons
---

# 缺陷说明

Web 管理端「系统设置」页（`/admin/settings/*`）同时存在两个功能相同的「保存设置」主按钮：页头 `settings-hero-actions` 右侧一处、各 Tab 面板底部 `settings-panel-footer` 操作区一处。两按钮共用同一 `handleSave()` 与 disabled 逻辑（`saving || !dirty`），行为一致，但视觉与交互重复，用户认为页头按钮多余。

> **Scope 说明**：本 BUG 聚焦 **重复 CTA 收敛为单入口**；不包含 PATCH 逻辑、恢复默认、Tab 切换或 save-tip 行为（见 BUG-0047）。

# 复现步骤

1. 以 `admin` 登录 Web 管理端。
2. 进入「系统设置」任意 Tab（如 `/admin/settings/basic`）。
3. 修改任意可写字段，观察页头与底部均出现可点击的「保存设置」。
4. （可选）分别点击两处按钮，均触发 `patchSettingsGroup` 并展示 save-tip。

# 期望结果

- 页面 **MUST** 删除页头右侧「保存设置」，**MUST** 仅保留底部「取消 / 恢复默认 / 保存设置」操作区（与 BUG-0023 / `fix-profile-duplicate-save-buttons` 修复方向一致）。
- 保留的底部按钮 **MUST** 维持现有校验、PATCH、disabled 与成功提示行为。
- 页头 **MAY** 保留 dirty 态 `有未保存修改` badge。

# 实际结果

- 页头（L806–813）与 `SettingsFooter`（L93–103）各渲染一个「保存设置」按钮。
- `SystemSettingsPage.test.tsx` 使用 `getAllByRole('button', { name: '保存设置' })` 断言双按钮存在。

# 影响范围

| 范围 | 影响 |
|---|---|
| Web 管理端 `/admin/settings/*` | 重复主 CTA，UX 冗余；功能不受影响 |
| `admin` 角色 | 唯一可访问者 |
| REQ-0017 验收 | AC-009 要求页头与底部均提供「保存设置」；与用户反馈及 Profile 修复模式需 reconcile |
| OpenSpec | `add-system-settings` spec 明确要求双入口 |
| 后端 / API / 数据库 / Orval | 无 |

**与 REQ-0017 / 已归档 Change 关系**

| 项 | 说明 |
|---|---|
| REQ-0017 AC-009 | 页头与底部均提供「保存设置」 |
| `add-system-settings` | 按 spec 实现双按钮 |
| `fix-profile-duplicate-save-buttons` | 已归档；Profile 页已收敛为单入口 |
| BUG-0023 | 同类型 UX 问题，可互为参考 |
| 本 BUG | 交付后 UX 反馈，非功能回归 |

# 严重等级说明

严重程度为 `low`。

理由：

- **不阻塞核心功能**：任一按钮均可正常保存。
- **100% 稳定复现**：访问页面并 dirty 表单即见。
- **影响限于 UX**：重复 CTA 增加视觉噪音。
- **修复面小**：预计改 `SystemSettingsPage.tsx`、测试及 OpenSpec delta；无 API/DB 变更。

# 代码线索

| 线索 | 路径 |
|---|---|
| 页头保存按钮 | `src/web/src/pages/admin/SystemSettingsPage.tsx`（L804–814） |
| 底部保存按钮 | 同文件 `SettingsFooter`（L93–103） |
| 共用保存逻辑 | 同文件 `handleSave()`（L197–217） |
| 单元测试 | `src/web/src/pages/admin/SystemSettingsPage.test.tsx` |
| 建议 Change | `fix-system-settings-duplicate-save-buttons` |

# 分类结论

| 判断 | 结论 |
|---|---|
| 需求 vs 缺陷 | 缺陷（REQ-0017 交付后的 UX polish） |
| 根因类型 | 前端按 spec/原型实现双 CTA，未收敛为单入口 |
| 是否回归 | 否 |
| 建议修复 Change | `fix-system-settings-duplicate-save-buttons` |
