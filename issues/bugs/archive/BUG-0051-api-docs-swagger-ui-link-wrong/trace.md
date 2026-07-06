---
bug_id: BUG-0051-api-docs-swagger-ui-link-wrong
status: done
lifecycle_stage: archive
severity: high
created_at: 2026-07-01 09:09:32
updated_at: 2026-07-05 07:58:01
---

# 缺陷追踪

## 基本信息

```yaml
bug_id: BUG-0051-api-docs-swagger-ui-link-wrong
bug_name: api-docs-swagger-ui-link-wrong
severity: high
status: done
owner: product
source: 用户反馈
environment: local
target_clients:
  web_admin: 本期
  web_catalog: 不涉及
  wechat_miniapp: 不涉及
related_requirement: REQ-0022-admin-api-docs-menu
related_bug: null
related_changes: []
lifecycle:
  captured: 2026-07-01 09:09:32
  generated: 2026-07-01 09:23:51
  enriching: 2026-07-01 09:27:51
  completed: 2026-07-01 09:27:51
  pending_review: 2026-07-01 09:27:51
  reviewed: 2026-07-01 14:02:05
  approved: 2026-07-01 14:02:05
iteration: sprint-004
openspec_changes:
  - change_id: fix-api-docs-swagger-ui-link-wrong
    type: fix
    status: proposed
readiness: Ready
readiness_notes: 已完成 /bug-opsx、/opsx-apply 与 /opsx-archive；修复方向为 Web 层代理 Swagger。
documents:
  - capture.md
  - bug.md
  - root-cause.md
  - workaround.md
  - acceptance.md
  - review.md
expected_openspec_change: fix-api-docs-swagger-ui-link-wrong
```

## 变更记录

| 2026-07-01 20:25:33 | lifecycle-stage-migrate | review → archive（/opsx-archive fix-api-docs-swagger-ui-link-wrong） |
| 2026-07-01 14:02:35 | lifecycle-stage-migrate | plan → review（/bug-review --approve） |
| 日期 | 动作 | 说明 |
|---|---|---|
| 2026-07-01 09:09:32 | `/capture` | 记录接口文档页 Swagger UI 入口跳转错误 |
| 2026-07-01 09:23:51 | `/bug-generate` | 生成 bug.md，状态更新为 draft |
| 2026-07-01 09:27:51 | `/bug-complete` | 补齐根因分析、临时规避、验收标准，状态进入 pending_review |
| 2026-07-01 13:59:48 | 修复方向确认 | 确认使用 Web 层代理 Swagger，并更新 root-cause / acceptance |
| 2026-07-01 14:02:05 | `/bug-review --approve` | 评审通过，确认进入常规修复流程 |
| 2026-07-01 14:15:14 | `/sprint-propose BUG-0051 纳入 sprint-004` | 正式纳入 sprint-004；待 `/bug-opsx` 创建 `fix-api-docs-swagger-ui-link-wrong` |
| 2026-07-01 14:15:14 | `/bug-opsx BUG-0051` | 创建 OpenSpec Change `fix-api-docs-swagger-ui-link-wrong` |
- 2026-07-01 20:25:28 workflow-sync：状态同步为 done（Change archived）
