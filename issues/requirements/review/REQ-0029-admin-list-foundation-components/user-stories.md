---
title: 用户故事
purpose: REQ-0029 管理端列表基础组件用户故事
content: 基于 requirement.md、capture.md、req-explore 结论与管理端列表页知识库提炼
source: AI 根据 PRD 与知识库生成，项目团队确认
update_method: PRD、原型、验收标准或 Design System 策略变更时同步更新
owner: product
status: draft
created_at: 2026-07-05 14:14:26
updated_at: 2026-07-05 14:14:26
note: REQ-0029-admin-list-foundation-components
---

# 用户故事

## US-001 前端开发复用 MetricCard

作为前端开发人员，我希望通过统一的 `MetricCard` 组件渲染管理端列表页指标摘要，以便避免在 SKU、品牌、日志、接口文档等页面重复手写 `metric-card` DOM。

验收要点：

- MUST 支持 `label`、`value`、`description` 基础字段。
- MUST 稳定输出 `.metric-card`、`.metric-label`、`.metric-value`、`.metric-desc`。
- MUST 支持空值或加载中统一占位。
- SHOULD 支持 danger / 异常描述变体。

## US-002 前端开发复用 MetricCardGrid

作为前端开发人员，我希望通过 `MetricCardGrid` 或等价容器承载 2–4 个指标卡，以便页面不再重复拼装 `summary-grid` 结构。

验收要点：

- MUST 支持 2、3、4 卡片布局。
- MUST 支持 `aria-label` 描述指标区域。
- MUST 保持与现有管理端列表页 spacing、圆角、边框和字号一致。
- MUST 不造成 hero、filter、table 的纵向位移。

## US-003 前端开发复用分页窗口工具

作为前端开发人员，我希望分页窗口算法从 feature 私有目录沉淀到共享层，以便所有管理端列表页使用同一套页码窗口规则。

验收要点：

- MUST 默认最多展示 5 个页码。
- MUST 覆盖单页、首页附近、末页附近、当前页居中、非法输入兜底等场景。
- SHOULD 保留现有 `getPaginationWindow` 的可理解 API。
- MUST 迁移或保留现有分页窗口测试。

## US-004 QA 验证列表页 DOM 契约

作为 QA，我希望通过稳定的 DOM class 与测试用例验证指标卡和分页结构，以便快速识别局部 DOM 漂移。

验收要点：

- MUST 能通过 Testing Library 查询关键文案和 DOM class。
- MUST 覆盖 `.page-summary`、`.page-right`、`.page-buttons`、`.page-size-wrap`。
- MUST 覆盖 `.metric-label`、`.metric-value`、`.metric-desc`。
- SHOULD 在首批接入页面保留结构 smoke 或 snapshot。

## US-005 产品负责人查看设计验收示例

作为产品负责人，我希望在 `/design-system` 或管理端设计验收区看到 MetricCard 与分页窗口示例，以便评审组件是否满足管理端列表页统一体验。

验收要点：

- MUST 展示正常、空值 / 加载中、danger 描述等指标卡样例。
- SHOULD 展示 2、3、4 卡片布局。
- SHOULD 展示分页窗口边界样例。
- MUST 使用管理端列表页一致性知识库中的 DOM 基准作为验收依据。

## US-006 管理端用户获得一致体验

作为企业内部管理员或运营员工，我希望不同管理端列表页的指标摘要与分页位置、结构和交互一致，以便降低跨页面操作成本。

验收要点：

- MUST 在首批接入页面保持原有筛选、分页状态、空态和权限逻辑不变。
- MUST 不引入跳页输入框或页面私有分页容器。
- SHOULD 优先覆盖 SKU、日志审计、接口文档或品牌中的 2–3 个页面。
- MUST 与 `REQ-0028-admin-list-page-contract` 的页面级契约保持一致。
