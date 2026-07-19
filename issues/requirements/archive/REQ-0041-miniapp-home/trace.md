---
requirement_id: REQ-0041-miniapp-home
status: done
priority: P1
created_at: 2026-07-16 09:09:51
updated_at: 2026-07-17 23:01:19
lifecycle:
  captured: 2026-07-16 09:09:51
  generated: 2026-07-16 09:20:59
  completed: 2026-07-16 09:24:44
  reviewed: 2026-07-16 09:40:45
  approved: 2026-07-16 09:40:45
iteration: sprint-008
openspec_changes:
  - change_id: add-miniapp-home
    type: add
    status: archived
related_requirements: []
knowledge_base_refs:
  - docs/knowledge-base/retrospectives/sprint-007-retrospective.md
cross_cutting_tags: []
lifecycle_stage: archive
---

```yaml
requirement_id: REQ-0041-miniapp-home
requirement_name: miniapp-home
status: done
priority: P1
lifecycle_stage: review
created_at: 2026-07-16 09:09:51
updated_at: 2026-07-16 10:21:50
lifecycle:
  captured: 2026-07-16 09:09:51
  generated: 2026-07-16 09:20:59
  completed: 2026-07-16 09:24:44
  reviewed: 2026-07-16 09:40:45
  approved: 2026-07-16 09:40:45
iteration: sprint-008
openspec_changes:
  - change_id: add-miniapp-home
    type: add
    status: archived
related_requirements: []
knowledge_base_refs:
  - docs/knowledge-base/retrospectives/sprint-007-retrospective.md
cross_cutting_tags: []
scope:
  backend_api: 本期可能需要小程序首页聚合、分享/咨询事件、热销统计接口；必须复用现有公开数据，若 API contract 变化需同步 OpenAPI/Orval/docs/tests
  database: 可能涉及行为统计事件或聚合字段；不得为了首页新增重复业务表，必要变化需同步数据库文档与测试
  web_admin: 不涉及；快捷入口和服务入口后台配置另拆需求
  web_storefront: 不涉及
  wechat_miniapp: 本期
  object_storage: 仅消费后端授权图片 URL；小程序不得直连未授权对象存储
readiness_notes: 已评审通过；可执行 /req-opsx；实现阶段需同步 API/DB/Orval/docs/tests，并保持收藏、预约、后台入口配置等不做项边界。
expected_openspec_change: add-miniapp-home
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-17 22:58:16 | lifecycle-stage-migrate | review → archive（/opsx-archive add-miniapp-home） |
| 2026-07-17 22:57:42 | /opsx-archive | Change `add-miniapp-home` 已归档，状态同步完成。 |
| 2026-07-16 10:46:52 | /opsx-apply | Change `add-miniapp-home` apply 完成，待 archive。 |
| 2026-07-16 09:41:19 | lifecycle-stage-migrate | plan → review（/req-review --approve） |
| 2026-07-16 09:09:51 | /req-capture | 记录微信小程序首页需求，附件版本号不作为项目需求版本事实 |
| 2026-07-16 09:20:59 | /req-generate | 生成微信小程序首页 PRD，状态更新为 draft |
| 2026-07-16 09:24:44 | /req-complete | 补齐用户故事、业务流程、验收标准与原型上下文；管理端 knowledge-base 横切标签 N/A，参考 sprint-007 复盘的分层验收与范围控制经验 |
| 2026-07-16 09:31:13 | /req-complete-refine | 按产品确认将分享功能、咨询功能、热销行为统计纳入本期范围，收藏与预约仍排除 |
| 2026-07-16 09:40:45 | /req-review --approve | 评审通过，状态更新为 approved，准备迁入 review 阶段 |
| 2026-07-16 09:40:45 | /req-opsx | 创建 OpenSpec Change `add-miniapp-home`，状态 proposed |
| 2026-07-16 10:21:50 | /sprint-propose | 纳入 sprint-008 正式范围，容量估算 12.0/30.0 人天 |

## 关联缺陷

| BUG | 严重等级 | 状态 | 关联 Change | 说明 |
|---|---|---|---|---|
| BUG-0065-miniapp-home-preview-deviation | high | done | fix-miniapp-home-preview-runtime-entry | 微信小程序首页预览效果与 REQ-0041 原型和验收差异明显 |
