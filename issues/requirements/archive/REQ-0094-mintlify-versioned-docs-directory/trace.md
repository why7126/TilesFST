---
requirement_id: REQ-0094-mintlify-versioned-docs-directory
status: done
priority: P1
created_at: 2026-08-03 13:15:49
updated_at: 2026-08-03 20:39:29
lifecycle_stage: archive
lifecycle:
  captured: 2026-08-03 13:15:49
  generated: 2026-08-03 18:14:00
  completed: 2026-08-03 18:30:03
  reviewed: 2026-08-03 18:38:56
  approved: 2026-08-03 18:38:56
iteration: sprint-018
openspec_changes:
  - change_id: add-mintlify-versioned-docs-site
    type: update
    status: archived
related_requirements:
  - REQ-0088-versioned-product-usage-docs
knowledge_base_refs:
  - docs/knowledge-base/README.md
  - docs/knowledge-base/retrospectives/sprint-017-retrospective.md
  - docs/02-deployment.md
  - rules/environment.md
  - rules/port-management.md
cross_cutting_tags: []
readiness: Ready
---

# REQ Trace

```yaml
requirement_id: REQ-0094-mintlify-versioned-docs-directory
status: done
priority: P1
created_at: 2026-08-03 13:15:49
updated_at: 2026-08-03 18:55:00
lifecycle_stage: review
lifecycle:
  captured: 2026-08-03 13:15:49
  generated: 2026-08-03 18:14:00
  completed: 2026-08-03 18:30:03
  reviewed: 2026-08-03 18:38:56
  approved: 2026-08-03 18:38:56
iteration: sprint-018
openspec_changes:
  - change_id: add-mintlify-versioned-docs-site
    type: update
    status: archived
related_requirements:
  - REQ-0088-versioned-product-usage-docs
knowledge_base_refs:
  - docs/knowledge-base/README.md
  - docs/knowledge-base/retrospectives/sprint-017-retrospective.md
  - docs/02-deployment.md
  - rules/environment.md
  - rules/port-management.md
cross_cutting_tags: []
readiness: Ready
```

## Readiness

| 项 | 状态 | 说明 |
|---|---|---|
| capture.md | ready | 已记录原始诉求和影响范围。 |
| requirement.md | ready | 已明确方案 B、release 快照、mintlify 站点目录和共享截图资产治理。 |
| user-stories.md | ready | 已覆盖公开读者、发布负责人、开发维护者、文档维护者、实施支持、评审者和部署人员。 |
| business-flow.md | ready | 已覆盖 release 快照到站点目录、共享截图、latest 指针、Docker Compose 文档站启动和异常流程。 |
| acceptance.md | ready | 已包含功能 AC、Docker Compose AC、非功能 AC、knowledge-base N/A 和验收回填块。 |
| prototype | N/A | 本 REQ 为文档站目录与发布治理，不涉及业务 UI 原型。 |

## Knowledge-base Cross-cutting Report

| 标签 | 引用文档 | 将写入 acceptance 的 AC 条数 |
|---|---|---|
| N/A | docs/knowledge-base/README.md；docs/knowledge-base/retrospectives/sprint-017-retrospective.md | 0 |

摘要：本 REQ 不命中 `admin-list`、`admin-form`、`admin-modal`、`media-upload` 横切标签；参考 sprint-017 复盘中 usage docs gate 的经验，保持 generate / skip / pending_confirmation 三态和发布文档“确认优先”原则。

## Deployment Governance Notes

- Mintlify 文档站服务应通过 `docs-site` 或等价 Docker Compose profile 启动，避免默认部署无条件增加服务。
- 新增服务端口必须遵守“容器内固定、宿主机可变”的端口策略，并通过 `.env.example` 变量维护。
- 若发布范围包含 Compose、Dockerfile 或文档站服务部署变更，必须同步部署文档和发布门禁，并评估是否需要镜像构建证据。

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-03 20:28:46 | lifecycle-stage-migrate | review → archive（/opsx-archive add-mintlify-versioned-docs-site） |
| 2026-08-03 20:28:27 | /opsx-archive | Change `add-mintlify-versioned-docs-site` 已归档，状态同步完成。 |
| 2026-08-03 19:12:12 | /opsx-modify | Change `add-mintlify-versioned-docs-site` 验收返修已同步，待复验或 archive。 |
| 2026-08-03 19:05:26 | /opsx-apply | Change `add-mintlify-versioned-docs-site` apply 完成，待 archive。 |
| 2026-08-03 18:39:25 | lifecycle-stage-migrate | plan → review（/req-review --approve） |
| 2026-08-03 13:15:49 | `/capture` | 记录 Mintlify 多版本产品文档目录与站点浏览需求。 |
| 2026-08-03 13:39:27 | `/req-generate` | 基于方案 B 生成 PRD：新增 `mintlify/` 文档站源目录，由 release 快照同步或投影到站点目录。 |
| 2026-08-03 18:14:00 | `/req-generate` | 更新 PRD：采纳 release manifest 引用截图、Mintlify 站点集中存放共享截图资产，并按内容 hash 跨版本复用。 |
| 2026-08-03 18:30:03 | `/req-complete` | 补齐 user-stories、business-flow、acceptance，扩写 trace readiness 与 knowledge-base refs，状态进入 pending_review。 |
| 2026-08-03 18:35:14 | `/req-complete` | 补充 Docker Compose 启动 Mintlify 文档站服务要求：使用可选 profile、端口变量、部署文档和发布门禁。 |
| 2026-08-03 18:38:56 | `/req-review --approve` | 评审通过，状态更新为 approved，允许后续 `/req-opsx` 或纳入 Sprint。 |
| 2026-08-03 18:45:22 | `/req-opsx` | 创建 OpenSpec Change `add-mintlify-versioned-docs-site`；后续已纳入 sprint-018 并归档。 |
| 2026-08-03 18:55:00 | `/sprint-propose sprint-018` | 纳入 `sprint-018` 正式范围，并关联 Change `add-mintlify-versioned-docs-site`。 |

- 2026-08-03 20:28:27 workflow-sync：状态同步为 done（Change archived）
