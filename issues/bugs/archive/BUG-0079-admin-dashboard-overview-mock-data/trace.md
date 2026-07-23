---
bug_id: BUG-0079-admin-dashboard-overview-mock-data
status: done
lifecycle_stage: archive
severity: medium
created_at: 2026-07-22 08:21:05
updated_at: 2026-07-22 09:27:53
lifecycle:
  captured: 2026-07-22 08:21:05
  generated: 2026-07-22 08:22:46
  completed: 2026-07-22 08:26:46
  reviewed: 2026-07-22 08:28:57
  approved: 2026-07-22 08:28:57
iteration: sprint-010
related_requirement: null
related_bug: null
related_change: fix-admin-dashboard-overview-real-data
source_command: /capture
captured_via: capture
classification_rationale: 管理端首页数据概览属于已有展示能力，当前仍使用 Mock 数据而非真实业务数据，属于已交付能力与实际数据源接入预期不一致的缺陷。
openspec_changes:
  - change_id: fix-admin-dashboard-overview-real-data
    type: fix
    status: archived
related_bugs: []
---

```yaml
bug_id: BUG-0079-admin-dashboard-overview-mock-data
status: done
severity: medium
lifecycle_stage: review
created_at: 2026-07-22 08:21:05
updated_at: 2026-07-22 09:19:39
lifecycle:
  captured: 2026-07-22 08:21:05
  generated: 2026-07-22 08:22:46
  completed: 2026-07-22 08:26:46
  reviewed: 2026-07-22 08:28:57
  approved: 2026-07-22 08:28:57
iteration: sprint-010
related_requirement: null
related_bug: null
related_change: fix-admin-dashboard-overview-real-data
source_command: /capture
captured_via: capture
openspec_changes:
  - change_id: fix-admin-dashboard-overview-real-data
    type: fix
    status: archived
related_bugs: []
scope:
  terminal: admin
  environment: null
  page: dashboard_home
  module: overview_metrics
  issue_type: mock_data_not_replaced
readiness:
  capture: done
  bug: done
  root_cause: done
  workaround: done
  acceptance: done
  review: done
  trace: done
  next: opsx-archive
```

## 来源

| 类型 | ID / 路径 | 说明 |
|---|---|---|
| 用户反馈 | `/capture` | admin 管理端首页数据概览仍使用 Mock 数据，需要调整为真实数据 |

## 建议复现要点

| 要点 | 说明 |
|---|---|
| 页面范围 | 确认 admin 管理端首页数据概览的所有指标项，包括总量、增长、待办、趋势或快捷统计 |
| 数据来源 | 定位当前前端 Mock 常量、临时接口或 fallback 逻辑，并确认是否存在对应真实后端接口 |
| 数据一致性 | 与数据库、后端接口、管理端列表页统计结果进行交叉验证 |
| 空数据状态 | 验证无数据、部分数据缺失、接口失败时的展示策略 |
| 权限边界 | 确认首页概览不暴露越权数据，遵循管理端权限范围 |

## 建议验收要点

| 验收点 | 说明 |
|---|---|
| 数据真实 | 首页数据概览指标来自后端真实接口或真实业务聚合，不再依赖 Mock 常量 |
| 统计准确 | 各概览指标与对应业务表、接口或列表页统计口径一致 |
| 加载状态 | 页面具备清晰 loading、empty、error 展示，不以 Mock 数据兜底误导用户 |
| 权限正确 | 不同权限账号只能看到允许范围内的概览数据 |
| 回归范围 | 管理端首页、相关 API、列表页统计和 Docker Compose 本地环境完成必要回归 |

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-22 09:27:24 | lifecycle-stage-migrate | review → archive（/opsx-archive fix-admin-dashboard-overview-real-data） |
| 2026-07-22 09:27:04 | /opsx-archive | Change `fix-admin-dashboard-overview-real-data` 已归档，状态同步完成。 |
| 2026-07-22 09:20:45 | /opsx-apply | Change `fix-admin-dashboard-overview-real-data` apply 完成，待 archive。 |
| 2026-07-22 09:19:39 | /opsx-apply | 已实现真实 Dashboard 概览 API、Web 接入、OpenAPI/Orval、文档和回归测试 |
| 2026-07-22 09:01:58 | /sprint-propose | 纳入 sprint-010 正式范围 |
| 2026-07-22 08:35:05 | /bug-opsx | 创建 OpenSpec Change `fix-admin-dashboard-overview-real-data` |
| 2026-07-22 08:29:32 | lifecycle-stage-migrate | plan → review（/bug-review --approve） |
| 2026-07-22 08:28:57 | /bug-review --approve | 评审通过，允许进入 bug-opsx 与 Sprint 规划 |
| 2026-07-22 08:26:46 | /bug-complete | 补齐 root-cause、workaround、acceptance，状态推进为 pending_review |
| 2026-07-22 08:22:46 | /bug-generate | 生成缺陷正式说明 bug.md，状态推进为 draft |
| 2026-07-22 08:21:05 | /capture | 记录管理端首页数据概览仍使用 Mock 数据缺陷 |

- 2026-07-22 09:26:59 workflow-sync：状态同步为 done（Change archived）
