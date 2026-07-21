---
requirement_id: REQ-0053-miniapp-custom-navigation-best-practice
title: 小程序自定义导航 best-practice 沉淀用户故事
status: done
created_at: 2026-07-19 18:41:33
updated_at: 2026-07-19 21:05:25
---

# REQ-0053 小程序自定义导航 best-practice 沉淀用户故事

## US-001 小程序开发按统一规则接入导航

作为小程序开发，我希望新增或改造页面时能引用统一的自定义导航 best-practice，以便状态栏、胶囊避让、返回兜底和页面 offset 不再散落在各页面中重复实现。

验收要点：

- best-practice 明确适用页面和豁免条件。
- 文档说明状态栏、胶囊、导航高度和右侧 reserve 的数据来源与 fallback。
- 文档提供页面接入 checklist，覆盖首页、TabBar 页、普通非首页和详情/分享直达页。
- 文档要求页面特殊 offset 必须说明原因，不允许多个页面互相冲突地硬编码顶部 padding。

## US-002 测试人员按截图矩阵验收

作为测试 / 验收人员，我希望能按固定截图矩阵验证小程序自定义导航，以便明确哪些视口、设备、页面状态和入口路径已经通过，哪些仍为 blocked 或 follow_up。

验收要点：

- 截图矩阵覆盖页面、入口、视口、真机、页面状态和结论字段。
- DevTools 320 / 375 / 430 pt 与真机验收结论分层记录。
- 没有真机 evidence 时不得写成真机通过。
- failed、blocked、follow_up 必须记录影响页面、原因和后续承接方式。

## US-003 产品负责人判断发布风险

作为产品 / 需求负责人，我希望自定义导航的验收结论能清楚表达状态栏不遮挡、胶囊不重叠、返回可兜底、内容不被 fixed header 遮挡，以便发布前判断是否存在用户可感知风险。

验收要点：

- acceptance 明确首页、搜索、分类、商品列表、详情、收藏、证书和门店信息的覆盖范围。
- 分享直达详情、异常参数、加载态、空状态和错误态被纳入风险判断。
- Release note 或 Sprint 验收报告只引用摘要，不复制完整矩阵。
- 设备验收不足时必须保留剩余风险和 follow-up。

## US-004 AI Agent 在后续 Change 中复用规则

作为 AI / Codex Agent，我希望后续小程序 REQ、OpenSpec Change、tasks 和 acceptance 能引用同一 best-practice，以便不再为每个页面重新生成互相冲突的导航验收规则。

验收要点：

- trace 记录 `knowledge_base_refs`，供后续 `/req-opsx` 写入 change design。
- OpenSpec tasks 可引用 best-practice 中的接入 checklist 和截图矩阵。
- Sprint acceptance-report 可引用 evidence 摘要，不重复展开全部细节。
- 若后续 Change 修改导航实现，必须检查 best-practice 是否需要同步更新。

## US-005 复盘行动项进入正式闭环

作为流程维护者，我希望 sprint-008 中暴露的小程序设备验收和导航遮挡风险能进入正式需求闭环，以便后续 Sprint 不再把状态栏、胶囊和 fixed header 风险留在人工备注中。

验收要点：

- trace 引用 sprint-008 复盘作为知识库来源。
- best-practice 明确继承 REQ-0048 的导航经验和 REQ-0052 的 evidence 模板。
- 历史截图和残留可作为案例，但不强制本需求回填全部历史 evidence。
- 后续若需要自动生成 follow-up Issue，应拆为独立工具链需求。
