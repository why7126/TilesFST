---
requirement_id: REQ-0014-profile-page
status: done
lifecycle_stage: archive
priority: P1
created_at: 2026-06-28 09:36:56
updated_at: 2026-06-28 19:40:42
lifecycle:
  captured: 2026-06-28 09:36:56
  exploring: 2026-06-28 09:54:52
  generated: 2026-06-28 09:56:03
  completed: 2026-06-28 09:57:19
  reviewed: 2026-06-28 09:59:00
  approved: 2026-06-28 09:59:00
  amended: 2026-06-28 18:53:00
iteration: sprint-003
openspec_changes:
  - change_id: add-admin-profile-page
    type: add
    status: archived
  - change_id: fix-profile-activities-display-limit
    type: fix
    status: proposed
related_requirements:
  - REQ-0004-admin-home
  - REQ-0015-password-change
readiness: Ready
readiness_notes: v1 已交付；v1.1 操作记录 limit 5 文档已修订，待 fix-profile-activities-display-limit
expected_openspec_change: fix-profile-activities-display-limit
documents:
  - capture.md
  - requirement.md
  - user-stories.md
  - business-flow.md
  - acceptance.md
  - review.md
  - trace.md
  - prototype/web/profile-page.html
  - prototype/images/profile-page.png
  - prototype/web/profile-page-context.md
---

# 需求追踪

## 基本信息

```yaml
requirement_id: REQ-0014-profile-page
requirement_name: profile-page
requirement_type: 管理端 / 个人资料 self-service
priority: P1
status: done
owner: product
source: 反馈
target_clients:
  web_admin: 本期
  web_catalog: 不涉及
  wechat_miniapp: 不涉及
related_requirements:
  - REQ-0004-admin-home
  - REQ-0015-password-change
  - REQ-0005-user-management
related_changes:
  - add-admin-profile-page
  - fix-profile-activities-display-limit
requirement_version: v1.1
```

## PNG 并排验收（opsx-apply 阶段填写）

| 检查项 | prototype PNG | 实现截图 | 通过 |
|---|---|---|---|
| 全页布局 | profile-page.png | ProfilePage | ✓ |
| 用户菜单高亮 | profile-page.png | AdminUserMenu active | ✓ |
| save-tip inline | profile-page.png | .save-tip | ✓ |
| timeline | profile-page.png | activities API | ✓ |

## 变更记录

| 2026-06-28 19:23:05 | lifecycle-stage-migrate | review → archive（backfill opsx-archive hook (sprint-003)） |
| 日期 | 动作 | 说明 |
|---|---|---|
| 2026-06-28 19:11:39 | BUG 归档 | BUG-0049 rejected → archive（转 REQ-0014 v1.1） |
| 2026-06-28 18:57:00 | `/req-opsx` | 创建 `fix-profile-activities-display-limit`；status → proposed |
| 2026-06-28 18:53:00 | 需求修订 v1.1 | 操作记录展示/API 默认 limit 20→5；BUG-0049 驳回 |
| 2026-06-28 12:20:00 | `/opsx-archive` | change archived；admin-profile-page + auth/dashboard/web-client spec 已合并 |
| 2026-06-28 12:15:00 | `/sprint-apply` | add-admin-profile-page apply 完成；openspec status → applied |
| 2026-06-28 10:15:13 | lifecycle-stage-migrate | plan → review（/req-review --approve 补迁） |
| 2026-06-28 10:04:56 | `/sprint-propose` | 纳入 sprint-003；status → in_sprint |
| 2026-06-28 10:02:30 | `/req-opsx` | 创建 OpenSpec change `add-admin-profile-page` |
| 2026-06-28 09:59:00 | `/req-review` | 评审通过（REV-REQ-0014-001）；status → approved |
| 2026-06-28 09:57:19 | `/req-complete` | 补齐 user-stories、business-flow、acceptance；status → pending_review |
| 2026-06-28 09:56:03 | `/req-generate` | 生成 requirement.md v1；status → draft |
| 2026-06-28 09:54:52 | `/req-explore` | 操作记录拍板：完整审计（profile_activity_logs + activities API） |
| 2026-06-28 09:51:20 | `/req-explore` | 探索结论落盘；5 项决策确认；status → exploring |
| 2026-06-28 09:36:56 | `/req-capture` | 创建 capture.md 与 trace 壳；落盘 prototype HTML/PNG/context |

## 关联缺陷

| BUG | 严重等级 | 状态 | 关联 Change | 说明 |
|---|---|---|---|---|
| BUG-0022-profile-basic-info-redundant-role-status | low | done | fix-profile-basic-info-redundant-role-status | 个人资料基础资料区所属角色与账号状态与账号安全卡片重复 |
| BUG-0023-profile-duplicate-save-buttons | low | done | fix-profile-duplicate-save-buttons | 个人资料页页头与表单底部重复保存修改按钮 |
| BUG-0024-change-password-error-wrong-field | medium | done | fix-change-password-modal-errors | 修改密码弹窗新密码错误提示显示在原密码字段下方 |
| BUG-0025-change-password-toggle-button-misalignment | medium | done | fix-change-password-modal-errors | 修改密码弹窗错误提示出现后显示/隐藏按钮垂直错位 |
| BUG-0026-change-password-cancel-confirm-redundant | low | done | fix-change-password-modal-errors | 修改密码弹窗取消时出现多余浏览器二次确认 |
| BUG-0041-sidebar-user-menu-avatar-missing | medium | done | fix-sidebar-user-menu-avatar | 侧边栏底部用户菜单未显示用户头像 |
| BUG-0049-profile-recent-activities-limit-five | P1 | done | fix-profile-activities-display-limit | profile recent activities limit five |
