---
bug_id: BUG-0022-profile-basic-info-redundant-role-status
status: pending_review
created_at: 2026-06-28 12:54:36
updated_at: 2026-06-28 12:54:36
root_cause_type: design
---

# 根因分析

## 1. 直接原因

### 1.1 表单 grid 内渲染角色/状态只读字段

`ProfilePage.tsx` 在 `profile-form-grid` 内为「所属角色」「账号状态」各渲染一个只读 `<input>`（`profile-role`、`profile-status`），与右侧「账号安全」卡片 info-list 展示相同数据。

### 1.2 账号安全卡片已承担权限/状态摘要职责

同页 `side-card` 已展示：登录账号、账号状态 badge、所属角色、最后登录。用户在同一视口内可见两套结构化只读字段，形成信息重复。

### 1.3 身份条与 card-head 进一步放大角色/状态可见度

身份条 `identity-meta` 含角色摘要、`mini-badge gold` 含角色；card-head 含「账号正常」状态 badge。表单内再列只读 input 为第四层重复（本 BUG 修复聚焦表单 grid，身份条/card-head 保留在 scope 外）。

## 2. 根本原因

### 2.1 REQ-0014 原 PRD / AC-011 要求表单内含角色/状态

`requirement.md` FR-004、`acceptance.md` AC-011 与 `profile-page-context.md` §5 均规定表单字段顺序含「所属角色（只读）」「账号状态（只读）」；同时 FR-005 / AC-022 要求账号安全卡片也展示相同信息。规格层面未禁止双区重复。

### 2.2 原型 HTML 双区并列展示

`profile-page.html` 表单 grid 与账号安全卡片均含角色/状态；`add-admin-profile-page` 按 HTML > PNG 优先级 CSS Port，忠实还原双区字段，未做信息架构收敛。

### 2.3 交付后 UX 反馈与 spec 冲突

页面功能验收通过后，用户反馈表单区冗余。产品采纳探索结论：角色/状态仅在账号安全卡片展示，MODIFIED AC-011 / FR-004 / OpenSpec `admin-profile-page` Scenario。

## 3. 触发条件

满足以下条件时可稳定复现（修复前）：

1. 以 `admin` 或 `employee` 登录 Web 管理端。
2. 访问 `/admin/profile`。
3. 观察「基础资料」表单与「账号安全」卡片：两处均可见所属角色、账号状态。

与账号数据、角色类型无关；任意有效 profile 均可复现。

## 4. 分类结论

| 维度 | 结论 |
|---|---|
| 缺陷分类 | design / frontend-ui（信息架构） |
| 是否接口缺陷 | 否 |
| 是否数据库缺陷 | 否 |
| 是否权限缺陷 | 否 |
| 是否回归 | 否（自 `add-admin-profile-page` 起即存在） |
| 主要修复面 | `ProfilePage.tsx`、REQ-0014 acceptance/prototype、OpenSpec delta |
| 关联需求 | REQ-0014 AC-011 MODIFIED、AC-022 不变 |
| 建议 Change | `fix-profile-page-ux-refine`（可与 BUG-0023 合并） |

## 5. 后续修复建议

1. 删除 `profile-form-grid` 内 `profile-role`、`profile-status` 两个 `field readonly` 块。
2. 保留账号安全卡片 `info-list` 中账号状态 badge 与所属角色。
3. 同步 MODIFIED：`REQ-0014/acceptance.md`、`requirement.md`、`profile-page.html`、`profile-page-context.md`、`openspec/specs/admin-profile-page/spec.md`。
4. `ProfilePage.test.tsx` 无需断言已移除字段；现有保存/重置/校验用例 MUST 仍通过。
5. 1440×1024 与 `profile-page.html` 并排验收表单字段顺序（无角色/状态 input）。
