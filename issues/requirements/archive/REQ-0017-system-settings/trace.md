---
requirement_id: REQ-0017-system-settings
status: done
lifecycle_stage: archive
priority: P1
created_at: 2026-06-28 11:06:12
updated_at: 2026-06-28 19:40:42
---

# 需求追踪

## 基本信息

```yaml
requirement_id: REQ-0017-system-settings
requirement_name: system-settings
requirement_type: 管理端 / 系统配置
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
  - REQ-0005-user-management
  - REQ-0012-object-storage-key-layout
  - REQ-0014-profile-page
  - REQ-0015-password-change
related_changes:
  - add-system-settings
lifecycle:
  captured: 2026-06-28 11:06:12
  exploring: 2026-06-28 11:15:38
  generated: 2026-06-28 11:17:13
  completed: 2026-06-28 11:18:24
  reviewed: 2026-06-28 11:26:02
  approved: 2026-06-28 11:26:02
iteration: sprint-003
openspec_changes:
  - change_id: add-system-settings
    type: add
    status: archived
readiness: Implemented (PNG Golden 待导出)
delivery_phases:
  P0: 路由 Shell + basic + media
  P1: security（P1b 登录锁定可选）
  P2: audit_logs + audit Tab
  P3: notification Tab（无真实发信）
documents:
  - capture.md
  - requirement.md
  - user-stories.md
  - business-flow.md
  - acceptance.md
  - trace.md
  - review.md
  - prototype/web/system-settings-basic.html
  - prototype/web/system-settings-basic-context.md
  - prototype/web/system-settings-security.html
  - prototype/web/system-settings-security-context.md
  - prototype/web/system-settings-media.html
  - prototype/web/system-settings-media-context.md
  - prototype/web/system-settings-notification.html
  - prototype/web/system-settings-notification-context.md
  - prototype/web/system-settings-audit.html
  - prototype/web/system-settings-audit-context.md
prototype_png_status: pending_export
expected_openspec_change: add-system-settings```

## 变更记录

| 2026-06-28 19:34:23 | lifecycle-stage-migrate | review → archive（/opsx-archive add-system-settings） |
| 2026-06-28 11:26:14 | lifecycle-stage-migrate | plan → review（/req-review --approve） |
| 日期 | 动作 | 说明 |
|---|---|---|
| 2026-06-28 19:11:39 | BUG 归档 | BUG-0044 done → archive（REQ-0017 权限已覆盖） |
| 2026-06-28 11:06:12 | `/req-capture` | 创建 capture.md 与 trace 壳 |
| 2026-06-28 11:15:38 | `/req-explore` | 写入 capture 探索结论；status → exploring |
| 2026-06-28 11:17:13 | `/req-generate` | 生成 requirement.md；status → draft |
| 2026-06-28 11:18:24 | `/req-complete` | 补齐 user-stories、business-flow、acceptance；修正 context 路径；status → pending_review |
| 2026-06-28 11:26:02 | `/req-review --approve` | 评审通过；status → approved |
| 2026-06-28 11:27:21 | `/req-opsx` | 创建 OpenSpec change `add-system-settings` |

## 原型 trace checklist（PNG 待导出）

| 分组 | HTML | PNG | Context | 实现 |
|---|---|---|---|---|
| 基础信息 | ✓ | 待导出 | ✓ | ✓ |
| 安全策略 | ✓ | 待导出 | ✓ | ✓ |
| 媒体与存储 | ✓ | 待导出 | ✓ | ✓ |
| 通知设置 | ✓ | 待导出 | ✓ | ✓ |
| 审计配置 | ✓ | 待导出 | ✓ | ✓ |

## 关联缺陷

| BUG | 严重等级 | 状态 | 关联 Change | 说明 |
|---|---|---|---|---|
| BUG-0042-system-settings-page-title-v2-suffix | low | done | fix-system-settings-page-title-v2-suffix | 系统设置页眉标多余 V2 后缀 |
| BUG-0043-system-settings-duplicate-save-buttons | low | done | fix-system-settings-duplicate-save-buttons | 系统设置页页头与底部重复保存设置按钮 |
| BUG-0044-system-settings-non-admin-access | P1 | done | add-system-settings | system settings non admin access |
| BUG-0045-system-settings-media-format-options-limited | medium | done | fix-system-settings-media-format-options | 系统设置媒体与存储图片/视频格式各仅 3 种 |
| BUG-0046-system-settings-reset-confirm-ui-inconsistency | medium | done | fix-system-settings-reset-confirm-ui | 系统设置恢复默认二次确认弹窗 UI 不一致 |
| BUG-0047-system-settings-save-tip-layout-shift | medium | done | fix-system-settings-save-tip-layout-shift | 系统设置保存成功提示导致下方内容位移 |

## Sprint / OpenSpec

- OpenSpec change：`add-system-settings`（status: in_progress，opsx-apply 完成 P0–P3）。
- 2026-06-28：`/opsx-apply add-system-settings` — 后端 8 pytest + 前端 3 vitest 通过。
- 2026-06-28 19:34:20 workflow-sync：状态同步为 done（Change archived）
