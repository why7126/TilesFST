---
requirement_id: REQ-0093-standardize-deployment-environment-matrix
status: done
priority: P1
created_at: 2026-08-03 10:44:00
updated_at: 2026-08-03 20:52:16
lifecycle_stage: archive
lifecycle:
  captured: 2026-08-03 10:44:00
  generated: 2026-08-03 13:39:30
  completed: 2026-08-03 18:31:16
  reviewed: 2026-08-03 18:37:18
  approved: 2026-08-03 18:37:18
iteration: sprint-018
openspec_changes:
  - change_id: standardize-deployment-environment-matrix
    type: update
    status: archived
related_requirements:
  - REQ-0081-release-image-build-governance
readiness: Ready
knowledge_base_gate: N/A
cross_cutting_tags: []
knowledge_base_refs:
  - docs/knowledge-base/README.md
  - docs/knowledge-base/retrospectives/sprint-017-retrospective.md
---

# REQ Trace

```yaml
requirement_id: REQ-0093-standardize-deployment-environment-matrix
status: done
priority: P1
created_at: 2026-08-03 10:44:00
updated_at: 2026-08-03 18:48:07
lifecycle_stage: review
lifecycle:
  captured: 2026-08-03 10:44:00
  generated: 2026-08-03 13:39:30
  completed: 2026-08-03 18:31:16
  reviewed: 2026-08-03 18:37:18
  approved: 2026-08-03 18:37:18
iteration: sprint-018
openspec_changes:
  - change_id: standardize-deployment-environment-matrix
    type: update
    status: archived
related_requirements:
  - REQ-0081-release-image-build-governance
readiness: Ready
knowledge_base_gate: N/A
cross_cutting_tags: []
knowledge_base_refs:
  - docs/knowledge-base/README.md
  - docs/knowledge-base/retrospectives/sprint-017-retrospective.md
```

## Readiness Report

| 项 | 结论 | 说明 |
|---|---|---|
| readiness | Ready | requirement、user-stories、business-flow、acceptance、trace 齐全；本需求不涉及 UI prototype。 |
| knowledge-base gate | N/A | 本需求为部署治理 / 目录治理 / 命令脚本能力，不命中 admin-list、admin-form、admin-modal、media-upload UI 标签。 |
| cross-cutting tags | — | 无 UI 横切 AC。 |
| prototype | N/A | 不新增 Web 管理端、店主 Web 或小程序 UI。 |

## Knowledge-base Cross-cutting Report

| 标签 | 引用文档 | 写入 acceptance 的 AC 条数 |
|---|---|---:|
| 无 UI 标签 | docs/knowledge-base/README.md | 0 |
| retrospective | docs/knowledge-base/retrospectives/sprint-017-retrospective.md | 0 |

复盘摘要：Sprint 017 复盘强调治理型需求应减少后续高风险阶段重复读取和集中返工，发布、归档、镜像与目录类能力应使用 summary-first、明确门禁和脚本化校验。本需求已将部署环境矩阵、目录结构校验、env 安全边界、Compose input hash 与发布镜像治理兼容写入验收标准。

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-03 20:47:08 | lifecycle-stage-migrate | review → archive（/opsx-archive standardize-deployment-environment-matrix） |
| 2026-08-03 20:46:44 | /opsx-archive | Change `standardize-deployment-environment-matrix` 已归档，状态同步完成。 |
| 2026-08-03 20:39:29 | /opsx-modify | Change `standardize-deployment-environment-matrix` 验收返修已同步；后续已完成归档。 |
| 2026-08-03 19:06:16 | /opsx-apply | Change `standardize-deployment-environment-matrix` apply 完成；后续已完成归档。 |
| 2026-08-03 18:48:07 | `/sprint-propose sprint-018` | REQ-0093 与 Change `standardize-deployment-environment-matrix` 纳入 sprint-018 正式范围；后续已完成归档。 |
| 2026-08-03 18:44:15 | `/req-opsx` | REQ 当时尚未纳入 Sprint，已保留 Change 关联；后续已纳入 sprint-018 并归档。 |
| 2026-08-03 18:42:44 | `/req-opsx` | 确认 REQ 尚未纳入 Sprint，保持 approved 状态；Change `standardize-deployment-environment-matrix` 已关联。 |
| 2026-08-03 18:43:20 | `/req-opsx` | 创建 OpenSpec Change `standardize-deployment-environment-matrix`；后续已纳入 sprint-018 并归档。 |
| 2026-08-03 18:37:46 | lifecycle-stage-migrate | plan → review（/req-review --approve） |
| 2026-08-03 18:37:18 | `/req-review --approve` | 评审通过，状态推进为 approved；准备从 plan 阶段迁移到 review 阶段。 |
| 2026-08-03 18:31:16 | `/req-complete` | 补齐 user-stories、business-flow、acceptance 与 trace 扩展；状态推进为 pending_review；Knowledge-base gate 为 N/A。 |
| 2026-08-03 13:39:30 | `/req-generate` | 生成 requirement.md，状态推进为 draft。 |
| 2026-08-03 10:44:00 | `/req-capture` | 记录部署环境矩阵标准化与中期 `deploy/` 目录治理需求。 |

- 2026-08-03 20:46:44 workflow-sync：状态同步为 done（Change archived）
