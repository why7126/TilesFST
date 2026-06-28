---
bug_id: BUG-0022-profile-basic-info-redundant-role-status
title: 个人资料基础资料区所属角色与账号状态与账号安全卡片重复
severity: low
status: draft
owner: product
discovered_at: 2026-06-28 12:37:33
environment: local|docker
related_requirement: REQ-0014-profile-page
related_change: null
related_bug: BUG-0023-profile-duplicate-save-buttons
---

# 缺陷说明

Web 管理端「个人资料」页（`/admin/profile`）的「基础资料」表单内展示了只读字段「所属角色」「账号状态」，而右侧「账号安全」卡片已以 badge / info-row 形式展示相同信息，造成同一页信息重复、表单区域冗余。

> **Scope 说明**：本 BUG 聚焦 **移除基础资料表单内的角色/状态只读字段**；身份条摘要（角色 meta、mini-badge）与 card-head「账号正常」badge 不在本 BUG 范围；账号安全卡片 MUST 继续展示角色与状态（AC-022）。

> **UX 定稿（2026-06-28）**：探索结论已采纳；REQ-0014 **AC-011 MODIFIED**——角色/状态仅在账号安全卡片展示。`ProfilePage.tsx` 已移除 `profile-role`、`profile-status` 表单字段；prototype 与 OpenSpec 已同步。

# 复现步骤

1. 以 `admin` 或 `employee` 登录 Web 管理端（`http://localhost:3000` 或 `http://localhost:5173`）。
2. 通过侧栏用户菜单进入「个人资料」页（`/admin/profile`）。
3. 观察左侧「基础资料」`profile-form-grid` 与右侧「账号安全」`side-card` 内容。
4. （修复前）表单内可见「所属角色」「账号状态」只读 input，与账号安全卡片信息重复。

# 期望结果

- 「所属角色」「账号状态」**MUST** 仅在「账号安全」卡片展示（含状态 badge）。
- 「基础资料」表单 **MUST** 仅含：用户名（只读）、昵称、联系邮箱、手机、备注。
- **MUST NOT** 在 `profile-form-grid` 内重复渲染角色/状态只读字段。
- 视觉 **MUST** 继续使用 semantic token，无裸 Hex。

# 实际结果

- （修复前）`ProfilePage.tsx` 在表单 grid 内渲染 `profile-role`、`profile-status` 只读 input（约 L289–296）。
- 同页「账号安全」卡片已展示 `账号状态` badge 与 `所属角色`（约 L351–360）。
- 用户标注红框区域为重复内容；REQ-0014 原 AC-011 曾要求表单内也含上述只读字段，与 UX 反馈冲突。

# 影响范围

| 范围 | 影响 |
|---|---|
| Web 管理端 `/admin/profile` | 信息重复、表单冗长；功能与 PATCH 不受影响 |
| `admin` / `employee` 角色 | 均受影响（页面共用） |
| REQ-0014 验收 | AC-011 已 MODIFIED；AC-022 仍为角色/状态唯一结构化展示区 |
| 后端 / API / 数据库 / Orval | 无 |
| 店主端 / 小程序 | 无 |

**与 REQ-0014 / 已归档 Change 关系**

| 项 | 说明 |
|---|---|
| REQ-0014 | 原 FR-004 / AC-011 要求表单内含角色/状态只读字段 |
| `add-admin-profile-page` | 已归档（2026-06-28）；按原 spec 实现双区展示 |
| UX 定稿 | BUG-0022 采纳；`acceptance.md`、`profile-page.html`、`openspec/specs/admin-profile-page/spec.md` 已 MODIFIED |
| BUG-0023 | 同页重复「保存修改」按钮；建议同 `fix-profile-page-ux-refine` change |
| 本 BUG | 交付后 UX 反馈，非功能回归 |

# 严重等级说明

严重程度为 `low`。

理由：

- **不阻塞核心功能**：只读展示重复，不影响编辑、保存或权限。
- **100% 稳定复现**（修复前）：访问页面即见，与账号/数据无关。
- **影响限于 UX / 信息架构**：降低表单聚焦度，略增阅读负担。
- **修复面小**：前端 `ProfilePage.tsx` + REQ/prototype delta；无 API/DB 变更。

# 代码线索

| 线索 | 路径 |
|---|---|
| 表单内角色/状态字段（已移除） | `src/web/src/pages/admin/ProfilePage.tsx` |
| 账号安全卡片（保留） | 同文件 `side-card` info-list |
| 单元测试 | `src/web/src/pages/admin/ProfilePage.test.tsx` |
| 样式 | `src/web/src/features/admin/styles/profile-page.css` |
| 关联需求 | `issues/requirements/archive/REQ-0014-profile-page/` |
| 关联 BUG | `issues/bugs/archive/BUG-0023-profile-duplicate-save-buttons/` |
| OpenSpec | `openspec/specs/admin-profile-page/spec.md`（Scenario 表单字段与只读规则） |
| 建议 Change | `fix-profile-page-ux-refine`（可与 BUG-0023 合并） |

# 分类结论

| 判断 | 结论 |
|---|---|
| 需求 vs 缺陷 | 缺陷（REQ-0014 交付后的 UX polish，非新能力 REQ） |
| 根因类型 | 前端 UI 按原 PRD/原型双区展示角色/状态，未收敛为单区 |
| 是否回归 | 否（自 `add-admin-profile-page` 起即存在重复） |
| 建议修复 Change | `fix-profile-page-ux-refine` |
