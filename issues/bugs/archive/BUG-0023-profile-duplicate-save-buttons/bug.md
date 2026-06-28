---
bug_id: BUG-0023-profile-duplicate-save-buttons
title: 个人资料页页头与表单底部重复保存修改按钮
severity: low
status: draft
owner: product
discovered_at: 2026-06-28 12:37:33
environment: local|docker
related_requirement: REQ-0014-profile-page
related_change: null
related_bug: BUG-0022-profile-basic-info-redundant-role-status
---

# 缺陷说明

Web 管理端「个人资料」页（`/admin/profile`）同时存在两个功能相同的「保存修改」主按钮：页头 `profile-page-head` 右侧一处、基础资料表单底部 `profile-form-actions` 与「重置」并列一处。两按钮共用同一 `handleSave()` 与 disabled 逻辑，行为一致，但视觉与交互重复，用户认为多余。

> **Scope 说明**：本 BUG 聚焦 **重复 CTA 收敛为单入口**；不包含保存校验、PATCH 逻辑、inline save-tip、头像上传或账号安全卡片（已由 REQ-0014 / `add-admin-profile-page` 交付）。

# 复现步骤

1. 以 `admin` 或 `employee` 登录 Web 管理端（`http://localhost:3000` 或 `http://localhost:5173`）。
2. 进入「个人资料」页（`/admin/profile`）。
3. 观察页头操作区与「基础资料」卡片底部按钮组。
4. （可选）修改昵称后分别点击两处「保存修改」，均触发 PATCH 并在表单底部展示 inline save-tip。

# 期望结果

- 页面 **MUST** 仅保留一处主「保存修改」入口，避免重复 CTA。
- **建议**保留表单底部与「重置」并列的按钮（与 inline save-tip 同区）；移除页头重复按钮。
- 保留的按钮 **MUST** 维持现有校验、PATCH、disabled（上传中/提交中）与成功提示行为。
- 视觉 **MUST** 继续使用 semantic token（品牌金 `btn primary`），无裸 Hex。

# 实际结果

- 页头与表单底部各渲染一个「保存修改」按钮（`ProfilePage.tsx` 约 L194–201、L329–336）。
- 两按钮文案、样式、行为完全一致；用户需在两处相同 CTA 间选择，造成认知冗余。
- `ProfilePage.test.tsx` 使用 `getAllByRole('button', { name: '保存修改' })`，测试与实现均假设双按钮存在。

# 影响范围

| 范围 | 影响 |
|---|---|
| Web 管理端 `/admin/profile` | 重复主 CTA，UX 冗余；功能不受影响 |
| `admin` / `employee` 角色 | 均受影响（页面共用） |
| REQ-0014 验收 | AC-017 要求页头与卡片内按钮行为一致，未禁止双按钮；与用户反馈需 reconcile |
| 后端 / API / 数据库 / Orval | 无 |
| 店主端 / 小程序 | 无 |

**与 REQ-0014 / 已归档 Change 关系**

| 项 | 说明 |
|---|---|
| REQ-0014 | FR-003 **MAY** 在页头提供「保存修改」；原型 HTML 含双按钮 |
| `add-admin-profile-page` | 已归档（2026-06-28）；按原型与 AC-017 实现双按钮 |
| `profile-page-context.md` §5 | 仅列表单区「重置 + 保存修改」，未强调页头 CTA |
| BUG-0022 | 同页 UX 问题（基础资料区角色/状态重复）；建议同 change 一并修复 |
| 本 BUG | 交付后 UX 反馈，非功能回归 |

# 严重等级说明

严重程度为 `low`。

理由：

- **不阻塞核心功能**：任一按钮均可正常保存；无数据丢失或权限问题。
- **100% 稳定复现**：访问页面即见，与账号/数据无关。
- **影响限于 UX**：重复 CTA 增加视觉噪音，略降表单操作清晰度。
- **修复面小**：预计仅改 `ProfilePage.tsx`、`ProfilePage.test.tsx` 及 acceptance delta；无 API/DB 变更。

# 代码线索

| 线索 | 路径 |
|---|---|
| 页头保存按钮 | `src/web/src/pages/admin/ProfilePage.tsx`（L194–201） |
| 表单底部保存按钮 | 同文件（L329–336） |
| 共用保存逻辑 | 同文件 `handleSave()`（L121–151） |
| 单元测试 | `src/web/src/pages/admin/ProfilePage.test.tsx`（`getAllByRole`） |
| 样式 | `src/web/src/features/admin/styles/profile-page.css` |
| 关联需求 | `issues/requirements/archive/REQ-0014-profile-page/` |
| 关联 BUG | `issues/bugs/archive/BUG-0022-profile-basic-info-redundant-role-status/` |
| 建议 Change | `fix-profile-page-ux-refine`（可与 BUG-0022 合并） |

# 分类结论

| 判断 | 结论 |
|---|---|
| 需求 vs 缺陷 | 缺陷（REQ-0014 交付后的 UX polish，非新能力 REQ） |
| 根因类型 | 前端 UI 与 spec/原型对齐过度，未收敛为单 CTA |
| 是否回归 | 否（自 `add-admin-profile-page` 起即存在双按钮） |
| 建议修复 Change | `fix-profile-page-ux-refine` |
