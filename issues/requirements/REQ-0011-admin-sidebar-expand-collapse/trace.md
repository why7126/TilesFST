---
requirement_id: REQ-0011-admin-sidebar-expand-collapse
status: done
priority: P1
created_at: 2026-06-27 10:19:43
updated_at: 2026-06-27 15:52:00
---

# 需求追踪

## 基本信息

```yaml
requirement_id: REQ-0011-admin-sidebar-expand-collapse
requirement_name: admin-sidebar-expand-collapse
requirement_type: 管理端 / 体验
priority: P1
status: done
owner: product
source: 竞品参考（SoulKing 侧边栏）
target_clients:
  web_admin: 本期
  web_catalog: 不涉及
  wechat_miniapp: 不涉及
related_requirements:
  - REQ-0010-product-version-display
  - REQ-0004-admin-home
prototype:
  web:
    - prototype/web/admin-sidebar-expanded.html
    - prototype/web/admin-sidebar-collapsed.html
    - prototype/web/admin-sidebar-collapse-context.md
    - prototype/web/images/admin-sidebar-expanded.png  # 待导出
    - prototype/web/images/admin-sidebar-collapsed.png  # 待导出
lifecycle:
  captured: 2026-06-27 10:19:43
  generated: 2026-06-27 10:22:49
  completed: 2026-06-27 10:25:49
  reviewed: 2026-06-27 10:45:07
  approved: 2026-06-27 10:45:07
iteration: sprint-002
openspec_changes:
  - change_id: add-admin-sidebar-collapse
    type: add
    status: archived
readiness: Partially Ready  # HTML 原型齐；PNG Golden Reference 待导出（非阻塞）```

## 变更记录

| 日期 | 动作 | 说明 |
|---|---|---|
| 2026-06-27 10:19:43 | `/req-capture` | 创建 capture.md 与 trace 壳；status → captured |
| 2026-06-27 10:22:49 | `/req-generate` | 生成 requirement.md；纳入 explore 结论；status → draft |
| 2026-06-27 10:25:49 | `/req-complete` | 补齐六件套与 prototype/web；status → pending_review |
| 2026-06-27 10:45:07 | `/req-review --approve` | 创建 review.md；status → approved |
| 2026-06-27 10:55:42 | `/req-opsx` | 创建 OpenSpec `add-admin-sidebar-collapse`（proposal/design/specs/tasks） |
| 2026-06-27 11:02:00 | `/sprint-propose sprint-002` | 纳入 sprint-002 正式范围 |
| 2026-06-27 11:03:00 | `/opsx-apply` | 实现侧栏折叠；vitest 78 passed；待 `/opsx-archive` |

## 文档清单

| 文档 | 状态 |
|---|---|
| capture.md | ✓ |
| requirement.md | ✓ |
| user-stories.md | ✓ |
| business-flow.md | ✓ |
| acceptance.md | ✓ |
| prototype/web/*.html + context.md | ✓ |
| prototype/web/images/*.png | 待导出（非阻塞） |
| review.md | ✓ approved |
- 2026-06-27 11:06:05 workflow-sync：状态同步为 done（Change archived）
