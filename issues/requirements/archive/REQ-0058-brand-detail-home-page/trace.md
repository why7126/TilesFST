---
requirement_id: REQ-0058-brand-detail-home-page
status: done
priority: P1
created_at: 2026-07-19 22:30:11
updated_at: 2026-07-20 22:43:31
lifecycle_stage: archive
lifecycle:
  captured: 2026-07-19 22:30:11
  generated: 2026-07-19 23:12:25
  completed: 2026-07-19 23:18:53
  reviewed: 2026-07-19 23:45:40
  approved: 2026-07-19 23:45:40
iteration: sprint-009
openspec_changes:
  - change_id: add-miniapp-brand-detail-home-page
    type: add
    status: archived
related_requirements:
  - REQ-0005-brand-management
knowledge_base_refs:
  - docs/knowledge-base/retrospectives/sprint-008-retrospective.md
  - docs/knowledge-base/best-practices/miniapp-custom-navigation.md
cross_cutting_tags: []
readiness: Ready
---

```yaml
requirement_id: REQ-0058-brand-detail-home-page
status: done
priority: P1
created_at: 2026-07-19 22:30:11
updated_at: 2026-07-20 08:12:39
lifecycle_stage: review
lifecycle:
  captured: 2026-07-19 22:30:11
  generated: 2026-07-19 23:12:25
  completed: 2026-07-19 23:18:53
  reviewed: 2026-07-19 23:45:40
  approved: 2026-07-19 23:45:40
iteration: sprint-009
openspec_changes:
  - change_id: add-miniapp-brand-detail-home-page
    type: add
    status: archived
related_requirements:
  - REQ-0005-brand-management
knowledge_base_refs:
  - docs/knowledge-base/retrospectives/sprint-008-retrospective.md
  - docs/knowledge-base/best-practices/miniapp-custom-navigation.md
cross_cutting_tags: []
readiness: Ready
```

# Trace

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-20 22:39:37 | lifecycle-stage-migrate | review → archive（/opsx-archive add-miniapp-brand-detail-home-page） |
| 2026-07-20 22:38:58 | /opsx-archive | Change `add-miniapp-brand-detail-home-page` 已归档，状态同步完成。 |
| 2026-07-20 08:12:39 | /sprint-propose | 纳入 sprint-009，关联 Change `add-miniapp-brand-detail-home-page`。 |
| 2026-07-20 00:01:09 | /req-opsx | 创建 OpenSpec Change `add-miniapp-brand-detail-home-page`，状态 proposed。 |
| 2026-07-19 23:52:27 | lifecycle-stage-migrate | plan → review（/req-review --approve） |
| 2026-07-19 23:45:40 | /req-review --approve | 需求评审通过；状态进入 approved；准备从 plan 阶段迁入 review 阶段。 |
| 2026-07-19 23:18:53 | /req-complete | 补齐 user-stories、business-flow、acceptance、prototype/miniapp；状态进入 pending_review；知识库参考 sprint-008 复盘和小程序自定义导航 best-practice。 |
| 2026-07-19 23:12:25 | /req-generate | 生成 requirement.md，状态进入 draft；范围收敛为微信小程序品牌入口页与品牌主页/详情页。 |
| 2026-07-19 22:30:11 | /req-capture | 记录新增品牌详情页/主页功能需求，暂定父需求为 REQ-0005-brand-management。 |

## 关联需求

| REQ | 关系 | 说明 |
|---|---|---|
| REQ-0005-brand-management | parent | 品牌主页/详情页复用品牌主数据 |
| REQ-0041-miniapp-home | related | 品牌轮播对齐首页轮播视觉和交互 |
| REQ-0056-product-list-card-only-layout | related | 商品 Tab 复用双列商品卡片策略 |
| REQ-0038-brand-certificate-management | related | 证书 Tab 复用品牌证书展示规则 |
| REQ-0057-certificate-list-page | related | 证书列表信息结构保持一致 |

## Knowledge-base Cross-cutting Report

| 标签 | 引用文档 | 将写入 acceptance 的 AC 条数 |
|---|---|---:|
| 无管理端横切标签 | 无 `admin-list` / `admin-form` / `admin-modal` / `media-upload` 命中；已参考 `docs/knowledge-base/retrospectives/sprint-008-retrospective.md` 与 `docs/knowledge-base/best-practices/miniapp-custom-navigation.md` | 0 |

补充说明：本 REQ 是微信小程序前台 UI，未触发 req-complete 定义的管理端横切 AC；小程序导航、设备视口和运行入口风险已写入 `acceptance.md` 的 AC-036 至 AC-039。
- 2026-07-20 22:38:58 workflow-sync：状态同步为 done（Change archived）
