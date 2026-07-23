---
bug_id: BUG-0074-prod-theme-preference-sync-toast-persistent
status: done
lifecycle_stage: archive
severity: medium
created_at: 2026-07-21 10:14:45
updated_at: 2026-07-22 08:59:01
lifecycle:
  captured: 2026-07-21 10:14:45
  generated: 2026-07-21 14:58:09
  completed: 2026-07-21 15:01:54
  reviewed: 2026-07-21 15:23:20
  approved: 2026-07-21 15:23:20
iteration: sprint-010
related_requirement: null
related_bug: null
related_change: fix-theme-preference-sync-toast-persistent
source_command: /capture
captured_via: capture
classification_rationale: 项目已有主题切换与账号偏好同步能力，生产环境提示“主题已在本机生效，但账号偏好同步失败，请稍后重试”且提示持续存在，属于既有偏好同步与 Toast 生命周期处理的行为偏差。
openspec_changes:
  - change_id: fix-theme-preference-sync-toast-persistent
    type: fix
    status: archived
related_bugs: []
---

```yaml
bug_id: BUG-0074-prod-theme-preference-sync-toast-persistent
status: done
severity: medium
lifecycle_stage: review
created_at: 2026-07-21 10:14:45
updated_at: 2026-07-21 15:32:13
lifecycle:
  captured: 2026-07-21 10:14:45
  generated: 2026-07-21 14:58:09
  completed: 2026-07-21 15:01:54
  reviewed: 2026-07-21 15:23:20
  approved: 2026-07-21 15:23:20
iteration: sprint-010
related_requirement: null
related_bug: null
related_change: fix-theme-preference-sync-toast-persistent
source_command: /capture
captured_via: capture
classification_rationale: 项目已有主题切换与账号偏好同步能力，生产环境提示“主题已在本机生效，但账号偏好同步失败，请稍后重试”且提示持续存在，属于既有偏好同步与 Toast 生命周期处理的行为偏差。
openspec_changes:
  - change_id: fix-theme-preference-sync-toast-persistent
    type: fix
    status: archived
related_bugs: []
scope:
  terminal: web
  environment: production
  module: theme_preference
  issue_type: preference_sync_failure_and_persistent_toast
readiness:
  capture: done
  bug: done
  root_cause: done
  workaround: done
  acceptance: done
  review: done
  trace: done
  next: opsx-apply
```

## 来源

| 类型 | ID / 路径 | 说明 |
|---|---|---|
| 用户反馈 | `/capture` | 生产环境主题切换后提示账号偏好同步失败，且提示一直存在 |

## 建议复现要点

| 要点 | 说明 |
|---|---|
| 账号状态 | 确认用户登录态、权限、Token 是否有效，是否仅特定账号复现 |
| 触发入口 | 确认发生在登录页、管理端 Shell、侧边栏主题选择器或其他主题切换入口 |
| 同步接口 | 记录账号偏好同步请求的 URL、HTTP 状态码、响应 JSON、错误码和请求耗时 |
| 前端状态 | 记录本地主题是否已写入 localStorage / 页面状态，失败后是否重复发起同步 |
| Toast 行为 | 确认提示是否设置自动关闭时长、是否可手动关闭、是否被持久化状态反复渲染 |
| 生产差异 | 对比本地/demo 与生产环境配置、API Base URL、鉴权 Cookie/Header、CORS 和网关响应 |

## 建议验收要点

| 验收点 | 说明 |
|---|---|
| 偏好同步成功 | 生产环境切换主题后账号偏好保存成功，刷新或重新登录后主题一致 |
| 失败提示可消失 | 同步失败时提示可自动消失或可关闭，不持续占据页面 |
| 本机回退明确 | 当仅本机主题生效时，提示文案明确且不阻断继续使用 |
| 重试不刷屏 | 多次切换或重试不会产生堆叠、常驻或重复错误提示 |
| 错误可诊断 | 同步失败时前端和后端日志能定位接口、错误码与账号上下文 |

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-22 08:56:33 | lifecycle-stage-migrate | review → archive（/opsx-archive fix-theme-preference-sync-toast-persistent） |
| 2026-07-22 08:56:09 | /opsx-archive | Change `fix-theme-preference-sync-toast-persistent` 已归档，状态同步完成。 |
| 2026-07-21 22:58:19 | /opsx-apply | Change `fix-theme-preference-sync-toast-persistent` apply 完成，待 archive。 |
| 2026-07-21 15:23:54 | lifecycle-stage-migrate | plan → review（/bug-review --approve） |
| 2026-07-21 10:14:45 | /capture | 记录生产环境主题偏好同步失败提示持续不消失缺陷 |
| 2026-07-21 14:58:09 | /bug-generate | 基于 capture 与 explore 结论生成 bug.md，状态更新为 draft |
| 2026-07-21 15:01:54 | /bug-complete | 补齐 root-cause、workaround、acceptance，状态更新为 pending_review |
| 2026-07-21 15:23:20 | /bug-review --approve | 评审通过，确认需要修复 |
| 2026-07-21 15:27:41 | /bug-opsx | 创建 OpenSpec Change `fix-theme-preference-sync-toast-persistent` |
| 2026-07-21 15:29:55 | workflow-sync-correction | BUG 尚未纳入 Sprint，保持 approved 状态并保留 Change 关联 |
| 2026-07-21 15:32:13 | /sprint-propose | 纳入 sprint-010 正式范围 |

- 2026-07-22 08:56:09 workflow-sync：状态同步为 done（Change archived）
