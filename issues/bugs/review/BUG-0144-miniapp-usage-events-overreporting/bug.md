---
bug_id: BUG-0144-miniapp-usage-events-overreporting
title: 小程序商品列表页与搜索页 usage-events 仍可能偏多
severity: medium
status: in_sprint
owner:
discovered_at: 2026-08-26 08:29:04
environment: local
related_requirement:
related_change: fix-miniapp-usage-events-overreporting
updated_at: 2026-08-26 09:52:55
created_at: 2026-08-26 08:34:31
---

# 现象

BUG-0143 已治理小程序启动阶段遥测请求自我放大和首页商品卡曝光逐条上报问题，但商品列表页与搜索页仍可能产生偏多 `/api/v1/usage-events` 请求。

当前观察到的剩余风险集中在三类口径：

- 商品列表页同时存在页面级列表曝光与商品卡组件曝光，两套事件可能对同一批 SKU 重复计入。
- 搜索页输入过程会在每次输入变化时上报 `search_input`，输入较快时 usage-events 数量会随字符变化频率放大。
- 搜索结果、列表刷新、分页、筛选切换等场景缺少统一可解释的曝光去重窗口，可能重复上报同一 SKU、同一模块、同一上下文的曝光。

# 复现步骤

1. 启动本地后端服务与微信小程序开发环境。
2. 打开微信开发者工具网络面板，过滤 `/api/v1/usage-events`。
3. 进入商品列表页，加载首屏商品。
4. 观察首屏商品列表是否同时触发 `product_list_item_exposure` 与 `product_card_exposure`。
5. 在商品列表页执行滚动、下拉刷新、加载更多、筛选或入口切换，继续观察 usage-events 数量与可见 SKU 数量的关系。
6. 进入搜索页，在搜索框连续输入关键词，例如快速输入 4-6 个字符。
7. 观察 `search_input`、`search_suggestion_exposure`、`search_result_exposure` 与商品卡曝光事件数量。
8. 对比实际搜索提交次数、实际结果展示次数、可见 SKU 数量和 usage-events 请求数量，确认是否存在重复口径或高频上报。

# 期望 vs 实际

期望：

- 商品列表页应只有一套主曝光口径，或页面级曝光与商品卡曝光有明确互斥/层级边界。
- 同一 SKU 在同一页面、同一模块、同一列表实例、同一曝光窗口内不应重复上报。
- 搜索输入不应按每个字符变化直接产生不可控 usage-events；连续输入应通过防抖、合并、采样或仅关键行为上报控制频率。
- 搜索结果曝光、商品卡曝光、列表分页和筛选刷新应具备统一去重策略，避免重复计入旧曝光，同时不误杀新的真实曝光。

实际：

- 商品列表页首屏可由页面逻辑上报 `product_list_item_exposure`，同时页面渲染的 `product-card` 组件又会上报 `product_card_exposure`。
- 搜索页 `search_input` 绑定输入变化即时上报，虽然搜索建议请求有防抖，但输入埋点本身没有同等频率控制。
- 搜索结果页使用 `product-card` 展示 SKU 结果时，可能同时存在结果级曝光与卡片级曝光，口径边界不够清晰。

# 影响范围

- 微信小程序商品列表页：分类商品、品牌商品、新品榜、热销榜、搜索承接列表。
- 微信小程序搜索页：搜索输入、搜索建议、搜索结果、筛选、结果商品卡。
- 微信小程序 `product-card` 组件曝光事件。
- 后端 `/api/v1/usage-events` 写入量、日志审计噪音和行为埋点数据质量。
- 搜索转化、商品曝光、热门商品、列表入口效果等后续分析报表口径。

# 严重等级说明

严重等级为 `medium`。

该问题不会阻断用户浏览商品、搜索、点击详情或分享，但会持续放大 usage-events 请求数量，并让商品曝光和搜索行为数据出现重复或高频噪音。若进入生产环境，可能增加后端写入和日志量，并降低后续行为分析、推荐统计和运营判断的可信度。

# 关联背景

- 关联缺陷：`BUG-0143-miniapp-telemetry-request-amplification`。
- BUG-0143 主要治理启动阶段埋点请求自我放大，以及首页商品卡曝光请求数量过高。
- BUG-0144 聚焦 BUG-0143 后续验收中暴露的商品列表页、搜索页和跨场景曝光去重策略缺口。
openspec_changes:
  - change_id: fix-miniapp-usage-events-overreporting
    type: fix
    status: applied
