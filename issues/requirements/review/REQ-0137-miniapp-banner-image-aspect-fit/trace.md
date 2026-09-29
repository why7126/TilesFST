---
requirement_id: REQ-0137-miniapp-banner-image-aspect-fit
status: in_sprint
priority: P1
created_at: '2026-09-07 22:45:57'
updated_at: 2026-09-08 18:43:00
lifecycle_stage: review
lifecycle:
  captured: '2026-09-07 22:45:57'
  generated: '2026-09-07 22:53:01'
  completed: '2026-09-07 22:58:53'
  reviewed: '2026-09-08 08:26:50'
  approved: '2026-09-08 08:26:50'
iteration: sprint-030
openspec_changes:
- change_id: fix-miniapp-banner-image-aspect-fit
  type: fix
  status: in_progress
related_requirements:
- REQ-0106-admin-banner-title-hidden
- REQ-0118-unified-web-miniapp-image-variant-consumption-matrix
knowledge_base_refs:
- docs/knowledge-base/README.md
- docs/knowledge-base/best-practices/miniapp-media-four-part-acceptance-practice.md
- docs/knowledge-base/retrospectives/sprint-028-retrospective.md
cross_cutting_tags: []
cross_cutting_tag_reason: 小程序图片展示，不涉及管理端列表、表单、弹窗或媒体上传；主动引用小程序媒体专项实践。
prototype_refs:
- prototype/web/banner-fit.html
- prototype/web/context.md
product_data_collection_observability:
  status: not_applicable
  affected_layers:
  - wechat_miniapp
  reason: 仅四类大图渲染与局部布局，不改变 API、DB、请求日志、行为事件、Task Trace、端请求封装、敏感采集字段或保留周期；无 Orval、迁移或部署输入变化。
  validation: 已核对需求及局部 WXML/WXSS，AC-OBS-001/002 覆盖后续差异、测试和脱敏验证；当前未实现或验收小程序。
related_changes:
  - fix-miniapp-banner-image-aspect-fit
---

# 需求跟踪

小程序所有 Banner 图片展示策略调整为完整适配，覆盖首页 Banner、品牌列表 Banner、品牌详情头图和商品详情顶部媒体图片；视频与非 Banner 缩略图暂不纳入。范围、分类依据与验收建议见 `capture.md`。

## 变更记录
| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-09-07 22:45:57 | /capture | 记录小程序 Banner 图片完整适配展示需求；未评审、未纳入 Sprint。 |
| 2026-09-07 22:53:01 | /req-generate | 生成 requirement.md 草案，明确四类大图完整适配、留白、稳定容器及视频排除边界；未评审、未纳入 Sprint。 |
| 2026-09-07 22:58:53 | /req-complete | 经 enriching 补齐故事、流程、验收及局部 HTML 原型，转 pending_review；读取 sprint-028 媒体验收经验，增加 3 条专项横切 AC，区分资源可读与实际 render 证据；未评审、未纳入 Sprint。 |
| 2026-09-08 08:26:50 | /req-review | 文档评审通过，状态 approved；视觉证据及真实尺寸验证由后续 Change 承接；补充 REQ-0106 兼容边界；未纳入 Sprint，容量需规划确认。 |
| 2026-09-08 18:37:50 | /req-opsx | 创建 fix-miniapp-banner-image-aspect-fit，四规格delta与UI Contract齐；同Sprint回填，未开发。 |

## 文档就绪与关联

需求、用户故事、业务流程、验收和 trace 已齐，局部原型及 context 已建立；PNG 导出为非阻塞辅助证据。readiness: Partially Ready（PNG 尚待导出）；knowledge-base gate: Pass（四个固定标签无匹配，主动采用媒体专项实践的 3 条 AC-XCUT）。

requirement.md 为范围事实源；user-stories.md 映射用户价值；business-flow.md 定义状态与品牌局部布局；acceptance.md 维护后续验收；prototype/web/context.md 维护局部设计边界。源 capture 保留历史记录，不作为已确认布局或验收事实。

本命令遵循 rules/requirement-management.md、issues-lifecycle.md、ui-design.md、document-governance.md、testing.md、security.md、agent-context-budget.md。仅需求与原型资产变更；预期实现只影响小程序，不影响 API、DB、Web、管理端，无需 Orval 或 Docker Compose 验证。业务测试留待 Change 实现，当前只核对需求包和原型。

## 本次校验摘要

需求包 Markdown 元数据解析通过，17 条 AC 编号唯一且均未勾选；原型 JavaScript 经 node --check 语法检查通过。浏览器安全策略拒绝打开本地 HTML，未产生 PNG、渲染或交互验证证据；该缺口不阻塞需求评审，readiness 保持 Partially Ready。Workflow Sync 成功，验收状态为 not_started；未创建 OpenSpec Change、业务代码或额外 Issue。

## 最新评审结论

review.md 记录 approved 结论及实施验收条件；验收状态仍为 not_started。需求已纳入 sprint-030，当前 iteration 为 sprint-030，openspec_changes 已关联 fix-miniapp-banner-image-aspect-fit。视觉证据缺口不阻塞本次文档评审，但不得据此跳过实现验收。
