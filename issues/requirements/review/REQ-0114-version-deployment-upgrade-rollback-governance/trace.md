---
requirement_id: REQ-0114-version-deployment-upgrade-rollback-governance
status: in_sprint
lifecycle_stage: review
priority: P1
created_at: 2026-08-21 18:29:40
updated_at: 2026-08-21 22:13:10
---

# 需求追踪

## 基本信息

```yaml
requirement_id: REQ-0114-version-deployment-upgrade-rollback-governance
requirement_name: version-deployment-upgrade-rollback-governance
requirement_type: 发布治理 / 部署升级 / 回滚治理
priority: P1
status: in_sprint
owner: product
source: 用户反馈
target_clients:
  web_admin: 不涉及用户功能
  web_catalog: 不涉及
  wechat_miniapp: 不涉及
related_requirements:
  - REQ-0081-release-image-build-governance
  - REQ-0093-standardize-deployment-environment-matrix
related_changes:
  - add-version-deployment-upgrade-rollback-governance
lifecycle:
  captured: 2026-08-21 18:29:40
  generated: 2026-08-21 18:31:45
  completed: 2026-08-21 18:34:27
  reviewed: 2026-08-21 18:41:30
  approved: 2026-08-21 18:41:30
iteration: sprint-025
openspec_changes:
  - change_id: add-version-deployment-upgrade-rollback-governance
    type: add
    status: applied
readiness: Ready
readiness_notes: 已补齐 capture、requirement、user-stories、business-flow、acceptance 与 trace；本需求不涉及 UI prototype，knowledge-base gate 为 N/A。
knowledge_base_refs:
  - docs/knowledge-base/README.md
  - docs/knowledge-base/retrospectives/sprint-023-retrospective.md
  - docs/knowledge-base/retrospectives/sprint-024-retrospective.md
cross_cutting_tags:
  - release-governance
  - deployment
  - upgrade
  - rollback
  - database-migration
  - environment
documents:
  - capture.md
  - requirement.md
  - user-stories.md
  - business-flow.md
  - acceptance.md
  - review.md
expected_openspec_change: add-version-deployment-upgrade-rollback-governance
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-21 22:13:10 | /opsx-modify | Change `add-version-deployment-upgrade-rollback-governance` 验收返修已同步，待复验或 archive。 |
| 2026-08-21 19:11:55 | /opsx-apply | Change `add-version-deployment-upgrade-rollback-governance` apply 完成，待 archive。 |
| 2026-08-21 19:11:39 | /opsx-apply | Change `add-version-deployment-upgrade-rollback-governance` apply 进行中，待补齐剩余验收。 |
| 2026-08-21 18:48:30 | `/req-opsx` | 创建 OpenSpec Change `add-version-deployment-upgrade-rollback-governance`，回填 linked Change，待 `/opsx-apply` 实现 |
| 2026-08-21 18:43:30 | `/sprint-propose` | 纳入 sprint-025 正式范围，估算 L / 5 人天，待 `/req-opsx` 创建 OpenSpec Change |
| 2026-08-21 18:41:57 | lifecycle-stage-migrate | plan → review（/req-review） |
| 2026-08-21 18:41:30 | `/req-review` | 评审通过，确认需求范围、验收标准、优先级与非 UI 边界；准备迁入 review 阶段 |
| 2026-08-21 18:34:27 | `/req-complete` | 补齐 user-stories、business-flow、acceptance 与 trace；知识库判定为非 UI 治理需求，横切 AC 为 N/A；参考 sprint-023/024 复盘中治理命令需闭环、证据与中间态文案需防漂移的模式 |
| 2026-08-21 18:31:45 | `/req-generate` | 生成版本部署升级与回滚治理能力 PRD，状态更新为 draft |
| 2026-08-21 18:29:40 | `/req-capture` | 记录版本部署升级与回滚治理能力需求，范围覆盖版本事实源、首次部署、相邻升级/回滚、跨版本升级/回滚、env diff、DB 升级验证和回滚证据；暂不包含可视化平台 |

## 关联缺陷

| BUG | 严重等级 | 状态 | 关联 Change | 说明 |
|---|---|---|---|---|
