---
bug_id: BUG-0075-prod-admin-brand-banner-save-fails
status: done
lifecycle_stage: archive
severity: high
created_at: 2026-07-21 10:17:39
updated_at: 2026-07-22 09:00:17
lifecycle:
  captured: 2026-07-21 10:17:39
  generated: 2026-07-21 15:00:10
  completed: 2026-07-21 15:21:45
  reviewed: 2026-07-21 15:24:31
  approved: 2026-07-21 15:24:31
iteration: sprint-010
related_requirement: REQ-0062-admin-banner-placement-scope
related_bug: null
related_change: fix-prod-admin-brand-banner-save
source_command: /capture
captured_via: capture
classification_rationale: 项目已有 Web 管理端 Banner 配置与品牌类型投放能力，生产环境配置品牌类型 Banner 无法保存属于既有管理端 Banner 保存链路的行为偏差，倾向记录为 BUG。
openspec_changes:
  - change_id: fix-prod-admin-brand-banner-save
    type: fix
    status: archived
related_bugs: []
---

```yaml
bug_id: BUG-0075-prod-admin-brand-banner-save-fails
status: done
severity: high
lifecycle_stage: review
created_at: 2026-07-21 10:17:39
updated_at: 2026-07-21 15:38:16
lifecycle:
  captured: 2026-07-21 10:17:39
  generated: 2026-07-21 15:00:10
  completed: 2026-07-21 15:21:45
  reviewed: 2026-07-21 15:24:31
  approved: 2026-07-21 15:24:31
iteration: sprint-010
related_requirement: REQ-0062-admin-banner-placement-scope
related_bug: null
related_change: fix-prod-admin-brand-banner-save
source_command: /capture
captured_via: capture
classification_rationale: 项目已有 Web 管理端 Banner 配置与品牌类型投放能力，生产环境配置品牌类型 Banner 无法保存属于既有管理端 Banner 保存链路的行为偏差，倾向记录为 BUG。
openspec_changes:
  - change_id: fix-prod-admin-brand-banner-save
    type: fix
    status: archived
related_bugs: []
scope:
  terminal: admin_web
  environment: production
  module: banner_management
  banner_type: brand
  issue_type: save_failure
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
| 用户反馈 | `/capture` | 生产环境 Web 管理端配置品牌类型 Banner 无法保存 |

## 建议复现要点

| 要点 | 说明 |
|---|---|
| Banner 入口 | 确认发生在新建 Banner、编辑 Banner、上架/启用或保存草稿入口 |
| 配置字段 | 记录 Banner 类型、关联品牌、图片/媒体、排序、投放范围、状态、开始/结束时间等表单值 |
| 前端校验 | 确认保存按钮是否被禁用、表单是否出现字段错误、是否有未展示的校验失败 |
| Network 响应 | 记录保存接口 URL、HTTP 状态码、响应 JSON、错误码和请求 payload |
| 后端日志 | 对照 FastAPI 日志，确认是否为鉴权、Schema 校验、品牌 ID 不存在、枚举不匹配、数据库约束或 MinIO 媒体字段问题 |
| 生产差异 | 对比本地/demo 与生产环境数据、品牌记录、Banner 枚举配置、迁移状态和前后端版本 |

## 建议验收要点

| 验收点 | 说明 |
|---|---|
| 品牌类型可保存 | 生产环境中合法的品牌类型 Banner 可以新建和编辑保存成功 |
| 关联品牌有效 | 保存后关联品牌 ID、展示名称、跳转目标或投放范围正确持久化 |
| 错误提示明确 | 字段缺失、品牌不存在、媒体不合法等失败场景返回明确错误码和用户可理解提示 |
| 列表与展示一致 | 保存成功后管理端列表、详情和相关展示端读取到同一配置 |
| 回归覆盖 | 覆盖品牌类型与非品牌类型 Banner 的新增、编辑、启用/停用保存回归 |

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-22 08:59:23 | lifecycle-stage-migrate | review → archive（/opsx-archive fix-prod-admin-brand-banner-save） |
| 2026-07-22 08:59:01 | /opsx-archive | Change `fix-prod-admin-brand-banner-save` 已归档，状态同步完成。 |
| 2026-07-21 23:01:52 | /opsx-apply | Change `fix-prod-admin-brand-banner-save` apply 完成，待 archive。 |
| 2026-07-21 15:25:16 | lifecycle-stage-migrate | plan → review（/bug-review --approve） |
| 2026-07-21 15:28:51 | /bug-opsx BUG-0075 | 创建 OpenSpec Change `fix-prod-admin-brand-banner-save` |
| 2026-07-21 15:32:33 | workflow-sync-correction | BUG 尚未纳入 Sprint，保持 approved 状态并保留 Change 关联 |
| 2026-07-21 15:38:16 | /sprint-propose | 纳入 `sprint-010` 正式范围 |
| 2026-07-21 15:24:31 | /bug-review --approve | 评审通过，允许 bug-opsx 与纳入 Sprint 规划 |
| 2026-07-21 15:21:45 | /bug-complete | 补齐 root-cause、workaround、acceptance，状态推进为 pending_review |
| 2026-07-21 15:00:10 | /bug-generate | 生成正式 bug.md，状态推进为 draft |
| 2026-07-21 10:17:39 | /capture | 记录生产环境管理端品牌类型 Banner 配置无法保存缺陷 |

- 2026-07-22 08:59:01 workflow-sync：状态同步为 done（Change archived）
