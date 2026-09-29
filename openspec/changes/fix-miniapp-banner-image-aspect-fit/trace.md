---
change_id: fix-miniapp-banner-image-aspect-fit
source_requirement: REQ-0137-miniapp-banner-image-aspect-fit
requirement_id: REQ-0137-miniapp-banner-image-aspect-fit
sprint: sprint-030
iteration: sprint-030
status: proposed
change_type: fix
created_at: '2026-09-08 18:37:50'
updated_at: '2026-09-11 09:07:09'
prototype_refs:
- issues/requirements/review/REQ-0137-miniapp-banner-image-aspect-fit/prototype/web/banner-fit.html
- issues/requirements/review/REQ-0137-miniapp-banner-image-aspect-fit/prototype/web/context.md
knowledge_base_refs:
- docs/knowledge-base/best-practices/miniapp-media-four-part-acceptance-practice.md
product_data_collection_observability:
  status: not_applicable
  affected_layers: [wechat_miniapp]
  reason: 仅图片mode与局部布局，不改API/DB、请求日志、行为事件、Task Trace、端请求封装、URL策略和保留周期。
  validation: 来源REQ的AC-OBS-001/002及tasks 4.1承接，当前仅文档核对，尚未实施或产品验收。
---

## 当前状态

CLI创建Change，proposal/design/四个delta specs/tasks已建立；Requirement Readiness为Partially Ready，HTML已具备，PNG与渲染证据留待实施。冲突报告及UI Contract见design.md；需求保持in_sprint，验收未开始。

## 视觉与PNG清单

- [ ] 原型拆解及Skeleton首轮确认。
- [ ] 1440px设计核对视口与小程序等价截图。
- [ ] 四页面320/375/430pt及关键交互状态证据。
- [ ] 图框、图文分区、背景、overflow和层级的样式证据。
- [ ] Mock/API边界及最终一致性复核，返修截图更新。

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-09-08 18:37:50 | /req-opsx | 基于REQ-0137创建视觉展示Change，待回填sprint-030；未实施业务代码。 |

## Apply 检查点（2026-09-08 18:42:45）

完成1.1，整体1/12。Skeleton结构见skeleton.md；人工确认与尺寸选择待定，独立静态门禁及37通过/1基线失败见implementation-evidence.md。当前未修改src，无产品视觉验收。archive_ready=false；不发送opsx.apply完成事件。


## 本轮继续实施

三个页面五个目标图片节点已切换aspectFit，保留同期authorized-image及媒体契约。任务1.1、4.1完成（2/12）；细节任务按Skeleton证据门禁保持未关闭。新增4项静态回归通过，原静态套件37通过/1端口配置基线失败；治理静态校验通过，行为运行器agent_runtime_closed待恢复。DevTools局部观察及全部证明边界见implementation-evidence.md。

品牌分区确认和完整视觉、Network、样式证据尚缺；当前为部分实施，archive_ready=false，不发送opsx.apply完成事件。观测N/A、无API/DB/Orval/Compose范围扩展。
