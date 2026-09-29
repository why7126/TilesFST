---
req_id: REQ-0134-miniapp-public-page-sharing
status: done
created_at: 2026-09-05 21:42:49
updated_at: 2026-09-08 08:28:42
recorded_by: product
source: 用户反馈
priority_hint: P1
parent_requirement: null
product_data_collection_observability:
  applicability: applicable
  affected_layers:
    - miniapp
    - usage_events
  reason: 补齐小程序分享交互及相应行为采集，复用既有请求封装与日志链路；不新增API或DB结构，不涉及复杂任务，Task Trace及流程节点为N/A。
  validation: capture阶段已完成分享回调覆盖静态核对；后续验证事件语义、参数脱敏、失败不阻断及真机分享直达。
---

# 一句话

补齐小程序公开内容页朋友及朋友圈分享。

# 原始描述

补齐公开内容页的朋友及朋友圈分享，个人收藏清单分享暂不纳入。

# 探索结论与范围

- 对象：已注册的首页、商品详情、商品列表、品牌列表、品牌详情、证书列表、证书详情、门店信息、分类、搜索及发现等公开内容页。
- 统一覆盖朋友与朋友圈分享；详情直达同一公开对象，列表与搜索结果保留必要且安全的上下文。
- 搜索首页仅分享公开入口，不携带最近搜索历史；个人收藏清单及可分享选品清单能力暂不纳入。
- 分享标题和图片应匹配公开内容，采用现有公开轻量素材与安全兜底；不得泄露本机个人数据或内部字段。
- 现状静态检查：5个注册页面具备两种回调，品牌列表、证书列表和发现页仅具备朋友回调，搜索、门店信息、分类和收藏页未定义两种回调。依据为 `src/miniapp/app.json` 和 `src/miniapp/pages/*/index.js`，不代表真机验证结论。
- 本需求补齐公开分享能力，可独立验收；不扩展购物、邀请奖励、分享排行或个人收藏清单发布能力。
- 优先复用现有接口和端侧分享实现，预计无需API、数据库、Orval及Docker Compose改动；若细化阶段改变接口边界，应另行明确同步要求。

优先级为记录阶段建议，待评审确定。来源：用户反馈与 `/explore`，由 `/req-capture` 记录；未关联 Sprint 或 OpenSpec Change。

# 待澄清

- [ ] 在需求设计阶段明确逐页标题、图片兜底、分享参数白名单和搜索/列表状态恢复矩阵。
- [ ] 在测试计划中确定微信客户端与基础库兼容范围，以及朋友圈单页入口验证条件。

# 建议验收要点

- 每个纳入页面均可发起朋友和朋友圈分享，接收者打开后显示对应公开内容。
- 中文关键词、必要分类/对象参数可正确恢复，不传个人搜索历史、收藏清单或内部字段。
- 覆盖内容不存在/下架、图片失败、网络失败、无页面栈返回和朋友圈单页入口。
- 分享行为沿用统一采集规范，区分分享触发与实际完成；上报失败不阻断分享。
- 静态回归与微信真机接收验证分别记录证据来源，不以回调存在替代分享成功。

# 规范依据

遵循 `rules/requirement-management.md`、`rules/issues-lifecycle.md`、`rules/document-governance.md`、`rules/security.md`、`rules/ui-design.md` 和 `rules/agent-context-budget.md`。产品数据采集适用性参照 `docs/standards/product-data-collection-observability.md`。
