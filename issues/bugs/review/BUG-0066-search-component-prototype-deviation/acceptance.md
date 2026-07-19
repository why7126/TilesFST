---
bug_id: BUG-0066-search-component-prototype-deviation
status: approved
created_at: 2026-07-19 13:17:45
updated_at: 2026-07-19 13:21:10
related_requirement: REQ-0046-search-component-application
source_change: add-miniapp-search-component
---

# Acceptance - BUG-0066 搜索组件整体交互与原型差异较大

## 回归验收标准

- [ ] AC-BUG-001 搜索页顶部结构与 REQ-0046 原型一致，包含返回按钮、搜索框、取消/搜索按钮，并位于顶部安全区下方。
- [ ] AC-BUG-002 独立搜索页复用 `components/search-entry`，或实现与该通用组件一致的关键词、清空、提交、取消/返回、禁用态、`scope` 和 `sourcePage` 行为。
- [ ] AC-BUG-003 搜索首页按 `01-search-home.html` 展示最近搜索、热门搜索和最近浏览；最近搜索支持单条删除和全部清空。
- [ ] AC-BUG-004 联想态按 `02-search-suggestions.html` 展示 6 到 10 条建议，并能区分最近搜索、品牌、SKU、类目/规格或普通搜索建议；证书不出现在联想中。
- [ ] AC-BUG-005 搜索结果页按 `03-search-results.html` 展示综合、SKU、品牌、类目、证书 Tab，综合默认激活且横向可滚动。
- [ ] AC-BUG-006 综合结果页渲染最多 1 条最佳匹配，并按后端 `sections` 展示相关 SKU、相关类目、相关证书等分区；不得仅展示扁平 SKU 列表。
- [ ] AC-BUG-007 SKU 卡片展示主图、产品名称、SKU 编码、品牌、规格和参考价格，整卡点击进入 SKU 详情，不展示收藏、分享、购物车或询价快捷操作。
- [ ] AC-BUG-008 快捷筛选覆盖品牌、类目、规格，选中态使用品牌金边框与浅金背景。
- [ ] AC-BUG-009 完整筛选抽屉按 `04-search-filter.html` 覆盖页面约 72%，遮罩约 62%，包含品牌、类目、规格和价格区间，并支持重置和确认。
- [ ] AC-BUG-010 筛选确认按钮展示应用筛选后的结果数量，筛选项和数量基于当前搜索结果动态聚合。
- [ ] AC-BUG-011 无结果页按 `05-search-empty.html` 展示当前关键词、搜索图标、调整建议列表和推荐搜索词，不展示联系商家、提交找砖、购物车、询价或在线下单入口。
- [ ] AC-BUG-012 搜索首页、联想态、加载态、结果态、筛选态、失败态和无结果态切换时无明显布局跳动、内容重叠或底部操作遮挡。
- [ ] AC-BUG-013 补充小程序静态或单元测试，覆盖搜索通用组件应用、综合分区渲染、品牌/类目/规格快捷筛选、价格区间筛选和无结果结构。
- [ ] AC-BUG-014 更新 `add-miniapp-search-component` 或后续修复 Change 的验收证据，明确对照 REQ-0046 的 5 个 HTML/PNG 原型完成复核。

## 验收证据要求

| 类型 | 要求 |
|---|---|
| 代码结构 | 搜索页 WXML/WXSS/TS 能对应 5 个原型状态 |
| 静态测试 | 覆盖关键 WXML 结构、事件名称、筛选入口和无结果结构 |
| 原型对照 | 至少逐项对照 `01-search-home` 至 `05-search-empty` |
| 文档追溯 | BUG、REQ-0046、修复 Change 和 Sprint 状态同步一致 |

## 非目标

- 本 BUG 不要求新增管理端搜索配置中心。
- 本 BUG 不要求新增后台热门词、同义词或自然语言搜索管理能力。
- 本 BUG 不要求改变搜索 API 的公开状态过滤、安全校验或埋点敏感字段策略，除非修复过程中发现接口契约实际不满足 AC。
