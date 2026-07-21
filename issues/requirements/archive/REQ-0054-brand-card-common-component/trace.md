---
requirement_id: REQ-0054-brand-card-common-component
status: done
priority: P1
created_at: 2026-07-19 17:36:54
updated_at: 2026-07-19 21:11:26
lifecycle:
  captured: 2026-07-19 17:36:54
  generated: 2026-07-19 17:41:55
  completed: 2026-07-19 17:45:31
  reviewed: 2026-07-19 17:49:48
  approved: 2026-07-19 17:49:48
iteration: sprint-009
openspec_changes:
  - change_id: add-miniapp-brand-card-component
    type: add
    status: archived
related_requirements:
  - REQ-0005-brand-management
  - REQ-0044-miniapp-sku-detail-page
  - REQ-0049-miniapp-product-card-component
  - REQ-0047-product-list-common-component-application
  - REQ-0038-brand-certificate-management
knowledge_base_refs: []
cross_cutting_tags:
  - miniapp
  - brand
  - component
  - design-system
lifecycle_stage: archive
---

# Trace

```yaml
requirement_id: REQ-0054-brand-card-common-component
status: done
priority: P1
created_at: 2026-07-19 17:36:54
updated_at: 2026-07-19 21:11:26
lifecycle:
  captured: 2026-07-19 17:36:54
  generated: 2026-07-19 17:41:55
  completed: 2026-07-19 17:45:31
  reviewed: 2026-07-19 17:49:48
  approved: 2026-07-19 17:49:48
iteration: sprint-009
openspec_changes:
  - change_id: add-miniapp-brand-card-component
    type: add
    status: archived
related_requirements:
  - REQ-0005-brand-management
  - REQ-0044-miniapp-sku-detail-page
  - REQ-0049-miniapp-product-card-component
  - REQ-0047-product-list-common-component-application
  - REQ-0038-brand-certificate-management
knowledge_base_refs: []
cross_cutting_tags:
  - miniapp
  - brand
  - component
  - design-system
lifecycle_stage: review
```

## 关联需求

| REQ | 关系 | 说明 |
|---|---|---|
| REQ-0005-brand-management | parent | 品牌卡片组件服务于品牌信息展示与复用，属于品牌管理/品牌展示能力的组件化延展 |
| REQ-0044-miniapp-sku-detail-page | related | 首版优先替换 SKU 详情页现有内联品牌卡片 |
| REQ-0049-miniapp-product-card-component | related | 参考小程序商品卡片组件的边界、图片 fallback、跳转和埋点策略 |
| REQ-0047-product-list-common-component-application | related | 后续品牌商品列表或推荐模块可能与商品列表通用能力联动 |
| REQ-0038-brand-certificate-management | related | 品牌证书属于后续品牌详情/资质展示范围，首版品牌卡片不直接展示证书列表 |

## Knowledge-base Cross-cutting

| 标签 | 引用文档 | 写入 acceptance 的 AC 条数 |
|---|---|---:|
| 无匹配标签 | 无横切 AC；本需求为微信小程序展示组件，不涉及管理端列表/表单/弹窗或媒体上传链路 | 0 |

最近复盘参考：`docs/knowledge-base/retrospectives/sprint-008-retrospective.md`。与本 REQ 直接相关的复发预防点为小程序组件边界拆清、设备/视口验收证据、`.ts` / `.js` 运行入口事实源一致性；已写入 `business-flow.md` 与 `acceptance.md` 的小程序验收要点。

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-19 21:10:57 | lifecycle-stage-migrate | review → archive（/opsx-archive add-miniapp-brand-card-component） |
| 2026-07-19 21:09:57 | /opsx-archive | Change `add-miniapp-brand-card-component` 已归档，状态同步完成。 |
| 2026-07-19 18:36:29 | /req-opsx REQ-0054 | 创建 OpenSpec Change `add-miniapp-brand-card-component`，状态为 proposed |
| 2026-07-19 17:53:58 | /sprint-propose | 纳入 sprint-009，状态进入 in_sprint；后续先 /req-opsx |
| 2026-07-19 17:50:42 | lifecycle-stage-migrate | plan → review（/req-review --approve） |
| 2026-07-19 17:49:48 | /req-review --approve | 需求评审通过，状态进入 approved；后续可 /req-opsx 或纳入 Sprint 规划 |
| 2026-07-19 17:45:31 | /req-complete | 补齐 user-stories、business-flow、acceptance 与小程序 prototype；Knowledge-base gate 为 N/A；状态进入 pending_review |
| 2026-07-19 17:41:55 | /req-generate | 生成 requirement.md，状态进入 draft；范围收敛为微信小程序品牌卡片组件 |
| 2026-07-19 17:36:54 | /req-capture | 捕获需求：生成品牌卡片通用组件 |

- 2026-07-19 21:09:57 workflow-sync：状态同步为 done（Change archived）
