---
req_id: REQ-0133-miniapp-price-red-display
status: done
created_at: 2026-09-05 21:42:49
updated_at: 2026-09-06 14:19:46
recorded_by: product
source: 用户反馈
priority_hint: P2
parent_requirement: null
product_data_collection_observability:
  applicability: not_applicable
  affected_layers: []
  reason: 仅调整小程序价格视觉样式，不改变API、数据库、请求日志、行为事件、Task Trace或端请求封装。
  validation: capture阶段已完成代码静态范围核对；尚未实施或进行视觉验收。
---

# 一句话

小程序有效价格统一红色展示。

# 原始描述

小程序有效价格统一红色展示。

# 探索结论与范围

- 对象：小程序商品卡片、首页、商品列表、搜索结果、商品详情及收藏中的有效价格金额。
- 有效价格金额统一使用独立价格语义红色；“参考价格”、单位说明和“暂无”等非金额信息保留辅助文字色。
- 保留品牌金用于品牌、按钮和激活态，不全局替换品牌色，不改变参考价格含义。
- 本需求为跨页面视觉增强，可独立验收；不修改价格计算、后端格式化字段、API、数据库或 Web / 管理端。
- 现状依据：`src/miniapp/components/product-card/index.wxss`、`src/miniapp/pages/tile-detail/index.wxss`、`src/miniapp/pages/favorites/index.wxss` 使用金色价格；`rules/ui-design.md` 定义现有品牌金方向。

优先级为记录阶段建议，待评审确定。来源：用户反馈与 `/explore`，由 `/req-capture` 记录；未关联 Sprint 或 OpenSpec Change。

# 待澄清

- [ ] 在需求设计阶段确定价格语义色色值及暗色背景可读性验收标准。

# 建议验收要点

- 所有有效价格入口显示一致，辅助文案与无价状态不误用金额强调色。
- 共享卡片及独立价格样式均覆盖；长价格、不同密度和暗色背景保持可读。
- 通过小程序样式检查及视觉验收，避免品牌按钮、警示状态和其他端颜色被误改。

# 规范依据

遵循 `rules/requirement-management.md`、`rules/issues-lifecycle.md`、`rules/document-governance.md`、`rules/security.md`、`rules/ui-design.md` 和 `rules/agent-context-budget.md`。产品数据采集适用性参照 `docs/standards/product-data-collection-observability.md`。
