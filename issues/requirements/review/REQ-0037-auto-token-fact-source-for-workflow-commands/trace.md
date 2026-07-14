---
requirement_id: REQ-0037-auto-token-fact-source-for-workflow-commands
status: in_sprint
lifecycle_stage: review
priority: P1
created_at: 2026-07-12 09:52:06
updated_at: 2026-07-12 10:22:40
---

# 需求追踪

## 基本信息

```yaml
requirement_id: REQ-0037-auto-token-fact-source-for-workflow-commands
requirement_name: auto-token-fact-source-for-workflow-commands
requirement_type: Agent 工作流 / AI 使用量事实源自动化
priority: P1
status: in_sprint
owner: product
source: 用户输入
target_clients:
  web_admin: 不涉及
  web_catalog: 不涉及
  wechat_miniapp: 不涉及
  agent_workflow: 本期
related_requirements:
  - REQ-0034-ai-token-usage-observability
related_changes: []
lifecycle:
  captured: 2026-07-12 09:52:06
  generated: 2026-07-12 09:54:10
  completed: 2026-07-12 09:56:48
  reviewed: 2026-07-12 09:59:37
  approved: 2026-07-12 09:59:37
iteration: sprint-007
openspec_changes:
  - change_id: add-auto-token-fact-source-for-workflow-commands
    type: add
    status: applied
knowledge_base_refs:
  - docs/knowledge-base/README.md
  - docs/knowledge-base/retrospectives/sprint-006-retrospective.md
cross_cutting_tags: []
readiness: Ready
readiness_notes: 已评审通过；可进入 /req-opsx，后续 design.md 需明确统一 post-command hook 与 Workflow Sync 职责边界。
documents:
  - capture.md
  - requirement.md
  - user-stories.md
  - business-flow.md
  - acceptance.md
  - review.md
expected_openspec_change: add-auto-token-fact-source-for-workflow-commands
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-12 10:22:40 | /opsx-apply | Change `add-auto-token-fact-source-for-workflow-commands` apply 完成，待 archive。 |
| 2026-07-12 10:06:42 | /sprint-propose | 纳入 `sprint-007` 正式范围 |
| 2026-07-12 10:02:48 | /req-opsx | 创建 OpenSpec Change `add-auto-token-fact-source-for-workflow-commands` |
| 2026-07-12 10:00:27 | lifecycle-stage-migrate | plan → review（/req-review --approve） |
| 2026-07-12 09:59:37 | /req-review --approve | 评审通过；状态 pending_review → approved |
| 2026-07-12 09:56:48 | /req-complete | 补齐 user-stories、business-flow、acceptance；知识库判定为非 UI，引用 sprint-006 复盘中 AI usage snapshot 缺失导致 estimated fallback 的经验 |
| 2026-07-12 09:54:10 | /req-generate | 生成 requirement.md，状态 captured → draft |
| 2026-07-12 09:52:06 | /capture | 记录每个 /req-*、/bug-*、/opsx-*、/sprint-* 命令自动构建 Token 事实源的工作流增强需求 |

## 关联缺陷

| BUG | 严重等级 | 状态 | 关联 Change | 说明 |
|---|---|---|---|---|
