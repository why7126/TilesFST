---
requirement_id: REQ-0059-favorite-list-page
status: done
lifecycle_stage: archive
priority: P1
created_at: 2026-07-19 22:26:46
updated_at: 2026-07-21 08:05:00
---

# 需求追踪

## 基本信息

```yaml
requirement_id: REQ-0059-favorite-list-page
requirement_name: favorite-list-page
requirement_type: 用户侧 / 收藏列表
priority: P1
status: done
owner: product
source: 用户输入
target_clients:
  web_admin: 不适用
  web_catalog: 后续评估
  wechat_miniapp: 首期实现
related_requirements: []
related_changes:
  - add-favorite-list-page
lifecycle:
  captured: 2026-07-19 22:26:46
  generated: 2026-07-19 23:09:18
  completed: 2026-07-19 23:13:48
  reviewed: 2026-07-19 23:35:25
  approved: 2026-07-19 23:35:25
iteration: sprint-009
openspec_changes:
  - change_id: add-favorite-list-page
    type: add
    status: archived
readiness: Ready
readiness_notes: 五件套已补齐；UI 原型策略为 prototype/web/prototype.html + context.md，PNG 待后续设计导出但不阻塞评审。
documents:
  - capture.md
  - requirement.md
  - user-stories.md
  - business-flow.md
  - acceptance.md
  - review.md
  - prototype/web/context.md
  - prototype/web/prototype.html
expected_openspec_change: add-favorite-list-page
knowledge_base_refs:
  - docs/knowledge-base/best-practices/miniapp-custom-navigation.md
  - docs/knowledge-base/retrospectives/sprint-008-retrospective.md
cross_cutting_tags: []
retrospective_refs:
  - docs/knowledge-base/retrospectives/sprint-008-retrospective.md
```

## 关联需求

| REQ | 关系 | 说明 |
|---|---|---|
| REQ-0047-product-list-common-component-application | upstream | 如收藏对象为 SKU / 商品，收藏卡片可复用商品卡片字段与图片占位策略 |
| REQ-0044-miniapp-sku-detail-page | upstream | 收藏项点击进入 SKU 详情页时依赖详情页路径与参数 |
| REQ-0045-category-list-page | upstream | 空状态可引导用户回到分类浏览 |
| REQ-0046-search-component-application | upstream | 空状态可引导用户通过搜索查找商品 |

## Knowledge-base Cross-cutting

| 标签 | 引用文档 | 写入 acceptance 的 AC 条数 |
|---|---|---:|
| 无匹配标签 | 无横切 AC；本需求为用户侧收藏列表页，不涉及管理端列表/表单/弹窗/上传 | 0 |

最近复盘参考：`docs/knowledge-base/retrospectives/sprint-008-retrospective.md`。与本 REQ 相关的复发预防点为小程序页面后续实现阶段需关注自定义导航 offset、状态栏/胶囊避让、设备验收 evidence，以及分类、搜索、商品列表组件边界复用。实现阶段若覆盖微信小程序，应引用 `docs/knowledge-base/best-practices/miniapp-custom-navigation.md`。

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-21 08:05:00 | /release-prepare follow-up | 按后续需求口径确认小程序收藏页自定义导航标题为“收藏列表”，同步修正发布验收契约。 |
| 2026-07-20 18:09:59 | lifecycle-stage-migrate | review → archive（/opsx-archive add-favorite-list-page） |
| 2026-07-20 18:09:15 | /opsx-archive | Change `add-favorite-list-page` 已归档，状态同步完成。 |
| 2026-07-20 08:46:21 | `/opsx-apply` | 完成 add-favorite-list-page 首期小程序实现；收藏列表使用本机快照，未新增 API / DB |
| 2026-07-19 23:47:14 | lifecycle-stage-migrate | plan → review（/req-review --approve） |
| 2026-07-19 23:55:27 | `/req-opsx` | 创建 OpenSpec Change：add-favorite-list-page |
| 2026-07-19 23:35:25 | `/req-review --approve` | 需求评审通过，状态进入 approved，阶段 plan → review |
| 2026-07-19 23:13:48 | `/req-complete` | 补齐 user-stories、business-flow、acceptance 与原型策略；Knowledge-base gate 为 N/A；状态进入 pending_review |
| 2026-07-19 23:09:18 | `/req-generate` | 生成收藏列表页 requirement.md，状态更新为 draft |
| 2026-07-19 22:26:46 | `/req-capture` | 记录新增收藏列表页需求 |

## 关联缺陷

| BUG | 严重等级 | 状态 | 关联 Change | 说明 |
|---|---|---|---|---|
- 2026-07-20 18:09:15 workflow-sync：状态同步为 done（Change archived）
