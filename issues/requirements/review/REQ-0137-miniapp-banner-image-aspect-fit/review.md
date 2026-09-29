---
review_id: REV-REQ-0137-001
requirement_id: REQ-0137-miniapp-banner-image-aspect-fit
date: '2026-09-08 08:26:50'
created_at: '2026-09-08 08:26:50'
updated_at: '2026-09-08 08:26:50'
participants: []
reviewed_by: AI
review_basis: 用户执行 /req-review，无反向 flag，按默认 approve 规则进行文档评审
result: approved
---

# 需求评审

## 评审结论

通过，优先级 P1。四类大图建立等比完整适配、允许留白、容器稳定的规则，视频、非 Banner 图片及媒体来源策略均排除。品牌详情采用现有总高内独立图片区与文字区的方案，220rpx/160rpx 为实施起点，按 AC-006 验证真实文案和尺寸。

本结论为需求与方案评审，不代表产品实现、Skeleton、视觉或真机验收通过。当前文档就绪度 Partially Ready：HTML 与 context 已具备，PNG 和浏览器视觉证据尚缺；不阻塞需求评审，后续实现与归档仍须完成对应验收。

## 评审清单

| 检查项 | 结论 | 依据 |
|---|---|---|
| 范围与排除项 | 通过 | requirement.md §3 明确四类大图与视频、非 Banner、API/DB/存储排除范围 |
| 可测试验收 | 通过 | acceptance.md 17 条验收项覆盖图片分支、状态、宽度、交互、观测边界与横切预防 |
| 优先级与依赖 | 通过 | P1 对应跨四页面信息完整性；沿用 REQ-0118 的 URL/变体契约，无新增服务端依赖 |
| UI 策略 | 通过，保留实施验证条件 | prototype/web/banner-fit.html 与 context.md；品牌文字不遮住图片，保留总高度与字段 |
| 产品数据采集与链路观测 | N/A 声明充分 | trace、requirement 状态块及 AC-OBS-001/002；参照 docs/standards/product-data-collection-observability.md，仅小程序渲染，无采集字段、请求封装、保留周期或 Orval 变化 |
| 重复与兼容边界 | 通过 | BUG-0148 只覆盖 grid 商品卡；REQ-0118 管变体消费；REQ-0106 管 Banner 标题隐藏，本需求不恢复有图 Banner 标题遮罩 |

## 条件通过项

- [ ] 实现前将局部原型转入 UI Contract 并完成 Skeleton 首轮确认；后续补齐 PNG/等价视觉、1440px 核对视口及小程序证据、关键样式和最终一致性核对（AC-PROTOTYPE-001～003）。本次未重试此前被浏览器策略拒绝的本地页面访问。
- [ ] 实现时核对真实 320/375/430 pt 视口与 padding，不能把原型 cqw 直接视为小程序 rpx；验证品牌长文案、留白、回退、混排视频和现有跳转，完成 17 条 AC 后再提出交付验收。

以上为后续实施和验收条件，不改变本次 approved 结论。acceptance 保持 not_started，未勾选产品验收项。

## 迭代与容量

本次不纳入 Sprint，不创建 Change。当前可选 active Sprint 为 sprint-029，其 sprint.yaml 当前估算 35 人天、容量 30 人天；这是评审时的规划快照，不修改已有 capacity_gate 结论。后续 sprint-propose 需确认新增需求估算、调整范围/容量或安排后续迭代，不能仅凭需求通过认定存在可用容量。

## 影响与证据边界

本次仅评审文档、状态和目录迁移；业务实现预期影响小程序，不影响 API、DB、Web、管理端，无需 Orval、迁移或 Docker Compose 验证。本次采用文档与原型源码核对，不执行或声称业务测试通过。

遵循 rules/requirement-management.md、rules/issues-lifecycle.md、rules/document-governance.md、rules/ui-design.md、rules/testing.md、rules/security.md、rules/agent-context-budget.md。无明显规范优化点；未自动创建 follow-up Issue/Change。
