---
requirement_id: REQ-0015-password-change
status: done
lifecycle_stage: archive
priority: P1
created_at: 2026-06-28 09:41:12
updated_at: 2026-07-10 20:42:15
lifecycle:
  captured: 2026-06-28 09:41:12
  exploring: 2026-06-28 09:47:30
  generated: 2026-06-28 09:55:31
  completed: 2026-06-28 09:57:09
  reviewed: 2026-06-28 10:01:12
  approved: 2026-06-28 10:01:12
iteration: sprint-003
openspec_changes:
  - change_id: add-admin-password-change
    type: add
    status: archived
related_requirements:
  - REQ-0004-admin-home
  - REQ-0014-profile-page
  - REQ-0005-user-management
readiness: Ready
readiness_notes: 五件套 + prototype HTML/PNG/context 齐全
expected_openspec_change: add-admin-password-change
documents:
  - capture.md
  - requirement.md
  - user-stories.md
  - business-flow.md
  - acceptance.md
  - review.md
  - trace.md
  - prototype/web/password-change-modal.html
  - prototype/web/password-change-modal.png
  - prototype/web/password-change-modal-context.md
---

# 需求追踪

## 基本信息

```yaml
requirement_id: REQ-0015-password-change
requirement_name: password-change
requirement_type: 管理端 / 账号安全
priority: P1
status: done
owner: product
parent_requirement: REQ-0004-admin-home
target_clients:
  web_admin: 本期
  web_catalog: 不涉及
  wechat_miniapp: 不涉及
related_requirements:
  - REQ-0004-admin-home
  - REQ-0014-profile-page
  - REQ-0005-user-management
related_changes:
  - add-admin-password-change
readiness: Ready
expected_openspec_change: add-admin-password-change
iteration: sprint-003
```

## 原型验收 checklist

| 项 | 参考 | 状态 |
|----|------|------|
| HTML 结构 | `prototype/web/password-change-modal.html` | 待开发对照 |
| Golden PNG | `prototype/web/password-change-modal.png` | 待并排验收 |
| Context | `prototype/web/password-change-modal-context.md` §8 | 待勾选 |

## 变更记录

| 日期 | 动作 | 说明 |
|---|---|---|
| 2026-06-28 19:23:06 | lifecycle-stage-migrate | review → archive（backfill opsx-archive hook (sprint-003)） |
| 2026-06-28 10:15:13 | lifecycle-stage-migrate | plan → review（/req-review --approve 补迁） |
| 2026-06-28 10:06:30 | `/req-opsx` | 创建 OpenSpec change `add-admin-password-change` |
| 2026-06-28 10:03:15 | `/sprint-propose sprint-003` | 纳入 sprint-003；iteration → sprint-003；status → in_sprint |
| 2026-06-28 10:01:12 | `/req-review --approve` | review.md REV-REQ-0015-001；status → approved |
| 2026-06-28 09:57:09 | `/req-complete` | 补齐 user-stories、business-flow、acceptance；更新 prototype context；status → pending_review |
| 2026-06-28 09:55:31 | `/req-generate` | 生成 requirement.md（PRD）；status → draft |
| 2026-06-28 09:47:30 | `/req-explore` | 记录探索结论：API 路径、token_version 全端失效、限流/弱密码、共享弹窗策略 |
| 2026-06-28 09:41:12 | `/req-capture` | 创建 capture.md 与 trace 壳；落盘 prototype HTML/PNG/context |

## 关联缺陷

| BUG | 严重等级 | 状态 | 关联 Change | 说明 |
|---|---|---|---|---|
| BUG-0061-change-password-policy-error-message-unclear | medium | done | fix-change-password-policy-error-message | 修改密码安全策略错误提示不清晰 |
